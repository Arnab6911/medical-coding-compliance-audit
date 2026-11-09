"""
Week 4 Data Models and Dataclasses
Defines domain structures for:
- Software Vendor Comparison
- Selection Evaluation Criteria & Scoring
- Practice Profile (Evergreen Valley Family Medicine)
- Data Migration Records & Reconciliation
- Real-Time Pre-Bill Validation Rules
- Risk Register Items
- RCM Key Performance Indicators
- Training Modules & Knowledge Assessment
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any

@dataclass
class VendorComparison:
    feature_id: str
    feature_name: str
    category: str
    athenahealth_capability: str
    athenahealth_status: str
    athenahealth_source: str
    advancedmd_capability: str
    advancedmd_status: str
    advancedmd_source: str
    tebra_capability: str
    tebra_status: str
    tebra_source: str
    research_date: str = "2026-11-09"

@dataclass
class EvaluationCriteria:
    criterion_id: str
    name: str
    category: str
    weight: float  # Percentage (e.g., 0.15 for 15%)
    score_athena: float  # 1.0 to 10.0
    score_advancedmd: float  # 1.0 to 10.0
    score_tebra: float  # 1.0 to 10.0
    justification_athena: str
    justification_advancedmd: str
    justification_tebra: str

@dataclass
class PracticeProfile:
    name: str = "Evergreen Valley Family Medicine & Multi-Specialty Clinic"
    practice_type: str = "Independent Outpatient Multi-Specialty Clinic"
    provider_count: int = 8
    providers_breakdown: str = "5 Primary Care Physicians, 1 Pediatrician, 2 Part-time Specialists (Cardiology & Orthopedics)"
    billing_staff_count: int = 4
    billing_staff_roles: str = "1 Billing Supervisor, 2 Certified Medical Coders (CPC/CCS), 1 Payment Posting Specialist"
    front_desk_staff_count: int = 3
    monthly_encounter_volume: int = 3000
    annual_encounter_volume: int = 36000
    legacy_ehr_system: str = "MedTech On-Premise EHR v12.4 (SQL Server Database)"
    legacy_pm_system: str = "Legacy Desktop Billing Manager (Standalone EDI 837 Exporter)"
    clearinghouse_workflow: str = "Manual nightly batch upload via external web portal (No real-time API)"
    baseline_first_pass_rate: float = 85.2
    baseline_denial_rate: float = 14.8
    baseline_days_in_ar: float = 52.4
    baseline_claim_submission_lag: float = 6.8  # days
    baseline_uncollected_patient_ar: float = 23.5  # percent
    operational_challenges: List[str] = field(default_factory=lambda: [
        "Disjointed on-premise systems requiring redundant manual demographic and charge entry.",
        "High initial denial rate (14.8%) primarily driven by missing prior authorizations and modifier omissions.",
        "Protracted accounts receivable cycle (52.4 Days in AR) caused by batch claim submission delays.",
        "Lack of real-time X12 270/271 eligibility verification leading to front-desk registration errors.",
        "Manual payment posting and reconciliation creating delayed visibility into patient balances."
    ])
    proposed_future_state: List[str] = field(default_factory=lambda: [
        "Unified cloud platform synchronizing clinical EHR documentation with practice management billing in real time.",
        "Automated pre-visit X12 270/271 eligibility batching with front-desk hard-stops on inactive coverage.",
        "Embedded pre-bill claim scrubber with real-time NCCI and payer edit checks prior to submission.",
        "Integrated clearinghouse with automated 837P transmission and auto-posting of 835 ERAs.",
        "Comprehensive RCM analytics dashboard tracking the 11 core financial and operational KPIs."
    ])

@dataclass
class MigrationRecord:
    legacy_patient_id: str
    first_name: str
    last_name: str
    dob: str
    gender: str
    address: str
    phone: str
    primary_payer: str
    policy_id: str
    group_id: str
    legacy_ar_balance: float
    migrated_ar_balance: float
    variance: float
    migration_status: str
    validation_flags: str
    reconciliation_notes: str

@dataclass
class ValidationRule:
    rule_id: str
    rule_name: str
    category: str
    severity: str  # HARD_STOP, WARNING, CODING_REVIEW
    description: str
    trigger_condition: str
    resolution_guidance: str
    code_governance_type: Optional[str] = None  # ANNUAL_ICD10, ANNUAL_CPT, NCCI_PTP, etc.

@dataclass
class RiskItem:
    risk_id: str
    category: str
    title: str
    description: str
    likelihood: int  # 1 to 5
    impact: int  # 1 to 5
    risk_score: int  # likelihood * impact
    risk_level: str  # Low, Medium, High, Critical
    mitigation_strategy: str
    contingency_plan: str
    owner_role: str

@dataclass
class KPIMetric:
    kpi_id: str
    name: str
    category: str
    formula: str
    baseline_value: Any
    target_value: float
    unit: str
    measurement_frequency: str
    status_target: str
    operational_impact: str

@dataclass
class AssessmentQuestion:
    question_id: str
    target_role: str
    question: str
    options: List[str]
    correct_option_index: int
    explanation: str
    guideline_reference: str

@dataclass
class TrainingModule:
    module_id: str
    target_role: str
    title: str
    duration_hours: float
    learning_objectives: List[str]
    practical_exercises: List[str]
