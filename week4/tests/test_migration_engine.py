"""
Unit Tests for Week 4 Data Migration Engine
Tests ETL validation, date standardization, duplicate patient chart detection,
and 100% census financial accounts receivable balance reconciliation ($0.00 variance).
"""

import pytest
from week4.src.migration_engine import MigrationEngine

def test_migration_dataset_loading():
    eng = MigrationEngine()
    assert len(eng.records) == 20
    patient_ids = [r.legacy_patient_id for r in eng.records]
    assert "LEG-1001" in patient_ids
    assert "LEG-1020" in patient_ids

def test_migration_cleansing_and_formatting():
    eng = MigrationEngine()
    val = eng.run_validation()
    assert val["total_records"] == 20
    assert val["clean_records"] == 16
    assert val["cleansed_records"] == 2
    assert val["cleansing_success_rate"] == 100.0
    assert len(val["formatting_issues"]) == 0

def test_mpi_duplicate_detection():
    eng = MigrationEngine()
    duplicates = eng.detect_duplicates()
    assert len(duplicates) >= 1
    
    # Check that Robert Banner and Bob Banner are detected
    match = duplicates[0]
    assert match["primary_id"] == "LEG-1019"
    assert match["duplicate_id"] == "LEG-1020"
    assert "Robert Banner" in match["primary_name"]
    assert "Bob Banner" in match["duplicate_name"]

def test_financial_reconciliation_zero_variance():
    eng = MigrationEngine()
    rec = eng.reconcile_financials()
    
    assert rec["total_account_count"] == 20
    assert rec["total_legacy_ar"] == 14110.00
    assert rec["total_migrated_ar"] == 14110.00
    assert rec["net_variance"] == 0.00
    assert rec["is_balanced"] is True
    assert rec["reconciliation_rate"] == 100.0
