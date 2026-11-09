"""Week 3: Billing Query Resolution and Error Analysis - Streamlit Interactive Application.

An educational medical billing simulation dashboard providing comprehensive error
detection, root cause analysis, query resolution workflows, preventive controls,
and financial reconciliation for fictional outpatient billing scenarios.

Educational Disclosure:
Curated historical FY 2024 ICD-10-CM and CPT 2024 references are utilized.
All patient records, encounters, and financial parameters are synthetic.
"""

from __future__ import annotations
import io
import os
import sys
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Ensure repository root and week3 root are on sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

WEEK3_ROOT = os.path.abspath(os.path.dirname(__file__))
if WEEK3_ROOT not in sys.path:
    sys.path.insert(0, WEEK3_ROOT)

from week3.src.workflow import BillingResolutionWorkflow
from week3.src.report_generator import BillingResolutionReportGenerator
from week3.src.visualizer import generate_resolution_flowchart
from week3.src.models import ErrorSeverity, ResolutionStatus


# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Week 3 – Billing Query Resolution & Error Analysis",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Healthcare Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background-color: #F8FAFC;
        border-radius: 8px;
        padding: 18px;
        border-left: 5px solid #1E3A8A;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .kpi-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0F172A;
        margin-top: 4px;
    }
    .callout-box {
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
        padding: 14px 18px;
        border-radius: 6px;
        margin: 12px 0;
        font-size: 0.95rem;
        color: #1E3A8A;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# DATA CACHING & PIPELINE EXECUTION
# -----------------------------------------------------------------------------

@st.cache_data(show_spinner=False)
def load_and_execute_simulation():
    """Execute the complete billing query resolution simulation and cache results."""
    workflow = BillingResolutionWorkflow(data_dir=os.path.join(WEEK3_ROOT, "data"))
    scenarios, findings, rcas, resolutions, controls, metrics = workflow.run_simulation()
    return scenarios, findings, rcas, resolutions, controls, metrics


scenarios, findings, rcas, resolutions, controls, metrics = load_and_execute_simulation()
res_map = {r.scenario_id: r for r in resolutions}
rca_map = {r.scenario_id: r for r in rcas}
ctrl_map = {c.error_code: c for c in controls}


# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------

st.sidebar.image("https://img.icons8.com/color/96/medical-history.png", width=64)
st.sidebar.title("Navigation")
st.sidebar.markdown("**Week 3: Query Resolution**")

pages = [
    "1. Executive Overview",
    "2. Scenario Explorer",
    "3. Error Detection Dashboard",
    "4. Root Cause Analysis",
    "5. Query Resolution Workbench",
    "6. Troubleshooting Guide",
    "7. Preventive Measures",
    "8. Financial Impact Analysis",
    "9. Final Reports & Downloads"
]

selected_page = st.sidebar.radio("Select View:", pages)

st.sidebar.markdown("---")
st.sidebar.caption("🩺 **Medical Billing Internship**")
st.sidebar.caption("Educational Simulation Project")
st.sidebar.caption("References: FY2024 ICD-10 & CPT 2024")
st.sidebar.caption("⚠️ *All patient & billing records are synthetic.*")


# -----------------------------------------------------------------------------
# PAGE 1: EXECUTIVE OVERVIEW
# -----------------------------------------------------------------------------

if selected_page == "1. Executive Overview":
    st.markdown('<div class="main-title">Billing Query Resolution & Error Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Executive Overview & Educational Simulation Cohort Analytics</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="callout-box">
    <strong>Educational Project Notice:</strong> This interactive application simulates end-to-end outpatient
    billing query resolution, claim error diagnostics, root cause classification, and preventive control design.
    All data is synthetic and complies with HIPAA de-identification standards. Code sets utilize historical
    curated FY 2024 ICD-10-CM and CPT 2024 reference subsets for educational demonstration purposes.
    </div>
    """, unsafe_allow_html=True)

    # Top KPI Metrics Cards
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Scenarios</div>
            <div class="kpi-value">{metrics.total_scenarios}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Errors Flagged</div>
            <div class="kpi-value" style="color: #DC2626;">{metrics.errors_identified_count}</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Compliant Cases</div>
            <div class="kpi-value" style="color: #059669;">{metrics.no_error_identified_count}</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Clean Resolution</div>
            <div class="kpi-value" style="color: #2563EB;">{metrics.clean_resolution_rate}%</div>
        </div>
        """, unsafe_allow_html=True)
    with c5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Net Variance</div>
            <div class="kpi-value" style="color: #9333EA;">${metrics.total_financial_variance:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Visual Analytics Row
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Billing Error Severity Distribution")
        fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)
        sev_data = metrics.severity_counts
        colors = {"Critical": "#EF4444", "High": "#F97316", "Medium": "#FBBF24", "Low": "#10B981"}
        bar_colors = [colors.get(k, "#94A3B8") for k in sev_data.keys()]
        bars = ax.bar(sev_data.keys(), sev_data.values(), color=bar_colors, edgecolor="#334155", linewidth=0.8)
        ax.set_ylabel("Scenario Count", fontsize=10, fontweight="bold")
        ax.set_ylim(0, max(sev_data.values()) + 2)
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        for b in bars:
            height = b.get_height()
            ax.annotate(f"{int(height)}", xy=(b.get_x() + b.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points", ha="center", va="bottom",
                        fontweight="bold", fontsize=10)
        plt.tight_layout()
        st.pyplot(fig)

    with col_chart2:
        st.subheader("Resolution Outcome Distribution")
        fig2, ax2 = plt.subplots(figsize=(6, 3.5), dpi=100)
        status_data = metrics.status_counts
        labels = [s.replace("Resolved – ", "Resolved:\n").replace("Pending ", "Pending:\n") for s in status_data.keys()]
        ax2.pie(
            status_data.values(),
            labels=labels,
            autopct="%1.1f%%",
            startangle=140,
            colors=["#3B82F6", "#10B981", "#F59E0B", "#8B5CF6"],
            textprops={"fontsize": 9}
        )
        ax2.axis("equal")
        plt.tight_layout()
        st.pyplot(fig2)

    st.markdown("---")
    st.subheader("Simulation Operational Summary")
    st.write(
        f"This simulation analyzed **{metrics.total_scenarios} outpatient encounters** across commercial PPO, HMO, and Medicare Part B coverage. "
        f"Of these, **{metrics.resolved_claims_count} claims were successfully corrected and released**, **{metrics.pending_query_count} queries "
        f"remain pending provider or external document response**, and **{metrics.no_error_identified_count} case was verified fully compliant** upon audit review. "
        f"The gross original billed amount across the cohort was **${metrics.total_original_gross_billed:,.2f}**, which adjusted to **${metrics.total_corrected_gross_billed:,.2f}** "
        f"following query resolution, yielding an exact net financial variance of **${metrics.total_financial_variance:,.2f}**."
    )


# -----------------------------------------------------------------------------
# PAGE 2: SCENARIO EXPLORER
# -----------------------------------------------------------------------------

elif selected_page == "2. Scenario Explorer":
    st.markdown('<div class="main-title">Billing Scenario Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Detailed Inspection of 18 Fictional Patient Billing Encounters</div>', unsafe_allow_html=True)

    scenario_options = [f"{s.scenario_id} – {s.patient_name} ({s.error_category})" for s in scenarios]
    selected_idx = st.selectbox("Select Scenario to Inspect:", range(len(scenario_options)), format_func=lambda i: scenario_options[i])
    s = scenarios[selected_idx]

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown(f"**Scenario ID:** `{s.scenario_id}`")
        st.markdown(f"**Encounter ID:** `{s.encounter_id}`")
        st.markdown(f"**Date of Service:** `{s.date_of_service}`")
    with col2:
        st.markdown(f"**Patient:** {s.patient_name} (ID: `{s.patient_id}`)")
        st.markdown(f"**Demographics:** {s.patient_age} yo {s.patient_gender}")
        st.markdown(f"**Payer:** {s.payer_name} ({s.plan_type})")
    with col3:
        st.markdown(f"**Error Category:** `{s.error_category}`")
        st.markdown(f"**Severity:** `{s.error_severity.value}`")
        st.markdown(f"**Status:** `{s.final_status.value}`")

    st.markdown("---")

    col_doc, col_code = st.columns([3, 2])
    with col_doc:
        st.subheader("Clinical Progress Note Narrative")
        st.info(s.clinical_documentation)
        st.markdown(f"**Billing Query / Audit Flag:**")
        st.warning(s.billing_query)

    with col_code:
        st.subheader("Coding & Financial Comparison")
        st.table(pd.DataFrame({
            "Metric": ["Primary ICD-10", "Billed CPT", "Gross Billed", "Provider Signature", "Prior Auth / Referral", "Units Billed"],
            "Original Value": [s.original_icd10, s.original_cpt, f"${s.original_billed_amount:,.2f}", str(s.has_provider_signature), str(s.has_prior_authorization), str(s.units_billed)],
            "Corrected Value": [s.corrected_icd10, s.corrected_cpt, f"${s.corrected_billed_amount:,.2f}", "Verified Authenticated" if not s.has_provider_signature else "True", "Obtained / N/A" if not s.has_prior_authorization else "True", "1" if s.units_billed > 1 else str(s.units_billed)]
        }))
        if s.variance_amount != 0.0:
            st.metric("Net Financial Variance", f"${s.variance_amount:,.2f}", delta=f"{s.variance_amount:,.2f}")
        else:
            st.metric("Net Financial Variance", "$0.00", delta="Balanced (No Charge Shift)")


# -----------------------------------------------------------------------------
# PAGE 3: ERROR DETECTION DASHBOARD
# -----------------------------------------------------------------------------

elif selected_page == "3. Error Detection Dashboard":
    st.markdown('<div class="main-title">Error Detection & Pre-Bill Audit Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Automated Rule Engine Flagging Discrepancies and Compliance Risks</div>', unsafe_allow_html=True)

    # Filter controls
    f_sev = st.multiselect("Filter by Severity:", [e.value for e in ErrorSeverity], default=[e.value for e in ErrorSeverity])

    filtered_findings = [f for f in findings if f.severity.value in f_sev]

    st.subheader(f"Active Audit Findings ({len(filtered_findings)} Total Flags)")

    table_data = []
    for f in filtered_findings:
        table_data.append({
            "Finding ID": f.finding_id,
            "Scenario": f.scenario_id,
            "Encounter": f.encounter_id,
            "Error Code": f.error_code,
            "Error Name": f.error_name,
            "Severity": f.severity.value,
            "Human Review Req.": "Yes" if f.manual_review_required else "No",
            "Confirmed Error": "Yes" if f.is_confirmed_error else "Audit Query (Compliant)"
        })

    st.dataframe(pd.DataFrame(table_data), use_container_width=True)

    st.markdown("---")
    st.subheader("Finding Detail Inspector")
    sel_fnd_id = st.selectbox("Select Finding to Inspect:", [f.finding_id for f in filtered_findings])
    sel_fnd = next((f for f in filtered_findings if f.finding_id == sel_fnd_id), None)

    if sel_fnd:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Finding Name:** {sel_fnd.error_name}")
            st.markdown(f"**Evidence Identified in Record:**")
            st.info(sel_fnd.evidence)
        with c2:
            st.markdown(f"**Compliance Reason Flagged:**")
            st.warning(sel_fnd.reason_flagged)
            st.markdown(f"**Recommended Clinical / Billing Action:**")
            st.success(sel_fnd.recommended_action)


# -----------------------------------------------------------------------------
# PAGE 4: ROOT CAUSE ANALYSIS
# -----------------------------------------------------------------------------

elif selected_page == "4. Root Cause Analysis":
    st.markdown('<div class="main-title">Root Cause Analysis (RCA)</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Systemic Breakdown across Revenue Cycle Workflow Stages</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])

    with c1:
        st.subheader("Root Cause Operational Categories")
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        rca_counts = metrics.root_cause_counts
        sorted_rca = dict(sorted(rca_counts.items(), key=lambda item: item[1], reverse=True))
        bars = ax.barh(list(sorted_rca.keys()), list(sorted_rca.values()), color="#4F46E5", edgecolor="#312E81")
        ax.set_xlabel("Occurrences", fontsize=10, fontweight="bold")
        ax.grid(axis="x", linestyle="--", alpha=0.3)
        for b in bars:
            width = b.get_width()
            ax.annotate(f"{int(width)}", xy=(width, b.get_y() + b.get_height() / 2),
                        xytext=(3, 0), textcoords="offset points", ha="left", va="center",
                        fontweight="bold", fontsize=9)
        plt.tight_layout()
        st.pyplot(fig)

    with c2:
        st.subheader("Error Classification Taxonomy")
        st.markdown("""
        Our investigation categorizes root causes into 5 operational domains:
        - **Front-End Registration & Scheduling:** Demographic typos, minor subscriber misallocations, and HMO PCP referral lapses.
        - **Clinical Documentation:** Unsigned draft notes and omitted procedure documentation for billed surgical codes.
        - **Medical Coding & Charge Capture:** Acute vs. chronic code confusion, specificity under-coding, and E/M upcoding macros.
        - **Billing & Claim Scrubbing:** Missing Modifier -25 on dual-service visits, duplicate charge lines, and MUE unit exceedance.
        - **Technical & Clearinghouse Integration:** Unmapped provider NPIs causing EDI 837P syntax rejections.
        """)
        st.info("💡 **Key Finding:** Over 60% of billing errors originated in front-end intake and clinical documentation prior to claim creation.")

    st.markdown("---")
    st.subheader("Comprehensive RCA Log")
    rca_table = []
    for r in rcas:
        rca_table.append({
            "Scenario": r.scenario_id,
            "Primary Root Cause Category": r.primary_category.value,
            "Operational Stage": r.operational_stage,
            "Underlying Cause Narrative": r.underlying_cause,
            "Financial Risk": r.financial_risk
        })
    st.dataframe(pd.DataFrame(rca_table), use_container_width=True)


# -----------------------------------------------------------------------------
# PAGE 5: QUERY RESOLUTION WORKBENCH
# -----------------------------------------------------------------------------

elif selected_page == "5. Query Resolution Workbench":
    st.markdown('<div class="main-title">Query Resolution Workbench</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Step-by-Step Resolution Roadmap & Stakeholder Communications</div>', unsafe_allow_html=True)

    scenario_options = [f"{s.scenario_id} – {s.error_category} ({s.final_status.value})" for s in scenarios]
    sel_idx = st.selectbox("Select Active Query to Resolve:", range(len(scenario_options)), format_func=lambda i: scenario_options[i])
    s = scenarios[sel_idx]
    r = res_map[s.scenario_id]

    col_meta1, col_meta2, col_meta3 = st.columns(3)
    with col_meta1:
        st.markdown(f"**Query ID:** `{r.query_id}`")
        st.markdown(f"**Encounter ID:** `{r.encounter_id}`")
    with col_meta2:
        st.markdown(f"**Claim Action Required:** `{r.claim_action}`")
        st.markdown(f"**Resolution Status:** `{r.final_status.value}`")
    with col_meta3:
        st.markdown(f"**Financial Impact:** `{r.financial_reconciliation}`")

    st.markdown("---")

    col_steps, col_comm = st.columns([3, 2])
    with col_steps:
        st.subheader("Standard Operating Procedure (SOP) Roadmap")
        for step in r.resolution_steps:
            st.markdown(f"- {step}")

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Required Supporting Evidence")
        for ev in r.required_evidence:
            st.markdown(f"- ✅ `{ev}`")

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Claim Validation Checks")
        for chk in r.validation_checks:
            st.markdown(f"- 🔍 `{chk}`")

    with col_comm:
        st.subheader("Stakeholder Communication")
        if r.provider_payer_communication:
            st.markdown("**Written Communication / Appeal Text:**")
            st.info(r.provider_payer_communication)


# -----------------------------------------------------------------------------
# PAGE 6: TROUBLESHOOTING GUIDE
# -----------------------------------------------------------------------------

elif selected_page == "6. Troubleshooting Guide":
    st.markdown('<div class="main-title">Billing Staff Troubleshooting Guide</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Standardized Operational Troubleshooting for Common Revenue Cycle Bottlenecks</div>', unsafe_allow_html=True)

    denial_types = [
        "1. Unauthenticated Records & Missing Provider Signature",
        "2. Duplicate Claim Submissions (CARC 18)",
        "3. Evaluation & Management (E/M) Downcoding & Level Selection",
        "4. Missing Prior Authorization / HMO Referral (CARC 197)",
        "5. Medical Necessity & Local Coverage Determinations (CARC 50)",
        "6. Technical Clearinghouse EDI Rejections (277CA STC A7)"
    ]

    selected_guide = st.selectbox("Select Denial / Query Category:", denial_types)

    if "1. Unauthenticated Records" in selected_guide:
        st.subheader("Missing Provider Signature Protocol")
        st.write("""
        - **Regulatory Basis:** Under Medicare Program Integrity Manual MLN MM6698, clinical services must be authenticated by the author before submission.
        - **Common Cause:** Clinician logs off EHR at end of shift with open draft progress notes.
        - **Actionable Steps:**
          1. Place billing pre-bill hold on encounter.
          2. Dispatch high-priority EHR inbox chart notification to rendering provider.
          3. Confirm clinician signs with cryptographic electronic timestamp.
          4. Release billing hold and submit clean claim.
        - **Preventive Control:** Implement EHR pre-bill hard stop preventing claim release if note status is 'Draft'.
        """)

    elif "2. Duplicate Claim Submissions" in selected_guide:
        st.subheader("Duplicate Procedure Billing (CARC 18) Protocol")
        st.write("""
        - **Regulatory Basis:** Submitting identical CPT codes for the same patient, date of service, and provider without modifier violates billing rules.
        - **Common Cause:** Duplicate charge entry or accidental rebilling of unacknowledged claims.
        - **Actionable Steps:**
          1. Inspect diagnostic test log and physician schedule to confirm if duplicate procedure was clinically executed.
          2. If duplicate is clerical, void the duplicate line item in billing ledger ($0.00 balance).
          3. If separate anatomical sites or sessions occurred, append Modifier 59 or XS/XP and provide documentation.
        - **Preventive Control:** Enable practice management pre-submission duplicate scrubber flagging identical CPT/DOS combinations.
        """)

    elif "3. Evaluation & Management" in selected_guide:
        st.subheader("E/M Complexity & MDM Scoring Protocol")
        st.write("""
        - **Regulatory Basis:** AMA/CMS 2021/2023 Outpatient E/M guidelines require leveling based on Medical Decision Making (MDM) or encounter duration.
        - **Common Cause:** Provider auto-selects Level 5 (CPT 99215) macro for straightforward or low-complexity conditions.
        - **Actionable Steps:**
          1. Evaluate documentation against the 3 MDM elements (Problems, Data, Risk).
          2. Level 5 requires 2 of 3 High components or 40-54 minutes face-to-face time.
          3. If unsupported, downcode to CPT 99213 or 99214 and adjust charge ledger before claim release.
        - **Preventive Control:** Integrate interactive MDM scoring calculators into EHR visit note templates.
        """)

    elif "4. Missing Prior Authorization" in selected_guide:
        st.subheader("HMO Gatekeeper Referral & Pre-Cert (CARC 197) Protocol")
        st.write("""
        - **Regulatory Basis:** Commercial HMO contracts mandate authorized PCP referral numbers prior to specialist consultations.
        - **Common Cause:** Patient scheduled directly without referral verification at check-in.
        - **Actionable Steps:**
          1. Contact referring primary care physician for retroactive referral authorization.
          2. Submit appeal with clinical documentation if medical emergency occurred.
          3. If payer upholds denial, apply contractual write-off; patient cannot be balance-billed per network contract.
        - **Preventive Control:** Enforce appointment scheduling hard-stops blocking check-in without an authorized referral number.
        """)

    elif "5. Medical Necessity" in selected_guide:
        st.subheader("Local Coverage Determination (LCD) Protocol")
        st.write("""
        - **Regulatory Basis:** Services must be reasonable and necessary for diagnosis or treatment under Social Security Act Section 1862(a)(1)(A).
        - **Common Cause:** Routine diagnostic imaging (e.g., chest X-ray) linked solely to uncomplicated hypertension (I10).
        - **Actionable Steps:**
          1. Review chart for unrecorded clinical symptoms (e.g., dyspnea, cough, abnormal lung sounds).
          2. Query clinician to determine if documentation can be augmented with clinical findings.
          3. If purely routine screening, remove procedure charge and bill E/M service only.
        - **Preventive Control:** Embed point-of-care Clinical Decision Support (CDS) in CPOE warning providers of LCD coverage gaps.
        """)

    elif "6. Technical Clearinghouse EDI" in selected_guide:
        st.subheader("Clearinghouse 277CA Syntax Rejection Protocol")
        st.write("""
        - **Regulatory Basis:** ANSI ASC X12N 837P requires valid Type 1 individual NPI in Box 24J/33a for rendering providers.
        - **Common Cause:** Software dictionary corruption or missing credentialing profile mapping following system updates.
        - **Actionable Steps:**
          1. Parse clearinghouse 277CA rejection STC A7 segment.
          2. Cross-reference rendering provider against NPPES registry.
          3. Update practice management billing dictionary with active NPI.
          4. Re-batch ANSI 837P claim file and transmit to clearinghouse.
        - **Preventive Control:** Establish automated EDI pre-batch validation verifying credentialing fields before file generation.
        """)


# -----------------------------------------------------------------------------
# PAGE 7: PREVENTIVE MEASURES
# -----------------------------------------------------------------------------

elif selected_page == "7. Preventive Measures":
    st.markdown('<div class="main-title">Preventive Measures & Compliance Controls</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Systemic Revenue Cycle Safeguards, EHR Hard-Stops, and Audit Schedules</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Departmental Governance & Responsibility")
        st.markdown("""
        - **Patient Registration & Scheduling:** Real-time eligibility (EDI 270/271), government ID scanning, and minor guarantor linkage.
        - **Clinical Providers:** Electronic signature compliance, comprehensive procedural documentation, and LCD decision support adherence.
        - **Health Information Management (HIM):** Certified coder review of acute vs. chronic pathology, E/M MDM validation, and specificity audits.
        - **Billing & Patient Accounts:** NCCI pre-bill claim scrubbing, MUE unit cross-checks, and waterfall patient-responsibility accounting.
        """)

    with col2:
        st.subheader("Recommended Audit Frequencies")
        st.markdown("""
        - **Pre-Bill Automated Scrubbing:** 100% of claims screened for NPI, signature, MUE, and NCCI edits prior to clearinghouse release.
        - **High-Risk Monthly Audits:** 100% sampling of Level 5 E/M (99215/99205), unlisted CPT codes, and high-dollar services.
        - **Random Quality Sampling:** 10 charts per provider per quarter reviewed by external or internal compliance auditors.
        - **Clearinghouse Rejection Reviews:** Daily morning triage of 277CA rejection reports to maintain AR days under 30.
        """)

    st.markdown("---")
    st.subheader("Preventive Controls Matrix")
    ctrl_table = []
    for c in controls:
        ctrl_table.append({
            "Error Code": c.error_code,
            "Preventive Policy Name": c.control_name,
            "Responsible Department": c.responsible_department,
            "Implementation Frequency": c.implementation_frequency,
            "EHR Hard-Stop Enforced": "Yes" if c.ehr_hard_stop else "No",
            "Expected Compliance Benefit": c.expected_benefit
        })
    st.dataframe(pd.DataFrame(ctrl_table), use_container_width=True)


# -----------------------------------------------------------------------------
# PAGE 8: FINANCIAL IMPACT ANALYSIS
# -----------------------------------------------------------------------------

elif selected_page == "8. Financial Impact Analysis":
    st.markdown('<div class="main-title">Financial Impact & Reconciliation Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Reconciliation of Chargemaster Billed Charges and Financial Variance</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Initial Gross Billed", f"${metrics.total_original_gross_billed:,.2f}")
    with c2:
        st.metric("Total Corrected Gross Billed", f"${metrics.total_corrected_gross_billed:,.2f}")
    with c3:
        st.metric("Net Financial Variance", f"${metrics.total_financial_variance:,.2f}", delta=f"{metrics.total_financial_variance:,.2f}")

    st.markdown("---")

    # Financial breakdown table
    st.subheader("Scenario-by-Scenario Financial Reconciliation")
    fin_data = []
    for s in scenarios:
        fin_data.append({
            "Scenario ID": s.scenario_id,
            "Patient Name": s.patient_name,
            "Payer": s.payer_name,
            "Error Category": s.error_category,
            "Initial Gross": f"${s.original_billed_amount:,.2f}",
            "Corrected Gross": f"${s.corrected_billed_amount:,.2f}",
            "Financial Variance": f"${s.variance_amount:,.2f}",
            "Status": s.final_status.value
        })
    st.dataframe(pd.DataFrame(fin_data), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Financial Variance Explanation")
    st.write("""
    Across the 18 scenarios, 6 encounters resulted in Chargemaster gross charge adjustments due to query resolution:
    - **SCN-3003 (-$35.00):** CPT 99385 ($240.00) corrected to established patient code CPT 99395 ($205.00).
    - **SCN-3004 (-$65.00):** Unsubstantiated skin biopsy CPT 11102 ($65.00) removed from claim.
    - **SCN-3005 (-$210.00):** Unsupported Level 5 E/M 99215 ($395.00) downcoded to Level 3 E/M 99213 ($185.00).
    - **SCN-3007 (-$220.00):** Non-covered screening chest X-ray CPT 71046 ($220.00) removed due to LCD policy gap.
    - **SCN-3011 (-$175.00):** Traumatic injury E/M charge adjusted from $360.00 to supported code $185.00.
    - **SCN-3013 (-$390.00):** IV hydration CPT 96360 corrected from 4 units ($520.00) to 1 unit ($130.00) per MUE limit.
    - **Total Net Variance:** -$35.00 + -$65.00 + -$210.00 + -$220.00 + -$175.00 + -$390.00 = **-$1,095.00**.
    """)


# -----------------------------------------------------------------------------
# PAGE 9: FINAL REPORTS & DOWNLOADS
# -----------------------------------------------------------------------------

elif selected_page == "9. Final Reports & Downloads":
    st.markdown('<div class="main-title">Final Deliverables & Report Downloads</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Access and Download All Compiled Internship Deliverables</div>', unsafe_allow_html=True)

    reports_dir = os.path.join(WEEK3_ROOT, "reports")
    docx_path = os.path.join(reports_dir, "Week_3_Billing_Query_Resolution_Report.docx")
    csv_path = os.path.join(reports_dir, "billing_error_analysis.csv")
    flowchart_path = os.path.join(reports_dir, "resolution_workflow.png")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader("📄 Formal Case Study Report")
        st.write("20-Section Comprehensive Academic Report (.docx)")
        if os.path.exists(docx_path):
            with open(docx_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download Word Report (.docx)",
                    data=f.read(),
                    file_name="Week_3_Billing_Query_Resolution_Report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
        else:
            st.warning("Report file not yet generated.")

    with c2:
        st.subheader("📊 Audit Findings Dataset")
        st.write("Comprehensive Scenario Resolution Log (.csv)")
        if os.path.exists(csv_path):
            with open(csv_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download Audit Findings (.csv)",
                    data=f.read(),
                    file_name="billing_error_analysis.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.warning("CSV dataset not yet generated.")

    with c3:
        st.subheader("🖼️ Workflow Diagram")
        st.write("300 DPI High-Resolution Flowchart (.png)")
        if os.path.exists(flowchart_path):
            with open(flowchart_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download Workflow Flowchart (.png)",
                    data=f.read(),
                    file_name="resolution_workflow.png",
                    mime="image/png",
                    use_container_width=True
                )
        else:
            st.warning("Flowchart not yet generated.")

    st.markdown("---")
    st.subheader("Embedded Workflow Diagram Preview")
    if os.path.exists(flowchart_path):
        st.image(flowchart_path, caption="Week 3: Billing Query Resolution Workflow (300 DPI)", use_container_width=True)
    else:
        st.info("Workflow image will appear here once generated.")
