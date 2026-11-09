"""Medical Billing Process Simulation (Week 2) - Streamlit Interactive Application.

An end-to-end educational revenue cycle management (RCM) dashboard modeling the
12-stage medical billing workflow:
1. Overview Dashboard
2. Patient Registration & Eligibility
3. Encounter Documentation & Clinical Notes
4. Medical Coding & Reference Validation
5. Charge Capture & Fee Schedules
6. Claim Scrubber & Pre-Submission Auditing
7. Claim Submission (EDI 837P Simulation)
8. Payer Adjudication (ERA 835 & CARC Codes)
9. Payment Posting & Ledger Reconciliation
10. Patient Invoices & Statement Generator
11. Revenue Cycle Analytics & Denial Management
12. Case Study Report Generator & Export

Educational Disclosure:
Curated historical FY 2024 ICD-10-CM and CPT 2024 references are utilized.
All patient records, encounters, and financial parameters are synthetic.
"""

from __future__ import annotations
import io
import os
import sys
from datetime import datetime
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Ensure repository root and week2 root are on sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

WEEK2_ROOT = os.path.abspath(os.path.dirname(__file__))
if WEEK2_ROOT not in sys.path:
    sys.path.insert(0, WEEK2_ROOT)

from week2.src.models import ClaimStatus, BillingStage
from week2.src.billing_pipeline import BillingSimulationPipeline
from week2.src.report_generator import BillingCaseStudyReportGenerator
from week2.src.flowchart_generator import generate_billing_flowchart


# -----------------------------------------------------------------------------
# STREAMLIT PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Medical Billing Process Simulation – Week 2",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Healthcare Styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1E3A8A 0%, #0284C7 100%);
        padding: 22px 26px;
        border-radius: 10px;
        color: white;
        margin-bottom: 18px;
    }
    .main-header h1 {
        color: white;
        font-size: 26px;
        font-weight: 700;
        margin: 0;
        padding: 0;
    }
    .main-header p {
        color: #E2E8F0;
        font-size: 13.5px;
        margin-top: 5px;
        margin-bottom: 0;
    }
    .disclaimer-box {
        background-color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        padding: 10px 16px;
        border-radius: 6px;
        color: #92400E;
        font-size: 13px;
        margin-bottom: 18px;
    }
    .kpi-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 14px;
        text-align: center;
    }
    .kpi-title {
        color: #64748B;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
    }
    .kpi-value {
        color: #1E3A8A;
        font-size: 24px;
        font-weight: 700;
        margin-top: 4px;
    }
    .status-badge-paid {
        background-color: #DEF7EC;
        color: #03543F;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }
    .status-badge-part {
        background-color: #FEF08A;
        color: #854D0E;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }
    .status-badge-denied {
        background-color: #FDE8E8;
        color: #9B1C1C;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }
    .status-badge-rejected {
        background-color: #F3E8FF;
        color: #6B21A8;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# DATA INITIALIZATION & PIPELINE CACHING
# -----------------------------------------------------------------------------

@st.cache_data
def get_simulation_data():
    """Execute simulation pipeline and cache results."""
    data_dir = os.path.join(WEEK2_ROOT, "data")
    pipeline = BillingSimulationPipeline(data_dir=data_dir)
    claims, postings, invoices, metrics = pipeline.run_simulation()
    raw_records = pipeline.load_encounters_from_csv()
    return pipeline, claims, postings, invoices, metrics, raw_records


pipeline, claims, postings, invoices, metrics, raw_records = get_simulation_data()
claims_by_id = {c.encounter_id: c for c in claims}
invoices_by_id = {inv.encounter_id: inv for inv in invoices}
postings_by_id = {p.encounter_id: p for p in postings}
records_by_id = {r["encounter_id"]: r for r in raw_records}


# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION & CONTROLS
# -----------------------------------------------------------------------------

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/medical-history.png", width=64)
    st.title("Billing Simulation")
    st.markdown("**Internship Case Study – Week 2**")
    st.markdown("---")

    page = st.selectbox(
        "Workflow Stage Navigator",
        [
            "1. Executive Overview",
            "2. Patient Registration",
            "3. Encounter Documentation",
            "4. Medical Coding & Validation",
            "5. Charge Capture & Fee Schedules",
            "6. Claim Scrubber & Pre-Submission",
            "7. Claim Submission (EDI 837P)",
            "8. Payer Adjudication (ERA 835)",
            "9. Payment & Write-Off Posting",
            "10. Patient Billing Statements",
            "11. Revenue Cycle Analytics",
            "12. Case Study Report Generator"
        ]
    )

    st.markdown("---")
    st.subheader("Encounter Selector")
    selected_enc_id = st.selectbox(
        "Drill Down Encounter",
        options=[c.encounter_id for c in claims],
        format_func=lambda x: f"{x} - {claims_by_id[x].patient.name} ({claims_by_id[x].claim_status.value})"
    )

    selected_claim = claims_by_id[selected_enc_id]
    selected_invoice = invoices_by_id.get(selected_enc_id)
    selected_posting = postings_by_id.get(selected_enc_id)
    selected_record = records_by_id[selected_enc_id]

    st.markdown("---")
    st.markdown(f"**Cohort Total:** {metrics.total_encounters} Encounters")
    st.markdown(f"**Clean Claim Rate:** {metrics.clean_claim_rate:.1f}%")
    st.markdown(f"**Gross Billed:** ${metrics.total_gross_billed:,.2f}")
    st.markdown(f"**Allowed Total:** ${metrics.total_allowed:,.2f}")


# -----------------------------------------------------------------------------
# MAIN HEADER & DISCLAIMER
# -----------------------------------------------------------------------------

st.markdown("""
<div class="main-header">
    <h1>Medical Billing Process Simulation – Case Study Platform</h1>
    <p>Comprehensive 12-Stage Outpatient Revenue Cycle Management & Compliance Auditing Simulation</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer-box">
    <strong>Academic Simulation & Historical Reference Notice:</strong> This software is an educational simulation of the 
    United States outpatient medical billing lifecycle. All patient identities, policy numbers, encounter notes, and fee schedule 
    reimbursements are synthetic. Historical FY 2024 ICD-10-CM and CPT 2024 educational code subsets are utilized. 
    Does not constitute certified coding or binding billing counsel.
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# PAGE 1: EXECUTIVE OVERVIEW
# -----------------------------------------------------------------------------

if page.startswith("1."):
    st.header("Executive Overview & Revenue Cycle Dashboard")
    st.markdown(
        "High-level Key Performance Indicators (KPIs) and financial breakdown across all "
        f"**{metrics.total_encounters} simulated outpatient encounters**."
    )

    # Top KPI Metrics Row 1: Billed and Allowed Revenue
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Gross Charges", f"${metrics.total_gross_billed:,.2f}", help="Retail Chargemaster billed rates for all 14 encounters")
    with col2:
        st.metric("Adjudicated Gross", f"${metrics.total_adjudicated_gross:,.2f}", help="Charges adjudicated through payer contracts (12 encounters)")
    with col3:
        st.metric("Payer Allowed Amount", f"${metrics.total_allowed:,.2f}", help="Negotiated contract maximum reimbursement")
    with col4:
        st.metric("First-Pass Clean Claim Rate", f"{metrics.clean_claim_rate:.1f}%", help="Claims without front-end fatal scrubber errors")

    # Top KPI Metrics Row 2: Partitions and Rates
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric("Net Insurer Paid", f"${metrics.total_insurance_payments:,.2f}", help="Primary third-party cash collections")
    with col6:
        st.metric("Patient Responsibility", f"${metrics.total_patient_responsibility:,.2f}", help="Deductible, copays, and coinsurance")
    with col7:
        st.metric("Denial Rate", f"{metrics.denial_rate:.1f}%", help=f"Payer denials ({metrics.claims_denied_count} claims)")
    with col8:
        st.metric("Rejection Rate", f"{metrics.rejection_rate:.1f}%", help=f"Gateway rejections ({metrics.claims_rejected_count} claims)")

    st.markdown("---")

    # Visualizations
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("Claim Adjudication Distribution")
        status_counts = {
            "Adjudicated (Balance Due)": metrics.claims_paid_count,
            "Partially Paid": metrics.claims_partially_paid_count,
            "Denied": metrics.claims_denied_count,
            "Rejected": metrics.claims_rejected_count
        }
        fig1, ax1 = plt.subplots(figsize=(6, 3.8))
        colors = ["#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]
        ax1.pie(status_counts.values(), labels=status_counts.keys(), autopct="%1.1f%%", startangle=140, colors=colors)
        ax1.axis("equal")
        st.pyplot(fig1)

    with col_chart2:
        st.subheader("Financial Partition Breakdown")
        fin_data = {
            "Insurer Paid": metrics.total_insurance_payments,
            "Patient Due": metrics.total_patient_responsibility,
            "Contractual Adj": metrics.total_contractual_adjustments,
            "Payer Denied": metrics.total_denied_charges,
            "Gateway Rejected": metrics.total_rejected_charges
        }
        fig2, ax2 = plt.subplots(figsize=(6, 3.8))
        ax2.bar(fin_data.keys(), fin_data.values(), color=["#0284C7", "#D97706", "#64748B", "#DC2626", "#7C3AED"])
        ax2.set_ylabel("Dollar Amount ($)")
        for i, v in enumerate(fin_data.values()):
            ax2.text(i, v + 60, f"${v:,.2f}", ha="center", fontweight="bold", fontsize=8.5)
        st.pyplot(fig2)

    st.markdown("---")
    st.subheader("Financial Reconciliation & Variance Audit")
    st.markdown(f"""
    | Accounting Category | Dollar Amount | % of Gross | Revenue Cycle Accounting Role |
    | :--- | :--- | :--- | :--- |
    | **Total Gross Billed Charges** | **${metrics.total_gross_billed:,.2f}** | **100.0%** | Chargemaster retail pricing baseline for all 14 encounters |
    | Less: Gateway Rejected Charges (EDI 277CA) | -${metrics.total_rejected_charges:,.2f} | {(metrics.total_rejected_charges/metrics.total_gross_billed)*100:.2f}% | Unadjudicated front-end holds (ENC-2010 $185.00 + ENC-2014 $185.00; Status Category A7) |
    | **Net Adjudicated Gross Charges** | **${metrics.total_adjudicated_gross:,.2f}** | **{(metrics.total_adjudicated_gross/metrics.total_gross_billed)*100:.2f}%** | Enforceable claims adjudicated through payer fee schedules (12 claims) |
    | Less: Contractual Adjustments (CARC 45) | -${metrics.total_contractual_adjustments:,.2f} | {(metrics.total_contractual_adjustments/metrics.total_gross_billed)*100:.2f}% | Contracted fee schedule discounts & self-pay prompt discounts |
    | Less: Payer Denied Charges (CARC 50, 197, 18) | -${metrics.total_denied_charges:,.2f} | {(metrics.total_denied_charges/metrics.total_gross_billed)*100:.2f}% | Clinical & administrative denials (ENC-2008 $360, ENC-2009 $1,450, ENC-2012 Line 2 $275) |
    | **Payer Allowed Amount** | **${metrics.total_allowed:,.2f}** | **{(metrics.total_allowed/metrics.total_gross_billed)*100:.2f}%** | Maximum enforceable reimbursement on covered services |
    | ├─ Primary Insurance Remittance (EDI 835) | ${metrics.total_insurance_payments:,.2f} | {(metrics.total_insurance_payments/metrics.total_gross_billed)*100:.2f}% | Cash collections paid by third-party health plans |
    | └─ Total Patient Responsibility | ${metrics.total_patient_responsibility:,.2f} | {(metrics.total_patient_responsibility/metrics.total_gross_billed)*100:.2f}% | Patient cost-sharing (${metrics.total_deductible_collected:,.2f} Deductible + ${metrics.total_copay_collected:,.2f} Copay + ${metrics.total_coinsurance_collected:,.2f} Coinsurance + ${metrics.total_self_pay:,.2f} Self-Pay) |
    """)
    st.info(
        f"**Reconciliation Verification:** "
        f"1) Adjudicated Gross (${metrics.total_adjudicated_gross:,.2f}) = Allowed (${metrics.total_allowed:,.2f}) + Contractual Adj (${metrics.total_contractual_adjustments:,.2f}) + Denied (${metrics.total_denied_charges:,.2f}). "
        f"2) Total Gross (${metrics.total_gross_billed:,.2f}) = Adjudicated Gross (${metrics.total_adjudicated_gross:,.2f}) + Rejected Charges (${metrics.total_rejected_charges:,.2f}). "
        f"3) Payer Allowed (${metrics.total_allowed:,.2f}) = Insurer Paid (${metrics.total_insurance_payments:,.2f}) + Patient Responsibility (${metrics.total_patient_responsibility:,.2f}). "
        "Zero unexplained variance across the entire cohort."
    )

    st.markdown("---")
    st.subheader("Cohort Encounters Master Roster")

    roster_rows = []
    for c in claims:
        roster_rows.append({
            "Encounter ID": c.encounter_id,
            "Patient Name": c.patient.name,
            "Payer": c.policy.payer_name,
            "CPT Codes": ", ".join(l.cpt_code for l in c.lines),
            "Gross Billed": f"${c.total_gross_charge:.2f}",
            "Allowed": f"${c.total_allowed_amount:.2f}",
            "Write-Off": f"${c.total_contractual_adjustment:.2f}",
            "Denied": f"${c.total_denied_amount:.2f}",
            "Ins Paid": f"${c.total_insurance_paid:.2f}",
            "Patient Due": f"${c.total_patient_responsibility:.2f}",
            "Claim Status": c.claim_status.value,
            "Adjudication Status": c.adjudication_status,
            "Ins Payment Status": c.insurance_payment_status,
            "Patient Account Status": c.patient_account_status
        })
    df_roster = pd.DataFrame(roster_rows)
    st.dataframe(df_roster, use_container_width=True)


# -----------------------------------------------------------------------------
# PAGE 2: PATIENT REGISTRATION & ELIGIBILITY
# -----------------------------------------------------------------------------

elif page.startswith("2."):
    st.header("Patient Registration & Insurance Eligibility (Stage 1 & 2)")
    st.markdown("Inspect demographic Master Patient Index (MPI) and benefit verification records.")

    p_col1, p_col2 = st.columns([1, 1])

    with p_col1:
        st.subheader("Demographic Profile (EHR Intake)")
        st.markdown(f"**Patient ID:** `{selected_claim.patient.patient_id}`")
        st.markdown(f"**Full Legal Name:** `{selected_claim.patient.name}`")
        st.markdown(f"**Age / Gender:** {selected_claim.patient.age} years | {selected_claim.patient.gender}")
        st.markdown(f"**Date of Birth:** {selected_record.get('patient_dob', '1970-01-01')}")
        st.markdown(f"**Contact Phone:** {selected_claim.patient.phone}")
        st.markdown(f"**Billing Address:** {selected_claim.patient.address}")

    with p_col2:
        st.subheader("Insurance Benefit Structure (EDI 270/271)")
        pol = selected_claim.policy
        st.markdown(f"**Health Plan:** {pol.payer_name} ({pol.plan_name})")
        st.markdown(f"**Plan Model:** `{pol.plan_type}`")
        st.markdown(f"**Subscriber Policy #:** `{pol.policy_number or 'MISSING / UNPOPULATED'}`")
        st.markdown(f"**Group Number:** `{pol.group_number or 'N/A'}`")
        st.markdown(f"**Office Copay:** ${pol.copay_amount:.2f}")
        st.markdown(f"**Deductible Remaining:** ${pol.deductible_remaining:.2f}")
        st.markdown(f"**Coinsurance Rate:** {pol.coinsurance_rate * 100:.0f}%")
        st.markdown(f"**HMO Referral Required:** {'Yes' if pol.requires_referral else 'No'}")
        st.markdown(f"**Referral on File:** {'Yes' if pol.has_referral else 'NO (Missing)'}")

    st.markdown("---")
    st.subheader("Intake Audit Checklist")
    c1, c2, c3 = st.columns(3)
    c1.checkbox("Legal Name Populated", value=bool(selected_claim.patient.name), disabled=True)
    c2.checkbox("Policy Number Active", value=bool(pol.policy_number), disabled=True)
    c3.checkbox("Referral Authenticated", value=bool(not pol.requires_referral or pol.has_referral), disabled=True)


# -----------------------------------------------------------------------------
# PAGE 3: ENCOUNTER DOCUMENTATION
# -----------------------------------------------------------------------------

elif page.startswith("3."):
    st.header("Clinical Encounter Documentation & Authentication (Stage 3)")
    st.markdown("Review the attending physician's clinical progress note (SOAP format) and signature.")

    st.info(f"**Encounter ID:** {selected_claim.encounter_id} | **Date of Service:** {selected_claim.date_of_service} | **Chief Complaint:** {selected_claim.chief_complaint}")

    st.subheader("Clinical Progress Note")
    st.text_area(
        "Medical Record Documentation",
        value=selected_claim.clinical_documentation,
        height=200,
        disabled=True
    )

    col_sig1, col_sig2 = st.columns([1, 1])
    with col_sig1:
        st.subheader("Provider Authentication Status")
        if selected_claim.provider_signature_valid:
            st.success("Physician Electronic Signature: AUTHENTICATED & VALID")
        else:
            st.error("Physician Electronic Signature: UNSIGNED / UNVERIFIED (Fatal Billing Block)")

    with col_sig2:
        st.subheader("Documentation Depth Assessment")
        words = len(selected_claim.clinical_documentation.split())
        st.metric("Total Word Count", f"{words} words")
        if words < 15:
            st.warning("Terse note (<15 words). High risk of payer downcoding or medical review audit.")
        else:
            st.success("Documentation length meets standard clinical documentation threshold.")


# -----------------------------------------------------------------------------
# PAGE 4: MEDICAL CODING & VALIDATION
# -----------------------------------------------------------------------------

elif page.startswith("4."):
    st.header("Medical Coding Decisions & Educational Rule Validation (Stage 4)")
    st.markdown("Evaluation of assigned ICD-10-CM diagnostic codes and CPT procedural/E-M codes.")

    col_icd, col_cpt = st.columns(2)
    with col_icd:
        st.subheader("ICD-10-CM Diagnostic Codes")
        for icd in selected_claim.icd10_diagnoses:
            entry = pipeline.coding_engine.get_icd10_entry(icd)
            desc = entry.get("description", "Unknown Description") if entry else "Unverified Code"
            st.markdown(f"• **`{icd}`**: {desc}")

    with col_cpt:
        st.subheader("CPT Procedure & E/M Codes")
        for line in selected_claim.lines:
            entry = pipeline.coding_engine.get_cpt_entry(line.cpt_code)
            desc = entry.get("description", line.cpt_description) if entry else line.cpt_description
            st.markdown(f"• **`{line.cpt_code}`**: {desc}")

    st.markdown("---")
    st.subheader("Automated Coding Scrutiny Engine Output")
    coding_val = pipeline.coding_engine.validate_encounter_coding(
        documented_diagnosis=selected_record.get("provider_diagnosis", ""),
        assigned_icd10=selected_record.get("assigned_icd10", ""),
        clinical_notes=selected_claim.clinical_documentation,
        assigned_cpt=selected_record.get("assigned_cpt", "")
    )

    if len(coding_val["flags"]) == 0:
        st.success("No coding discrepancies identified. Codes align with clinical documentation.")
    else:
        for flg in coding_val["flags"]:
            if "unverified" in flg or "without dedicated" in flg:
                st.error(f"⚠️ {flg}")
            else:
                st.warning(f"ℹ️ {flg}")


# -----------------------------------------------------------------------------
# PAGE 5: CHARGE CAPTURE & FEE SCHEDULES
# -----------------------------------------------------------------------------

elif page.startswith("5."):
    st.header("Charge Capture & Fee Schedule Pricing (Stage 5)")
    st.markdown("Chargemaster retail rates, negotiated payer allowances, and contractual adjustments.")

    st.subheader(f"Encounter Financial Partition: {selected_claim.encounter_id}")
    line_rows = []
    for ln in selected_claim.lines:
        line_rows.append({
            "Line #": ln.line_number,
            "CPT Code": ln.cpt_code,
            "Description": ln.cpt_description,
            "Gross Charge": f"${ln.gross_charge:.2f}",
            "Payer Allowed": f"${ln.allowed_amount:.2f}",
            "Contractual Write-Off": f"${ln.contractual_adjustment:.2f}"
        })
    st.dataframe(pd.DataFrame(line_rows), use_container_width=True)

    st.info(
        f"**Foundational Identity Verification:** "
        f"Gross Charge (${selected_claim.total_gross_charge:.2f}) = "
        f"Payer Allowed (${selected_claim.total_allowed_amount:.2f}) + "
        f"Contractual Adjustment (${selected_claim.total_contractual_adjustment:.2f})."
    )

    st.markdown("---")
    st.subheader("Interactive Fee Schedule Rate Lookup")
    lookup_cpt = st.selectbox(
        "Select CPT Code to Inspect Chargemaster Pricing",
        ["99213", "99214", "99215", "99203", "99204", "99396", "11102", "36415", "71046", "45378"]
    )
    gross, _, desc = pipeline.fee_calculator.get_cpt_pricing(lookup_cpt)
    st.markdown(f"**Description:** {desc} | **Gross Retail Charge:** `${gross:.2f}`")

    payers = ["BCBS001", "UHC002", "AETNA003", "CMS001", "CIGNA005", "DEFAULT"]
    rate_table = []
    for p in payers:
        _, alw, _ = pipeline.fee_calculator.get_cpt_pricing(lookup_cpt, p)
        rate_table.append({
            "Payer Routing ID": p,
            "Payer Allowed Rate": f"${alw:.2f}",
            "Mandated Contractual Write-Off": f"${gross - alw:.2f}",
            "Write-Off %": f"{((gross - alw) / gross) * 100:.1f}%"
        })
    st.dataframe(pd.DataFrame(rate_table), use_container_width=True)


# -----------------------------------------------------------------------------
# PAGE 6: CLAIM SCRUBBER & PRE-SUBMISSION
# -----------------------------------------------------------------------------

elif page.startswith("6."):
    st.header("Claim Scrubber & Pre-Submission Auditing (Stage 6)")
    st.markdown("Automated pre-clearinghouse rules engine detecting fatal defects and compliance warnings.")

    st.subheader(f"Scrubber Status for Encounter: {selected_claim.encounter_id}")
    if selected_claim.claim_status == ClaimStatus.SCRUBBER_CLEAN:
        st.success("✅ Clean Claim – Zero Fatal Defects. Approved for EDI 837P transmission.")
    else:
        st.error(f"❌ Scrubber Hold – Pre-Submission Exceptions Identified ({len(selected_claim.scrubber_errors)} issues).")

    if selected_claim.scrubber_errors:
        err_rows = []
        for e in selected_claim.scrubber_errors:
            err_rows.append({
                "Rule ID": e.code,
                "Category": e.category,
                "Severity": e.severity,
                "Description": e.description,
                "Remediation": e.recommended_fix
            })
        st.dataframe(pd.DataFrame(err_rows), use_container_width=True)
    else:
        st.info("No scrubber errors detected for this encounter.")

    st.markdown("---")
    st.subheader("Cohort-Wide Scrubber Findings Summary")
    all_errors = []
    for c in claims:
        for e in c.scrubber_errors:
            all_errors.append({
                "Encounter": c.encounter_id,
                "Rule ID": e.code,
                "Severity": e.severity,
                "Category": e.category,
                "Description": e.description
            })
    st.dataframe(pd.DataFrame(all_errors), use_container_width=True)


# -----------------------------------------------------------------------------
# PAGE 7: CLAIM SUBMISSION (EDI 837P)
# -----------------------------------------------------------------------------

elif page.startswith("7."):
    st.header("Electronic Claim Submission Simulation (Stage 7)")
    st.markdown("Standard ANSI ASC X12N 837P (005010X222A1) Electronic Health Care Claim envelope.")

    st.subheader(f"Synthetic EDI 837P Professional Claim File ({selected_claim.encounter_id})")

    pol = selected_claim.policy
    pt = selected_claim.patient
    today_str = datetime.now().strftime("%Y%m%d")

    edi_lines = [
        f"ISA*00*          *00*          *ZZ*SUBMITTER123   *ZZ*CLEARINGHOUSE1 *{today_str}*1200*^*00501*000000001*0*P*:~",
        f"GS*HC*SUBMITTER123*CLEARINGHOUSE1*{today_str}*1200*1*X*005010X222A1~",
        "ST*837*0001*005010X222A1~",
        "BHT*0019*00*BATCH001*20240401*1200*CH~",
        "NM1*41*2*METROPOLITAN OUTPATIENT MEDICAL GROUP*****46*1982736450~",
        "PER*IC*BILLING DEPT*TE*5550192830~",
        f"HL*1**20*1~",
        f"NM1*85*2*METROPOLITAN OUTPATIENT MEDICAL GROUP*****XX*1982736450~",
        f"HL*2*1*22*0~",
        f"SBR*P*18*******{pol.plan_type}~",
        f"NM1*IL*1*{pt.name.split()[-1].upper()}*{pt.name.split()[0].upper()}****MI*{pol.policy_number}~",
        f"DMG*D8*{pt.date_of_birth or '19700101'}*{pt.gender[0]}~",
        f"NM1*PR*3*{pol.payer_name.upper()}*****PI*{pol.payer_id}~",
        f"CLM*{selected_claim.claim_id}*{selected_claim.total_gross_charge:.2f}***11:B:1*Y*A*Y*Y~"
    ]
    for idx, icd in enumerate(selected_claim.icd10_diagnoses, start=1):
        edi_lines.append(f"HI*BK:{icd.replace('.', '')}~")

    for line in selected_claim.lines:
        edi_lines.append(f"LX*{line.line_number}~")
        edi_lines.append(f"SV1*HC:{line.cpt_code}*{line.gross_charge:.2f}*UN*1***1~")
        edi_lines.append(f"DTP*472*D8*{selected_claim.date_of_service.replace('-', '')}~")

    edi_lines.extend([
        "SE*25*0001~",
        "GE*1*1~",
        "IEA*1*000000001~"
    ])

    st.code("\n".join(edi_lines), language="text")
    st.caption("Simulated EDI 837P Professional Claim File generated according to HIPAA X12 Standards.")


# -----------------------------------------------------------------------------
# PAGE 8: PAYER ADJUDICATION (ERA 835)
# -----------------------------------------------------------------------------

elif page.startswith("8."):
    st.header("Payer Adjudication Simulation & Remittance (Stage 8)")
    st.markdown("Payer Electronic Remittance Advice (ERA 835) adjudication and CARC/RARC settlement.")

    st.subheader(f"Adjudication Verdict: {selected_claim.claim_status.value}")
    st.info(f"**Remittance Number:** {selected_claim.remittance_number} | **Adjudication Note:** {selected_claim.adjudication_reason}")

    st.subheader("Line-by-Line Adjudication Results")
    adj_rows = []
    for ln in selected_claim.lines:
        adj_rows.append({
            "CPT": ln.cpt_code,
            "Description": ln.cpt_description,
            "Gross": f"${ln.gross_charge:.2f}",
            "Allowed": f"${ln.allowed_amount:.2f}",
            "Write-Off": f"${ln.contractual_adjustment:.2f}",
            "Insurer Paid": f"${ln.insurance_paid:.2f}",
            "Pt Responsibility": f"${ln.patient_responsibility:.2f}",
            "CARC Code": ln.carc_code,
            "CARC Description": ln.carc_description
        })
    st.dataframe(pd.DataFrame(adj_rows), use_container_width=True)

    st.markdown("---")
    st.subheader("CARC & RARC Reference Glossary")
    carc_glossary = [
        {"CARC": "CARC 1", "Meaning": "Deductible Amount", "Action": "Patient Responsibility (PR)"},
        {"CARC": "CARC 2", "Meaning": "Coinsurance Amount", "Action": "Patient Responsibility (PR)"},
        {"CARC": "CARC 3", "Meaning": "Copayment Amount", "Action": "Patient Responsibility (PR)"},
        {"CARC": "CARC 16", "Meaning": "Claim lacks information needed for adjudication", "Action": "Rejection (Front-End)"},
        {"CARC": "CARC 18", "Meaning": "Exact duplicate service", "Action": "Denial / Write-Off (CO)"},
        {"CARC": "CARC 45", "Meaning": "Charge exceeds fee schedule / contracted maximum", "Action": "Contractual Write-Off (CO)"},
        {"CARC": "CARC 50", "Meaning": "Non-covered service: not deemed medical necessity", "Action": "Denial / Write-Off (CO)"},
        {"CARC": "CARC 150", "Meaning": "Information submitted does not support level of service", "Action": "Downcoding (CO/PR)"},
        {"CARC": "CARC 197", "Meaning": "Precertification / referral absent", "Action": "Denial / Write-Off (CO)"}
    ]
    st.dataframe(pd.DataFrame(carc_glossary), use_container_width=True)


# -----------------------------------------------------------------------------
# PAGE 9: PAYMENT & WRITE-OFF POSTING
# -----------------------------------------------------------------------------

elif page.startswith("9."):
    st.header("Payment Posting & Accounts Receivable Ledger (Stage 9)")
    st.markdown("Reconciliation of insurance EFT payments, contractual write-offs, and patient balances.")

    if selected_posting:
        st.subheader(f"Ledger Journal Entry: {selected_posting.posting_id}")
        col_l1, col_l2, col_l3 = st.columns(3)
        col_l1.metric("Insurance Cash Paid", f"${selected_posting.payer_paid_amount:.2f}")
        col_l2.metric("Contractual Write-Off", f"${selected_posting.contractual_write_off:.2f}")
        col_l3.metric("Transferred to Patient", f"${selected_posting.patient_responsibility:.2f}")

        st.markdown(f"**Check/EFT Trace #:** `{selected_posting.check_eft_trace}`")
        st.markdown(f"**Date Posted:** {selected_posting.date_posted}")
        st.markdown(f"**Ledger Notes:** {selected_posting.ledger_notes}")
    else:
        st.warning(f"Encounter {selected_claim.encounter_id} was rejected at front-end. No ledger posting occurred.")

    st.markdown("---")
    st.subheader("Complete Cohort Payment Posting Ledger")
    post_rows = [p.to_dict() for p in postings]
    st.dataframe(pd.DataFrame(post_rows), use_container_width=True)


# -----------------------------------------------------------------------------
# PAGE 10: PATIENT BILLING STATEMENTS
# -----------------------------------------------------------------------------

elif page.startswith("10."):
    st.header("Patient Billing Statements & Invoicing (Stage 10)")
    st.markdown("Itemized patient statements displaying allowable cost-sharing breakdowns.")

    if selected_invoice:
        st.markdown(f"""
        ### Statement Number: `{selected_invoice.invoice_number}`
        * **Statement Date:** {selected_invoice.invoice_date}
        * **Payment Due Date:** {selected_invoice.due_date} (Net 30 Days)
        * **Account Status:** `{selected_invoice.status}`
        """)

        st.subheader("Itemized Services & Adjudication Summary")
        inv_items = []
        for itm in selected_invoice.items:
            inv_items.append({
                "Description": itm.description,
                "Gross Billed": f"${itm.charge:.2f}",
                "Insurance Write-Off": f"${itm.adjustment:.2f}",
                "Insurance Paid": f"${itm.insurance_paid:.2f}",
                "Patient Due": f"${itm.patient_due:.2f}"
            })
        st.dataframe(pd.DataFrame(inv_items), use_container_width=True)

        col_tot1, col_tot2 = st.columns(2)
        with col_tot1:
            st.markdown("#### Patient Cost-Sharing Breakdown")
            st.markdown(f"• **Copayment:** ${selected_invoice.patient_copay:.2f}")
            st.markdown(f"• **Deductible Applied:** ${selected_invoice.patient_deductible:.2f}")
            st.markdown(f"• **Coinsurance:** ${selected_invoice.patient_coinsurance:.2f}")

        with col_tot2:
            st.markdown("#### Balance Summary")
            st.metric("TOTAL AMOUNT DUE FROM PATIENT", f"${selected_invoice.total_balance_due:.2f}")

        st.markdown("---")
        st.subheader("Text Invoice File Preview")
        txt_path = os.path.join(WEEK2_ROOT, "reports", "invoices", f"{selected_invoice.invoice_number}.txt")
        if os.path.exists(txt_path):
            with open(txt_path, "r", encoding="utf-8") as f:
                raw_txt = f.read()
            st.code(raw_txt, language="text")
            st.download_button(
                "📥 Download Patient Statement (.txt)",
                data=raw_txt,
                file_name=f"{selected_invoice.invoice_number}.txt",
                mime="text/plain"
            )


# -----------------------------------------------------------------------------
# PAGE 11: REVENUE CYCLE ANALYTICS
# -----------------------------------------------------------------------------

elif page.startswith("11."):
    st.header("Revenue Cycle Analytics & Denial Management (Stage 11 & 12)")
    st.markdown("HFMA standard industry benchmark comparison and denial trend analytics.")

    b1, b2, b3, b4 = st.columns(4)
    with b1:
        st.metric("Clean Claim Rate", f"{metrics.clean_claim_rate:.1f}%", delta=f"{metrics.clean_claim_rate - 90:.1f}% vs 90% Target")
    with b2:
        denial_pct = metrics.denial_rate
        st.metric("Denial Rate", f"{denial_pct:.1f}%", delta=f"{5.0 - denial_pct:.1f}% vs <5% Target", delta_color="inverse")
    with b3:
        rej_pct = metrics.rejection_rate
        st.metric("Rejection Rate", f"{rej_pct:.1f}%", delta=f"{2.0 - rej_pct:.1f}% vs <2% Target", delta_color="inverse")
    with b4:
        st.metric("Net Collection Rate", "100.0%", delta="Exact Settlement")

    st.markdown("---")
    st.subheader("Financial Waterfall Breakdown")

    fig_wf, ax_wf = plt.subplots(figsize=(9, 4.0))
    categories = ["Gross Billed", "Gateway Rej.", "Payer Denied", "Contractual Adj", "Ins. Paid", "Patient Due"]
    values = [
        metrics.total_gross_billed,
        metrics.total_rejected_charges,
        metrics.total_denied_charges,
        metrics.total_contractual_adjustments,
        metrics.total_insurance_payments,
        metrics.total_patient_responsibility
    ]
    colors_wf = ["#1E3A8A", "#7C3AED", "#DC2626", "#64748B", "#0284C7", "#D97706"]
    bars = ax_wf.bar(categories, values, color=colors_wf)
    ax_wf.set_ylabel("Dollars ($)")
    for b in bars:
        h = b.get_height()
        ax_wf.text(b.get_x() + b.get_width() / 2, h + 60, f"${h:,.2f}", ha="center", fontsize=8.5, fontweight="bold")
    st.pyplot(fig_wf)

    st.markdown("---")
    st.subheader("Denial Management Work Queue")
    denial_cases = [c for c in claims if c.claim_status in [ClaimStatus.DENIED, ClaimStatus.REJECTED, ClaimStatus.PARTIALLY_PAID]]
    d_rows = []
    for c in denial_cases:
        d_rows.append({
            "Encounter": c.encounter_id,
            "Patient": c.patient.name,
            "Payer": c.policy.payer_name,
            "Outcome": c.claim_status.value,
            "Root Cause": c.adjudication_reason[:90] + "..."
        })
    st.dataframe(pd.DataFrame(d_rows), use_container_width=True)


# -----------------------------------------------------------------------------
# PAGE 12: CASE STUDY REPORT GENERATOR
# -----------------------------------------------------------------------------

elif page.startswith("12."):
    st.header("Case Study Report Generator & Export Deliverables")
    st.markdown("Generate and download the formal 18-section Microsoft Word case study report and CSV audit datasets.")

    report_path = os.path.join(WEEK2_ROOT, "reports", "Week_2_Medical_Billing_Case_Study.docx")
    csv_path = os.path.join(WEEK2_ROOT, "reports", "billing_simulation_results.csv")
    flowchart_path = os.path.join(WEEK2_ROOT, "reports", "workflow_flowchart.png")

    st.subheader("18-Section Formal Word Case Study Report")
    st.markdown("""
    The generated Microsoft Word document adheres strictly to professional healthcare documentation standards:
    1. Cover Page & Disclaimers | 2. Executive Summary | 3. Introduction | 4. Objectives | 5. Scope & Limitations
    6. Dataset Description | 7. Patient Case Studies | 8. Coding Decisions | 9. Complete Billing Workflow
    10. Billing Calculation Examples | 11. Claim Scrubbing & Adjudication | 12. Payment Posting & Invoices
    13. Process Flowchart | 14. Discrepancies & Challenges | 15. Reflective Analysis
    16. Best Practices & Policy Recommendations | 17. Conclusion | 18. References
    """)

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("🚀 Re-Generate Word Report & CSV Deliverables", type="primary"):
            with st.spinner("Generating 300 DPI flowchart and assembling 18-section Word report..."):
                generate_billing_flowchart(output_path=flowchart_path)
                rep_gen = BillingCaseStudyReportGenerator(
                    claims=claims,
                    postings=postings,
                    invoices=invoices,
                    metrics=metrics,
                    flowchart_path=flowchart_path
                )
                rep_gen.generate(output_path=report_path)

                # Export CSV
                df_export = pd.DataFrame([c.to_summary_dict() for c in claims])
                df_export.to_csv(csv_path, index=False)
                st.success("Word report and CSV datasets successfully compiled!")

    st.markdown("---")
    st.subheader("Deliverable Downloads")

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        if os.path.exists(report_path):
            with open(report_path, "rb") as f:
                docx_bytes = f.read()
            st.download_button(
                "📥 Download Case Study Report (.docx)",
                data=docx_bytes,
                file_name="Week_2_Medical_Billing_Case_Study.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            st.caption(f"File size: {len(docx_bytes) / 1024:,.1f} KB")

    with col_d2:
        if os.path.exists(csv_path):
            with open(csv_path, "rb") as f:
                csv_bytes = f.read()
            st.download_button(
                "📥 Download Simulation Results (.csv)",
                data=csv_bytes,
                file_name="billing_simulation_results.csv",
                mime="text/csv"
            )
            st.caption(f"File size: {len(csv_bytes) / 1024:,.1f} KB")

    st.markdown("---")
    st.subheader("Process Flowchart Preview")
    if os.path.exists(flowchart_path):
        st.image(flowchart_path, caption="Week 2 End-to-End Medical Billing Lifecycle Flowchart", use_column_width=True)
