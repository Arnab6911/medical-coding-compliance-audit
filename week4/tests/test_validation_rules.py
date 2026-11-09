"""
Unit Tests for Week 4 Real-Time Pre-Bill Validation Framework
Tests rule classification, severity levels (HARD_STOP vs WARNING),
annual code set update governance schedules, and provider query guidelines.
"""

import pytest
from week4.src.validation_rules import ValidationRuleEngine

def test_validation_rule_inventory():
    engine = ValidationRuleEngine()
    assert len(engine.rules) == 12
    rule_ids = [r.rule_id for r in engine.rules]
    assert "RULE-01" in rule_ids
    assert "RULE-12" in rule_ids

def test_severity_classification_distribution():
    engine = ValidationRuleEngine()
    categorized = engine.get_rules_by_severity()
    assert len(categorized["HARD_STOP"]) == 9
    assert len(categorized["WARNING"]) == 3

    # Check key hard stops
    hard_stop_ids = [r.rule_id for r in categorized["HARD_STOP"]]
    assert "RULE-01" in hard_stop_ids  # Missing demographics
    assert "RULE-02" in hard_stop_ids  # Inactive insurance
    assert "RULE-03" in hard_stop_ids  # Invalid ICD-10
    assert "RULE-05" in hard_stop_ids  # Missing signature

    # Check warning review items
    warning_ids = [r.rule_id for r in categorized["WARNING"]]
    assert "RULE-06" in warning_ids  # Medical necessity / LCD
    assert "RULE-07" in warning_ids  # Level 5 E/M scrutiny

def test_code_governance_schedules():
    engine = ValidationRuleEngine()
    schedules = engine.get_code_governance_schedule()
    assert len(schedules) == 3
    
    cycles = [s["cycle"] for s in schedules]
    assert any("ICD-10-CM" in c for c in cycles)
    assert any("CPT" in c for c in cycles)
    assert any("NCCI" in c for c in cycles)

def test_ethical_provider_query_guideline():
    engine = ValidationRuleEngine()
    query_guide = engine.format_provider_query_guideline()
    assert "non-leading" in query_guide["policy_title"].lower() or any("non-leading" in p.lower() for p in query_guide["core_principles"])
    assert len(query_guide["core_principles"]) >= 4
