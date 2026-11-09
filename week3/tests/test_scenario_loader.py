"""Unit tests for ScenarioLoader in Week 3."""

import os
import pytest
from week3.src.scenario_loader import ScenarioLoader
from week3.src.models import BillingScenario, ErrorSeverity, ResolutionStatus


@pytest.fixture
def loader():
    return ScenarioLoader()


def test_loader_initialization(loader):
    assert loader is not None
    assert "categories" in loader.error_categories
    assert "resolution_protocols" in loader.resolution_rules


def test_load_scenarios_from_csv(loader):
    scenarios = loader.load_scenarios_from_csv()
    assert len(scenarios) == 18
    assert all(isinstance(s, BillingScenario) for s in scenarios)


def test_scenario_field_types(loader):
    scenarios = loader.load_scenarios_from_csv()
    first = scenarios[0]
    assert first.scenario_id == "SCN-3001"
    assert first.encounter_id == "ENC-3001"
    assert isinstance(first.patient_age, int)
    assert isinstance(first.original_billed_amount, float)
    assert isinstance(first.error_severity, ErrorSeverity)
    assert isinstance(first.final_status, ResolutionStatus)
    assert isinstance(first.has_provider_signature, bool)


def test_missing_csv_file_raises_error(loader):
    with pytest.raises(FileNotFoundError):
        loader.load_scenarios_from_csv("non_existent_path.csv")


def test_category_metadata_lookup(loader):
    meta = loader.get_category_metadata("ERR_SIGNATURE_MISSING")
    assert meta["default_severity"] == "Critical"
    assert meta["responsible_department"] == "Clinical Providers"


def test_unknown_category_fallback(loader):
    meta = loader.get_category_metadata("UNKNOWN_KEY")
    assert meta["group"] == "General"
    assert meta["default_severity"] == "Medium"


def test_resolution_protocol_lookup(loader):
    proto = loader.get_resolution_protocol("ERR_DUPLICATE_BILLING")
    assert "steps" in proto
    assert len(proto["steps"]) >= 4
    assert proto["resolution_status"] == "Resolved – Corrected Claim"
