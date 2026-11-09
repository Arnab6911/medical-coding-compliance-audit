"""Scenario loader and schema validator for Week 3 billing error simulation."""

import os
import json
import pandas as pd
from typing import Dict, List, Optional, Any

from .models import BillingScenario, ErrorSeverity, ResolutionStatus


class ScenarioLoader:
    """Loads and validates fictional billing scenarios and reference configuration rules."""

    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(base_dir, "data")

        self.data_dir = data_dir
        self.rules_dir = os.path.join(data_dir, "reference_rules")
        self.error_categories = self._load_json(os.path.join(self.rules_dir, "error_categories.json"))
        self.resolution_rules = self._load_json(os.path.join(self.rules_dir, "resolution_rules.json"))

    def _load_json(self, file_path: str) -> Dict[str, Any]:
        """Safely load JSON configuration file."""
        if not os.path.exists(file_path):
            return {}
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_scenarios_from_csv(self, csv_path: Optional[str] = None) -> List[BillingScenario]:
        """Parse, validate, and instantiate BillingScenario objects from CSV."""
        if csv_path is None:
            csv_path = os.path.join(self.data_dir, "billing_scenarios.csv")

        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Billing scenarios file not found at: {csv_path}")

        df = pd.read_csv(csv_path)

        # Validate mandatory schema columns
        required_cols = [
            "scenario_id", "encounter_id", "patient_id", "patient_name",
            "date_of_service", "payer_name", "plan_type", "clinical_documentation",
            "original_icd10", "original_cpt", "original_billed_amount",
            "billing_query", "error_category", "error_severity", "root_cause",
            "evidence_required", "recommended_action", "final_status",
            "preventive_measure", "manual_review_required"
        ]
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise ValueError(f"Scenario CSV is missing required columns: {missing}")

        scenarios: List[BillingScenario] = []

        for _, row in df.iterrows():
            # Parse booleans safely
            def to_bool(val: Any, default: bool = True) -> bool:
                if pd.isna(val):
                    return default
                if isinstance(val, bool):
                    return val
                return str(val).strip().lower() in ["true", "1", "yes"]

            # Parse severity
            raw_sev = str(row.get("error_severity", "Medium")).strip().capitalize()
            try:
                severity = ErrorSeverity(raw_sev)
            except ValueError:
                severity = ErrorSeverity.MEDIUM

            # Parse status
            raw_status = str(row.get("final_status", "Resolved – Corrected Claim")).strip()
            try:
                status = ResolutionStatus(raw_status)
            except ValueError:
                status = ResolutionStatus.RESOLVED_CORRECTED

            scenario = BillingScenario(
                scenario_id=str(row["scenario_id"]).strip(),
                encounter_id=str(row["encounter_id"]).strip(),
                patient_id=str(row.get("patient_id", "UNKNOWN")).strip(),
                patient_name=str(row.get("patient_name", "Unknown Patient")).strip(),
                patient_age=int(row.get("patient_age", 50)),
                patient_gender=str(row.get("patient_gender", "Unknown")).strip(),
                date_of_service=str(row.get("date_of_service", "2024-05-01")).strip(),
                payer_name=str(row.get("payer_name", "Standard Payer")).strip(),
                plan_type=str(row.get("plan_type", "PPO")).strip(),
                clinical_documentation=str(row.get("clinical_documentation", "")).strip(),
                original_icd10=str(row.get("original_icd10", "")).strip(),
                original_cpt=str(row.get("original_cpt", "")).strip(),
                original_billed_amount=float(row.get("original_billed_amount", 0.00)),
                billing_query=str(row.get("billing_query", "")).strip(),
                error_category=str(row.get("error_category", "ERR_ICD_INCORRECT")).strip(),
                error_severity=severity,
                root_cause=str(row.get("root_cause", "")).strip(),
                evidence_required=str(row.get("evidence_required", "")).strip(),
                recommended_action=str(row.get("recommended_action", "")).strip(),
                final_status=status,
                preventive_measure=str(row.get("preventive_measure", "")).strip(),
                manual_review_required=to_bool(row.get("manual_review_required", True)),
                corrected_icd10=str(row.get("corrected_icd10", row.get("original_icd10", ""))).strip(),
                corrected_cpt=str(row.get("corrected_cpt", row.get("original_cpt", ""))).strip(),
                corrected_billed_amount=float(row.get("corrected_billed_amount", row.get("original_billed_amount", 0.00))),
                variance_amount=float(row.get("variance_amount", 0.00)),
                has_provider_signature=to_bool(row.get("has_provider_signature", True)),
                has_prior_authorization=to_bool(row.get("has_prior_authorization", True)),
                units_billed=int(row.get("units_billed", 1)),
                modifier_applied=str(row.get("modifier_applied", "None")).strip() if not pd.isna(row.get("modifier_applied")) else "None"
            )
            scenarios.append(scenario)

        return scenarios

    def get_category_metadata(self, category_key: str) -> Dict[str, Any]:
        """Fetch metadata, default severity, and CARC mappings for a given error code."""
        cats = self.error_categories.get("categories", {})
        return cats.get(category_key, {
            "name": category_key,
            "group": "General",
            "default_severity": "Medium",
            "description": "Standard billing query investigation.",
            "carc_mapping": ["CARC 16"],
            "rarc_mapping": ["N/A"],
            "responsible_department": "Billing & Compliance",
            "prevention_control": "Standard operational review."
        })

    def get_resolution_protocol(self, category_key: str) -> Dict[str, Any]:
        """Fetch step-by-step resolution SOP and evidence rules for an error code."""
        protocols = self.resolution_rules.get("resolution_protocols", {})
        return protocols.get(category_key, {
            "steps": [
                "1. Review clinical documentation and encounter details.",
                "2. Identify discrepancy and verify against coding guidelines.",
                "3. Communicate with provider or payer if needed.",
                "4. Resubmit corrected claim or close query."
            ],
            "required_evidence": ["Progress note narrative", "Billing ledger"],
            "resolution_status": "Resolved – Corrected Claim"
        })
