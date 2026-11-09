"""Unit tests for ErrorDetector in Week 3."""

import pytest
from week3.src.scenario_loader import ScenarioLoader
from week3.src.error_detector import ErrorDetector
from week3.src.models import ErrorSeverity


@pytest.fixture
def loader():
    return ScenarioLoader()


@pytest.fixture
def detector(loader):
    return ErrorDetector(categories_meta=loader.error_categories.get("categories", {}))


@pytest.fixture
def scenarios(loader):
    return loader.load_scenarios_from_csv()


def test_detect_signature_missing(detector, scenarios):
    s = next(s for s in scenarios if s.scenario_id == "SCN-3001")
    findings = detector.detect_errors(s)
    assert len(findings) >= 1
    f = next(f for f in findings if f.error_code == "ERR_SIGNATURE_MISSING")
    assert f.severity == ErrorSeverity.CRITICAL
    assert "Awaiting Clinician Signature" in f.evidence or "has_provider_signature is False" in f.evidence
    assert f.manual_review_required is True


def test_detect_duplicate_billing(detector, scenarios):
    s = next(s for s in scenarios if s.scenario_id == "SCN-3002")
    findings = detector.detect_errors(s)
    assert any(f.error_code == "ERR_DUPLICATE_BILLING" for f in findings)


def test_detect_cpt_incorrect_new_vs_established(detector, scenarios):
    s = next(s for s in scenarios if s.scenario_id == "SCN-3003")
    findings = detector.detect_errors(s)
    f = next(f for f in findings if f.error_code == "ERR_CPT_INCORRECT")
    assert "99385" in f.evidence
    assert "99395" in f.recommended_action


def test_detect_missing_procedure_documentation(detector, scenarios):
    s = next(s for s in scenarios if s.scenario_id == "SCN-3004")
    findings = detector.detect_errors(s)
    f = next(f for f in findings if f.error_code == "ERR_DOCUMENTATION_MISSING")
    assert "11102" in f.evidence


def test_detect_unsupported_em_level(detector, scenarios):
    s = next(s for s in scenarios if s.scenario_id == "SCN-3005")
    findings = detector.detect_errors(s)
    f = next(f for f in findings if f.error_code == "ERR_EM_UNSUPPORTED")
    assert "99215" in f.evidence
    assert "99213" in f.recommended_action


def test_detect_minor_as_subscriber(detector, scenarios):
    s = next(s for s in scenarios if s.scenario_id == "SCN-3006")
    findings = detector.detect_errors(s)
    f = next(f for f in findings if f.error_code == "ERR_SUBSCRIBER_INFO")
    assert "7 years old" in f.evidence or "minor" in f.reason_flagged.lower()


def test_detect_medical_necessity_gap(detector, scenarios):
    s = next(s for s in scenarios if s.scenario_id == "SCN-3007")
    findings = detector.detect_errors(s)
    f = next(f for f in findings if f.error_code == "ERR_MEDICAL_NECESSITY")
    assert "71046" in f.evidence


def test_detect_missing_hmo_referral(detector, scenarios):
    s = next(s for s in scenarios if s.scenario_id == "SCN-3008")
    findings = detector.detect_errors(s)
    f = next(f for f in findings if f.error_code == "ERR_AUTH_REFERRAL_MISSING")
    assert "HMO" in f.reason_flagged


def test_detect_cob_order(detector, scenarios):
    s = next(s for s in scenarios if s.scenario_id == "SCN-3009")
    findings = detector.detect_errors(s)
    f = next(f for f in findings if f.error_code == "ERR_COB_ROUTING")
    assert "Medicare Part B" in f.evidence


def test_detect_missing_modifier_25(detector, scenarios):
    s = next(s for s in scenarios if s.scenario_id == "SCN-3010")
    findings = detector.detect_errors(s)
    f = next(f for f in findings if f.error_code == "ERR_MODIFIER_APPLICATION")
    assert "Modifier -25" in f.error_name or "Modifier -25" in f.recommended_action


def test_detect_acute_trauma_as_chronic(detector, scenarios):
    s = next(s for s in scenarios if s.scenario_id == "SCN-3011")
    findings = detector.detect_errors(s)
    f = next(f for f in findings if f.error_code == "ERR_ICD_INCORRECT")
    assert "M23.23" in f.evidence
    assert "S83.241A" in f.recommended_action


def test_detect_diabetic_ckd_specificity(detector, scenarios):
    s = next(s for s in scenarios if s.scenario_id == "SCN-3012")
    findings = detector.detect_errors(s)
    f = next(f for f in findings if f.error_code == "ERR_ICD_SPECIFICITY")
    assert "E11.9" in f.evidence
    assert "E11.22" in f.recommended_action


def test_detect_mue_units_violation(detector, scenarios):
    s = next(s for s in scenarios if s.scenario_id == "SCN-3013")
    findings = detector.detect_errors(s)
    f = next(f for f in findings if f.error_code == "ERR_UNITS_QUANTITY")
    assert "96360" in f.evidence
    assert "4" in f.evidence


def test_detect_demographic_dob_typo(detector, scenarios):
    s = next(s for s in scenarios if s.scenario_id == "SCN-3014")
    findings = detector.detect_errors(s)
    f = next(f for f in findings if f.error_code == "ERR_DEMOGRAPHIC_TYPO")
    assert "birth" in f.evidence.lower() or "dob" in f.error_name.lower()


def test_detect_clearinghouse_edi_npi_rejection(detector, scenarios):
    s = next(s for s in scenarios if s.scenario_id == "SCN-3015")
    findings = detector.detect_errors(s)
    f = next(f for f in findings if f.error_code == "ERR_SUBMISSION_REJECTED")
    assert "NPI" in f.evidence or "2010AA" in f.evidence


def test_detect_balance_billing_calculation(detector, scenarios):
    s = next(s for s in scenarios if s.scenario_id == "SCN-3016")
    findings = detector.detect_errors(s)
    f = next(f for f in findings if f.error_code == "ERR_CALCULATION_BALANCE")
    assert "164.40" in f.evidence


def test_compliant_em_no_error(detector, scenarios):
    s = next(s for s in scenarios if s.scenario_id == "SCN-3017")
    findings = detector.detect_errors(s)
    assert len(findings) == 1
    f = findings[0]
    assert f.error_code == "QUERY_NO_ERROR"
    assert f.is_confirmed_error is False
    assert f.severity == ErrorSeverity.LOW


def test_pending_documentation_detection(detector, scenarios):
    s = next(s for s in scenarios if s.scenario_id == "SCN-3018")
    findings = detector.detect_errors(s)
    f = next(f for f in findings if f.error_code == "QUERY_PENDING_DOCS")
    assert f.is_confirmed_error is False
    assert "external" in f.reason_flagged.lower() or "outside" in f.evidence.lower()
