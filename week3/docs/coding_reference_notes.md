# Historical Coding Reference Notes & Educational Subsets
## FY 2024 ICD-10-CM & CPT 2024 Educational Reference Guide – Week 3

---

### 1. Regulatory Context & Disclaimers

This educational simulation utilizes historical code subsets derived from the **FY 2024 ICD-10-CM** (effective October 1, 2023 – September 30, 2024) and **CPT® 2024 Standard Edition** (effective January 1, 2024). 

> [!IMPORTANT]
> **Academic Reference Notice:** This reference guide contains curated educational subsets designed to demonstrate billing query resolution. It does not reproduce proprietary CPT codebook text in full, nor does it represent active coding compliance for fiscal years 2026 or 2027.

---

### 2. Diagnostic Coding Rules (FY 2024 ICD-10-CM)

#### A. Traumatic Acute Injury vs. Chronic Derangement
* **Rule:** Traumatic injuries occurring from recent mechanical trauma (e.g., twisting injury during yard work yesterday) must be coded using Chapter 19 Injury codes (`S00–T88`) with a 7th character identifying the episode of care (`A` = initial encounter).
* **Clinical Example (SCN-3001):**
  * *Documented:* Acute lateral meniscus tear of right knee following twisting injury.
  * *Incorrect Billed Code:* `M23.23` (Derangement of meniscus due to old tear or injury, right knee - Chronic).
  * *Compliant Code:* `S83.241A` (Tear of lateral meniscus, current injury, right knee, initial encounter).
  * *Rationale:* Billing `M23.23` for an acute trauma causes medical necessity rejections and improperly classifies an injury as a pre-existing degenerative condition.

#### B. Combination Coding & Manifestation Staging
* **Rule:** When documentation substantiates a diabetic manifestation (e.g., diabetic chronic kidney disease), ICD-10-CM mandates combination coding rather than assigning an unspecified code.
* **Clinical Example (SCN-3002):**
  * *Documented:* Type 2 diabetes with chronic kidney disease, stage 3b (eGFR 38 mL/min).
  * *Incorrect Billed Code:* `E11.9` (Type 2 diabetes mellitus without complications).
  * *Compliant Combination Coding:* `E11.22` (Type 2 diabetes mellitus with diabetic chronic kidney disease) as primary diagnosis, paired with secondary code `N18.32` (Chronic kidney disease, stage 3b).
  * *Rationale:* Code `E11.9` underreports illness severity and omits critical risk-adjustment (HCC) diagnostic capture.

---

### 3. Procedural Coding Rules (CPT 2024)

#### A. Established Patient vs. New Patient Definition
* **Rule:** An established patient is one who has received professional services from the physician, or another physician of the exact same specialty and subspecialty who belongs to the same group practice, within the past three years.
* **Clinical Example (SCN-3003):**
  * *Documented:* 41-year-old male receiving continuous primary care at the clinic for 5 years.
  * *Incorrect Billed Code:* `99385` (Initial comprehensive preventive medicine evaluation and management, 40–64 years).
  * *Compliant Code:* `99395` (Periodic comprehensive preventive medicine evaluation and management, established patient, 40–64 years).
  * *Rationale:* Billing new patient codes for established patients triggers payer downcoding and constitutes non-compliant charge entry.

#### B. Evaluation and Management (E/M) Complexity & MDM Guidelines
* Under 2021/2023 AMA E/M guidelines, code selection for office visits (`99202–99215`) is based solely on **Medical Decision Making (MDM)** or **Total Physician Time** on the date of encounter:
  * **CPT 99213 (Level 3):** Low MDM (2+ minor problems, or 1 stable chronic illness, or 1 acute uncomplicated illness; low risk).
  * **CPT 99214 (Level 4):** Moderate MDM (1+ chronic illness with mild exacerbation, or 2+ stable chronic illnesses, or 1 undiagnosed new problem with uncertain prognosis; moderate risk such as prescription drug management).
  * **CPT 99215 (Level 5):** High MDM (1+ chronic illness with severe exacerbation, or 1 acute/chronic illness posing an immediate threat to life or bodily function; high risk such as emergency transfer or intensive monitoring) OR 40–54 minutes total time.
* **Scenarios in Cohort:**
  * *SCN-3005:* Mild allergic rhinitis, 10 minutes time, minimal risk. Billed `99215`. Downcoded to `99213`.
  * *SCN-3017:* Severe acute chest pain, diaphoresis, acute nitroglycerin, emergency cardiac transfer, 50 minutes physician time. Billed `99215`. **Confirmed fully compliant under High MDM ("No Error Identified")**.

#### C. Minor Surgery and Modifier -25
* **Rule:** A physician may bill an Evaluation and Management service on the same day as a minor surgical procedure (0 or 10-day global period) only if the E/M service represents a significant, separately identifiable medical evaluation addressing a separate clinical problem.
* **Clinical Example (SCN-3012):**
  * *Documented:* Sebaceous cyst excision (CPT 11402) on back. Separately, patient presented with acute onset severe vertigo/nausea, receiving full neurological/vestibular examination and meclizine prescription.
  * *Billed:* `11402` and `99214` without modifier.
  * *Payer Denial:* CARC 97 (Bundled).
  * *Compliant Coding:* `11402` and `99214-25` (Modifier -25 appended to E/M code).
  * *Rationale:* Modifier -25 communicates to payer claims adjudication engines that the E/M evaluation was clinically distinct from routine surgical pre- and post-operative care.

#### D. Medically Unlikely Edits (MUE) & Infusion Coding
* **Rule:** CMS Medically Unlikely Edits (MUE) establish the maximum units of service that a provider would report under most circumstances for a single beneficiary on a single date of service.
* **Clinical Example (SCN-3013):**
  * *CPT 96360:* Intravenous hydration infusion, initial, 31 to 60 minutes.
  * *MUE Limit:* 1 unit per date of service.
  * *Error:* Entering 45 minutes as "4" units resulted in CARC 151 MUE denial and a $520.00 erroneous charge. Corrected to 1 unit ($130.00).
