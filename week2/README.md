# Case Study – Medical Billing Process Simulation
## Healthcare Revenue Cycle Management (RCM) – Week 2 Internship Project

---

### Executive Overview

The **Medical Billing Process Simulation** is an end-to-end software simulation modeling the complete outpatient revenue cycle management (RCM) continuum for physician practices. Developed as the Week 2 capstone deliverable of the Healthcare Compliance & Revenue Cycle Internship, this system simulates every operational, clinical, and financial phase from patient registration through third-party payer adjudication and patient statement invoicing.

This project is completely modular and isolated within the `week2/` directory, leaving the Week 1 Medical Coding Compliance Audit Simulation 100% untouched and operational.

---

### Key Capabilities & Architectural Features

1. **12-Stage Outpatient Billing Workflow:**
   * Patient Registration & Master Patient Index (MPI) Intake
   * Insurance Eligibility & Benefit Verification (EDI 270/271)
   * Clinical Encounter Documentation & Electronic Authentication
   * Diagnostic & Procedural Medical Coding Validation
   * Charge Capture & Chargemaster Pricing Crosswalking
   * Pre-Submission Claim Scrubbing & Compliance Rules
   * Electronic Claim Submission (EDI 837P ANSI ASC X12)
   * Third-Party Payer Adjudication (ERA 835) & CARC/RARC Crosswalking
   * Remittance Processing, Contractual Write-Offs & Payment Posting
   * Itemized Patient Billing Statements & Balance Invoicing
   * Accounts Receivable (A/R) & Denial Management
   * Executive Revenue Cycle Performance Analytics

2. **Strict Financial Mathematical Integrity:**
   * **Reconciliation Identity 1:** $\text{Gross Charge} = \text{Payer Allowed Amount} + \text{Contractual Adjustment}$
   * **Reconciliation Identity 2:** $\text{Payer Allowed Amount} = \text{Insurer Payment} + \text{Patient Responsibility}$
   * **Reconciliation Identity 3:** $\text{Patient Responsibility} = \text{Copayment} + \text{Deductible Applied} + \text{Coinsurance}$
   * **Zero Double-Counting:** Strict waterfall order of operations ensures copayments, deductibles, and coinsurance are never double-billed.

3. **Authentic Regulatory Standards & Codes:**
   * Utilizes standard Claim Adjustment Reason Codes (CARC 1, 2, 3, 16, 18, 45, 50, 150, 197) and Remittance Advice Remark Codes (RARC N30, N381, MA01).
   * Models commercial PPO, POS, HMO, High-Deductible Health Plans (HDHP), Medicare Part B, and Self-Pay policies.

4. **18-Section Formal Word Case Study Report:**
   * Publication-standard Microsoft Word document (`Week_2_Medical_Billing_Case_Study.docx`) featuring 18 structured sections, 5 detailed empirical tables, executive callout boxes, and an embedded 300 DPI workflow flowchart diagram.

5. **Multi-Page Interactive Streamlit Application:**
   * Dedicated 12-page web interface (`week2/app.py`) for live drill-downs into claims, EDI 837P files, ERA 835 remittances, ledger entries, patient statements, and analytics.

6. **Comprehensive Automated Test Suite:**
   * 25 unit and integration tests (`week2/tests/test_billing_simulation.py`) verifying all 12 stages, financial formulas, error interception, and report generation (100% pass rate).

---

### Directory Structure

```
Medical-Coding-Compliance-Audit/
├── week2/
│   ├── app.py                          # 12-page interactive Streamlit dashboard
│   ├── generate_reports.py             # Standalone report & invoice generator
│   ├── README.md                       # Week 2 comprehensive documentation
│   ├── data/
│   │   ├── encounters_week2.csv        # 14 simulated outpatient encounters
│   │   ├── insurance_plans.json        # 6 payer policy benefit definitions
│   │   ├── fee_schedule.json           # Chargemaster gross & allowed fee schedules
│   │   └── rules/
│   │       ├── icd10_codes_fy2024.json # FY2024 ICD-10-CM educational subset
│   │       └── cpt_codes_2024.json     # CPT 2024 educational reference subset
│   ├── docs/
│   │   ├── billing_workflow.md         # 12-stage RCM technical guide & CARC glossary
│   │   └── calculation_formulas.md     # Mathematical cost-sharing specifications
│   ├── reports/
│   │   ├── Week_2_Medical_Billing_Case_Study.docx  # 18-section Word report (645 KB)
│   │   ├── billing_simulation_results.csv          # Structured audit findings CSV
│   │   ├── workflow_flowchart.png                  # 300 DPI high-res flowchart (656 KB)
│   │   └── invoices/                               # 14 itemized text statements (INV-2001.txt - INV-2014.txt)
│   ├── src/
│   │   ├── models.py                   # Dataclasses (Patient, Claim, Policy, Invoice, Posting)
│   │   ├── coding_engine.py            # Code verification & specificity auditor
│   │   ├── fee_calculator.py           # Financial waterfall & cost-sharing engine
│   │   ├── claim_scrubber.py           # Pre-submission rule-based claim scrubber
│   │   ├── adjudication_engine.py      # ERA 835 remittance simulation & CARC generator
│   │   ├── payment_poster.py           # Practice ledger & write-off posting engine
│   │   ├── invoice_generator.py        # Itemized patient invoice builder
│   │   ├── flowchart_generator.py      # Matplotlib 300 DPI publication diagram generator
│   │   ├── billing_pipeline.py         # 12-stage orchestrator & batch metrics engine
│   │   └── report_generator.py         # 18-section python-docx report compiler
│   └── tests/
│       └── test_billing_simulation.py  # 25 automated unit & integration tests
```

---

### Quick Start Guide

#### 1. Launch the Interactive Streamlit Dashboard
From the repository root directory, run:
```bash
streamlit run week2/app.py
```
Navigate through the 12 workflow stages in the sidebar to inspect individual encounters, view EDI 837P files, decode ERA 835 remittances, view invoices, and analyze revenue cycle metrics.

#### 2. Execute Standalone Report Generation
To regenerate all deliverables (Word case study report, CSV dataset, 300 DPI flowchart, and 14 text invoices) without running the web server:
```bash
python week2/generate_reports.py
```

#### 3. Run Automated Tests
To run the Week 2 automated test suite (25 tests):
```bash
pytest week2/tests/ -v
```

To run the entire workspace test suite (Week 1 + Week 2 = 42 tests):
```bash
pytest -v
```

---

### Simulation Cohort Scenario Matrix (14 Encounters)

| Encounter ID | Patient Name | Payer & Plan Type | Billed CPT | Gross | Allowed | Write-Off | Denied | Ins Paid | Pt Due | Final Claim Status & CARC Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ENC-2001** | Johnathan Miller | BCBS (PPO) | 99213 | $185.00 | $115.00 | $70.00 | $0.00 | $0.00 | $115.00 | **Adjudicated – Patient Balance Due** – $85 deductible + $30 copay (CARC 1, 3). |
| **ENC-2002** | Eleanor Vance | Medicare Part B | 99214, 36415 | $310.00 | $150.50 | $159.50 | $0.00 | $120.40 | $30.10 | **Adjudicated – Patient Balance Due** – 80/20 Medicare coinsurance after deductible met (CARC 2). |
| **ENC-2003** | Carlos Ramirez | Aetna (HMO) | 99213 | $185.00 | $108.00 | $77.00 | $0.00 | $79.20 | $28.80 | **Adjudicated – Patient Balance Due** – HMO primary care visit: $20 copay + 10% coinsurance ($8.80) (CARC 2, 3). |
| **ENC-2004** | Sophia Chen | Cigna (HDHP) | 99213 | $185.00 | $112.00 | $73.00 | $0.00 | $0.00 | $112.00 | **Adjudicated – Patient Balance Due** – High-deductible health plan; full $112 applied to deductible (CARC 1). |
| **ENC-2005** | Marcus Brody | UHC (POS) | 99396, 36415 | $345.00 | $206.00 | $139.00 | $0.00 | $190.00 | $16.00 | **Adjudicated – Patient Balance Due** – Preventive visit 99396 covered in full ($190); $16 deductible applied to venipuncture 36415 (CARC 1). |
| **ENC-2006** | Beatrice Campbell| Medicare Part B | 11102 | $220.00 | $98.20 | $121.80 | $0.00 | $78.56 | $19.64 | **Adjudicated – Patient Balance Due** – Tangential biopsy with 20% coinsurance ($19.64) (CARC 2). |
| **ENC-2007** | David Kim | BCBS (PPO) | 99215 | $395.00 | $115.00 | $280.00 | $0.00 | $0.00 | $115.00 | **Partially Paid – Remaining Balance** – CPT 99215 downcoded to 99213 (CARC 150); $85 deductible + $30 copay due. |
| **ENC-2008** | Maria Santos | Aetna (HMO) | 99204 | $360.00 | $0.00 | $0.00 | $360.00 | $0.00 | $0.00 | **Denied – Review Required** – Missing mandatory HMO specialist referral (CARC 197; patient held harmless). |
| **ENC-2009** | Robert Hayes | UHC (POS) | 45378 | $1,450.00 | $0.00 | $0.00 | $1,450.00 | $0.00 | $0.00 | **Denied – Review Required** – Colonoscopy billed for sore throat; lack of medical necessity (CARC 50). |
| **ENC-2010** | Linda Washington | BCBS (PPO) | 99213 | $185.00 | $0.00 | $0.00 | $0.00 | $0.00 | $0.00 | **Rejected – Resubmission Required** – Missing subscriber policy ID; clearinghouse gateway rejection (EDI 277CA STC: A7 / CARC 16). |
| **ENC-2011** | Thomas Wright | Self-Pay | 99213 | $185.00 | $129.50 | $55.50 | $0.00 | $0.00 | $129.50 | **Adjudicated – Patient Balance Due** – Uninsured self-pay with 30% prompt-pay discount ($129.50 due from patient). |
| **ENC-2012** | Patricia Kelly | Medicare Part B | 99214, 99214 | $550.00 | $138.50 | $136.50 | $275.00 | $110.80 | $27.70 | **Partially Paid – Remaining Balance** – Line 1 paid ($110.80 ins / $27.70 coins); Line 2 denied as duplicate (CARC 18). |
| **ENC-2013** | James O'Connor | Cigna (HDHP) | 99214, 71046 | $450.00 | $240.00 | $210.00 | $0.00 | $36.00 | $204.00 | **Adjudicated – Patient Balance Due** – $200 deductible absorbed + 10% coinsurance on Line 2 remainder ($4.00) (CARC 1, 2). |
| **ENC-2014** | Rachel Green | Aetna (HMO) | 99213 | $185.00 | $0.00 | $0.00 | $0.00 | $0.00 | $0.00 | **Rejected – Resubmission Required** – Progress note unsigned by rendering clinician; gateway rejection (EDI 277CA STC: A7 / CARC 16). |
| **TOTALS** | **14 Encounters** | **Diverse Mix** | **18 Lines** | **$5,190.00** | **$1,412.70** | **$1,322.30** | **$2,085.00** | **$614.96** | **$797.74** | **Clean Rate: 64.3% (9 Clean, 5 Exceptions)** |

---

### Empirical Cohort Metrics & Financial Reconciliation

* **Total Encounters Analyzed:** 14
* **Total Gross Billed Charges:** $5,190.00 (100.00%)
* **Gateway Rejected Charges (EDI 277CA):** $370.00 (7.13% — unadjudicated: ENC-2010 $185.00, ENC-2014 $185.00)
* **Net Adjudicated Gross Charges:** $4,820.00 (92.87% — processed across 12 encounters)
* **Contractual Fee Schedule Adjustments (CARC 45):** $1,322.30 (25.48% of gross — in-network provider write-offs)
* **Payer Denials / Non-Covered Charges (CARC 50, 197, 18):** $2,085.00 (40.17% of gross — non-reimbursed provider write-offs)
* **Net Payer Allowed Revenue:** $1,412.70 (27.22% of gross allowable yield)
* **Primary Insurance Payments Posted:** $614.96 (43.53% of allowable)
* **Patient Cost-Sharing Due:** $797.74 (56.47% of allowable)
  * *Patient Deductible Applied:* $498.00
  * *Patient Copayments Billed:* $80.00
  * *Patient Coinsurance Billed:* $90.24
  * *Self-Pay Responsibility:* $129.50
* **First-Pass Clean Claim Rate:** 64.3% (9 clean claims / 14 encounters)
* **Payer Adjudication Status Breakdown:**
  * Adjudicated – Patient Balance Due: 8 (57.1%)
  * Partially Paid – Remaining Balance: 2 (14.3%)
  * Denied – Review Required: 2 (14.3%)
  * Rejected – Resubmission Required: 2 (14.3%)
* **Reconciliation Proof (Exact to the penny):**
  - Gross Billed ($5,190.00) = Adjudicated Gross ($4,820.00) + Gateway Rejections ($370.00)
  - Adjudicated Gross ($4,820.00) = Allowed ($1,412.70) + Contractual Adjustments ($1,322.30) + Denials ($2,085.00)
  - Payer Allowed ($1,412.70) = Insurer Paid ($614.96) + Patient Due ($797.74)
  - Patient Due ($797.74) = Deductible ($498.00) + Copay ($80.00) + Coinsurance ($90.24) + Self-Pay ($129.50)

---

### Disclosures & Regulatory Attestation

1. **Synthetic Educational Data:** All patient demographic profiles, encounter notes, insurance card numbers, and financial transactions are synthetic fictional models constructed exclusively for training and academic demonstration.
2. **Historical Reference Code Sets:** Diagnostic (ICD-10-CM) and procedural (CPT) code sets are based on historical **FY 2024** educational reference subsets. They do not reflect real-time active clinical coding updates for subsequent fiscal years.
3. **No Commercial or Legal Advice:** The reimbursement algorithms and workflow logic reflect general theoretical principles of U.S. outpatient medical billing and do not constitute binding legal, financial, or certified coding counsel.
4. **Week 1 Preservation:** All files, datasets, report generators, and tests for Week 1 (Medical Coding Compliance Audit Simulation) remain completely intact and continue to pass 100% of tests.
