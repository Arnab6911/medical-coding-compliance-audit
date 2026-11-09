"""Word document audit report generator for Medical Coding Compliance Audit Simulation.

Builds structured, professionally formatted Microsoft Word (.docx) audit reports
adhering to the 14-section compliance reporting standard.

All statistical metrics and findings are derived directly from the executed AuditEngine results.
"""

from __future__ import annotations
import io
from datetime import datetime
from typing import Optional, List, Dict
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from src.models import AuditSummary, AuditFinding, AuditSeverity, PatientRecord


# Color constants for document styling
PRIMARY_COLOR = RGBColor(30, 58, 138)    # Deep Navy (#1E3A8A)
SECONDARY_COLOR = RGBColor(14, 116, 144) # Ocean Teal (#0E7490)
ALERT_RED = RGBColor(220, 38, 38)        # High Severity (#DC2626)
WARN_AMBER = RGBColor(217, 119, 6)       # Medium Severity (#D97706)
INFO_BLUE = RGBColor(37, 99, 235)        # Low Severity (#2563EB)
MUTED_GRAY = RGBColor(100, 116, 139)     # Slate (#64748B)
TEXT_DARK = RGBColor(30, 41, 59)         # Dark slate (#1E293B)


def set_cell_background(cell, fill_hex: str) -> None:
    """Apply background shading color to a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top: int = 100, bottom: int = 100, left: int = 120, right: int = 120) -> None:
    """Set inner cell padding in twips."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


class ComplianceReportGenerator:
    """Builds comprehensive 14-section Word compliance audit reports from audit results."""

    def __init__(self, summary: AuditSummary, records: Optional[List[PatientRecord]] = None):
        self.summary = summary
        self.records = records or []
        self.doc: Document = Document()
        self._configure_styles()

    def _configure_styles(self) -> None:
        """Set up standard typography and page layout."""
        for section in self.doc.sections:
            section.top_margin = Inches(1.0)
            section.bottom_margin = Inches(1.0)
            section.left_margin = Inches(1.0)
            section.right_margin = Inches(1.0)

        style = self.doc.styles['Normal']
        style.font.name = 'Calibri'
        style.font.size = Pt(10.5)
        style.font.color.rgb = TEXT_DARK

    def generate(self, output_path_or_stream: Optional[str] = None) -> io.BytesIO:
        """Assemble full 14-section audit report and write to file or stream.

        Args:
            output_path_or_stream: Optional file path string to save the .docx.

        Returns:
            BytesIO stream containing the binary document data.
        """
        # Section 1: Cover Page
        self._add_section_1_cover_page()

        # Section 2: Executive Summary
        self._add_section_2_executive_summary()

        # Section 3: Introduction
        self._add_section_3_introduction()

        # Section 4: Objectives
        self._add_section_4_objectives()

        # Section 5: Scope and Limitations
        self._add_section_5_scope_and_limitations()

        # Section 6: Audit Methodology
        self._add_section_6_audit_methodology()

        # Section 7: Coding Compliance Criteria
        self._add_section_7_compliance_criteria()

        # Section 8: Dataset Description
        self._add_section_8_dataset_description()

        # Section 9: Detailed Audit Findings with Encounter IDs
        self._add_section_9_detailed_findings()

        # Section 10: Issue-Wise Explanations
        self._add_section_10_issue_explanations()

        # Section 11: Corrective Actions
        self._add_section_11_corrective_actions()

        # Section 12: Preventive Recommendations
        self._add_section_12_preventive_recommendations()

        # Section 13: Conclusion
        self._add_section_13_conclusion()

        # Section 14: References
        self._add_section_14_references()

        stream = io.BytesIO()
        self.doc.save(stream)
        stream.seek(0)

        if output_path_or_stream:
            with open(output_path_or_stream, 'wb') as f:
                f.write(stream.getvalue())

        return stream

    # -------------------------------------------------------------------------
    # SECTION 1: COVER PAGE
    # -------------------------------------------------------------------------
    def _add_section_1_cover_page(self) -> None:
        """Generate professional cover page with metadata and simulation notice."""
        p_space = self.doc.add_paragraph()
        p_space.paragraph_format.space_before = Pt(40)

        p_org = self.doc.add_paragraph()
        r_org = p_org.add_run("HEALTHCARE COMPLIANCE & INTEGRITY AUDIT DIVISION")
        r_org.font.size = Pt(11)
        r_org.font.bold = True
        r_org.font.color.rgb = SECONDARY_COLOR
        p_org.paragraph_format.space_after = Pt(20)

        p_title = self.doc.add_paragraph()
        r_title = p_title.add_run("Medical Coding Compliance Audit Report")
        r_title.font.size = Pt(26)
        r_title.font.bold = True
        r_title.font.color.rgb = PRIMARY_COLOR
        p_title.paragraph_format.space_after = Pt(6)

        p_sub = self.doc.add_paragraph()
        r_sub = p_sub.add_run("Automated Documentation Review, Diagnostic Alignment, and Risk Analysis")
        r_sub.font.size = Pt(14)
        r_sub.font.italic = True
        r_sub.font.color.rgb = MUTED_GRAY
        p_sub.paragraph_format.space_after = Pt(40)

        # Meta Box
        tbl_meta = self.doc.add_table(rows=5, cols=2)
        tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
        meta_items = [
            ("Audit Project:", "Medical Coding Compliance Audit Simulation"),
            ("Date of Audit:", datetime.now().strftime("%B %d, %Y")),
            ("Audited Records:", f"{self.summary.total_records} Fictional Encounters"),
            ("Code Set Standards:", "ICD-10-CM (FY 2024 Standard) & CPT® (2024 Educational Reference)"),
            ("Project Level:", "Internship Submission & Academic Simulation Standard")
        ]
        for row_idx, (lbl, val) in enumerate(meta_items):
            c1, c2 = tbl_meta.cell(row_idx, 0), tbl_meta.cell(row_idx, 1)
            set_cell_margins(c1, top=60, bottom=60, left=80, right=80)
            set_cell_margins(c2, top=60, bottom=60, left=80, right=80)
            set_cell_background(c1, "F8FAFC")
            set_cell_background(c2, "F8FAFC")
            p1 = c1.paragraphs[0].add_run(lbl)
            p1.font.bold = True
            p1.font.size = Pt(9.5)
            p2 = c2.paragraphs[0].add_run(val)
            p2.font.size = Pt(9.5)

        self.doc.add_paragraph().paragraph_format.space_after = Pt(50)

        # Cover Page Disclaimer Callout
        tbl_disc = self.doc.add_table(rows=1, cols=1)
        tbl_disc.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell_disc = tbl_disc.cell(0, 0)
        set_cell_background(cell_disc, "FEF3C7")
        set_cell_margins(cell_disc, top=120, bottom=120, left=150, right=150)
        p_disc = cell_disc.paragraphs[0]
        r_dhdr = p_disc.add_run("EDUCATIONAL SIMULATION NOTICE\n")
        r_dhdr.font.bold = True
        r_dhdr.font.size = Pt(9.5)
        r_dhdr.font.color.rgb = RGBColor(146, 64, 14)
        r_dbody = p_disc.add_run(
            "This report is generated by an educational simulation application. All patient names, "
            "demographics, encounter IDs, and clinical notes are synthetic and fictional. This document "
            "DOES NOT constitute certified medical coding advice, legal counsel, or official billing guidance. "
            "The system is not HIPAA certified and must never process real Protected Health Information (PHI). "
            "Automated flags require human review and never modify patient records."
        )
        r_dbody.font.size = Pt(8.5)
        r_dbody.font.color.rgb = RGBColor(120, 53, 15)

        self.doc.add_page_break()

    # -------------------------------------------------------------------------
    # SECTION 2: EXECUTIVE SUMMARY
    # -------------------------------------------------------------------------
    def _add_section_2_executive_summary(self) -> None:
        """Render Section 2: Executive Summary with empirical audit metrics."""
        self._add_section_heading("2. Executive Summary")

        p = self.doc.add_paragraph()
        p.add_run(
            f"This audit evaluated {self.summary.total_records} fictional outpatient encounter records to assess "
            f"compliance with federal billing regulations, ICD-10-CM Official Coding Guidelines (FY 2024), and "
            f"CPT 2024 documentation requirements. The audit engine identified {self.summary.total_findings} distinct "
            f"compliance findings across {self.summary.records_flagged} encounter(s), yielding an overall encounter "
            f"compliance rate of {self.summary.compliance_rate}% and a manual review requirement rate of "
            f"{self.summary.review_rate}%.\n\n"
            f"High-severity issues—representing imminent recoupment or False Claims Act scrutiny—account for "
            f"{self.summary.high_severity_count} findings ({round(self.summary.high_severity_count / max(self.summary.total_findings, 1) * 100, 1)}% "
            f"of total issues). A total of {self.summary.clean_records} encounter(s) demonstrated complete documentation, "
            f"valid clinician signatures, and fully substantiated coding."
        )

        # Summary Metrics Table
        tbl = self.doc.add_table(rows=6, cols=3)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

        headers = ["Compliance Metric", "Empirical Count", "Audit Benchmark / Implication"]
        for col_idx, h_text in enumerate(headers):
            cell = tbl.cell(0, col_idx)
            set_cell_background(cell, "1E3A8A")
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            r = cell.paragraphs[0].add_run(h_text)
            r.font.bold = True
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(255, 255, 255)

        metrics = [
            ("Total Records Audited", str(self.summary.total_records), "100% of study cohort"),
            ("Records Requiring Manual Review", str(self.summary.records_flagged), f"{self.summary.review_rate}% review rate"),
            ("Compliant Encounters (Clean)", str(self.summary.clean_records), f"{self.summary.compliance_rate}% compliance rate"),
            ("High-Severity Discrepancies", str(self.summary.high_severity_count), "Priority stop: overpayment / recoupment risk"),
            ("Documentation vs Coding Issues", f"{self.summary.documentation_issues_count} Doc / {self.summary.coding_issues_count} Code", "Categorical issue balance")
        ]

        for row_idx, (m_lbl, m_val, m_note) in enumerate(metrics, start=1):
            bg = "F1F5F9" if row_idx % 2 == 1 else "FFFFFF"
            for col_idx, val in enumerate([m_lbl, m_val, m_note]):
                cell = tbl.cell(row_idx, col_idx)
                set_cell_background(cell, bg)
                set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
                p = cell.paragraphs[0]
                r = p.add_run(val)
                r.font.size = Pt(9)
                if col_idx == 1:
                    r.font.bold = True
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

        self.doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SECTION 3: INTRODUCTION
    # -------------------------------------------------------------------------
    def _add_section_3_introduction(self) -> None:
        """Render Section 3: Introduction."""
        self._add_section_heading("3. Introduction")
        p = self.doc.add_paragraph()
        p.add_run(
            "Healthcare reimbursement in the United States relies upon the accurate translation of clinical encounters "
            "into standardized alphanumeric code sets: ICD-10-CM for diagnoses and CPT/HCPCS for outpatient procedures and "
            "Evaluation and Management (E/M) services. Healthcare providers bear the legal responsibility to ensure that "
            "every code submitted to Medicare, Medicaid, or commercial payers is strictly substantiated by authentic, legible, "
            "and clinically sufficient medical documentation.\n\n"
            "The Department of Health and Human Services Office of Inspector General (HHS-OIG) consistently targets improper "
            "coding practices under the False Claims Act (31 U.S.C. § 3729) and the Civil Monetary Penalties Law. Conducting "
            "regular pre-bill and retrospective coding compliance audits is an essential safeguard to maintain billing "
            "integrity, optimize clinical documentation, and eliminate financial liability."
        )
        p.paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SECTION 4: OBJECTIVES
    # -------------------------------------------------------------------------
    def _add_section_4_objectives(self) -> None:
        """Render Section 4: Objectives."""
        self._add_section_heading("4. Objectives")
        p = self.doc.add_paragraph()
        p.add_run("The primary objectives of this compliance audit simulation are to:\n")

        objectives = [
            ("Quantify Documentation Completeness", "Evaluate whether patient encounter notes meet baseline length, clinical depth, and electronic authentication requirements."),
            ("Detect Coding Mismatches", "Identify diagnostic and procedural code assignments that conflict with documented clinical conditions or lack textual substantiation."),
            ("Verify Medical Necessity", "Assess whether assigned CPT procedure codes are supported by appropriate primary ICD-10-CM diagnosis codes under Medicare guidelines."),
            ("Audit High-Risk E/M Encounters", "Scrutinize Level 5 E/M visits (CPT 99215) for requisite Medical Decision Making (MDM) complexity or qualifying time documentation."),
            ("Facilitate Human Auditor Workflows", "Generate actionable recommendations and authoritative citations without ever automatically altering patient charts.")
        ]
        for title, desc in objectives:
            p_obj = self.doc.add_paragraph(style='List Bullet')
            r_b = p_obj.add_run(f"{title}: ")
            r_b.font.bold = True
            p_obj.add_run(desc)

        self.doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SECTION 5: SCOPE AND LIMITATIONS
    # -------------------------------------------------------------------------
    def _add_section_5_scope_and_limitations(self) -> None:
        """Render Section 5: Scope and Limitations."""
        self._add_section_heading("5. Scope & Limitations")
        p = self.doc.add_paragraph()
        p.add_run(
            "Audit Scope & Code Set Versions:\n"
            "The audit scope is confined to outpatient physician encounter records. Evaluated code sets include "
            "ICD-10-CM FY 2024 diagnostic codes (effective October 1, 2023 through September 30, 2024) and CPT 2024 "
            "outpatient Evaluation and Management (E/M) and common office procedure codes (effective January 1, 2024).\n\n"
            "Historical vs. Current Coding Context:\n"
            "Medical code sets undergo regular statutory revisions. ICD-10-CM updates annually on October 1st, while CPT "
            "updates annually on January 1st. In 2021 and 2023, the American Medical Association (AMA) and CMS executed "
            "landmark revisions to outpatient Evaluation and Management (E/M) coding, eliminating the historical 1995/1997 "
            "scoring of history and physical exam bullet counts in favor of Medical Decision Making (MDM) or total encounter time. "
            "This simulation applies these modernized 2021/2023 E/M documentation principles.\n\n"
            "Operational & Regulatory Limitations:\n"
            "1. Educational Simulation: This application is constructed strictly as an educational learning platform. "
            "It does not replace certified professional coding judgment (CPC, CCS, CPMA).\n"
            "2. Non-HIPAA Environment: The software operates on de-identified synthetic data only. It lacks HIPAA-certified "
            "encryption and must not receive real Protected Health Information (PHI).\n"
            "3. Codebook Coverage: The reference database encompasses an educational standard subset. Codes outside this "
            "curated subset are flagged as 'Unverified Reference Code' for manual verification rather than assumed invalid.\n"
            "4. Missing Documentation vs. Coding Error: Missing clinical documentation is flagged as an unverified service "
            "requiring chart retrieval and provider query, rather than an automatic accusation of intentional coding fraud.\n"
            "5. Zero Automatic Modifications: In adherence to compliance integrity standards, the audit engine is read-only "
            "and never modifies clinical documentation or billed codes."
        )
        p.paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SECTION 6: AUDIT METHODOLOGY
    # -------------------------------------------------------------------------
    def _add_section_6_audit_methodology(self) -> None:
        """Render Section 6: Audit Methodology."""
        self._add_section_heading("6. Audit Methodology")
        p = self.doc.add_paragraph()
        p.add_run(
            "The audit simulation executes a multi-tiered, rule-based algorithmic review modeled upon OIG compliance "
            "audit protocols. The methodology proceeds through five discrete stages:\n"
            "1. Record Ingestion & Normalization: Fictional encounter records are parsed from CSV files into strongly typed "
            "data structures capturing encounter IDs, patient demographics, clinical notes, and assigned codes.\n"
            "2. Automated Rule Execution: Independent, modular Python validation functions inspect each encounter across "
            "missing fields, code duplication, diagnostic alignment, procedure substantiation, and E/M justification.\n"
            "3. Clinical Negation & Category Cross-Validation: Diagnosis matching does not rely solely on simple keyword search; "
            "it evaluates clinical negation phrases (e.g. 'no history of', 'denies', 'ruled out') to eliminate false positive matches.\n"
            "4. Severity Scoring: Each discrepancy is stratified into High (regulatory/recoupment risk), Medium (technical defect/signature gap), "
            "or Low (coding specificity optimization) severity.\n"
            "5. Duplicate Finding Suppression: Emits distinct compliance issues while suppressing duplicate reporting of identical findings.\n"
            "6. Actionable Remediation Generation: For each flagged encounter, the engine synthesizes a specific corrective action "
            "and binds an authoritative regulatory citation."
        )
        p.paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SECTION 7: CODING COMPLIANCE CRITERIA
    # -------------------------------------------------------------------------
    def _add_section_7_compliance_criteria(self) -> None:
        """Render Section 7: Coding Compliance Criteria."""
        self._add_section_heading("7. Coding Compliance Criteria")
        p = self.doc.add_paragraph()
        p.add_run("Audited encounters were measured against the following authoritative regulatory benchmarks:\n")

        criteria = [
            ("Documentation Substantiation", "ICD-10-CM Official Guidelines FY 2024 Section I.B.1 mandates that all reported diagnosis codes must be supported by explicit provider documentation."),
            ("Diagnostic Alignment", "ICD-10-CM Guideline Section I.A.19 specifies that code assignment must accurately represent the condition documented by the attending clinician."),
            ("Medical Necessity", "Social Security Act § 1862(a)(1)(A) and CMS Pub 100-02 Chapter 15 §20 prohibit payment for services that are not reasonable and necessary for diagnosis or treatment."),
            ("Clinician Authentication", "CMS MLN Matters MM6698 requires a legible, compliant electronic or handwritten signature with credentials for all reimbursable encounters."),
            ("E/M Complexity Criteria", "AMA CPT 2024 E/M guidelines require Level 5 established visits (99215) to satisfy high Medical Decision Making (MDM) or 40-54 minutes of encounter time."),
            ("Multiple Procedure Duplication", "CMS NCCI Policy Manual Chapter 1 §B requires distinct modifiers for repeatable services and prohibits unbundled duplicates.")
        ]
        for name, text in criteria:
            p_crit = self.doc.add_paragraph(style='List Bullet')
            r_b = p_crit.add_run(f"{name}: ")
            r_b.font.bold = True
            p_crit.add_run(text)

        self.doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SECTION 8: DATASET DESCRIPTION
    # -------------------------------------------------------------------------
    def _add_section_8_dataset_description(self) -> None:
        """Render Section 8: Dataset Description."""
        self._add_section_heading("8. Dataset Description")
        p = self.doc.add_paragraph()
        p.add_run(
            f"The audit dataset comprises {len(self.records) if self.records else self.summary.total_records} "
            f"synthetic outpatient encounter records. The dataset incorporates balanced patient demographics, varied "
            f"clinical specialties (general internal medicine, cardiology, pulmonology, gastroenterology, orthopedics), "
            f"and diverse documentation completeness profiles.\n\n"
            f"Dataset Characteristics:\n"
            f"• Encounter Identifier Format: ENC-1001 through ENC-1020\n"
            f"• Patient Age Distribution: 28 to 72 years (Mean: 50.4 years)\n"
            f"• Patient Gender Distribution: Balanced male and female fictional cohorts\n"
            f"• Applicable Code Sets: ICD-10-CM (FY 2024) and CPT (2024)\n"
            f"• Clinical Conditions Documented: Essential hypertension, type 2 diabetes mellitus, acute pharyngitis, "
            f"severe asthma, osteoarthritis, acute bronchitis, preventive wellness, GERD, pneumonia, chest pain, and fatigue\n"
            f"• CPT Procedures Sampled: Outpatient E/M levels 1-5, screening colonoscopy, 12-lead ECG, 2-view chest radiography, and routine venipuncture"
        )
        p.paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SECTION 9: DETAILED AUDIT FINDINGS WITH ENCOUNTER IDS
    # -------------------------------------------------------------------------
    def _add_section_9_detailed_findings(self) -> None:
        """Render Section 9: Detailed Audit Findings Table with Code-Set Year."""
        self._add_section_heading("9. Detailed Audit Findings with Encounter IDs")

        if not self.summary.findings:
            p = self.doc.add_paragraph()
            p.add_run("No compliance findings were identified in the audited dataset.")
            return

        p_intro = self.doc.add_paragraph()
        p_intro.add_run(
            f"A total of {len(self.summary.findings)} discrete compliance findings were identified across "
            f"{self.summary.records_flagged} encounter(s). The table below itemizes every flagged encounter, "
            f"patient reference, assigned codes, applicable code-set year, issue category, assigned severity, "
            f"and specific audit rationale."
        )

        tbl = self.doc.add_table(rows=1 + len(self.summary.findings), cols=7)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

        headers = ["Encounter ID", "Patient ID", "Assigned Code", "Code Set Year", "Issue Category", "Severity", "Audit Rationale & Citation"]
        for col_idx, h_text in enumerate(headers):
            cell = tbl.cell(0, col_idx)
            set_cell_background(cell, "1E3A8A")
            set_cell_margins(cell, top=90, bottom=90, left=70, right=70)
            r = cell.paragraphs[0].add_run(h_text)
            r.font.bold = True
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(255, 255, 255)

        for row_idx, finding in enumerate(self.summary.findings, start=1):
            bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            col_data = [
                finding.encounter_id,
                finding.patient_id,
                finding.assigned_code,
                finding.code_set_year,
                finding.audit_issue,
                finding.severity.value,
                f"{finding.reason}\n\nGuideline: {finding.reference_guideline}"
            ]
            for col_idx, text in enumerate(col_data):
                cell = tbl.cell(row_idx, col_idx)
                set_cell_background(cell, bg)
                set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
                p = cell.paragraphs[0]
                r = p.add_run(text)
                r.font.size = Pt(8)

                if col_idx == 0:
                    r.font.bold = True
                elif col_idx == 5:
                    r.font.bold = True
                    if finding.severity == AuditSeverity.HIGH:
                        r.font.color.rgb = ALERT_RED
                    elif finding.severity == AuditSeverity.MEDIUM:
                        r.font.color.rgb = WARN_AMBER
                    else:
                        r.font.color.rgb = INFO_BLUE

        self.doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # -------------------------------------------------------------------------
    # SECTION 10: ISSUE-WISE EXPLANATIONS
    # -------------------------------------------------------------------------
    def _add_section_10_issue_explanations(self) -> None:
        """Render Section 10: Issue-Wise Explanations."""
        self._add_section_heading("10. Issue-Wise Explanations")
        p = self.doc.add_paragraph()
        p.add_run(
            "Below is a detailed analysis of each compliance issue category identified by the audit engine:\n"
        )

        issues_map: Dict[str, List[AuditFinding]] = {}
        for f in self.summary.findings:
            issues_map.setdefault(f.audit_issue, []).append(f)

        explanations = {
            "Diagnosis Code Mismatch": (
                "Occurs when an assigned ICD-10-CM code contradicts the documented diagnosis in the physician note. "
                "For example, in encounter ENC-1002, Essential Hypertension was documented, but E11.9 (Type 2 Diabetes) "
                "was assigned. Such mismatches distort clinical registries, alter risk adjustment scores (HCCs), and cause claim audits."
            ),
            "Unsupported Procedure Medical Necessity": (
                "Identified when CPT procedural codes lack medical necessity justification based on the reported primary diagnosis. "
                "In encounter ENC-1003, CPT 45378 (Colonoscopy) was billed alongside acute pharyngitis without any gastrointestinal indication."
            ),
            "Missing Procedure Documentation": (
                "Occurs when an invasive or diagnostic procedure CPT code is billed but the encounter lacks standalone operative or "
                "imaging findings documentation (e.g. ENC-1003 colonoscopy or ENC-1015 chest x-ray). Represents an unsubstantiated service requiring chart retrieval."
            ),
            "Unsupported E/M Level": (
                "Triggered when high-complexity Level 5 outpatient E/M codes (CPT 99215) are billed for uncomplicated conditions "
                "(e.g., routine back strain in ENC-1018) without documenting high Medical Decision Making (MDM) or qualifying encounter time."
            ),
            "Missing Clinical Documentation": (
                "Occurs when an encounter has codes assigned in the billing system but the clinical documentation progress note is "
                "entirely absent (e.g., ENC-1020). Submitting claims with zero clinical documentation represents an acute False Claims liability."
            ),
            "Missing Diagnosis Documentation": (
                "Occurs when ICD-10 codes are populated on a claim line, but the Documented Diagnosis field is blank (e.g., ENC-1019). "
                "Codes must originate from documented physician diagnoses."
            ),
            "Incomplete Clinical Documentation": (
                "Triggered when clinical notes are excessively terse (under 15 words, e.g., ENC-1004 'Meds refilled.'), failing to "
                "establish history, physical examination, or treatment plan."
            ),
            "Missing Provider Signature": (
                "Identified when encounter documentation lacks an authenticated clinician electronic signature (e.g., ENC-1011). "
                "Medicare rules deem unauthenticated records non-reimbursable."
            ),
            "Duplicate Diagnosis Entry": (
                "Detected when identical ICD-10 codes are entered multiple times on the same encounter (e.g., ENC-1012). Causes clearinghouse claim rejections."
            ),
            "Duplicate Procedure Entry": (
                "Detected when identical CPT codes are entered multiple times on the same encounter without required CPT modifiers."
            ),
            "Unverified Reference Code": (
                "Triggered when a code outside the active reference standard is assigned (e.g., ENC-1017 Z99.999). Mandates manual tabular verification."
            ),
            "Unspecified Code Warning": (
                "Flagged when an unspecified code (e.g., M17.9 Knee Osteoarthritis Unspecified in ENC-1006) is assigned despite the clinical note "
                "explicitly specifying laterality (Right knee). Encourages specificity optimization."
            )
        }

        for issue_name, findings_list in issues_map.items():
            exp_text = explanations.get(issue_name, "Compliance discrepancy requiring coder and clinician review.")
            p_issue = self.doc.add_paragraph()
            r_head = p_issue.add_run(f"• {issue_name} ({len(findings_list)} occurrences):\n")
            r_head.font.bold = True
            r_head.font.color.rgb = PRIMARY_COLOR
            p_issue.add_run(exp_text)
            p_issue.paragraph_format.space_after = Pt(6)

        self.doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SECTION 11: CORRECTIVE ACTIONS
    # -------------------------------------------------------------------------
    def _add_section_11_corrective_actions(self) -> None:
        """Render Section 11: Corrective Actions."""
        self._add_section_heading("11. Corrective Actions")
        p = self.doc.add_paragraph()
        p.add_run(
            "To remediate the specific findings identified during this audit, the compliance department recommends "
            "the following immediate operational actions:\n"
        )

        actions = [
            ("Pre-Bill Claim Holds", "Place billing holds on encounters flagged with High Severity (ENC-1002, ENC-1003, ENC-1004, ENC-1008, ENC-1015, ENC-1018, ENC-1019, ENC-1020) to prevent immediate payer submission."),
            ("Physician Documentation Addenda", "Request attending clinician addenda for encounters with terse notes (ENC-1004) or missing progress notes (ENC-1020) before billing is finalized."),
            ("Electronic Signature Enforcement", "Route unsigned encounters (ENC-1011) back to the authoring provider for authenticated electronic signature and timestamp completion."),
            ("Code Realignment & Removal", "Correct diagnostic codes to match documented conditions (re-align ENC-1002 to I10, ENC-1008 to acute bronchitis) and remove unperformed procedure CPTs (remove 45378 from ENC-1003, 71046 from ENC-1015)."),
            ("Downcoding Overbilled E/M", "Downcode encounter ENC-1018 from Level 5 (CPT 99215) to Level 3 (CPT 99213) in accordance with the documented low-complexity Medical Decision Making.")
        ]
        for title, desc in actions:
            p_act = self.doc.add_paragraph(style='List Bullet')
            r_b = p_act.add_run(f"{title}: ")
            r_b.font.bold = True
            p_act.add_run(desc)

        self.doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SECTION 12: PREVENTIVE RECOMMENDATIONS
    # -------------------------------------------------------------------------
    def _add_section_12_preventive_recommendations(self) -> None:
        """Render Section 12: Preventive Recommendations."""
        self._add_section_heading("12. Preventive Recommendations")
        p = self.doc.add_paragraph()
        p.add_run(
            "To prevent recurrence of identified documentation and coding defects across the healthcare organization, "
            "the following preventive policies should be enacted:\n"
        )

        preventative = [
            ("EHR Automated Hard Stops", "Configure the electronic health record (EHR) to prevent encounter finalization unless all mandatory fields, clinical progress notes, and compliant electronic signatures are validated."),
            ("Automated Medical Necessity Crosswalks", "Implement clearinghouse claim scrubbing rules that cross-reference CPT procedure codes with primary ICD-10-CM diagnosis codes prior to claim submission."),
            ("Provider E/M Documentation Education", "Deliver targeted clinical documentation training to clinicians regarding 2021/2023 E/M revisions, highlighting specific MDM complexity thresholds required for Level 4 and Level 5 services."),
            ("Clinical Documentation Improvement (CDI) Workflow", "Establish a standardized, non-leading physician query process to resolve diagnostic ambiguities before coding finalization."),
            ("Periodic Audit Cadence", "Conduct prospective quarterly audits of high-risk coding categories (Level 5 E/M, surgical procedures, and diagnostic imaging) to monitor provider compliance trends.")
        ]
        for title, desc in preventative:
            p_prev = self.doc.add_paragraph(style='List Bullet')
            r_b = p_prev.add_run(f"{title}: ")
            r_b.font.bold = True
            p_prev.add_run(desc)

        self.doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SECTION 13: CONCLUSION
    # -------------------------------------------------------------------------
    def _add_section_13_conclusion(self) -> None:
        """Render Section 13: Conclusion."""
        self._add_section_heading("13. Conclusion")
        p = self.doc.add_paragraph()
        p.add_run(
            f"The Medical Coding Compliance Audit Simulation demonstrated an overall encounter compliance rate of "
            f"{self.summary.compliance_rate}%, identifying critical vulnerabilities in procedure substantiation, diagnostic "
            f"alignment, and clinician electronic authentication. The identification of {self.summary.high_severity_count} "
            f"high-severity discrepancies underscores the necessity of continuous compliance oversight.\n\n"
            f"By executing timely corrective actions on flagged encounters and embedding automated EHR validation rules, "
            f"healthcare organizations can protect against severe regulatory recoupment, maintain clinical documentation integrity, "
            f"and uphold the highest standards of healthcare billing compliance."
        )
        p.paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SECTION 14: REFERENCES
    # -------------------------------------------------------------------------
    def _add_section_14_references(self) -> None:
        """Render Section 14: References."""
        self._add_section_heading("14. References")
        p = self.doc.add_paragraph()
        p.add_run("The audit methodology, coding criteria, and compliance evaluations reference the following authoritative standards:\n")

        citations = [
            "Centers for Medicare & Medicaid Services (CMS) & National Center for Health Statistics (NCHS). (2024). ICD-10-CM Official Guidelines for Coding and Reporting (FY 2024).",
            "American Medical Association (AMA). (2024). Current Procedural Terminology (CPT®) 2024 Standard Edition. Chicago, IL: AMA.",
            "CMS. (2024). Medicare Claims Processing Manual (Pub. 100-04), Chapter 23 – Fee Schedule Administration and Coding Requirements. Baltimore, MD: CMS.",
            "CMS. (2024). Medicare Program Integrity Manual (Pub. 100-08), Chapter 3 – Verifying Potential Errors and Taking Corrective Action. Baltimore, MD: CMS.",
            "CMS. (2024). Medicare Benefit Policy Manual (Pub. 100-02), Chapter 15 – Covered Medical and Other Health Services (§20 Medical Necessity). Baltimore, MD: CMS.",
            "CMS Medicare Learning Network (MLN). (2024). MLN Matters Article MM6698: Signature Guidelines for Medical Review. Baltimore, MD: CMS.",
            "United States Department of Health and Human Services, Office of Inspector General (HHS-OIG). (2024). OIG General Compliance Program Guidance (GCPG). Washington, DC: HHS-OIG.",
            "United States Congress. False Claims Act, 31 U.S.C. §§ 3729-3733."
        ]
        for cit in citations:
            p_ref = self.doc.add_paragraph(style='List Bullet')
            p_ref.add_run(cit)
            p_ref.paragraph_format.space_after = Pt(4)

    def _add_section_heading(self, text: str) -> None:
        """Add standardized numbered section heading."""
        h1 = self.doc.add_heading(level=1)
        r = h1.add_run(text)
        r.font.name = "Calibri"
        r.font.color.rgb = PRIMARY_COLOR
        r.font.size = Pt(14)
        r.font.bold = True
        h1.paragraph_format.space_before = Pt(14)
        h1.paragraph_format.space_after = Pt(6)
