"""
Unit Tests for Week 4 Software Evaluator
Tests vendor comparison dataset, verification classifications,
criteria weight calculations, and illustrative selection scoring.
"""

import pytest
from pathlib import Path
from week4.src.software_evaluator import SoftwareEvaluator

def test_software_comparison_loading():
    evaluator = SoftwareEvaluator()
    assert len(evaluator.features) == 18
    feature_ids = [f.feature_id for f in evaluator.features]
    assert "FEAT-01" in feature_ids
    assert "FEAT-18" in feature_ids

def test_feature_verification_classification():
    evaluator = SoftwareEvaluator()
    summary = evaluator.get_feature_matrix_summary()
    assert summary["total_features"] == 18
    # Athenahealth: verified >= 15, requires confirmation >= 1, not verified == 0
    assert summary["athenahealth"]["verified"] >= 15
    assert summary["athenahealth"]["not_verified"] == 0
    # AdvancedMD
    assert summary["advancedmd"]["verified"] >= 15
    assert summary["advancedmd"]["not_verified"] == 0
    # Tebra
    assert summary["tebra"]["verified"] >= 15
    assert summary["tebra"]["not_verified"] == 0

def test_criteria_weights_sum_to_one():
    evaluator = SoftwareEvaluator()
    assert len(evaluator.criteria) == 10
    total_weight = sum(c.weight for c in evaluator.criteria)
    assert abs(total_weight - 1.0) < 0.001

def test_scoring_calculation_and_ranking():
    evaluator = SoftwareEvaluator()
    results = evaluator.calculate_scores()
    
    assert "recommended_vendor" in results
    assert results["recommended_vendor"] == "athenahealth athenaOne"
    assert results["recommended_score"] > 9.0
    
    scores = results["vendor_scores"]
    assert scores["athenahealth athenaOne"] > scores["AdvancedMD"]
    assert scores["AdvancedMD"] > scores["Tebra"]
    assert len(results["ranked_vendors"]) == 3

def test_dynamic_weight_override():
    evaluator = SoftwareEvaluator()
    # Change weights so cost is 50% and billing is 50%
    custom_weights = {
        "CRIT-01": 0.50,
        "CRIT-10": 0.50
    }
    # Remaining set to 0
    for c in evaluator.criteria:
        if c.criterion_id not in custom_weights:
            custom_weights[c.criterion_id] = 0.0

    evaluator.update_weights(custom_weights)
    results = evaluator.calculate_scores()
    assert abs(results["total_weight"] - 1.0) < 0.001
