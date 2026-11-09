"""End-to-End Medical Billing Simulation Pipeline Controller for Week 2.

Coordinates the 12-stage medical billing lifecycle across a cohort of patient encounters:
1. Patient Registration & Verification
2. Insurance Benefit Parsing
3. Documentation & Medical Coding
4. Charge Capture & Chargemaster Pricing
5. Claim Scrubbing & Validation
6. Electronic Claim Submission (EDI 837P)
7. Payer Adjudication (EDI 835 Remittance)
8. Payment & Write-Off Posting
9. Patient Invoice & Statement Generation
10. Aggregated Financial & Operational Metrics Computation
"""

import os
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any

from .models import (
    Claim, ClaimLine, Patient, InsurancePolicy, ClaimStatus, BillingStage,
    PaymentPosting, PatientInvoice, SimulationBatchMetrics
)
from .coding_engine import CodingEngine
from .fee_calculator import FeeCalculator
from .claim_scrubber import ClaimScrubber
from .adjudication_engine import AdjudicationEngine
from .payment_poster import PaymentPoster
from .invoice_generator import InvoiceGenerator


class BillingSimulationPipeline:
    """Orchestrates end-to-end billing simulation for all patient encounters."""

    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(base_dir, "data")

        self.data_dir = data_dir
        self.coding_engine = CodingEngine()
        self.fee_calculator = FeeCalculator(data_dir=data_dir)
        self.scrubber = ClaimScrubber(self.coding_engine)
        self.adjudicator = AdjudicationEngine(self.fee_calculator)
        self.payment_poster = PaymentPoster()
        self.invoice_generator = InvoiceGenerator()

    def load_encounters_from_csv(self, csv_path: Optional[str] = None) -> List[Dict[str, Any]]:
        """Parse encounter records from CSV file."""
        if csv_path is None:
            csv_path = os.path.join(self.data_dir, "encounters_week2.csv")

        df = pd.read_csv(csv_path)
        # Fill NaNs with clean defaults
        df = df.fillna({
            "policy_number": "",
            "group_number": "",
            "deductible_remaining": 0.0,
            "copay_amount": 0.0,
            "has_provider_signature": True,
            "has_prior_authorization": True,
            "has_referral": True
        })
        return df.to_dict(orient="records")

    def build_claim_from_record(self, record: Dict[str, Any]) -> Claim:
        """Construct initial Claim instance from parsed encounter dictionary."""
        patient = Patient(
            patient_id=str(record.get("patient_id", "UNKNOWN")),
            name=str(record.get("patient_name", "Unknown Patient")),
            age=int(record.get("patient_age", 50)),
            gender=str(record.get("patient_gender", "Unknown"))
        )

        plan_key = str(record.get("insurance_provider", "BCBS_PPO"))
        plan_def = self.fee_calculator.insurance_plans.get("plans", {}).get(plan_key, {})

        # Parse boolean fields safely
        def to_bool(val: Any) -> bool:
            if isinstance(val, bool):
                return val
            return str(val).strip().lower() in ["true", "1", "yes"]

        policy = InsurancePolicy(
            payer_id=str(plan_def.get("payer_id", "DEFAULT")),
            payer_name=str(plan_def.get("payer_name", plan_key)),
            plan_name=str(plan_def.get("plan_name", "Standard Plan")),
            plan_type=str(plan_def.get("plan_type", "PPO")),
            policy_number=str(record.get("policy_number", "")),
            group_number=str(record.get("group_number", "")),
            copay_amount=float(record.get("copay_amount", plan_def.get("copay_pcp", 30.00))),
            deductible_remaining=float(record.get("deductible_remaining", 0.00)),
            coinsurance_rate=float(plan_def.get("coinsurance_rate", 0.20)),
            oop_max=float(plan_def.get("oop_max", 4000.00)),
            self_pay_discount_rate=float(plan_def.get("self_pay_discount_rate", 0.00)),
            requires_referral=bool(plan_def.get("requires_referral", False)),
            has_referral=to_bool(record.get("has_referral", True)),
            has_prior_authorization=to_bool(record.get("has_prior_authorization", True))
        )

        icd_str = str(record.get("assigned_icd10", ""))
        icd_list = [c.strip() for c in icd_str.split(";") if c.strip()]

        cpt_str = str(record.get("assigned_cpt", ""))
        cpt_list = [c.strip() for c in cpt_str.split(";") if c.strip()]

        # Generate initial unadjudicated claim lines with Chargemaster gross pricing
        lines: List[ClaimLine] = []
        for idx, cpt in enumerate(cpt_list, start=1):
            gross, allowed, desc = self.fee_calculator.get_cpt_pricing(cpt, policy.payer_id)
            lines.append(
                ClaimLine(
                    line_number=idx,
                    cpt_code=cpt,
                    cpt_description=desc,
                    diagnosis_pointers=["1"],
                    gross_charge=gross,
                    allowed_amount=allowed,
                    contractual_adjustment=round(gross - allowed, 2),
                    line_status="Initial Charge Captured"
                )
            )

        claim = Claim(
            claim_id=f"CLM-{record.get('encounter_id', '0000')[-4:]}",
            encounter_id=str(record.get("encounter_id", "UNKNOWN")),
            patient=patient,
            policy=policy,
            date_of_service=str(record.get("encounter_date", "2024-04-01")),
            icd10_diagnoses=icd_list,
            chief_complaint=str(record.get("chief_complaint", "")),
            clinical_documentation=str(record.get("clinical_documentation", "")),
            provider_signature_valid=to_bool(record.get("has_provider_signature", True)),
            lines=lines,
            stage=BillingStage.CHARGE_CAPTURED
        )

        return claim

    def run_simulation(
        self,
        csv_path: Optional[str] = None
    ) -> Tuple[List[Claim], List[PaymentPosting], List[PatientInvoice], SimulationBatchMetrics]:
        """Execute end-to-end simulation across all encounters.

        Returns:
            Tuple of (claims, postings, invoices, metrics)
        """
        records = self.load_encounters_from_csv(csv_path)
        claims: List[Claim] = []
        postings: List[PaymentPosting] = []
        invoices: List[PatientInvoice] = []

        for rec in records:
            # 1. Build & Charge Capture
            claim = self.build_claim_from_record(rec)

            # 2. Scrub Claim
            self.scrubber.scrub_claim(claim)

            # 3. Simulate Submission (if not rejected at front-end)
            if claim.claim_status != ClaimStatus.SCRUBBER_ERROR:
                claim.stage = BillingStage.SUBMITTED

            # 4. Adjudicate
            self.adjudicator.adjudicate_claim(claim)

            # 5. Payment Posting
            posting = self.payment_poster.post_remittance(claim)
            if posting:
                postings.append(posting)

            # 6. Patient Invoice Generation
            invoice = self.invoice_generator.generate_invoice(claim)
            invoices.append(invoice)
            self.invoice_generator.export_invoice_text(invoice)

            claims.append(claim)

        # Compute Aggregated Batch Metrics
        metrics = self._calculate_metrics(claims)
        return (claims, postings, invoices, metrics)

    def _calculate_metrics(self, claims: List[Claim]) -> SimulationBatchMetrics:
        """Aggregate financial and performance metrics across the cohort."""
        total_enc = len(claims)
        clean_count = sum(1 for c in claims if not any(e.severity == "Fatal" for e in c.scrubber_errors))
        scrub_errors_count = sum(1 for c in claims if any(e.severity == "Fatal" for e in c.scrubber_errors))

        paid_count = sum(1 for c in claims if c.claim_status in [ClaimStatus.ADJUDICATED_BALANCE_DUE, ClaimStatus.ADJUDICATED_SETTLED, ClaimStatus.PAID])
        part_count = sum(1 for c in claims if c.claim_status == ClaimStatus.PARTIALLY_PAID)
        denied_count = sum(1 for c in claims if c.claim_status == ClaimStatus.DENIED)
        rejected_count = sum(1 for c in claims if c.claim_status == ClaimStatus.REJECTED)

        total_gross = sum(c.total_gross_charge for c in claims)
        adjudicated_gross = sum(c.total_gross_charge for c in claims if c.claim_status != ClaimStatus.REJECTED)
        rejected_charges = sum(c.total_gross_charge for c in claims if c.claim_status == ClaimStatus.REJECTED)
        total_allowed = sum(c.total_allowed_amount for c in claims)
        total_adj = sum(c.total_contractual_adjustment for c in claims)
        total_denied = sum(c.total_denied_amount for c in claims)
        total_ins_paid = sum(c.total_insurance_paid for c in claims)
        total_pt_resp = sum(c.total_patient_responsibility for c in claims)
        total_ded = sum(c.total_deductible for c in claims)
        total_copay = sum(c.total_copay for c in claims)
        total_coins = sum(c.total_coinsurance for c in claims)
        total_self_pay = sum(c.total_patient_responsibility for c in claims if c.policy.plan_type == "Self-Pay")

        return SimulationBatchMetrics(
            total_encounters=total_enc,
            clean_claims_count=clean_count,
            scrubber_errors_count=scrub_errors_count,
            claims_paid_count=paid_count,
            claims_partially_paid_count=part_count,
            claims_denied_count=denied_count,
            claims_rejected_count=rejected_count,
            total_gross_billed=round(total_gross, 2),
            total_adjudicated_gross=round(adjudicated_gross, 2),
            total_rejected_charges=round(rejected_charges, 2),
            total_allowed=round(total_allowed, 2),
            total_contractual_adjustments=round(total_adj, 2),
            total_denied_charges=round(total_denied, 2),
            total_insurance_payments=round(total_ins_paid, 2),
            total_patient_responsibility=round(total_pt_resp, 2),
            total_deductible_collected=round(total_ded, 2),
            total_copay_collected=round(total_copay, 2),
            total_coinsurance_collected=round(total_coins, 2),
            total_self_pay=round(total_self_pay, 2)
        )


    def export_results_csv(self, claims: List[Claim], output_path: str) -> str:
        """Export tabular summary of all claims and financial calculations to CSV."""
        rows = [c.to_summary_dict() for c in claims]
        df = pd.DataFrame(rows)
        df.to_csv(output_path, index=False)
        return output_path
