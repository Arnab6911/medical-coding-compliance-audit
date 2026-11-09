"""
Week 4 Workflow Orchestration Module
Executes the full end-to-end simulation pipeline:
1. Practice Profile Loading
2. Software Evaluation Matrix Calculation
3. Data Migration Validation & Reconciliation
4. Real-Time Pre-Bill Claim Rule Initialization
5. Risk Assessment Matrix & Metrics Generation
6. Role-Based Training & Competency Verification
7. Diagram Rendering (Architecture, Workflow, Risk Matrix)
8. Comprehensive Word Report Compilation
"""

from pathlib import Path
from typing import Dict, Any, Optional

from week4.src.models import PracticeProfile
from week4.src.software_evaluator import SoftwareEvaluator
from week4.src.migration_engine import MigrationEngine
from week4.src.validation_rules import ValidationRuleEngine
from week4.src.risk_engine import RiskEngine
from week4.src.training_engine import TrainingEngine
from week4.src.visualizer import IntegrationVisualizer
from week4.src.report_generator import IntegrationReportGenerator

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"

class IntegrationWorkflow:
    def __init__(self):
        self.profile = PracticeProfile()
        self.evaluator = SoftwareEvaluator()
        self.migration = MigrationEngine()
        self.rules_engine = ValidationRuleEngine()
        self.risk_engine = RiskEngine()
        self.training = TrainingEngine()
        self.visualizer = IntegrationVisualizer()
        self.report_gen = IntegrationReportGenerator()

    def run_simulation(self, compile_word_report: bool = True) -> Dict[str, Any]:
        """Executes full simulation pipeline and returns aggregated metrics."""
        print("Starting Week 4 Integration Simulation Pipeline...")

        # 1. Evaluation Scoring
        eval_results = self.evaluator.calculate_scores()
        eval_summary = self.evaluator.get_feature_matrix_summary()

        # 2. Migration & Reconciliation
        mig_validation = self.migration.run_validation()
        mig_duplicates = self.migration.detect_duplicates()
        mig_reconciliation = self.migration.reconcile_financials()

        # 3. Validation Rules
        rules_by_sev = self.rules_engine.get_rules_by_severity()
        code_gov = self.rules_engine.get_code_governance_schedule()

        # 4. Risk Assessment
        risk_metrics = self.risk_engine.get_summary_metrics()

        # 5. Training Curriculum
        training_summary = self.training.get_summary()

        # 6. Diagram Generation (300 DPI)
        diagram_paths = self.visualizer.generate_all_diagrams()

        # 7. Word Report Compilation
        docx_path = None
        if compile_word_report:
            docx_path = self.report_gen.generate_report()

        print("Week 4 Simulation Pipeline Completed Successfully.")

        return {
            "status": "SUCCESS",
            "practice_name": self.profile.name,
            "evaluation": {
                "recommended_vendor": eval_results["recommended_vendor"],
                "recommended_score": eval_results["recommended_score"],
                "vendor_scores": eval_results["vendor_scores"],
                "feature_summary": eval_summary
            },
            "migration": {
                "total_records": mig_validation["total_records"],
                "cleansing_success_rate": mig_validation["cleansing_success_rate"],
                "duplicate_candidates_found": len(mig_duplicates),
                "total_legacy_ar": mig_reconciliation["total_legacy_ar"],
                "total_migrated_ar": mig_reconciliation["total_migrated_ar"],
                "net_variance": mig_reconciliation["net_variance"],
                "is_balanced": mig_reconciliation["is_balanced"],
                "reconciliation_rate": mig_reconciliation["reconciliation_rate"]
            },
            "validation_rules": {
                "total_rules": len(self.rules_engine.rules),
                "hard_stops": len(rules_by_sev["HARD_STOP"]),
                "warnings": len(rules_by_sev["WARNING"]),
                "governance_cycles": len(code_gov)
            },
            "risk_assessment": {
                "total_risks": risk_metrics["total_risks"],
                "average_risk_score": risk_metrics["average_risk_score"],
                "distribution_by_level": risk_metrics["distribution_by_level"],
                "top_risks_count": len(risk_metrics["top_risks"])
            },
            "training": {
                "total_modules": training_summary["total_modules"],
                "total_hours": training_summary["total_training_hours"],
                "total_questions": training_summary["total_questions"],
                "passing_threshold_pct": training_summary["passing_grade_percent"]
            },
            "diagrams": {k: str(p) for k, p in diagram_paths.items()},
            "report_path": str(docx_path) if docx_path else None
        }
