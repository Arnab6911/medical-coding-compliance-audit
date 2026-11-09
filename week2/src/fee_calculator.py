"""Fee Calculator and Financial Adjudication Module for Week 2.

Implements transparent, reproducible billing calculations for:
- Chargemaster Gross Charges
- Payer Contracted Allowed Amounts
- Contractual Adjustments / Write-Offs
- Patient Deductible Application
- Copayment Deductions
- Coinsurance Allocations
- Insurance Net Remittance
- Patient Remaining Balance

Strictly enforces the foundational medical billing identity:
Total Billed Amount = Allowed Amount + Contractual Adjustment
Allowed Amount = Insurance Payment + Patient Responsibility (Deductible + Copay + Coinsurance)
Zero double-counting of deductible, copay, and coinsurance.
"""

import json
import os
from typing import Dict, List, Optional, Tuple, Any

from .models import ClaimLine, InsurancePolicy


class FeeCalculator:
    """Manages Chargemaster pricing, payer fee schedules, and patient cost-sharing allocations."""

    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(base_dir, "data")

        self.data_dir = data_dir
        self.fee_schedule = self._load_json("fee_schedule.json")
        self.insurance_plans = self._load_json("insurance_plans.json")

    def _load_json(self, filename: str) -> Dict[str, Any]:
        path = os.path.join(self.data_dir, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def get_cpt_pricing(self, cpt_code: str, payer_id: str = "DEFAULT") -> Tuple[float, float, str]:
        """Retrieve Gross Charge, Payer Allowed Amount, and CPT description.

        Returns:
            Tuple of (gross_charge, allowed_amount, description)
        """
        clean_cpt = cpt_code.strip()
        item = self.fee_schedule.get("items", {}).get(clean_cpt, {})
        if not item:
            # Fallback for unlisted CPT
            return (150.00, 100.00, f"Unlisted Outpatient Service ({clean_cpt})")

        gross_charge = float(item.get("gross_charge", 150.00))
        allowed_map = item.get("allowed_amounts", {})
        allowed_amount = float(allowed_map.get(payer_id, allowed_map.get("DEFAULT", 100.00)))
        description = item.get("description", f"CPT {clean_cpt}")

        return (gross_charge, allowed_amount, description)

    def calculate_claim_line_financials(
        self,
        cpt_code: str,
        policy: InsurancePolicy,
        current_deductible_remaining: float,
        is_first_copay_eligible_line: bool = True,
        is_downcoded: bool = False,
        downcode_to_cpt: str = "99213"
    ) -> Tuple[ClaimLine, float]:
        """Perform line-by-line financial calculation and return ClaimLine and updated remaining deductible.

        Guarantees that:
        1. contractual_adjustment = gross_charge - allowed_amount
        2. allowed_amount = insurance_paid + patient_responsibility
        3. patient_responsibility = copay_applied + deductible_applied + coinsurance_applied
        """
        effective_cpt = downcode_to_cpt if is_downcoded else cpt_code
        gross_charge, allowed_amount, description = self.get_cpt_pricing(effective_cpt, policy.payer_id)

        # If line was downcoded, gross charge billed reflects original CPT, but allowed amount reflects downcoded rate
        if is_downcoded and effective_cpt != cpt_code:
            orig_gross, _, orig_desc = self.get_cpt_pricing(cpt_code, policy.payer_id)
            gross_charge = orig_gross
            description = f"{orig_desc} [Downcoded to {effective_cpt} by Payer]"

        contractual_adjustment = round(max(0.0, gross_charge - allowed_amount), 2)

        # ---------------------------------------------------------------------
        # Case A: Self-Pay (Uninsured)
        # ---------------------------------------------------------------------
        if policy.plan_type == "Self-Pay":
            discount_rate = policy.self_pay_discount_rate if policy.self_pay_discount_rate > 0 else 0.30
            discount_amount = round(gross_charge * discount_rate, 2)
            patient_due = round(gross_charge - discount_amount, 2)

            line = ClaimLine(
                line_number=1,
                cpt_code=cpt_code,
                cpt_description=description,
                diagnosis_pointers=["1"],
                gross_charge=gross_charge,
                allowed_amount=patient_due,
                contractual_adjustment=discount_amount,
                deductible_applied=0.00,
                copay_applied=0.00,
                coinsurance_applied=0.00,
                insurance_paid=0.00,
                patient_responsibility=patient_due,
                carc_code="SELF-PAY",
                carc_description="30% Prompt-Pay Financial Assistance Discount Applied",
                line_status="Self-Pay Due"
            )
            return (line, current_deductible_remaining)

        # ---------------------------------------------------------------------
        # Case B: ACA Mandated Preventive Service (CPT 99396 / screening)
        # ---------------------------------------------------------------------
        if cpt_code in ["99396", "G0438", "G0439"]:
            line = ClaimLine(
                line_number=1,
                cpt_code=cpt_code,
                cpt_description=description,
                diagnosis_pointers=["1"],
                gross_charge=gross_charge,
                allowed_amount=allowed_amount,
                contractual_adjustment=contractual_adjustment,
                deductible_applied=0.00,
                copay_applied=0.00,
                coinsurance_applied=0.00,
                insurance_paid=allowed_amount,
                patient_responsibility=0.00,
                carc_code="CARC 45",
                carc_description="Contractual Adjustment (ACA 100% Preventive Coverage)",
                line_status="Paid in Full"
            )
            return (line, current_deductible_remaining)

        # ---------------------------------------------------------------------
        # Case C: Standard Insured Medical Service (PPO, POS, HMO, Medicare, HDHP)
        # ---------------------------------------------------------------------
        # 1. Copay Allocation (applied only once per encounter on the primary E/M line)
        copay_applied = 0.00
        if is_first_copay_eligible_line and policy.copay_amount > 0:
            copay_applied = min(policy.copay_amount, allowed_amount)

        rem_after_copay = round(max(0.0, allowed_amount - copay_applied), 2)

        # 2. Deductible Allocation (applies to allowed amount remaining after copay)
        deductible_applied = 0.00
        if current_deductible_remaining > 0 and rem_after_copay > 0:
            deductible_applied = min(current_deductible_remaining, rem_after_copay)
            current_deductible_remaining = round(current_deductible_remaining - deductible_applied, 2)

        rem_after_deductible = round(max(0.0, rem_after_copay - deductible_applied), 2)

        # 3. Coinsurance Allocation (applies to remainder after copay and deductible)
        coinsurance_applied = 0.00
        if rem_after_deductible > 0 and policy.coinsurance_rate > 0:
            coinsurance_applied = round(rem_after_deductible * policy.coinsurance_rate, 2)

        # 4. Insurance Payment = Remainder after patient coinsurance
        insurance_paid = round(rem_after_deductible - coinsurance_applied, 2)

        # 5. Patient Responsibility
        patient_responsibility = round(copay_applied + deductible_applied + coinsurance_applied, 2)

        # 6. Reconciliation Guard: Guarantee insurance_paid + patient_responsibility == allowed_amount exactly
        delta = round(allowed_amount - (insurance_paid + patient_responsibility), 2)
        if delta != 0.0:
            insurance_paid = round(insurance_paid + delta, 2)

        carc_notes = []
        if contractual_adjustment > 0:
            carc_notes.append("CARC 45: Contractual Write-off")
        if deductible_applied > 0:
            carc_notes.append(f"CARC 1: Deductible (${deductible_applied:.2f})")
        if copay_applied > 0:
            carc_notes.append(f"CARC 3: Copayment (${copay_applied:.2f})")
        if coinsurance_applied > 0:
            carc_notes.append(f"CARC 2: Coinsurance (${coinsurance_applied:.2f})")

        carc_str = "; ".join(carc_notes) if carc_notes else "Clean Adjudication"

        line = ClaimLine(
            line_number=1,
            cpt_code=cpt_code,
            cpt_description=description,
            diagnosis_pointers=["1"],
            gross_charge=gross_charge,
            allowed_amount=allowed_amount,
            contractual_adjustment=contractual_adjustment,
            deductible_applied=deductible_applied,
            copay_applied=copay_applied,
            coinsurance_applied=coinsurance_applied,
            insurance_paid=insurance_paid,
            patient_responsibility=patient_responsibility,
            carc_code="CARC 45" if contractual_adjustment > 0 else "PAID",
            carc_description=carc_str,
            line_status="Paid" if insurance_paid > 0 else "Patient Responsibility"
        )

        return (line, current_deductible_remaining)
