"""Unit and Integration Tests for Week 2 Medical Billing Process Simulation.

Validates:
1. Patient registration and demographic validation.
2. Diagnosis coding validation (FY 2024 ICD-10-CM subset).
3. Procedure coding validation (CPT 2024 subset) and documentation checks.
4. Charge capture and Chargemaster pricing lookup.
5. Deductible calculation and accumulator handling.
6. Coinsurance calculation on post-deductible allowable balance.
7. Prevention of double counting (Mathematical Identity: Allowed == Insurance Payment + Patient Responsibility).
8. Claim validation for clean claims (First-pass clean pass).
9. Claim validation for claims with scrubber errors (Fatal and warnings).
10. Claim rejection simulation (Clearinghouse / Administrative holds).
11. Claim denial simulation (CARC 197 missing referral, CARC 50 medical necessity, CARC 150 downcoding).
12. Payment posting and ledger accounting reconciliation.
13. Patient invoice generation and text file export.
14. Workflow state transitions (REGISTRATION -> INVOICED).
15. Flowchart generation and image validation.
16. 18-Section Word case study report generation and python-docx verification.
"""

import os
import sys
import pytest
import docx

# Ensure repository root and week2 root are on sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

WEEK2_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if WEEK2_ROOT not in sys.path:
    sys.path.insert(0, WEEK2_ROOT)

from week2.src.models import (
    BillingStage,
    ClaimStatus,
    PlanType,
    Patient,
    InsurancePolicy,
    ClaimLine,
    Claim,
    PaymentPosting,
    PatientInvoice,
    SimulationBatchMetrics
)
from week2.src.coding_engine import CodingEngine
from week2.src.fee_calculator import FeeCalculator
from week2.src.claim_scrubber import ClaimScrubber
from week2.src.adjudication_engine import AdjudicationEngine
from week2.src.payment_poster import PaymentPoster
from week2.src.invoice_generator import InvoiceGenerator
from week2.src.billing_pipeline import BillingSimulationPipeline
from week2.src.report_generator import BillingCaseStudyReportGenerator
from week2.src.flowchart_generator import generate_billing_flowchart


# -----------------------------------------------------------------------------
# FIXTURES
# -----------------------------------------------------------------------------

@pytest.fixture
def coding_engine():
    """Provides initialized CodingEngine."""
    rules_dir = os.path.join(WEEK2_ROOT, "data", "rules")
    return CodingEngine(rules_dir=rules_dir)


@pytest.fixture
def fee_calc():
    """Provides initialized FeeCalculator."""
    data_dir = os.path.join(WEEK2_ROOT, "data")
    return FeeCalculator(data_dir=data_dir)


@pytest.fixture
def scrubber(coding_engine):
    """Provides initialized ClaimScrubber."""
    return ClaimScrubber(coding_engine=coding_engine)


@pytest.fixture
def adjudicator(fee_calc):
    """Provides initialized AdjudicationEngine."""
    return AdjudicationEngine(fee_calculator=fee_calc)


@pytest.fixture
def payment_poster():
    """Provides initialized PaymentPoster."""
    return PaymentPoster()


@pytest.fixture
def invoice_gen(tmp_path):
    """Provides initialized InvoiceGenerator targeting temporary directory."""
    return InvoiceGenerator(output_dir=str(tmp_path))


@pytest.fixture
def pipeline():
    """Provides initialized BillingSimulationPipeline."""
    data_dir = os.path.join(WEEK2_ROOT, "data")
    return BillingSimulationPipeline(data_dir=data_dir)


# -----------------------------------------------------------------------------
# 1. PATIENT REGISTRATION TESTS
# -----------------------------------------------------------------------------

def test_patient_registration_valid():
    """Test standard patient creation with demographic identifiers."""
    patient = Patient(
        patient_id="PT-TEST-001",
        name="Eleanor Vance",
        age=48,
        gender="F",
        date_of_birth="1976-06-14",
        phone="555-0199",
        address="100 Hilltop Rd"
    )
    assert patient.patient_id == "PT-TEST-001"
    assert patient.name == "Eleanor Vance"
    assert patient.gender == "F"
    assert patient.age == 48
    d = patient.to_dict()
    assert d["patient_id"] == "PT-TEST-001"
    assert d["name"] == "Eleanor Vance"


def test_insurance_policy_creation():
    """Test insurance policy object structure."""
    policy = InsurancePolicy(
        payer_id="BCBS001",
        payer_name="Blue Cross Blue Shield",
        plan_name="Preferred Choice PPO",
        plan_type="PPO",
        policy_number="BCB-8839210",
        group_number="GRP-55410",
        copay_amount=30.00,
        deductible_remaining=150.00,
        coinsurance_rate=0.20,
        oop_max=4000.00,
        requires_referral=False
    )
    assert policy.policy_number == "BCB-8839210"
    assert policy.payer_id == "BCBS001"
    assert policy.copay_amount == 30.00
    assert policy.deductible_remaining == 150.00
    assert policy.coinsurance_rate == 0.20


# -----------------------------------------------------------------------------
# 2. DIAGNOSIS CODING VALIDATION TESTS
# -----------------------------------------------------------------------------

def test_diagnosis_coding_valid(coding_engine):
    """Test validation of valid FY 2024 ICD-10-CM codes."""
    entry = coding_engine.get_icd10_entry("E11.65")
    assert entry is not None
    assert "Type 2 diabetes mellitus with hyperglycemia" in entry.get("description", "")

    val = coding_engine.validate_encounter_coding(
        documented_diagnosis="Type 2 diabetes mellitus with hyperglycemia",
        assigned_icd10="E11.65",
        clinical_notes="Patient presents with elevated fasting glucose. Routine follow-up.",
        assigned_cpt="99214"
    )
    assert val["is_valid"] is True
    assert len([f for f in val["flags"] if "unverified" in f]) == 0


def test_diagnosis_coding_unverified_code(coding_engine):
    """Test detection of unverified or nonexistent ICD-10 code."""
    val = coding_engine.validate_encounter_coding(
        documented_diagnosis="Fictional Disorder",
        assigned_icd10="INVALID.99",
        clinical_notes="Patient presents with unverified symptoms for evaluation.",
        assigned_cpt="99213"
    )
    assert val["is_valid"] is False
    assert any("unverified in active FY2024 educational subset" in f for f in val["flags"])


def test_diagnosis_specificity_alert(coding_engine):
    """Test alert when unspecified code is used with specific laterality in note."""
    val = coding_engine.validate_encounter_coding(
        documented_diagnosis="Unspecified asthma",
        assigned_icd10="J45.909",  # Unspecified asthma
        clinical_notes="Patient presents with wheezing and persistent rales in the right lung field.",
        assigned_cpt="99213"
    )
    assert any("unspecified, but documentation includes specific laterality" in f for f in val["flags"])


# -----------------------------------------------------------------------------
# 3. PROCEDURE CODING VALIDATION TESTS
# -----------------------------------------------------------------------------

def test_procedure_coding_valid(coding_engine):
    """Test validation of authentic CPT 2024 codes."""
    entry = coding_engine.get_cpt_entry("99214")
    assert entry is not None
    assert "established patient" in entry.get("description", "")
    assert "30-39 minutes" in entry.get("description", "")


def test_procedure_coding_unsupported_note(coding_engine):
    """Test detection of procedural CPT billed without procedure report."""
    val = coding_engine.validate_encounter_coding(
        documented_diagnosis="Cough and mild dyspnea",
        assigned_icd10="R05.9",
        clinical_notes="Patient seen for dry cough. Lungs clear to auscultation. Prescribed antitussive.",
        assigned_cpt="71046"  # Chest X-ray 2 views
    )
    assert val["is_valid"] is False
    assert any("billed without dedicated procedure/imaging report" in f for f in val["flags"])


def test_high_level_em_documentation_scrutiny(coding_engine):
    """Test flagging of high-level E/M code without documented high MDM."""
    val = coding_engine.validate_encounter_coding(
        documented_diagnosis="Hypertension",
        assigned_icd10="I10",
        clinical_notes="Brief routine visit. Blood pressure checked. Refilled lisinopril.",
        assigned_cpt="99215"  # High complexity E/M
    )
    assert any("requires high Medical Decision Making" in f for f in val["flags"])


# -----------------------------------------------------------------------------
# 4. CHARGE CALCULATION & CHARGEMASTER TESTS
# -----------------------------------------------------------------------------

def test_chargemaster_pricing_lookup(fee_calc):
    """Test Chargemaster gross charge and allowable retrieval."""
    gross, allowed, desc = fee_calc.get_cpt_pricing("99214", "BCBS001")
    assert gross == 275.00
    assert allowed == 165.00
    assert "Office or other outpatient visit" in desc
    assert round(gross - allowed, 2) == 110.00


def test_self_pay_discount_pricing(fee_calc):
    """Test self-pay charge calculation with 30% financial assistance discount."""
    policy = InsurancePolicy(
        payer_id="SELF_PAY",
        payer_name="Self-Pay Patient",
        plan_name="Uninsured Self-Pay",
        plan_type="Self-Pay",
        policy_number="SELF-PAY-UNINSURED",
        group_number="SELF-NONE",
        self_pay_discount_rate=0.30
    )
    line, _ = fee_calc.calculate_claim_line_financials(
        cpt_code="99213",
        policy=policy,
        current_deductible_remaining=0.0
    )
    assert line.gross_charge == 185.00
    assert line.contractual_adjustment == 55.50  # 30% of $185
    assert line.patient_responsibility == 129.50
    assert line.insurance_paid == 0.00


# -----------------------------------------------------------------------------
# 5. DEDUCTIBLE CALCULATION TESTS
# -----------------------------------------------------------------------------

def test_deductible_absorbs_entire_allowed(fee_calc):
    """Test deductible when remaining deductible exceeds allowed amount."""
    policy = InsurancePolicy(
        payer_id="CIGNA005",
        payer_name="Cigna Health",
        plan_name="Choice HDHP",
        plan_type="HDHP",
        policy_number="CIG-HDHP-100",
        group_number="GRP-CIG",
        deductible_remaining=1500.00,
        copay_amount=0.00,
        coinsurance_rate=0.20
    )
    line, rem_ded = fee_calc.calculate_claim_line_financials(
        cpt_code="99214",
        policy=policy,
        current_deductible_remaining=1500.00
    )
    # Allowed for CIGNA005 99214 is $158.00
    assert line.allowed_amount == 158.00
    assert line.deductible_applied == 158.00
    assert line.coinsurance_applied == 0.00
    assert line.patient_responsibility == 158.00
    assert line.insurance_paid == 0.00
    assert rem_ded == 1500.00 - 158.00


# -----------------------------------------------------------------------------
# 6. COINSURANCE CALCULATION TESTS
# -----------------------------------------------------------------------------

def test_coinsurance_with_zero_deductible(fee_calc):
    """Test standard 80/20 coinsurance when deductible is already met."""
    policy = InsurancePolicy(
        payer_id="CMS001",
        payer_name="Medicare Part B",
        plan_name="Traditional Fee-for-Service",
        plan_type="Medicare",
        policy_number="MED-1049281",
        group_number="GRP-MED01",
        deductible_remaining=0.00,
        copay_amount=0.00,
        coinsurance_rate=0.20
    )
    line, rem_ded = fee_calc.calculate_claim_line_financials(
        cpt_code="99213",
        policy=policy,
        current_deductible_remaining=0.00
    )
    # Allowed for CMS001 99213 is $92.05
    assert line.allowed_amount == 92.05
    assert line.deductible_applied == 0.00
    assert line.coinsurance_applied == 18.41  # 20% of $92.05
    assert line.patient_responsibility == 18.41
    assert line.insurance_paid == 73.64       # 80% of $92.05
    assert rem_ded == 0.00


# -----------------------------------------------------------------------------
# 7. PREVENTION OF DOUBLE COUNTING (MATHEMATICAL IDENTITY)
# -----------------------------------------------------------------------------

def test_mathematical_identity_across_all_simulation_encounters(pipeline):
    """Test that every processed encounter strictly satisfies:
    1. Insurance Payment + Patient Responsibility == Allowed Amount.
    2. Gross Charge == Allowed Amount + Contractual Adjustment (for processed claims).
    3. Copay + Deductible + Coinsurance == Patient Responsibility (for insured claims).
    Zero double counting across the entire cohort.
    """
    claims, postings, invoices, metrics = pipeline.run_simulation()

    assert len(claims) == 14, "Expected 14 simulated encounters"

    for claim in claims:
        for line in claim.lines:
            # 1. Allowed == Ins Paid + Pt Resp (within 1 cent)
            calc_allowed = round(line.insurance_paid + line.patient_responsibility, 2)
            assert abs(line.allowed_amount - calc_allowed) < 0.01, (
                f"Double counting or mismatch in {claim.claim_id} line {line.cpt_code}: "
                f"Allowed {line.allowed_amount} != Ins {line.insurance_paid} + Pt {line.patient_responsibility}"
            )

            # 2. Copay + Deductible + Coinsurance == Total Patient Responsibility (insured)
            if claim.policy.plan_type != "Self-Pay":
                cost_sum = round(line.copay_applied + line.deductible_applied + line.coinsurance_applied, 2)
                assert abs(line.patient_responsibility - cost_sum) < 0.01, (
                    f"Cost sharing breakdown mismatch in {claim.claim_id}: "
                    f"Pt Resp {line.patient_responsibility} != Sum {cost_sum}"
                )
            else:
                # Self-Pay: Patient responsibility equals allowable
                assert line.patient_responsibility == line.allowed_amount

            # 3. Gross == Allowed + Contractual Adj + Denied Amount (for non-rejected lines)
            if claim.claim_status != ClaimStatus.REJECTED:
                calc_gross = round(line.allowed_amount + line.contractual_adjustment + line.denied_amount, 2)
                assert abs(line.gross_charge - calc_gross) < 0.01, (
                    f"Gross charge partition mismatch in {claim.claim_id}: "
                    f"Gross {line.gross_charge} != Allowed {line.allowed_amount} + Adj {line.contractual_adjustment} + Denied {line.denied_amount}"
                )


# -----------------------------------------------------------------------------
# 8. CLAIM VALIDATION (CLEAN CLAIMS)
# -----------------------------------------------------------------------------

def test_clean_claim_scrubber_pass(pipeline, scrubber):
    """Test that a complete, valid encounter passes scrubber with zero fatal errors."""
    records = pipeline.load_encounters_from_csv()
    clean_rec = [r for r in records if r["encounter_id"] == "ENC-2001"][0]
    claim = pipeline.build_claim_from_record(clean_rec)

    errors = scrubber.scrub_claim(claim)
    fatal_errors = [e for e in errors if e.severity == "Fatal"]

    assert len(fatal_errors) == 0, f"Clean claim produced unexpected fatal errors: {fatal_errors}"
    assert claim.claim_status == ClaimStatus.SCRUBBER_CLEAN


# -----------------------------------------------------------------------------
# 9. CLAIM VALIDATION (SCRUBBER DEFECTS)
# -----------------------------------------------------------------------------

def test_scrubber_detects_fatal_missing_patient_name(pipeline, scrubber):
    """Test SCRUB-01: Missing patient name."""
    records = pipeline.load_encounters_from_csv()
    rec = dict([r for r in records if r["encounter_id"] == "ENC-2001"][0])
    rec["patient_name"] = ""

    claim = pipeline.build_claim_from_record(rec)
    errors = scrubber.scrub_claim(claim)
    codes = [e.code for e in errors]

    assert "SCRUB-01" in codes
    assert claim.claim_status == ClaimStatus.SCRUBBER_ERROR


def test_scrubber_detects_fatal_missing_policy_id(pipeline, scrubber):
    """Test SCRUB-03: Missing insurance policy number (ENC-2010)."""
    records = pipeline.load_encounters_from_csv()
    rec = dict([r for r in records if r["encounter_id"] == "ENC-2010"][0])

    claim = pipeline.build_claim_from_record(rec)
    errors = scrubber.scrub_claim(claim)
    codes = [e.code for e in errors]

    assert "SCRUB-03" in codes
    assert claim.claim_status == ClaimStatus.SCRUBBER_ERROR


def test_scrubber_detects_unsigned_note(pipeline, scrubber):
    """Test SCRUB-06: Clinical progress note not signed by provider (ENC-2014)."""
    records = pipeline.load_encounters_from_csv()
    rec = dict([r for r in records if r["encounter_id"] == "ENC-2014"][0])

    claim = pipeline.build_claim_from_record(rec)
    errors = scrubber.scrub_claim(claim)
    codes = [e.code for e in errors]

    assert "SCRUB-06" in codes
    assert claim.claim_status == ClaimStatus.SCRUBBER_ERROR


# -----------------------------------------------------------------------------
# 10. CLAIM REJECTION SIMULATION
# -----------------------------------------------------------------------------

def test_claim_rejection_on_fatal_scrubber_error(pipeline):
    """Test clearinghouse rejection (CARC 16) when claim has missing policy or unsigned note."""
    claims, _, _, _ = pipeline.run_simulation()
    rej_claims = [c for c in claims if c.claim_status == ClaimStatus.REJECTED]

    assert len(rej_claims) == 2, f"Expected 2 rejected claims, got {len(rej_claims)}"
    rej_ids = [c.encounter_id for c in rej_claims]
    assert "ENC-2010" in rej_ids
    assert "ENC-2014" in rej_ids

    for c in rej_claims:
        assert any("CARC 16" in l.carc_code for l in c.lines)
        assert c.total_allowed_amount == 0.00
        assert c.total_insurance_paid == 0.00
        assert c.total_patient_responsibility == 0.00


# -----------------------------------------------------------------------------
# 11. CLAIM DENIAL SIMULATION
# -----------------------------------------------------------------------------

def test_claim_denial_missing_hmo_referral(pipeline):
    """Test CARC 197 denial when specialist visit lacks HMO referral (ENC-2008)."""
    claims, _, _, _ = pipeline.run_simulation()
    claim_2008 = [c for c in claims if c.encounter_id == "ENC-2008"][0]

    assert claim_2008.claim_status == ClaimStatus.DENIED
    assert any("CARC 197" in l.carc_code for l in claim_2008.lines)
    # In-network denial protects patient: patient responsibility must be 0
    assert claim_2008.total_patient_responsibility == 0.00
    assert claim_2008.total_insurance_paid == 0.00
    assert claim_2008.total_denied_amount == claim_2008.total_gross_charge
    assert claim_2008.total_contractual_adjustment == 0.00


def test_claim_downcoding_carc_150(pipeline):
    """Test CARC 150 partial payment/downcoding for CPT 99215 with low MDM (ENC-2007)."""
    claims, _, _, _ = pipeline.run_simulation()
    claim_2007 = [c for c in claims if c.encounter_id == "ENC-2007"][0]

    assert claim_2007.claim_status == ClaimStatus.PARTIALLY_PAID
    assert any("CARC 150" in l.carc_code for l in claim_2007.lines)
    # Allowed amount was downcoded to 99213 rate under BCBS001 ($115.00)
    assert claim_2007.lines[0].allowed_amount == 115.00


# -----------------------------------------------------------------------------
# 12. PAYMENT POSTING TESTS
# -----------------------------------------------------------------------------

def test_payment_posting_reconciliation(pipeline):
    """Test payment poster creates balanced ledger entry."""
    claims, postings, _, _ = pipeline.run_simulation()
    assert len(postings) == 12, "Expected 12 postings (14 total encounters minus 2 rejected)"

    posting_2001 = [p for p in postings if p.encounter_id == "ENC-2001"][0]
    assert posting_2001.claim_id == "CLM-2001"
    assert posting_2001.payer_paid_amount == 0.00
    assert posting_2001.contractual_write_off == 70.00
    assert posting_2001.patient_responsibility == 115.00
    assert "EFT-BCBS001-2001-835" in posting_2001.check_eft_trace


# -----------------------------------------------------------------------------
# 13. PATIENT INVOICE GENERATION TESTS
# -----------------------------------------------------------------------------

def test_patient_invoice_generation_and_export(pipeline, invoice_gen, tmp_path):
    """Test patient invoice creation and formatted text file generation."""
    records = pipeline.load_encounters_from_csv()
    rec = [r for r in records if r["encounter_id"] == "ENC-2001"][0]
    claim = pipeline.build_claim_from_record(rec)
    pipeline.scrubber.scrub_claim(claim)
    pipeline.adjudicator.adjudicate_claim(claim)
    pipeline.payment_poster.post_remittance(claim)

    invoice = invoice_gen.generate_invoice(claim)
    assert invoice.invoice_number == "INV-2001"
    assert invoice.patient_name == "Johnathan Miller"
    assert invoice.total_balance_due == 115.00

    filepath = invoice_gen.export_invoice_text(invoice)
    assert os.path.exists(filepath)

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    assert "PATIENT BILLING STATEMENT / SUMMARY INVOICE" in content
    assert "Johnathan Miller" in content
    assert "115.00" in content
    assert "PAYMENT NOTICE & REGULATORY DISCLAIMER" in content


# -----------------------------------------------------------------------------
# 14. WORKFLOW STATE TRANSITIONS TESTS
# -----------------------------------------------------------------------------

def test_workflow_state_transitions(pipeline):
    """Test sequential progression across all 12 stages ending in INVOICED."""
    records = pipeline.load_encounters_from_csv()
    rec = [r for r in records if r["encounter_id"] == "ENC-2001"][0]

    # Stage 1: Build
    claim = pipeline.build_claim_from_record(rec)
    assert claim.stage == BillingStage.CHARGE_CAPTURED

    # Stage 2: Scrub
    pipeline.scrubber.scrub_claim(claim)
    assert claim.stage == BillingStage.SCRUBBED

    # Stage 3: Submit
    claim.stage = BillingStage.SUBMITTED
    assert claim.stage == BillingStage.SUBMITTED

    # Stage 4: Adjudicate
    pipeline.adjudicator.adjudicate_claim(claim)
    assert claim.stage == BillingStage.ADJUDICATED

    # Stage 5: Payment Post
    pipeline.payment_poster.post_remittance(claim)
    assert claim.stage == BillingStage.PAYMENT_POSTED

    # Stage 6: Invoice
    pipeline.invoice_generator.generate_invoice(claim)
    assert claim.stage == BillingStage.INVOICED


# -----------------------------------------------------------------------------
# 15. FLOWCHART IMAGE GENERATION TESTS
# -----------------------------------------------------------------------------

def test_flowchart_image_generation(tmp_path):
    """Test that billing flowchart generates a valid PNG file."""
    output_png = str(tmp_path / "test_flowchart.png")
    generate_billing_flowchart(output_path=output_png)

    assert os.path.exists(output_png)
    file_size = os.path.getsize(output_png)
    assert file_size > 50000, f"Flowchart PNG file too small: {file_size} bytes"


# -----------------------------------------------------------------------------
# 16. 18-SECTION WORD REPORT GENERATION TESTS
# -----------------------------------------------------------------------------

def test_word_case_study_report_generation(pipeline, tmp_path):
    """Test that BillingCaseStudyReportGenerator builds an 18-section Word document."""
    claims, postings, invoices, metrics = pipeline.run_simulation()

    test_docx_path = str(tmp_path / "Test_Billing_Case_Study.docx")
    flowchart_path = os.path.join(WEEK2_ROOT, "reports", "workflow_flowchart.png")

    report_gen = BillingCaseStudyReportGenerator(
        claims=claims,
        postings=postings,
        invoices=invoices,
        metrics=metrics,
        flowchart_path=flowchart_path
    )
    report_gen.generate(output_path=test_docx_path)

    assert os.path.exists(test_docx_path)
    file_size = os.path.getsize(test_docx_path)
    assert file_size > 100000, f"Report .docx size suspiciously small: {file_size} bytes"

    # Open docx and inspect structure
    doc = docx.Document(test_docx_path)
    all_paras = [p.text for p in doc.paragraphs]
    
    # Check for presence of all numbered sections 2 to 18
    for i in range(2, 19):
        prefix = f"{i}. "
        assert any(text.startswith(prefix) for text in all_paras), f"Missing section {i} starting with '{prefix}' in report"

    # Also verify Section 1: Cover page title
    assert any("Medical Billing Process Simulation" in text for text in all_paras)
    assert len(doc.tables) >= 5, f"Expected at least 5 tables, found {len(doc.tables)}"


# -----------------------------------------------------------------------------
# 17. DASHBOARD METRICS & RECONCILIATION REGRESSION TESTS
# -----------------------------------------------------------------------------

def test_dashboard_metric_attributes(pipeline):
    """Regression Test: Verify all SimulationBatchMetrics properties accessed by app.py exist and return correct values."""
    claims, postings, invoices, metrics = pipeline.run_simulation()

    # Verify counts and aliases
    assert metrics.paid_claims == 8
    assert metrics.claims_paid_count == 8
    assert metrics.partially_paid_claims == 2
    assert metrics.claims_partially_paid_count == 2
    assert metrics.denied_claims == 2
    assert metrics.claims_denied_count == 2
    assert metrics.rejected_claims == 2
    assert metrics.claims_rejected_count == 2
    assert metrics.clean_claims == 9
    assert metrics.clean_claims_count == 9

    # Verify rates and percentages
    assert metrics.clean_claim_rate == 64.3
    assert metrics.rejection_rate == 14.3
    assert metrics.denial_rate == 14.3
    assert metrics.net_collection_rate == 100.0

    # Verify amounts and aliases
    assert metrics.total_gross_billed == 5190.00
    assert metrics.total_adjudicated_gross == 4820.00
    assert metrics.total_rejected_charges == 370.00
    assert metrics.total_allowed == 1412.70
    assert metrics.total_allowed_amount == 1412.70
    assert metrics.total_contractual_adjustments == 1322.30
    assert metrics.total_denied_charges == 2085.00
    assert metrics.total_insurance_payments == 614.96
    assert metrics.total_patient_responsibility == 797.74
    assert metrics.total_adjustments_and_denials == 3407.30


def test_financial_reconciliation_identity(pipeline):
    """Regression Test: Verify mathematical double-entry reconciliation across all 14 encounters."""
    claims, postings, invoices, metrics = pipeline.run_simulation()

    # 1. Total Gross Billed == Adjudicated Gross + Rejected Charges
    assert metrics.total_gross_billed == round(metrics.total_adjudicated_gross + metrics.total_rejected_charges, 2)
    assert metrics.total_gross_billed == 5190.00
    assert metrics.total_adjudicated_gross == 4820.00
    assert metrics.total_rejected_charges == 370.00

    # 2. Adjudicated Gross == Allowed + Contractual Adjustments + Denied Charges
    calculated_adjudicated = round(
        metrics.total_allowed + metrics.total_contractual_adjustments + metrics.total_denied_charges, 2
    )
    assert metrics.total_adjudicated_gross == calculated_adjudicated
    assert calculated_adjudicated == 4820.00

    # 3. Payer Allowed == Insurance Paid + Patient Responsibility
    calculated_allowed = round(metrics.total_insurance_payments + metrics.total_patient_responsibility, 2)
    assert metrics.total_allowed == calculated_allowed
    assert calculated_allowed == 1412.70

    # 4. Patient Responsibility breakdown (Deductible + Copay + Coinsurance + Self-Pay)
    assert metrics.total_deductible_collected == 498.00
    assert metrics.total_copay_collected == 80.00
    assert metrics.total_coinsurance_collected == 90.24
    assert metrics.total_self_pay == 129.50
    pt_cost_sharing = round(
        metrics.total_deductible_collected + metrics.total_copay_collected + metrics.total_coinsurance_collected + metrics.total_self_pay, 2
    )
    assert metrics.total_patient_responsibility == pt_cost_sharing
    assert metrics.total_patient_responsibility == 797.74


def test_enc_2009_denial_amount(pipeline):
    """Regression Test: Verify ENC-2009 gross charge and denied amount is exactly $1,450.00."""
    claims, _, _, _ = pipeline.run_simulation()
    c_2009 = next(c for c in claims if c.encounter_id == "ENC-2009")
    assert c_2009.total_gross_charge == 1450.00
    assert c_2009.total_denied_amount == 1450.00
    assert c_2009.total_allowed_amount == 0.00
    assert c_2009.total_insurance_paid == 0.00
    assert c_2009.total_patient_responsibility == 0.00
    assert c_2009.claim_status == ClaimStatus.DENIED


def test_370_dollar_discrepancy_investigation(pipeline):
    """Regression Test: Prove root cause of previously unexplained $370 difference.

    The $370 gap equals exactly the gross billed sum of the 2 pre-adjudication
    clearinghouse rejected encounters:
    - ENC-2010 (Linda Washington, missing policy ID, CPT 99213): $185.00
    - ENC-2014 (Rachel Green, unsigned clinical note, CPT 99213): $185.00
    Sum: $185.00 + $185.00 = $370.00
    """
    claims, _, _, metrics = pipeline.run_simulation()

    rejected_claims = [c for c in claims if c.claim_status == ClaimStatus.REJECTED]
    assert len(rejected_claims) == 2

    rej_enc_ids = {c.encounter_id for c in rejected_claims}
    assert rej_enc_ids == {"ENC-2010", "ENC-2014"}

    claim_2010 = [c for c in rejected_claims if c.encounter_id == "ENC-2010"][0]
    claim_2014 = [c for c in rejected_claims if c.encounter_id == "ENC-2014"][0]

    assert claim_2010.total_gross_charge == 185.00
    assert claim_2014.total_gross_charge == 185.00
    assert claim_2010.total_allowed_amount == 0.00
    assert claim_2014.total_allowed_amount == 0.00
    assert claim_2010.total_contractual_adjustment == 0.00
    assert claim_2014.total_contractual_adjustment == 0.00

    sum_rejected = round(claim_2010.total_gross_charge + claim_2014.total_gross_charge, 2)
    assert sum_rejected == 370.00
    assert metrics.total_rejected_charges == 370.00

    # Prove that subtracting rejected charges from total gross billed equals adjudicated gross
    variance = round(metrics.total_gross_billed - metrics.total_adjudicated_gross, 2)
    assert variance == 370.00


def test_claim_status_counts_exhaustive(pipeline):
    """Regression Test: Validate exhaustive partition of all 14 simulated encounters by claim status."""
    claims, _, _, metrics = pipeline.run_simulation()
    assert len(claims) == 14

    paid = [c for c in claims if c.claim_status == ClaimStatus.PAID]
    partially_paid = [c for c in claims if c.claim_status == ClaimStatus.PARTIALLY_PAID]
    denied = [c for c in claims if c.claim_status == ClaimStatus.DENIED]
    rejected = [c for c in claims if c.claim_status == ClaimStatus.REJECTED]

    assert len(paid) == 8
    assert len(partially_paid) == 2
    assert len(denied) == 2
    assert len(rejected) == 2
    assert len(paid) + len(partially_paid) + len(denied) + len(rejected) == 14

    # Verify matching metric counts
    assert metrics.paid_claims == len(paid)
    assert metrics.partially_paid_claims == len(partially_paid)
    assert metrics.denied_claims == len(denied)
    assert metrics.rejected_claims == len(rejected)


def test_invoices_and_postings_generation_integrity(pipeline):
    """Regression Test: Verify 12 ledger postings and 14 patient billing statements."""
    claims, postings, invoices, _ = pipeline.run_simulation()

    # 12 postings: exactly 14 minus 2 rejected
    assert len(postings) == 12
    posting_enc_ids = {p.encounter_id for p in postings}
    assert "ENC-2010" not in posting_enc_ids
    assert "ENC-2014" not in posting_enc_ids

    # 14 invoices: all encounters receive statements
    assert len(invoices) == 14
    invoice_map = {inv.encounter_id: inv for inv in invoices}

    # Verify rejected invoices have 0 balance due and zero patient responsibility
    for rej_id in ["ENC-2010", "ENC-2014"]:
        assert invoice_map[rej_id].total_balance_due == 0.00
        assert invoice_map[rej_id].status == "Paid in Full ($0 Balance)"

    # Verify adjudicated invoices have total_balance_due matching patient responsibility
    for claim in claims:
        if claim.claim_status != ClaimStatus.REJECTED:
            inv = invoice_map[claim.encounter_id]
            assert abs(inv.total_balance_due - claim.total_patient_responsibility) < 0.01

