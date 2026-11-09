"""
Week 4 Risk Assessment & Mitigation Engine
Manages the integration risk register, calculates 5x5 likelihood-impact risk scores,
categorizes risks into severity tiers, and formulates actionable contingency strategies.
"""

import csv
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from week4.src.models import RiskItem

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class RiskEngine:
    def __init__(self, risk_csv: Optional[Path] = None):
        self.risk_csv = risk_csv or (DATA_DIR / "risk_register.csv")
        self.risks: List[RiskItem] = []
        self._load_risks()

    def _load_risks(self):
        if not self.risk_csv.exists():
            raise FileNotFoundError(f"Risk register CSV not found: {self.risk_csv}")

        with open(self.risk_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                likelihood = int(row["likelihood"])
                impact = int(row["impact"])
                score = likelihood * impact
                level = row.get("risk_level", "")
                if not level:
                    if score >= 15:
                        level = "Critical"
                    elif score >= 10:
                        level = "High"
                    elif score >= 5:
                        level = "Medium"
                    else:
                        level = "Low"

                self.risks.append(RiskItem(
                    risk_id=row["risk_id"],
                    category=row["category"],
                    title=row["title"],
                    description=row["description"],
                    likelihood=likelihood,
                    impact=impact,
                    risk_score=score,
                    risk_level=level,
                    mitigation_strategy=row["mitigation_strategy"],
                    contingency_plan=row["contingency_plan"],
                    owner_role=row["owner_role"]
                ))

    def get_summary_metrics(self) -> Dict[str, Any]:
        """Calculates risk distribution metrics across categories and severity tiers."""
        total_risks = len(self.risks)
        scores = [r.risk_score for r in self.risks]
        avg_score = round(sum(scores) / total_risks, 2) if total_risks else 0.0

        by_level = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
        by_category = {}

        for r in self.risks:
            by_level[r.risk_level] = by_level.get(r.risk_level, 0) + 1
            by_category[r.category] = by_category.get(r.category, 0) + 1

        top_risks = sorted(self.risks, key=lambda x: x.risk_score, reverse=True)[:5]

        return {
            "total_risks": total_risks,
            "average_risk_score": avg_score,
            "distribution_by_level": by_level,
            "distribution_by_category": by_category,
            "top_risks": [
                {
                    "risk_id": r.risk_id,
                    "title": r.title,
                    "category": r.category,
                    "score": r.risk_score,
                    "level": r.risk_level,
                    "owner": r.owner_role
                }
                for r in top_risks
            ]
        }

    def get_matrix_grid(self) -> Dict[Tuple[int, int], List[str]]:
        """Returns a mapping of (likelihood, impact) coordinates to risk IDs for 5x5 heatmap plotting."""
        grid = {}
        for l in range(1, 6):
            for i in range(1, 6):
                grid[(l, i)] = []

        for r in self.risks:
            coord = (r.likelihood, r.impact)
            if coord in grid:
                grid[coord].append(r.risk_id)

        return grid
