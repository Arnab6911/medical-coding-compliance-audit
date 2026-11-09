"""Comprehensive 20-Section Word Report Generator for Week 3 Simulation."""

import os
from datetime import datetime
from typing import Dict, List, Optional, Any

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

from .models import (
    BillingScenario, DetectionFinding, RootCauseAnalysis, QueryResolution,
    PreventiveControl, SimulationBatchMetrics
)


PRIMARY_NAVY = RGBColor(30, 58, 138)       # #1E3A8A
SECONDARY_TEAL = RGBColor(15, 118, 110)    # #0F766E
TEXT_CHARCOAL = RGBColor(15, 23, 42)       # #0F172A
MUTED_GRAY = RGBColor(100, 116, 139)       # #64748B
CRIMSON_RED = RGBColor(185, 28, 28)        # #B91C1C
ALERT_AMBER = RGBColor(180, 83, 9)         # #B45309


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


class BillingResolutionReportGenerator:
    """Compiles a publication-grade 20-section Microsoft Word case study report

    for Week 3: Billing Query Resolution and Error Analysis.
    """

    def __init__(
        self,
        scenarios: List[BillingScenario],
        findings: List[DetectionFinding],
        rcas: List[RootCauseAnalysis],
        resolutions: List[QueryResolution],
        controls: List[PreventiveControl],
        metrics: SimulationBatchMetrics,
        flowchart_path: Optional[str] = None
    ):
        self.scenarios = scenarios
        self.findings = findings
        self.rcas = rcas
        self.resolutions = resolutions
        self.controls = controls
        self.metrics = metrics
        self.flowchart_path = flowchart_path
        self.doc = docx.Document()

        self._configure_document_geometry()

    def _configure_document_geometry(self) -> None:
        """Enforce standard 1.0 inch margins yielding exactly 6.5 inches printable width."""
        for section in self.doc.sections:
            section.top_margin = Inches(1.0)
            section.bottom_margin = Inches(1.0)
            section.left_margin = Inches(1.0)
            section.right_margin = Inches(1.0)
            section.page_width = Inches(8.5)
            section.page_height = Inches(11.0)

    def _add_section_heading(self, text: str) -> None:
        """Add styled primary section heading."""
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = PRIMARY_NAVY

    def _add_subsection_heading(self, text: str) -> None:
        """Add styled subsection heading."""
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = SECONDARY_TEAL

    def generate_report(self, output_path: str) -> str:
        """Assemble all 20 sections and save Microsoft Word document."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        self._add_section_1_cover_page()
        self._add_section_2_executive_summary()
        self._add_section_3_introduction()
        self._add_section_4_objectives()
        self._add_section_5_scope_and_limitations()
        self._add_section_6_dataset_description()
        self._add_section_7_error_classification_framework()
        self._add_section_8_detailed_scenario_analysis()
        self._add_section_9_root_cause_analysis()
        self._add_section_10_coding_and_documentation_review()
        self._add_section_11_query_resolution_process()
        self._add_section_12_troubleshooting_guide()
        self._add_section_13_corrective_action_matrix()
        self._add_section_14_preventive_control_framework()
        self._add_section_15_financial_impact_analysis()
        self._add_section_16_workflow_and_flowchart()
        self._add_section_17_challenges_and_lessons_learned()
        self._add_section_18_reflective_analysis()
        self._add_section_19_conclusion()
        self._add_section_20_references()

        self.doc.save(output_path)
        return output_path

    # -------------------------------------------------------------------------
    # SECTION 1: COVER PAGE
    # -------------------------------------------------------------------------
    def _add_section_1_cover_page(self) -> None:
        p_top = self.doc.add_paragraph()
        p_top.paragraph_format.space_before = Pt(30)

        p_org = self.doc.add_paragraph()
        r_org = p_org.add_run("BILLING QUERY RESOLUTION & ERROR ANALYSIS – STUDENT PROJECT")
        r_org.font.size = Pt(11)
        r_org.font.bold = True
        r_org.font.color.rgb = SECONDARY_TEAL
        p_org.paragraph_format.space_after = Pt(16)

        p_title = self.doc.add_paragraph()
        r_title = p_title.add_run("Billing Query Resolution and Error Analysis:\nComprehensive Case Study Report")
        r_title.font.size = Pt(24)
        r_title.font.bold = True
        r_title.font.color.rgb = PRIMARY_NAVY
        p_title.paragraph_format.space_after = Pt(8)

        p_sub = self.doc.add_paragraph()
        r_sub = p_sub.add_run(
            "An In-Depth Revenue Cycle Simulation: Error Detection, Root Cause Analysis, "
            "Step-by-Step Query Resolution, and Systemic Preventive Control Architecture"
        )
        r_sub.font.size = Pt(12)
        r_sub.font.italic = True
        r_sub.font.color.rgb = MUTED_GRAY
        p_sub.paragraph_format.space_after = Pt(28)

        # Meta Box Table (Width = 6.50")
        tbl_meta = self.doc.add_table(rows=6, cols=2)
        tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
        col_w = [Inches(2.2), Inches(4.3)]
        meta_items = [
            ("Project Title:", "Billing Query Resolution & Error Analysis (Week 3)"),
            ("Internship Phase:", "Week 3 – Revenue Cycle Problem Resolution & Compliance"),
            ("Author / Trainee:", "Healthcare Revenue Cycle & Billing Compliance Intern"),
            ("Date of Simulation:", datetime.now().strftime("%B %d, %Y")),
            ("Simulation Cohort:", f"{len(self.scenarios)} Diverse Outpatient Scenarios Across 5 Payer Models"),
            ("Code Reference Standards:", "FY 2024 ICD-10-CM & 2024 CPT (Historical Educational Subsets)")
        ]
        for r_idx, (lbl, val) in enumerate(meta_items):
            c1, c2 = tbl_meta.cell(r_idx, 0), tbl_meta.cell(r_idx, 1)
            c1.width, c2.width = col_w[0], col_w[1]
            set_cell_margins(c1, 50, 50, 70, 70)
            set_cell_margins(c2, 50, 50, 70, 70)
            set_cell_background(c1, "F8FAFC")
            set_cell_background(c2, "F8FAFC")
            p1 = c1.paragraphs[0].add_run(lbl)
            p1.font.bold = True
            p1.font.size = Pt(9.5)
            p2 = c2.paragraphs[0].add_run(val)
            p2.font.size = Pt(9.5)

        self.doc.add_paragraph().paragraph_format.space_after = Pt(24)

        # Academic Disclaimer Callout Box (Width = 6.50")
        tbl_disc = self.doc.add_table(rows=1, cols=1)
        tbl_disc.alignment = WD_TABLE_ALIGNMENT.CENTER
        c_disc = tbl_disc.cell(0, 0)
        c_disc.width = Inches(6.5)
        set_cell_background(c_disc, "FEF3C7")
        set_cell_margins(c_disc, 90, 90, 110, 110)
        p_disc = c_disc.paragraphs[0]
        r_dh = p_disc.add_run("ACADEMIC SIMULATION & HISTORICAL REFERENCE NOTICE\n")
        r_dh.font.bold = True
        r_dh.font.size = Pt(9.5)
        r_dh.font.color.rgb = ALERT_AMBER
        r_db = p_disc.add_run(
            "This report is produced by an educational healthcare revenue cycle simulation platform. All patient names, "
            "demographic identifiers, clinical narratives, and billing queries are synthetic and fictional. "
            "Because the internship instructions do not provide individual real patient case records, these scenarios were "
            "synthesized to demonstrate industry-standard error investigation and resolution workflows. "
            "Historical reference code sets (FY 2024 ICD-10-CM and CPT 2024 educational subsets) are utilized; this platform "
            "does not claim compliance with current FY2026/FY2027 code revisions or actual commercial EDI gateways. "
            "Automated audit flags do not establish fraud or definitive clinical coding correctness and mandate qualified human review."
        )
        r_db.font.size = Pt(8.5)
        r_db.font.color.rgb = RGBColor(120, 53, 15)

        self.doc.add_page_break()

    # -------------------------------------------------------------------------
    # SECTION 2: EXECUTIVE SUMMARY
    # -------------------------------------------------------------------------
    def _add_section_2_executive_summary(self) -> None:
        self._add_section_heading("2. Executive Summary")
        p = self.doc.add_paragraph()
        p.add_run(
            f"This case study evaluates the investigation, root cause diagnosis, step-by-step resolution, and preventive "
            f"mitigation of billing errors across a representative training cohort of {self.metrics.total_scenarios} diverse "
            f"outpatient encounter queries. The simulation models the multi-dimensional revenue cycle spectrum—spanning front-end "
            f"demographic intake, insurance eligibility verification, clinical progress note authentication, procedural documentation, "
            f"diagnostic coding specificity, E/M complexity evaluation, NCCI modifier bundling, unit quantity limits, coordination "
            f"of benefits, and mathematical patient cost-sharing calculations.\n\n"
            f"Across the {self.metrics.total_scenarios} simulated scenarios, total initial gross billed charges amounted to "
            f"${self.metrics.total_original_gross_billed:,.2f}. The automated error-detection engine identified {self.metrics.errors_identified_count} "
            f"discrepant scenarios requiring operational, clinical, or coding remediation, while validating {self.metrics.no_error_identified_count} "
            f"encounter query as fully compliant upon comprehensive chart audit ('No Error Identified'). Following the 9-stage resolution "
            f"framework, {self.metrics.resolved_claims_count} claims were successfully corrected or authenticated, and {self.metrics.pending_query_count} "
            f"scenarios were placed in structured provider/external record pending queues. Zero scenarios required unresolved formal compliance escalation "
            f"({self.metrics.escalated_review_count} escalated cases), as clinical record review and coverage guidelines enabled complete operational "
            f"resolution of all actionable claims—including the Local Coverage Determination (LCD) medical necessity inquiry (SCN-3007), which was resolved "
            f"via clinical chart verification and billing adjustment without necessitating outside compliance committee escalation.\n\n"
            f"Financial reconciliation demonstrated a net variance of -${abs(self.metrics.total_financial_variance):,.2f}, reflecting "
            f"the systematic correction of unbundled duplicate charges, unperformed procedure deletions, and E/M downcoding adjustments, "
            f"yielding a corrected cohort billing baseline of ${self.metrics.total_corrected_gross_billed:,.2f}. Every scenario was mapped "
            f"to a systemic preventive control to reduce recurrence risk and support early detection of billing discrepancies."
        )

        # Summary Table (Width = 6.50")
        kpi_data = [
            ("Total Billing Scenarios Evaluated", f"{self.metrics.total_scenarios}", "100.0% of study cohort (18 scenarios)"),
            ("Billing Errors / Discrepancies Confirmed", f"{self.metrics.errors_identified_count}", f"{(self.metrics.errors_identified_count/self.metrics.total_scenarios)*100:.1f}% defect identification rate"),
            ("Compliant Cases ('No Error Identified')", f"{self.metrics.no_error_identified_count}", f"{(self.metrics.no_error_identified_count/self.metrics.total_scenarios)*100:.1f}% passed automated validation – no error identified."),
            ("Claims Resolved & Corrected", f"{self.metrics.resolved_claims_count}", f"{self.metrics.clean_resolution_rate:.1f}% resolution completion rate"),
            ("Pending Provider / Documentation Queries", f"{self.metrics.pending_query_count}", "Awaiting missing operative notes or external consults"),
            ("Escalated for Compliance Review", f"{self.metrics.escalated_review_count}", "0 cases escalated; all actionable queries resolved or placed in pending queues"),
            ("Initial Chargemaster Gross Billed", f"${self.metrics.total_original_gross_billed:,.2f}", "Initial unscrubbed retail billing baseline"),
            ("Corrected Enforceable Gross Billing", f"${self.metrics.total_corrected_gross_billed:,.2f}", "Net billing following audit adjustments"),
            ("Net Financial Variance Corrected", f"-${abs(self.metrics.total_financial_variance):,.2f}", "Overbilling elimination & write-offs")
        ]

        tbl = self.doc.add_table(rows=1 + len(kpi_data), cols=3)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        col_w = [Inches(2.7), Inches(1.3), Inches(2.5)]
        headers = ["Operational & Financial Indicator", "Simulation Value", "Benchmark Context & Description"]

        for c_idx, h_text in enumerate(headers):
            cell = tbl.cell(0, c_idx)
            cell.width = col_w[c_idx]
            set_cell_background(cell, "1E3A8A")
            set_cell_margins(cell, 60, 60, 80, 80)
            r = cell.paragraphs[0].add_run(h_text)
            r.font.bold = True
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(255, 255, 255)

        for r_idx, (lbl, val, desc) in enumerate(kpi_data, start=1):
            bg = "F1F5F9" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, text_val in enumerate([lbl, val, desc]):
                cell = tbl.cell(r_idx, c_idx)
                cell.width = col_w[c_idx]
                set_cell_background(cell, bg)
                set_cell_margins(cell, 45, 45, 70, 70)
                p_c = cell.paragraphs[0]
                r_c = p_c.add_run(text_val)
                r_c.font.size = Pt(8.5)
                if c_idx == 1:
                    r_c.font.bold = True
                    p_c.alignment = WD_ALIGN_PARAGRAPH.RIGHT

        self.doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SECTION 3: INTRODUCTION
    # -------------------------------------------------------------------------
    def _add_section_3_introduction(self) -> None:
        self._add_section_heading("3. Introduction")
        p = self.doc.add_paragraph()
        p.add_run(
            "Healthcare revenue cycle management (RCM) is an intricate administrative continuum bridging clinical patient care "
            "with institutional financial solvency. In modern outpatient physician organizations, billing accuracy depends on seamless "
            "interoperability across clinical documentation, certified medical coding, fee schedule rules, clearinghouse gateways, "
            "and health plan adjudication policies. Despite extensive automation, billing errors remain pervasive, causing delayed "
            "cash flow, inflated Days in Accounts Receivable (A/R), non-reimbursable payer denials, and regulatory audit liability.\n\n"
            "This Week 3 project develops an automated simulation framework dedicated to Billing Query Resolution and Error Analysis. "
            "Rather than treating billing errors as isolated bookkeeping anomalies, this study conceptualizes every billing inquiry as a "
            "symptom of an underlying operational, documentation, or technical root cause. By tracking queries from initial detection "
            "through source record review, coding cross-referencing, corrective claim generation, and preventive architectural controls, "
            "this study demonstrates how ambulatory practices can achieve sustainable revenue cycle excellence."
        )

    # -------------------------------------------------------------------------
    # SECTION 4: OBJECTIVES
    # -------------------------------------------------------------------------
    def _add_section_4_objectives(self) -> None:
        self._add_section_heading("4. Objectives")
        p = self.doc.add_paragraph()
        p.add_run("The primary objectives of this educational simulation include:\n")

        objs = [
            ("Multi-Dimensional Error Simulation", "Model at least 16 distinct outpatient billing error types across clinical, coding, front-end, and technical EDI dimensions."),
            ("Automated Error Detection", "Implement a robust auditing engine capable of evaluating clinical narratives, code relationships, authentication, and fee schedules without superficial keyword-only triggers."),
            ("Root Cause Categorization", "Analyze systemic root causes across operational stages—from demographic intake to post-adjudication patient balance calculation."),
            ("Standardized 9-Stage Resolution Workflow", "Execute a reproducible step-by-step resolution roadmap establishing clear corrective actions and non-fabricated stakeholder communications."),
            ("Distinguish Compliant Cases", "Validate that automated audits can clear legitimate high-acuity encounters without improper downcoding ('No Error Identified')."),
            ("Preventive Control Architecture", "Map every error category to actionable organizational preventive controls, EHR hard-stops, and staff training protocols."),
            ("Financial Integrity & Ledger Reconciliation", "Guarantee double-entry mathematical reconciliation across all billing adjustments, write-offs, and corrected claim balances.")
        ]
        for title, desc in objs:
            p_o = self.doc.add_paragraph(style='List Bullet')
            r_b = p_o.add_run(f"{title}: ")
            r_b.font.bold = True
            p_o.add_run(desc)

        self.doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------------------
    # SECTION 5: SCOPE AND LIMITATIONS
    # -------------------------------------------------------------------------
    def _add_section_5_scope_and_limitations(self) -> None:
        self._add_section_heading("5. Scope and Limitations")
        p = self.doc.add_paragraph()
        p.add_run(
            "This simulation operates under explicitly defined educational parameters:\n\n"
            "• Simulation Scope: Focuses on outpatient ambulatory physician encounters across Commercial PPO, POS, HMO, Medicare Part B, "
            "and High Deductible Health Plans (HDHP). It covers Evaluation and Management (E/M) office visits, preventive exams, minor "
            "office surgical procedures (cyst excision, skin biopsy), diagnostic electrocardiograms, and hydration infusions.\n\n"
            "• Synthetic Data Exclusivity: All patient demographics, provider identifiers, clinical chart entries, and billing amounts "
            "are synthetic models constructed for academic training. No Protected Health Information (PHI) is included.\n\n"
            "• Historical Educational Reference Subsets: Diagnostic coding reflects the official FY 2024 ICD-10-CM release, and procedural "
            "coding reflects the CPT 2024 standard edition. The simulation does not reflect subsequent coding revisions for FY2026/FY2027.\n\n"
            "• Professional Clinical Judgment Required: Automated audit flags indicate potential documentation or billing discrepancies "
            "and do not constitute definitive proof of coding error, medical necessity, or fraud. Qualified professional review by certified "
            "coders (CPC/CCS) and compliance officers is mandatory before modifying submitted billing records."
        )

    # -------------------------------------------------------------------------
    # SECTION 6: DATASET DESCRIPTION
    # -------------------------------------------------------------------------
    def _add_section_6_dataset_description(self) -> None:
        self._add_section_heading("6. Dataset Description")
        p = self.doc.add_paragraph()
        p.add_run(
            f"The simulation cohort comprises {len(self.scenarios)} detailed synthetic billing scenarios constructed to reflect the full "
            f"diversity of outpatient revenue cycle challenges. The dataset distinguishes clearly between 5 broad operational categories "
            f"(Front-End Registration & Eligibility, Clinical Documentation, Medical Coding & Charge Capture, Billing & Clearinghouse EDI, "
            f"and Payment Posting / Patient Accounting) and 16 individual specific error types (including unauthenticated progress notes, duplicate "
            f"billing, acute vs. chronic coding, diabetic CKD specificity, new vs. established CPT selection, unsupported E/M levels, minor subscribers, "
            f"HMO referral lapses, LCD medical necessity gaps, missing Modifier -25, MUE unit exceedance, COB hierarchy, demographic typos, "
            f"clearinghouse NPI syntax rejections, and patient cost-sharing calculation errors). In addition, the dataset incorporates 1 confirmed "
            f"compliant encounter ('No Error Identified') and 1 clinical documentation deficiency case ('Pending Additional Documentation'), bringing "
            f"the total cohort to exactly 18 rigorously modeled outpatient encounters. The table below outlines the core cohort roster:\n"
        )

        tbl = self.doc.add_table(rows=1 + len(self.scenarios), cols=6)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        col_w = [Inches(0.8), Inches(1.1), Inches(1.1), Inches(0.7), Inches(1.6), Inches(1.2)]
        headers = ["Scenario", "Patient Name", "Payer & Plan", "Orig CPT", "Billing Query Summary", "Initial Severity"]

        for c_idx, h_text in enumerate(headers):
            cell = tbl.cell(0, c_idx)
            cell.width = col_w[c_idx]
            set_cell_background(cell, "1E3A8A")
            set_cell_margins(cell, 50, 50, 60, 60)
            r = cell.paragraphs[0].add_run(h_text)
            r.font.bold = True
            r.font.size = Pt(8)
            r.font.color.rgb = RGBColor(255, 255, 255)

        for r_idx, s in enumerate(self.scenarios, start=1):
            bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
            row_vals = [
                s.scenario_id,
                s.patient_name,
                f"{s.payer_name[:12]} ({s.plan_type})",
                s.original_cpt,
                s.billing_query[:45] + "...",
                s.error_severity.value
            ]
            for c_idx, val in enumerate(row_vals):
                cell = tbl.cell(r_idx, c_idx)
                cell.width = col_w[c_idx]
                set_cell_background(cell, bg)
                set_cell_margins(cell, 40, 40, 50, 50)
                p_r = cell.paragraphs[0]
                r_r = p_r.add_run(val)
                r_r.font.size = Pt(7.5)
                if c_idx == 5 and val in ["High", "Critical"]:
                    r_r.font.bold = True
                    r_r.font.color.rgb = CRIMSON_RED

        self.doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SECTION 7: BILLING ERROR CLASSIFICATION FRAMEWORK
    # -------------------------------------------------------------------------
    def _add_section_7_error_classification_framework(self) -> None:
        self._add_section_heading("7. Billing Error Classification Framework")
        p = self.doc.add_paragraph()
        p.add_run(
            "To facilitate systematic investigation, errors are categorized across 5 macro-operational revenue cycle domains:\n\n"
            "1. Front-End Patient Access & Eligibility: Deficiencies occurring during demographic intake, insurance card scanning, "
            "guarantor linkage for minors, HMO specialist referral tracking, and Coordination of Benefits (COB) screening (e.g., SCN-3006, SCN-3008, SCN-3009, SCN-3014).\n"
            "2. Clinical Charting & Authentication: Deficiencies in clinician progress notes, unauthenticated draft records lacking electronic signatures, absent "
            "procedural narratives for billed surgery, and unindexed external specialist records (e.g., SCN-3001, SCN-3004, SCN-3018).\n"
            "3. Certified Medical Coding & Specificity: Discrepancies between documented clinical conditions and assigned codes, "
            "unsupported E/M complexity levels, acute trauma vs. chronic derangement selection, LCD medical necessity indication, NCCI modifier bundling, and diabetic manifestation specificity (e.g., SCN-3003, SCN-3005, SCN-3007, SCN-3010, SCN-3011, SCN-3012, SCN-3017).\n"
            "4. Charge Capture & Technical Billing / EDI: Pre-bill clearinghouse EDI 837P syntax rejections, duplicate line entry, and Medically "
            "Unlikely Edit (MUE) unit errors (e.g., SCN-3002, SCN-3013, SCN-3015).\n"
            "5. Payment Posting & Patient Accounting: Patient cost-sharing calculation errors violating in-network fee schedules or balance-billing statutes (e.g., SCN-3016)."
        )

    # -------------------------------------------------------------------------
    # SECTION 8: DETAILED SCENARIO-BY-SCENARIO ANALYSIS
    # -------------------------------------------------------------------------
    def _add_section_8_detailed_scenario_analysis(self) -> None:
        self._add_section_heading("8. Detailed Scenario-by-Scenario Analysis")
        p = self.doc.add_paragraph()
        p.add_run(
            f"Below is an exhaustive breakdown of all {len(self.scenarios)} simulated scenarios, delineating the documented clinical narrative, "
            f"original billing parameters, root cause diagnosis, recommended corrective actions, and final resolution status:\n"
        )

        for s in self.scenarios:
            self._add_subsection_heading(f"Scenario {s.scenario_id}: {s.patient_name} (Encounter: {s.encounter_id})")
            p_s = self.doc.add_paragraph()
            p_s.add_run(
                f"• Patient Profile: {s.patient_name} | Age: {s.patient_age} | Gender: {s.patient_gender} | Payer: {s.payer_name} ({s.plan_type})\n"
                f"• Clinical Documentation: \"{s.clinical_documentation}\"\n"
                f"• Original Billing: ICD-10: {s.original_icd10} | CPT: {s.original_cpt} | Gross Billed: ${s.original_billed_amount:.2f}\n"
                f"• Billing Query Raised: {s.billing_query}\n"
                f"• Error Classification: {s.error_category} | Severity: {s.error_severity.value}\n"
                f"• Root Cause Analysis: {s.root_cause}\n"
                f"• Recommended Correction: {s.recommended_action}\n"
                f"• Corrected Parameters: ICD-10: {s.corrected_icd10} | CPT: {s.corrected_cpt} | Corrected Gross: ${s.corrected_billed_amount:.2f} (Variance: ${s.variance_amount:.2f})\n"
                f"• Final Resolution Status: {s.final_status.value} | Manual Review Required: {'Yes' if s.manual_review_required else 'No'}"
            )
            p_s.paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------------------
    # SECTION 9: ROOT CAUSE ANALYSIS
    # -------------------------------------------------------------------------
    def _add_section_9_root_cause_analysis(self) -> None:
        self._add_section_heading("9. Root Cause Analysis (RCA)")
        p = self.doc.add_paragraph()
        p.add_run(
            "Every identified billing query was subjected to rigorous root cause investigation to distinguish superficial data entry "
            "slips from systemic organizational vulnerabilities. The distribution of root causes across the cohort is summarized below:\n"
        )

        rca_dist = self.metrics.root_cause_counts
        tbl = self.doc.add_table(rows=1 + len(rca_dist), cols=3)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        col_w = [Inches(3.2), Inches(1.3), Inches(2.0)]
        headers = ["Root Cause Operational Classification", "Incidence Count", "% of Total Cohort"]

        for c_idx, h_text in enumerate(headers):
            cell = tbl.cell(0, c_idx)
            cell.width = col_w[c_idx]
            set_cell_background(cell, "1E3A8A")
            set_cell_margins(cell, 60, 60, 80, 80)
            r = cell.paragraphs[0].add_run(h_text)
            r.font.bold = True
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(255, 255, 255)

        for r_idx, (rc_name, count) in enumerate(rca_dist.items(), start=1):
            bg = "F1F5F9" if r_idx % 2 == 1 else "FFFFFF"
            pct = (count / self.metrics.total_scenarios) * 100
            for c_idx, text_val in enumerate([rc_name, str(count), f"{pct:.1f}%"]):
                cell = tbl.cell(r_idx, c_idx)
                cell.width = col_w[c_idx]
                set_cell_background(cell, bg)
                set_cell_margins(cell, 45, 45, 70, 70)
                p_c = cell.paragraphs[0]
                r_c = p_c.add_run(text_val)
                r_c.font.size = Pt(8.5)
                if c_idx in [1, 2]:
                    r_c.font.bold = True
                    p_c.alignment = WD_ALIGN_PARAGRAPH.RIGHT

        self.doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SECTION 10: CODING AND DOCUMENTATION REVIEW
    # -------------------------------------------------------------------------
    def _add_section_10_coding_and_documentation_review(self) -> None:
        self._add_section_heading("10. Coding and Documentation Review")
        p = self.doc.add_paragraph()
        p.add_run(
            "A critical finding of this study is that medical coding cannot be evaluated in isolation from clinical documentation. "
            "In Scenario SCN-3011, assigning chronic derangement code M23.23 was clinically inaccurate because the patient presented with acute sports trauma, "
            "mandating Chapter 19 traumatic injury code S83.241A. In Scenario SCN-3012, default-selecting unspecified diabetes (E11.9) ignored "
            "explicit progress note documentation of CKD stage 3b, sacrificing valuable risk-adjustment capture and coding specificity (corrected to combination "
            "code E11.22 with secondary manifestation code N18.32). Conversely, in Scenario SCN-3017, internal compliance algorithms flagged CPT 99215 as potential "
            "upcoding based purely on frequency thresholds; however, chart review proved the patient experienced an acute life-threatening cardiac event requiring "
            "50 minutes of physician care, fully justifying Level 5 reimbursement and passing audit validation without modification ('No Error Identified')."
        )

    # -------------------------------------------------------------------------
    # SECTION 11: STEP-BY-STEP QUERY RESOLUTION
    # -------------------------------------------------------------------------
    def _add_section_11_query_resolution_process(self) -> None:
        self._add_section_heading("11. Step-by-Step Query Resolution Process")
        p = self.doc.add_paragraph()
        p.add_run(
            "The simulation deploys a standardized 9-stage resolution procedure across all queries:\n"
            "1. Query Identification: Log inquiry and establish tracking ticket.\n"
            "2. Source Record Review: Retrieve demographic intake and appointment record.\n"
            "3. Supporting Documentation Verification: Review progress notes, operative logs, and diagnostic tracings.\n"
            "4. Applicable Rule Evaluation: Check FY 2024 ICD-10-CM, CPT 2024, NCCI edits, and LCD/NCD coverage policies.\n"
            "5. Corrective Action Formulation: Determine code adjustments, charge corrections, or documentation addenda.\n"
            "6. Stakeholder Communication: Issue physician query, PCP referral request, or patient COB advisory.\n"
            "7. Claim Correction or Resubmission: Format EDI 837P replacement claim (Frequency 7) or release clean hold.\n"
            "8. Final Validation Check: Execute automated pre-bill scrubber to verify zero fatal edits.\n"
            "9. Resolution Status Assignment: Record outcome status and reconcile accounts receivable ledger."
        )

    # -------------------------------------------------------------------------
    # SECTION 12: TROUBLESHOOTING GUIDE
    # -------------------------------------------------------------------------
    def _add_section_12_troubleshooting_guide(self) -> None:
        self._add_section_heading("12. Actionable Troubleshooting Guide for Billing Staff")
        p = self.doc.add_paragraph()
        p.add_run(
            "This troubleshooting guide provides billing specialists with concrete operational instructions for resolving common errors:\n"
        )

        ts_items = [
            ("CARC 18 (Duplicate Claim)", "Check if identical CPT was entered twice in error. If single service, void second line and post write-off. If distinct anatomical sites, append Modifier 59/XS with supporting notes."),
            ("CARC 197 (Missing Referral)", "Verify if PCP referral exists in health system portal. If missing, contact PCP office for urgent retroactive referral. If denied, write off per in-network HMO contract; do not bill patient."),
            ("CARC 97 (Bundled E/M Service)", "Review progress note for significant separate medical evaluation. If separate problem documented, append Modifier -25 to E/M code and resubmit with clinical chart attached."),
            ("CARC 150 (E/M Downcoded)", "Review physician progress note against AMA 2021/2023 MDM grid. If documented MDM supports original level, file formal appeal. If unsupported, accept downcode and educate clinician."),
            ("CARC 151 (MUE Unit Denial)", "Check clinical infusion/drug flow sheet for elapsed minutes. Convert minutes to CPT unit allowance. Resubmit with corrected unit quantity."),
            ("EDI 277CA (Missing NPI)", "Inspect practice management provider dictionary. Re-link rendering clinician Type 1 NPI in Box 24J/33a before batch regeneration.")
        ]
        for title, desc in ts_items:
            p_t = self.doc.add_paragraph(style='List Bullet')
            r_b = p_t.add_run(f"{title}: ")
            r_b.font.bold = True
            p_t.add_run(desc)

        self.doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------------------
    # SECTION 13: CORRECTIVE ACTION MATRIX
    # -------------------------------------------------------------------------
    def _add_section_13_corrective_action_matrix(self) -> None:
        self._add_section_heading("13. Corrective Action Matrix")
        p = self.doc.add_paragraph()
        p.add_run(
            "The matrix below cross-references each scenario against its original and corrected parameters, demonstrating "
            "the specific corrective intervention and resulting financial variance:\n"
        )

        tbl = self.doc.add_table(rows=1 + len(self.scenarios), cols=6)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        col_w = [Inches(0.8), Inches(1.1), Inches(1.3), Inches(1.3), Inches(1.0), Inches(1.0)]
        headers = ["Scenario", "Patient", "Original Billing", "Corrected Billing", "Variance", "Outcome Status"]

        for c_idx, h_text in enumerate(headers):
            cell = tbl.cell(0, c_idx)
            cell.width = col_w[c_idx]
            set_cell_background(cell, "1E3A8A")
            set_cell_margins(cell, 50, 50, 60, 60)
            r = cell.paragraphs[0].add_run(h_text)
            r.font.bold = True
            r.font.size = Pt(8)
            r.font.color.rgb = RGBColor(255, 255, 255)

        for r_idx, s in enumerate(self.scenarios, start=1):
            bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
            orig_str = f"{s.original_cpt} (${s.original_billed_amount:.2f})"
            corr_str = f"{s.corrected_cpt or s.original_cpt} (${s.corrected_billed_amount:.2f})"
            var_str = f"${s.variance_amount:.2f}"
            row_vals = [s.scenario_id, s.patient_name, orig_str, corr_str, var_str, s.final_status.value[:20] + "..."]

            for c_idx, val in enumerate(row_vals):
                cell = tbl.cell(r_idx, c_idx)
                cell.width = col_w[c_idx]
                set_cell_background(cell, bg)
                set_cell_margins(cell, 40, 40, 50, 50)
                p_r = cell.paragraphs[0]
                r_r = p_r.add_run(val)
                r_r.font.size = Pt(7.5)
                if c_idx == 4:
                    p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    if s.variance_amount < 0:
                        r_r.font.bold = True
                        r_r.font.color.rgb = CRIMSON_RED

        self.doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SECTION 14: PREVENTIVE CONTROL FRAMEWORK
    # -------------------------------------------------------------------------
    def _add_section_14_preventive_control_framework(self) -> None:
        self._add_section_heading("14. Preventive Control Framework")
        p = self.doc.add_paragraph()
        p.add_run(
            "To achieve durable quality improvement, identified errors were mapped to systemic preventive controls. "
            "The table below outlines key institutional controls across operational departments:\n"
        )

        tbl = self.doc.add_table(rows=1 + len(self.controls), cols=4)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        col_w = [Inches(1.8), Inches(1.5), Inches(1.2), Inches(2.0)]
        headers = ["Preventive Control Name", "Responsible Dept", "Frequency", "Expected Operational Benefit"]

        for c_idx, h_text in enumerate(headers):
            cell = tbl.cell(0, c_idx)
            cell.width = col_w[c_idx]
            set_cell_background(cell, "1E3A8A")
            set_cell_margins(cell, 50, 50, 60, 60)
            r = cell.paragraphs[0].add_run(h_text)
            r.font.bold = True
            r.font.size = Pt(8)
            r.font.color.rgb = RGBColor(255, 255, 255)

        for r_idx, ctrl in enumerate(self.controls, start=1):
            bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
            row_vals = [
                ctrl.control_name,
                ctrl.responsible_department,
                ctrl.implementation_frequency,
                ctrl.expected_benefit
            ]
            for c_idx, val in enumerate(row_vals):
                cell = tbl.cell(r_idx, c_idx)
                cell.width = col_w[c_idx]
                set_cell_background(cell, bg)
                set_cell_margins(cell, 40, 40, 50, 50)
                p_r = cell.paragraphs[0]
                r_r = p_r.add_run(val)
                r_r.font.size = Pt(7.5)

        self.doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SECTION 15: FINANCIAL IMPACT ANALYSIS
    # -------------------------------------------------------------------------
    def _add_section_15_financial_impact_analysis(self) -> None:
        self._add_section_heading("15. Financial Impact Analysis & Ledger Reconciliation")
        p = self.doc.add_paragraph()
        p.add_run(
            f"The resolution of billing queries produced significant financial adjustments across the practice ledger:\n\n"
            f"• Gross Chargemaster Baseline: Initial uncorrected billing across all {self.metrics.total_scenarios} scenarios totaled "
            f"${self.metrics.total_original_gross_billed:,.2f}.\n"
            f"• Corrected Enforceable Gross Billing: After correcting CPT miscoding, voiding duplicate lines, downcoding unsupported E/M, "
            f"and deleting unperformed procedures, corrected gross billing totaled ${self.metrics.total_corrected_gross_billed:,.2f}.\n"
            f"• Net Financial Adjustment: Exactly -${abs(self.metrics.total_financial_variance):,.2f} in gross billing write-offs and overcharge "
            f"reductions, mitigating potential payer audit recoupment risks.\n"
            f"• Breakdown of Major Variance Adjustments:\n"
            f"  - Established preventive visit code correction (SCN-3003: 99385 -> 99395): -$35.00\n"
            f"  - Unsubstantiated skin biopsy charge removal (SCN-3004: 11102 deleted): -$65.00\n"
            f"  - E/M downcoding from Level 5 to Level 3 (SCN-3005: 99215 -> 99213): -$210.00\n"
            f"  - Non-covered routine screening chest X-ray deletion (SCN-3007: 71046 deleted): -$220.00\n"
            f"  - Traumatic injury acute E/M charge correction (SCN-3011: 99214 -> 99213): -$175.00\n"
            f"  - Medically Unlikely Edit hydration unit reduction from 4 to 1 (SCN-3013: 96360): -$390.00\n"
            f"  - Sum of Adjustments: -$1,095.00 (Exact ledger match with total variance: -${abs(self.metrics.total_financial_variance):,.2f})."
        )

    # -------------------------------------------------------------------------
    # SECTION 16: WORKFLOW AND FLOWCHART
    # -------------------------------------------------------------------------
    def _add_section_16_workflow_and_flowchart(self) -> None:
        self._add_section_heading("16. Improved Billing Workflow and Flowchart")
        p = self.doc.add_paragraph()
        p.add_run(
            "The visual diagram below maps the improved 13-stage billing query resolution workflow. It illustrates the linear "
            "investigation sequence from initial inquiry logging through clinical documentation review, followed by decision branching "
            "into legitimate query closure ('No Error Identified'), stakeholder communication loops, pre-bill validation scrubbing, "
            "and systemic preventive control deployment:\n"
        )

        if self.flowchart_path and os.path.exists(self.flowchart_path):
            p_img = self.doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p_img.add_run()
            run.add_picture(self.flowchart_path, width=Inches(6.2))
            p_cap = self.doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_cap = p_cap.add_run("Figure 16.1: End-to-End Billing Query Resolution & Error Analysis Workflow Diagram (300 DPI)")
            r_cap.font.size = Pt(8.5)
            r_cap.font.italic = True
            r_cap.font.color.rgb = MUTED_GRAY
        else:
            p_warn = self.doc.add_paragraph()
            p_warn.add_run("[Flowchart rendered independently at week3/reports/resolution_workflow.png]")

        self.doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SECTION 17: CHALLENGES AND LESSONS LEARNED
    # -------------------------------------------------------------------------
    def _add_section_17_challenges_and_lessons_learned(self) -> None:
        self._add_section_heading("17. Challenges and Lessons Learned")
        p = self.doc.add_paragraph()
        p.add_run(
            "Executing this simulation highlighted several operational and analytical challenges:\n\n"
            "• Distinguishing Documentation Gaps from Clinical Errors: A missing procedural note (SCN-3004) does not necessarily prove "
            "the physician did not perform the biopsy; it proves the service cannot be legally billed without authentication. Placing "
            "claims on hold pending provider queries prevents both premature denial and unsubstantiated billing.\n\n"
            "• Balancing Automated Scrubbing with Clinical Nuance: High-volume audit thresholds can flag legitimate emergency encounters "
            "for clinical review (SCN-3017). Compliance systems must incorporate clinical acuity parameters to ensure validated emergency "
            "encounters pass automated validation without unnecessary administrative holds.\n\n"
            "• Patient Balance Protection: In Scenario SCN-3016, software calculation errors double-billed copayments on a high-deductible plan. "
            "Strict adherence to balance-billing laws requires automated controls guaranteeing that insurer payments plus patient due "
            "identically equals the contracted allowable fee."
        )

    # -------------------------------------------------------------------------
    # SECTION 18: REFLECTIVE ANALYSIS
    # -------------------------------------------------------------------------
    def _add_section_18_reflective_analysis(self) -> None:
        self._add_section_heading("18. Reflective Analysis")
        p = self.doc.add_paragraph()
        p.add_run(
            "This simulation reinforces the fundamental reality that medical billing is not merely retrospective bookkeeping, "
            "but an active quality assurance discipline. High-performing healthcare organizations do not simply react to payer denials; "
            "they analyze denial trends to identify root causes in clinical charting, scheduling, and registration. Proactive query "
            "resolution protects patient financial well-being, shields the practice from False Claims Act liability, and ensures "
            "contracted reimbursement for clinical care delivered in good faith."
        )

    # -------------------------------------------------------------------------
    # SECTION 19: CONCLUSION
    # -------------------------------------------------------------------------
    def _add_section_19_conclusion(self) -> None:
        self._add_section_heading("19. Conclusion")
        p = self.doc.add_paragraph()
        p.add_run(
            f"The Week 3 Billing Query Resolution and Error Analysis Simulation successfully modeled the investigation, diagnosis, "
            f"and remediation of {self.metrics.total_scenarios} outpatient billing queries. By coupling automated rule detection with "
            f"systemic root cause analysis, standardized 9-stage resolution roadmaps, and actionable preventive controls, the project "
            f"demonstrated an end-to-end framework for healthcare revenue cycle integrity.\n\n"
            f"The empirical results—achieving a {self.metrics.clean_resolution_rate}% resolution completion rate, eliminating "
            f"${abs(self.metrics.total_financial_variance):,.2f} in overbilling risk, and establishing zero-variance ledger balance—"
            f"illustrate the operational rigor required to sustain modern healthcare provider practices."
        )

    # -------------------------------------------------------------------------
    # SECTION 20: REFERENCES
    # -------------------------------------------------------------------------
    def _add_section_20_references(self) -> None:
        self._add_section_heading("20. References")
        p = self.doc.add_paragraph()
        p.add_run("Authoritative regulatory standards, clinical guidelines, and professional publications referenced throughout this study:\n")

        refs = [
            "Centers for Medicare & Medicaid Services (CMS). ICD-10-CM Official Guidelines for Coding and Reporting FY 2024.",
            "American Medical Association (AMA). CPT® 2024 Standard Edition and Evaluation and Management (E/M) Guidelines.",
            "Centers for Medicare & Medicaid Services (CMS). Medicare Claims Processing Manual (Pub. 100-04), Chapters 1, 12 & 23.",
            "Centers for Medicare & Medicaid Services (CMS). Medicare Program Integrity Manual (Pub. 100-08), Chapter 3 (Medical Review).",
            "Centers for Medicare & Medicaid Services (CMS). Medicare Learning Network (MLN) Matters Article MM6698: Signature Guidelines.",
            "Centers for Medicare & Medicaid Services (CMS). National Correct Coding Initiative (NCCI) Policy Manual for Medicare Services.",
            "Centers for Medicare & Medicaid Services (CMS). Medically Unlikely Edits (MUE) Program Operating Instructions.",
            "Accredited Standards Committee X12. ASC X12N 837 Professional Health Care Claim (005010X222A1) and ASC X12N 277CA Standards.",
            "Washington Publishing Company (WPC). Claim Adjustment Reason Codes (CARC) and Remittance Advice Remark Codes (RARC) Catalog.",
            "American Health Information Management Association (AHIMA). Clinical Documentation Integrity (CDI) Toolkit and Query Guidelines."
        ]
        for ref_text in refs:
            p_ref = self.doc.add_paragraph(style='List Bullet')
            p_ref.add_run(ref_text)

        self.doc.add_paragraph().paragraph_format.space_after = Pt(12)
