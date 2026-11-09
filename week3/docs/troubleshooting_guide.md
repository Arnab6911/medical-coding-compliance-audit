# Outpatient Billing Staff Troubleshooting Guide
## Standard Operating Procedures (SOP) for Query Resolution & Denial Management

---

### Purpose & Structure

This troubleshooting guide provides ambulatory billing specialists, revenue cycle coordinators, and coding auditors with step-by-step procedures for diagnosing and resolving the most common outpatient billing errors.

For each error type, follow the 8-point operational workflow:
1. **Recognition:** How the error appears on clearinghouse 277CA reports, ERA 835 remittances, or pre-bill scrubbers.
2. **Investigation Location:** Where in the EHR or Practice Management (PM) system to look.
3. **Records to Check:** Which specific documents and files to inspect.
4. **Diagnostic Questions:** Critical inquiries to identify the exact breakdown.
5. **Required Evidence:** Substantiating records necessary before altering billing.
6. **Correction Procedure:** Exact operational steps to correct the ledger or claim.
7. **Escalation Triggers:** When to route the issue to physician advisors or compliance officers.
8. **Recurrence Prevention:** Systemic controls to implement.

---

### Category 1: CARC 18 – Duplicate Procedure Line Submission

* **1. Recognition:** Payer ERA 835 remittance denies Line 2 with CARC 18 (*"Exact duplicate service"*), or pre-bill scrubber flags duplicate CPT on same DOS.
* **2. Investigation Location:** Practice Management Charge Entry module and encounter billing ledger.
* **3. Records to Check:** Diagnostic tracing/report, operative log, physician appointment schedule.
* **4. Diagnostic Questions:**
  * Did the clinician perform two clinically separate procedures (e.g., bilateral lesions or repeat ECG post-treatment)?
  * If separate, is there clear chart documentation detailing distinct clinical times or anatomical sites?
  * Was this an accidental double keying or dual-interface sync glitch?
* **5. Required Evidence:** Documented clinical narrative proving a single procedure was executed, or separate operative notes proving distinct procedures.
* **6. Correction Procedure:**
  * If single service: Void duplicate line in PM ledger. Post write-off for duplicate charge. Refund any patient copay collected in duplicate.
  * If distinct service: Append appropriate modifier (e.g., Modifier 59, 76, or XS) to Line 2 with supporting notes and resubmit.
* **7. Escalation Triggers:** Escalate if multiple claims across the practice exhibit duplicate line spikes, indicating an EHR-to-PM interface integration bug.
* **8. Recurrence Prevention:** Configure PM pre-bill scrubber with automated duplicate charge suppression interlocks.

---

### Category 2: CARC 197 – Missing HMO Referral / Prior Authorization

* **1. Recognition:** Payer ERA 835 denies specialist service with CARC 197 (*"Pre-certification/authorization/notification/referral absent"*).
* **2. Investigation Location:** Payer portal, PM Authorization Module, and incoming fax/EHR referral queue.
* **3. Records to Check:** PCP referral letter, insurance eligibility verification (EDI 271), payer HMO operating manual.
* **4. Diagnostic Questions:**
  * Did the patient's PCP issue a referral prior to the encounter that was simply not linked in the PM system?
  * Was the patient aware of HMO network restrictions at intake?
  * Does the payer permit retroactive referral requests within timely filing limits (e.g., within 14 days)?
* **5. Required Evidence:** PCP referral form, consultation report transmitted to PCP, confirmation of active HMO enrollment on DOS.
* **6. Correction Procedure:**
  * If referral exists: Enter referral number in Loop 2300 of the 837P claim and submit replacement claim.
  * If referral was missing: Submit urgent retroactive referral appeal to PCP office with clinical chart notes.
  * If referral is denied: Write off charge under in-network HMO contract. **Do not bill patient** (patient is held harmless under contractual managed care agreements).
* **7. Escalation Triggers:** Escalate to Contracting Department if payer repeatedly denies claims where timely referrals were confirmed on payer portals.
* **8. Recurrence Prevention:** Implement electronic scheduling gatekeeper blocking specialist booking without confirmed referral number.

---

### Category 3: CARC 150 – Unsupported Evaluation and Management (E/M) Service Level

* **1. Recognition:** Payer ERA 835 downcodes Level 5 E/M (CPT 99215) to Level 3 (CPT 99213) with CARC 150 (*"Payer deems the information submitted does not support this level of service"*).
* **2. Investigation Location:** EHR clinical progress note and provider coding history.
* **3. Records to Check:** Attending SOAP progress note, laboratory/diagnostic orders, medication administration records, total face-to-face physician time logs.
* **4. Diagnostic Questions:**
  * Does documented Medical Decision Making (MDM) demonstrate High complexity across 2 of 3 categories (extensive problems, extensive data, high risk)?
  * If coded on time, does the note document 40–54 minutes of physician face-to-face time with specific activities detailed?
  * Was a brief note inadvertently templated with a Level 5 code?
* **5. Required Evidence:** Clinical note narrative, AMA 2024 MDM scoring worksheet, time documentation.
* **6. Correction Procedure:**
  * If chart supports Level 5: Submit formal redetermination appeal with progress note and AMA MDM scoring letter.
  * If chart supports only Level 3: Accept payer downcoding. Update internal billing ledger to reflect CPT 99213 ($185.00). Send educational notification to clinician.
* **7. Escalation Triggers:** Escalate to Physician Compliance Officer if a provider exhibits >15% Level 5 coding frequency across routine ambulatory visits.
* **8. Recurrence Prevention:** Deploy EHR smart documentation tools calculating MDM level based on documented clinical data.

---

### Category 4: EDI 277CA – Unauthenticated Progress Note / Missing Signature

* **1. Recognition:** Clearinghouse 277CA gateway rejection with Status Category Code STC: A7, or pre-bill scrubber fatal error ERR-003.
* **2. Investigation Location:** EHR Incomplete Chart Workqueue / Physician Inbox.
* **3. Records to Check:** Clinical encounter document status, provider electronic signature audit log.
* **4. Diagnostic Questions:**
  * Did the attending provider finalize the encounter?
  * Is the note marked "Draft", "Preliminary", or "Awaiting Signature"?
  * Has the provider left the practice or is currently on leave?
* **5. Required Evidence:** Cryptographically authenticated electronic signature with date and time stamp matching rendering clinician NPI.
* **6. Correction Procedure:**
  * Place immediate billing hold in PM system.
  * Route urgent task to provider in EHR requesting review and signature.
  * Once authenticated, verify note status shifts to "Final / Locked". Release claim for electronic submission.
* **7. Escalation Triggers:** Escalate to Clinical Department Chair if progress notes remain unsigned beyond 72 hours post-encounter.
* **8. Recurrence Prevention:** Configure EHR to prohibit charge capture release until progress notes are locked and signed.

---

### Category 5: CARC 97 – Missing Modifier -25 on Separate E/M Service

* **1. Recognition:** Payer denies Evaluation & Management code (e.g., CPT 99214) with CARC 97 (*"Payment adjusted because the benefit for this service is included in the payment for another service"*).
* **2. Investigation Location:** Progress note and minor procedural operative report on same date of service.
* **3. Records to Check:** Minor surgical note (e.g., cyst excision 11402) and E/M evaluation note.
* **4. Diagnostic Questions:**
  * Did the clinician evaluate a distinct, significant medical condition above and beyond normal pre/post-procedure care?
  * Does the E/M narrative stand alone with its own subjective history, examination, and treatment plan?
* **5. Required Evidence:** Progress note documenting separate diagnosis (e.g., acute vertigo) distinct from surgical site.
* **6. Correction Procedure:**
  * Append Modifier -25 to E/M code (e.g., CPT 99214-25).
  * Submit corrected electronic claim (EDI 837P Claim Frequency 7) or administrative appeal with progress notes attached.
* **7. Escalation Triggers:** Escalate if payer denies Modifier -25 claims across all providers, violating CMS NCCI guidelines.
* **8. Recurrence Prevention:** Configure pre-bill claim scrubber to check dual-service encounters (surgery + E/M) for Modifier -25.

---

### Category 6: CARC 22 – Coordination of Benefits (COB) Payer Hierarchy Error

* **1. Recognition:** Payer denies claim under CARC 22 (*"This care may be covered by another payer per coordination of benefits"*).
* **2. Investigation Location:** PM Payer Hierarchy Master, patient demographic profile, and Medicare eligibility records.
* **3. Records to Check:** Patient Medicare card, commercial policy card, Medicare Secondary Payer (MSP) questionnaire.
* **4. Diagnostic Questions:**
  * Has the patient turned 65 and enrolled in Medicare Part B?
  * Is the commercial insurance an active employer group health plan (>20 employees) or a retiree secondary plan?
* **5. Required Evidence:** Signed Medicare Secondary Payer questionnaire, EDI 271 eligibility confirmation of primary Medicare Part B.
* **6. Correction Procedure:**
  * Re-order insurance hierarchy in PM system: Set Medicare Part B as Primary, commercial PPO as Secondary.
  * Transmit initial 837P claim to Medicare Part B.
  * Upon receipt of Medicare 835 remittance, bill commercial secondary plan with Medicare payment details attached.
* **7. Escalation Triggers:** Escalate to Patient Access Supervisor if registration staff fail to identify Medicare enrollment at patient intake.
* **8. Recurrence Prevention:** Mandate annual COB/MSP screening questionnaires for all patients aged 64.5 and older at check-in.
