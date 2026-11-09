"""Unit tests for PreventiveEngine in Week 3."""

import pytest
from week3.src.scenario_loader import ScenarioLoader
from week3.src.preventive_engine import PreventiveEngine
from week3.src.models import PreventiveControl


@pytest.fixture
def loader():
    return ScenarioLoader()


@pytest.fixture
def engine(loader):
    return PreventiveEngine(error_categories_meta=loader.error_categories.get("categories", {}))


@pytest.fixture
def scenarios(loader):
    return loader.load_scenarios_from_csv()


def test_get_control_by_code(engine):
    ctrl = engine.get_control_by_code("ERR_SIGNATURE_MISSING")
    assert isinstance(ctrl, PreventiveControl)
    assert ctrl.error_code == "ERR_SIGNATURE_MISSING"
    assert ctrl.ehr_hard_stop is True
    assert "Clinical" in ctrl.responsible_department


def test_get_control_for_all_scenarios(engine, scenarios):
    for s in scenarios:
        ctrl = engine.get_control_for_scenario(s)
        assert isinstance(ctrl, PreventiveControl)
        assert ctrl.error_code == s.error_category
        assert len(ctrl.control_name) > 0
        assert len(ctrl.responsible_department) > 0


def test_ehr_hard_stop_distribution(engine, scenarios):
    controls = [engine.get_control_for_scenario(s) for s in scenarios]
    hard_stops = [c for c in controls if c.ehr_hard_stop]
    # Significant portion of controls enforce hard-stops
    assert len(hard_stops) >= 5
