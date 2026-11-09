"""Unit tests for financial reconciliation and consistency in Week 3."""

import pytest
from week3.src.scenario_loader import ScenarioLoader
from week3.src.workflow import BillingResolutionWorkflow


@pytest.fixture
def loader():
    return ScenarioLoader()


@pytest.fixture
def scenarios(loader):
    return loader.load_scenarios_from_csv()


@pytest.fixture
def workflow_results():
    wf = BillingResolutionWorkflow()
    return wf.run_simulation()


def test_scenario_count(scenarios):
    assert len(scenarios) == 18


def test_cohort_gross_financial_totals(scenarios):
    total_original = sum(s.original_billed_amount for s in scenarios)
    total_corrected = sum(s.corrected_billed_amount for s in scenarios)
    total_variance = sum(s.variance_amount for s in scenarios)

    assert round(total_original, 2) == 5440.00
    assert round(total_corrected, 2) == 4345.00
    assert round(total_variance, 2) == -1095.00
    assert round(total_original - total_corrected, 2) == round(abs(total_variance), 2)


def test_individual_charge_adjustments(scenarios):
    sc_map = {s.scenario_id: s for s in scenarios}

    # SCN-3003: 99385 -> 99395
    assert sc_map["SCN-3003"].original_billed_amount == 240.00
    assert sc_map["SCN-3003"].corrected_billed_amount == 205.00
    assert sc_map["SCN-3003"].variance_amount == -35.00

    # SCN-3004: Remove CPT 11102
    assert sc_map["SCN-3004"].original_billed_amount == 130.00
    assert sc_map["SCN-3004"].corrected_billed_amount == 65.00
    assert sc_map["SCN-3004"].variance_amount == -65.00

    # SCN-3005: 99215 -> 99213
    assert sc_map["SCN-3005"].original_billed_amount == 395.00
    assert sc_map["SCN-3005"].corrected_billed_amount == 185.00
    assert sc_map["SCN-3005"].variance_amount == -210.00

    # SCN-3007: Remove CPT 71046
    assert sc_map["SCN-3007"].original_billed_amount == 495.00
    assert sc_map["SCN-3007"].corrected_billed_amount == 275.00
    assert sc_map["SCN-3007"].variance_amount == -220.00

    # SCN-3011: 99214 ($360) -> 99213 ($185)
    assert sc_map["SCN-3011"].original_billed_amount == 360.00
    assert sc_map["SCN-3011"].corrected_billed_amount == 185.00
    assert sc_map["SCN-3011"].variance_amount == -175.00

    # SCN-3013: 4 units -> 1 unit
    assert sc_map["SCN-3013"].original_billed_amount == 520.00
    assert sc_map["SCN-3013"].corrected_billed_amount == 130.00
    assert sc_map["SCN-3013"].variance_amount == -390.00


def test_zero_variance_scenarios(scenarios):
    zero_var_ids = [
        "SCN-3001", "SCN-3002", "SCN-3006", "SCN-3008", "SCN-3009",
        "SCN-3010", "SCN-3012", "SCN-3014", "SCN-3015", "SCN-3016",
        "SCN-3017", "SCN-3018"
    ]
    sc_map = {s.scenario_id: s for s in scenarios}
    for sid in zero_var_ids:
        s = sc_map[sid]
        assert s.variance_amount == 0.00
        assert s.original_billed_amount == s.corrected_billed_amount


def test_workflow_batch_metrics_reconciliation(workflow_results):
    scenarios, findings, rcas, resolutions, controls, metrics = workflow_results
    assert metrics.total_scenarios == 18
    assert metrics.total_original_gross_billed == 5440.00
    assert metrics.total_corrected_gross_billed == 4345.00
    assert metrics.total_financial_variance == -1095.00
    assert metrics.clean_resolution_rate > 80.0
