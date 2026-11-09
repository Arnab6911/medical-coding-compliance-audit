"""
Week 4 Professional Word Report Generator
Compiles the comprehensive 21-section Word report:
week4/reports/Week_4_Billing_Software_Integration_Report.docx

Features:
- Student project cover page
- Exact 21 formal sections
- Standard 1.0" margins yielding exactly 6.50" printable width
- All table column widths explicitly set and strictly summing to 6.50"
- 3 embedded 300 DPI high-resolution figures (Architecture, Workflow, Risk Matrix)
- Complete vendor comparison, evaluation scoring, migration sample, validation rules,
  governance schedules, training curriculum, 10-question assessment, and risk register.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

from week4.src.models import PracticeProfile
from week4.src.software_evaluator import SoftwareEvaluator
from week4.src.migration_engine import MigrationEngine
from week4.src.validation_rules import ValidationRuleEngine
from week4.src.risk_engine import RiskEngine
from week4.src.training_engine import TrainingEngine
from week4.src.visualizer import IntegrationVisualizer

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

PRIMARY_NAVY = RGBColor(15, 41, 66)        # #0F2942
SECONDARY_BLUE = RGBColor(2, 132, 199)     # #0284C7
ACCENT_SLATE = RGBColor(71, 85, 105)       # #475569
TEXT_DARK = RGBColor(15, 23, 42)           # #0F172A
BORDER_GRAY = "CBD5E1"
HEADER_BG = "F1F5F9"
ALERT_RED = RGBColor(185, 28, 28)
ALERT_GREEN = RGBColor(22, 101, 52)

def set_cell_background(cell, hex_color: str) -> None:
    """Set the background color of a Word table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=60, bottom=60, left=80, right=80) -> None:
    """Set internal cell padding in dxa (1 pt = 20 dxa)."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

class IntegrationReportGenerator:
    def __init__(self, output_docx: Optional[Path] = None):
        self.output_docx = output_docx or (REPORTS_DIR / "Week_4_Billing_Software_Integration_Report.docx")
        self.doc = docx.Document()
        self.profile = PracticeProfile()
        self.evaluator = SoftwareEvaluator()
        self.migration = MigrationEngine()
        self.rules_engine = ValidationRuleEngine()
        self.risk_engine = RiskEngine()
        self.training = TrainingEngine()
        self.visualizer = IntegrationVisualizer()
        self._configure_document_geometry()

    def _configure_document_geometry(self) -> None:
        """Enforces standard 1.0 inch margins yielding exactly 6.50 inches printable width."""
        for section in self.doc.sections:
            section.top_margin = Inches(1.0)
            section.bottom_margin = Inches(1.0)
            section.left_margin = Inches(1.0)
            section.right_margin = Inches(1.0)
            section.page_width = Inches(8.5)
            section.page_height = Inches(11.0)

    def _add_section_heading(self, text: str) -> None:
        """Adds a standardized top-level section heading."""
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.size = Pt(13.5)
        run.font.bold = True
        run.font.color.rgb = PRIMARY_NAVY

    def _add_subsection_heading(self, text: str) -> None:
        """Adds a styled subsection heading."""
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(11)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = SECONDARY_BLUE

    def _add_paragraph(self, text: str, space_after: int = 4, italic: bool = False, bold: bool = False) -> Any:
        """Helper to add body text."""
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.size = Pt(9.5)
        run.font.color.rgb = TEXT_DARK
        run.italic = italic
        run.bold = bold
        return p

    def _add_bullet(self, bold_prefix: str, text: str) -> None:
        """Adds a bullet point with bold prefix."""
        p = self.doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        run_b = p.add_run(bold_prefix)
        run_b.font.size = Pt(9.5)
        run_b.font.bold = True
        run_b.font.color.rgb = TEXT_DARK
        run_t = p.add_run(text)
        run_t.font.size = Pt(9.5)
        run_t.font.color.rgb = TEXT_DARK

    def _add_callout(self, title: str, text: str, alert_type: str = "info") -> None:
        """Adds a shaded callout container."""
        tbl = self.doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.50)
        bg = "E0F2FE" if alert_type == "info" else ("FEF3C7" if alert_type == "warning" else "F1F5F9")
        set_cell_background(cell, bg)
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        run_title = p.add_run(f"[{title.upper()}]\n")
        run_title.font.bold = True
        run_title.font.size = Pt(9.0)
        run_title.font.color.rgb = PRIMARY_NAVY
        run_body = p.add_run(text)
        run_body.font.size = Pt(9.0)
        run_body.font.color.rgb = TEXT_DARK
        self.doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def generate_report(self) -> Path:
        """Executes full report assembly across all 21 sections."""
        print("Compiling Week 4 Integration Report...")
        # Ensure diagrams exist
        self.visualizer.generate_all_diagrams()

        # Section 1: Cover Page
        self._section_1_cover_page()
        self.doc.add_page_break()

        # Section 2: Executive Summary
        self._section_2_executive_summary()

        # Section 3: Introduction
        self._section_3_introduction()

        # Section 4: Project Objectives
        self._section_4_project_objectives()

        # Section 5: Fictional Practice Profile
        self._section_5_practice_profile()

        # Section 6: Software Research & Comparison
        self._section_6_software_comparison()

        # Section 7: Software Selection Framework
        self._section_7_selection_framework()

        # Section 8: Proposed System Architecture
        self._section_8_system_architecture()

        # Section 9: Integration Strategy
        self._section_9_integration_strategy()

        # Section 10: Data Migration Plan
        self._section_10_data_migration_plan()

        # Section 11: Real-Time Coding & Billing Validation
        self._section_11_validation_framework()

        # Section 12: Security, Privacy and Compliance
        self._section_12_security_compliance()

        # Section 13: Best Practices Guide
        self._section_13_best_practices_guide()

        # Section 14: Coding Update Governance
        self._section_14_coding_update_governance()

        # Section 15: Staff Training Program
        self._section_15_staff_training_program()

        # Section 16: Risk Assessment and Mitigation
        self._section_16_risk_assessment()

        # Section 17: Implementation Timeline
        self._section_17_implementation_timeline()

        # Section 18: KPI and Success Measurement
        self._section_18_kpi_framework()

        # Section 19: Challenges and Lessons Learned
        self._section_19_challenges_lessons()

        # Section 20: Conclusion
        self._section_20_conclusion()

        # Section 21: References
        self._section_21_references()

        # Save document
        self.output_docx.parent.mkdir(parents=True, exist_ok=True)
        self.doc.save(str(self.output_docx))
        print(f"Successfully generated 21-section Word report: {self.output_docx}")
        return self.output_docx

    # -------------------------------------------------------------
    # SECTION BUILDERS (1 to 21)
    # -------------------------------------------------------------

    def _section_1_cover_page(self) -> None:
        p_sub = self.doc.add_paragraph()
        p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_sub.paragraph_format.space_before = Pt(36)
        p_sub.paragraph_format.space_after = Pt(8)
        run_sub = p_sub.add_run("MEDICAL CODING & BILLING INTERNSHIP – STUDENT PROJECT")
        run_sub.font.size = Pt(11)
        run_sub.font.bold = True
        run_sub.font.color.rgb = SECONDARY_BLUE

        p_title = self.doc.add_paragraph()
        p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_title.paragraph_format.space_after = Pt(12)
        run_title = p_title.add_run("Week 4: Integration of Billing Software and Best Practices Implementation")
        run_title.font.size = Pt(19)
        run_title.font.bold = True
        run_title.font.color.rgb = PRIMARY_NAVY

        p_sub2 = self.doc.add_paragraph()
        p_sub2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_sub2.paragraph_format.space_after = Pt(30)
        run_sub2 = p_sub2.add_run("Strategic Architecture, Multi-Vendor Evaluation, Data Migration Protocol, Real-Time Claim Scrubbing, and Governance Framework")
        run_sub2.font.size = Pt(10.5)
        run_sub2.italic = True
        run_sub2.font.color.rgb = ACCENT_SLATE

        # Metadata Table: Width 2.2" + 4.3" = 6.50"
        tbl = self.doc.add_table(rows=6, cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        col_w = [Inches(2.20), Inches(4.30)]
        meta_items = [
            ("Project Title:", "Billing Software Integration & Best Practices (Week 4)"),
            ("Case Study Practice:", self.profile.name),
            ("Practice Scale:", f"{self.profile.provider_count} Providers | {self.profile.monthly_encounter_volume:,} Outpatient Encounters/Month"),
            ("Evaluated Solutions:", "athenahealth athenaOne, AdvancedMD, Tebra (Kareo/PatientPop)"),
            ("Document Version:", "1.0 – Production Internship Simulation"),
            ("Date of Publication:", datetime.now().strftime("%B %d, %Y"))
        ]
        for r_idx, (lbl, val) in enumerate(meta_items):
            c1, c2 = tbl.cell(r_idx, 0), tbl.cell(r_idx, 1)
            c1.width, c2.width = col_w[0], col_w[1]
            set_cell_margins(c1, 40, 40, 60, 60)
            set_cell_margins(c2, 40, 40, 60, 60)
            set_cell_background(c1, HEADER_BG)
            set_cell_background(c2, "FFFFFF")
            p1 = c1.paragraphs[0]
            p1.paragraph_format.space_after = Pt(1)
            r1 = p1.add_run(lbl)
            r1.font.bold = True
            r1.font.size = Pt(9.0)
            p2 = c2.paragraphs[0]
            p2.paragraph_format.space_after = Pt(1)
            r2 = p2.add_run(val)
            r2.font.size = Pt(9.0)

        # Academic Disclaimer Box
        self.doc.add_paragraph().paragraph_format.space_before = Pt(36)
        self._add_callout(
            "Academic Student Project & Non-PHI Compliance Disclosure",
            "This document represents a comprehensive strategic integration simulation and implementation proposal developed exclusively for academic internship purposes. All healthcare practice details, encounter metrics, provider names, patient accounts, financial balances, and data migration samples are strictly synthetic. No Protected Health Information (PHI) has been accessed or used. Vendor capabilities are derived from publicly accessible vendor documentation as of November 2026. Illustrative evaluation scores and proposed performance benchmarks reflect student integration analysis and do not constitute commercial software endorsements, actual enterprise deployments, or certified HIPAA compliance guarantees. This project is an educational simulation and does not claim official HIPAA certification, regulatory endorsement, or commercial compliance verification.",
            alert_type="warning"
        )

    def _section_2_executive_summary(self) -> None:
        self._add_section_heading("2. Executive Summary")
        self._add_paragraph(
            "This capstone report synthesizes the strategic planning, architectural design, data migration protocol, real-time validation controls, and operational governance required to successfully integrate modern cloud-based medical billing software into an independent outpatient healthcare environment. Building upon foundational insights established in Week 1 (Medical Coding Compliance Audit), Week 2 (End-to-End Billing Simulation), and Week 3 (Billing Query Resolution and Error Analysis), this Week 4 investigation elevates operational analysis to a comprehensive systems-integration perspective."
        )
        self._add_paragraph(
            f"The case study centers on {self.profile.name}, a simulated 8-provider multi-specialty outpatient practice handling approximately 3,000 patient encounters monthly (36,000 annually). The practice's legacy operational state is severely constrained by an on-premise Electronic Health Record ('MedTech v12.4') and a disconnected desktop billing module. This fragmentation drives an elevated initial claim denial rate of 14.8% (dollar-weighted), a protracted accounts receivable cycle of 52.4 Days in A/R, a 6.8-day claim submission lag, and an uncollected patient balance rate of 23.5%."
        )
        self._add_paragraph(
            "To resolve these operational deficits, this report establishes a rigorous 10-criteria weighted evaluation framework comparing three prominent commercial medical billing platforms: athenahealth athenaOne, AdvancedMD, and Tebra. Based on documented capabilities across clinical interoperability, native clearinghouse connectivity, rules-engine sophistication, and automated payment posting, athenahealth athenaOne emerged as the highest-scoring candidate (9.22/10), followed by AdvancedMD (8.78/10) and Tebra (8.13/10). All scores represent illustrative student evaluation judgments based on publicly available vendor information."
        )
        self._add_paragraph(
            "Key strategic deliverables formulated in this implementation proposal include: (1) a 7-tier cloud integration architecture leveraging HL7 FHIR and X12 EDI standards; (2) an 11-step ETL migration protocol verified by an exact $0.00 financial reconciliation variance across the 20-record synthetic test dataset totaling $14,110.00 (demonstrating protocol mechanics rather than guaranteeing zero loss in enterprise production); (3) a 12-rule pre-bill claim scrubbing engine with hard-stop controls and ethical provider clarification query protocols; (4) a 46-hour role-based staff training curriculum with an 85% competency assessment; (5) a 5x5 Likelihood-Impact risk matrix with 12 managed operational risks; and (6) an 11-metric RCM Key Performance Indicator (KPI) framework designed to reduce claim denials (dollar-weighted) to <5.0% and Days in A/R to under 35 days."
        )

    def _section_3_introduction(self) -> None:
        self._add_section_heading("3. Introduction")
        self._add_paragraph(
            "The healthcare revenue cycle management (RCM) domain has experienced an unprecedented paradigm shift over the past decade. The historical reliance on isolated desktop billing software, paper superbills, and manual batch clearinghouse uploads has become financially unsustainable and operationally hazardous. Modern healthcare reimbursement necessitates a seamless, automated, and real-time continuum connecting patient registration, clinical encounter documentation, coding validation, electronic clearinghouse EDI transmission, electronic remittance posting, and transparent patient financial accounting."
        )
        self._add_paragraph(
            "Throughout this internship, each developmental milestone has tackled a distinct dimension of the revenue cycle: Week 1 examined coding integrity and guideline compliance; Week 2 mapped the procedural flow of patient registration, claim scrubbing, and remittance posting; Week 3 diagnosed the root causes of billing errors and engineered preventive workflow controls. This Week 4 investigation consolidates these findings into an enterprise-wide integration blueprint."
        )
        self._add_paragraph(
            "Integrating new clinical and billing software is fundamentally a socio-technical transformation. It demands not only robust technical interfaces (such as HL7 FHIR APIs and X12 EDI pipelines) but also rigorous data hygiene, structured change management, role-based workforce training, and disciplined regulatory governance. This document provides a transparent, evidence-based roadmap for executing this transformation while safeguarding patient privacy and organizational financial liquidity."
        )

    def _section_4_project_objectives(self) -> None:
        self._add_section_heading("4. Project Objectives")
        self._add_paragraph("The primary strategic and technical objectives of this Week 4 integration project are defined as follows:")
        self._add_bullet("1. Multi-Vendor Market & Feature Evaluation: ", "Perform an objective, evidence-based feature comparison of athenahealth athenaOne, AdvancedMD, and Tebra across 18 functional, technical, and regulatory dimensions using official public documentation.")
        self._add_bullet("2. Transparent Decision Modeling: ", "Construct a weighted multi-criteria software selection matrix with configurable parameters to objectively evaluate vendor alignment against multi-specialty outpatient requirements.")
        self._add_bullet("3. Enterprise System Architecture Design: ", "Design a resilient 7-tier cloud integration architecture utilizing HL7 FHIR, RESTful APIs, and ASC X12 EDI standards (270/271, 837P, 276/277, 835) backed by HIPAA Security Rule safeguards.")
        self._add_bullet("4. Synthetic Data Migration, Deduplication & Financial Reconciliation: ", "Formulate a comprehensive 11-step ETL migration protocol incorporating deterministic Master Patient Index (MPI) deduplication and demonstrating exact $0.00 accounts receivable financial reconciliation.")
        self._add_bullet("5. Real-Time Pre-Bill Claim Scrubbing Engine: ", "Engineer a 12-rule pre-bill claim validation framework enforcing hard-stop gating on fatal errors, human-in-the-loop review for clinical ambiguities, and annual code set update governance.")
        self._add_bullet("6. Role-Based Workforce Enablement & Risk Control: ", "Develop a 46-hour role-specific training curriculum with an 85% assessment threshold, supported by a 5x5 Likelihood-Impact risk register managing 12 operational integration risks.")

    def _section_5_practice_profile(self) -> None:
        self._add_section_heading("5. Fictional Healthcare Practice Profile")
        self._add_paragraph(
            f"To ground the integration methodology in realistic operational parameters, this case study establishes {self.profile.name} as a fictional outpatient healthcare organization. All clinical volumes, staffing ratios, and financial metrics are synthetic constructs designed to simulate real-world multi-specialty billing complexities."
        )
        
        # Table of Practice Characteristics: Width 2.30" + 4.20" = 6.50"
        tbl = self.doc.add_table(rows=8, cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        col_w = [Inches(2.30), Inches(4.20)]
        profile_data = [
            ("Practice Classification", self.profile.practice_type),
            ("Clinical Provider Workforce", self.profile.providers_breakdown),
            ("Revenue Cycle Workforce", self.profile.billing_staff_roles),
            ("Patient Access Workforce", f"{self.profile.front_desk_staff_count} Front-Desk Coordinators across 2 clinic reception stations"),
            ("Encounter Volume", f"{self.profile.monthly_encounter_volume:,} Outpatient Encounters / Month ({self.profile.annual_encounter_volume:,} Annually)"),
            ("Legacy Technical Stack", f"{self.profile.legacy_ehr_system} and {self.profile.legacy_pm_system}"),
            ("Clearinghouse Workflow", self.profile.clearinghouse_workflow),
            ("Baseline Performance Metrics", f"Denial Rate: {self.profile.baseline_denial_rate}% | Days in AR: {self.profile.baseline_days_in_ar} | First-Pass: {self.profile.baseline_first_pass_rate}%")
        ]
        for r_idx, (k, v) in enumerate(profile_data):
            c1, c2 = tbl.cell(r_idx, 0), tbl.cell(r_idx, 1)
            c1.width, c2.width = col_w[0], col_w[1]
            set_cell_margins(c1, 35, 35, 60, 60)
            set_cell_margins(c2, 35, 35, 60, 60)
            set_cell_background(c1, HEADER_BG)
            set_cell_background(c2, "FFFFFF")
            p1 = c1.paragraphs[0]
            p1.paragraph_format.space_after = Pt(1)
            r1 = p1.add_run(k)
            r1.font.bold = True
            r1.font.size = Pt(8.5)
            p2 = c2.paragraphs[0]
            p2.paragraph_format.space_after = Pt(1)
            r2 = p2.add_run(v)
            r2.font.size = Pt(8.5)

        self._add_subsection_heading("Current Operational Bottlenecks & Gaps")
        self._add_paragraph("The practice's existing disconnected architecture suffers from five fundamental vulnerabilities:")
        for ch in self.profile.operational_challenges:
            self._add_bullet("• ", ch)

        self._add_subsection_heading("Proposed Future-State Operational Capabilities")
        self._add_paragraph("The integrated cloud solution must establish the following operational capabilities upon cutover:")
        for fs in self.profile.proposed_future_state:
            self._add_bullet("• ", fs)

    def _section_6_software_comparison(self) -> None:
        self._add_section_heading("6. Software Research and Comparison")
        self._add_paragraph(
            "An objective evaluation was conducted examining three publicly available commercial medical billing and practice management systems: athenahealth athenaOne, AdvancedMD, and Tebra. Each platform was researched across 18 distinct functional, technical, and regulatory dimensions using official vendor documentation published as of November 9, 2026."
        )
        self._add_paragraph(
            "In accordance with rigorous technical auditing standards, all features were categorized into three verification tiers: (1) Verified from official vendor information; (2) Requires vendor confirmation (e.g., custom enterprise pricing or specialized onboarding pipelines); and (3) Not verified from available public documentation. No capabilities or certifications were invented."
        )

        # Comparison Matrix Table: 6.50" total
        # Cols: Feature (1.30"), Category (0.90"), athenahealth (1.45"), AdvancedMD (1.45"), Tebra (1.40") = 6.50"
        features = self.evaluator.features
        tbl = self.doc.add_table(rows=len(features) + 1, cols=5)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        col_w = [Inches(1.30), Inches(0.90), Inches(1.45), Inches(1.45), Inches(1.40)]

        headers = ["Feature Dimension", "Category", "athenahealth athenaOne", "AdvancedMD", "Tebra"]
        for c_idx, h in enumerate(headers):
            cell = tbl.cell(0, c_idx)
            cell.width = col_w[c_idx]
            set_cell_margins(cell, 40, 40, 50, 50)
            set_cell_background(cell, "0F2942")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(h)
            run.font.bold = True
            run.font.size = Pt(8.0)
            run.font.color.rgb = RGBColor(255, 255, 255)

        for r_idx, f in enumerate(features):
            row_cells = [tbl.cell(r_idx + 1, c) for c in range(5)]
            row_data = [
                f"{f.feature_name}\n({f.feature_id})",
                f.category,
                f"{f.athenahealth_capability}\nStatus: {f.athenahealth_status}",
                f"{f.advancedmd_capability}\nStatus: {f.advancedmd_status}",
                f"{f.tebra_capability}\nStatus: {f.tebra_status}"
            ]
            bg_color = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
            for c_idx, val in enumerate(row_data):
                cell = row_cells[c_idx]
                cell.width = col_w[c_idx]
                set_cell_margins(cell, 35, 35, 45, 45)
                set_cell_background(cell, bg_color)
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(1)
                run = p.add_run(val)
                run.font.size = Pt(7.5)
                if "Status: Verified" in val:
                    # subtle green note
                    pass

        self._add_paragraph("").paragraph_format.space_after = Pt(4)
        summary = self.evaluator.get_feature_matrix_summary()
        self._add_callout(
            "Public Documentation Verification Audit",
            f"Total feature dimensions audited: {summary['total_features']}. Athenahealth: {summary['athenahealth']['verified']} verified, {summary['athenahealth']['requires_confirmation']} require confirmation. AdvancedMD: {summary['advancedmd']['verified']} verified, {summary['advancedmd']['requires_confirmation']} require confirmation. Tebra: {summary['tebra']['verified']} verified, {summary['tebra']['requires_confirmation']} require confirmation. Official vendor URLs and research timestamps are detailed in Section 21 References.",
            alert_type="info"
        )

    def _section_7_selection_framework(self) -> None:
        self._add_section_heading("7. Software Selection Framework")
        self._add_paragraph(
            "To eliminate subjective bias, an objective multi-criteria decision analysis (MCDA) framework was engineered. Ten distinct evaluation criteria were established, weighted to reflect the operational priorities of a multi-specialty outpatient practice transitioning from disconnected legacy applications."
        )
        self._add_paragraph(
            "Evaluation weights prioritize core billing workflows (15%), pre-bill claim scrubbing (15%), clinical interoperability (10%), and real-time eligibility (10%). All vendor scores (scale 1.0 to 10.0) represent illustrative student evaluation judgments derived from documented features and architectural alignment, not independent product certifications or commercial endorsements."
        )

        res = self.evaluator.calculate_scores()
        breakdown = res["breakdown"]

        # Selection Matrix Table: 6.50" total
        # Cols: Criterion (1.90"), Weight (0.70"), Athena (1.30"), AdvMD (1.30"), Tebra (1.30") = 6.50"
        tbl = self.doc.add_table(rows=len(breakdown) + 2, cols=5)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        col_w = [Inches(1.90), Inches(0.70), Inches(1.30), Inches(1.30), Inches(1.30)]

        headers = ["Evaluation Criterion", "Weight", "athenahealth", "AdvancedMD", "Tebra"]
        for c_idx, h in enumerate(headers):
            cell = tbl.cell(0, c_idx)
            cell.width = col_w[c_idx]
            set_cell_margins(cell, 40, 40, 50, 50)
            set_cell_background(cell, "0F2942")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(h)
            run.font.bold = True
            run.font.size = Pt(8.0)
            run.font.color.rgb = RGBColor(255, 255, 255)

        for r_idx, b in enumerate(breakdown):
            row_cells = [tbl.cell(r_idx + 1, c) for c in range(5)]
            row_data = [
                b["name"],
                f"{b['weight_pct']}%",
                f"{b['score_athena']} ({b['weighted_athena']:.2f} pts)",
                f"{b['score_advancedmd']} ({b['weighted_advancedmd']:.2f} pts)",
                f"{b['score_tebra']} ({b['weighted_tebra']:.2f} pts)"
            ]
            bg_color = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
            for c_idx, val in enumerate(row_data):
                cell = row_cells[c_idx]
                cell.width = col_w[c_idx]
                set_cell_margins(cell, 35, 35, 45, 45)
                set_cell_background(cell, bg_color)
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(1)
                run = p.add_run(val)
                run.font.size = Pt(8.0)

        # Total Row
        tot_cells = [tbl.cell(len(breakdown) + 1, c) for c in range(5)]
        scores = res["vendor_scores"]
        tot_data = [
            "TOTAL WEIGHTED SCORE",
            "100.0%",
            f"{scores['athenahealth athenaOne']:.2f} / 10.0",
            f"{scores['AdvancedMD']:.2f} / 10.0",
            f"{scores['Tebra']:.2f} / 10.0"
        ]
        for c_idx, val in enumerate(tot_data):
            cell = tot_cells[c_idx]
            cell.width = col_w[c_idx]
            set_cell_margins(cell, 40, 40, 50, 50)
            set_cell_background(cell, "E2E8F0")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(val)
            run.font.bold = True
            run.font.size = Pt(8.5)
            run.font.color.rgb = PRIMARY_NAVY

        self._add_paragraph("").paragraph_format.space_after = Pt(4)
        self._add_callout(
            "Selection Outcome & Architectural Rationale",
            f"Recommendation: {res['recommended_vendor']} ranked highest with an illustrative weighted score of {res['recommended_score']:.2f}/10.0. Key differentiators include its native built-in clearinghouse on the athenaNet backbone (eliminating external EDI portal handoffs), continuously updated cloud-wide payer rules, and an open Developer Portal with documented REST APIs and certified FHIR endpoints. AdvancedMD (8.78) demonstrated exceptional multi-clearinghouse flexibility and published pricing transparency. Tebra (8.13) presented an intuitive interface highly suited for smaller practices. Note: Selection rankings and scores represent illustrative student evaluation judgments based on publicly documented vendor capabilities and feature alignment with the multi-specialty practice profile. This is not an independent product performance certification, commercial endorsement, or official audit.",
            alert_type="info"
        )

    def _section_8_system_architecture(self) -> None:
        self._add_section_heading("8. Proposed System Architecture")
        self._add_paragraph(
            "The proposed enterprise integration architecture establishes a resilient 7-tier cloud continuum connecting clinical documentation, revenue cycle management, electronic data interchange (EDI), and executive oversight. The architectural paradigm emphasizes bi-directional synchronization, zero duplicate data entry, and proposed technical safeguards designed in alignment with HIPAA Security Rule specifications."
        )

        # Embed Figure 1
        arch_img = REPORTS_DIR / "integration_architecture.png"
        if arch_img.exists():
            p_img = self.doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(4)
            self.doc.add_picture(str(arch_img), width=Inches(6.20))
            p_cap = self.doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(8)
            r_cap = p_cap.add_run("Figure 1: Proposed 7-Tier Cloud Healthcare IT & Revenue Cycle Integration Architecture (300 DPI)")
            r_cap.font.size = Pt(8.5)
            r_cap.font.bold = True
            r_cap.font.color.rgb = ACCENT_SLATE

        self._add_subsection_heading("Architectural Tiers & Data Flow Specifications")
        tiers = [
            ("Tier 1: Patient Intake & Access: ", "Captures verified legal demographics, scans insurance cards, queries real-time X12 270 eligibility 72h/24h in advance, and collects patient copayments at check-in."),
            ("Tier 2: Clinical EHR Documentation: ", "Provides structured outpatient encounter charting, MDM/time-based E/M code selection, electronic superbill assembly, and mandatory 24-hour attending physician e-signature gating."),
            ("Tier 3: Pre-Bill Rules Scrubber: ", "Executes automated pre-submission error trapping, enforcing hard-stop gating on fatal errors (missing notes, deleted ICD-10 codes, NCCI unbundling) and routing warnings to coding queues."),
            ("Tier 4: Practice Management & Charge Staging: ", "Maintains fee schedules, unbilled encounter worklists, secondary claim staging, certified coder audit queues, and open accounts receivable ledgers."),
            ("Tier 5: Integrated Clearinghouse & EDI Gateway: ", "Automates daily batch transmission of X12 837P claims, tracks real-time 999 acknowledgments and 277CA rejections, and ingests X12 835 Remittance Advices."),
            ("Tier 6: Payment Posting & Patient Accounting: ", "Auto-posts 835 remittances, applies contractual write-offs, routes secondary crossover claims, and generates electronic patient statements via the patient portal."),
            ("Tier 7: Executive RCM Analytics & Compliance: ", "Monitors the 11 core financial KPIs, analyzes denial trends by CARC/RARC codes, maintains proposed immutable security audit logs supporting HIPAA Security Rule audit-control requirements, and coordinates annual coding updates.")
        ]
        for t_name, t_desc in tiers:
            self._add_bullet(t_name, t_desc)

        self._add_subsection_heading("Interface Standards & Interoperability Protocols")
        self._add_paragraph("The integration pipeline enforces the following standardized healthcare data interchange specifications:")
        self._add_bullet("• HL7 FHIR R4: ", "Standardized RESTful JSON resources (Patient, Encounter, Coverage, Claim) for clinical-to-billing synchronization and third-party portal connectivity.")
        self._add_bullet("• ASC X12 270 / 271: ", "Health Care Eligibility Benefit Inquiry (270) and Information Response (271) for automated pre-service benefit determination.")
        self._add_bullet("• ASC X12 837P (v5010): ", "Health Care Claim: Professional transaction standard for electronic claim submission to government and commercial payers.")
        self._add_bullet("• ASC X12 276 / 277: ", "Health Care Claim Status Request (276) and Notification (277/277CA) for real-time tracking of clearinghouse and payer adjudication queues.")
        self._add_bullet("• ASC X12 835 (v5010): ", "Health Care Claim Payment / Advice transaction standard for automated electronic remittance posting, adjustment balancing, and denial code ingestion.")

    def _section_9_integration_strategy(self) -> None:
        self._add_section_heading("9. Integration Strategy")
        self._add_paragraph(
            "To mitigate operational disruption and revenue cycle volatility, a structured 12-phase implementation strategy is established across a 24-week timeline. The methodology organizes deployment into four progressive stages: Evaluation & Design, Technical Preparation & Migration, Testing & Training, and Cutover & Optimization."
        )

        # Embed Figure 2
        wf_img = REPORTS_DIR / "integration_workflow.png"
        if wf_img.exists():
            p_img = self.doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(4)
            self.doc.add_picture(str(wf_img), width=Inches(6.20))
            p_cap = self.doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(8)
            r_cap = p_cap.add_run("Figure 2: 12-Phase Structured Implementation Roadmap Across 4 Deployment Stages (300 DPI)")
            r_cap.font.size = Pt(8.5)
            r_cap.font.bold = True
            r_cap.font.color.rgb = ACCENT_SLATE

        self._add_subsection_heading("Implementation Phase Governance Matrix")
        # Table of 12 Phases: Width: Phase (1.10"), Stage (1.00"), Role (1.20"), Key Deliverable (1.80"), Gate Criteria (1.40") = 6.50"
        tbl = self.doc.add_table(rows=13, cols=5)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        col_w = [Inches(1.10), Inches(1.00), Inches(1.20), Inches(1.80), Inches(1.40)]

        headers = ["Phase", "Stage", "Lead Role", "Key Deliverables", "Gate Criteria"]
        for c_idx, h in enumerate(headers):
            cell = tbl.cell(0, c_idx)
            cell.width = col_w[c_idx]
            set_cell_margins(cell, 40, 40, 50, 50)
            set_cell_background(cell, "0F2942")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(h)
            run.font.bold = True
            run.font.size = Pt(8.0)
            run.font.color.rgb = RGBColor(255, 255, 255)

        phases_data = [
            ("Phase 1", "Stage 1", "Project Manager", "Stakeholder requirements & legacy gap analysis report", "Steering Committee sign-off on scope"),
            ("Phase 2", "Stage 1", "Lead Architect", "Vendor RFP comparison, demos, BAA execution", "Vendor selection & legal contract execution"),
            ("Phase 3", "Stage 1", "Clinical / Billing Leads", "Clinical templates, fee schedules, superbill configs", "Practice workflow sign-off by Medical Director"),
            ("Phase 4", "Stage 2", "Lead Architect", "FHIR/REST API endpoints, X12 EDI pipelines", "Successful EDI 270/837/835 sandbox connectivity"),
            ("Phase 5", "Stage 2", "Migration Engineer", "ETL data extraction scripts & MPI deduplication logic", "Schema validation & test data cleansing pass"),
            ("Phase 6", "Stage 2", "Billing Supervisor", "Test migration runs & open AR balance audit", "100% census match & $0.00 financial variance"),
            ("Phase 7", "Stage 3", "Lead Coder (CPC)", "12 pre-bill scrubber rules & NCCI/MUE tables", "Zero fatal errors bypassed in scrubber validation"),
            ("Phase 8", "Stage 3", "Integration Engineer", "500-claim end-to-end sandbox batch processing", "98%+ first-pass acceptance in test clearinghouse"),
            ("Phase 9", "Stage 3", "Training Lead", "Role-based training delivery across 5 modules", "100% of staff scoring >= 85% on assessment"),
            ("Phase 10", "Stage 4", "Clinic Supervisor", "2-week live pilot deployment in Cardiology clinic", "Pilot denial rate < 6.0%; zero fatal incidents"),
            ("Phase 11", "Stage 4", "SteerCo / PM", "Cutover weekend, final AR snapshot, enterprise live", "Clean cutover with active 837P submissions"),
            ("Phase 12", "Stage 4", "Practice Manager", "Weekly KPI dashboards, monthly denial root-cause", "Achievement of DAR < 35.0 days and dollar-weighted denial rate <5.0% (target ceiling)")
        ]
        for r_idx, (p_num, stg, role, deliv, gate) in enumerate(phases_data):
            row_cells = [tbl.cell(r_idx + 1, c) for c in range(5)]
            row_data = [p_num, stg, role, deliv, gate]
            bg_color = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
            for c_idx, val in enumerate(row_data):
                cell = row_cells[c_idx]
                cell.width = col_w[c_idx]
                set_cell_margins(cell, 35, 35, 45, 45)
                set_cell_background(cell, bg_color)
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(1)
                run = p.add_run(val)
                run.font.size = Pt(7.5)

    def _section_10_data_migration_plan(self) -> None:
        self._add_section_heading("10. Data Migration Plan")
        self._add_paragraph(
            "Migrating historical healthcare data from an on-premise relational database ('MedTech v12.4') to a cloud-based practice management system is fraught with operational and financial risk. To safeguard data integrity, prevent duplicate record creation, and eliminate financial balance sheet leakage, a formal 11-step ETL migration protocol is enforced."
        )

        self._add_subsection_heading("The 11-Step Data Migration Protocol")
        steps = [
            ("Step 1: Source System Assessment: ", "Audit MedTech v12.4 database schema, table structures, and field truncation risks."),
            ("Step 2: Data Extraction & Staging: ", "Extract patient master records, insurance policies, clinical histories, and open AR into encrypted staging storage."),
            ("Step 3: Schema Mapping & Crosswalking: ", "Map legacy tables to target cloud database entities, establishing code crosswalks."),
            ("Step 4: Data Cleansing & Normalization: ", "Standardize DOB strings to ISO-8601 (YYYY-MM-DD), format phone numbers, and apply postal ZIP+4 hyphenation."),
            ("Step 5: MPI Deduplication Engine: ", "Run deterministic and fuzzy matching algorithms to detect duplicate charts and consolidate patient histories."),
            ("Step 6: Transformation & Formatting: ", "Structure data into ingestion-ready FHIR/CSV formats conforming to cloud vendor specifications."),
            ("Step 7: Pilot Test Migration: ", "Execute 3 test loads into staging sandbox; evaluate field truncation, rejected records, and exceptions."),
            ("Step 8: Record Count & Field Reconciliation: ", "Verify 100% record-count identity across all extracted vs loaded tables."),
            ("Step 9: Financial AR Trial Balance Audit: ", "Execute line-by-line financial reconciliation matching legacy trial balance to target system ($0.00 variance required in synthetic validation; tolerance thresholds defined for production)."),
            ("Step 10: Final Cutover Migration: ", "Execute production cutover over scheduled weekend window; apply delta transactions."),
            ("Step 11: Rollback & Recovery Assurance: ", "Maintain a secure, read-only snapshot of the legacy MedTech database for a proposed seven-year retention period, subject to applicable federal and state record-retention requirements, contractual obligations, and the organization's approved retention policy.")
        ]
        for s_title, s_desc in steps:
            self._add_bullet(s_title, s_desc)

        self._add_subsection_heading("Synthetic Migration Dataset Audit & Verification")
        self._add_paragraph(
            "To prove protocol efficacy without utilizing real patient health information (PHI), a 20-record synthetic patient migration dataset was processed through the cleansing, deduplication, and financial reconciliation pipeline."
        )

        # Migration Sample Table: 6.50" total
        # Cols: Patient ID (0.90"), Name (1.10"), DOB (0.80"), Primary Payer (1.20"), Legacy AR (0.80"), Migrated AR (0.80"), Variance & Status (0.90") = 6.50"
        records = self.migration.records
        tbl = self.doc.add_table(rows=len(records) + 1, cols=7)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        col_w = [Inches(0.90), Inches(1.10), Inches(0.80), Inches(1.20), Inches(0.80), Inches(0.80), Inches(0.90)]

        headers = ["Patient ID", "Patient Name", "DOB", "Primary Payer", "Legacy AR", "Migrated AR", "Status / Notes"]
        for c_idx, h in enumerate(headers):
            cell = tbl.cell(0, c_idx)
            cell.width = col_w[c_idx]
            set_cell_margins(cell, 35, 35, 40, 40)
            set_cell_background(cell, "0F2942")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(h)
            run.font.bold = True
            run.font.size = Pt(7.5)
            run.font.color.rgb = RGBColor(255, 255, 255)

        for r_idx, r in enumerate(records):
            row_cells = [tbl.cell(r_idx + 1, c) for c in range(7)]
            row_data = [
                r.legacy_patient_id,
                f"{r.first_name} {r.last_name}",
                r.dob,
                r.primary_payer,
                f"${r.legacy_ar_balance:,.2f}",
                f"${r.migrated_ar_balance:,.2f}",
                f"{r.migration_status}\nVar: ${r.variance:.2f}"
            ]
            bg_color = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
            for c_idx, val in enumerate(row_data):
                cell = row_cells[c_idx]
                cell.width = col_w[c_idx]
                set_cell_margins(cell, 30, 30, 40, 40)
                set_cell_background(cell, bg_color)
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(1)
                run = p.add_run(val)
                run.font.size = Pt(7.0)

        # Financial Reconciliation Summary
        self._add_paragraph("").paragraph_format.space_after = Pt(4)
        rec = self.migration.reconcile_financials()
        self._add_callout(
            "Financial Ledger Reconciliation Audit Sign-Off",
            f"Census Account Total: {rec['total_account_count']} records. Total Legacy Accounts Receivable Balance: ${rec['total_legacy_ar']:,.2f}. Total Migrated Accounts Receivable Balance: ${rec['total_migrated_ar']:,.2f}. Net Reconciliation Variance: ${rec['net_variance']:,.2f} (100.0% Financial Identity Achieved across the 20-record synthetic test dataset). Master Patient Index (MPI) deduplication successfully detected and consolidated duplicate accounts LEG-1019 ('Robert Banner') and LEG-1020 ('Bob Banner') without ledger loss. Note: While zero variance was verified in this controlled synthetic sample, enterprise production migrations carry inherent operational risks and require extensive parallel trial balancing rather than an unverified assumption of zero data loss.",
            alert_type="info"
        )

    def _section_11_validation_framework(self) -> None:
        self._add_section_heading("11. Real-Time Coding and Billing Validation")
        self._add_paragraph(
            "A high-performing revenue cycle requires proactive pre-bill claim scrubbing rather than retroactive denial appeals. The integration framework implements a 12-rule automated validation engine operating prior to electronic X12 837P transmission. Rules are classified into two operational tiers: HARD_STOP (blocking transmission until rectified) and WARNING (triggering human-in-the-loop review by certified medical coders)."
        )

        # Rules Table: 6.50" total
        # Cols: Rule ID (0.80"), Name & Trigger (2.30"), Category (1.10"), Severity (0.90"), Resolution Protocol (1.40") = 6.50"
        rules = self.rules_engine.rules
        tbl = self.doc.add_table(rows=len(rules) + 1, cols=5)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        col_w = [Inches(0.80), Inches(2.30), Inches(1.10), Inches(0.90), Inches(1.40)]

        headers = ["Rule ID", "Rule Name & Description", "Category", "Severity", "Enforcement & Resolution Guidance"]
        for c_idx, h in enumerate(headers):
            cell = tbl.cell(0, c_idx)
            cell.width = col_w[c_idx]
            set_cell_margins(cell, 40, 40, 50, 50)
            set_cell_background(cell, "0F2942")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(h)
            run.font.bold = True
            run.font.size = Pt(8.0)
            run.font.color.rgb = RGBColor(255, 255, 255)

        for r_idx, r in enumerate(rules):
            row_cells = [tbl.cell(r_idx + 1, c) for c in range(5)]
            row_data = [
                r.rule_id,
                f"{r.rule_name}\n• Trigger: {r.trigger_condition}",
                r.category,
                r.severity,
                r.resolution_guidance
            ]
            bg_color = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
            for c_idx, val in enumerate(row_data):
                cell = row_cells[c_idx]
                cell.width = col_w[c_idx]
                set_cell_margins(cell, 35, 35, 45, 45)
                set_cell_background(cell, bg_color)
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(1)
                run = p.add_run(val)
                run.font.size = Pt(7.5)
                if r.severity == "HARD_STOP" and c_idx == 3:
                    run.font.bold = True
                    run.font.color.rgb = ALERT_RED
                elif r.severity == "WARNING" and c_idx == 3:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(180, 83, 9)

        self._add_paragraph("").paragraph_format.space_after = Pt(4)
        self._add_callout(
            "Ethical Coding & Human-in-the-Loop Principle",
            "CRITICAL COMPLIANCE DIRECTIVE: The automated claim scrubber is strictly an administrative gatekeeper and diagnostic filter. Software must NEVER automatically alter assigned ICD-10-CM diagnosis codes, append procedural modifiers, or modify clinical documentation to force claim reimbursement. All warning-level findings, medical necessity ambiguities, and coding queries require thorough review and documented authentication by certified medical coders (CPC/CCS) or the attending clinician.",
            alert_type="warning"
        )

    def _section_12_security_compliance(self) -> None:
        self._add_section_heading("12. Security, Privacy and Compliance")
        self._add_paragraph(
            "Protecting electronic Protected Health Information (ePHI) is a fundamental legal obligation under the Health Insurance Portability and Accountability Act (HIPAA) Security and Privacy Rules (45 CFR Parts 160 and 164) and HITECH standards. The proposed integration strategy incorporates enterprise safeguards across administrative, physical, and technical domains."
        )
        self._add_paragraph(
            "Statutory Framework vs. Proposed Technical Specifications: The HIPAA Security Rule (45 CFR § 164.312) is inherently technology-neutral and establishes required and addressable implementation specifications rather than mandating specific proprietary algorithms, key lengths, or software solutions. For instance, encryption at rest (§ 164.312(a)(2)(iv)) and encryption in transit (§ 164.312(e)(2)(ii)) are addressable specifications. The architectural choices detailed below—specifically AES-256 encryption at rest, TLS 1.3 in transit, a seven-year immutable log retention schedule, and disaster recovery metrics of RPO < 15 minutes and RTO < 2 hours—represent proposed industry-standard architectural selections rather than explicit statutory mandates. Notably, seven-year audit-log retention is designated as a proposed project policy subject to applicable state law and contractual requirements, not as a universal HIPAA requirement (which mandates a 6-year retention period for compliance documentation under 45 CFR § 164.316(b)(2)(i)). Furthermore, the Department of Health and Human Services (HHS) Office for Civil Rights (OCR) does not endorse, certify, or provide compliance seals for software products or academic simulations. This simulated project is an educational proposal and does not possess or claim official HIPAA certification."
        )

        self._add_subsection_heading("Administrative Safeguards (45 CFR § 164.308)")
        self._add_bullet("• Role-Based Access Control (RBAC): ", "Staff permissions strictly follow the principle of least privilege. Front-desk personnel access demographic and eligibility modules but are restricted from clinical progress notes; clinical providers access charting and superbills but cannot edit billing rules; billing specialists manage claim queues without patient record creation rights.")
        self._add_bullet("• Business Associate Agreements (BAAs): ", "Formal, executed BAAs are required with the cloud software vendor, clearinghouse partner, and third-party IT contractors prior to transferring any staging data or establishing API credentials.")
        self._add_bullet("• Security Workforce Training: ", "Mandatory annual HIPAA privacy training and quarterly phishing simulations required for all clinic staff.")

        self._add_subsection_heading("Physical & Technical Safeguards (Proposed Architecture under 45 CFR § 164.310 & § 164.312)")
        self._add_bullet("• Cryptographic Standards (Proposed Architecture): ", "End-to-end data encryption enforcing AES-256 for all stored data, database backups, and staging snapshots (at-rest), and TLS 1.3 for all web portal traffic, API calls, and EDI transmissions (in-transit).")
        self._add_bullet("• Multi-Factor Authentication (MFA): ", "Enforced MFA across all provider, billing, and administrative portal access points utilizing FIDO2/WebAuthn or hardware security tokens.")
        self._add_bullet("• Immutable Audit Logging (Proposed Architecture): ", "System captures immutable log records of every patient chart view, demographic edit, claim dispatch, payment posting, and user login event. Seven-year retention of security audit logs in write-once-read-many (WORM) cloud storage is a proposed project policy subject to applicable state law and contractual requirements, not a universal HIPAA requirement.")
        self._add_bullet("• Business Continuity & Disaster Recovery (Proposed Targets): ", "Proposed Recovery Point Objective (RPO) of < 15 minutes and Recovery Time Objective (RTO) of < 2 hours backed by geo-redundant automated cloud database replication.")

    def _section_13_best_practices_guide(self) -> None:
        self._add_section_heading("13. Best Practices Guide")
        self._add_paragraph(
            "Achieving sustained operational excellence requires coupling technology with standardized operational best practices across the entire revenue cycle continuum."
        )
        bp_stages = [
            ("1. Patient Access & Front-Desk Workflow: ", "Perform automated 72h and 24h pre-service X12 270 eligibility checks for all scheduled appointments. Require front-desk staff to review eligibility flags upon patient check-in, collect copayments and deductible portions at the point of service (POS), and scan photo ID and insurance cards into the electronic chart."),
            ("2. Clinical Documentation Integrity (CDI): ", "Physicians document encounters utilizing structured smart phrases and specialty-specific templates. Clinicians must record clear medical decision making (MDM) justification or time thresholds to support E/M levels. Progress notes must be finalized and electronically signed within 24 hours of encounter completion."),
            ("3. Certified Coding Oversight: ", "Certified professional coders review high-level E/M visits (99205/99215), minor surgical procedures requiring modifier -25, and surgical unbundling edits. Coders verify that documented clinical indications satisfy payer Local Coverage Determinations (LCDs) prior to claim generation."),
            ("4. Pre-Bill Claim Scrubbing: ", "Zero tolerance for bypassing hard-stop scrubber edits. Billing specialists review claim rejection worklists daily, ensuring that all demographic or NPI errors are corrected within 24 hours of scrubber flagging."),
            ("5. Denial Management & Root-Cause Triage: ", "All incoming claim denials are categorized by CARC and RARC codes within 48 hours of receipt. Appeals are submitted electronically with pre-formatted evidence packets and attached clinical documentation. Monthly denial trends are analyzed by provider and specialty to prevent recurring errors."),
            ("6. Patient Financial Transparency: ", "Deliver clear, itemized patient billing statements immediately following primary and secondary payer adjudication. Provide self-service online portal payments, automated payment plans for balances over $250, and credit-card-on-file guarantees for self-pay services.")
        ]
        for s_title, s_desc in bp_stages:
            self._add_bullet(s_title, s_desc)

    def _section_14_coding_update_governance(self) -> None:
        self._add_section_heading("14. Coding Update Governance")
        self._add_paragraph(
            "Medical code sets are dynamic regulatory constructs. Ingesting annual and mid-year coding updates on schedule is critical to preventing mass claim rejections for deleted or truncated codes. The practice enforces a strict Code Update Governance Protocol."
        )

        self._add_subsection_heading("Annual & Mid-Year Code Release Lifecycle")
        schedules = self.rules_engine.get_code_governance_schedule()
        for sched in schedules:
            self._add_bullet(f"• {sched['cycle']} (Effective: {sched['effective_date']}): ", f"Governance Window: {sched['governance_window']}. Risk Controls: {sched['risk_controls']}")

        self._add_subsection_heading("Date of Service (DOS) Gating Architecture")
        self._add_paragraph(
            "The practice management rules engine enforces strict Date of Service (DOS) gating. Code validity is evaluated dynamically based on the encounter DOS rather than the billing submission date. For example, for encounters taking place in calendar year 2026, an encounter occurring on September 28, 2026 must be billed using FY2026 ICD-10-CM codes, even if processed in October; conversely, an encounter occurring on or after October 1, 2026 (such as October 2, 2026) must utilize FY2027 ICD-10-CM codes. Annual CPT/HCPCS code updates take effect on January 1 of each calendar year. Similarly, Evaluation and Management (E/M) code selection must adhere to current applicable E/M documentation guidelines, with code descriptions and specific complexity requirements verified against the encounter date of service and authorized AMA CPT materials (without reproducing proprietary code text). The system maintains historical code databases in parallel to eliminate billing lockouts during transition windows."
        )

        self._add_subsection_heading("Ethical Provider Clarification Query Protocol")
        guidelines = self.rules_engine.format_provider_query_guideline()
        self._add_paragraph(
            f"When clinical documentation lacks specificity or exhibits conflicting entries, coders must execute the formal {guidelines['policy_title']}. Under AHIMA and ACDIS standards:"
        )
        for princ in guidelines["core_principles"]:
            self._add_bullet("• ", princ)

    def _section_15_staff_training_program(self) -> None:
        self._add_section_heading("15. Staff Training Program")
        self._add_paragraph(
            "Human competency is the ultimate determinant of software integration success. The training program establishes a role-based 46-hour curriculum across five distinct organizational roles, concluding with a mandatory 10-question competency assessment requiring an 85% passing grade prior to granting production system access."
        )

        # Training Modules Table: 6.50" total
        # Cols: Role (1.60"), Title (2.10"), Hours (0.60"), Objectives (2.20") = 6.50"
        modules = self.training.modules
        tbl = self.doc.add_table(rows=len(modules) + 1, cols=4)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        col_w = [Inches(1.60), Inches(2.10), Inches(0.60), Inches(2.20)]

        headers = ["Target Role", "Module Title", "Duration", "Core Learning Competencies"]
        for c_idx, h in enumerate(headers):
            cell = tbl.cell(0, c_idx)
            cell.width = col_w[c_idx]
            set_cell_margins(cell, 40, 40, 50, 50)
            set_cell_background(cell, "0F2942")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(h)
            run.font.bold = True
            run.font.size = Pt(8.0)
            run.font.color.rgb = RGBColor(255, 255, 255)

        for r_idx, m in enumerate(modules):
            row_cells = [tbl.cell(r_idx + 1, c) for c in range(4)]
            row_data = [
                m.target_role,
                m.title,
                f"{m.duration_hours:.1f} hrs",
                "\n".join([f"• {obj}" for obj in m.learning_objectives[:3]])
            ]
            bg_color = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
            for c_idx, val in enumerate(row_data):
                cell = row_cells[c_idx]
                cell.width = col_w[c_idx]
                set_cell_margins(cell, 35, 35, 45, 45)
                set_cell_background(cell, bg_color)
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(1)
                run = p.add_run(val)
                run.font.size = Pt(7.5)

        self._add_subsection_heading("Knowledge Assessment & Verified Answer Key")
        self._add_paragraph(
            "All personnel complete the 10-question evaluation upon concluding their role curriculum. The table below provides the full question stems, answer options, verified correct responses, operational explanations, and authoritative guideline citations."
        )

        # Questions Table: 6.50" total
        # Cols: Q# & Role (1.00"), Question Stem (2.20"), Correct Answer (1.30"), Explanation & Citation (2.00") = 6.50"
        questions = self.training.questions
        tbl_q = self.doc.add_table(rows=len(questions) + 1, cols=4)
        tbl_q.alignment = WD_TABLE_ALIGNMENT.CENTER
        col_w_q = [Inches(1.00), Inches(2.20), Inches(1.30), Inches(2.00)]

        q_headers = ["Q# & Role", "Question Stem & Options", "Correct Answer", "Operational Rationale & Guideline Citation"]
        for c_idx, h in enumerate(q_headers):
            cell = tbl_q.cell(0, c_idx)
            cell.width = col_w_q[c_idx]
            set_cell_margins(cell, 40, 40, 50, 50)
            set_cell_background(cell, "0F2942")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(h)
            run.font.bold = True
            run.font.size = Pt(8.0)
            run.font.color.rgb = RGBColor(255, 255, 255)

        for r_idx, q in enumerate(questions):
            row_cells = [tbl_q.cell(r_idx + 1, c) for c in range(4)]
            opts_text = "\n".join([f"[{idx+1}] {opt}" for idx, opt in enumerate(q.options)])
            correct_txt = f"Option [{q.correct_option_index + 1}]:\n{q.options[q.correct_option_index]}"
            rationale_txt = f"{q.explanation}\nRef: {q.guideline_reference}"

            row_data = [
                f"{q.question_id}\n({q.target_role})",
                f"{q.question}\n\nOptions:\n{opts_text}",
                correct_txt,
                rationale_txt
            ]
            bg_color = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
            for c_idx, val in enumerate(row_data):
                cell = row_cells[c_idx]
                cell.width = col_w_q[c_idx]
                set_cell_margins(cell, 35, 35, 45, 45)
                set_cell_background(cell, bg_color)
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(1)
                run = p.add_run(val)
                run.font.size = Pt(7.0)
                if c_idx == 2:
                    run.font.bold = True
                    run.font.color.rgb = ALERT_GREEN

    def _section_16_risk_assessment(self) -> None:
        self._add_section_heading("16. Risk Assessment and Mitigation")
        self._add_paragraph(
            "A structured risk management program was executed to identify, quantify, and mitigate potential integration threats. Twelve strategic risks spanning Technical, Operational, Financial, Clinical, Compliance, and Regulatory categories were evaluated on a 5x5 Likelihood (1-5) and Consequence/Impact (1-5) scale."
        )

        # Embed Figure 3
        risk_img = REPORTS_DIR / "risk_assessment_matrix.png"
        if risk_img.exists():
            p_img = self.doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(4)
            self.doc.add_picture(str(risk_img), width=Inches(6.20))
            p_cap = self.doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(8)
            r_cap = p_cap.add_run("Figure 3: 5x5 Likelihood vs Impact Integration Risk Assessment Matrix Heatmap (300 DPI)")
            r_cap.font.size = Pt(8.5)
            r_cap.font.bold = True
            r_cap.font.color.rgb = ACCENT_SLATE

        self._add_subsection_heading("Enterprise Integration Risk Register")
        # Risk Table: 6.50" total
        # Cols: ID (0.70"), Category & Title (1.60"), L/I/Score (0.80"), Mitigation Strategy (1.80"), Contingency & Owner (1.60") = 6.50"
        risks = self.risk_engine.risks
        tbl = self.doc.add_table(rows=len(risks) + 1, cols=5)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        col_w = [Inches(0.70), Inches(1.60), Inches(0.80), Inches(1.80), Inches(1.60)]

        headers = ["Risk ID", "Category & Title", "L x I = Score", "Proactive Mitigation Strategy", "Contingency Plan & Owner"]
        for c_idx, h in enumerate(headers):
            cell = tbl.cell(0, c_idx)
            cell.width = col_w[c_idx]
            set_cell_margins(cell, 40, 40, 50, 50)
            set_cell_background(cell, "0F2942")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(h)
            run.font.bold = True
            run.font.size = Pt(8.0)
            run.font.color.rgb = RGBColor(255, 255, 255)

        for r_idx, r in enumerate(risks):
            row_cells = [tbl.cell(r_idx + 1, c) for c in range(5)]
            row_data = [
                r.risk_id,
                f"{r.title}\n({r.category})",
                f"L:{r.likelihood} x I:{r.impact}\nScore: {r.risk_score} ({r.risk_level})",
                r.mitigation_strategy,
                f"{r.contingency_plan}\nOwner: {r.owner_role}"
            ]
            bg_color = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
            for c_idx, val in enumerate(row_data):
                cell = row_cells[c_idx]
                cell.width = col_w[c_idx]
                set_cell_margins(cell, 35, 35, 45, 45)
                set_cell_background(cell, bg_color)
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(1)
                run = p.add_run(val)
                run.font.size = Pt(7.0)
                if c_idx == 2 and r.risk_score >= 15:
                    run.font.bold = True
                    run.font.color.rgb = ALERT_RED
                elif c_idx == 2 and r.risk_score >= 10:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(194, 65, 12)

    def _section_17_implementation_timeline(self) -> None:
        self._add_section_heading("17. Implementation Timeline")
        self._add_paragraph(
            "The 24-week implementation schedule is organized into sequential milestones with defined gatekeeper approvals. Critical path activities—specifically payer EDI clearinghouse re-enrollment, legacy data migration balancing, and staff competency testing—are prioritized to ensure a smooth cutover."
        )

        # Timeline Table: Width: Weeks (1.10"), Stage / Activity (2.20"), Key Milestones (1.80"), Gate Approval (1.40") = 6.50"
        tbl = self.doc.add_table(rows=7, cols=4)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        col_w = [Inches(1.10), Inches(2.20), Inches(1.80), Inches(1.40)]

        headers = ["Timeline", "Implementation Stage & Activities", "Milestones & Key Outputs", "Gatekeeper Approval"]
        for c_idx, h in enumerate(headers):
            cell = tbl.cell(0, c_idx)
            cell.width = col_w[c_idx]
            set_cell_margins(cell, 40, 40, 50, 50)
            set_cell_background(cell, "0F2942")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(h)
            run.font.bold = True
            run.font.size = Pt(8.0)
            run.font.color.rgb = RGBColor(255, 255, 255)

        timeline_data = [
            ("Weeks 1 - 4", "Stage 1: Discovery & Requirements Analysis\nStakeholder interviews, workflow mapping, vendor demo scoring", "Project Charter signed; Multi-vendor evaluation matrix finalized", "Steering Committee"),
            ("Weeks 5 - 8", "Stage 1-2: Architecture Planning & Contracting\nVendor selection, BAA execution, payer EDI credentialing kickoff", "Executed vendor contract; Payer EDI 837/835 applications submitted", "CFO & Legal Counsel"),
            ("Weeks 9 - 14", "Stage 2: Technical Configuration & ETL Migration\nInterface build, ETL cleansing, MPI deduplication, test loads", "Sandbox interface verified; $0.00 AR financial trial balance achieved", "Migration Lead & Coder"),
            ("Weeks 15 - 18", "Stage 3: End-to-End Testing & Scrubber Setup\nPre-bill rule engine deployment, 500 test claim batches, 835 auto-post", "98%+ first-pass clean claim test rate; Zero fatal edit bypasses", "Billing Supervisor"),
            ("Weeks 19 - 20", "Stage 3: Role-Based Staff Training\nDelivery of 5 role curricula (46 hours), practical hands-on exercises", "100% staff pass rate (>= 85%) on competency assessment", "Training Lead & Clinic Mgr"),
            ("Weeks 21 - 24+", "Stage 4: Pilot, Enterprise Cutover & Optimization\nCardiology pilot (Wk 21-22), full cutover weekend (Wk 23), stabilization", "Cutover completed; DAR < 35.0 days and dollar-weighted denial rate <5.0% target ceiling achieved", "Medical Director & SteerCo")
        ]
        for r_idx, (t_range, acts, mls, gates) in enumerate(timeline_data):
            row_cells = [tbl.cell(r_idx + 1, c) for c in range(4)]
            row_data = [t_range, acts, mls, gates]
            bg_color = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
            for c_idx, val in enumerate(row_data):
                cell = row_cells[c_idx]
                cell.width = col_w[c_idx]
                set_cell_margins(cell, 35, 35, 45, 45)
                set_cell_background(cell, bg_color)
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(1)
                run = p.add_run(val)
                run.font.size = Pt(7.5)

    def _section_18_kpi_framework(self) -> None:
        self._add_section_heading("18. KPI and Success Measurement")
        self._add_paragraph(
            "To evaluate operational and financial performance post-integration, an 11-metric Key Performance Indicator (KPI) framework was formulated. All targets represent proposed project objectives reflecting high-performing multi-specialty outpatient standards rather than proven industry benchmarks. In particular, the initial claim denial rate target (KPI-02) is established as a performance ceiling of <5.0% (<5.0% target ceiling) to drive continuous front-end claim scrubbing and root-cause resolution."
        )

        # KPI Table: 6.50" total
        # Cols: ID (0.70"), Metric Name (1.60"), Category (1.00"), Formula (1.50"), Baseline (0.80"), Target (0.90") = 6.50"
        with open(DATA_DIR / "kpi_definitions.json", "r", encoding="utf-8") as f:
            import json
            kpi_data = json.load(f)

        tbl = self.doc.add_table(rows=len(kpi_data) + 1, cols=6)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        col_w = [Inches(0.70), Inches(1.60), Inches(1.00), Inches(1.50), Inches(0.80), Inches(0.90)]

        headers = ["KPI ID", "Metric Name", "Category", "Mathematical Formula", "Baseline", "Project Target"]
        for c_idx, h in enumerate(headers):
            cell = tbl.cell(0, c_idx)
            cell.width = col_w[c_idx]
            set_cell_margins(cell, 40, 40, 50, 50)
            set_cell_background(cell, "0F2942")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(h)
            run.font.bold = True
            run.font.size = Pt(8.0)
            run.font.color.rgb = RGBColor(255, 255, 255)

        for r_idx, k in enumerate(kpi_data):
            row_cells = [tbl.cell(r_idx + 1, c) for c in range(6)]
            base_val = k['baseline_value']
            base_str = f"{base_val}{k['unit']}" if isinstance(base_val, (int, float)) else str(base_val)
            tgt_val = k['target_value']
            if k.get("kpi_id") == "KPI-02":
                tgt_str = "<5.0%"
            elif k.get("target_display"):
                tgt_str = k["target_display"]
            else:
                tgt_str = f"{tgt_val}{k['unit']}" if isinstance(tgt_val, (int, float)) else str(tgt_val)
            row_data = [
                k["kpi_id"],
                k["name"],
                k["category"],
                k["formula"],
                base_str,
                tgt_str
            ]
            bg_color = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
            for c_idx, val in enumerate(row_data):
                cell = row_cells[c_idx]
                cell.width = col_w[c_idx]
                set_cell_margins(cell, 35, 35, 45, 45)
                set_cell_background(cell, bg_color)
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(1)
                run = p.add_run(val)
                run.font.size = Pt(7.0)
                if c_idx == 5:
                    run.font.bold = True
                    run.font.color.rgb = ALERT_GREEN

    def _section_19_challenges_lessons(self) -> None:
        self._add_section_heading("19. Challenges and Lessons Learned")
        self._add_paragraph(
            "Healthcare software integration is among the most demanding IT endeavors due to the convergence of life-critical clinical workflows, intricate coding guidelines, and strict financial accounting rules. Key technical and organizational lessons identified include:"
        )
        self._add_bullet("1. Payer EDI Credentialing Lead Times: ", "Re-enrolling with Medicare, Medicaid, and major commercial payers for X12 837P claim submission and 835 ERA delivery typically requires 45 to 60 business days. Initiating enrollment in Stage 1 and maintaining redundant direct-entry payer portal capabilities are essential to prevent revenue cash-flow freezes.")
        self._add_bullet("2. Legacy Data Schema Heterogeneity: ", "Legacy on-premise systems frequently harbor free-text demographic strings, unformatted dates, and non-standard modifiers. Automated ETL scripts must be paired with human sampling to catch subtle truncation issues before cutover.")
        self._add_bullet("3. Clinician Documentation Inertia: ", "Providers often resist structured EHR templates if they increase charting time. Deploying specialty-specific smart phrases, voice recognition, and real-time coding prompts within the clinical workflow mitigates charting resistance far more effectively than punitive administrative mandates.")
        self._add_bullet("4. Limits of Automated Claim Scrubbing: ", "Software rules engines excel at catching syntactic errors (missing NPIs, unbundled CPT pairs, invalid ICD-10 codes) but cannot interpret clinical context or determine medical necessity. Retaining experienced certified medical coders in the loop is indispensable for coding integrity.")

    def _section_20_conclusion(self) -> None:
        self._add_section_heading("20. Conclusion")
        self._add_paragraph(
            f"This Week 4 master integration proposal demonstrates that successful medical billing software modernization requires an integrated socio-technical strategy. By transitioning {self.profile.name} from fragmented on-premise tools to a unified cloud architecture featuring native clearinghouse connectivity, real-time 270 eligibility, automated claim scrubbing, and role-based training, the practice establishes a sustainable foundation for revenue cycle integrity, maintaining a dollar-weighted initial claim denial rate below the proposed <5.0% target ceiling and Days in A/R under 35 days."
        )
        self._add_paragraph(
            "Across the four-week internship continuum, each case study has systematically addressed a core pillar of the healthcare revenue cycle: auditing compliance and coding ethics (Week 1), modeling procedural billing workflows and financial identities (Week 2), diagnosing errors and formulating preventive controls (Week 3), and engineering enterprise software integration and governance frameworks (Week 4). The resulting technical architecture protects organizational financial health while ensuring strict adherence to healthcare coding, privacy, and regulatory standards."
        )

    def _section_21_references(self) -> None:
        self._add_section_heading("21. References")
        self._add_paragraph("The technical specifications, vendor feature evaluations, and regulatory standards detailed in this report are grounded in the following official publications:")
        refs = [
            ("athenahealth, Inc. (2026). ", "athenaOne Practice Management, Billing Solutions, and Developer Portal Documentation. Official Vendor Information. https://www.athenahealth.com/solutions/medical-billing and https://developer.athenahealth.com (Accessed November 9, 2026)."),
            ("AdvancedMD, Inc. (2026). ", "AdvancedMD Cloud EHR, Practice Management, and AdvancedInsight Reporting Documentation. Official Vendor Information. https://www.advancedmd.com/medical-billing-software and https://www.advancedmd.com/pricing (Accessed November 9, 2026)."),
            ("Tebra, Inc. (2026). ", "Tebra Practice Management, Clinical EHR, and Medical Billing Solutions. Official Vendor Information. https://www.tebra.com/billing-software and https://www.tebra.com/pricing (Accessed November 9, 2026)."),
            ("Centers for Medicare & Medicaid Services (CMS). (2026). ", "Medicare Claims Processing Manual, Publication 100-04, Chapter 24 – EDI and Electronic Claims Processing Standards. U.S. Department of Health and Human Services. https://www.cms.gov/regulations-and-guidance/guidance/manuals/internet-only-manuals-ioms-items/cms018912"),
            ("Centers for Medicare & Medicaid Services (CMS). (2026). ", "National Correct Coding Initiative (NCCI) Policy Manual for Medicare Services. Chapters 1, 9, 11 (General Coding Policies, Modifier -25, and Modifier -59). https://www.cms.gov/medicare/coding-billing/national-correct-coding-initiative-ncci-edits/medicare-ncci-policy-manual"),
            ("American Medical Association (AMA). (2026). ", "CPT Professional Edition and Current Evaluation & Management (E/M) Guidelines. Chicago: AMA Press. Note: CPT rules and code sets must be verified against the encounter date of service and authorized AMA publications; proprietary CPT content is not reproduced herein. https://www.ama-assn.org/practice-management/cpt"),
            ("National Center for Health Statistics (NCHS) & CMS. (2025/2026). ", "ICD-10-CM Official Guidelines for Coding and Reporting (FY 2026 for DOS prior to Oct 1, 2026; FY 2027 for DOS on or after Oct 1, 2026). U.S. Department of Health and Human Services / CDC. https://www.cdc.gov/nchs/icd/icd-10-cm/index.html"),
            ("U.S. Department of Health and Human Services (HHS) Office for Civil Rights (OCR). (2024). ", "Health Insurance Portability and Accountability Act (HIPAA) Security Rule (45 CFR Parts 160 and 164, Subparts A and C). Note: Technical specifications such as AES-256 and TLS 1.3 represent industry-recommended implementation methods for addressable standards, not statutory mandates; HHS OCR does not certify software products or organizations. https://www.hhs.gov/hipaa/for-professionals/security/index.html"),
            ("National Institute of Standards and Technology (NIST). (2024). ", "NIST Special Publication 800-66 Revision 2: Implementing the Health Insurance Portability and Accountability Act (HIPAA) Security Rule: Cybersecurity Resource Guide. https://csrc.nist.gov/pubs/sp/800/66/r2/final"),
            ("Workgroup for Electronic Data Interchange (WEDI) & Accredited Standards Committee X12. (2022). ", "ASC X12 Standards for Electronic Data Interchange: Technical Report Type 3 (TR3) for 005010X279A1 (270/271), 005010X222A1 (837P), and 005010X221A1 (835). https://www.x12.org/"),
            ("American Health Information Management Association (AHIMA) & ACDIS. (2022). ", "Guidelines for Achieving a Compliant Query Practice: 2022 Update. Journal of AHIMA. https://www.ahima.org/"),
            ("Medical Group Management Association (MGMA). (2024). ", "MGMA DataDive Cost and Revenue: Outpatient Multi-Specialty Revenue Cycle Benchmarks (Days in AR, Denial Rates, First-Pass Acceptance). https://www.mgma.com/"),
            ("Healthcare Financial Management Association (HFMA). (2024). ", "MAP Keys: Industry Standard Revenue Cycle Key Performance Indicators and Strategic Benchmarks. https://www.hfma.org/")
        ]
        for author, cite in refs:
            self._add_bullet(author, cite)
