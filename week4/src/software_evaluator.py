"""
Week 4 Software Evaluator Module
Implements a transparent weighted evaluation model comparing:
1. athenahealth athenaOne
2. AdvancedMD
3. Tebra

Features 10 weighted evaluation criteria with configurable weights and transparent justifications.
All scores represent illustrative evaluation judgments based on publicly documented product capabilities.
"""

import csv
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from week4.src.models import VendorComparison, EvaluationCriteria

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class SoftwareEvaluator:
    def __init__(self, comparison_csv: Optional[Path] = None):
        self.comparison_csv = comparison_csv or (DATA_DIR / "software_comparison.csv")
        self.features: List[VendorComparison] = []
        self.criteria: List[EvaluationCriteria] = []
        self._load_features()
        self._initialize_criteria()

    def _load_features(self):
        if not self.comparison_csv.exists():
            raise FileNotFoundError(f"Software comparison file not found: {self.comparison_csv}")
        
        with open(self.comparison_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.features.append(VendorComparison(
                    feature_id=row["feature_id"],
                    feature_name=row["feature_name"],
                    category=row["category"],
                    athenahealth_capability=row["athenahealth_capability"],
                    athenahealth_status=row["athenahealth_status"],
                    athenahealth_source=row["athenahealth_source"],
                    advancedmd_capability=row["advancedmd_capability"],
                    advancedmd_status=row["advancedmd_status"],
                    advancedmd_source=row["advancedmd_source"],
                    tebra_capability=row["tebra_capability"],
                    tebra_status=row["tebra_status"],
                    tebra_source=row["tebra_source"],
                    research_date=row.get("research_date", "2026-11-09")
                ))

    def _initialize_criteria(self):
        """Initializes 10 balanced evaluation criteria totaling 100% (1.00) weight."""
        self.criteria = [
            EvaluationCriteria(
                criterion_id="CRIT-01",
                name="Billing Workflow & Clearinghouse Integration",
                category="Billing Core",
                weight=0.15,
                score_athena=9.5,
                score_advancedmd=8.8,
                score_tebra=8.0,
                justification_athena="Native built-in clearinghouse on athenaNet; automated 837P transmission and auto-posting of 835 ERAs without third-party portal logins.",
                justification_advancedmd="Robust integrated clearinghouse via Waystar/Change Healthcare partnerships with strong in-app claim tracking and auto-posting.",
                justification_tebra="Integrated clearinghouse via TriZetto partner; streamlined daily batch submissions but less granular customization."
            ),
            EvaluationCriteria(
                criterion_id="CRIT-02",
                name="Pre-Bill Claim Scrubbing & Rules Engine",
                category="Revenue Integrity",
                weight=0.15,
                score_athena=9.6,
                score_advancedmd=9.0,
                score_tebra=8.2,
                justification_athena="Proprietary payer-specific billing rules engine continuously updated cloud-wide across the network; real-time pre-submission error trapping.",
                justification_advancedmd="AdvancedClaim rules engine with comprehensive automated edit checks, custom rule builder, and automated NCCI PTP/MUE validation.",
                justification_tebra="Standard claim scrubber checking core NCCI edits, missing demographics, and primary payer validation rules."
            ),
            EvaluationCriteria(
                criterion_id="CRIT-03",
                name="EHR Interoperability & Open APIs",
                category="Interoperability",
                weight=0.10,
                score_athena=9.4,
                score_advancedmd=7.8,
                score_tebra=7.0,
                justification_athena="Publicly documented Developer Portal with REST APIs, certified FHIR R4 endpoints, free sandbox, and OAuth 2.0 authentication.",
                justification_advancedmd="RESTful API library available through formal Integration Partner Program; requires developer license agreement and NDA.",
                justification_tebra="Partner API program requiring sales review and business partnership agreement; less publicly transparent developer tooling."
            ),
            EvaluationCriteria(
                criterion_id="CRIT-04",
                name="Real-Time Eligibility Verification (270/271)",
                category="Front-Desk",
                weight=0.10,
                score_athena=9.2,
                score_advancedmd=9.0,
                score_tebra=8.4,
                justification_athena="Automated 72h/48h/24h scheduled batch eligibility checks plus instant on-demand 270 check at front desk with copay breakdown.",
                justification_advancedmd="Automated batch eligibility scheduling and on-demand real-time verification with detailed benefit co-pay/deductible breakdown.",
                justification_tebra="Automated daily eligibility batching and real-time inquiries via TriZetto clearinghouse engine."
            ),
            EvaluationCriteria(
                criterion_id="CRIT-05",
                name="Denial Management & Appeals Workflow",
                category="Revenue Integrity",
                weight=0.10,
                score_athena=9.2,
                score_advancedmd=8.8,
                score_tebra=7.8,
                justification_athena="Automated CARC/RARC categorization, built-in appeal letter templates with attached clinical documentation, and re-submission queues.",
                justification_advancedmd="Dedicated denial worklists, root-cause categorization, appeal letter generator, and denial trend reporting.",
                justification_tebra="Rejection and denial work queues with CARC display and manual appeal letter generation tools."
            ),
            EvaluationCriteria(
                criterion_id="CRIT-06",
                name="Financial Reporting & RCM Analytics",
                category="Analytics",
                weight=0.10,
                score_athena=9.5,
                score_advancedmd=9.4,
                score_tebra=8.0,
                justification_athena="athenaNet Insight provides real-time KPI tracking and national peer provider performance benchmarking.",
                justification_advancedmd="AdvancedInsight reporting engine with customizable RCM reports, multi-dimensional financial data cube, and visual KPI dashboards.",
                justification_tebra="Standard billing dashboards, aging reports by payer/patient buckets, and CSV/Excel exports."
            ),
            EvaluationCriteria(
                criterion_id="CRIT-07",
                name="Security, Privacy & Regulatory Compliance",
                category="Compliance",
                weight=0.10,
                score_athena=9.6,
                score_advancedmd=9.2,
                score_tebra=9.0,
                justification_athena="HITRUST CSF Certified, SOC 2 Type II compliant, HIPAA compliant, role-based access control, TLS 1.3/AES-256 encryption.",
                justification_advancedmd="AWS healthcare cloud infrastructure, SOC 2 Type II audited, HIPAA compliant, fine-grained user permissions.",
                justification_tebra="HIPAA compliant cloud infrastructure, SOC 2 Type II certified, role-based access controls, encrypted data storage."
            ),
            EvaluationCriteria(
                criterion_id="CRIT-08",
                name="Staff Usability & Training Methodology",
                category="Change Management",
                weight=0.08,
                score_athena=8.8,
                score_advancedmd=8.5,
                score_tebra=9.0,
                justification_athena="Structured onboarding curriculum, athenaHealth University LMS, role-based webinars, and dedicated project manager.",
                justification_advancedmd="AdvancedMD University interactive learning modules, implementation consultant, and live classroom webinars.",
                justification_tebra="Highly intuitive modern user interface, Tebra Academy video tutorials, and rapid onboarding timeline."
            ),
            EvaluationCriteria(
                criterion_id="CRIT-09",
                name="Data Migration Support & Tools",
                category="Implementation",
                weight=0.07,
                score_athena=8.6,
                score_advancedmd=8.5,
                score_tebra=8.0,
                justification_athena="Dedicated data conversion team with standardized intake pipelines for legacy CCDA, demographic CSV, and open AR transfer.",
                justification_advancedmd="Proprietary Data Conversion Services team with standard conversion templates for demographics, fee schedules, and balances.",
                justification_tebra="Assisted onboarding data import wizards for patient demographics, calendars, and address books."
            ),
            EvaluationCriteria(
                criterion_id="CRIT-10",
                name="Pricing Transparency & Total Cost of Ownership",
                category="Cost",
                weight=0.05,
                score_athena=7.2,
                score_advancedmd=8.2,
                score_tebra=8.0,
                justification_athena="Collections-percentage model (4-7%) aligns incentives with collections but adds variable cost; implementation fees require quote.",
                justification_advancedmd="Transparent published tiered SaaS pricing ($429-$1,070/provider/mo); predictable monthly subscription expenditure.",
                justification_tebra="Quote-based pricing with modular tier options; competitive estimated entry costs for small practices."
            )
        ]

    def update_weights(self, weight_overrides: Dict[str, float]):
        """Allows dynamic adjustment of criteria weights."""
        total = sum(weight_overrides.values())
        if abs(total - 1.0) > 0.001 and abs(total - 100.0) > 0.1:
            raise ValueError(f"Weights must sum to 1.0 (or 100%). Current sum: {total}")
        
        # Normalize if passed as percentages 0-100
        factor = 1.0 if total <= 1.01 else 100.0
        for crit in self.criteria:
            if crit.criterion_id in weight_overrides:
                crit.weight = weight_overrides[crit.criterion_id] / factor

    def calculate_scores(self) -> Dict[str, Any]:
        """Calculates weighted scores for each vendor and determines the rank."""
        total_athena = 0.0
        total_advancedmd = 0.0
        total_tebra = 0.0
        total_weight = sum(c.weight for c in self.criteria)

        breakdown = []
        for c in self.criteria:
            wt_athena = c.score_athena * c.weight
            wt_advancedmd = c.score_advancedmd * c.weight
            wt_tebra = c.score_tebra * c.weight

            total_athena += wt_athena
            total_advancedmd += wt_advancedmd
            total_tebra += wt_tebra

            breakdown.append({
                "criterion_id": c.criterion_id,
                "name": c.name,
                "weight_pct": round(c.weight * 100, 1),
                "score_athena": c.score_athena,
                "weighted_athena": round(wt_athena, 3),
                "score_advancedmd": c.score_advancedmd,
                "weighted_advancedmd": round(wt_advancedmd, 3),
                "score_tebra": c.score_tebra,
                "weighted_tebra": round(wt_tebra, 3)
            })

        results = {
            "athenahealth athenaOne": round(total_athena, 2),
            "AdvancedMD": round(total_advancedmd, 2),
            "Tebra": round(total_tebra, 2)
        }

        ranked = sorted(results.items(), key=lambda x: x[1], reverse=True)
        recommended_vendor = ranked[0][0]
        recommended_score = ranked[0][1]

        return {
            "total_weight": round(total_weight, 4),
            "breakdown": breakdown,
            "vendor_scores": results,
            "ranked_vendors": ranked,
            "recommended_vendor": recommended_vendor,
            "recommended_score": recommended_score,
            "evaluation_note": "Scores are illustrative student evaluation judgments derived from publicly documented vendor capabilities and feature alignment with the multi-specialty practice profile. This is not an independent product performance certification, commercial endorsement, or official audit."
        }

    def get_feature_matrix_summary(self) -> Dict[str, Any]:
        """Summarizes verified vs unverified features across vendors."""
        summary = {
            "total_features": len(self.features),
            "athenahealth": {"verified": 0, "requires_confirmation": 0, "not_verified": 0},
            "advancedmd": {"verified": 0, "requires_confirmation": 0, "not_verified": 0},
            "tebra": {"verified": 0, "requires_confirmation": 0, "not_verified": 0}
        }

        for f in self.features:
            for vendor in ["athenahealth", "advancedmd", "tebra"]:
                status = getattr(f, f"{vendor}_status")
                if "Verified" in status:
                    summary[vendor]["verified"] += 1
                elif "Requires" in status:
                    summary[vendor]["requires_confirmation"] += 1
                else:
                    summary[vendor]["not_verified"] += 1

        return summary
