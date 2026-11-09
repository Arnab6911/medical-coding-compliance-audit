"""Data models for Medical Coding Compliance Audit Simulation.

Defines typed dataclasses and enums representing patient records, audit findings,
severity rankings, and aggregate audit summaries.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Any, Dict


class AuditSeverity(str, Enum):
    """Compliance audit severity levels for flagged findings."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class IssueType(str, Enum):
    """Categorized medical coding compliance discrepancy types."""
    MISSING_REQUIRED_FIELD = "Missing Required Field"
    MISSING_DIAGNOSIS = "Missing Diagnosis Documentation"
    MISSING_CLINICAL_DOCUMENTATION = "Missing Clinical Documentation"
    CODE_MISMATCH = "Diagnosis Code Mismatch"
    UNVERIFIED_CODE = "Unverified Reference Code"
    INCOMPLETE_DOCUMENTATION = "Incomplete Clinical Documentation"
    DUPLICATE_DIAGNOSIS = "Duplicate Diagnosis Entry"
    DUPLICATE_PROCEDURE = "Duplicate Procedure Entry"
    UNSUPPORTED_PROCEDURE = "Unsupported Procedure Coding"
    UNSUPPORTED_EM_LEVEL = "Unsupported E/M Level"
    UNSPECIFIED_CODE_USAGE = "Unspecified Code Warning"
    MISSING_PROVIDER_SIGNATURE = "Missing Provider Signature"


@dataclass
class PatientRecord:
    """Represents a fictional patient clinical encounter record."""
    encounter_id: str
    patient_id: str
    patient_age: str
    patient_gender: str
    encounter_date: str
    clinical_documentation: str
    documented_diagnosis: str
    assigned_icd10: str
    procedure_description: str
    assigned_cpt: str
    documentation_completeness: str = "Complete"

    # Backward compatibility aliases
    @property
    def record_id(self) -> str:
        return self.encounter_id

    @property
    def documentation_notes(self) -> str:
        return self.clinical_documentation

    def split_icd10_codes(self) -> List[str]:
        """Return list of individual ICD-10 codes, splitting multiple entries."""
        if not self.assigned_icd10:
            return []
        raw_codes = [c.strip().upper() for c in self.assigned_icd10.replace(",", ";").split(";")]
        return [c for c in raw_codes if c]

    def split_cpt_codes(self) -> List[str]:
        """Return list of individual CPT codes, splitting multiple entries."""
        if not self.assigned_cpt:
            return []
        raw_codes = [c.strip().upper() for c in self.assigned_cpt.replace(",", ";").split(";")]
        return [c for c in raw_codes if c]

    def split_documented_diagnoses(self) -> List[str]:
        """Return list of documented diagnoses."""
        if not self.documented_diagnosis:
            return []
        raw = [d.strip() for d in self.documented_diagnosis.replace(";", "\n").splitlines()]
        return [d for d in raw if d]


@dataclass
class AuditFinding:
    """Represents an individual audit discrepancy identified by the audit engine.

    Attributes:
        encounter_id: Unique encounter reference ID.
        patient_id: Fictional patient reference ID.
        original_diagnosis: Clinical diagnosis as documented in record.
        assigned_code: Assigned ICD-10 or CPT code flagged by audit.
        audit_issue: Category of the compliance issue.
        severity: AuditSeverity enum (High, Medium, Low).
        reason: Plain-language rationale for flagging the item.
        recommended_action: Suggested remediation for the human auditor.
        reference_guideline: Official coding or regulatory standard citation.
        manual_review_required: Always True for flagged compliance findings.
    """
    encounter_id: str
    patient_id: str
    original_diagnosis: str
    assigned_code: str
    audit_issue: str
    severity: AuditSeverity
    reason: str
    recommended_action: str
    reference_guideline: str
    manual_review_required: bool = True

    # Backward compatibility alias
    @property
    def record_id(self) -> str:
        return self.encounter_id

    def to_dict(self) -> dict:
        """Convert finding to dictionary for tabular representation."""
        return {
            "Encounter ID": self.encounter_id,
            "Record ID": self.encounter_id,
            "Patient ID": self.patient_id,
            "Original Diagnosis": self.original_diagnosis or "(None Documented)",
            "Assigned Code": self.assigned_code or "(None)",
            "Audit Issue": self.audit_issue,
            "Severity": self.severity.value,
            "Reason for Flagging": self.reason,
            "Recommended Corrective Action": self.recommended_action,
            "Reference / Guideline": self.reference_guideline,
            "Manual Review Required": "Yes" if self.manual_review_required else "No"
        }


@dataclass
class AuditSummary:
    """Summary metrics of an executed compliance audit session."""
    total_records: int = 0
    records_reviewed: int = 0
    records_flagged: int = 0
    clean_records: int = 0
    total_findings: int = 0
    high_severity_count: int = 0
    medium_severity_count: int = 0
    low_severity_count: int = 0
    coding_issues_count: int = 0
    documentation_issues_count: int = 0
    findings: List[AuditFinding] = field(default_factory=list)

    @property
    def compliance_rate(self) -> float:
        """Percentage of records without any audit flags."""
        if self.total_records == 0:
            return 100.0
        return round((self.clean_records / self.total_records) * 100, 1)

    @property
    def review_rate(self) -> float:
        """Percentage of records requiring manual audit review."""
        if self.total_records == 0:
            return 0.0
        return round((self.records_flagged / self.total_records) * 100, 1)
