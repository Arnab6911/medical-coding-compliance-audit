"""Data models and enums for Week 3: Billing Query Resolution and Error Analysis."""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Optional, Any


class ErrorSeverity(str, Enum):
    """Severity classification for detected billing queries and errors."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class ResolutionStatus(str, Enum):
    """Standardized resolution outcome states for billing queries."""
    RESOLVED_CORRECTED = "Resolved – Corrected Claim"
    RESOLVED_DOCS = "Resolved – Documentation Updated"
    PENDING_PROVIDER = "Pending Provider Query"
    PENDING_PAYER = "Pending Payer Clarification"
    PENDING_DOCS = "Pending Additional Documentation"
    REJECTED_CORRECTION = "Rejected – Correction Required"
    NO_ERROR = "No Error Identified"
    ESCALATED = "Escalated for Human Review"


class RootCauseCategory(str, Enum):
    """Primary operational and workflow classifications for error root causes."""
    REGISTRATION_ERROR = "Registration Error"
    ELIGIBILITY_FAILURE = "Eligibility Verification Failure"
    CLINICAL_DOC_DEFICIENCY = "Clinical Documentation Deficiency"
    CODING_KNOWLEDGE_ERROR = "Coding Knowledge Error"
    INCORRECT_CODE_SELECTION = "Incorrect Code Selection"
    CHARGE_CAPTURE_ERROR = "Charge Capture Error"
    DUPLICATE_SUBMISSION = "Duplicate Submission"
    MODIFIER_UNIT_ERROR = "Modifier or Unit Error"
    AUTHORIZATION_FAILURE = "Authorization / Referral Failure"
    SCRUBBER_FAILURE = "Claim-Scrubbing Failure"
    PAYER_PROCESSING_ISSUE = "Payer Processing Issue"
    PAYMENT_POSTING_ERROR = "Payment-Posting / Financial Calculation Error"
    WORKFLOW_TRAINING = "Staff Training or Workflow Deficiency"
    COMPLIANCE_AUDIT = "Auditing & Compliance Verification"


@dataclass
class BillingScenario:
    """Represents a single fictional outpatient billing scenario or query."""
    scenario_id: str
    encounter_id: str
    patient_id: str
    patient_name: str
    patient_age: int
    patient_gender: str
    date_of_service: str
    payer_name: str
    plan_type: str
    clinical_documentation: str
    original_icd10: str
    original_cpt: str
    original_billed_amount: float
    billing_query: str
    error_category: str
    error_severity: ErrorSeverity
    root_cause: str
    evidence_required: str
    recommended_action: str
    final_status: ResolutionStatus
    preventive_measure: str
    manual_review_required: bool = True
    corrected_icd10: Optional[str] = None
    corrected_cpt: Optional[str] = None
    corrected_billed_amount: Optional[float] = None
    variance_amount: float = 0.00
    has_provider_signature: bool = True
    has_prior_authorization: bool = True
    units_billed: int = 1
    modifier_applied: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert scenario to dictionary representation."""
        d = asdict(self)
        d["error_severity"] = self.error_severity.value
        d["final_status"] = self.final_status.value
        return d


@dataclass
class DetectionFinding:
    """Represents an automated error-detection finding for a billing query."""
    finding_id: str
    scenario_id: str
    encounter_id: str
    error_code: str
    error_name: str
    severity: ErrorSeverity
    evidence: str
    reason_flagged: str
    recommended_action: str
    manual_review_required: bool
    is_confirmed_error: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert finding to dictionary."""
        d = asdict(self)
        d["severity"] = self.severity.value
        return d


@dataclass
class RootCauseAnalysis:
    """Root cause investigation record for a billing query."""
    scenario_id: str
    encounter_id: str
    primary_category: RootCauseCategory
    secondary_factors: List[str]
    operational_stage: str
    underlying_cause: str
    financial_risk: str
    evidence_needed: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert RCA to dictionary."""
        d = asdict(self)
        d["primary_category"] = self.primary_category.value
        return d


@dataclass
class QueryResolution:
    """Step-by-step resolution roadmap and outcome for a billing query."""
    scenario_id: str
    encounter_id: str
    query_id: str
    resolution_steps: List[str]
    required_evidence: List[str]
    provider_payer_communication: str
    claim_action: str
    validation_checks: List[str]
    final_status: ResolutionStatus
    financial_reconciliation: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert resolution to dictionary."""
        d = asdict(self)
        d["final_status"] = self.final_status.value
        return d


@dataclass
class PreventiveControl:
    """Systemic preventive measure designed to avoid recurrence of a billing error."""
    error_code: str
    control_name: str
    description: str
    responsible_department: str
    implementation_frequency: str
    ehr_hard_stop: bool
    expected_benefit: str
    regulatory_or_best_practice: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert preventive control to dictionary."""
        return asdict(self)


@dataclass
class SimulationBatchMetrics:
    """Aggregated operational and financial metrics across all scenarios."""
    total_scenarios: int = 0
    errors_identified_count: int = 0
    no_error_identified_count: int = 0
    pending_query_count: int = 0
    escalated_review_count: int = 0
    resolved_claims_count: int = 0
    manual_review_required_count: int = 0
    total_original_gross_billed: float = 0.00
    total_corrected_gross_billed: float = 0.00
    total_financial_variance: float = 0.00
    clean_resolution_rate: float = 0.00
    category_counts: Dict[str, int] = field(default_factory=dict)
    severity_counts: Dict[str, int] = field(default_factory=dict)
    status_counts: Dict[str, int] = field(default_factory=dict)
    root_cause_counts: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary."""
        return asdict(self)
