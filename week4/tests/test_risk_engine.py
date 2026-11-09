"""
Unit Tests for Week 4 Risk Assessment Engine
Tests 5x5 matrix calculations, risk score boundaries, severity tiers,
and category distributions for 12 integration risks.
"""

import pytest
from week4.src.risk_engine import RiskEngine

def test_risk_register_loading():
    engine = RiskEngine()
    assert len(engine.risks) == 12
    risk_ids = [r.risk_id for r in engine.risks]
    assert "RSK-01" in risk_ids
    assert "RSK-12" in risk_ids

def test_risk_scores_and_levels():
    engine = RiskEngine()
    for r in engine.risks:
        assert 1 <= r.likelihood <= 5
        assert 1 <= r.impact <= 5
        assert r.risk_score == r.likelihood * r.impact
        if r.risk_score >= 15:
            assert r.risk_level == "Critical"
        elif r.risk_score >= 10:
            assert r.risk_level == "High"
        elif r.risk_score >= 5:
            assert r.risk_level == "Medium"
        else:
            assert r.risk_level == "Low"

def test_risk_summary_metrics():
    engine = RiskEngine()
    summary = engine.get_summary_metrics()
    assert summary["total_risks"] == 12
    assert summary["average_risk_score"] > 0
    assert summary["distribution_by_level"]["Critical"] >= 1
    assert summary["distribution_by_level"]["High"] >= 1
    assert len(summary["top_risks"]) == 5

def test_matrix_grid_mapping():
    engine = RiskEngine()
    grid = engine.get_matrix_grid()
    assert len(grid) == 25
    # Total risks across grid cells should equal 12
    plotted_total = sum(len(r_list) for r_list in grid.values())
    assert plotted_total == 12
