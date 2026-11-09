# Regulatory Code Governance & Query Ethics Policy

**Code Set Versioning, Pre-Bill Scrubbing, and Provider Clarification Standards**  
*Document Version:* 1.0 | *Practice:* Evergreen Valley Family Medicine & Multi-Specialty Clinic  

---

## 1. Annual & Mid-Year Code Release Governance

Healthcare code sets are dynamic regulatory systems governed by the Centers for Medicare & Medicaid Services (CMS), the American Medical Association (AMA), and the National Center for Health Statistics (CDC NCHS).

### The Three Core Governance Windows
1. **Annual ICD-10-CM Update (Effective: October 1):**
   - *August 1 – 15:* Download CMS/CDC NCHS Tabular and Index releases, code conversion tables, and addenda.
   - *August 16 – September 15:* Ingest new, revised, and invalid codes into the staging rules engine. Execute automated regression tests across historical encounter templates.
   - *September 16 – 30:* Distribute specialty crosswalk guides to providers and certified coders. Conduct crosswalk training webinars.
   - *October 1 (00:00 Hours):* Deploy production rule update.
2. **Annual CPT / HCPCS Level II Update (Effective: January 1):**
   - *November 1 – 30:* Ingest AMA CPT code set release and CMS HCPCS Level II updates. Update practice chargemaster pricing and fee schedules.
   - *December 1 – 20:* Review E/M guideline changes, telemedicine code modifiers, and deleted descriptors. Test pre-bill scrubbing rules against AMA CPT descriptor changes.
   - *January 1 (00:00 Hours):* Deploy production rule update.
3. **Quarterly NCCI & MUE Edits (Effective: Jan 1, Apr 1, Jul 1, Oct 1):**
   - *15 Days Prior to Quarter Start:* Ingest CMS National Correct Coding Initiative (NCCI) Procedure-to-Procedure (PTP) and Medically Unlikely Edit (MUE) tables.
   - Update pre-bill scrubbing rule engine modifier bypass tables (`-25`, `-59`, `-X{EPSU}`).

### Date of Service (DOS) Gating Principle
The pre-bill scrubber evaluates code validity strictly based on encounter **Date of Service (DOS)**, not the claim submission or generation date:
- For encounters occurring in calendar year 2026 prior to October 1, 2026 (e.g., September 30, 2026), FY2026 ICD-10-CM codes apply, even if billed on or after October 1.
- For encounters occurring on or after October 1, 2026, FY2027 ICD-10-CM codes apply; deleted codes result in immediate HARD_STOP blocks.
- CPT/HCPCS code sets and Evaluation and Management (E/M) complexity guidelines must be verified against the encounter date of service (effective January 1 annually) and authorized CPT guidance (without reproducing proprietary code text).

---

## 2. Ethical Provider Clarification Query Protocol

The practice adheres strictly to the joint **AHIMA & ACDIS Guidelines for Achieving a Compliant Query Practice (2022 Update)**.

### Core Non-Leading Principles
- **Non-Leading Formulation:** Queries must present clinically plausible alternatives based on existing chart evidence and must never steer the clinician toward a specific high-paying code.
- **No Financial Mentions:** Queries must never reference reimbursement rates, RVU values, payer coverage policies, or denial prevention.
- **Provider Autonomy:** The clinician retains absolute clinical discretion to clarify, corroborate, or decline documentation additions.
- **Permanent Record Integration:** All queries, provider responses, and note addenda become permanent parts of the authenticated legal health record.

### Standardized Clarification Triggers
1. **Clinical Specificity:** Documented condition lacks anatomical laterality or disease staging (e.g., specifying Chronic Kidney Disease Stage 3a vs Stage 4).
2. **Conflicting Documentation:** Discrepancies between progress note narrative, nursing intake notes, and laboratory results.
3. **Medical Necessity & Secondary Indications:** High-level E/M or procedure where clinical indications are mentioned in history but omitted from formal assessment/plan.
