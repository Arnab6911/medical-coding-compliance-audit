# Medical Coding Compliance Audit - Validation Rules Specification

## 1. Rule Architecture & Separation of Concerns

The compliance audit engine maintains a strict separation between **business validation logic**, **reference code dictionaries**, and **regulatory thresholds**:

```
data/rules/
├── icd10_codes_fy2024.json     <- Version-aware ICD-10-CM FY 2024 reference subset
├── cpt_codes_2024.json         <- Version-aware CPT 2024 reference subset
└── audit_rules_config.json     <- Configurable thresholds and official citations

src/
├── rules_engine.py             <- Modular validation functions evaluating records
└── reference_data.py           <- Loads and accesses versioned rules data
```

### Version Awareness & Code Set Metadata
All reference files explicitly document their release fiscal year and publishing body:
- **ICD-10-CM:** FY 2024 Educational Standard Subset (CMS / NCHS, Released Oct 1, 2023 / Effective FY 2024)
- **CPT:** 2024 Educational Standard Reference (AMA, Effective Jan 1, 2024)
- **Rules Config:** Engine Version 2024.1

No fictitious codes are claimed to be valid. Any code outside the reference database is classified as *Unverified Reference Code* requiring manual verification against official tabular indices.

---

## 2. Complete Rule Catalog

### R-01: Missing Clinical Documentation Notes
- **Issue Type:** Missing Clinical Documentation
- **Default Severity:** `High`
- **Trigger:** Assigned codes (ICD-10 or CPT) are present, but the `Clinical_Documentation` chart note field is completely empty.
- **Compliance Rationale:** Billing services without progress notes violates False Claims Act and Conditions of Payment.
- **Recommended Action:** Locate and append signed encounter progress note or withdraw claim from clearinghouse.
- **Citation:** *Medicare Program Integrity Manual (Pub. 100-08) Chapter 3 §3.3.2.4.*

---

### R-02: Missing Diagnosis Documentation
- **Issue Type:** Missing Diagnosis Documentation
- **Default Severity:** `High`
- **Trigger:** Assigned ICD-10 code is present on the encounter, but `Documented_Diagnosis` is empty or missing from clinical chart notes.
- **Compliance Rationale:** Billing diagnosis codes without clinical documentation violates fundamental billing rules.
- **Recommended Action:** Query attending provider to obtain diagnostic assessment or remove unsupported code.
- **Citation:** *ICD-10-CM Official Guidelines for Coding and Reporting FY 2024, Section I.B.1.*

---

### R-03: Diagnosis Code Mismatch
- **Issue Type:** Diagnosis Code Mismatch
- **Default Severity:** `High`
- **Trigger:** Documented condition (e.g., Essential Hypertension) does not match the clinical definition or keywords of the assigned ICD-10 code (e.g., E11.9 Type 2 Diabetes).
- **Compliance Rationale:** Mismatched diagnosis codes distort clinical history, alter risk adjustment scores (HCCs), and lead to claim rejections.
- **Recommended Action:** Review clinical note, align assigned ICD-10-CM code to the documented condition, or initiate a physician query.
- **Citation:** *ICD-10-CM Official Guidelines for Coding and Reporting FY 2024, Section I.A.19.*

---

### R-04: Unverified Reference Code Detection
- **Issue Type:** Unverified Reference Code
- **Default Severity:** `Medium`
- **Trigger:** Assigned ICD-10 or CPT code is not present in the verified active reference dataset (e.g., `Z99.999`).
- **Compliance Rationale:** Unverified or outdated codes cause immediate payer clearinghouse rejections.
- **Recommended Action:** Manually verify code validity against current fiscal year ICD-10-CM Tabular Index or AMA CPT Standard Edition.
- **Citation:** *ICD-10-CM Official Guidelines Section I.A.19 & AMA CPT Instructions.*

---

### R-05: Incomplete Clinical Documentation
- **Issue Type:** Incomplete Clinical Documentation
- **Default Severity:** `High` (if note < 5 words) / `Medium` (if note < 15 words)
- **Trigger:** Clinical documentation notes contain fewer than 15 words (e.g., "Meds refilled."), failing to establish history, examination, or medical decision making.
- **Compliance Rationale:** Medicare Condition of Payment requires notes to be legible and clinically sufficient to justify the care billed.
- **Recommended Action:** Request clinician addendum detailing encounter elements before claim submission.
- **Citation:** *Medicare Program Integrity Manual (Pub. 100-08) Chapter 3 §3.3.2.4.*

---

### R-06: Missing Provider Signature & Authentication
- **Issue Type:** Missing Provider Signature
- **Default Severity:** `Medium`
- **Trigger:** Documentation note lacks an authenticated provider electronic signature, date/timestamp, or credential (e.g., "Electronically signed by Dr. X, MD").
- **Compliance Rationale:** Unauthenticated medical records fail Medicare conditions of payment and are vulnerable to 100% technical claim recoupment during payer audits.
- **Recommended Action:** Route record back to authoring clinician for electronic signature completion.
- **Citation:** *CMS Medicare Learning Network (MLN) Matters Article MM6698.*

---

### R-07: Duplicate Diagnosis & Procedure Detection
- **Issue Type:** Duplicate Diagnosis Entry / Duplicate Procedure Entry
- **Default Severity:** `Medium`
- **Trigger:** Identical ICD-10 code or identical CPT code is billed more than once on the same encounter date for the same patient (e.g., `I10; I10` or `99213; 99213`).
- **Compliance Rationale:** Duplicate codes cause billing clearinghouse rejections and payer scrub errors.
- **Recommended Action:** Consolidate redundant diagnosis entries to report the code once, or append distinct CPT modifiers (e.g. 76/59) if multiple procedures were performed.
- **Citation:** *CMS Medicare Claims Processing Manual (Pub. 100-04) Chapter 23 §10 & NCCI Policy Manual Chapter 1 §B.*

---

### R-08: Unsupported Procedure Coding & Medical Necessity
- **Issue Type:** Unsupported Procedure Coding
- **Default Severity:** `High`
- **Trigger:**
  1. Invasive/diagnostic CPT code (e.g., 45378 Colonoscopy, 71046 Chest X-Ray, 93000 ECG) billed without any procedure note or findings documented in the clinical chart.
  2. Assigned CPT code lacks medical necessity support from the primary diagnosis (e.g., Colonoscopy billed with Pharyngitis J02.9).
- **Compliance Rationale:** Billing for services without documentation or medical necessity is considered improper billing under federal compliance standards.
- **Recommended Action:** Obtain standalone procedure report or remove unperformed CPT code from the claim.
- **Citation:** *Social Security Act §1862(a)(1)(A) & CMS Pub 100-02 Chapter 15 §20.*

---

### R-09: Unsupported High-Level E/M Coding
- **Issue Type:** Unsupported E/M Level
- **Default Severity:** `High`
- **Trigger:** Level 5 outpatient E/M code (CPT 99215 or 99205) assigned for uncomplicated conditions (e.g., simple back strain, routine refill) or without documentation of high-complexity Medical Decision Making (MDM) or qualifying total time (40-54 minutes for 99215).
- **Compliance Rationale:** Level 5 visits are heavily targeted by OIG Work Plans and Medicare RAC audits for systemic overcoding.
- **Recommended Action:** Downcode to supported E/M level (e.g. 99213 or 99214) or request physician addendum substantiating qualifying time or high complexity.
- **Citation:** *AMA CPT 2024 E/M Guidelines & CMS 2021/2023 Outpatient E/M Documentation Revisions.*

---

### R-10: Unspecified Code Usage Warning
- **Issue Type:** Unspecified Code Warning
- **Default Severity:** `Low`
- **Trigger:** Unspecified code (e.g., M17.9 Knee Osteoarthritis Unspecified) is billed when the clinical documentation explicitly records laterality (e.g., Right knee, Left knee).
- **Compliance Rationale:** Commercial payers frequently deny unspecified codes when documentation supports a specific code.
- **Recommended Action:** Update code to specified laterality (e.g., M17.11 for right knee osteoarthritis).
- **Citation:** *ICD-10-CM Official Guidelines Section I.B.18.*

---

## 3. Severity Matrix

| Severity | Color Code | Operational Meaning | Action Timeline |
|---|---|---|---|
| **High** | Crimson (`#DC2626`) | Critical compliance violation, False Claims Act exposure, or total lack of medical necessity. | Mandatory pre-bill stop. Immediate human auditor review required. |
| **Medium** | Amber (`#F59E0B`) | Technical defect, missing clinician signature, unverified code, or duplicate code. | Hold claim for provider query or documentation addendum. |
| **Low** | Blue (`#3B82F6`) | Specificity optimization, unspecified code warning. | Post-bill educational feedback / coding refinement. |

---

## 4. Distinction: Automated Flag vs Confirmed Error

An automated flag represents a **potential discrepancy identified for human auditor evaluation**. It is not a legal or definitive confirmation of coding error. 

A certified compliance auditor must always evaluate the full clinical context, review physician queries, and make the final adjudication. The software preserves the integrity of patient records by **never automatically altering assigned codes**.
