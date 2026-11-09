# End-to-End Medical Billing Process Workflow
## Revenue Cycle Management (RCM) Technical Guide – Week 2 Simulation

---

### Executive Overview

Medical billing is the operational discipline that converts clinical documentation into standardized electronic claims, submits them to third-party payers, reconciles remittances, and collects patient cost-sharing liabilities. In the United States healthcare reimbursement system, this is governed by the Health Insurance Portability and Accountability Act (HIPAA) Electronic Data Interchange (EDI) standards, federal Medicare regulations, and commercial payer contracts.

This document details the 12-stage outpatient billing workflow implemented in the **Week 2 Medical Billing Process Simulation**.

---

### 12-Stage Outpatient Billing Workflow

```
[1. Registration] ──> [2. Insurance Verification] ──> [3. Clinical Encounter]
                                                              │
[6. Claim Scrubbing] <── [5. Charge Capture] <── [4. Medical Coding]
        │
   (Pass/Fail)
   ├─ Fail ──> [Rejection / Pre-bill Hold (Scrubber Errors)]
   └─ Pass ──> [7. EDI 837P Submission]
                      │
              [8. Adjudication]
                      │
   ┌──────────────────┴──────────────────┐
   │                                     │
[Approved / Paid]                 [Denied / Downcoded]
   │                                     │
   └───────────────┬─────────────────────┘
                   ▼
         [9. Payment Posting]
                   │
         [10. Patient Invoice]
                   │
         [11. Denial Appeals]
                   │
         [12. Executive Analytics]
```

---

### Detailed Stage Specifications

#### Stage 1: Patient Registration & Demographic Intake
* **Objective:** Establish the Master Patient Index (MPI) record with verified demographic identifiers.
* **Key Data Captured:**
  * Patient Full Legal Name, Date of Birth (DOB), Gender, Social Security Number / Fictional Patient ID.
  * Residential Address, Contact Phone, Emergency Contact.
  * Guarantor Information (if patient is a minor or dependent).
* **Compliance Safeguard:** Enforces non-blank names, valid historical birth dates, and standard identification indexing to prevent duplicate master files.

#### Stage 2: Insurance Eligibility & Benefit Verification (EDI 270/271)
* **Objective:** Validate insurance policy status, coverage period, network participation, and cost-sharing obligations prior to service delivery.
* **Payer Categories Simulated:**
  1. **Commercial PPO (Preferred Provider Organization):** Lower copay/deductible in-network, out-of-network benefits available (e.g., Blue Cross Blue Shield PPO).
  2. **Commercial POS (Point of Service):** Hybrid HMO/PPO; requires primary care designation (e.g., UnitedHealthcare POS).
  3. **Commercial HMO (Health Maintenance Organization):** In-network only; strict requirement for specialist referrals (e.g., Aetna HMO).
  4. **Government Fee-For-Service:** Medicare Part B; 80/20 coinsurance after annual deductible.
  5. **High Deductible Health Plan (HDHP):** High initial deductible ($2,000+) paired with Health Savings Accounts (HSA) (e.g., Cigna HDHP).
  6. **Self-Pay / Uninsured:** 100% patient responsibility subject to prompt-pay discounts.
* **Pre-Authorization & Referral Rule:** HMO specialist encounters require an authenticated Prior Authorization Number on file before claim creation. Missing authorization triggers pre-bill scrubber flags or subsequent payer denial.

#### Stage 3: Clinical Encounter Documentation
* **Objective:** Capture the complete clinical narrative following the SOAP (Subjective, Objective, Assessment, Plan) format.
* **Authentication Standard:**
  * Every clinical note must be electronically signed and authenticated by the rendering provider (physician, nurse practitioner, or physician assistant).
  * Unauthenticated progress notes (`physician_signature: False`) prevent claim finalization and generate fatal scrubber exceptions.

#### Stage 4: Medical Coding & Code Set Validation
* **Objective:** Translate documented diagnoses into ICD-10-CM codes and services/procedures into CPT codes.
* **Historical Educational Code Sets:**
  * **ICD-10-CM:** FY 2024 CMS/CDC official code subset.
  * **CPT:** 2024 AMA code subset.
* **Auditing Checks Applied:**
  * *Code Existence:* Validates code against the reference catalog.
  * *Symptom vs. Definitive Diagnosis:* Alerts if symptom codes (e.g., R07.9) are billed alongside confirmed definitive etiologies.
  * *Specificity Check:* Flags unspecified codes (e.g., J45.909) when detailed clinical notes justify specific options (e.g., J45.51).
  * *High-Level Evaluation & Management (E/M) Scrutiny:* Codes CPT 99205 and 99215 require comprehensive medical decision-making (MDM) or extended documentation depth.

#### Stage 5: Charge Capture & Chargemaster (CDM) Pricing
* **Objective:** Associate assigned CPT codes with facility or professional fee schedules to generate gross billed charges.
* **Components:**
  * **Gross Charge (Chargemaster Rate):** Standard retail rate billed on the claim.
  * **Payer Allowed Amount:** Negotiated contract maximum rate that the provider agrees to accept as payment in full.
  * **Contractual Adjustment (Write-Off):** Difference between Gross Billed and Allowed Amount (`Gross Charge - Allowed Amount`). The provider is legally and contractually prohibited from balance-billing this amount to in-network patients.

#### Stage 6: Claim Scrubbing & Pre-Submission Validation
* **Objective:** Screen claims through automated rule sets before dispatch to the clearinghouse to maximize First-Pass Clean Claim Rates.
* **Scrubber Rule Dimensions:**
  * `ERR-001` (Fatal): Missing or blank patient first/last name.
  * `ERR-002` (Fatal): Missing or non-alphanumeric insurance policy ID.
  * `ERR-003` (Fatal): Clinical note not signed by rendering provider.
  * `ERR-004` (Fatal): Primary diagnosis code missing or invalid.
  * `ERR-005` (Fatal): Missing required procedural documentation in the progress note.
  * `ERR-006` (Fatal): Duplicate claim submission (same patient, provider, date, and service).
  * `ERR-007` (Warning): Specialist HMO service without documented prior authorization.
  * `ERR-008` (Warning): High-level E/M code without documented high MDM.
* **Outcome Routing:** Clean claims advance to Stage 7. Claims with fatal errors are routed to the billing work queue for human correction.

#### Stage 7: Claim Generation & EDI 837P Submission
* **Objective:** Format clean billing data into the ANSI ASC X12N 837P (Professional) 005010X222A1 standard electronic envelope.
* **Key EDI Loops & Segments:**
  * `ISA/GS`: Interchange and Functional Group Envelopes.
  * `Loop 2000A / 2010AA`: Billing Provider Hierarchical Level & Name (NM1*85).
  * `Loop 2000B / 2010BA`: Subscriber Hierarchical Level & Identification (NM1*IL).
  * `Loop 2000C / 2010CA`: Patient Hierarchical Level (if different from subscriber).
  * `Loop 2300`: Claim Information (CLM, HI diagnosis pointers).
  * `Loop 2400`: Service Line Information (LX, SV1 procedure code, charges, units).

#### Stage 8: Clearinghouse Gateway Validation (EDI 277CA) & Payer Adjudication (EDI 835)
* **Objective:** Validate claim syntax at the clearinghouse gateway, transmit clean claims to payers, and process third-party adjudication remittance files.
* **Clearinghouse Gateway Acknowledgment (EDI 277CA):**
  * The clearinghouse executes HIPAA syntax validation and front-end pre-adjudication edits.
  * Clean claims pass through to health plans for adjudication.
  * Claims with fatal omissions (e.g., missing subscriber policy number or unauthenticated progress note) generate an EDI 277CA Claim Acknowledgment transaction with Status Category Code **STC: A7** (Acknowledgment / Rejected for Invalid Information).
  * These claims are stopped prior to payer entry and mapped to CARC 16 billing workqueues for front-end demographic or signature correction.
* **Payer Adjudication & Electronic Remittance Advice (EDI 835):**
  * Transmitted claims are adjudicated by payers against member benefit schedules, medical necessity coverage policies, and contracted fee allowances.
  * The payer issues an ANSI ASC X12N 835 Health Care Claim Payment/Advice file accompanied by Electronic Funds Transfers (EFT).
* **Adjudication Decisions & Standardized Statuses:**
  1. **Adjudicated – Fully Settled:** Claim processed and allowed; insurer payment and/or write-off completely settles charge; patient responsibility is $0.00.
  2. **Adjudicated – Patient Balance Due:** Claim processed and allowed; payer remits payment and allocates cost-sharing (deductible, copay, coinsurance) to the patient.
  3. **Partially Paid – Remaining Balance:** Payer downcodes or partially remits line items, leaving an allowable balance due.
  4. **Denied – Review Required:** Payer denies claim on the 835 ERA (e.g., CARC 50 medical necessity, CARC 197 missing referral, CARC 18 duplicate line).
  5. **Rejected – Resubmission Required:** Clearinghouse stops claim pre-adjudication via EDI 277CA (STC: A7); no remittance generated until corrected and retransmitted.

#### Stage 9: Remittance Processing & Payment Posting
* **Objective:** Parse ERA 835 data and update patient and insurance accounts in the practice management ledger.
* **Ledger Entries Posted:**
  * Insurance Payment (Cash credit).
  * Contractual Allowance Adjustment (Write-off debit to gross charges under CARC 45).
  * Transfer Remaining Balance to Patient Responsibility (Deductible, Copayment, Coinsurance).
* **Reconciliation Identity:**
  $$\text{Gross Charge} = \text{Insurance Paid} + \text{Patient Responsibility} + \text{Contractual Adjustment}$$
  *(For processed claims where Allowed Amount equals Insurance Paid plus Patient Responsibility).*

#### Stage 10: Patient Statement & Invoicing
* **Objective:** Generate a clear, transparent, itemized patient bill for remaining out-of-pocket balances.
* **Statement Itemization:**
  * Date of Service, Rendering Provider, Procedure Description.
  * Gross Charge, Insurance Payment, Contractual Savings.
  * Itemized Cost-Sharing: Deductible applied, Copayment, Coinsurance.
  * Due Date (Standard Net 30 days), Financial Assistance Notice, and Prompt-Pay Options.

#### Stage 11: Accounts Receivable (A/R) & Denial Management
* **Objective:** Monitor aging receivables and appeal invalid payer denials within payer timely filing limits (typically 90 to 180 days).
* **Appeal Workflows:**
  * *EDI 277CA (STC: A7 / CARC 16):* Add missing policy ID or clinician signature; resubmit as clean initial claim.
  * *CARC 197 (Missing Pre-Auth/Referral):* Submit retroactive authorization request with clinical documentation.
  * *CARC 150 (Downcoding):* Submit appeal packet with medical decision-making chart notes justifying the assigned E/M level.
  * *CARC 50 (Medical Necessity):* Provide full chart notes, diagnostic test results, and applicable coverage criteria.

#### Stage 12: Executive Analytics & Revenue Cycle KPI Tracking
* **Objective:** Measure end-to-end operational and financial health through standard HFMA (Healthcare Financial Management Association) metrics.
* **Core KPIs:**
  * **First-Pass Clean Claim Rate:** Target > 90%. Measures billing front-end accuracy.
  * **Denial Rate:** Target < 5%. Measures clinical documentation and authorization rigor.
  * **Net Collection Rate:** Effective reimbursement collected relative to allowable amounts.
  * **Days in A/R (Aging):** Average days from date of service to cash collection.

---

### Standard Claim Adjustment Reason Codes (CARC) & Remittance Advice Remark Codes (RARC)

| CARC Code | Standard Meaning | Category | Simulation Encounter Mapping |
| :--- | :--- | :--- | :--- |
| **CARC 1** | Deductible Amount | Patient Responsibility (PR) | High-deductible or early-year visits (ENC-2001, ENC-2004, ENC-2005, ENC-2007, ENC-2013) |
| **CARC 2** | Coinsurance Amount | Patient Responsibility (PR) | Cost sharing percentages (ENC-2002, ENC-2003, ENC-2006, ENC-2012, ENC-2013) |
| **CARC 3** | Copayment Amount | Patient Responsibility (PR) | Fixed office visit copays (ENC-2001, ENC-2003, ENC-2007) |
| **CARC 16 / 277CA** | Claim lacks information or has submission/billing error(s) (EDI 277CA STC: A7) | Gateway Rejection / Workqueue | Missing policy ID (ENC-2010), unauthenticated note (ENC-2014) |
| **CARC 18** | Exact duplicate service | Denial / Compliance (CO) | Duplicate billings on same date of service (ENC-2012 Line 2) |
| **CARC 45** | Charge exceeds fee schedule/maximum allowable or contracted rate | Contractual Obligation (CO) | Universal in-network contractual adjustments |
| **CARC 50** | Non-covered services because not deemed a 'medical necessity' | Denial / Clinical (CO) | Preventive screening colonoscopy coding mismatch (ENC-2009) |
| **CARC 150** | Payer deems the information submitted does not support this level of service | Downcode / Clinical (CO/PR) | E/M downcoded from 99215 to 99214 (ENC-2007) |
| **CARC 197** | Pre-certification/authorization/notification/pre-treatment absent | Denial / Authorization (CO) | HMO specialist visits without PCP referral (ENC-2008) |

#### Accompanying Remittance Advice Remark Codes (RARC)
* **RARC N30:** Patient ineligible for this service under plan benefits.
* **RARC N381:** Service denied due to absence of required pre-service referral or authorization.
* **RARC MA01:** Alert: You have the right to appeal this determination within 180 days of this notice.

---

### Educational & Regulatory Disclosures

1. **Simulated Nature of Data:** All patient identifiers, policy numbers, insurance plans, and dollar amounts are entirely synthetic and constructed for educational and demonstration purposes.
2. **Historical Reference Subsets:** Diagnosis and procedure code sets are based on historical **FY 2024 ICD-10-CM** and **CPT 2024** references. They do not represent real-time active clinical guidelines for subsequent fiscal years.
3. **No Legal or Compliance Advice:** This technical workflow documentation reflects standard theoretical industry workflows and should not be construed as legal advice or binding billing counsel.
