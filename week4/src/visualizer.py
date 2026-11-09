"""
Week 4 Visualizer Module
Generates high-resolution (300 DPI) architectural, workflow, and risk matrix diagrams:
1. week4/reports/integration_architecture.png (System Architecture Diagram)
2. week4/reports/integration_workflow.png (12-Phase Implementation Roadmap)
3. week4/reports/risk_assessment_matrix.png (5x5 Likelihood x Impact Heatmap)
"""

from pathlib import Path
from typing import Optional, Dict
import matplotlib
matplotlib.use("Agg")  # Headless backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"

class IntegrationVisualizer:
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or REPORTS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_system_architecture_diagram(self) -> Path:
        """Generates 300 DPI integration system architecture diagram."""
        filepath = self.output_dir / "integration_architecture.png"
        fig, ax = plt.subplots(figsize=(14, 10), dpi=300)
        ax.set_facecolor("#f8fafc")
        fig.patch.set_facecolor("#ffffff")

        # Title
        ax.text(0.5, 0.96, "PROPOSED HEALTHCARE IT & RCM INTEGRATION ARCHITECTURE",
                ha="center", va="center", fontsize=15, fontweight="bold", color="#0f172a")
        ax.text(0.5, 0.93, "Evergreen Valley Multi-Specialty Clinic | Cloud Practice Management & Billing Pipeline",
                ha="center", va="center", fontsize=10, color="#475569", style="italic")

        # Define Architectural Tiers / Component Boxes
        boxes = [
            # Layer 1: Front-Desk & Patient Intake
            {"x": 0.05, "y": 0.72, "w": 0.26, "h": 0.16, "title": "1. Patient Intake & Access",
             "items": ["• Digital Check-In / Kiosk", "• Demographic Capture & MPI", "• Real-Time 270 Eligibility", "• Copay POS Collection"],
             "bg": "#e0f2fe", "border": "#0284c7"},

            # Layer 2: Clinical EHR & Encounter Documentation
            {"x": 0.37, "y": 0.72, "w": 0.26, "h": 0.16, "title": "2. Clinical EHR Documentation",
             "items": ["• Progress Notes & Templates", "• MDM / Time E/M Selection", "• Electronic Superbill Entry", "• 24h Physician E-Signature"],
             "bg": "#f0fdf4", "border": "#16a34a"},

            # Layer 3: Pre-Bill Claim Validation Engine
            {"x": 0.69, "y": 0.72, "w": 0.26, "h": 0.16, "title": "3. Pre-Bill Rules Scrubber",
             "items": ["• Hard-Stop / Fatal Edit Block", "• NCCI PTP & MUE Validation", "• ICD-10/CPT DOS Gating", "• Warning / Coding Audit Queue"],
             "bg": "#fef3c7", "border": "#d97706"},

            # Layer 4: Practice Management & Billing Core
            {"x": 0.05, "y": 0.42, "w": 0.42, "h": 0.18, "title": "4. Practice Management & Charge Staging",
             "items": ["• Daily Encounter Reconciliation & Missing Charge Audits",
                       "• Certified Coder Review & Provider Clarification Queries",
                       "• Secondary Insurance Staging & Self-Pay Balance Ledger",
                       "• Chargemaster Fee Schedules & Patient Accounts Receivable"],
             "bg": "#ede9fe", "border": "#7c3aed"},

            # Layer 5: EDI Clearinghouse Gateway
            {"x": 0.53, "y": 0.42, "w": 0.42, "h": 0.18, "title": "5. Integrated Clearinghouse & EDI Gateway",
             "items": ["• Automated Electronic X12 837P Batch Transmission",
                       "• Real-Time 999 Acknowledgments & 277CA Rejections",
                       "• Ingestion of X12 835 Electronic Remittance Advice (ERA)",
                       "• Automated CARC/RARC Denial Categorization & Routing"],
             "bg": "#fae8ff", "border": "#c026d3"},

            # Layer 6: Downstream Payer & Patient Adjudication
            {"x": 0.05, "y": 0.14, "w": 0.42, "h": 0.18, "title": "6. Payment Posting & Patient Accounting",
             "items": ["• Automated 835 Remittance Matching & Auto-Posting",
                       "• Contractual Write-Offs & COB Secondary Claim Dispatch",
                       "• Electronic & Paper Patient Statement Generation",
                       "• Online Patient Payment Portal & Card-on-File"],
             "bg": "#ccfbf1", "border": "#0d9488"},

            # Layer 7: Executive Analytics & Compliance Oversight
            {"x": 0.53, "y": 0.14, "w": 0.42, "h": 0.18, "title": "7. Executive RCM Dashboard & Governance",
             "items": ["• 11 Core RCM KPIs (DAR, Denial Rate, Clean Claims)",
                       "• Denial Root-Cause Analytics & Payer SLA Tracking",
                       "• HIPAA Security Audit Logging & Role-Based Access",
                       "• Annual ICD-10 / CPT Code Update Versioning"],
             "bg": "#ffe4e6", "border": "#e11d48"},
        ]

        # Draw boxes
        for b in boxes:
            rect = patches.FancyBboxPatch(
                (b["x"], b["y"]), b["w"], b["h"],
                boxstyle="round,pad=0.015,rounding_size=0.02",
                facecolor=b["bg"], edgecolor=b["border"], linewidth=1.5
            )
            ax.add_patch(rect)
            ax.text(b["x"] + 0.015, b["y"] + b["h"] - 0.03, b["title"],
                    fontsize=10.5, fontweight="bold", color=b["border"])
            
            y_offset = b["y"] + b["h"] - 0.06
            for item in b["items"]:
                ax.text(b["x"] + 0.015, y_offset, item, fontsize=8.5, color="#1e293b")
                y_offset -= 0.027

        # Connectors & Arrows
        arrows = [
            # Intake to EHR
            ((0.31, 0.80), (0.37, 0.80), "Demographics / 271 Eligibility", "#0284c7"),
            # EHR to Scrubber
            ((0.63, 0.80), (0.69, 0.80), "Clinical Note & Superbill", "#16a34a"),
            # Scrubber down to PM
            ((0.82, 0.72), (0.26, 0.60), "Validated Claims", "#d97706"),
            # PM to Clearinghouse
            ((0.47, 0.51), (0.53, 0.51), "X12 837P Claims", "#7c3aed"),
            # Clearinghouse down to Payment Posting
            ((0.74, 0.42), (0.26, 0.32), "X12 835 Remittance / 277CA", "#c026d3"),
            # PM down to Analytics
            ((0.26, 0.42), (0.74, 0.32), "Financial Ledgers & Logs", "#475569"),
            # Payment Posting to Analytics
            ((0.47, 0.23), (0.53, 0.23), "Posted Cash & Reconciliations", "#0d9488"),
        ]

        for start, end, label, color in arrows:
            ax.annotate("", xy=end, xytext=start,
                        arrowprops=dict(arrowstyle="->", color=color, lw=1.8,
                                        connectionstyle="arc3,rad=-0.12"))
            mid_x = (start[0] + end[0]) / 2
            mid_y = (start[1] + end[1]) / 2 + 0.02
            ax.text(mid_x, mid_y, label, fontsize=7.5, fontweight="bold", color=color,
                    ha="center", bbox=dict(boxstyle="round,pad=0.2", facecolor="#ffffff", edgecolor=color, lw=0.8))

        # Security & Compliance Foundation Banner
        banner = patches.FancyBboxPatch(
            (0.05, 0.02), 0.90, 0.065,
            boxstyle="round,pad=0.01",
            facecolor="#1e293b", edgecolor="#0f172a", linewidth=1.5
        )
        ax.add_patch(banner)
        ax.text(0.5, 0.062, "SECURITY, PRIVACY & COMPLIANCE FOUNDATION",
                ha="center", va="center", fontsize=9.5, fontweight="bold", color="#38bdf8")
        ax.text(0.5, 0.038, "HIPAA Security Rule (45 CFR § 164) • TLS 1.3 In-Transit • AES-256 At-Rest • RBAC • BAA Covered Entity Execution • Immutable Audit Logs",
                ha="center", va="center", fontsize=8.0, color="#f1f5f9")

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        plt.tight_layout()
        plt.savefig(filepath, format="png", dpi=300, bbox_inches="tight")
        plt.close(fig)
        print(f"Generated system architecture diagram: {filepath}")
        return filepath

    def generate_implementation_workflow_diagram(self) -> Path:
        """Generates 300 DPI 12-phase implementation workflow roadmap."""
        filepath = self.output_dir / "integration_workflow.png"
        fig, ax = plt.subplots(figsize=(15, 9), dpi=300)
        ax.set_facecolor("#f8fafc")
        fig.patch.set_facecolor("#ffffff")

        ax.text(0.5, 0.96, "12-PHASE BILLING SOFTWARE INTEGRATION & IMPLEMENTATION ROADMAP",
                ha="center", va="center", fontsize=15, fontweight="bold", color="#0f172a")
        ax.text(0.5, 0.925, "Evergreen Valley Multi-Specialty Clinic | 24-Week Structured Implementation Methodology",
                ha="center", va="center", fontsize=10, color="#475569", style="italic")

        # 12 Phases organized across 4 stages (3 phases per stage)
        stages = [
            {"stage": "STAGE 1: EVALUATION & DESIGN (Weeks 1-6)", "color": "#0284c7", "y": 0.72},
            {"stage": "STAGE 2: TECHNICAL PREPARATION & MIGRATION (Weeks 7-14)", "color": "#7c3aed", "y": 0.50},
            {"stage": "STAGE 3: TESTING, TRAINING & PILOT (Weeks 15-20)", "color": "#d97706", "y": 0.28},
            {"stage": "STAGE 4: GO-LIVE & OPTIMIZATION (Weeks 21-24+)", "color": "#16a34a", "y": 0.06}
        ]

        phases = [
            # Stage 1
            {"num": 1, "title": "Phase 1: Requirements Gathering", "desc": "Stakeholder interviews, legacy gap analysis, workflow discovery.", "x": 0.04, "y": 0.73, "stage_idx": 0},
            {"num": 2, "title": "Phase 2: Vendor Evaluation", "desc": "Weighted scoring matrix, vendor demos, contract & BAA review.", "x": 0.36, "y": 0.73, "stage_idx": 0},
            {"num": 3, "title": "Phase 3: Workflow Configuration", "desc": "EHR clinical templates, superbill mapping, provider scheduling.", "x": 0.68, "y": 0.73, "stage_idx": 0},

            # Stage 2
            {"num": 4, "title": "Phase 4: Architecture & APIs", "desc": "REST/FHIR interfaces, clearinghouse setup, 270/837/835 pipes.", "x": 0.04, "y": 0.51, "stage_idx": 1},
            {"num": 5, "title": "Phase 5: Migration Preparation", "desc": "Schema mapping, ETL scripts, data cleansing, MPI deduplication.", "x": 0.36, "y": 0.51, "stage_idx": 1},
            {"num": 6, "title": "Phase 6: Data Migration & AR Balance", "desc": "Test loads, open AR ledger audit, $0.00 variance sign-off.", "x": 0.68, "y": 0.51, "stage_idx": 1},

            # Stage 3
            {"num": 7, "title": "Phase 7: Pre-Bill Rules Configuration", "desc": "Hard-stop claim rules, NCCI PTP/MUE tables, DOS coding gating.", "x": 0.04, "y": 0.29, "stage_idx": 2},
            {"num": 8, "title": "Phase 8: End-to-End Testing", "desc": "500 sandbox test claims, 837P transmission, 835 auto-post check.", "x": 0.36, "y": 0.29, "stage_idx": 2},
            {"num": 9, "title": "Phase 9: Role-Based Staff Training", "desc": "5 role curricula, exercises, 85% passing grade assessment.", "x": 0.68, "y": 0.29, "stage_idx": 2},

            # Stage 4
            {"num": 10, "title": "Phase 10: Pilot Deployment", "desc": "Cardiology clinic 2-week pilot, rapid issue triage, workflow tuning.", "x": 0.04, "y": 0.07, "stage_idx": 3},
            {"num": 11, "title": "Phase 11: Enterprise Cutover & Go-Live", "desc": "Cutover weekend, final AR snapshot, command center support.", "x": 0.36, "y": 0.07, "stage_idx": 3},
            {"num": 12, "title": "Phase 12: Monitoring & Optimization", "desc": "Weekly KPI tracking (DAR, Denials), monthly SteerCo reviews.", "x": 0.68, "y": 0.07, "stage_idx": 3},
        ]

        # Draw stage backdrops
        for s in stages:
            stage_rect = patches.FancyBboxPatch(
                (0.02, s["y"] - 0.04), 0.96, 0.19,
                boxstyle="round,pad=0.01",
                facecolor="#ffffff", edgecolor=s["color"], linewidth=1.8, linestyle="--"
            )
            ax.add_patch(stage_rect)
            ax.text(0.03, s["y"] + 0.13, s["stage"], fontsize=9.5, fontweight="bold", color=s["color"])

        # Draw phase cards
        for p in phases:
            stg = stages[p["stage_idx"]]
            card = patches.FancyBboxPatch(
                (p["x"], p["y"]), 0.28, 0.12,
                boxstyle="round,pad=0.01",
                facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=1.2
            )
            ax.add_patch(card)

            # Phase header
            ax.text(p["x"] + 0.012, p["y"] + 0.09, p["title"], fontsize=9.0, fontweight="bold", color="#0f172a")
            # Phase description
            ax.text(p["x"] + 0.012, p["y"] + 0.045, p["desc"], fontsize=7.5, color="#475569", wrap=True)

        # Draw sequential flow arrows between phases
        # Intra-stage horizontal arrows
        ax.annotate("", xy=(0.36, 0.79), xytext=(0.32, 0.79), arrowprops=dict(arrowstyle="->", color="#0284c7", lw=1.5))
        ax.annotate("", xy=(0.68, 0.79), xytext=(0.64, 0.79), arrowprops=dict(arrowstyle="->", color="#0284c7", lw=1.5))

        # Transition Stage 1 to Stage 2
        ax.annotate("", xy=(0.04, 0.57), xytext=(0.96, 0.73),
                    arrowprops=dict(arrowstyle="->", color="#64748b", lw=1.5, connectionstyle="angle,angleA=0,angleB=90,rad=10"))

        # Stage 2 horizontal arrows
        ax.annotate("", xy=(0.36, 0.57), xytext=(0.32, 0.57), arrowprops=dict(arrowstyle="->", color="#7c3aed", lw=1.5))
        ax.annotate("", xy=(0.68, 0.57), xytext=(0.64, 0.57), arrowprops=dict(arrowstyle="->", color="#7c3aed", lw=1.5))

        # Transition Stage 2 to Stage 3
        ax.annotate("", xy=(0.04, 0.35), xytext=(0.96, 0.51),
                    arrowprops=dict(arrowstyle="->", color="#64748b", lw=1.5, connectionstyle="angle,angleA=0,angleB=90,rad=10"))

        # Stage 3 horizontal arrows
        ax.annotate("", xy=(0.36, 0.35), xytext=(0.32, 0.35), arrowprops=dict(arrowstyle="->", color="#d97706", lw=1.5))
        ax.annotate("", xy=(0.68, 0.35), xytext=(0.64, 0.35), arrowprops=dict(arrowstyle="->", color="#d97706", lw=1.5))

        # Transition Stage 3 to Stage 4
        ax.annotate("", xy=(0.04, 0.13), xytext=(0.96, 0.29),
                    arrowprops=dict(arrowstyle="->", color="#64748b", lw=1.5, connectionstyle="angle,angleA=0,angleB=90,rad=10"))

        # Stage 4 horizontal arrows
        ax.annotate("", xy=(0.36, 0.13), xytext=(0.32, 0.13), arrowprops=dict(arrowstyle="->", color="#16a34a", lw=1.5))
        ax.annotate("", xy=(0.68, 0.13), xytext=(0.64, 0.13), arrowprops=dict(arrowstyle="->", color="#16a34a", lw=1.5))

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        plt.tight_layout()
        plt.savefig(filepath, format="png", dpi=300, bbox_inches="tight")
        plt.close(fig)
        print(f"Generated implementation workflow diagram: {filepath}")
        return filepath

    def generate_risk_assessment_matrix(self) -> Path:
        """Generates 300 DPI 5x5 Likelihood vs Impact risk matrix heatmap."""
        filepath = self.output_dir / "risk_assessment_matrix.png"
        fig, ax = plt.subplots(figsize=(11, 8.5), dpi=300)
        ax.set_facecolor("#ffffff")

        # 5x5 matrix dimensions: Rows = Likelihood (1 to 5), Columns = Impact (1 to 5)
        # Risk score = L * I
        # Colors: Green (1-4), Yellow (5-9), Orange (10-14), Red (15-25)
        matrix = np.zeros((5, 5))
        for l in range(1, 6):
            for i in range(1, 6):
                matrix[5 - l, i - 1] = l * i  # Invert row so Likelihood 5 is at top

        # Custom colormap or cell-by-cell rendering for crisp colors
        colors = {
            "Low": "#dcfce7",       # Light Green (1-4)
            "Medium": "#fef9c3",    # Light Yellow (5-9)
            "High": "#ffedd5",      # Light Orange (10-14)
            "Critical": "#fee2e2"   # Light Red (15-25)
        }
        border_colors = {
            "Low": "#22c55e",
            "Medium": "#eab308",
            "High": "#f97316",
            "Critical": "#ef4444"
        }

        # Plot 5x5 cells
        for l_idx in range(5):
            for i_idx in range(5):
                score = matrix[l_idx, i_idx]
                if score >= 15:
                    cat = "Critical"
                elif score >= 10:
                    cat = "High"
                elif score >= 5:
                    cat = "Medium"
                else:
                    cat = "Low"

                rect = patches.Rectangle(
                    (i_idx, 4 - l_idx), 1, 1,
                    facecolor=colors[cat], edgecolor="#cbd5e1", linewidth=1.0
                )
                ax.add_patch(rect)
                ax.text(i_idx + 0.12, 4 - l_idx + 0.85, f"{int(score)}",
                        fontsize=9, color="#94a3b8", fontweight="bold")

        # Plot 12 risks into their exact cells
        # Risk list with (Likelihood, Impact):
        risk_coords = {
            "RSK-01": (3, 4),  # Technical: API Latency
            "RSK-02": (4, 4),  # Operational: Eligibility Omission
            "RSK-03": (3, 4),  # Technical: Migration Truncation
            "RSK-04": (4, 3),  # Operational: Staff Productivity Slump
            "RSK-05": (4, 5),  # Financial: EDI Enrollment Delay
            "RSK-06": (3, 4),  # Clinical: Unsigned Notes
            "RSK-07": (2, 5),  # Compliance: PHI Exposure
            "RSK-08": (3, 4),  # Technical: Duplicate Records
            "RSK-09": (2, 5),  # Financial: Unbalanced AR
            "RSK-10": (2, 4),  # Regulatory: Annual Code Update
            "RSK-11": (2, 5),  # Operational: Clearinghouse Downtime
            "RSK-12": (3, 3),  # Technical: Scope Creep
        }

        # Group risks by cell for clean multi-line display
        cell_risks = {}
        for r_id, (l, i) in risk_coords.items():
            cell_risks.setdefault((l, i), []).append(r_id)

        for (l, i), r_list in cell_risks.items():
            cell_x = i - 1  # 0 to 4
            cell_y = l - 1  # 0 to 4
            
            # Formatted badge display
            badge_text = "\n".join(r_list)
            score = l * i
            badge_color = "#991b1b" if score >= 15 else ("#c2410c" if score >= 10 else ("#854d0e" if score >= 5 else "#166534"))
            
            ax.text(cell_x + 0.5, cell_y + 0.45, badge_text,
                    ha="center", va="center", fontsize=8.5, fontweight="bold",
                    color=badge_color,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="#ffffff", edgecolor=badge_color, lw=1.2))

        # Matrix Axes Styling
        ax.set_xlim(0, 5)
        ax.set_ylim(0, 5)
        ax.set_xticks([0.5, 1.5, 2.5, 3.5, 4.5])
        ax.set_xticklabels(["1 - Negligible", "2 - Minor", "3 - Moderate", "4 - Major", "5 - Catastrophic"], fontsize=9.5, fontweight="bold", color="#1e293b")
        ax.set_yticks([0.5, 1.5, 2.5, 3.5, 4.5])
        ax.set_yticklabels(["1 - Rare", "2 - Unlikely", "3 - Possible", "4 - Likely", "5 - Almost Certain"], fontsize=9.5, fontweight="bold", color="#1e293b")

        ax.set_xlabel("CONSEQUENCE / IMPACT SEVERITY", fontsize=11, fontweight="bold", color="#0f172a", labelpad=10)
        ax.set_ylabel("PROBABILITY / LIKELIHOOD", fontsize=11, fontweight="bold", color="#0f172a", labelpad=10)

        # Title & Subtitle
        ax.text(2.5, 5.35, "INTEGRATION RISK ASSESSMENT MATRIX (5x5 HEATMAP)",
                ha="center", va="center", fontsize=14, fontweight="bold", color="#0f172a")
        ax.text(2.5, 5.15, "12 Strategic Risks Mapped by Likelihood and Consequence | Severity Thresholds & Plotted IDs",
                ha="center", va="center", fontsize=9.5, color="#475569", style="italic")

        # Severity Legend at bottom
        legend_patches = [
            patches.Patch(facecolor="#fee2e2", edgecolor="#ef4444", label="Critical Risk (Score 15-25): Immediate Executive Mitigation"),
            patches.Patch(facecolor="#ffedd5", edgecolor="#f97316", label="High Risk (Score 10-14): Senior Lead Active Management"),
            patches.Patch(facecolor="#fef9c3", edgecolor="#eab308", label="Medium Risk (Score 5-9): Standard Operational Controls"),
            patches.Patch(facecolor="#dcfce7", edgecolor="#22c55e", label="Low Risk (Score 1-4): Routine Process Monitoring")
        ]
        ax.legend(handles=legend_patches, loc="upper center", bbox_to_anchor=(0.5, -0.10),
                  ncol=2, fontsize=8.5, frameon=True, edgecolor="#cbd5e1")

        plt.subplots_adjust(top=0.88, bottom=0.18)
        plt.savefig(filepath, format="png", dpi=300, bbox_inches="tight")
        plt.close(fig)
        print(f"Generated risk assessment matrix: {filepath}")
        return filepath

    def generate_all_diagrams(self) -> Dict[str, Path]:
        return {
            "architecture": self.generate_system_architecture_diagram(),
            "workflow": self.generate_implementation_workflow_diagram(),
            "risk_matrix": self.generate_risk_assessment_matrix()
        }
