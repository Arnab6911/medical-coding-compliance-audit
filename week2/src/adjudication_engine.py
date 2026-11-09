"""Claim Adjudication Simulation Engine for Week 2.

Simulates payer Electronic Remittance Advice (ERA 835) adjudication processing.
Evaluates submitted claims and determines outcomes:
1. ACCEPTED / PAID IN FULL: Clean covered services with contractual fee schedule reimbursement.
2. PARTIALLY PAID / DOWNCODED: Downcoded E/M services or duplicate line partial denials.
3. DENIED: Medical necessity failure (CARC 50), missing authorization/referral (CARC 197).
4. REJECTED: Front-end clearinghouse/payer 277CA rejection for missing subscriber ID or unsigned notes (CARC 16).

All simulation decisions are transparently annotated with standard CARC/RARC codes.
Educational Disclosure: Simulated payer decisions are educational models and do not represent real insurer decisions.
"""

from datetime import datetime
from typing import List

from .models import Claim, ClaimLine, ClaimStatus, BillingStage
from .fee_calculator import FeeCalculator


class AdjudicationEngine:
    """Simulates payer adjudication and remittance advice generation."""

    def __init__(self, fee_calculator: FeeCalculator):
        self.fee_calculator = fee_calculator

    def adjudicate_claim(self, claim: Claim) -> Claim:
        """Process claim through payer adjudication rules engine and calculate net financial settlements."""
        claim.stage = BillingStage.ADJUDICATED
        claim.remittance_number = f"ERA-{claim.encounter_id[-4:]}-2024"

        # ---------------------------------------------------------------------
        # 1. Check for Pre-Submission Scrubber Errors (Clearinghouse / 277CA Rejection)
        # ---------------------------------------------------------------------
        fatal_errors = [e for e in claim.scrubber_errors if e.severity == "Fatal"]
        has_unauthenticated_note = any(e.code == "SCRUB-06" for e in fatal_errors)
        has_missing_policy = any(e.code == "SCRUB-03" for e in fatal_errors)

        if has_missing_policy or has_unauthenticated_note:
            claim.claim_status = ClaimStatus.REJECTED
            reasons = []
            if has_missing_policy:
                reasons.append("Missing Subscriber Policy Number (EDI 277CA Status Category A7; Mapped to CARC 16)")
            if has_unauthenticated_note:
                reasons.append("Unauthenticated Clinical Progress Note (EDI 277CA Status Category A7; Mapped to CARC 16)")

            claim.adjudication_reason = (
                f"EDI 277CA Gateway Rejection: Claim halted at clearinghouse pre-adjudication gateway. "
                f"Reason(s): {', '.join(reasons)}. Re-submission required via corrected EDI 837P."
            )
            # Rejection means claim did not adjudicate: $0 allowed, $0 paid, $0 patient due from insurance yet
            for line in claim.lines:
                line.allowed_amount = 0.00
                line.contractual_adjustment = 0.00
                line.denied_amount = 0.00
                line.insurance_paid = 0.00
                line.patient_responsibility = 0.00
                line.carc_code = "EDI 277CA: A7 (CARC 16)"
                line.carc_description = "Pre-adjudication clearinghouse rejection for missing/invalid required data."
                line.line_status = "Rejected (Pre-Adjudication)"
            return claim

        # ---------------------------------------------------------------------
        # 2. Check for Missing HMO Specialist Referral
        # ---------------------------------------------------------------------
        if claim.policy.requires_referral and not claim.policy.has_referral:
            claim.claim_status = ClaimStatus.DENIED
            claim.adjudication_reason = (
                "EDI 835 Remittance Claim Denial: Patient attended specialist clinic without required Primary Care Physician (PCP) "
                "referral on file (CARC 197: Pre-certification/authorization/referral absent; RARC N381). Administrative review required."
            )
            for line in claim.lines:
                line.allowed_amount = 0.00
                line.contractual_adjustment = 0.00
                line.denied_amount = line.gross_charge  # Non-covered service / denial
                line.insurance_paid = 0.00
                line.patient_responsibility = 0.00  # Patient protected by managed care in-network hold
                line.carc_code = "CARC 197"
                line.carc_description = "Precertification / authorization / referral absent. Service not covered; provider hold."
                line.rarc_code = "N381"
                line.line_status = "Denied (Missing Referral)"
            return claim

        # ---------------------------------------------------------------------
        # 3. Check for Medical Necessity Failure (e.g. Colonoscopy for Sore Throat)
        # ---------------------------------------------------------------------
        has_missing_proc_doc = any(e.code == "SCRUB-11" for e in fatal_errors)
        if has_missing_proc_doc:
            claim.claim_status = ClaimStatus.DENIED
            claim.adjudication_reason = (
                "EDI 835 Remittance Claim Denial: Reported procedural service lacks clinical indication and authentic procedure report "
                "in submitted documentation (CARC 50: Non-covered services because not deemed a medical necessity). Clinical review required."
            )
            for line in claim.lines:
                line.allowed_amount = 0.00
                line.contractual_adjustment = 0.00
                line.denied_amount = line.gross_charge  # Non-covered service / denial
                line.insurance_paid = 0.00
                line.patient_responsibility = 0.00  # Provider liability under in-network contract
                line.carc_code = "CARC 50"
                line.carc_description = "Non-covered service: medical necessity not established by documentation."
                line.line_status = "Denied (Medical Necessity)"
            return claim

        # ---------------------------------------------------------------------
        # 4. Check for High E/M Downcoding (e.g. 99215 with 4-word note)
        # ---------------------------------------------------------------------
        has_em_warning = any(e.code == "SCRUB-12" for e in claim.scrubber_errors)
        is_downcoded = False
        if has_em_warning and any(l.cpt_code == "99215" for l in claim.lines):
            is_downcoded = True
            claim.claim_status = ClaimStatus.PARTIALLY_PAID
            claim.adjudication_reason = (
                "EDI 835 Remittance Medical Review Downcode: Level 5 E/M (99215) downcoded to Level 3 (99213) due to insufficient "
                "Medical Decision Making (MDM) complexity in clinical note (CARC 150: Payer deems information does not "
                "support this level of service; CARC 45: Contractual adjustment applied)."
            )

        # ---------------------------------------------------------------------
        # 5. Check for Duplicate Line Items (e.g. Two 99214 lines on same claim)
        # ---------------------------------------------------------------------
        has_duplicate_error = any(e.code == "SCRUB-10" for e in claim.scrubber_errors)
        if has_duplicate_error:
            claim.claim_status = ClaimStatus.PARTIALLY_PAID
            claim.adjudication_reason = (
                "EDI 835 Remittance Partial Payment: Primary service line approved and paid; duplicate line item denied "
                "under CMS NCCI duplication policy (CARC 18: Exact duplicate service)."
            )


        # ---------------------------------------------------------------------
        # 6. Adjudicate Service Lines Financials
        # ---------------------------------------------------------------------
        cur_deductible = claim.policy.deductible_remaining
        adjudicated_lines: List[ClaimLine] = []
        seen_cpts = set()
        first_copay_eligible = True

        for idx, line in enumerate(claim.lines, start=1):
            cpt = line.cpt_code

            # Handle duplicate line denial
            if cpt in seen_cpts and has_duplicate_error:
                denied_line = ClaimLine(
                    line_number=idx,
                    cpt_code=cpt,
                    cpt_description=f"{line.cpt_description} [Duplicate Entry]",
                    diagnosis_pointers=line.diagnosis_pointers,
                    gross_charge=line.gross_charge,
                    allowed_amount=0.00,
                    contractual_adjustment=0.00,
                    denied_amount=line.gross_charge,  # Denied duplicate service
                    deductible_applied=0.00,
                    copay_applied=0.00,
                    coinsurance_applied=0.00,
                    insurance_paid=0.00,
                    patient_responsibility=0.00,
                    carc_code="CARC 18",
                    carc_description="Exact duplicate claim/service. Zero payment; denied.",
                    line_status="Denied (Duplicate)"
                )
                adjudicated_lines.append(denied_line)
                continue

            seen_cpts.add(cpt)

            # Handle downcoded E/M line
            line_downcoded = is_downcoded and cpt == "99215"
            calc_line, cur_deductible = self.fee_calculator.calculate_claim_line_financials(
                cpt_code=cpt,
                policy=claim.policy,
                current_deductible_remaining=cur_deductible,
                is_first_copay_eligible_line=first_copay_eligible,
                is_downcoded=line_downcoded,
                downcode_to_cpt="99213"
            )
            calc_line.line_number = idx
            calc_line.diagnosis_pointers = line.diagnosis_pointers

            if line_downcoded:
                calc_line.carc_code = "CARC 150 / CARC 45"
                calc_line.carc_description = "Downcoded from 99215 to 99213 for insufficient MDM complexity; Contractual write-off."

            if calc_line.copay_applied > 0:
                first_copay_eligible = False

            adjudicated_lines.append(calc_line)

        claim.lines = adjudicated_lines

        # If claim wasn't already marked as PARTIALLY_PAID, DENIED, or REJECTED
        if claim.claim_status not in [ClaimStatus.PARTIALLY_PAID, ClaimStatus.DENIED, ClaimStatus.REJECTED]:
            if claim.total_patient_responsibility == 0.0:
                claim.claim_status = ClaimStatus.ADJUDICATED_SETTLED
            else:
                claim.claim_status = ClaimStatus.ADJUDICATED_BALANCE_DUE
            claim.adjudication_reason = (
                "EDI 835 Electronic Remittance Advice: Claim approved and adjudicated according to contracted fee schedule "
                "and member benefit design (CARC 45 Contractual Write-off applied)."
            )

        return claim

