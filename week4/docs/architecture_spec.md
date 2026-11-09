# Proposed Technical Architecture Specification

**Healthcare IT Integration Specification – 7-Tier Cloud RCM Continuum**  
*Document Version:* 1.0 | *Practice:* Evergreen Valley Family Medicine & Multi-Specialty Clinic  

---

## 1. Architectural Overview & Tiers

The proposed architecture organizes data flows into 7 interconnected, secure tiers:

```text
[Tier 1: Patient Access]  ──(Demographics / 270/271)──>  [Tier 2: Clinical EHR]
                                                                  │
                                                        (Superbill & Progress Note)
                                                                  ▼
[Tier 4: Practice Management] <──(Clean Claims)── [Tier 3: Pre-Bill Rules Scrubber]
        │
    (837P Claims)
        ▼
[Tier 5: Clearinghouse Gateway] ──(835 Remittance)──> [Tier 6: Payment Posting & Portal]
        │                                                              │
        └──────────────(Ledgers & Audit Trail Logs)────────────────────┘
                                       │
                                       ▼
                       [Tier 7: Executive RCM Analytics]
```

---

## 2. Interface Standards & Transaction Protocols

### ASC X12 EDI Transactions
- **X12 270 / 271 (Health Care Eligibility Benefit Inquiry & Response):**
  - Trigger: Automated nightly batch (72h, 24h before appointment) and ad-hoc front-desk check-in.
  - Payload: Subscriber ID, Group ID, Date of Service, Service Type Code (`30` for Health Benefit Plan Coverage).
  - Validation: Active policy status, copay amount, deductible balance, and primary care provider (PCP) assignment.
- **X12 837P (Health Care Claim: Professional v5010):**
  - Trigger: Automated daily batch dispatch at 18:00 hours following scrubber approval.
  - Content: Header, Billing Provider NPI, Subscriber/Patient Demographics, Diagnosis Pointers, Service Line CPT/HCPCS codes, Modifiers, Billed Charges, and Units.
- **X12 276 / 277 & 277CA (Claim Status Request & Claim Acknowledgment):**
  - Ingested automatically within 2 hours of clearinghouse receipt to identify claim acceptance or early EDI rejections.
- **X12 835 (Health Care Claim Payment / Remittance Advice v5010):**
  - Received daily from payers; automatically matched by Claim Control Number (`CLP01`), posting allowed amounts, paid amounts, contractual write-offs, and patient responsibility.

### HL7 FHIR R4 Specifications
- **Patient Resource (`/Patient`):** Synchronizes legal name, DOB, gender, postal address, and contact numbers.
- **Coverage Resource (`/Coverage`):** Maintains active insurance policy linkages, member IDs, and payer organization identifiers.
- **Encounter Resource (`/Encounter`):** Connects clinical visit status (e.g., `finished`) to downstream billing charge capture.
- **Claim Resource (`/Claim`):** Encapsulates diagnosis codes, CPT procedure codes, and billed amounts for pre-bill validation.

---

## 3. Cryptographic & Regulatory Safeguards

- **In-Transit Protection:** Mandatory TLS 1.3 encryption across all public RESTful API endpoints, web browser portals, and SFTP clearinghouse conduits.
- **At-Rest Protection:** AES-256 encryption applied to all relational databases, document storage buckets, and offline backups.
- **Identity & Authentication:** OAuth 2.0 with JSON Web Tokens (JWT) for microservices and API authentication; multi-factor authentication (MFA) required for all interactive user logins.
- **Audit Trails:** Proposed immutable security audit logs supporting HIPAA Security Rule audit-control requirements. Retained for 7 years in write-once-read-many (WORM) storage as a proposed project policy subject to applicable state law and contractual requirements, not as a universal HIPAA requirement.
