# Comprehensive Medical Billing Error Taxonomy
## Classification Standard & CARC/RARC Crosswalk – Week 3 Simulation

---

### 1. Architectural Taxonomy Overview

The **Billing Error Taxonomy** classifies outpatient revenue cycle discrepancies across 4 functional domains, 12 operational subcategories, and standard ANSI ASC X12 Claim Adjustment Reason Codes (CARC) and Remittance Advice Remark Codes (RARC).

```
                            [Medical Billing Error Taxonomy]
                                           │
         ┌──────────────────┬──────────────┴──────────────┬──────────────────┐
         ▼                  ▼                             ▼                  ▼
   [Domain I:         [Domain II:                   [Domain III:       [Domain IV:
    Front-End          Clinical Charting             Coding &           Billing, EDI &
    Registration &     & Documentation]              Specificity]       Financial Ledger]
    Eligibility]
```

---

### 2. Detailed Error Code Specifications & Crosswalk

| Error Code | Error Category Name | Operational Domain | Severity | Primary CARC / RARC | Typical Root Cause |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ERR_ICD_INCORRECT** | Incorrect ICD-10 Diagnosis Code | Coding & Specificity | High | CARC 11, 167; RARC N382 | Coder selected chronic code instead of acute traumatic injury code. |
| **ERR_ICD_SPECIFICITY** | Diagnosis Specificity Mismatch | Coding & Specificity | Medium | CARC 16, 167; RARC M81 | Default selection of unspecified (.9) code despite documented staging. |
| **ERR_CPT_INCORRECT** | Incorrect CPT Procedure Code | Coding & Specificity | High | CARC 4, 16; RARC N56 | New patient preventive code billed for established clinic patient. |
| **ERR_DUPLICATE_BILLING**| Duplicate Procedure Billing | Billing & EDI | High | CARC 18; RARC N522 | Accidental double entry during EHR-PMS batch synchronization. |
| **ERR_EM_UNSUPPORTED** | Unsupported E/M Service Level | Clinical & Coding | High | CARC 150; RARC N34 | High-level Level 5 code billed for self-limited minor condition. |
| **ERR_SIGNATURE_MISSING**| Missing Provider Electronic Signature | Clinical Documentation | Critical | CARC 16; EDI 277CA STC: A7 | Clinician logged off before locking and electronically signing note. |
| **ERR_DOCUMENTATION_MISSING**| Missing Clinical Documentation | Clinical Documentation | Critical | CARC 16, 252; RARC N29 | Surgical CPT charge submitted with zero accompanying operative note. |
| **ERR_SUBSCRIBER_INFO** | Missing Subscriber Information | Front-End Registration | High | CARC 16, 26; EDI 277CA STC: A7 | Minor dependent submitted as primary subscriber without guarantor. |
| **ERR_DEMOGRAPHIC_TYPO**| Demographic Information Mismatch | Front-End Registration | Medium | CARC 16, 31; RARC N245 | Typographical error in date of birth during intake data entry. |
| **ERR_AUTH_REFERRAL_MISSING**| Missing HMO Specialist Referral | Front-End Authorization | High | CARC 197; RARC N381 | Specialist visit scheduled without verifying mandatory PCP referral. |
| **ERR_MEDICAL_NECESSITY**| Medical Necessity Gap (LCD) | Clinical & Coding | High | CARC 50; RARC N115 | Diagnostic X-ray ordered without documented signs/symptoms under LCD. |
| **ERR_MODIFIER_APPLICATION**| Incorrect Modifier Application | Coding & Billing | High | CARC 4, 97; RARC N56 | Failure to append Modifier -25 to significant separate E/M service. |
| **ERR_UNITS_QUANTITY** | Incorrect Units / Quantity Billed | Billing & EDI | High | CARC 151; RARC N362 | Infusion minutes entered as units, violating CMS MUE daily limit. |
| **ERR_COB_ROUTING** | Coordination of Benefits (COB) Error| Front-End Eligibility | High | CARC 22; RARC N103 | Commercial PPO billed as primary for patient 65+ with active Medicare. |
| **ERR_CALCULATION_BALANCE**| Patient Balance Calculation Defect| Financial Ledger | High | INTERNAL_AUDIT_ALERT | Billed patient amount exceeding contractual allowed fee schedule. |
| **ERR_SUBMISSION_REJECTED**| Incomplete Submission / Missing NPI| Billing & EDI | Critical | CARC 16; EDI 277CA STC: A7 | Software dictionary unmapped rendering provider NPI in Loop 2010AA. |
| **QUERY_NO_ERROR** | Auditing Review – No Error Identified| Compliance Auditing | Low | N/A | High E/M audit threshold triggered, but chart proves High MDM. |
| **QUERY_PENDING_DOCS** | Documentation Deficiency – Pending Docs| Clinical Charting | Medium | CARC 16, 252; RARC N29 | High-risk therapy initiated based on outside labs not scanned into EHR. |

---

### 3. Severity Level Definitions

1. **Critical Severity:**
   * Immediate fatal billing block. Claim cannot be transmitted or adjudicated.
   * Causes immediate clearinghouse gateway 277CA rejection or total payment forfeiture.
   * Examples: Unsigned progress note (`ERR_SIGNATURE_MISSING`), missing NPI (`ERR_SUBMISSION_REJECTED`), unrecorded surgery (`ERR_DOCUMENTATION_MISSING`).

2. **High Severity:**
   * Results in formal claim denial on ERA 835 remittance advice or significant financial audit clawback.
   * Represents compliance risks under False Claims Act (e.g., upcoding) or contractual write-off losses.
   * Examples: Missing HMO referral (`ERR_AUTH_REFERRAL_MISSING`), duplicate billing (`ERR_DUPLICATE_BILLING`), unsupported E/M (`ERR_EM_UNSUPPORTED`), balance-billing calculation defect (`ERR_CALCULATION_BALANCE`).

3. **Medium Severity:**
   * Delays cash collection, triggers Additional Documentation Requests (ADRs), or impairs risk-adjustment capture.
   * Solvable via routine administrative correction or demographic cross-matching.
   * Examples: Diagnostic code specificity omission (`ERR_ICD_SPECIFICITY`), date of birth typo (`ERR_DEMOGRAPHIC_TYPO`), pending external consult records (`QUERY_PENDING_DOCS`).

4. **Low Severity (Informational Query):**
   * Pre-bill sampling alerts where clinical and coding review substantiates original billing.
   * Requires auditor documentation but results in zero claim alterations.
   * Examples: Legitimate emergency Level 5 E/M evaluation cleared upon chart inspection (`QUERY_NO_ERROR`).
