"""Audit rules engine for Medical Coding Compliance Audit Simulation.

Implements modular, clinically aware validation functions to evaluate clinical records,
detect missing fields, identify duplicate codes, compare diagnoses with code mappings,
flag unsupported or unverified codes, and check documentation deficiencies.

All findings are non-destructive advisory flags for certified human auditor review;
this engine strictly enforces that patient records and codes are never modified automatically.
"""

from __future__ import annotations
import re
from typing import List, Dict, Any, Optional, Set
import pandas as pd

from src.models import PatientRecord, AuditFinding, AuditSummary, AuditSeverity, IssueType
from src.reference_data import ReferenceDataManager, get_reference_manager


# Clinical stopwords ignored during diagnostic core concept token comparison
CLINICAL_STOPWORDS: Set[str] = {
    "with", "without", "unspecified", "other", "initial", "subsequent",
    "encounter", "due", "to", "of", "in", "and", "or", "for", "primary",
    "secondary", "type", "site", "not", "specified"
}

# Standard clinical negation phrases to prevent false positive keyword matching
NEGATION_PATTERNS = [
    r"\bno\b",
    r"\bdenies\b",
    r"\bwithout\b",
    r"\bnegative\s+for\b",
    r"\bno\s+history\s+of\b",
    r"\bruled\s+out\b",
    r"\bno\s+evidence\s+of\b",
    r"\bno\s+signs\s+of\b",
    r"\bnot\s+indicated\b"
]


def is_negated_in_text(keyword: str, text: str) -> bool:
    """Check if a clinical keyword is preceded by a common medical negation phrase.

    Args:
        keyword: Clinical symptom or disease term.
        text: Clinical note text.

    Returns:
        True if the term appears only in a negative/ruled-out context.
    """
    text_lower = text.lower()
    kw_lower = keyword.lower()

    if kw_lower not in text_lower:
        return False

    # Check each occurrence of keyword for preceding negation within a 35-character window
    for match in re.finditer(re.escape(kw_lower), text_lower):
        start_idx = match.start()
        window_start = max(0, start_idx - 35)
        preceding_snippet = text_lower[window_start:start_idx]
        for pattern in NEGATION_PATTERNS:
            if re.search(pattern, preceding_snippet):
                return True
    return False


def is_diagnosis_supported(
    code_entry: Optional[Dict[str, Any]],
    documented_diagnosis: str,
    clinical_documentation: str
) -> bool:
    """Evaluate whether an assigned ICD-10 code is clinically substantiated by documentation.

    Prevents false-positive mismatches by combining:
    1. Direct phrase alignment with official code descriptions.
    2. Core clinical concept token overlap.
    3. Keyword synonyms evaluated with clinical negation awareness.

    Args:
        code_entry: Dictionary containing code metadata, description, and keywords.
        documented_diagnosis: Diagnosis as recorded in clinical chart.
        clinical_documentation: Free-text progress note from encounter.

    Returns:
        True if the diagnosis is substantiated; False if an actual clinical mismatch exists.
    """
    if not code_entry:
        return True

    doc_lower = (documented_diagnosis or "").lower().strip()
    notes_lower = (clinical_documentation or "").lower().strip()
    desc_lower = code_entry.get("description", "").lower().strip()

    if not doc_lower:
        return False

    # 1. Direct equality or substring containment
    if doc_lower == desc_lower or desc_lower in doc_lower or doc_lower in desc_lower:
        return True

    # 2. Tokenized core clinical concept overlap
    doc_words = set(re.sub(r"[^\w\s]", " ", doc_lower).split()) - CLINICAL_STOPWORDS
    desc_words = set(re.sub(r"[^\w\s]", " ", desc_lower).split()) - CLINICAL_STOPWORDS

    # If core descriptive words of the code are a subset of documented diagnosis
    if desc_words and desc_words.issubset(doc_words):
        return True

    # If substantial overlap exists (>= 50% of significant code description words)
    overlap = desc_words.intersection(doc_words)
    if desc_words and len(overlap) / len(desc_words) >= 0.5:
        return True

    # 3. Check curated clinical keywords against documented diagnosis and notes
    keywords = code_entry.get("keywords", [])
    for kw in keywords:
        kw_l = kw.lower()
        # Direct keyword appearance in documented diagnosis
        if kw_l in doc_lower:
            return True
        # Keyword appearance in notes, provided it is NOT in a negated context
        if kw_l in notes_lower and not is_negated_in_text(kw_l, notes_lower):
            return True

    return False


# -----------------------------------------------------------------------------
# MODULAR AUDIT VALIDATION FUNCTIONS
# -----------------------------------------------------------------------------

def check_missing_fields(record: PatientRecord, ref: ReferenceDataManager) -> List[AuditFinding]:
    """Validate presence of essential administrative and clinical encounter fields.

    Args:
        record: PatientRecord to evaluate.
        ref: ReferenceDataManager providing citation guidelines.

    Returns:
        List of AuditFinding objects for any missing required fields.
    """
    findings: List[AuditFinding] = []

    # 1. Missing clinical documentation entirely
    doc_notes = (record.clinical_documentation or "").strip()
    if not doc_notes:
        findings.append(
            AuditFinding(
                encounter_id=record.encounter_id,
                patient_id=record.patient_id,
                original_diagnosis=record.documented_diagnosis,
                assigned_code=record.assigned_icd10 or record.assigned_cpt or "(None)",
                code_set_year="FY 2024 / 2024 (Historical)",
                audit_issue=IssueType.MISSING_CLINICAL_DOCUMENTATION.value,
                severity=AuditSeverity.HIGH,
                reason=(
                    f"Encounter [{record.encounter_id}] lacks clinical progress notes in chart documentation. "
                    f"Under Medicare integrity rules, services cannot be billed without supporting medical documentation. "
                    f"Note: Missing documentation requires chart retrieval/reconciliation, not assumption of intentional miscoding."
                ),
                recommended_action=(
                    "Locate and append clinical progress note for this encounter, or place claim on hold "
                    "pending provider verification to prevent billing compliance risk."
                ),
                reference_guideline=ref.get_citation("incomplete_clinical_notes"),
                manual_review_required=True
            )
        )

    # 2. Missing documented diagnosis when ICD-10 is assigned
    doc_diag = (record.documented_diagnosis or "").strip()
    assigned_icds = record.split_icd10_codes()
    if assigned_icds and not doc_diag:
        findings.append(
            AuditFinding(
                encounter_id=record.encounter_id,
                patient_id=record.patient_id,
                original_diagnosis="",
                assigned_code=", ".join(assigned_icds),
                code_set_year="FY 2024 (Historical)",
                audit_issue=IssueType.MISSING_DIAGNOSIS.value,
                severity=AuditSeverity.HIGH,
                reason=(
                    f"Encounter bills diagnosis code(s) [{', '.join(assigned_icds)}] "
                    f"but the documented diagnosis field is unpopulated. Diagnosis codes must reflect documented provider assessments."
                ),
                recommended_action=(
                    "Verify patient chart documentation. A certified coder must query "
                    "the attending physician to clarify the diagnostic assessment before claim submission."
                ),
                reference_guideline=ref.get_citation("missing_diagnosis_support"),
                manual_review_required=True
            )
        )

    # 3. Missing Encounter Date
    if not (record.encounter_date or "").strip():
        findings.append(
            AuditFinding(
                encounter_id=record.encounter_id,
                patient_id=record.patient_id,
                original_diagnosis=record.documented_diagnosis,
                assigned_code="(Administrative)",
                code_set_year="N/A",
                audit_issue=IssueType.MISSING_REQUIRED_FIELD.value,
                severity=AuditSeverity.MEDIUM,
                reason="Encounter date of service is missing or unpopulated.",
                recommended_action="Populate verified date of service from EHR master encounter schedule.",
                reference_guideline="CMS Claims Processing Manual (Pub. 100-04) Chapter 1 §80: Basic claim line elements including date of service are mandatory for valid claim adjudication.",
                manual_review_required=True
            )
        )

    return findings


def identify_duplicate_codes(record: PatientRecord, ref: ReferenceDataManager) -> List[AuditFinding]:
    """Detect duplicate diagnosis or procedure codes billed on the same encounter date.

    Args:
        record: PatientRecord to evaluate.
        ref: ReferenceDataManager providing citation guidelines.

    Returns:
        List of AuditFinding objects for duplicate codes.
    """
    findings: List[AuditFinding] = []

    # Check duplicate ICD-10 codes
    icd_codes = record.split_icd10_codes()
    seen_icd = set()
    dup_icd = set()
    for code in icd_codes:
        if code in seen_icd:
            dup_icd.add(code)
        else:
            seen_icd.add(code)

    for dup in dup_icd:
        findings.append(
            AuditFinding(
                encounter_id=record.encounter_id,
                patient_id=record.patient_id,
                original_diagnosis=record.documented_diagnosis,
                assigned_code=dup,
                code_set_year="FY 2024 (Historical)",
                audit_issue=IssueType.DUPLICATE_DIAGNOSIS.value,
                severity=AuditSeverity.MEDIUM,
                reason=(
                    f"ICD-10 code [{dup}] is entered multiple times for this single encounter. "
                    f"Duplicate diagnosis codes cause claim rejections and payer scrub errors."
                ),
                recommended_action=(
                    f"Remove duplicate instance of [{dup}] from the encounter claim line. "
                    f"Ensure each diagnosis is reported only once per encounter unless distinct modifiers apply."
                ),
                reference_guideline=ref.get_citation("duplicate_diagnosis"),
                manual_review_required=True
            )
        )

    # Check duplicate CPT codes
    cpt_codes = record.split_cpt_codes()
    seen_cpt = set()
    dup_cpt = set()
    for code in cpt_codes:
        if code in seen_cpt:
            dup_cpt.add(code)
        else:
            seen_cpt.add(code)

    for dup in dup_cpt:
        findings.append(
            AuditFinding(
                encounter_id=record.encounter_id,
                patient_id=record.patient_id,
                original_diagnosis=record.documented_diagnosis,
                assigned_code=f"CPT {dup}",
                code_set_year="2024 (Historical)",
                audit_issue=IssueType.DUPLICATE_PROCEDURE.value,
                severity=AuditSeverity.MEDIUM,
                reason=(
                    f"CPT procedure code [{dup}] is billed multiple times on the same encounter date without distinct modifier."
                ),
                recommended_action=(
                    f"Review whether CPT [{dup}] was performed multiple times. If so, append appropriate CPT modifier "
                    f"(e.g., modifier 76/59) or remove duplicate line."
                ),
                reference_guideline="CMS National Correct Coding Initiative (NCCI) Policy Manual Chapter 1 §B: Multiple procedure duplication guidelines; repeatable services require distinct modifiers.",
                manual_review_required=True
            )
        )

    return findings


def flag_unsupported_or_unverified_codes(record: PatientRecord, ref: ReferenceDataManager) -> List[AuditFinding]:
    """Verify assigned ICD-10 and CPT codes against authoritative code subsets.

    Codes not verified in the active reference dictionary are explicitly marked as requiring manual verification.

    Args:
        record: PatientRecord to evaluate.
        ref: ReferenceDataManager providing reference code sets.

    Returns:
        List of AuditFinding objects for unverified codes.
    """
    findings: List[AuditFinding] = []

    # Check ICD-10 codes
    for code in record.split_icd10_codes():
        entry = ref.get_icd10_entry(code)
        if entry is None:
            findings.append(
                AuditFinding(
                    encounter_id=record.encounter_id,
                    patient_id=record.patient_id,
                    original_diagnosis=record.documented_diagnosis,
                    assigned_code=code,
                    code_set_year="Unverified Code Set",
                    audit_issue=IssueType.UNVERIFIED_CODE.value,
                    severity=AuditSeverity.MEDIUM,
                    reason=(
                        f"Assigned ICD-10 code [{code}] is not verified in the active "
                        f"{ref.icd10_version} reference dataset. "
                        f"Explicit manual verification against official CMS Tabular Index required."
                    ),
                    recommended_action=(
                        f"Manually verify [{code}] in the official ICD-10-CM coding manual. "
                        f"Confirm code validity, header chapter, and required 4th/5th/6th/7th characters."
                    ),
                    reference_guideline=ref.get_citation("unverified_code_manual_check"),
                    manual_review_required=True
                )
            )

    # Check CPT codes
    for cpt in record.split_cpt_codes():
        entry = ref.get_cpt_entry(cpt)
        if entry is None:
            findings.append(
                AuditFinding(
                    encounter_id=record.encounter_id,
                    patient_id=record.patient_id,
                    original_diagnosis=record.documented_diagnosis,
                    assigned_code=f"CPT {cpt}",
                    code_set_year="Unverified Code Set",
                    audit_issue=IssueType.UNVERIFIED_CODE.value,
                    severity=AuditSeverity.MEDIUM,
                    reason=(
                        f"Assigned CPT code [{cpt}] is not verified in the active "
                        f"{ref.cpt_version} educational reference dataset. "
                        f"Manual verification against AMA CPT codebook required."
                    ),
                    recommended_action=(
                        f"Verify CPT [{cpt}] against AMA Current Procedural Terminology standard index "
                        f"and confirm documentation substantiates all code descriptor requirements."
                    ),
                    reference_guideline="AMA CPT Standard Edition: All reported procedural codes must be verified against current annual editions.",
                    manual_review_required=True
                )
            )

    return findings


def compare_diagnoses_with_mappings(record: PatientRecord, ref: ReferenceDataManager) -> List[AuditFinding]:
    """Detect inconsistencies or contradictions between documented diagnoses and assigned codes.

    Uses category cross-validation, token overlap, and clinical negation awareness
    rather than simplistic substring matching, preventing false positive mismatches.

    Args:
        record: PatientRecord to evaluate.
        ref: ReferenceDataManager providing keyword definitions.

    Returns:
        List of AuditFinding objects for genuine code/diagnosis mismatches.
    """
    findings: List[AuditFinding] = []
    codes = record.split_icd10_codes()

    for code in codes:
        code_entry = ref.get_icd10_entry(code)
        if not code_entry:
            continue

        code_desc = code_entry.get("description", "")
        code_year = "FY 2024 (Historical)"

        # Clinically evaluate whether code is supported
        supported = is_diagnosis_supported(
            code_entry,
            record.documented_diagnosis,
            record.clinical_documentation
        )

        if not supported and (record.documented_diagnosis or "").strip():
            findings.append(
                AuditFinding(
                    encounter_id=record.encounter_id,
                    patient_id=record.patient_id,
                    original_diagnosis=record.documented_diagnosis,
                    assigned_code=f"{code} ({code_desc})",
                    code_set_year=code_year,
                    audit_issue=IssueType.CODE_MISMATCH.value,
                    severity=AuditSeverity.HIGH,
                    reason=(
                        f"Documented condition '{record.documented_diagnosis}' conflicts with assigned code "
                        f"[{code}: {code_desc}]. Clinical documentation does not positively substantiate this diagnosis."
                    ),
                    recommended_action=(
                        f"Re-examine provider documentation. Align assigned ICD-10-CM code to match documented "
                        f"condition ('{record.documented_diagnosis}') or issue provider query."
                    ),
                    reference_guideline=ref.get_citation("code_diagnosis_mismatch"),
                    manual_review_required=True
                )
            )

    return findings


def identify_documentation_deficiencies(record: PatientRecord, ref: ReferenceDataManager) -> List[AuditFinding]:
    """Evaluate note length, clinical substance, and provider authentication.

    Args:
        record: PatientRecord to evaluate.
        ref: ReferenceDataManager providing thresholds and citations.

    Returns:
        List of AuditFinding objects for documentation deficiencies.
    """
    findings: List[AuditFinding] = []
    notes = (record.clinical_documentation or "").strip()
    word_count = len(notes.split())
    thresholds = ref.get_thresholds()
    min_words = thresholds.get("min_note_word_count_standard", 15)

    # 1. Terse or grossly incomplete note (skip if note was completely empty, which is handled by check_missing_fields)
    if 0 < word_count < min_words:
        findings.append(
            AuditFinding(
                encounter_id=record.encounter_id,
                patient_id=record.patient_id,
                original_diagnosis=record.documented_diagnosis,
                assigned_code=record.assigned_cpt or "(No CPT)",
                code_set_year="2024 (Historical)",
                audit_issue=IssueType.INCOMPLETE_DOCUMENTATION.value,
                severity=AuditSeverity.HIGH if word_count < 5 else AuditSeverity.MEDIUM,
                reason=(
                    f"Clinical documentation contains only {word_count} word(s) (minimum threshold: {min_words} words). "
                    f"Documentation fails to substantiate encounter complexity, physical exam, or clinical management. "
                    f"Note: This documentation deficiency requires clinician addendum, not automatic assumption of fraud."
                ),
                recommended_action=(
                    "Request clinician addendum detailing Chief Complaint, History of Present Illness (HPI), "
                    "Examination, and Medical Decision Making before billing."
                ),
                reference_guideline=ref.get_citation("incomplete_clinical_notes"),
                manual_review_required=True
            )
        )

    # 2. Check provider signature / electronic attestation
    sig_keywords = thresholds.get("signature_keywords", ["electronically signed", "signed by", "dr.", "m.d."])
    notes_lower = notes.lower()
    has_signature = any(sig in notes_lower for sig in sig_keywords)

    if not has_signature and word_count >= min_words:
        findings.append(
            AuditFinding(
                encounter_id=record.encounter_id,
                patient_id=record.patient_id,
                original_diagnosis=record.documented_diagnosis,
                assigned_code=record.assigned_cpt or "(E/M Encounter)",
                code_set_year="2024 (Historical)",
                audit_issue=IssueType.MISSING_PROVIDER_SIGNATURE.value,
                severity=AuditSeverity.MEDIUM,
                reason=(
                    "Clinical note lacks authenticated provider electronic signature, date/timestamp, or credential. "
                    "Unauthenticated records represent a potential compliance risk under Medicare Conditions of Payment "
                    "and require provider signature authentication prior to claim submission."
                ),
                recommended_action=(
                    "Route record back to attending provider for electronic authentication and signature completion."
                ),
                reference_guideline=ref.get_citation("missing_provider_signature"),
                manual_review_required=True
            )
        )

    return findings


def check_unsupported_procedures(record: PatientRecord, ref: ReferenceDataManager) -> List[AuditFinding]:
    """Verify that assigned CPT codes have medical necessity and procedure documentation.

    Distinguishes missing procedure operative reports from lack of medical necessity.

    Args:
        record: PatientRecord to evaluate.
        ref: ReferenceDataManager providing CPT metadata and citations.

    Returns:
        List of AuditFinding objects for procedure discrepancies.
    """
    findings: List[AuditFinding] = []
    cpt_codes = record.split_cpt_codes()
    notes_lower = (record.clinical_documentation or "").lower()

    for cpt in cpt_codes:
        cpt_entry = ref.get_cpt_entry(cpt)
        if not cpt_entry:
            continue

        requires_proc_note = cpt_entry.get("requires_procedure_note", False)
        keywords = cpt_entry.get("keywords", [])
        compatible_diags = cpt_entry.get("compatible_diagnoses", [])

        # 1. Check if procedure documentation is present in notes when required
        if requires_proc_note:
            has_proc_mention = any(kw.lower() in notes_lower for kw in keywords)
            if not has_proc_mention:
                is_imaging = "radiolog" in cpt_entry.get("description", "").lower() or cpt == "71046"
                if is_imaging:
                    doc_desc = "appropriate radiology documentation/report (interpretation and report)"
                    retrieval_text = "Requires radiology report retrieval; not definitive proof of improper coding."
                    action_text = (
                        f"Initiate a pre-bill hold and verify encounter records. Locate and append standalone radiology "
                        f"report/interpretation signed by performing or interpreting clinician; remove CPT [{cpt}] only "
                        f"if non-performance is established."
                    )
                else:
                    doc_desc = "formal procedure documentation/report"
                    retrieval_text = "Requires procedure report retrieval; not definitive proof of improper coding."
                    action_text = (
                        f"Initiate a pre-bill hold and verify encounter records. Locate and append standalone procedure "
                        f"report signed by performing clinician; remove CPT [{cpt}] only if non-performance is established."
                    )

                findings.append(
                    AuditFinding(
                        encounter_id=record.encounter_id,
                        patient_id=record.patient_id,
                        original_diagnosis=record.documented_diagnosis,
                        assigned_code=f"CPT {cpt} ({cpt_entry.get('description', '')})",
                        code_set_year="2024 (Historical)",
                        audit_issue=IssueType.MISSING_PROCEDURE_DOCUMENTATION.value,
                        severity=AuditSeverity.HIGH,
                        reason=(
                            f"CPT code [{cpt}] requires {doc_desc}, but clinical note "
                            f"contains no documentation of the service being performed or findings interpreted. "
                            f"{retrieval_text}"
                        ),
                        recommended_action=action_text,
                        reference_guideline=ref.get_citation("missing_procedure_documentation"),
                        manual_review_required=True
                    )
                )

        # 2. Check medical necessity compatibility
        if compatible_diags:
            assigned_icds = record.split_icd10_codes()
            has_compatible_icd = any(icd in compatible_diags for icd in assigned_icds)
            if not has_compatible_icd:
                findings.append(
                    AuditFinding(
                        encounter_id=record.encounter_id,
                        patient_id=record.patient_id,
                        original_diagnosis=record.documented_diagnosis,
                        assigned_code=f"CPT {cpt}",
                        code_set_year="2024 (Historical)",
                        audit_issue=IssueType.UNSUPPORTED_PROCEDURE.value,
                        severity=AuditSeverity.HIGH,
                        reason=(
                            f"Potential medical necessity concern: Documented primary diagnosis ('{record.documented_diagnosis}') "
                            f"and assigned ICD-10 ([{record.assigned_icd10}]) do not readily establish coverage for procedure CPT [{cpt}]. "
                            f"This finding does not conclude the procedure is unnecessary based only on the primary diagnosis, but identifies "
                            f"a potential compliance concern requiring review of the complete clinical record and applicable coverage policies."
                        ),
                        recommended_action=(
                            f"Initiate a pre-bill hold and verify encounter records. Review the complete clinical record, physician orders, "
                            f"and applicable coverage policies (LCD/NCD) to establish medical necessity before billing CPT [{cpt}]; "
                            f"remove code only if non-performance or lack of medical necessity is established."
                        ),
                        reference_guideline=ref.get_citation("unsupported_procedure"),
                        manual_review_required=True
                    )
                )

    return findings


def check_unsupported_em_levels(record: PatientRecord, ref: ReferenceDataManager) -> List[AuditFinding]:
    """Detect overcoding or lack of documented complexity for high-level E/M visits.

    Args:
        record: PatientRecord to evaluate.
        ref: ReferenceDataManager providing threshold parameters.

    Returns:
        List of AuditFinding objects for unsupported E/M levels.
    """
    findings: List[AuditFinding] = []
    cpt_codes = record.split_cpt_codes()
    notes_lower = (record.clinical_documentation or "").lower()
    word_count = len((record.clinical_documentation or "").split())
    thresholds = ref.get_thresholds()

    for cpt in cpt_codes:
        cpt_entry = ref.get_cpt_entry(cpt)
        if not cpt_entry:
            continue

        if cpt in ["99215", "99205"]:
            min_high_words = thresholds.get("min_note_word_count_high_em", 45)
            high_keywords = cpt_entry.get("keywords", [])
            has_high_indicators = any(kw in notes_lower for kw in high_keywords)
            has_time_documented = bool(re.search(r"\b(\d{2,3})\s*(minutes|mins)\b", notes_lower))

            is_minor_diagnosis = any(term in (record.documented_diagnosis or "").lower() for term in [
                "low back pain", "sore throat", "uri", "cough", "routine", "refill", "mild", "uncomplicated"
            ])

            if (word_count < min_high_words or is_minor_diagnosis) and not has_time_documented:
                findings.append(
                    AuditFinding(
                        encounter_id=record.encounter_id,
                        patient_id=record.patient_id,
                        original_diagnosis=record.documented_diagnosis,
                        assigned_code=f"CPT {cpt} (Level 5 E/M)",
                        code_set_year="2024 (Historical)",
                        audit_issue=IssueType.UNSUPPORTED_EM_LEVEL.value,
                        severity=AuditSeverity.HIGH,
                        reason=(
                            f"Level 5 E/M code [{cpt}] assigned for diagnosis '{record.documented_diagnosis}'. "
                            f"Documentation lacks evidence of high Medical Decision Making (MDM) complexity "
                            f"or qualifying total encounter time (requires 40-54 min for 99215 under 2021/2023 E/M rules)."
                        ),
                        recommended_action=(
                            "Downcode to appropriate E/M level supported by documentation (e.g. 99213/99214) "
                            "or obtain provider documentation substantiating qualifying time/MDM elements."
                        ),
                        reference_guideline=ref.get_citation("high_level_em_underdocumented"),
                        manual_review_required=True
                    )
                )

    return findings


def check_unspecified_code_usage(record: PatientRecord, ref: ReferenceDataManager) -> List[AuditFinding]:
    """Flag usage of unspecified codes when documentation contains specific anatomical or clinical details.

    Args:
        record: PatientRecord to evaluate.
        ref: ReferenceDataManager providing code metadata.

    Returns:
        List of AuditFinding objects for unspecified codes with documented specificity.
    """
    findings: List[AuditFinding] = []
    codes = record.split_icd10_codes()
    full_text = f"{record.documented_diagnosis} {record.clinical_documentation}".lower()

    for code in codes:
        code_entry = ref.get_icd10_entry(code)
        if not code_entry or not code_entry.get("is_unspecified", False):
            continue

        has_laterality = any(lat in full_text for lat in ["right", "left", "bilateral"])
        alternatives = code_entry.get("specific_alternatives", [])

        if has_laterality and ("knee" in full_text or "joint" in full_text or "artery" in full_text):
            alt_str = ", ".join(alternatives) if alternatives else "more specific subcategory code"
            findings.append(
                AuditFinding(
                    encounter_id=record.encounter_id,
                    patient_id=record.patient_id,
                    original_diagnosis=record.documented_diagnosis,
                    assigned_code=code,
                    code_set_year="FY 2024 (Historical)",
                    audit_issue=IssueType.UNSPECIFIED_CODE_USAGE.value,
                    severity=AuditSeverity.LOW,
                    reason=(
                        f"Assigned code [{code}: {code_entry.get('description')}] is unspecified, "
                        f"yet documentation specifies laterality/details in the clinical chart ('{record.documented_diagnosis}')."
                    ),
                    recommended_action=(
                        f"Upgrade to specific code (e.g. {alt_str}) to satisfy specificity requirements "
                        f"and prevent commercial payer claim denials."
                    ),
                    reference_guideline=ref.get_citation("unspecified_code_usage"),
                    manual_review_required=True
                )
            )

    return findings


# -----------------------------------------------------------------------------
# AUDIT ENGINE CLASS
# -----------------------------------------------------------------------------

class AuditEngine:
    """Executes compliance validation rules against medical records."""

    def __init__(self, ref_manager: Optional[ReferenceDataManager] = None):
        self.ref = ref_manager or get_reference_manager()

    def audit_record(self, record: PatientRecord) -> List[AuditFinding]:
        """Run all compliance checks on a single patient record with duplicate suppression.

        Args:
            record: PatientRecord to evaluate.

        Returns:
            List of distinct, deduplicated AuditFinding instances.
        """
        raw_findings: List[AuditFinding] = []

        # 1. Missing fields & missing documentation
        raw_findings.extend(check_missing_fields(record, self.ref))

        # 2. Duplicate codes (ICD-10 & CPT)
        raw_findings.extend(identify_duplicate_codes(record, self.ref))

        # 3. Unverified reference codes (codes outside reference dictionary)
        raw_findings.extend(flag_unsupported_or_unverified_codes(record, self.ref))

        # 4. Code vs documented diagnosis mismatches (with negation awareness)
        raw_findings.extend(compare_diagnoses_with_mappings(record, self.ref))

        # 5. Unspecified code usage when specificity is documented
        raw_findings.extend(check_unspecified_code_usage(record, self.ref))

        # 6. Incomplete clinical documentation & missing signatures
        raw_findings.extend(identify_documentation_deficiencies(record, self.ref))

        # 7. Unsupported procedures and medical necessity (distinct issues)
        raw_findings.extend(check_unsupported_procedures(record, self.ref))

        # 8. Unsupported high-level E/M coding
        raw_findings.extend(check_unsupported_em_levels(record, self.ref))

        # Strict duplicate finding prevention:
        # Prevent emitting identical findings for the same encounter, code, and issue type
        deduped_findings: List[AuditFinding] = []
        seen_keys = set()
        for f in raw_findings:
            # Key uniquely identifies encounter, base code (without long desc), and issue category
            base_code = f.assigned_code.split(" (")[0].strip()
            dedup_key = (f.encounter_id, base_code, f.audit_issue)
            if dedup_key not in seen_keys:
                seen_keys.add(dedup_key)
                deduped_findings.append(f)

        return deduped_findings

    def audit_dataset(self, records: List[PatientRecord]) -> AuditSummary:
        """Audit an entire collection of patient records and build summary statistics.

        Args:
            records: List of PatientRecord objects.

        Returns:
            AuditSummary dataclass containing aggregated metrics and findings.
        """
        all_findings: List[AuditFinding] = []
        flagged_encounter_ids = set()
        coding_issues = 0
        doc_issues = 0

        for record in records:
            rec_findings = self.audit_record(record)
            if rec_findings:
                flagged_encounter_ids.add(record.encounter_id)
                for f in rec_findings:
                    all_findings.append(f)
                    if f.audit_issue in [
                        IssueType.INCOMPLETE_DOCUMENTATION.value,
                        IssueType.MISSING_PROVIDER_SIGNATURE.value,
                        IssueType.MISSING_CLINICAL_DOCUMENTATION.value,
                        IssueType.MISSING_REQUIRED_FIELD.value,
                        IssueType.MISSING_PROCEDURE_DOCUMENTATION.value
                    ]:
                        doc_issues += 1
                    else:
                        coding_issues += 1

        total = len(records)
        flagged = len(flagged_encounter_ids)
        clean = total - flagged

        high_count = sum(1 for f in all_findings if f.severity == AuditSeverity.HIGH)
        med_count = sum(1 for f in all_findings if f.severity == AuditSeverity.MEDIUM)
        low_count = sum(1 for f in all_findings if f.severity == AuditSeverity.LOW)

        return AuditSummary(
            total_records=total,
            records_reviewed=total,
            records_flagged=flagged,
            clean_records=clean,
            total_findings=len(all_findings),
            high_severity_count=high_count,
            medium_severity_count=med_count,
            low_severity_count=low_count,
            coding_issues_count=coding_issues,
            documentation_issues_count=doc_issues,
            findings=all_findings
        )


def load_records_from_csv(csv_path_or_buffer) -> List[PatientRecord]:
    """Parse patient records from CSV file path, buffer, or string.

    Supports case-insensitive headers and multiple column name aliases.

    Args:
        csv_path_or_buffer: Path to CSV or file-like buffer.

    Returns:
        List of populated PatientRecord instances.
    """
    df = pd.read_csv(csv_path_or_buffer)
    records: List[PatientRecord] = []

    # Map column headers case-insensitively and strip whitespace
    col_map = {str(col).strip().lower().replace(" ", "_"): col for col in df.columns}

    def get_val(row, target_names: List[str], default: str = "") -> str:
        for t in target_names:
            if t in col_map:
                val = row[col_map[t]]
                if pd.notna(val):
                    return str(val).strip()
        return default

    for _, row in df.iterrows():
        rec = PatientRecord(
            encounter_id=get_val(row, ["encounter_id", "record_id", "rec_id", "id"], default="UNKNOWN"),
            patient_id=get_val(row, ["patient_id", "pt_id", "patient"], default="UNKNOWN"),
            patient_age=get_val(row, ["patient_age", "age"], default="N/A"),
            patient_gender=get_val(row, ["patient_gender", "gender", "sex"], default="N/A"),
            encounter_date=get_val(row, ["encounter_date", "date", "service_date"], default=""),
            clinical_documentation=get_val(row, ["clinical_documentation", "documentation_notes", "notes", "chart_notes"], default=""),
            documented_diagnosis=get_val(row, ["documented_diagnosis", "diagnosis", "dx"], default=""),
            assigned_icd10=get_val(row, ["assigned_icd10", "icd10", "icd_10", "icd"], default=""),
            procedure_description=get_val(row, ["procedure_description", "procedure", "cpt_desc"], default=""),
            assigned_cpt=get_val(row, ["assigned_cpt", "cpt", "cpt_code"], default=""),
            documentation_completeness=get_val(row, ["documentation_completeness", "completeness"], default="Complete")
        )
        records.append(rec)

    return records
