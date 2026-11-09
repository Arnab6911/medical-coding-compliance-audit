# Data Migration & Master Patient Index (MPI) Protocol

**Legacy Cutover Protocol – MedTech v12.4 to Cloud Practice Management**  
*Document Version:* 1.0 | *Practice:* Evergreen Valley Family Medicine & Multi-Specialty Clinic  

---

## 1. The 11-Step ETL Migration Protocol

1. **Source System Assessment:** Perform complete cataloging of legacy Microsoft SQL Server tables (`Patients`, `Policies`, `Encounters`, `Billing_Charges`, `Transactions`). Identify legacy field truncation risks (e.g., 20-character address limits).
2. **Data Extraction & Staging:** Execute automated read-only SQL extraction scripts exporting data into an encrypted, isolated staging storage volume.
3. **Schema Mapping & Data Dictionary:** Map legacy fields to target cloud schema entities. Establish standardized lookups for payer IDs, provider NPIs, and facility POS codes.
4. **Data Cleansing & Standardization:**
   - DOB parsing: Convert ambiguous date strings (e.g., `05/08/1954`) into ISO-8601 (`YYYY-MM-DD`).
   - Postal validation: Validate 5-digit and 9-digit ZIP codes against USPS database standards.
   - Phone formatting: Standardize phone strings to E.164 format.
5. **Master Patient Index (MPI) Deduplication:** Deploy deterministic and fuzzy algorithms to identify duplicate charts (see Section 2).
6. **Data Transformation & Ingestion Formatting:** Assemble cleaned records into target FHIR JSON and CSV batch formats conforming to vendor ingestion specifications.
7. **Pilot Test Migrations:** Conduct 3 sequential test loads into the cloud vendor staging sandbox. Analyze error logs, truncated text fields, and rejected records.
8. **Record Count Reconciliation:** Execute census audit verifying 100% record-count identity across extracted legacy records and ingested cloud records.
9. **Financial Trial Balance Reconciliation:** Sum legacy accounts receivable balances by patient, payer, and aging bucket; compare against cloud target balances. **Mandatory gate: exact $0.00 variance required.**
10. **Final Cutover Migration:** Freeze legacy billing entry on Friday at 18:00 hours; run delta extraction; load final transactions; verify financial balance identity.
11. **Legacy Snapshot Retention & Rollback:** Maintain a read-only, air-gapped instance of MedTech v12.4 for 7 years to satisfy federal and state medical record retention laws.

---

## 2. MPI Deduplication Algorithm Specifications

To prevent medical record fragmentation and split patient billing ledgers, the deduplication engine executes a two-stage evaluation:

### Stage 1: Deterministic Matching
A record pair is flagged as a candidate match if any of the following deterministic criteria are met:
- **Rule A:** Identical Date of Birth (`dob`) AND Identical Phone Number (`phone`).
- **Rule B:** Identical Last Name (`last_name`, case-insensitive) AND Identical Date of Birth (`dob`) AND Matching Gender (`gender`).
- **Rule C:** Matching Social Security Number Last-4 (`ssn_last4`) AND Matching Date of Birth (`dob`).

### Stage 2: Probabilistic / Fuzzy Nickname Normalization
Candidate pairs are evaluated using common nickname lookup dictionaries:
- `Bob` / `Rob` / `Bobby` ↔ `Robert`
- `Bill` / `Billy` ↔ `William`
- `Jim` / `Jimmy` ↔ `James`
- `Dick` / `Rich` ↔ `Richard`
- `Liz` / `Beth` / `Betty` ↔ `Elizabeth`

### Resolution Protocol
- When a match is confirmed, the older account with complete clinical history is designated the **Primary MPI Record** (`MIGRATED_MERGED_PRIMARY`).
- The duplicate account is marked as **Secondary Merged Chart** (`MIGRATED_MERGED_SECONDARY`).
- All open accounts receivable line items and historical encounters from the secondary chart are consolidated into the primary ledger, ensuring zero financial loss and an exact $0.00 reconciliation variance.
