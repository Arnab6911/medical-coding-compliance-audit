"""
Week 4 Interactive Streamlit Dashboard
Medical Billing Software Integration & Best Practices Implementation
Evergreen Valley Family Medicine & Multi-Specialty Clinic

11 Comprehensive Navigation Pages:
1. Executive Overview
2. Software Comparison
3. Integration Roadmap
4. System Architecture
5. Data Migration Planner
6. Real-Time Validation Framework
7. Best Practices
8. Staff Training Module
9. Risk Assessment
10. KPI Monitoring
11. Final Report Downloads
"""

import sys
import json
from pathlib import Path
import streamlit as st
import pandas as pd

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from week4.src.models import PracticeProfile
from week4.src.software_evaluator import SoftwareEvaluator
from week4.src.migration_engine import MigrationEngine
from week4.src.validation_rules import ValidationRuleEngine
from week4.src.risk_engine import RiskEngine
from week4.src.training_engine import TrainingEngine

DATA_DIR = Path(__file__).resolve().parent / "data"
REPORTS_DIR = Path(__file__).resolve().parent / "reports"

st.set_page_config(
    page_title="Week 4 - Billing Software Integration",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f2942;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.0rem;
        color: #475569;
        margin-bottom: 1.2rem;
    }
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .callout-box {
        background-color: #e0f2fe;
        border-left: 4px solid #0284c7;
        padding: 12px;
        border-radius: 4px;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Cache data loading
@st.cache_resource
def load_components():
    profile = PracticeProfile()
    evaluator = SoftwareEvaluator()
    migration = MigrationEngine()
    rules = ValidationRuleEngine()
    risks = RiskEngine()
    training = TrainingEngine()
    return profile, evaluator, migration, rules, risks, training

profile, evaluator, migration, rules_engine, risk_engine, training_engine = load_components()

# Sidebar Navigation
st.sidebar.title("🏥 Week 4 RCM Integration")
st.sidebar.markdown("**Medical Billing Internship**")
st.sidebar.caption("Student Project | Non-PHI Simulation")

pages = [
    "1. Executive Overview",
    "2. Software Comparison",
    "3. Integration Roadmap",
    "4. System Architecture",
    "5. Data Migration Planner",
    "6. Real-Time Validation Framework",
    "7. Best Practices",
    "8. Staff Training Module",
    "9. Risk Assessment",
    "10. KPI Monitoring",
    "11. Final Report Downloads"
]

selected_page = st.sidebar.radio("Navigate Sections:", pages)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Practice:** {profile.name}")
st.sidebar.markdown(f"**Scale:** {profile.provider_count} Providers | {profile.monthly_encounter_volume:,}/mo")
st.sidebar.markdown("**Evaluation Winner:** athenahealth athenaOne (9.22/10)")

# -------------------------------------------------------------
# PAGE 1: EXECUTIVE OVERVIEW
# -------------------------------------------------------------
if selected_page == "1. Executive Overview":
    st.markdown('<div class="main-header">Executive Overview & Case Study Scope</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Strategic Billing Software Integration & Revenue Cycle Modernization</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="callout-box">
    <strong>Academic Project Disclaimer:</strong> This application simulates the strategic evaluation, data migration,
    pre-bill validation, and risk mitigation required to integrate modern cloud billing software into an outpatient multi-specialty clinic.
    All encounter volumes, provider staffing, patient ledgers, and financial numbers are synthetic constructs.
    </div>
    """, unsafe_allow_html=True)

    # Top KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Clinical Providers", f"{profile.provider_count}", "Multi-Specialty")
    with col2:
        st.metric("Monthly Encounters", f"{profile.monthly_encounter_volume:,}", "36,000 / Year")
    with col3:
        st.metric("Initial Denial Rate", f"{profile.baseline_denial_rate}%", "Target: < 5.0%", delta_color="inverse")
    with col4:
        st.metric("Days in A/R", f"{profile.baseline_days_in_ar}", "Target: < 35.0 Days", delta_color="inverse")

    st.markdown("### Fictional Practice Profile: Evergreen Valley Multi-Specialty Clinic")
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.write(f"**Organization Type:** {profile.practice_type}")
        st.write(f"**Provider Breakdown:** {profile.providers_breakdown}")
        st.write(f"**Billing & HIM Workforce:** {profile.billing_staff_roles}")
        st.write(f"**Patient Access Staff:** {profile.front_desk_staff_count} Front-Desk Coordinators")
    with p_col2:
        st.write(f"**Legacy EHR Stack:** {profile.legacy_ehr_system}")
        st.write(f"**Legacy Billing Tool:** {profile.legacy_pm_system}")
        st.write(f"**Clearinghouse Pipeline:** {profile.clearinghouse_workflow}")
        st.write(f"**Baseline Submission Lag:** {profile.baseline_claim_submission_lag} Days")

    st.markdown("---")
    st.markdown("### Operational Gaps vs Future-State Vision")
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        st.error("**Current Operational Bottlenecks:**")
        for ch in profile.operational_challenges:
            st.markdown(f"- ❌ {ch}")
    with g_col2:
        st.success("**Proposed Future-State Capabilities:**")
        for fs in profile.proposed_future_state:
            st.markdown(f"- ✅ {fs}")

# -------------------------------------------------------------
# PAGE 2: SOFTWARE COMPARISON
# -------------------------------------------------------------
elif selected_page == "2. Software Comparison":
    st.markdown('<div class="main-header">Medical Billing Software Market Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Objective Feature-Based Assessment of athenahealth, AdvancedMD, and Tebra</div>', unsafe_allow_html=True)

    summary = evaluator.get_feature_matrix_summary()
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.info(f"**athenahealth athenaOne**\n\nVerified: {summary['athenahealth']['verified']} | Confirm: {summary['athenahealth']['requires_confirmation']}")
    with m_col2:
        st.info(f"**AdvancedMD**\n\nVerified: {summary['advancedmd']['verified']} | Confirm: {summary['advancedmd']['requires_confirmation']}")
    with m_col3:
        st.info(f"**Tebra (Kareo + PatientPop)**\n\nVerified: {summary['tebra']['verified']} | Confirm: {summary['tebra']['requires_confirmation']}")

    # Category Filter
    categories = sorted(list(set(f.category for f in evaluator.features)))
    selected_cat = st.selectbox("Filter by Functional Category:", ["All Categories"] + categories)

    filtered_features = evaluator.features if selected_cat == "All Categories" else [f for f in evaluator.features if f.category == selected_cat]

    df_data = []
    for f in filtered_features:
        df_data.append({
            "Feature ID": f.feature_id,
            "Dimension": f.feature_name,
            "Category": f.category,
            "athenahealth athenaOne": f"{f.athenahealth_capability}\n[{f.athenahealth_status}]",
            "AdvancedMD": f"{f.advancedmd_capability}\n[{f.advancedmd_status}]",
            "Tebra": f"{f.tebra_capability}\n[{f.tebra_status}]"
        })
    df_features = pd.DataFrame(df_data)
    st.dataframe(df_features, use_container_width=True, height=450)

    st.markdown("### Software Selection Scoring Matrix")
    eval_res = evaluator.calculate_scores()
    st.table(pd.DataFrame(eval_res["breakdown"])[["name", "weight_pct", "score_athena", "score_advancedmd", "score_tebra"]])
    st.success(f"**Recommended Vendor:** {eval_res['recommended_vendor']} (Score: {eval_res['recommended_score']:.2f} / 10.0)")

# -------------------------------------------------------------
# PAGE 3: INTEGRATION ROADMAP
# -------------------------------------------------------------
elif selected_page == "3. Integration Roadmap":
    st.markdown('<div class="main-header">12-Phase Implementation Roadmap</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Structured 24-Week Transition Methodology Across 4 Sequential Stages</div>', unsafe_allow_html=True)

    wf_img = REPORTS_DIR / "integration_workflow.png"
    if wf_img.exists():
        st.image(str(wf_img), use_container_width=True, caption="Figure: 12-Phase Implementation Methodology")

    st.markdown("### Phase-by-Phase Governance Details")
    stages = {
        "Stage 1: Evaluation & Design (Weeks 1-6)": [
            ("Phase 1: Requirements Gathering", "PM", "Gap analysis & stakeholder discovery", "Steering Committee Charter"),
            ("Phase 2: Vendor Evaluation & Selection", "Lead Architect", "Vendor RFP demos, pricing & BAA review", "Vendor contract executed"),
            ("Phase 3: Workflow Mapping & Config", "Clinical/Billing Leads", "Clinical templates, fee schedules & superbills", "Medical Director sign-off")
        ],
        "Stage 2: Technical Preparation & Migration (Weeks 7-14)": [
            ("Phase 4: Architecture & Interface Build", "Lead Architect", "FHIR REST APIs, X12 EDI pipelines (270/837/835)", "Sandbox connectivity pass"),
            ("Phase 5: Migration Data Preparation", "Migration Engineer", "ETL extraction scripts, cleansing & MPI deduplication", "Cleansing validation pass"),
            ("Phase 6: Data Migration & AR Reconciliation", "Billing Supervisor", "Test migration loads & open AR ledger trial balance", "100% census match & $0.00 variance")
        ],
        "Stage 3: Testing, Training & Pilot (Weeks 15-20)": [
            ("Phase 7: Pre-Bill Rules Configuration", "Lead Coder", "12 claim scrubber rules & NCCI/MUE edit tables", "Zero fatal bypass pass"),
            ("Phase 8: End-to-End System Testing", "Integration Engineer", "500-claim sandbox batch transmission & 835 check", "98%+ first-pass clean rate"),
            ("Phase 9: Role-Based Staff Training", "Training Lead", "5 role curricula delivery & competency testing", "100% staff score >= 85%")
        ],
        "Stage 4: Cutover & Optimization (Weeks 21-24+)": [
            ("Phase 10: Pilot Deployment", "Clinic Supervisor", "2-week live pilot in Cardiology specialty clinic", "Pilot denial rate < 6.0%"),
            ("Phase 11: Enterprise Cutover & Go-Live", "SteerCo / PM", "Scheduled cutover weekend & enterprise go-live", "Production 837P transmission"),
            ("Phase 12: Monitoring & Optimization", "Practice Manager", "Weekly KPI dashboards & denial root-cause triage", "DAR < 35.0 days & dollar-weighted denials <5.0% (target ceiling)")
        ]
    }

    for stg_name, phase_list in stages.items():
        with st.expander(stg_name, expanded=True):
            for p_title, p_role, p_deliv, p_gate in phase_list:
                st.markdown(f"**{p_title}** | *Lead:* {p_role}")
                st.markdown(f"- *Key Deliverables:* {p_deliv}")
                st.markdown(f"- *Gate Criteria:* {p_gate}")

# -------------------------------------------------------------
# PAGE 4: SYSTEM ARCHITECTURE
# -------------------------------------------------------------
elif selected_page == "4. System Architecture":
    st.markdown('<div class="main-header">Proposed Healthcare IT & RCM Architecture</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">7-Tier Cloud Continuum Connecting Clinical, Billing, EDI, and Executive Modules</div>', unsafe_allow_html=True)

    arch_img = REPORTS_DIR / "integration_architecture.png"
    if arch_img.exists():
        st.image(str(arch_img), use_container_width=True, caption="Figure: Proposed 7-Tier Cloud System Architecture (300 DPI)")

    st.markdown("### Architectural Tiers Breakdown")
    colA, colB = st.columns(2)
    with colA:
        with st.expander("Tier 1: Patient Access & Intake", expanded=True):
            st.write("Digital check-in, demographic capture, MPI deduplication, automated 270 eligibility checks, and point-of-service copay collections.")
        with colB:
            with st.expander("Tier 2: Clinical EHR Documentation", expanded=True):
                st.write("Structured progress notes, applicable MDM/time E/M code selection (verified by date of service and authorized CPT guidance), electronic superbill creation, and mandatory 24h physician electronic signatures.")

    colC, colD = st.columns(2)
    with colC:
        with st.expander("Tier 3: Pre-Bill Rules Scrubber", expanded=True):
            st.write("Hard-stop gating for missing notes/NPIs/deleted codes, NCCI procedure-to-procedure unbundling, and warning queues for human coder audit.")
        with colD:
            with st.expander("Tier 4: Practice Management Core", expanded=True):
                st.write("Fee schedules, unbilled encounter staging, secondary crossover queues, and open accounts receivable ledgers.")

    colE, colF = st.columns(2)
    with colE:
        with st.expander("Tier 5: Integrated Clearinghouse & EDI", expanded=True):
            st.write("Automated 837P claim dispatch, 999 acknowledgments, 277CA acceptance tracking, and ingestion of 835 Remittance Advices.")
        with colF:
            with st.expander("Tier 6: Payment Posting & Patient Accounting", expanded=True):
                st.write("Automated 835 remittance matching, contractual write-offs, electronic patient statements, and online payment portal.")

    with st.expander("Tier 7: Executive RCM Analytics & Compliance Foundation", expanded=True):
        st.write("11 real-time KPIs, denial root-cause tracking by CARC/RARC, proposed technical safeguards (TLS 1.3 / AES-256 aligned with HIPAA Security Rule specifications), and proposed immutable security audit logs supporting HIPAA Security Rule audit-control requirements.")

# -------------------------------------------------------------
# PAGE 5: DATA MIGRATION PLANNER
# -------------------------------------------------------------
elif selected_page == "5. Data Migration Planner":
    st.markdown('<div class="main-header">Data Migration & Financial Reconciliation</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">ETL Protocol, Cleansing, MPI Deduplication & $0.00 Variance Verification (Synthetic Test Dataset)</div>', unsafe_allow_html=True)

    rec = migration.reconcile_financials()
    val = migration.run_validation()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Migrated Accounts", f"{rec['total_account_count']}")
    with col2:
        st.metric("Legacy AR Balance", f"${rec['total_legacy_ar']:,.2f}")
    with col3:
        st.metric("Migrated AR Balance", f"${rec['total_migrated_ar']:,.2f}")
    with col4:
        st.metric("Reconciliation Variance", f"${rec['net_variance']:,.2f}", "100.0% Match")

    st.markdown("### Master Patient Index (MPI) Deduplication Engine")
    duplicates = migration.detect_duplicates()
    if duplicates:
        st.warning(f"**Potential Duplicate Accounts Detected:** {len(duplicates)}")
        for d in duplicates:
            st.markdown(f"- **Primary Account:** `{d['primary_id']}` ({d['primary_name']}) ↔ **Duplicate Chart:** `{d['duplicate_id']}` ({d['duplicate_name']})")
            st.markdown(f"  *Match Factors:* {', '.join([r for r in d['match_reasons'] if r])} | *Action:* {d['resolution']}")

    st.markdown("### Synthetic Migration Records Explorer")
    status_filter = st.selectbox("Filter by Record Migration Status:", ["All Records"] + list(set(r.migration_status for r in migration.records)))
    
    table_data = []
    for r in migration.records:
        if status_filter == "All Records" or r.migration_status == status_filter:
            table_data.append({
                "Patient ID": r.legacy_patient_id,
                "Name": f"{r.first_name} {r.last_name}",
                "DOB": r.dob,
                "Payer": r.primary_payer,
                "Legacy AR": f"${r.legacy_ar_balance:,.2f}",
                "Migrated AR": f"${r.migrated_ar_balance:,.2f}",
                "Variance": f"${r.variance:,.2f}",
                "Status": r.migration_status,
                "Cleansing Notes": r.reconciliation_notes
            })
    st.dataframe(pd.DataFrame(table_data), use_container_width=True)

# -------------------------------------------------------------
# PAGE 6: REAL-TIME VALIDATION FRAMEWORK
# -------------------------------------------------------------
elif selected_page == "6. Real-Time Validation Framework":
    st.markdown('<div class="main-header">Real-Time Pre-Bill Claim Validation Framework</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">12-Rule Claim Scrubbing Engine with Hard-Stops & Annual Code Governance</div>', unsafe_allow_html=True)

    rules_by_sev = rules_engine.get_rules_by_severity()
    c1, c2 = st.columns(2)
    with c1:
        st.error(f"**HARD-STOP Fatal Edit Rules:** {len(rules_by_sev['HARD_STOP'])}")
        st.caption("Blocks electronic claim generation until rectified; zero transmission of non-compliant claims.")
    with c2:
        st.warning(f"**WARNING / Clinical Audit Rules:** {len(rules_by_sev['WARNING'])}")
        st.caption("Routes encounter to certified coder queue for clinical record review and non-leading queries.")

    sev_filter = st.radio("Filter Rules by Severity:", ["All Severities", "HARD_STOP", "WARNING"], horizontal=True)
    filtered_rules = rules_engine.rules if sev_filter == "All Severities" else [r for r in rules_engine.rules if r.severity == sev_filter]

    for r in filtered_rules:
        with st.expander(f"{r.rule_id}: {r.rule_name} [{r.severity}]", expanded=(r.severity == "HARD_STOP")):
            st.write(f"**Category:** {r.category}")
            st.write(f"**Trigger Condition:** {r.trigger_condition}")
            st.write(f"**Resolution Protocol:** {r.resolution_guidance}")
            if r.code_governance_type:
                st.info(f"**Code Governance Standard:** {r.code_governance_type}")

    st.markdown("---")
    st.markdown("### Annual Code Set Release Governance")
    schedules = rules_engine.get_code_governance_schedule()
    for s in schedules:
        st.markdown(f"**{s['cycle']}** (Effective: `{s['effective_date']}`)")
        st.markdown(f"- *Governance Window:* {s['governance_window']}")
        st.markdown(f"- *Risk Controls:* {s['risk_controls']}")

# -------------------------------------------------------------
# PAGE 7: BEST PRACTICES
# -------------------------------------------------------------
elif selected_page == "7. Best Practices":
    st.markdown('<div class="main-header">Revenue Cycle Best Practices Guide</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Operational Principles Across Front-Desk, Clinical, Coding, and Billing Teams</div>', unsafe_allow_html=True)

    bp = [
        ("1. Front-Desk Patient Access", "Automated 72h/24h 270 eligibility batching, card scanning, POS copay collection, and duplicate check-in checks."),
        ("2. Clinical Documentation Integrity", "Structured outpatient charting templates, E/M MDM justification, and mandatory 24-hour electronic signature compliance."),
        ("3. Certified Coding Oversight", "Human-in-the-loop audit for high-level E/M (99205/99215), modifier -25 usage, and non-leading provider queries."),
        ("4. Pre-Bill Claim Scrubbing", "Zero tolerance for bypassing hard-stop errors; daily clearinghouse reject work queue triage under 24 hours."),
        ("5. Denial Management & Appeals", "Automated CARC/RARC categorization, 48-hour appeal package dispatch, and monthly provider denial root-cause feedback."),
        ("6. Patient Financial Experience", "Itemized electronic billing statements, self-service patient portal payments, and transparent payment installment agreements.")
    ]
    for title, desc in bp:
        with st.expander(title, expanded=True):
            st.markdown(desc)

# -------------------------------------------------------------
# PAGE 8: STAFF TRAINING MODULE
# -------------------------------------------------------------
elif selected_page == "8. Staff Training Module":
    st.markdown('<div class="main-header">Staff Training Program & Competency Assessment</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">46-Hour Role-Based Curriculum & 10-Question Knowledge Evaluation (85% Passing Threshold)</div>', unsafe_allow_html=True)

    t_sum = training_engine.get_summary()
    st.info(f"**Curriculum:** {t_sum['title']} | **Total Hours:** {t_sum['total_training_hours']:.1f} hrs across {t_sum['total_modules']} specialized modules.")

    tab1, tab2 = st.tabs(["Role-Based Curriculum Outlines", "Interactive Knowledge Assessment"])

    with tab1:
        for m in training_engine.modules:
            with st.expander(f"{m.module_id}: {m.title} ({m.duration_hours:.1f} hrs) - {m.target_role}", expanded=False):
                st.write("**Core Learning Objectives:**")
                for obj in m.learning_objectives:
                    st.write(f"- {obj}")
                st.write("**Practical Hands-On Exercises:**")
                for ex in m.practical_exercises:
                    st.write(f"- {ex}")

    with tab2:
        st.markdown("### Interactive 10-Question Staff Assessment")
        st.write("Test staff competency across registration, coding, claims, and compliance. Select responses below and submit for scoring:")

        user_answers = {}
        for idx, q in enumerate(training_engine.questions):
            st.markdown(f"**{q.question_id}: {q.question}** ({q.target_role})")
            user_answers[q.question_id] = st.radio(
                f"Options for {q.question_id}:",
                options=list(range(len(q.options))),
                format_func=lambda i, opts=q.options: f"[{i+1}] {opts[i]}",
                key=f"assess_{q.question_id}"
            )
            st.write("")

        if st.button("Submit Assessment & Evaluate Competency"):
            eval_res = training_engine.evaluate_answers(user_answers)
            score = eval_res["score_percent"]
            passed = eval_res["passed"]
            
            if passed:
                st.success(f"🎉 **Assessment Passed! Score: {score}%** ({eval_res['correct_count']} of {eval_res['total_questions']} correct). Passing threshold: {eval_res['passing_grade_percent']}%.")
            else:
                st.error(f"❌ **Assessment Failed. Score: {score}%** ({eval_res['correct_count']} of {eval_res['total_questions']} correct). Passing threshold is {eval_res['passing_grade_percent']}%. Remediation training required.")

            st.markdown("#### Question-by-Question Feedback & Explanations:")
            for fb in eval_res["feedback"]:
                status_icon = "✅" if fb["is_correct"] else "❌"
                with st.expander(f"{status_icon} {fb['question_id']}: Correct Answer: Option [{fb['correct_option_index']+1}]"):
                    st.write(f"**Selected:** Option [{fb['selected_option_index']+1}] - {fb['selected_option_text']}")
                    st.write(f"**Operational Explanation:** {fb['explanation']}")
                    st.write(f"**Guideline Citation:** {fb['guideline_reference']}")

# -------------------------------------------------------------
# PAGE 9: RISK ASSESSMENT
# -------------------------------------------------------------
elif selected_page == "9. Risk Assessment":
    st.markdown('<div class="main-header">Integration Risk Assessment & Mitigation</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">5x5 Likelihood x Impact Heatmap & 12 Managed Operational Risks</div>', unsafe_allow_html=True)

    risk_img = REPORTS_DIR / "risk_assessment_matrix.png"
    if risk_img.exists():
        st.image(str(risk_img), use_container_width=True, caption="Figure: 5x5 Likelihood vs Consequence Risk Heatmap (300 DPI)")

    r_sum = risk_engine.get_summary_metrics()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Risks Evaluated", f"{r_sum['total_risks']}")
    with c2:
        st.metric("Average Risk Score", f"{r_sum['average_risk_score']} / 25")
    with c3:
        st.metric("Critical Risks", f"{r_sum['distribution_by_level']['Critical']}", "Immediate Mitigation")
    with c4:
        st.metric("High Risks", f"{r_sum['distribution_by_level']['High']}", "Active Management")

    st.markdown("### Risk Register Explorer")
    cat_filter = st.selectbox("Filter by Category:", ["All Categories"] + list(set(r.category for r in risk_engine.risks)))
    filtered_risks = risk_engine.risks if cat_filter == "All Categories" else [r for r in risk_engine.risks if r.category == cat_filter]

    r_table = []
    for r in filtered_risks:
        r_table.append({
            "Risk ID": r.risk_id,
            "Title": r.title,
            "Category": r.category,
            "Likelihood": r.likelihood,
            "Impact": r.impact,
            "Score": r.risk_score,
            "Level": r.risk_level,
            "Mitigation": r.mitigation_strategy,
            "Contingency": r.contingency_plan,
            "Owner": r.owner_role
        })
    st.dataframe(pd.DataFrame(r_table), use_container_width=True)

# -------------------------------------------------------------
# PAGE 10: KPI MONITORING
# -------------------------------------------------------------
elif selected_page == "10. KPI Monitoring":
    st.markdown('<div class="main-header">Revenue Cycle KPI Monitoring Framework</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">11 Core RCM Metrics, Formulas, Baselines, and Post-Go-Live Targets</div>', unsafe_allow_html=True)

    with open(DATA_DIR / "kpi_definitions.json", "r", encoding="utf-8") as f:
        kpi_list = json.load(f)

    for k in kpi_list:
        with st.expander(f"{k['kpi_id']}: {k['name']} [{k['category']}]", expanded=False):
            c1, c2, c3 = st.columns(3)
            with c1:
                base_disp = f"{k['baseline_value']} {k['unit']}" if isinstance(k['baseline_value'], (int, float)) else str(k['baseline_value'])
                st.metric("Baseline Value", base_disp)
            with c2:
                tgt_disp = k.get("target_display", f"{k['target_value']} {k['unit']}" if isinstance(k['target_value'], (int, float)) else str(k['target_value']))
                st.metric("Project Target", tgt_disp)
            with c3:
                st.write(f"**Frequency:** {k['measurement_frequency']}")
                st.write(f"**Status:** {k['status_target']}")
            st.write(f"**Mathematical Formula:** `{k['formula']}`")
            st.write(f"**Operational Impact:** {k['operational_impact']}")

# -------------------------------------------------------------
# PAGE 11: FINAL REPORT DOWNLOADS
# -------------------------------------------------------------
elif selected_page == "11. Final Report Downloads":
    st.markdown('<div class="main-header">Final Report & Asset Downloads</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Access Official Word Audit Report, Datasets, and 300 DPI Architectural Diagrams</div>', unsafe_allow_html=True)

    docx_path = REPORTS_DIR / "Week_4_Billing_Software_Integration_Report.docx"
    if docx_path.exists():
        with open(docx_path, "rb") as f:
            st.download_button(
                label="📄 Download Full 21-Section Word Report (.docx)",
                data=f.read(),
                file_name="Week_4_Billing_Software_Integration_Report.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        st.success(f"Verified Word Document Available: `{docx_path}` ({docx_path.stat().st_size / (1024*1024):.2f} MB)")
    else:
        st.error("Word report file not found. Run `python week4/generate_reports.py` to compile.")

    st.markdown("### Export Reference Datasets & High-Resolution Diagrams")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv_comp = DATA_DIR / "software_comparison.csv"
        if csv_comp.exists():
            with open(csv_comp, "rb") as f:
                st.download_button("📊 Download Software Comparison (CSV)", f.read(), "software_comparison.csv", "text/csv")

    with col2:
        csv_risk = DATA_DIR / "risk_register.csv"
        if csv_risk.exists():
            with open(csv_risk, "rb") as f:
                st.download_button("⚠️ Download Risk Register (CSV)", f.read(), "risk_register.csv", "text/csv")

    with col3:
        csv_mig = DATA_DIR / "migration_sample.csv"
        if csv_mig.exists():
            with open(csv_mig, "rb") as f:
                st.download_button("🔄 Download Migration Sample (CSV)", f.read(), "migration_sample.csv", "text/csv")
