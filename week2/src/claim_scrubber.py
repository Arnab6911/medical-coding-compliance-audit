"""Claim Scrubber and Pre-Submission Validation Engine for Week 2.

Audits professional medical claims prior to clearinghouse submission (EDI 837P).
Flags fatal defects and warnings across:
1. Patient Demographics & Intake Information
2. Insurance Policy Numbers and Payer Identifiers
3. Provider Signature Authentication
4. ICD-10 and CPT Reference Validity
5. Clinical Documentation Substantiation
6. Medical Necessity Indications
7. Duplicate Service Lines
8. Managed Care Referral & Authorization Requirements
"""

from typing import List, Tuple

from .models import Claim, ClaimStatus, ScrubberError, BillingStage
from .coding_engine import CodingEngine


class ClaimScrubber:
    """Automated claim scrubbing engine validating claims against billing and compliance rules."""

    def __init__(self, coding_engine: CodingEngine):
        self.coding_engine = coding_engine

    def scrub_claim(self, claim: Claim) -> List[ScrubberError]:
        """Perform comprehensive pre-submission claim scrub.

        Populates and returns claim.scrubber_errors and updates claim_status.
        """
        errors: List[ScrubberError] = []

        # ---------------------------------------------------------------------
        # 1. Patient Demographics Check
        # ---------------------------------------------------------------------
        if not claim.patient.name or claim.patient.name.strip() in ["", "UNKNOWN"]:
            errors.append(
                ScrubberError(
                    code="SCRUB-01",
                    category="Patient Demographics",
                    description="Patient name is missing or unpopulated in master index.",
                    severity="Fatal",
                    recommended_fix="Update patient full legal name in EHR registration."
                )
            )

        if not claim.patient.age or claim.patient.age <= 0:
            errors.append(
                ScrubberError(
                    code="SCRUB-02",
                    category="Patient Demographics",
                    description="Patient age or date of birth is invalid or unpopulated.",
                    severity="Fatal",
                    recommended_fix="Verify and record patient date of birth."
                )
            )

        # ---------------------------------------------------------------------
        # 2. Insurance Verification Check
        # ---------------------------------------------------------------------
        if claim.policy.plan_type != "Self-Pay":
            if not claim.policy.policy_number or claim.policy.policy_number.strip() == "":
                errors.append(
                    ScrubberError(
                        code="SCRUB-03",
                        category="Insurance Eligibility",
                        description="Subscriber insurance policy/member ID is missing.",
                        severity="Fatal",
                        recommended_fix="Request active insurance card copy from patient and input valid Policy ID."
                    )
                )

            if not claim.policy.payer_id or claim.policy.payer_id.strip() == "":
                errors.append(
                    ScrubberError(
                        code="SCRUB-04",
                        category="Insurance Eligibility",
                        description="Payer electronic routing ID is unpopulated.",
                        severity="Fatal",
                        recommended_fix="Assign valid clearinghouse Payer ID for electronic submission."
                    )
                )

            # HMO Referral Check
            if claim.policy.requires_referral and not claim.policy.has_referral:
                errors.append(
                    ScrubberError(
                        code="SCRUB-05",
                        category="Managed Care Compliance",
                        description="HMO policy requires primary care physician (PCP) referral, but no referral is on file.",
                        severity="Fatal",
                        recommended_fix="Obtain retroactive PCP referral number prior to claim submission."
                    )
                )

        # ---------------------------------------------------------------------
        # 3. Clinician Authentication Check
        # ---------------------------------------------------------------------
        if not claim.provider_signature_valid:
            errors.append(
                ScrubberError(
                    code="SCRUB-06",
                    category="Provider Authentication",
                    description="Clinical encounter documentation lacks authenticated clinician electronic signature.",
                    severity="Fatal",
                    recommended_fix="Route encounter chart back to attending provider for electronic signature."
                )
            )

        # ---------------------------------------------------------------------
        # 4. Diagnostic & Procedural Code Validation
        # ---------------------------------------------------------------------
        if not claim.icd10_diagnoses or len(claim.icd10_diagnoses) == 0:
            errors.append(
                ScrubberError(
                    code="SCRUB-07",
                    category="Coding Compliance",
                    description="Encounter has no primary ICD-10-CM diagnosis code assigned.",
                    severity="Fatal",
                    recommended_fix="Assign validated primary ICD-10-CM code matching clinical diagnosis."
                )
            )
        else:
            for icd in claim.icd10_diagnoses:
                entry = self.coding_engine.get_icd10_entry(icd)
                if not entry:
                    errors.append(
                        ScrubberError(
                            code="SCRUB-08",
                            category="Coding Compliance",
                            description=f"Assigned diagnosis code [{icd}] is unverified in active FY2024 educational subset.",
                            severity="Fatal",
                            recommended_fix=f"Verify ICD-10 code [{icd}] in official CMS tabular index."
                        )
                    )

        if not claim.lines or len(claim.lines) == 0:
            errors.append(
                ScrubberError(
                    code="SCRUB-09",
                    category="Coding Compliance",
                    description="Claim contains zero billable CPT procedure or E/M service lines.",
                    severity="Fatal",
                    recommended_fix="Capture billable CPT codes substantiated by clinical notes."
                )
            )
        else:
            # Check for duplicate CPT lines
            seen_cpts = set()
            for line in claim.lines:
                cpt = line.cpt_code
                if cpt in seen_cpts:
                    errors.append(
                        ScrubberError(
                            code="SCRUB-10",
                            category="Duplicate Billing",
                            description=f"CPT code [{cpt}] is billed multiple times on the same date of service without modifier.",
                            severity="Fatal",
                            recommended_fix=f"Append appropriate CPT modifier (e.g. 76 or 59) or remove duplicate line item."
                        )
                    )
                seen_cpts.add(cpt)

                # Check documentation support for invasive/diagnostic CPT
                cpt_entry = self.coding_engine.get_cpt_entry(cpt)
                if cpt_entry:
                    if cpt_entry.get("requires_procedure_note", False):
                        notes_lower = (claim.clinical_documentation or "").lower()
                        kws = cpt_entry.get("keywords", [])
                        has_mention = any(kw.lower() in notes_lower for kw in kws)
                        if not has_mention:
                            errors.append(
                                ScrubberError(
                                    code="SCRUB-11",
                                    category="Documentation Deficiency",
                                    description=(
                                        f"CPT [{cpt} - {cpt_entry.get('description', '')}] requires procedure/imaging report, "
                                        f"but clinical notes contain no record of performance."
                                    ),
                                    severity="Fatal",
                                    recommended_fix="Locate and append signed procedure report or remove unperformed CPT."
                                )
                            )

                # Check High-Level E/M Substantiation
                if cpt in ["99215", "99205"]:
                    words = len((claim.clinical_documentation or "").split())
                    if words < 15 or "refilled" in (claim.clinical_documentation or "").lower():
                        errors.append(
                            ScrubberError(
                                code="SCRUB-12",
                                category="Medical Necessity / Overcoding",
                                description=(
                                    f"Level 5 E/M CPT [{cpt}] is billed, but clinical documentation is terse ({words} words). "
                                    f"Fails to substantiate high Medical Decision Making complexity."
                                ),
                                severity="Warning",
                                recommended_fix="Downcode to Level 3 (99213) or request detailed physician MDM addendum."
                            )
                        )

        # ---------------------------------------------------------------------
        # Final Status Assignment
        # ---------------------------------------------------------------------
        claim.scrubber_errors = errors
        fatal_count = sum(1 for e in errors if e.severity == "Fatal")

        if fatal_count > 0:
            claim.claim_status = ClaimStatus.SCRUBBER_ERROR
        else:
            claim.claim_status = ClaimStatus.SCRUBBER_CLEAN

        claim.stage = BillingStage.SCRUBBED
        return errors
