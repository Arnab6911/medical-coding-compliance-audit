"""Medical Coding Compliance Audit Simulation - Interactive Streamlit Dashboard.

An educational compliance auditing interface that analyzes fictional medical records,
identifies potential coding and documentation discrepancies, visualizes audit metrics,
and exports comprehensive Word and CSV compliance reports.
"""

from __future__ import annotations
import io
import pandas as pd
import streamlit as st

from src.models import AuditSeverity, IssueType, PatientRecord, AuditSummary
from src.rules_engine import AuditEngine, load_records_from_csv
from src.reference_data import get_reference_manager
from src.report_generator import ComplianceReportGenerator
from src.visualizer import (
    plot_severity_distribution,
    plot_issue_categories,
    plot_audit_status_breakdown
)


# Configure Streamlit page layout
st.set_page_config(
    page_title="Medical Coding Compliance Audit Simulation",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling for healthcare compliance aesthetic
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1E3A8A 0%, #0E7490 100%);
        padding: 24px 28px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
    }
    .main-header h1 {
        color: white;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        padding: 0;
    }
    .main-header p {
        color: #E2E8F0;
        font-size: 14px;
        margin-top: 6px;
        margin-bottom: 0;
    }
    .disclaimer-banner {
        background-color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        padding: 12px 18px;
        border-radius: 6px;
        color: #92400E;
        font-size: 13px;
        margin-bottom: 22px;
    }
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
    }
    .kpi-title {
        font-size: 12px;
        text-transform: uppercase;
        font-weight: 600;
        color: #64748B;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: 800;
        margin-top: 4px;
        color: #1E293B;
    }
    .badge-high {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 12px;
    }
    .badge-medium {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 12px;
    }
    .badge-low {
        background-color: #DBEAFE;
        color: #1E40AF;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)


def main():
    ref_manager = get_reference_manager()
    engine = AuditEngine(ref_manager)

    # Header Banner
    st.markdown("""
    <div class="main-header">
        <h1>🩺 Medical Coding Compliance Audit Simulation</h1>
        <p>Automated Clinical Documentation & Diagnostic Code Verification Engine for Healthcare Compliance Training</p>
    </div>
    """, unsafe_allow_html=True)

    # Mandatory Simulation Notice
    st.markdown("""
    <div class="disclaimer-banner">
        ⚠️ <strong>EDUCATIONAL SIMULATION NOTICE:</strong> This application analyzes synthetic, fictional medical records
        for educational compliance demonstration. It does <strong>not</strong> provide certified medical coding advice, legal counsel,
        or HIPAA-certified security. Automated flags highlight potential discrepancies requiring <strong>certified human auditor review</strong>.
        In strict compliance with audit governance, this software <strong>never modifies patient records or billing codes</strong>.
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # SIDEBAR: DATA INGESTION & CONTROLS
    # -------------------------------------------------------------------------
    st.sidebar.image("https://img.icons8.com/color/96/medical-clipboard.png", width=64)
    st.sidebar.title("Audit Control Panel")

    data_source = st.sidebar.radio(
        "Data Ingestion Source",
        ["Default Fictional Dataset (20 Records)", "Upload Custom CSV File"],
        help="Choose between pre-packaged fictional training records or upload your own CSV file."
    )

    records: list[PatientRecord] = []

    if data_source == "Default Fictional Dataset (20 Records)":
        sample_path = "data/sample_records.csv"
        try:
            records = load_records_from_csv(sample_path)
            st.sidebar.success(f"Loaded {len(records)} fictional records from standard dataset.")
        except Exception as e:
            st.sidebar.error(f"Error reading sample dataset: {e}")
    else:
        uploaded_file = st.sidebar.file_uploader(
            "Upload Encounter Records CSV",
            type=["csv"],
            help="Expected columns: Encounter_ID, Patient_ID, Patient_Age, Patient_Gender, Encounter_Date, Clinical_Documentation, Documented_Diagnosis, Assigned_ICD10, Procedure_Description, Assigned_CPT, Documentation_Completeness"
        )
        if uploaded_file is not None:
            try:
                records = load_records_from_csv(uploaded_file)
                st.sidebar.success(f"Loaded {len(records)} records from uploaded file.")
            except Exception as e:
                st.sidebar.error(f"Failed to parse CSV: {e}")
        else:
            st.info("Please upload a CSV file or switch to the default fictional dataset.")
            return

    if not records:
        st.warning("No records available to audit.")
        return

    # Execute Audit Engine
    summary: AuditSummary = engine.audit_dataset(records)

    # Sidebar Filter Controls
    st.sidebar.markdown("---")
    st.sidebar.subheader("Filter Findings")

    selected_severities = st.sidebar.multiselect(
        "Severity Levels",
        options=[s.value for s in AuditSeverity],
        default=[s.value for s in AuditSeverity]
    )

    available_issues = sorted(list({f.audit_issue for f in summary.findings}))
    selected_issues = st.sidebar.multiselect(
        "Issue Categories",
        options=available_issues,
        default=available_issues
    )

    search_query = st.sidebar.text_input(
        "Search Records or Codes",
        placeholder="e.g. ENC-1002, I10, 99215, asthma"
    ).strip().lower()

    # Sidebar Reference Standards Info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📚 Reference Code Standards")
    st.sidebar.caption(f"**ICD-10-CM:** {ref_manager.icd10_version}")
    st.sidebar.caption(f"**CPT:** {ref_manager.cpt_version}")
    st.sidebar.caption(f"**Rules Engine:** v{ref_manager.rules_version}")

    # -------------------------------------------------------------------------
    # TABS INTERFACE
    # -------------------------------------------------------------------------
    tab_dashboard, tab_explorer, tab_guidelines = st.tabs([
        "📊 Compliance Dashboard",
        "🔍 Record Audit Explorer",
        "📖 Audit Methodology & Rules"
    ])

    # -------------------------------------------------------------------------
    # TAB 1: COMPLIANCE DASHBOARD
    # -------------------------------------------------------------------------
    with tab_dashboard:
        # 5 Metric KPI Cards as specified
        k1, k2, k3, k4, k5 = st.columns(5)
        with k1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Records Audited</div>
                <div class="kpi-value">{summary.total_records}</div>
            </div>
            """, unsafe_allow_html=True)
        with k2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Requires Manual Review</div>
                <div class="kpi-value" style="color: #DC2626;">{summary.records_flagged}</div>
            </div>
            """, unsafe_allow_html=True)
        with k3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Correctly Documented</div>
                <div class="kpi-value" style="color: #10B981;">{summary.clean_records}</div>
            </div>
            """, unsafe_allow_html=True)
        with k4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Potential Coding Errors</div>
                <div class="kpi-value" style="color: #2563EB;">{summary.coding_issues_count}</div>
            </div>
            """, unsafe_allow_html=True)
        with k5:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Documentation Deficiencies</div>
                <div class="kpi-value" style="color: #D97706;">{summary.documentation_issues_count}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Audit Visualizations Row
        c1, c2, c3 = st.columns([1, 1.4, 1])
        with c1:
            fig_sev = plot_severity_distribution(summary)
            st.pyplot(fig_sev, use_container_width=True)
        with c2:
            fig_cat = plot_issue_categories(summary)
            st.pyplot(fig_cat, use_container_width=True)
        with c3:
            fig_stat = plot_audit_status_breakdown(summary)
            st.pyplot(fig_stat, use_container_width=True)

        st.markdown("---")

        # Detailed Findings Table with Search & Filtering
        st.subheader("📋 Detailed Compliance Findings Table")

        # Apply active filters
        filtered_findings = [
            f for f in summary.findings
            if f.severity.value in selected_severities
            and f.audit_issue in selected_issues
        ]

        if search_query:
            filtered_findings = [
                f for f in filtered_findings
                if search_query in f.encounter_id.lower()
                or search_query in f.patient_id.lower()
                or search_query in f.assigned_code.lower()
                or search_query in f.original_diagnosis.lower()
                or search_query in f.audit_issue.lower()
                or search_query in f.reason.lower()
            ]

        st.caption(f"Showing **{len(filtered_findings)}** of {summary.total_findings} total findings based on active filters.")

        if filtered_findings:
            table_data = [f.to_dict() for f in filtered_findings]
            df_findings = pd.DataFrame(table_data)

            st.dataframe(
                df_findings[[
                    "Encounter ID", "Patient ID", "Severity", "Audit Issue",
                    "Assigned Code", "Original Diagnosis", "Reason for Flagging",
                    "Recommended Corrective Action", "Reference / Guideline"
                ]],
                use_container_width=True,
                height=400
            )
        else:
            st.info("No findings match the selected filters or search terms.")

        # Multi-Format Export Hub
        st.markdown("### 📤 Compliance Export Hub")
        exp_col1, exp_col2 = st.columns(2)

        with exp_col1:
            # CSV Download
            csv_data = pd.DataFrame([f.to_dict() for f in summary.findings]).to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Audit Findings (CSV)",
                data=csv_data,
                file_name="medical_coding_compliance_findings.csv",
                mime="text/csv",
                use_container_width=True
            )

        with exp_col2:
            # Word Report Download
            report_gen = ComplianceReportGenerator(summary, records=records)
            docx_stream = report_gen.generate()
            st.download_button(
                label="📄 Generate & Download Formal Word Audit Report (.docx)",
                data=docx_stream.getvalue(),
                file_name="Medical_Coding_Compliance_Audit_Report.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )

    # -------------------------------------------------------------------------
    # TAB 2: RECORD AUDIT EXPLORER
    # -------------------------------------------------------------------------
    with tab_explorer:
        st.subheader("🔍 Encounter Detail & Compliance Inspection")
        st.caption("Drill down into individual patient encounter records to review clinical documentation, assigned codes, and audit rationale.")

        # Record Selector
        encounter_ids = [r.encounter_id for r in records]
        selected_enc_id = st.selectbox(
            "Select Encounter ID to Inspect",
            options=encounter_ids,
            index=0
        )

        selected_record = next(r for r in records if r.encounter_id == selected_enc_id)
        record_findings = engine.audit_record(selected_record)

        col_left, col_right = st.columns([1.1, 1])

        with col_left:
            st.markdown("#### 📄 Clinical Encounter Record")
            st.markdown(
                f"**Encounter ID:** `{selected_record.encounter_id}` | "
                f"**Patient ID:** `{selected_record.patient_id}` | "
                f"**Age:** `{selected_record.patient_age}` | "
                f"**Gender:** `{selected_record.patient_gender}` | "
                f"**Date:** `{selected_record.encounter_date}`"
            )

            st.text_input("Documented Diagnosis", value=selected_record.documented_diagnosis or "(Empty)", disabled=True)
            st.text_input("Assigned ICD-10 Code(s)", value=selected_record.assigned_icd10 or "(None)", disabled=True)

            st.text_input("Procedure Description", value=selected_record.procedure_description or "(None)", disabled=True)
            st.text_input("Assigned CPT Code(s)", value=selected_record.assigned_cpt or "(None)", disabled=True)

            st.text_input("Documentation Completeness Flag", value=selected_record.documentation_completeness, disabled=True)

            st.markdown("**Clinical Documentation Notes:**")
            st.text_area(
                "Clinical Chart Notes",
                value=selected_record.clinical_documentation or "(No clinical documentation in chart)",
                height=180,
                disabled=True,
                label_visibility="collapsed"
            )

        with col_right:
            st.markdown("#### ⚖️ Audit Engine Findings")
            if not record_findings:
                st.success("✅ **CORRECTLY DOCUMENTED ENCOUNTER:** No compliance discrepancies detected. Documentation and coding meet baseline standards.")
            else:
                st.warning(f"⚠️ **MANUAL REVIEW REQUIRED:** {len(record_findings)} compliance issue(s) flagged for human auditor review.")

                for idx, finding in enumerate(record_findings, start=1):
                    sev = finding.severity.value
                    sev_class = "badge-high" if sev == "High" else ("badge-medium" if sev == "Medium" else "badge-low")

                    with st.expander(f"Finding #{idx}: {finding.audit_issue} ({sev})", expanded=True):
                        st.markdown(f"<span class='{sev_class}'>Severity: {sev}</span>", unsafe_allow_html=True)
                        st.markdown(f"**Flagged Code:** `{finding.assigned_code}`")
                        st.markdown(f"**Discrepancy Rationale:** {finding.reason}")
                        st.markdown(f"**Recommended Remediation:** {finding.recommended_action}")
                        st.info(f"**Regulatory Reference:**\n{finding.reference_guideline}")

            st.markdown("---")
            st.caption(
                "🔒 **Audit Governance Rule:** The audit engine operates in strictly read-only mode. "
                "Automated modification of clinical charts or billing codes is prohibited. "
                "All corrective actions must be validated by a certified coding professional (CPC/CCS)."
            )

    # -------------------------------------------------------------------------
    # TAB 3: AUDIT METHODOLOGY & RULES
    # -------------------------------------------------------------------------
    with tab_guidelines:
        st.subheader("📖 Compliance Audit Methodology & Rules Specification")

        st.markdown("""
        ### Multi-Tiered Compliance Audit Framework
        This simulation implements a proactive pre-bill compliance audit engine designed to reflect standard healthcare
        compliance methodologies established by the **Office of Inspector General (OIG)** and the **Centers for Medicare & Medicaid Services (CMS)**.
        """)

        with st.expander("1. Diagnosis Documentation Verification (ICD-10-CM Guideline I.B.1)", expanded=True):
            st.markdown("""
            - **Objective:** Ensure no diagnosis code is reported without corresponding clinical documentation.
            - **Audit Rule:** If an ICD-10 code is present on the encounter claim, but `Documented_Diagnosis` is empty or absent from clinical notes, a **High Severity** flag is generated.
            - **Remediation:** Clinician query or removal of unsupported diagnosis.
            - **Citation:** *ICD-10-CM Official Guidelines for Coding and Reporting FY 2024, Section I.B.1.*
            """)

        with st.expander("2. Diagnostic Alignment & Code Mismatch Detection", expanded=True):
            st.markdown("""
            - **Objective:** Prevent incorrect code assignment resulting from typographical errors, misinterpretation, or unverified codes.
            - **Audit Rule:** Cross-references assigned ICD-10 code definitions and clinical keywords against documented conditions. If conflict is detected (e.g. Hypertension documented but Diabetes code assigned), a **High Severity** mismatch flag is logged.
            - **Remediation:** Re-align code to documented condition after chart review.
            - **Citation:** *ICD-10-CM Official Guidelines for Coding and Reporting FY 2024, Section I.A.19.*
            """)

        with st.expander("3. Documentation Completeness & Clinician Authentication", expanded=True):
            st.markdown("""
            - **Objective:** Enforce Medicare Conditions of Payment regarding note sufficiency and clinician signature.
            - **Audit Rule:**
                - Notes under 15 words trigger an **Incomplete Documentation** flag.
                - Notes lacking standard electronic signatures/credentials (e.g., "Electronically signed by Dr. X, MD") trigger a **Missing Provider Signature** flag (Medium Severity).
            - **Remediation:** Route back to attending physician for completion and electronic attestation.
            - **Citation:** *CMS MLN Matters MM6698 & Medicare Program Integrity Manual Pub. 100-08.*
            """)

        with st.expander("4. Procedure Medical Necessity & Documentation Support", expanded=True):
            st.markdown("""
            - **Objective:** Guard against unsupported procedure billing and lack of medical necessity.
            - **Audit Rule:**
                - Invasive or diagnostic procedures (e.g. CPT 45378 Colonoscopy, CPT 71046 Chest X-ray, CPT 93000 ECG) must have explicit documentation of the service in the notes.
                - Primary diagnosis must justify procedure medical necessity (e.g. Colonoscopy requires colorectal screening or GI indication, not Pharyngitis).
            - **Remediation:** Obtain missing procedure report or remove unperformed service.
            - **Citation:** *Social Security Act §1862(a)(1)(A) & CMS Pub 100-02 Chapter 15 §20.*
            """)

        with st.expander("5. High-Level Evaluation & Management (E/M) Substantiation", expanded=True):
            st.markdown("""
            - **Objective:** Mitigate high-risk overcoding of Level 5 E/M encounters (CPT 99215 / 99205).
            - **Audit Rule:** High-level E/M visits require evidence of high Medical Decision Making (MDM) complexity or documented total encounter time (40-54 minutes for 99215). Routine complaints or terse notes billed as Level 5 trigger a **High Severity** flag.
            - **Remediation:** Downcode to supported E/M level (e.g. 99213/99214) or request physician documentation of complexity.
            - **Citation:** *AMA CPT 2024 E/M Guidelines & CMS 2021/2023 Outpatient E/M Documentation Revisions.*
            """)

        with st.expander("6. Specificity Optimization (Unspecified Code Warnings)", expanded=True):
            st.markdown("""
            - **Objective:** Encourage coding to highest level of specificity supported by the medical record.
            - **Audit Rule:** If an unspecified code (e.g. M17.9 Knee Osteoarthritis Unspecified) is billed, but clinical notes document laterality (e.g. Right knee), a **Low Severity** warning is generated suggesting specific alternative codes (e.g. M17.11).
            - **Remediation:** Update code to specify anatomical site.
            - **Citation:** *ICD-10-CM Official Guidelines Section I.B.18.*
            """)

        with st.expander("7. Duplicate Diagnosis Suppression", expanded=True):
            st.markdown("""
            - **Objective:** Eliminate redundant diagnosis codes on identical encounter dates.
            - **Audit Rule:** Scans for identical ICD-10 codes billed on the same encounter (e.g. I10; I10).
            - **Remediation:** Consolidate duplicate claim lines.
            - **Citation:** *CMS Claims Processing Manual Pub. 100-04 Chapter 23 §10.*
            """)


if __name__ == "__main__":
    main()
