"""Workflow orchestrator for Week 3: Billing Query Resolution and Error Analysis."""

import os
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any

from .models import (
    BillingScenario, DetectionFinding, RootCauseAnalysis, QueryResolution,
    PreventiveControl, SimulationBatchMetrics, ResolutionStatus, ErrorSeverity
)
from .scenario_loader import ScenarioLoader
from .error_detector import ErrorDetector
from .root_cause_analyzer import RootCauseAnalyzer
from .resolution_engine import ResolutionEngine
from .preventive_engine import PreventiveEngine


class BillingResolutionWorkflow:
    """Coordinates the end-to-end billing query resolution lifecycle:

    Ingestion -> Detection -> Root Cause Analysis -> Resolution Roadmap -> Prevention -> Metrics Computation.
    """

    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(base_dir, "data")

        self.data_dir = data_dir
        self.loader = ScenarioLoader(data_dir=data_dir)
        self.detector = ErrorDetector(categories_meta=self.loader.error_categories.get("categories", {}))
        self.rca_analyzer = RootCauseAnalyzer()
        self.resolution_engine = ResolutionEngine(resolution_rules=self.loader.resolution_rules)
        self.preventive_engine = PreventiveEngine(error_categories_meta=self.loader.error_categories)

    def run_simulation(
        self,
        csv_path: Optional[str] = None
    ) -> Tuple[
        List[BillingScenario],
        List[DetectionFinding],
        List[RootCauseAnalysis],
        List[QueryResolution],
        List[PreventiveControl],
        SimulationBatchMetrics
    ]:
        """Execute the complete billing query resolution simulation across all scenarios.

        Returns:
            Tuple of (scenarios, findings, rcas, resolutions, controls, metrics)
        """
        scenarios = self.loader.load_scenarios_from_csv(csv_path)
        all_findings: List[DetectionFinding] = []
        all_rcas: List[RootCauseAnalysis] = []
        all_resolutions: List[QueryResolution] = []
        all_controls: List[PreventiveControl] = []

        for scenario in scenarios:
            # 1. Error Detection
            findings = self.detector.detect_errors(scenario)
            all_findings.extend(findings)

            # 2. Root Cause Analysis
            rca = self.rca_analyzer.analyze_root_cause(scenario, findings)
            all_rcas.append(rca)

            # 3. Query Resolution Process
            resolution = self.resolution_engine.resolve_query(scenario, findings)
            all_resolutions.append(resolution)

            # 4. Preventive Control Mapping
            control = self.preventive_engine.get_control_for_scenario(scenario)
            all_controls.append(control)

        # 5. Compute Batch Metrics
        metrics = self._calculate_metrics(scenarios, all_findings, all_rcas, all_resolutions)

        return (scenarios, all_findings, all_rcas, all_resolutions, all_controls, metrics)

    def export_analysis_csv(
        self,
        scenarios: List[BillingScenario],
        resolutions: List[QueryResolution],
        output_path: Optional[str] = None
    ) -> str:
        """Export comprehensive billing error resolution audit dataset to CSV."""
        if output_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            output_path = os.path.join(base_dir, "reports", "billing_error_analysis.csv")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        res_map = {r.scenario_id: r for r in resolutions}
        rows: List[Dict[str, Any]] = []

        for s in scenarios:
            r = res_map.get(s.scenario_id)
            rows.append({
                "Scenario ID": s.scenario_id,
                "Encounter ID": s.encounter_id,
                "Patient ID": s.patient_id,
                "Patient Name": s.patient_name,
                "Age": s.patient_age,
                "Gender": s.patient_gender,
                "Date of Service": s.date_of_service,
                "Payer Name": s.payer_name,
                "Plan Type": s.plan_type,
                "Clinical Documentation": s.clinical_documentation,
                "Original ICD-10": s.original_icd10,
                "Original CPT": s.original_cpt,
                "Original Billed Amount": f"${s.original_billed_amount:.2f}",
                "Corrected ICD-10": s.corrected_icd10,
                "Corrected CPT": s.corrected_cpt,
                "Corrected Billed Amount": f"${s.corrected_billed_amount:.2f}" if s.corrected_billed_amount is not None else f"${s.original_billed_amount:.2f}",
                "Financial Variance": f"${s.variance_amount:.2f}",
                "Billing Query": s.billing_query,
                "Error Category": s.error_category,
                "Severity": s.error_severity.value,
                "Root Cause": s.root_cause,
                "Evidence Required": s.evidence_required,
                "Recommended Action": s.recommended_action,
                "Resolution Status": s.final_status.value,
                "Stakeholder Communication": r.provider_payer_communication if r else "",
                "Claim Resubmission Action": r.claim_action if r else "",
                "Preventive Measure": s.preventive_measure,
                "Manual Review Required": "Yes" if s.manual_review_required else "No"
            })

        df = pd.DataFrame(rows)
        df.to_csv(output_path, index=False, encoding="utf-8")
        return output_path

    def _calculate_metrics(
        self,
        scenarios: List[BillingScenario],
        findings: List[DetectionFinding],
        rcas: List[RootCauseAnalysis],
        resolutions: List[QueryResolution]
    ) -> SimulationBatchMetrics:
        """Calculate cohort-level operational, clinical, and financial reconciliation metrics."""
        total = len(scenarios)

        no_error = sum(1 for s in scenarios if s.final_status == ResolutionStatus.NO_ERROR)
        pending = sum(1 for s in scenarios if s.final_status in [
            ResolutionStatus.PENDING_PROVIDER,
            ResolutionStatus.PENDING_PAYER,
            ResolutionStatus.PENDING_DOCS
        ])
        escalated = sum(1 for s in scenarios if s.final_status == ResolutionStatus.ESCALATED)
        resolved = sum(1 for s in scenarios if s.final_status in [
            ResolutionStatus.RESOLVED_CORRECTED,
            ResolutionStatus.RESOLVED_DOCS
        ])
        errors_identified = total - no_error
        manual_review = sum(1 for s in scenarios if s.manual_review_required)

        total_orig_gross = sum(s.original_billed_amount for s in scenarios)
        total_corr_gross = sum(
            s.corrected_billed_amount if s.corrected_billed_amount is not None else s.original_billed_amount
            for s in scenarios
        )
        total_variance = sum(s.variance_amount for s in scenarios)

        clean_res_rate = round((resolved / total) * 100, 1) if total > 0 else 0.0

        # Distribution dictionaries
        cat_counts: Dict[str, int] = {}
        for s in scenarios:
            cat_counts[s.error_category] = cat_counts.get(s.error_category, 0) + 1

        sev_counts: Dict[str, int] = {}
        for s in scenarios:
            sev_counts[s.error_severity.value] = sev_counts.get(s.error_severity.value, 0) + 1

        status_counts: Dict[str, int] = {}
        for s in scenarios:
            status_counts[s.final_status.value] = status_counts.get(s.final_status.value, 0) + 1

        rca_counts: Dict[str, int] = {}
        for r in rcas:
            rca_counts[r.primary_category.value] = rca_counts.get(r.primary_category.value, 0) + 1

        return SimulationBatchMetrics(
            total_scenarios=total,
            errors_identified_count=errors_identified,
            no_error_identified_count=no_error,
            pending_query_count=pending,
            escalated_review_count=escalated,
            resolved_claims_count=resolved,
            manual_review_required_count=manual_review,
            total_original_gross_billed=round(total_orig_gross, 2),
            total_corrected_gross_billed=round(total_corr_gross, 2),
            total_financial_variance=round(total_variance, 2),
            clean_resolution_rate=clean_res_rate,
            category_counts=cat_counts,
            severity_counts=sev_counts,
            status_counts=status_counts,
            root_cause_counts=rca_counts
        )
