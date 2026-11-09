"""Data models for Week 2: Medical Billing Process Simulation.

Defines strongly-typed dataclasses for all phases of the medical billing lifecycle:
patient registration, insurance verification, coding, charge capture, claim scrubbing,
adjudication, payment posting, and patient invoicing.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Dict, List, Optional, Any


class BillingStage(str, Enum):
    """Lifecycle stages of a medical encounter within the billing simulation."""
    REGISTRATION = "Patient Registration"
    INSURANCE_VERIFIED = "Insurance Verified"
    DOCUMENTATION_REVIEW = "Documentation Review"
    CODED = "Medical Coding"
    CHARGE_CAPTURED = "Charge Capture"
    SCRUBBED = "Claim Scrubbed"
    SUBMITTED = "Claim Submitted"
    ADJUDICATED = "Claim Adjudicated"
    PAYMENT_POSTED = "Payment Posted"
    INVOICED = "Patient Invoiced"
    CLOSED = "Account Closed"


class ClaimStatus(str, Enum):
    """Claim adjudication and account settlement status categories."""
    DRAFT = "Draft"
    SCRUBBER_CLEAN = "Clean (Ready to Submit)"
    SCRUBBER_ERROR = "Scrubber Error (Pre-Submission Hold)"
    SUBMITTED = "Submitted to Payer (EDI 837P)"
    ADJUDICATED_BALANCE_DUE = "Adjudicated – Patient Balance Due"
    ADJUDICATED_SETTLED = "Adjudicated – Fully Settled"
    PARTIALLY_PAID = "Partially Paid – Remaining Balance"
    DENIED = "Denied – Review Required"
    REJECTED = "Rejected – Resubmission Required"

    # Backward compatibility alias
    PAID = "Adjudicated – Patient Balance Due"


class PlanType(str, Enum):
    """Supported insurance plan categories."""
    PPO = "PPO"
    HMO = "HMO"
    POS = "POS"
    MEDICARE = "Medicare"
    HDHP = "HDHP"
    SELF_PAY = "Self-Pay"


@dataclass
class Patient:
    """Fictional patient demographic profile."""
    patient_id: str
    name: str
    age: int
    gender: str
    date_of_birth: str = ""
    phone: str = "555-0100"
    address: str = "100 Medical Center Blvd, Suite 200"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "date_of_birth": self.date_of_birth,
            "phone": self.phone,
            "address": self.address
        }


@dataclass
class InsurancePolicy:
    """Patient insurance coverage details and benefit design."""
    payer_id: str
    payer_name: str
    plan_name: str
    plan_type: str
    policy_number: str
    group_number: str
    copay_amount: float = 0.00
    deductible_remaining: float = 0.00
    coinsurance_rate: float = 0.20
    oop_max: float = 4000.00
    self_pay_discount_rate: float = 0.00
    requires_referral: bool = False
    has_referral: bool = True
    has_prior_authorization: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "payer_id": self.payer_id,
            "payer_name": self.payer_name,
            "plan_name": self.plan_name,
            "plan_type": self.plan_type,
            "policy_number": self.policy_number,
            "group_number": self.group_number,
            "copay_amount": self.copay_amount,
            "deductible_remaining": self.deductible_remaining,
            "coinsurance_rate": self.coinsurance_rate,
            "oop_max": self.oop_max,
            "requires_referral": self.requires_referral,
            "has_referral": self.has_referral
        }


@dataclass
class ScrubberError:
    """Pre-submission claim validation defect identified by claim scrubber."""
    code: str
    category: str
    description: str
    severity: str  # "Fatal" (blocks submission) or "Warning"
    recommended_fix: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "category": self.category,
            "description": self.description,
            "severity": self.severity,
            "recommended_fix": self.recommended_fix
        }


@dataclass
class ClaimLine:
    """Individual service line item billed on a professional claim."""
    line_number: int
    cpt_code: str
    cpt_description: str
    diagnosis_pointers: List[str]
    units: int = 1
    gross_charge: float = 0.00
    allowed_amount: float = 0.00
    contractual_adjustment: float = 0.00
    denied_amount: float = 0.00
    deductible_applied: float = 0.00
    copay_applied: float = 0.00
    coinsurance_applied: float = 0.00
    insurance_paid: float = 0.00
    patient_responsibility: float = 0.00
    carc_code: str = ""
    carc_description: str = ""
    rarc_code: str = ""
    line_status: str = "Pending"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "line_number": self.line_number,
            "cpt_code": self.cpt_code,
            "cpt_description": self.cpt_description,
            "diagnosis_pointers": ", ".join(self.diagnosis_pointers),
            "units": self.units,
            "gross_charge": round(self.gross_charge, 2),
            "allowed_amount": round(self.allowed_amount, 2),
            "contractual_adjustment": round(self.contractual_adjustment, 2),
            "denied_amount": round(self.denied_amount, 2),
            "deductible_applied": round(self.deductible_applied, 2),
            "copay_applied": round(self.copay_applied, 2),
            "coinsurance_applied": round(self.coinsurance_applied, 2),
            "insurance_paid": round(self.insurance_paid, 2),
            "patient_responsibility": round(self.patient_responsibility, 2),
            "carc_code": self.carc_code,
            "carc_description": self.carc_description,
            "line_status": self.line_status
        }


@dataclass
class Claim:
    """Professional medical claim (CMS-1500 / EDI 837P) representation."""
    claim_id: str
    encounter_id: str
    patient: Patient
    policy: InsurancePolicy
    date_of_service: str
    icd10_diagnoses: List[str]
    chief_complaint: str
    clinical_documentation: str
    provider_signature_valid: bool = True
    lines: List[ClaimLine] = field(default_factory=list)
    scrubber_errors: List[ScrubberError] = field(default_factory=list)
    claim_status: ClaimStatus = ClaimStatus.DRAFT
    stage: BillingStage = BillingStage.REGISTRATION
    adjudication_reason: str = ""
    remittance_number: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    @property
    def total_gross_charge(self) -> float:
        return round(sum(ln.gross_charge for ln in self.lines), 2)

    @property
    def total_allowed_amount(self) -> float:
        return round(sum(ln.allowed_amount for ln in self.lines), 2)

    @property
    def total_contractual_adjustment(self) -> float:
        return round(sum(ln.contractual_adjustment for ln in self.lines), 2)

    @property
    def total_denied_amount(self) -> float:
        return round(sum(ln.denied_amount for ln in self.lines), 2)

    @property
    def total_insurance_paid(self) -> float:
        return round(sum(ln.insurance_paid for ln in self.lines), 2)

    @property
    def total_patient_responsibility(self) -> float:
        return round(sum(ln.patient_responsibility for ln in self.lines), 2)

    @property
    def total_deductible(self) -> float:
        return round(sum(ln.deductible_applied for ln in self.lines), 2)

    @property
    def total_copay(self) -> float:
        return round(sum(ln.copay_applied for ln in self.lines), 2)

    @property
    def total_coinsurance(self) -> float:
        return round(sum(ln.coinsurance_applied for ln in self.lines), 2)

    @property
    def adjudication_status(self) -> str:
        """Payer adjudication outcome."""
        if self.claim_status == ClaimStatus.REJECTED:
            return "Rejected (Gateway Hold)"
        elif self.claim_status == ClaimStatus.DENIED:
            return "Denied (Payer Adjudicated)"
        elif self.claim_status == ClaimStatus.PARTIALLY_PAID:
            return "Adjudicated (Downcoded / Partial)"
        elif self.claim_status == ClaimStatus.ADJUDICATED_SETTLED:
            return "Adjudicated (Fully Settled)"
        else:
            return "Adjudicated (Approved / Allowed)"

    @property
    def insurance_payment_status(self) -> str:
        """Third-party insurance payment status."""
        if self.claim_status == ClaimStatus.REJECTED:
            return "Unadjudicated ($0.00)"
        elif self.claim_status == ClaimStatus.DENIED:
            return "Denied ($0.00 Paid)"
        elif self.total_insurance_paid > 0:
            return f"Remitted (${self.total_insurance_paid:.2f})"
        else:
            return "$0.00 Paid (Deductible Absorbed)"

    @property
    def patient_account_status(self) -> str:
        """Patient financial ledger balance status."""
        if self.claim_status in [ClaimStatus.REJECTED, ClaimStatus.DENIED]:
            return "Billing Hold ($0.00 Due)"
        elif self.total_patient_responsibility > 0:
            return f"Patient Balance Due (${self.total_patient_responsibility:.2f})"
        else:
            return "Account Settled ($0.00 Due)"

    def to_summary_dict(self) -> Dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "encounter_id": self.encounter_id,
            "patient_id": self.patient.patient_id,
            "patient_name": self.patient.name,
            "date_of_service": self.date_of_service,
            "payer_name": self.policy.payer_name,
            "plan_type": self.policy.plan_type,
            "claim_status": self.claim_status.value,
            "adjudication_status": self.adjudication_status,
            "insurance_payment_status": self.insurance_payment_status,
            "patient_account_status": self.patient_account_status,
            "billing_stage": self.stage.value,
            "total_gross_charge": self.total_gross_charge,
            "total_allowed_amount": self.total_allowed_amount,
            "total_contractual_adjustment": self.total_contractual_adjustment,
            "total_denied_amount": self.total_denied_amount,
            "total_insurance_paid": self.total_insurance_paid,
            "total_deductible": self.total_deductible,
            "total_copay": self.total_copay,
            "total_coinsurance": self.total_coinsurance,
            "total_patient_responsibility": self.total_patient_responsibility,
            "adjudication_reason": self.adjudication_reason
        }


@dataclass
class PaymentPosting:
    """Payment ledger posting record corresponding to an Electronic Remittance Advice (ERA 835)."""
    posting_id: str
    claim_id: str
    encounter_id: str
    patient_id: str
    patient_name: str
    date_posted: str
    payer_paid_amount: float
    contractual_write_off: float
    denied_amount: float = 0.00
    patient_responsibility: float = 0.00
    check_eft_trace: str = ""
    remittance_status: str = ""
    ledger_notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "posting_id": self.posting_id,
            "claim_id": self.claim_id,
            "encounter_id": self.encounter_id,
            "patient_name": self.patient_name,
            "date_posted": self.date_posted,
            "payer_paid_amount": round(self.payer_paid_amount, 2),
            "contractual_write_off": round(self.contractual_write_off, 2),
            "denied_amount": round(self.denied_amount, 2),
            "patient_responsibility": round(self.patient_responsibility, 2),
            "check_eft_trace": self.check_eft_trace,
            "remittance_status": self.remittance_status,
            "ledger_notes": self.ledger_notes
        }


@dataclass
class InvoiceLineItem:
    """Line item displayed on the patient billing statement."""
    description: str
    charge: float
    insurance_paid: float
    adjustment: float
    patient_due: float


@dataclass
class PatientInvoice:
    """Patient statement / invoice generated after insurance adjudication and payment posting."""
    invoice_number: str
    invoice_date: str
    due_date: str
    patient_id: str
    patient_name: str
    patient_address: str
    encounter_id: str
    date_of_service: str
    provider_name: str
    items: List[InvoiceLineItem] = field(default_factory=list)
    total_charges: float = 0.00
    insurance_payments: float = 0.00
    contractual_adjustments: float = 0.00
    prior_payments: float = 0.00
    patient_copay: float = 0.00
    patient_deductible: float = 0.00
    patient_coinsurance: float = 0.00
    total_balance_due: float = 0.00
    status: str = "Issued - Unpaid"
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "invoice_number": self.invoice_number,
            "invoice_date": self.invoice_date,
            "due_date": self.due_date,
            "patient_id": self.patient_id,
            "patient_name": self.patient_name,
            "encounter_id": self.encounter_id,
            "total_charges": round(self.total_charges, 2),
            "insurance_payments": round(self.insurance_payments, 2),
            "contractual_adjustments": round(self.contractual_adjustments, 2),
            "patient_copay": round(self.patient_copay, 2),
            "patient_deductible": round(self.patient_deductible, 2),
            "patient_coinsurance": round(self.patient_coinsurance, 2),
            "total_balance_due": round(self.total_balance_due, 2),
            "status": self.status
        }


@dataclass
class SimulationBatchMetrics:
    """Aggregated financial and operational metrics for the Week 2 simulation."""
    total_encounters: int = 0
    clean_claims_count: int = 0
    scrubber_errors_count: int = 0
    claims_paid_count: int = 0
    claims_partially_paid_count: int = 0
    claims_denied_count: int = 0
    claims_rejected_count: int = 0
    total_gross_billed: float = 0.00
    total_adjudicated_gross: float = 0.00
    total_rejected_charges: float = 0.00
    total_allowed: float = 0.00
    total_contractual_adjustments: float = 0.00
    total_denied_charges: float = 0.00
    total_insurance_payments: float = 0.00
    total_patient_responsibility: float = 0.00
    total_deductible_collected: float = 0.00
    total_copay_collected: float = 0.00
    total_coinsurance_collected: float = 0.00
    total_self_pay: float = 0.00

    @property
    def paid_claims(self) -> int:
        return self.claims_paid_count

    @property
    def adjudicated_claims(self) -> int:
        return self.claims_paid_count

    @property
    def partially_paid_claims(self) -> int:
        return self.claims_partially_paid_count

    @property
    def denied_claims(self) -> int:
        return self.claims_denied_count

    @property
    def rejected_claims(self) -> int:
        return self.claims_rejected_count

    @property
    def clean_claims(self) -> int:
        return self.clean_claims_count

    @property
    def total_allowed_amount(self) -> float:
        return self.total_allowed

    @property
    def clean_claim_rate(self) -> float:
        if self.total_encounters == 0:
            return 0.0
        return round((self.clean_claims_count / self.total_encounters) * 100, 1)

    @property
    def net_collection_rate(self) -> float:
        if self.total_allowed == 0:
            return 0.0
        # Percentage of allowed amount collected (insurance + patient)
        total_collected = self.total_insurance_payments + self.total_patient_responsibility
        return round((total_collected / self.total_allowed) * 100, 1)

    @property
    def denial_rate(self) -> float:
        if self.total_encounters == 0:
            return 0.0
        return round((self.claims_denied_count / self.total_encounters) * 100, 1)

    @property
    def rejection_rate(self) -> float:
        if self.total_encounters == 0:
            return 0.0
        return round((self.claims_rejected_count / self.total_encounters) * 100, 1)

    @property
    def total_adjustments_and_denials(self) -> float:
        """Combined non-billable provider adjustments (contractual fee schedule write-offs + payer denials)."""
        return round(self.total_contractual_adjustments + self.total_denied_charges, 2)
