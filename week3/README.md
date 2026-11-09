# Week 3: Billing Query Resolution and Error Analysis
## Medical Billing Internship Simulation

**Author:** Arnab (Student Project)  
**Academic Module:** Revenue Cycle Management (RCM) & Billing Query Resolution  
**Repository:** [https://github.com/Arnab6911/medical-coding-compliance-audit](https://github.com/Arnab6911/medical-coding-compliance-audit)  
**Historical Coding References:** FY 2024 ICD-10-CM & CPT 2024 (Educational Subsets)  
**Compliance Standard:** All patient records, clinical notes, and financial data are 100% synthetic.

---

## 1. Project Overview & Objective

Week 3 focuses on **Billing Query Resolution and Error Analysis** in healthcare revenue cycle management. While Week 1 covered pre-bill medical coding compliance auditing and Week 2 modeled the 12-stage end-to-end outpatient billing lifecycle, Week 3 establishes an advanced, educational simulation for diagnosing, investigating, resolving, and preventing common outpatient billing discrepancies and claim rejections.

### Core Capabilities:
- **18 Synthetic Scenarios:** 16 distinct billing error categories, 1 fully compliant case (*No Error Identified*), and 1 clinical documentation deficiency case (*Pending Additional Documentation*).
- **Automated Error Detection Engine:** Algorithmic auditing covering missing signatures, duplicate billing, acute vs. chronic coding, diabetic CKD specificity, new vs. established patient codes, unsupported E/M levels, minor subscribers, HMO referral lapses, LCD medical necessity, Modifier -25 bundling, and Medically Unlikely Edits (MUE).
- **Root Cause Analysis (RCA) Engine:** Systematic classification across front-end registration, clinical documentation, medical coding, billing/clearinghouse, and financial accounting.
- **9-Stage Query Resolution Roadmap:** Standard Operating Procedures (SOPs) generating stakeholder communications (provider query memos and payer appeals) without fabrication.
- **Preventive Controls & EHR Safeguards:** Real-time pre-bill scrubbers, EHR hard-stops, and clinical decision support (CDS) rules.
- **Automated Multi-Deliverable Generator:** Produces a 20-section formal Microsoft Word case study report (`Week_3_Billing_Query_Resolution_Report.docx`), an audit findings dataset (`billing_error_analysis.csv`), and a publication-grade 300 DPI workflow diagram (`resolution_workflow.png`).
- **9-Page Interactive Streamlit Dashboard:** Complete web application (`week3/app.py`) for cohort exploration and workflow simulation.

---

## 2. Directory Architecture

```
week3/
├── README.md                                  # Complete technical documentation and scenario guide
├── requirements.txt                           # Week 3 Python dependencies
├── generate_reports.py                        # Standalone CLI report and artifact generator
├── app.py                                     # 9-Page interactive Streamlit dashboard
├── data/
│   ├── billing_scenarios.csv                  # 18 curated fictional billing scenarios
│   └── reference_rules/
│       ├── error_categories.json              # 18-category taxonomy with CARC/RARC mappings
│       └── resolution_rules.json              # Step-by-step SOPs and evidence requirements
├── src/
│   ├── __init__.py                            # Package initialization
│   ├── models.py                              # Dataclasses and Enums
│   ├── scenario_loader.py                     # CSV parser and schema validator
│   ├── error_detector.py                      # Rule-based error detection engine
│   ├── root_cause_analyzer.py                 # RCA engine and risk mapper
│   ├── resolution_engine.py                   # 9-stage query resolution engine
│   ├── preventive_engine.py                   # Preventive controls & EHR hard-stops
│   ├── workflow.py                            # End-to-end simulation orchestrator
│   ├── visualizer.py                          # 300 DPI Matplotlib flowchart generator
│   ├── report_generator.py                    # 20-section python-docx Word compiler
│   └── init_data.py                           # Clean data generator script
├── docs/
│   ├── methodology.md                         # Resolution and audit methodology
│   ├── error_taxonomy.md                      # Detailed error codes & CARC crosswalk
│   ├── troubleshooting_guide.md               # Actionable billing staff troubleshooting SOPs
│   └── coding_reference_notes.md              # Historical reference notes & disclaimers
├── reports/
│   ├── Week_3_Billing_Query_Resolution_Report.docx  # 20-Section Word report (validated)
│   ├── billing_error_analysis.csv             # Exported CSV findings dataset
│   └── resolution_workflow.png                # 300 DPI resolution flowchart diagram
└── tests/
    ├── __init__.py                            # Test package initialization
    ├── test_scenario_loader.py                # Ingestion and schema validation tests
    ├── test_error_detector.py                 # Error detection suite across all 18 cases
    ├── test_resolution_engine.py              # Query resolution workflow tests
    ├── test_prevention_engine.py              # Preventive controls and hard-stops tests
    ├── test_financial_consistency.py          # Mathematical reconciliation tests
    └── test_report_generation.py              # Word docx table margins and PNG tests
```

---

## 3. Scenario Matrix (18 Fictional Encounters)

| Scenario ID | Encounter | Patient Name | Demographics | Payer (Plan) | Error Category Code | Severity | Original Gross | Corrected Gross | Variance | Resolution Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **SCN-3001** | ENC-3001 | Eleanor Vance | 54yo F | BCBS (PPO) | `ERR_SIGNATURE_MISSING` | Critical | $275.00 | $275.00 | $0.00 | Resolved – Documentation Updated |
| **SCN-3002** | ENC-3002 | Marcus Thorne | 62yo M | Aetna (PPO) | `ERR_DUPLICATE_BILLING` | High | $275.00 | $275.00 | $0.00 | Resolved – Corrected Claim |
| **SCN-3003** | ENC-3003 | Samuel Green | 45yo M | UHC (Choice Plus) | `ERR_CPT_INCORRECT` | High | $240.00 | $205.00 | -$35.00 | Resolved – Corrected Claim |
| **SCN-3004** | ENC-3004 | Brenda Ramirez | 58yo F | Cigna (Open Access) | `ERR_DOCUMENTATION_MISSING` | Critical | $130.00 | $65.00 | -$65.00 | Resolved – Corrected Claim |
| **SCN-3005** | ENC-3005 | David Kim | 32yo M | BCBS (HMO) | `ERR_EM_UNSUPPORTED` | High | $395.00 | $185.00 | -$210.00 | Resolved – Corrected Claim |
| **SCN-3006** | ENC-3006 | Chloe Bennett | 7yo F | Humana (PPO) | `ERR_SUBSCRIBER_INFO` | High | $185.00 | $185.00 | $0.00 | Resolved – Corrected Claim |
| **SCN-3007** | ENC-3007 | Robert Hayes | 51yo M | BCBS (PPO) | `ERR_MEDICAL_NECESSITY` | High | $495.00 | $275.00 | -$220.00 | Resolved – Corrected Claim |
| **SCN-3008** | ENC-3008 | Maria Santos | 42yo F | UHC (HMO) | `ERR_AUTH_REFERRAL_MISSING` | High | $185.00 | $185.00 | $0.00 | Pending Provider Query |
| **SCN-3009** | ENC-3009 | Thomas Wright | 68yo M | Aetna (PPO) | `ERR_COB_ROUTING` | High | $185.00 | $185.00 | $0.00 | Resolved – Corrected Claim |
| **SCN-3010** | ENC-3010 | Evelyn Foster | 39yo F | Cigna (PPO) | `ERR_MODIFIER_APPLICATION` | High | $360.00 | $360.00 | $0.00 | Resolved – Corrected Claim |
| **SCN-3011** | ENC-3011 | Jonathan Reed | 29yo M | BCBS (PPO) | `ERR_ICD_INCORRECT` | High | $360.00 | $185.00 | -$175.00 | Resolved – Corrected Claim |
| **SCN-3012** | ENC-3012 | Patricia Miller | 63yo F | Medicare Part B | `ERR_ICD_SPECIFICITY` | Medium | $535.00 | $535.00 | $0.00 | Resolved – Corrected Claim |
| **SCN-3013** | ENC-3013 | Anthony Davis | 48yo M | UHC (PPO) | `ERR_UNITS_QUANTITY` | High | $520.00 | $130.00 | -$390.00 | Resolved – Corrected Claim |
| **SCN-3014** | ENC-3014 | Hannah Wilson | 26yo F | Humana (PPO) | `ERR_DEMOGRAPHIC_TYPO` | Medium | $185.00 | $185.00 | $0.00 | Resolved – Corrected Claim |
| **SCN-3015** | ENC-3015 | Charles Robinson | 56yo M | BCBS (PPO) | `ERR_SUBMISSION_REJECTED` | Critical | $185.00 | $185.00 | $0.00 | Resolved – Corrected Claim |
| **SCN-3016** | ENC-3016 | Gary Taylor | 61yo M | Aetna (PPO) | `ERR_CALCULATION_BALANCE` | High | $260.00 | $260.00 | $0.00 | Resolved – Corrected Claim |
| **SCN-3017** | ENC-3017 | Arthur Pendelton | 66yo M | Medicare Part B | `QUERY_NO_ERROR` | Low | $395.00 | $395.00 | $0.00 | No Error Identified |
| **SCN-3018** | ENC-3018 | Laura Hughes | 44yo F | UHC (Choice Plus) | `QUERY_PENDING_DOCS` | Medium | $275.00 | $275.00 | $0.00 | Pending Additional Documentation |
| **TOTAL** | — | **18 Scenarios** | — | — | — | — | **$5,440.00** | **$4,345.00** | **-$1,095.00** | **83.3% Clean Resolution** |

---

## 4. Empirical Financial Reconciliation

Across the 18 scenarios, 6 encounters required Chargemaster gross charge adjustments:
1. **SCN-3003 (-$35.00):** CPT 99385 ($240.00) adjusted to established patient code CPT 99395 ($205.00).
2. **SCN-3004 (-$65.00):** Omitted surgical biopsy CPT 11102 ($65.00) removed from claim.
3. **SCN-3005 (-$210.00):** Unsupported Level 5 E/M 99215 ($395.00) downcoded to Level 3 E/M 99213 ($185.00).
4. **SCN-3007 (-$220.00):** Non-covered screening chest X-ray CPT 71046 ($220.00) removed due to LCD policy gap.
5. **SCN-3011 (-$175.00):** Traumatic injury E/M charge adjusted from $360.00 to supported code $185.00.
6. **SCN-3013 (-$390.00):** IV hydration CPT 96360 corrected from 4 units ($520.00) to 1 unit ($130.00) per MUE limit.

**Cohort Balance Identity:**  
$$\text{Gross Initial Billed} - \text{Gross Corrected Billed} = |\text{Net Financial Variance}|$$  
$$\$5,440.00 - \$4,345.00 = \$1,095.00$$

---

## 5. 9-Stage Query Resolution Workflow

The resolution engine implements a structured 9-stage standard operating procedure:
1. **Query Identification:** Log ticket with unique identifier, encounter ID, and error category.
2. **Source Record Review:** Inspect patient intake, appointment history, and registration ledger.
3. **Supporting Documentation Verification:** Extract and analyze clinical progress notes, diagnostic tracings, and nursing flowsheets.
4. **Applicable Rule Evaluation:** Cross-reference official FY 2024 ICD-10-CM guidelines, CPT 2024 rules, CMS LCD/NCD coverage policies, and NCCI edit manuals.
5. **Corrective Action Plan Formulation:** Specify whether coding replacement, modifier application, downcoding, or charge voiding is indicated.
6. **Provider / Payer Stakeholder Communication:** Generate non-fabricated provider queries or formal payer appeal justifications.
7. **Claim Adjustment & Resubmission:** Generate replacement EDI 837P claim (Frequency Code 7), void duplicate line, or release billing hold.
8. **Final Validation Check:** Execute pre-submission claim scrubber ensuring zero fatal syntax or coverage edits.
9. **Resolution Outcome & Ledger Reconciliation:** Finalize claim status, adjust patient accounting ledger, and log preventive control.

---

## 6. Quick Start & Execution Commands

### A. Run Deliverables Generator CLI
Generates the 20-section Word report, exports the CSV audit dataset, renders the 300 DPI flowchart, and validates document formatting programmatically:
```bash
python week3/generate_reports.py
```

### B. Launch Streamlit Interactive Application
Launches the 9-page interactive revenue cycle workbench:
```bash
streamlit run week3/app.py
```

### C. Run Automated Test Suite
Executes all 41 Week 3 pytest unit tests:
```bash
python -m pytest week3/tests/ -v
```

### D. Verify Repository Isolation & Prior Weeks
Confirms that Week 1 (17 tests) and Week 2 (31 tests) remain 100% functional and untouched:
```bash
python -m pytest tests/ -v
python -m pytest week2/tests/ -v
```

---

## 7. Deliverables & Artifact Verification

| Deliverable | File Path | Status | Verification Summary |
| :--- | :--- | :---: | :--- |
| **Word Case Study Report** | `week3/reports/Week_3_Billing_Query_Resolution_Report.docx` | Verified | 20 Formal sections, student project cover page, all 7 tables validated strictly to 6.50" margins. |
| **Audit Findings CSV** | `week3/reports/billing_error_analysis.csv` | Verified | 18 Comprehensive scenario rows, 25 columns, exact financial reconciliation. |
| **Resolution Flowchart** | `week3/reports/resolution_workflow.png` | Verified | 300 DPI publication-grade diagram illustrating the 9-stage resolution workflow. |
| **Streamlit Dashboard** | `week3/app.py` | Verified | 9 interactive pages tested via `AppTest` with zero runtime exceptions. |
| **Pytest Unit Suite** | `week3/tests/` | Verified | 41 automated tests covering loader, detector, RCA, resolution, prevention, and financials. |

---

## 8. Compliance & Educational Disclaimers

> [!NOTE]
> **Educational Reference Subset:** This project utilizes historical, curated subsets of the FY 2024 ICD-10-CM and CPT 2024 coding references for instructional simulation. It does not claim compliance with current FY 2026/FY 2027 coding updates.

> [!IMPORTANT]
> **Synthetic Data Protection:** All patient identities, encounter dates, clinician names, and insurance account numbers are entirely fictional. Any similarity to actual persons or clinical events is strictly coincidental. Automated audit flags indicate compliance review thresholds and do not represent definitive findings of fraud or non-reimbursement.
