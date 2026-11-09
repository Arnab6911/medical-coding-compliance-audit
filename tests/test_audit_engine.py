"""Unit tests for the Medical Coding Compliance Audit Engine.

Validates:
1. CSV loading with complete schema (Encounter ID, age, gender, completeness).
2. Missing field detection (empty diagnosis, missing clinical notes, missing date).
3. Duplicate code detection (ICD-10 and CPT duplicates).
4. Unverified code detection (codes outside active reference standards).
5. Comprehensive audit findings generation and summary metrics.
6. 14-section Word compliance report generation (.docx).
7. Specific audit rule accuracy and non-modification guarantees.
8. Duplicate finding prevention (preventing identical findings for the same code).
9. Statistical consistency across audit engine, CSV export, and Word report.
10. Clinical negation awareness (preventing false-positive keyword matching).
"""

import io
import pandas as pd
import pytest
import docx

from src.models import PatientRecord, AuditSeverity, IssueType, AuditSummary
from src.rules_engine import (
    AuditEngine,
    load_records_from_csv,
    check_missing_fields,
    identify_duplicate_codes,
    flag_unsupported_or_unverified_codes,
    compare_diagnoses_with_mappings,
    identify_documentation_deficiencies,
    check_unsupported_procedures,
    check_unsupported_em_levels,
    check_unspecified_code_usage,
    is_negated_in_text
)
from src.reference_data import get_reference_manager
from src.report_generator import ComplianceReportGenerator


@pytest.fixture
def ref():
    """Provides ReferenceDataManager singleton."""
    return get_reference_manager()


@pytest.fixture
def engine(ref):
    """Provides initialized AuditEngine."""
    return AuditEngine(ref)


# -----------------------------------------------------------------------------
# 1. CSV LOADING TESTS
# -----------------------------------------------------------------------------

def test_csv_loading():
    """Test loading fictional dataset from CSV, validating row counts and required fields."""
    records = load_records_from_csv("data/sample_records.csv")
    assert len(records) >= 15, "Dataset must contain at least 15 encounter records"
    assert len(records) == 20, "Sample dataset expected to contain exactly 20 records"

    first = records[0]
    assert first.encounter_id.startswith("ENC-")
    assert first.patient_id.startswith("PT-")
    assert first.patient_age != "N/A"
    assert first.patient_gender in ["Female", "Male", "Other"]
    assert first.encounter_date != ""
    assert len(first.clinical_documentation) > 0
    assert first.documented_diagnosis != ""
    assert first.assigned_icd10 != ""
    assert first.assigned_cpt != ""
    assert first.documentation_completeness in ["Complete", "Incomplete", "Terse", "Missing Notes"]


# -----------------------------------------------------------------------------
# 2. MISSING FIELD DETECTION TESTS
# -----------------------------------------------------------------------------

def test_missing_field_detection(ref):
    """Test detection of missing required administrative and clinical fields."""
    # Test completely missing clinical documentation notes
    rec_no_notes = PatientRecord(
        encounter_id="ENC-TEST-NONOTES",
        patient_id="PT-TEST-01",
        patient_age="45",
        patient_gender="Male",
        encounter_date="2024-03-01",
        clinical_documentation="",
        documented_diagnosis="Essential hypertension",
        assigned_icd10="I10",
        procedure_description="Office visit",
        assigned_cpt="99213",
        documentation_completeness="Missing Notes"
    )
    findings_no_notes = check_missing_fields(rec_no_notes, ref)
    issues = [f.audit_issue for f in findings_no_notes]
    assert IssueType.MISSING_CLINICAL_DOCUMENTATION.value in issues
    assert any(f.severity == AuditSeverity.HIGH for f in findings_no_notes)
    # Ensure reason does not accuse provider of fraud
    assert "not assumption of intentional miscoding" in findings_no_notes[0].reason

    # Test missing documented diagnosis with assigned ICD-10
    rec_no_dx = PatientRecord(
        encounter_id="ENC-TEST-NODX",
        patient_id="PT-TEST-02",
        patient_age="50",
        patient_gender="Female",
        encounter_date="2024-03-01",
        clinical_documentation="Follow-up visit. BP 120/80 mmHg. Signed by Dr. Smith, MD.",
        documented_diagnosis="",
        assigned_icd10="I10",
        procedure_description="Office visit",
        assigned_cpt="99213"
    )
    findings_no_dx = check_missing_fields(rec_no_dx, ref)
    issues_dx = [f.audit_issue for f in findings_no_dx]
    assert IssueType.MISSING_DIAGNOSIS.value in issues_dx
    assert any(f.severity == AuditSeverity.HIGH for f in findings_no_dx)

    # Test missing encounter date
    rec_no_date = PatientRecord(
        encounter_id="ENC-TEST-NODATE",
        patient_id="PT-TEST-03",
        patient_age="30",
        patient_gender="Male",
        encounter_date="",
        clinical_documentation="Routine checkup. Signed by Dr. Smith, MD.",
        documented_diagnosis="Essential hypertension",
        assigned_icd10="I10",
        procedure_description="Office visit",
        assigned_cpt="99213"
    )
    findings_no_date = check_missing_fields(rec_no_date, ref)
    issues_date = [f.audit_issue for f in findings_no_date]
    assert IssueType.MISSING_REQUIRED_FIELD.value in issues_date


# -----------------------------------------------------------------------------
# 3. DUPLICATE CODE DETECTION TESTS
# -----------------------------------------------------------------------------

def test_duplicate_code_detection(ref):
    """Test identification of duplicate ICD-10 and CPT codes on the same encounter."""
    rec = PatientRecord(
        encounter_id="ENC-TEST-DUP",
        patient_id="PT-TEST-04",
        patient_age="60",
        patient_gender="Male",
        encounter_date="2024-03-01",
        clinical_documentation="Follow up. Signed by Dr. Mark Davis, MD.",
        documented_diagnosis="Essential hypertension; Essential hypertension",
        assigned_icd10="I10; I10",
        procedure_description="Office visit; Office visit",
        assigned_cpt="99213; 99213"
    )
    findings = identify_duplicate_codes(rec, ref)
    issues = [f.audit_issue for f in findings]
    assert IssueType.DUPLICATE_DIAGNOSIS.value in issues
    assert IssueType.DUPLICATE_PROCEDURE.value in issues
    assert any(f.assigned_code == "I10" for f in findings)
    assert any("99213" in f.assigned_code for f in findings)


# -----------------------------------------------------------------------------
# 4. UNVERIFIED CODE DETECTION TESTS
# -----------------------------------------------------------------------------

def test_unverified_code_detection(ref):
    """Test that codes not verified in active reference codebooks are explicitly flagged."""
    rec = PatientRecord(
        encounter_id="ENC-TEST-UNVERIFIED",
        patient_id="PT-TEST-05",
        patient_age="55",
        patient_gender="Female",
        encounter_date="2024-03-01",
        clinical_documentation="General fatigue evaluation. Signed by Dr. Elena Ramos, MD.",
        documented_diagnosis="Fatigue syndrome",
        assigned_icd10="Z99.999",
        procedure_description="Office visit",
        assigned_cpt="99212"
    )
    findings = flag_unsupported_or_unverified_codes(rec, ref)
    unverified = [f for f in findings if f.audit_issue == IssueType.UNVERIFIED_CODE.value]
    assert len(unverified) >= 1
    assert unverified[0].severity == AuditSeverity.MEDIUM
    assert "not verified" in unverified[0].reason.lower()
    assert "manual verification" in unverified[0].reason.lower()


# -----------------------------------------------------------------------------
# 5. AUDIT FINDINGS GENERATION & SUMMARY METRICS TESTS
# -----------------------------------------------------------------------------

def test_audit_findings_generation(engine):
    """Test full dataset audit execution, summary counts, and metric formulas."""
    records = load_records_from_csv("data/sample_records.csv")
    summary = engine.audit_dataset(records)

    assert isinstance(summary, AuditSummary)
    assert summary.total_records == 20
    assert summary.records_flagged > 0
    assert summary.clean_records > 0
    assert summary.total_records == summary.records_flagged + summary.clean_records
    assert summary.total_findings > 0

    # Severity distribution checks
    assert summary.high_severity_count > 0
    assert summary.medium_severity_count > 0
    assert summary.low_severity_count > 0
    assert summary.total_findings == (
        summary.high_severity_count + summary.medium_severity_count + summary.low_severity_count
    )

    # Coding vs Documentation breakdown
    assert summary.coding_issues_count > 0
    assert summary.documentation_issues_count > 0

    # Percentage formulas
    assert summary.compliance_rate == round((summary.clean_records / summary.total_records) * 100, 1)
    assert summary.review_rate == round((summary.records_flagged / summary.total_records) * 100, 1)
    assert round(summary.compliance_rate + summary.review_rate, 1) == 100.0


# -----------------------------------------------------------------------------
# 6. REPORT GENERATION TESTS
# -----------------------------------------------------------------------------

def test_report_generation(engine):
    """Test generating 14-section Word compliance audit report via python-docx."""
    records = load_records_from_csv("data/sample_records.csv")
    summary = engine.audit_dataset(records)

    generator = ComplianceReportGenerator(summary, records=records)
    stream = generator.generate()

    assert isinstance(stream, io.BytesIO)
    content = stream.getvalue()
    assert len(content) > 20000, "Generated Word report must contain substantial content"
    assert content.startswith(b"PK"), "Report must start with standard docx zip signature"

    doc = docx.Document(stream)
    headings = [p.text.strip() for p in doc.paragraphs if p.style.name.startswith("Heading 1")]

    expected_sections = [
        "2. Executive Summary",
        "3. Introduction",
        "4. Objectives",
        "5. Scope & Limitations",
        "6. Audit Methodology",
        "7. Coding Compliance Criteria",
        "8. Dataset Description",
        "9. Detailed Audit Findings with Encounter IDs",
        "10. Issue-Wise Explanations",
        "11. Corrective Actions",
        "12. Preventive Recommendations",
        "13. Conclusion",
        "14. References"
    ]
    for sec in expected_sections:
        assert any(sec in h for h in headings), f"Missing expected report section: {sec}"


# -----------------------------------------------------------------------------
# 7. SPECIFIC AUDIT RULE TESTS
# -----------------------------------------------------------------------------

def test_clean_record_passes_without_findings(engine):
    """Verify compliant, well-documented encounter produces zero findings."""
    clean_rec = PatientRecord(
        encounter_id="ENC-TEST-CLEAN",
        patient_id="PT-TEST-CLEAN",
        patient_age="58",
        patient_gender="Female",
        encounter_date="2024-03-12",
        clinical_documentation="Patient presents for routine 6-month blood pressure follow-up. Current BP 128/82 mmHg. Reports taking amlodipine 5mg daily with good compliance and no side effects. Normal cardiovascular exam, regular rate and rhythm, no peripheral edema. Plan: Continue current medication regimen. Recheck in 6 months. Electronically signed by Dr. Sarah Jenkins, MD.",
        documented_diagnosis="Essential hypertension",
        assigned_icd10="I10",
        procedure_description="Office visit established patient low MDM",
        assigned_cpt="99213",
        documentation_completeness="Complete"
    )
    findings = engine.audit_record(clean_rec)
    assert len(findings) == 0


def test_diagnosis_code_mismatch(engine):
    """Verify diagnosis conflicts with assigned code (e.g. Hypertension vs Diabetes)."""
    rec = PatientRecord(
        encounter_id="ENC-TEST-MISMATCH",
        patient_id="PT-TEST-MISMATCH",
        patient_age="64",
        patient_gender="Male",
        encounter_date="2024-03-12",
        clinical_documentation="Patient seen for blood pressure check. Blood pressure 134/86 mmHg. Reports compliant with lisinopril. Lungs clear, cardiac exam normal. Electronically signed by Dr. Mark Davis, MD.",
        documented_diagnosis="Essential hypertension",
        assigned_icd10="E11.9",
        procedure_description="Office visit established patient low MDM",
        assigned_cpt="99213",
        documentation_completeness="Complete"
    )
    findings = engine.audit_record(rec)
    mismatches = [f for f in findings if f.audit_issue == IssueType.CODE_MISMATCH.value]
    assert len(mismatches) == 1
    assert mismatches[0].severity == AuditSeverity.HIGH
    assert mismatches[0].code_set_year == "FY 2024"


def test_unsupported_procedure_and_medical_necessity(engine):
    """Verify colonoscopy billed for acute pharyngitis is flagged for lack of medical necessity."""
    rec = PatientRecord(
        encounter_id="ENC-TEST-PROC",
        patient_id="PT-TEST-PROC",
        patient_age="31",
        patient_gender="Female",
        encounter_date="2024-03-14",
        clinical_documentation="Patient complains of sore throat for 2 days. Pharynx red. Rapid strep negative. Saline gargles advised. Electronically signed by Dr. Sarah Jenkins, MD.",
        documented_diagnosis="Acute pharyngitis",
        assigned_icd10="J02.9",
        procedure_description="Diagnostic flexible colonoscopy",
        assigned_cpt="45378",
        documentation_completeness="Complete"
    )
    findings = engine.audit_record(rec)
    issues = [f.audit_issue for f in findings]
    assert IssueType.UNSUPPORTED_PROCEDURE.value in issues
    assert IssueType.MISSING_PROCEDURE_DOCUMENTATION.value in issues


def test_unsupported_high_level_em(engine):
    """Verify Level 5 E/M (99215) billed for minor complaint without MDM or time is flagged."""
    rec = PatientRecord(
        encounter_id="ENC-TEST-EM5",
        patient_id="PT-TEST-EM5",
        patient_age="46",
        patient_gender="Male",
        encounter_date="2024-04-01",
        clinical_documentation="Patient complains of lower back ache after gardening over the weekend. Straight leg raise negative. Prescribed cyclobenzaprine and advised core stretches. Electronically signed by Dr. Robert Vance, MD.",
        documented_diagnosis="Low back pain",
        assigned_icd10="M54.50",
        procedure_description="Office visit established patient high MDM",
        assigned_cpt="99215",
        documentation_completeness="Complete"
    )
    findings = engine.audit_record(rec)
    em_flags = [f for f in findings if f.audit_issue == IssueType.UNSUPPORTED_EM_LEVEL.value]
    assert len(em_flags) == 1
    assert em_flags[0].severity == AuditSeverity.HIGH


def test_missing_provider_signature(engine):
    """Verify note lacking authenticated clinician signature is flagged."""
    rec = PatientRecord(
        encounter_id="ENC-TEST-SIG",
        patient_id="PT-TEST-SIG",
        patient_age="28",
        patient_gender="Female",
        encounter_date="2024-03-22",
        clinical_documentation="Patient presents with 2 days of dysuria and frequency. In-office urinalysis shows positive nitrites and leukocyte esterase. Prescribed nitrofurantoin.",
        documented_diagnosis="Urinary tract infection",
        assigned_icd10="N39.0",
        procedure_description="Office visit established patient low MDM",
        assigned_cpt="99213",
        documentation_completeness="Incomplete"
    )
    findings = engine.audit_record(rec)
    sig_flags = [f for f in findings if f.audit_issue == IssueType.MISSING_PROVIDER_SIGNATURE.value]
    assert len(sig_flags) == 1
    assert sig_flags[0].severity == AuditSeverity.MEDIUM


def test_record_immutability(engine):
    """Audit engine must NEVER modify patient record attributes."""
    orig_code = "I10"
    orig_diag = "Essential hypertension"
    rec = PatientRecord(
        encounter_id="ENC-TEST-IMMUTABLE",
        patient_id="PT-TEST-IMMUTABLE",
        patient_age="55",
        patient_gender="Male",
        encounter_date="2024-03-01",
        clinical_documentation="BP 130/80 mmHg. Electronically signed by Dr. Smith, MD.",
        documented_diagnosis=orig_diag,
        assigned_icd10=orig_code,
        procedure_description="Office visit",
        assigned_cpt="99213",
        documentation_completeness="Complete"
    )
    engine.audit_record(rec)
    assert rec.assigned_icd10 == orig_code
    assert rec.documented_diagnosis == orig_diag


# -----------------------------------------------------------------------------
# 8. DUPLICATE FINDING PREVENTION TESTS (ENC-1003 & DEDUPLICATION)
# -----------------------------------------------------------------------------

def test_duplicate_finding_prevention(engine):
    """Verify that duplicate identical findings for the same code and issue are prevented.

    In ENC-1003, colonoscopy has two distinct issues:
    1. Missing Procedure Documentation (no operative note in chart)
    2. Unsupported Procedure Medical Necessity (pharyngitis does not justify colonoscopy)
    They must be distinctly categorized and must NOT emit duplicate identical entries.
    """
    records = load_records_from_csv("data/sample_records.csv")
    enc_1003 = next(r for r in records if r.encounter_id == "ENC-1003")
    findings = engine.audit_record(enc_1003)

    # Check for distinct issue categories
    issue_types = [f.audit_issue for f in findings]
    assert len(issue_types) == len(set(issue_types)), "All findings on ENC-1003 must be distinct issue categories"
    assert IssueType.MISSING_PROCEDURE_DOCUMENTATION.value in issue_types
    assert IssueType.UNSUPPORTED_PROCEDURE.value in issue_types

    # Ensure no exact duplicate tuple exists across any encounter in the sample dataset
    summary = engine.audit_dataset(records)
    seen_tuples = set()
    for f in summary.findings:
        base_code = f.assigned_code.split(" (")[0].strip()
        tup = (f.encounter_id, base_code, f.audit_issue)
        assert tup not in seen_tuples, f"Duplicate finding emitted for {tup}"
        seen_tuples.add(tup)


# -----------------------------------------------------------------------------
# 9. STATISTICAL CONSISTENCY ACROSS ENGINE, CSV, AND WORD REPORT
# -----------------------------------------------------------------------------

def test_consistency_report_statistics_and_audit_results(engine):
    """Verify that Word report, CSV export, and engine summary counts are identical."""
    records = load_records_from_csv("data/sample_records.csv")
    summary = engine.audit_dataset(records)

    # 1. Verify summary internal mathematical consistency
    assert summary.total_records == summary.records_flagged + summary.clean_records
    assert summary.total_findings == len(summary.findings)
    assert summary.total_findings == (
        summary.high_severity_count + summary.medium_severity_count + summary.low_severity_count
    )

    # 2. Verify CSV findings match summary
    df = pd.DataFrame([f.to_dict() for f in summary.findings])
    assert len(df) == summary.total_findings
    assert (df["Severity"] == "High").sum() == summary.high_severity_count
    assert (df["Severity"] == "Medium").sum() == summary.medium_severity_count
    assert (df["Severity"] == "Low").sum() == summary.low_severity_count
    assert (df["Manual Review Required"] == "Yes").all(), "All findings must require human review"

    # 3. Verify Word Report findings table rows match summary
    generator = ComplianceReportGenerator(summary, records=records)
    stream = generator.generate()
    doc = docx.Document(stream)

    findings_table = None
    for tbl in doc.tables:
        if len(tbl.rows) > 0 and tbl.rows[0].cells[0].text.strip() == "Encounter ID":
            findings_table = tbl
            break

    assert findings_table is not None, "Word report must contain Section 9 findings table"
    assert len(findings_table.rows) - 1 == summary.total_findings, (
        f"Findings table rows ({len(findings_table.rows) - 1}) must match summary.total_findings ({summary.total_findings})"
    )


# -----------------------------------------------------------------------------
# 10. CLINICAL NEGATION AWARENESS TESTS
# -----------------------------------------------------------------------------

def test_clinical_negation_awareness(engine):
    """Verify that diagnoses mentioned only in a negative context are not falsely matched."""
    # Note states 'No history of diabetes mellitus' while documenting 'Essential hypertension'
    rec_negated = PatientRecord(
        encounter_id="ENC-TEST-NEGATION",
        patient_id="PT-TEST-NEG",
        patient_age="52",
        patient_gender="Female",
        encounter_date="2024-03-01",
        clinical_documentation="Patient presents for blood pressure evaluation. BP 130/80 mmHg. No history of diabetes mellitus. Compliant with lisinopril. Electronically signed by Dr. Mark Davis, MD.",
        documented_diagnosis="Essential hypertension",
        assigned_icd10="E11.9", # Diabetes code assigned!
        procedure_description="Office visit",
        assigned_cpt="99213",
        documentation_completeness="Complete"
    )
    findings = engine.audit_record(rec_negated)
    mismatches = [f for f in findings if f.audit_issue == IssueType.CODE_MISMATCH.value]
    assert len(mismatches) == 1, (
        "Negated mention 'No history of diabetes' must not be treated as a positive match for diabetes code E11.9"
    )
