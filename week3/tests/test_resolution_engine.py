"""Unit tests for QueryResolutionEngine in Week 3."""

import pytest
from week3.src.scenario_loader import ScenarioLoader
from week3.src.error_detector import ErrorDetector
from week3.src.resolution_engine import ResolutionEngine
from week3.src.models import ResolutionStatus, QueryResolution


@pytest.fixture
def loader():
    return ScenarioLoader()


@pytest.fixture
def engine(loader):
    return ResolutionEngine(resolution_rules=loader.resolution_rules.get("resolution_protocols", {}))


@pytest.fixture
def detector(loader):
    return ErrorDetector(categories_meta=loader.error_categories.get("categories", {}))


@pytest.fixture
def scenarios(loader):
    return loader.load_scenarios_from_csv()


def test_resolve_corrected_claim(engine, detector, scenarios):
    s = next(s for s in scenarios if s.scenario_id == "SCN-3003")
    findings = detector.detect_errors(s)
    resolution = engine.resolve_query(s, findings)
    assert isinstance(resolution, QueryResolution)
    assert resolution.scenario_id == "SCN-3003"
    assert resolution.final_status == ResolutionStatus.RESOLVED_CORRECTED
    assert len(resolution.resolution_steps) >= 4
    assert len(resolution.required_evidence) >= 1
    assert "837P" in resolution.claim_action or "Corrected" in resolution.claim_action


def test_resolve_unauthenticated_note_signature(engine, detector, scenarios):
    s = next(s for s in scenarios if s.scenario_id == "SCN-3001")
    findings = detector.detect_errors(s)
    resolution = engine.resolve_query(s, findings)
    assert resolution.final_status == ResolutionStatus.RESOLVED_DOCS
    assert "signature" in resolution.provider_payer_communication.lower()


def test_resolve_pending_provider_query(engine, detector, scenarios):
    s = next(s for s in scenarios if s.scenario_id == "SCN-3008")
    findings = detector.detect_errors(s)
    resolution = engine.resolve_query(s, findings)
    assert resolution.final_status == ResolutionStatus.PENDING_PROVIDER


def test_resolve_compliant_case_no_error(engine, detector, scenarios):
    s = next(s for s in scenarios if s.scenario_id == "SCN-3017")
    findings = detector.detect_errors(s)
    resolution = engine.resolve_query(s, findings)
    assert resolution.final_status == ResolutionStatus.NO_ERROR
    assert "Release original claim" in resolution.claim_action or "Approve" in resolution.claim_action


def test_resolve_pending_additional_docs(engine, detector, scenarios):
    s = next(s for s in scenarios if s.scenario_id == "SCN-3018")
    findings = detector.detect_errors(s)
    resolution = engine.resolve_query(s, findings)
    assert resolution.final_status == ResolutionStatus.PENDING_DOCS
