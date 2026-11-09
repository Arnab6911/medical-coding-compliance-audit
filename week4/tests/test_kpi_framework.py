"""
Unit Tests for Week 4 KPI Framework
Tests 11 post-implementation RCM metrics, formulas, baseline/target values,
and proposed project target designations.
"""

import json
import pytest
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def test_kpi_definitions_file_exists():
    filepath = DATA_DIR / "kpi_definitions.json"
    assert filepath.exists()
    with open(filepath, "r", encoding="utf-8") as f:
        kpis = json.load(f)
    assert len(kpis) == 11

def test_kpi_metric_attributes():
    filepath = DATA_DIR / "kpi_definitions.json"
    with open(filepath, "r", encoding="utf-8") as f:
        kpis = json.load(f)

    for k in kpis:
        assert "kpi_id" in k
        assert "name" in k
        assert "category" in k
        assert "formula" in k
        assert "baseline_value" in k
        assert "target_value" in k
        assert "unit" in k
        assert "measurement_frequency" in k
        assert k["status_target"] == "Proposed Project Target"

def test_core_financial_targets():
    filepath = DATA_DIR / "kpi_definitions.json"
    with open(filepath, "r", encoding="utf-8") as f:
        kpis = {k["kpi_id"]: k for k in json.load(f)}

    # Exactly 11 unique KPI IDs
    assert len(kpis) == 11
    # KPI-01: First-pass acceptance rate
    assert kpis["KPI-01"]["target_value"] >= 95.0
    # KPI-02: Denial rate is dollar-weighted
    assert "Dollar-Weighted" in kpis["KPI-02"]["name"]
    assert kpis["KPI-02"]["target_value"] <= 5.0
    assert kpis["KPI-02"].get("target_display") == "<5.0%"
    # KPI-03: Days in AR
    assert kpis["KPI-03"]["target_value"] <= 35.0
    # KPI-09: Staff training baseline is "Not measured"
    assert kpis["KPI-09"]["baseline_value"] == "Not measured"
    assert kpis["KPI-09"]["target_value"] == 100.0
    # KPI-11: Data migration financial reconciliation rate baseline is "Not measured"
    assert kpis["KPI-11"]["baseline_value"] == "Not measured"
    assert kpis["KPI-11"]["target_value"] == 100.0
