# Vendor Research Notes: Public Capabilities & Official Citations

**Medical Billing & Practice Management Software Market Research**  
*Research Conducted:* November 9, 2026 | *Internship Project:* Week 4  

---

## 1. athenahealth athenaOne

### Vendor Overview
- **Company:** athenahealth, Inc. (Watertown, MA).
- **Core Architecture:** Unified cloud-based healthcare platform uniting clinical documentation (`athenaClinicals`), practice management and medical billing (`athenaCollector`), and patient engagement (`athenaCommunicator`).
- **Clearinghouse Model:** Built-in proprietary clearinghouse integrated directly into the `athenaNet` network. Continuous cloud-wide payer rules maintained and updated by athenahealth network operations. No external clearinghouse subscription required.

### Verified Public Capabilities
- **Electronic Claims & EDI:** Native generation and direct electronic transmission of ASC X12 837P professional claims. Ingestion and auto-posting of ASC X12 835 Remittance Advice with automated contractual write-offs and secondary crossover routing.
- **Eligibility Verification:** Automated pre-service X12 270 eligibility checks scheduled at 72 hours, 48 hours, and 24 hours prior to appointment; real-time on-demand 270 inquiry at front-desk check-in.
- **API & Interoperability:** Publicly accessible Developer Portal (`https://developer.athenahealth.com`) offering documented RESTful APIs and certified HL7 FHIR R4 endpoints. Sandbox access provided without upfront developer fees.
- **Security & Certifications:** HITRUST CSF Certified, SOC 2 Type II compliant, HIPAA compliant, role-based access control, TLS 1.3 encryption in transit, AES-256 encryption at rest.

### Commercial & Implementation Model (Requires Vendor Confirmation)
- **Pricing Structure:** Collections-percentage model (typically 4% to 7% of net collected collections) plus baseline software platform fee (~$140/provider/month).
- **Implementation:** Structured onboarding with dedicated project manager, athenaHealth University LMS, and data conversion pipelines for CCDA, demographic CSV, and open AR ledgers. Implementation fees range from $15,000 to $40,000+ depending on practice size and specialty scope. Custom quote required.
- **Official URLs:**
  - `https://www.athenahealth.com/solutions/medical-billing`
  - `https://www.athenahealth.com/solutions/practice-management`
  - `https://developer.athenahealth.com`
  - `https://www.athenahealth.com/trust-and-security`

---

## 2. AdvancedMD

### Vendor Overview
- **Company:** AdvancedMD, Inc. (South Jordan, UT).
- **Core Architecture:** Cloud-hosted practice management and EHR suite built natively on Amazon Web Services (AWS) healthcare cloud infrastructure.

### Verified Public Capabilities
- **Billing & Practice Management:** Central scheduling, electronic charge capture, customizable electronic charge slips, unbilled encounter tracking, and AdvancedClaim pre-bill scrubbing engine with automated NCCI and payer edit checks.
- **Clearinghouse Model:** Integrated multi-clearinghouse architecture via strategic partnerships with Waystar and Change Healthcare / Optum.
- **Eligibility & Remittance:** Scheduled batch eligibility verification and real-time on-demand benefit breakdown; automated matching and posting of X12 835 ERAs.
- **Reporting & Analytics:** `AdvancedInsight` reporting engine featuring customizable financial reports, visual KPI dashboards, drill-down financial cube, and automated report scheduling.
- **Security & Certifications:** AWS healthcare cloud hosting, SOC 2 Type II audited, HIPAA Security Rule compliant, role-based user permissions.

### Commercial & Implementation Model
- **Pricing Structure:** Transparent published tiered SaaS subscription pricing starting at $429/provider/month (PM only), $729/provider/month (PM + EHR), up to $1,070+/provider/month for complete suite. Optional full outsourced RCM service available at 4% to 8% of collections.
- **API Access (Requires Confirmation):** RESTful API library available through formal Integration Partner Program; requires developer license agreement, partner application review, and non-disclosure agreement (NDA).
- **Official URLs:**
  - `https://www.advancedmd.com/medical-billing-software`
  - `https://www.advancedmd.com/pricing`
  - `https://www.advancedmd.com/integrations`
  - `https://www.advancedmd.com/cloud-solutions`

---

## 3. Tebra

### Vendor Overview
- **Company:** Tebra, Inc. (Formed from the merger of Kareo and PatientPop, Newport Beach, CA).
- **Core Architecture:** Integrated practice growth and clinical/billing suite uniting Kareo Practice Management/Billing with PatientPop digital front-door and patient engagement.

### Verified Public Capabilities
- **Billing & Practice Management:** Intuitive calendar scheduling, smart charge capture templates, missing encounter tracking, electronic superbills, and mobile provider charge entry.
- **Clearinghouse Model:** Integrated clearinghouse connectivity primarily utilizing TriZetto Provider Solutions (Cognizant).
- **Eligibility & Remittance:** Automated daily batch eligibility verification and real-time checks; automated ERA 835 receipt and batch posting.
- **Patient Engagement:** Digital intake forms, online appointment booking, SMS reminders, and self-service patient payment portal.
- **Security & Certifications:** HIPAA compliant cloud infrastructure, SOC 2 Type II certified, encrypted data storage.

### Commercial & Implementation Model (Requires Vendor Confirmation)
- **Pricing Structure:** Quote-based modular pricing depending on bundle selection (Practice Essentials, Practice Automation, Full RCM). Estimated entry cost range: $100 to $500/provider/month.
- **API Access:** REST API program available for verified partners and third-party developers through Tebra Partner Network; quote and partnership approval required.
- **Official URLs:**
  - `https://www.tebra.com/billing-software`
  - `https://www.tebra.com/pricing`
  - `https://www.tebra.com/partners`
  - `https://www.tebra.com/security`
