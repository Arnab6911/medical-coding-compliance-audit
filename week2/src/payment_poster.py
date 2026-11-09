"""Payment Posting and Provider Accounts Receivable Ledger Module for Week 2.

Handles Electronic Remittance Advice (ERA 835) payment posting into practice management ledger:
1. Posts Contractual Adjustments / Write-Offs (CARC 45).
2. Posts Payer Electronic Funds Transfer (EFT) / Check Payments.
3. Automatically posts secondary/patient billing responsibility.
4. Generates immutable ledger transaction records with audit traces.
"""

from datetime import datetime
from typing import List, Optional

from .models import Claim, PaymentPosting, BillingStage, ClaimStatus


class PaymentPoster:
    """Manages payment posting and ledger transactions."""

    def post_remittance(self, claim: Claim) -> Optional[PaymentPosting]:
        """Post adjudicated claim payment and contractual write-offs to practice ledger.

        Returns PaymentPosting ledger record or None if claim was rejected.
        """
        if claim.claim_status == ClaimStatus.REJECTED:
            # Rejected claims cannot be posted to receivables until corrected and re-adjudicated
            return None

        claim.stage = BillingStage.PAYMENT_POSTED

        eft_trace = f"EFT-{claim.policy.payer_id}-{claim.encounter_id[-4:]}-835"
        posting_id = f"POST-{claim.encounter_id[-4:]}"

        ledger_notes = (
            f"Posted via Payer Remittance {claim.remittance_number}. "
            f"Total Gross: ${claim.total_gross_charge:.2f} | "
            f"Contractual Write-Off: ${claim.total_contractual_adjustment:.2f} | "
            f"Denied: ${claim.total_denied_amount:.2f} | "
            f"Ins. Paid: ${claim.total_insurance_paid:.2f} | "
            f"Pt. Due: ${claim.total_patient_responsibility:.2f}."
        )

        posting = PaymentPosting(
            posting_id=posting_id,
            claim_id=claim.claim_id,
            encounter_id=claim.encounter_id,
            patient_id=claim.patient.patient_id,
            patient_name=claim.patient.name,
            date_posted=datetime.now().strftime("%Y-%m-%d"),
            payer_paid_amount=claim.total_insurance_paid,
            contractual_write_off=claim.total_contractual_adjustment,
            denied_amount=claim.total_denied_amount,
            patient_responsibility=claim.total_patient_responsibility,
            check_eft_trace=eft_trace,
            remittance_status=claim.claim_status.value,
            ledger_notes=ledger_notes
        )

        return posting
