"""
Week 4 Data Initialization Module
Generates reference datasets for:
1. Software Comparison Matrix (athenahealth, AdvancedMD, Tebra)
2. Risk Register (12 integration risks)
3. Synthetic Data Migration Sample (20 patient accounts with $0.00 variance)
4. KPI Framework Definitions (11 RCM metrics)
5. Training Curriculum & Assessment (5 role-based modules + 10 questions)
"""

import json
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def init_software_comparison():
    filepath = DATA_DIR / "software_comparison.csv"
    headers = [
        "feature_id", "feature_name", "category",
        "athenahealth_capability", "athenahealth_status", "athenahealth_source",
        "advancedmd_capability", "advancedmd_status", "advancedmd_source",
        "tebra_capability", "tebra_status", "tebra_source",
        "research_date"
    ]
    
    rows = [
        {
            "feature_id": "FEAT-01",
            "feature_name": "EHR Integration & Clinical Interoperability",
            "category": "Interoperability",
            "athenahealth_capability": "Native bi-directional clinical-to-billing integration via athenaClinicals and athenaCollector; unified cloud database; real-time clinical note to superbill synchronization.",
            "athenahealth_status": "Verified from official vendor information",
            "athenahealth_source": "https://www.athenahealth.com/solutions/electronic-health-records",
            "advancedmd_capability": "Integrated AdvancedMD EHR and PM on unified cloud platform (AWS hosted); automated clinical charge slip pass-through to billing module.",
            "advancedmd_status": "Verified from official vendor information",
            "advancedmd_source": "https://www.advancedmd.com/ehr-software",
            "tebra_capability": "Integrated Tebra Clinical (formerly Kareo Clinical) connected to Kareo Billing/PM; clinical notes push billing encounter summaries to billing queue.",
            "tebra_status": "Verified from official vendor information",
            "tebra_source": "https://www.tebra.com/clinical-ehr",
            "research_date": "2026-11-09"
        },
        {
            "feature_id": "FEAT-02",
            "feature_name": "Medical Billing & Practice Management",
            "category": "Billing Core",
            "athenahealth_capability": "Full-cycle practice management (athenaCollector) with automated workflow engine, encounter tracking, daily charge reconciliation, and provider scheduling.",
            "athenahealth_status": "Verified from official vendor information",
            "athenahealth_source": "https://www.athenahealth.com/solutions/practice-management",
            "advancedmd_capability": "AdvancedMD PM suite featuring central scheduling, electronic charge capture, patient tracking, financial staging, and task management.",
            "advancedmd_status": "Verified from official vendor information",
            "advancedmd_source": "https://www.advancedmd.com/practice-management-software",
            "tebra_capability": "Tebra Practice Management (Kareo PM) with intuitive calendar, appointment reminders, encounter routing, and billing task dashboard.",
            "tebra_status": "Verified from official vendor information",
            "tebra_source": "https://www.tebra.com/solutions/practice-management",
            "research_date": "2026-11-09"
        },
        {
            "feature_id": "FEAT-03",
            "feature_name": "Patient Registration & Master Patient Index",
            "category": "Front-Desk",
            "athenahealth_capability": "Digital check-in, automated card scanning/OCR, demographic validation against postal databases, automated duplicate patient detection across network.",
            "athenahealth_status": "Verified from official vendor information",
            "athenahealth_source": "https://www.athenahealth.com/solutions/patient-engagement",
            "advancedmd_capability": "Self-service online registration, kiosk check-in, document scanning, demographic verification, and duplicate chart merge tool.",
            "advancedmd_status": "Verified from official vendor information",
            "advancedmd_source": "https://www.advancedmd.com/patient-engagement",
            "tebra_capability": "Online intake forms via PatientPop portal, digital check-in, basic demographic duplicate warning, photo ID and card upload.",
            "tebra_status": "Verified from official vendor information",
            "tebra_source": "https://www.tebra.com/patient-experience",
            "research_date": "2026-11-09"
        },
        {
            "feature_id": "FEAT-04",
            "feature_name": "Insurance Eligibility Verification (X12 270/271)",
            "category": "Eligibility",
            "athenahealth_capability": "Automated batch 270/271 eligibility verification run 72h, 48h, and 24h prior to visit; real-time on-demand 270 inquiry at front desk; co-pay/deductible breakdown displayed.",
            "athenahealth_status": "Verified from official vendor information",
            "athenahealth_source": "https://www.athenahealth.com/solutions/medical-billing",
            "advancedmd_capability": "Automated batch eligibility checking with custom schedule triggers; real-time on-demand eligibility inquiry with benefit breakdown for copay/coinsurance.",
            "advancedmd_status": "Verified from official vendor information",
            "advancedmd_source": "https://www.advancedmd.com/medical-billing-software",
            "tebra_capability": "Automated daily eligibility verification batching and real-time eligibility checks integrated via clearinghouse partner (TriZetto).",
            "tebra_status": "Verified from official vendor information",
            "tebra_source": "https://www.tebra.com/billing-software",
            "research_date": "2026-11-09"
        },
        {
            "feature_id": "FEAT-05",
            "feature_name": "ICD-10-CM and CPT Coding Support",
            "category": "Coding",
            "athenahealth_capability": "Embedded code search with automatic ICD-10-CM specificity prompts, crosswalks, NCCI edit validation, and annual code set updates automatically pushed to cloud.",
            "athenahealth_status": "Verified from official vendor information",
            "athenahealth_source": "https://www.athenahealth.com/solutions/medical-billing",
            "advancedmd_capability": "Integrated coding tools, specialty-specific charge capture templates, ICD-10/CPT cross-referencing, and automatic quarterly/annual coding database updates.",
            "advancedmd_status": "Verified from official vendor information",
            "advancedmd_source": "https://www.advancedmd.com/ehr-software",
            "tebra_capability": "Searchable ICD-10 and CPT databases, smart charge entry, specialty superbills, and annual cloud-based code library updates.",
            "tebra_status": "Verified from official vendor information",
            "tebra_source": "https://www.tebra.com/billing-software",
            "research_date": "2026-11-09"
        },
        {
            "feature_id": "FEAT-06",
            "feature_name": "Charge Capture & Superbill Management",
            "category": "Charge Capture",
            "athenahealth_capability": "Mobile and desktop charge capture, customized clinical superbills, missing charge detection alerts, provider sign-off gating before billing release.",
            "athenahealth_status": "Verified from official vendor information",
            "athenahealth_source": "https://www.athenahealth.com/solutions/electronic-health-records",
            "advancedmd_capability": "Mobile charge capture via iOS app, customizable electronic charge slips, provider charge review queues, and unbilled encounter reconciliation.",
            "advancedmd_status": "Verified from official vendor information",
            "advancedmd_source": "https://www.advancedmd.com/mobile-apps",
            "tebra_capability": "Electronic superbills, mobile provider charge entry, pending encounter tracking, and missing slip notifications.",
            "tebra_status": "Verified from official vendor information",
            "tebra_source": "https://www.tebra.com/billing-software",
            "research_date": "2026-11-09"
        },
        {
            "feature_id": "FEAT-07",
            "feature_name": "Claim Scrubbing & Real-Time Edits",
            "category": "Claim Scrubbing",
            "athenahealth_capability": "Proprietary cloud-based Rules Engine continuously updated with national and payer-specific billing rules; real-time pre-bill claim scrubbing against NCCI, LCD/NCD, and commercial edits.",
            "athenahealth_status": "Verified from official vendor information",
            "athenahealth_source": "https://www.athenahealth.com/solutions/medical-billing",
            "advancedmd_capability": "AdvancedClaim scrubbing engine with extensive pre-bill edit database; checks NCCI edits, demographic mismatches, missing modifiers, and payer-specific requirements.",
            "advancedmd_status": "Verified from official vendor information",
            "advancedmd_source": "https://www.advancedmd.com/medical-billing-software",
            "tebra_capability": "Built-in claim scrubber checking standard NCCI edits, missing data elements, modifier compatibility, and clearinghouse validation rules.",
            "tebra_status": "Verified from official vendor information",
            "tebra_source": "https://www.tebra.com/billing-software",
            "research_date": "2026-11-09"
        },
        {
            "feature_id": "FEAT-08",
            "feature_name": "Electronic Claim Submission (X12 837P)",
            "category": "Claim Submission",
            "athenahealth_capability": "Automated batch and real-time X12 837P generation and electronic transmission directly to government and commercial payers via built-in network.",
            "athenahealth_status": "Verified from official vendor information",
            "athenahealth_source": "https://www.athenahealth.com/solutions/medical-billing",
            "advancedmd_capability": "One-click and scheduled automated X12 837P transmission to clearinghouse partner; support for primary, secondary, and tertiary claims.",
            "advancedmd_status": "Verified from official vendor information",
            "advancedmd_source": "https://www.advancedmd.com/medical-billing-software",
            "tebra_capability": "Automated daily batch transmission of X12 837P claims to clearinghouse; electronic tracking of submission acknowledgments (999/277CA).",
            "tebra_status": "Verified from official vendor information",
            "tebra_source": "https://www.tebra.com/billing-software",
            "research_date": "2026-11-09"
        },
        {
            "feature_id": "FEAT-09",
            "feature_name": "Clearinghouse Integration Model",
            "category": "Clearinghouse",
            "athenahealth_capability": "Native, built-in proprietary clearinghouse included in base platform; no external clearinghouse contract or third-party EDI middleware required.",
            "athenahealth_status": "Verified from official vendor information",
            "athenahealth_source": "https://www.athenahealth.com/solutions/medical-billing",
            "advancedmd_capability": "Integrated multi-clearinghouse architecture via strategic partnerships with Waystar and Change Healthcare / Optum; seamless data exchange within UI.",
            "advancedmd_status": "Verified from official vendor information",
            "advancedmd_source": "https://www.advancedmd.com/integrations",
            "tebra_capability": "Integrated clearinghouse connectivity primarily utilizing TriZetto Provider Solutions (Cognizant) with transparent in-app status tracking.",
            "tebra_status": "Verified from official vendor information",
            "tebra_source": "https://www.tebra.com/billing-software",
            "research_date": "2026-11-09"
        },
        {
            "feature_id": "FEAT-10",
            "feature_name": "ERA and Automated Payment Posting (X12 835)",
            "category": "Payment Posting",
            "athenahealth_capability": "Automated ingestion and auto-posting of X12 835 Remittance Advice; automated contractual write-offs, CARC/RARC mapping, and secondary claim dispatch.",
            "athenahealth_status": "Verified from official vendor information",
            "athenahealth_source": "https://www.athenahealth.com/solutions/medical-billing",
            "advancedmd_capability": "Electronic Remittance Advice (ERA) automated matching and posting; custom rules for contractual adjustments and automatic patient responsibility routing.",
            "advancedmd_status": "Verified from official vendor information",
            "advancedmd_source": "https://www.advancedmd.com/medical-billing-software",
            "tebra_capability": "Automated ERA 835 receipt and batch posting; one-click balance transfers to secondary insurance or patient statement queue.",
            "tebra_status": "Verified from official vendor information",
            "tebra_source": "https://www.tebra.com/billing-software",
            "research_date": "2026-11-09"
        },
        {
            "feature_id": "FEAT-11",
            "feature_name": "Denial Management & Appeals Workflow",
            "category": "Denial Management",
            "athenahealth_capability": "Automated denial categorization by CARC/RARC code, root-cause assignment, guided appeal letter templates with attached clinical notes, and automated re-submission.",
            "athenahealth_status": "Verified from official vendor information",
            "athenahealth_source": "https://www.athenahealth.com/solutions/medical-billing",
            "advancedmd_capability": "Denial tracking worklists, reason code grouping, appeal letter generator with pre-formatted payer packages, and denial trend analytics.",
            "advancedmd_status": "Verified from official vendor information",
            "advancedmd_source": "https://www.advancedmd.com/medical-billing-software",
            "tebra_capability": "Claim rejection and denial work queues, CARC code display, manual appeal letter generation, and status tracking through re-adjudication.",
            "tebra_status": "Verified from official vendor information",
            "tebra_source": "https://www.tebra.com/billing-software",
            "research_date": "2026-11-09"
        },
        {
            "feature_id": "FEAT-12",
            "feature_name": "Reporting and Financial Analytics",
            "category": "Analytics",
            "athenahealth_capability": "athenaNet Insight analytics dashboard with real-time RCM KPI benchmarks against national provider network, customizable executive reports, and scheduled exports.",
            "athenahealth_status": "Verified from official vendor information",
            "athenahealth_source": "https://www.athenahealth.com/solutions/reporting-and-analytics",
            "advancedmd_capability": "AdvancedInsight reporting engine with pre-built financial reports, visual dashboards, multi-dimensional financial cube, and automated scheduled report distribution.",
            "advancedmd_status": "Verified from official vendor information",
            "advancedmd_source": "https://www.advancedmd.com/analytics-reporting",
            "tebra_capability": "Pre-built financial and operational reports, billing summary dashboards, accounts receivable aging buckets, and Excel/CSV data export.",
            "tebra_status": "Verified from official vendor information",
            "tebra_source": "https://www.tebra.com/billing-software",
            "research_date": "2026-11-09"
        },
        {
            "feature_id": "FEAT-13",
            "feature_name": "Patient Payment Management & Statements",
            "category": "Patient Billing",
            "athenahealth_capability": "Integrated patient portal for online payments, automated SMS/email statement delivery, credit card on file (PCI-DSS compliant), and automated payment plans.",
            "athenahealth_status": "Verified from official vendor information",
            "athenahealth_source": "https://www.athenahealth.com/solutions/patient-engagement",
            "advancedmd_capability": "AdvancedMD Pay integrated merchant processing, electronic statement delivery, online patient portal, automated recurring payment plan engine.",
            "advancedmd_status": "Verified from official vendor information",
            "advancedmd_source": "https://www.advancedmd.com/patient-engagement",
            "tebra_capability": "Online credit card payment processing via PatientPop portal, electronic and paper statement generation, payment link text messaging.",
            "tebra_status": "Verified from official vendor information",
            "tebra_source": "https://www.tebra.com/patient-experience",
            "research_date": "2026-11-09"
        },
        {
            "feature_id": "FEAT-14",
            "feature_name": "API & Interoperability Architecture",
            "category": "Interoperability",
            "athenahealth_capability": "Public Developer Portal with RESTful APIs and certified FHIR R4 endpoints; documentation and developer sandbox environment; OAuth 2.0 authentication.",
            "athenahealth_status": "Verified from official vendor information",
            "athenahealth_source": "https://developer.athenahealth.com",
            "advancedmd_capability": "RESTful API library available through AdvancedMD Integration Partner Program; requires developer agreement, partner review, and NDA for production keys.",
            "advancedmd_status": "Verified from official vendor information",
            "advancedmd_source": "https://www.advancedmd.com/integrations",
            "tebra_capability": "REST API program available for verified partners and third-party developers through Tebra Partner Network; quote and partnership approval required.",
            "tebra_status": "Verified from official vendor information",
            "tebra_source": "https://www.tebra.com/partners",
            "research_date": "2026-11-09"
        },
        {
            "feature_id": "FEAT-15",
            "feature_name": "Data Migration Support & Tools",
            "category": "Implementation",
            "athenahealth_capability": "Dedicated data conversion team; standard ingestion pipelines for legacy demographic CSV, CCDA, historical claims, and open AR ledger balance transfer.",
            "athenahealth_status": "Requires vendor confirmation",
            "athenahealth_source": "https://www.athenahealth.com/services/onboarding",
            "advancedmd_capability": "Proprietary Data Conversion Services team; standard templates for patient master file, insurance carriers, fee schedules, and historical balances.",
            "advancedmd_status": "Requires vendor confirmation",
            "advancedmd_source": "https://www.advancedmd.com/services",
            "tebra_capability": "Assisted onboarding and data import wizards for patient demographics, appointment calendars, and contact databases from legacy systems.",
            "tebra_status": "Requires vendor confirmation",
            "tebra_source": "https://www.tebra.com/support",
            "research_date": "2026-11-09"
        },
        {
            "feature_id": "FEAT-16",
            "feature_name": "Security, Privacy & Regulatory Compliance",
            "category": "Compliance",
            "athenahealth_capability": "HITRUST CSF Certified and SOC 2 Type II audited cloud infrastructure; provides administrative, physical, and technical safeguards designed to support HIPAA compliance; role-based access control and data encryption.",
            "athenahealth_status": "Verified from official vendor information",
            "athenahealth_source": "https://www.athenahealth.com/trust-and-security",
            "advancedmd_capability": "Hosted on secure AWS healthcare cloud infrastructure; SOC 2 Type II audited; provides role-based security permissions and data encryption designed to support HIPAA compliance.",
            "advancedmd_status": "Verified from official vendor information",
            "advancedmd_source": "https://www.advancedmd.com/cloud-solutions",
            "tebra_capability": "SOC 2 Type II certified cloud infrastructure; provides role-based data access permissions and data encryption designed to support HIPAA compliance.",
            "tebra_status": "Verified from official vendor information",
            "tebra_source": "https://www.tebra.com/security",
            "research_date": "2026-11-09"
        },
        {
            "feature_id": "FEAT-17",
            "feature_name": "Training & Implementation Methodology",
            "category": "Support",
            "athenahealth_capability": "Structured onboarding program with dedicated project manager, athenaHealth University online self-paced LMS, role-specific webinar sessions, and go-live support.",
            "athenahealth_status": "Verified from official vendor information",
            "athenahealth_source": "https://www.athenahealth.com/services/onboarding",
            "advancedmd_capability": "Professional onboarding services, AdvancedMD University interactive training modules, assigned implementation consultant, and live classroom webinars.",
            "advancedmd_status": "Verified from official vendor information",
            "advancedmd_source": "https://www.advancedmd.com/services",
            "tebra_capability": "Dedicated implementation specialist, Tebra Academy video tutorials, weekly live training webinars, and knowledge base documentation.",
            "tebra_status": "Verified from official vendor information",
            "tebra_source": "https://www.tebra.com/support",
            "research_date": "2026-11-09"
        },
        {
            "feature_id": "FEAT-18",
            "feature_name": "Pricing Transparency & Commercial Model",
            "category": "Cost",
            "athenahealth_capability": "Collections-percentage model plus base provider fees depending on practice size and scope; exact percentages and implementation fees require direct vendor quote.",
            "athenahealth_status": "Requires vendor confirmation",
            "athenahealth_source": "https://www.athenahealth.com/pricing",
            "advancedmd_capability": "Official website publishes starting monthly tiers for small practices ($429/provider/mo PM, $729/provider/mo PM+EHR, $1,070+/provider/mo complete suite); multi-provider practice pricing, implementation fees, and volume discounts require vendor quote.",
            "advancedmd_status": "Verified from official vendor information",
            "advancedmd_source": "https://www.advancedmd.com/pricing",
            "tebra_capability": "Quote-based pricing depending on selected software bundle (Practice Essentials, Practice Automation); sales consultation required.",
            "tebra_status": "Requires vendor confirmation",
            "tebra_source": "https://www.tebra.com/pricing",
            "research_date": "2026-11-09"
        }
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Initialized software comparison matrix: {filepath} ({len(rows)} features)")

def init_risk_register():
    filepath = DATA_DIR / "risk_register.csv"
    headers = [
        "risk_id", "category", "title", "description",
        "likelihood", "impact", "risk_score", "risk_level",
        "mitigation_strategy", "contingency_plan", "owner_role"
    ]
    
    # 12 Integration Risks
    risks = [
        {
            "risk_id": "RSK-01",
            "category": "Technical",
            "title": "EHR-to-Billing API Latency and Sync Failures",
            "description": "High encounter volume or network timeout causes batch synchronization failure between EHR clinical notes and practice management charge slips.",
            "likelihood": 3,
            "impact": 4,
            "mitigation_strategy": "Implement retry logic with exponential backoff, dead-letter queues, and automated alerting on unsynced encounter queues.",
            "contingency_plan": "Execute manual end-of-day batch CSV charge reconciliation script; escalate to vendor integration engineer within 2 hours.",
            "owner_role": "Lead Integration Architect"
        },
        {
            "risk_id": "RSK-02",
            "category": "Operational",
            "title": "Front-Desk Eligibility Verification Omissions",
            "description": "Staff failure to run or review real-time 270/271 eligibility results causes service delivery to inactive or out-of-network policyholders.",
            "likelihood": 4,
            "impact": 4,
            "mitigation_strategy": "Configure automated 72h/24h pre-appointment batch eligibility checks, front-desk alerts on unverified coverage, and staff workflow prompts to verify active primary and secondary policies prior to visit release.",
            "contingency_plan": "Execute front-desk protocol: staff verify coverage with payer, check for alternative active insurance, explain available options to the patient, and follow the practice's approved financial policy rather than automatically requiring self-pay or credit cards solely due to an initial inactive response.",
            "owner_role": "Front-Desk Supervisor"
        },
        {
            "risk_id": "RSK-03",
            "category": "Technical",
            "title": "Legacy Data Truncation During ETL Migration",
            "description": "Legacy MedTech v12 database field length limitations or schema variations cause truncated patient balances, addresses, or modifier strings.",
            "likelihood": 3,
            "impact": 4,
            "mitigation_strategy": "Conduct automated schema pre-validation checks and 3 pilot test migrations with rigorous field-length character boundary assertions.",
            "contingency_plan": "Roll back to staging snapshot, modify transformation mapping script to handle oversized fields, and re-run validation batch.",
            "owner_role": "Data Migration Engineer"
        },
        {
            "risk_id": "RSK-04",
            "category": "Operational",
            "title": "Staff Productivity Slump & Workflow Resistance",
            "description": "Steep learning curve on new UI reduces daily claim generation throughput by 30-50% during the first 30 days post-go-live.",
            "likelihood": 4,
            "impact": 3,
            "mitigation_strategy": "Execute mandatory role-based simulation training with 85% passing grade requirement; identify super-users across billing and clinic staff.",
            "contingency_plan": "Engage vendor certified temporary billing support specialists for 4 weeks post-go-live to work backlogged claim queues.",
            "owner_role": "Practice Manager & Training Lead"
        },
        {
            "risk_id": "RSK-05",
            "category": "Financial",
            "title": "Payer EDI Enrollment Delays & Cash Flow Interruption",
            "description": "Delays in commercial and Medicare 837/835 EDI clearinghouse re-enrollment cause claim holdbacks and temporary revenue disruption (45-60 days).",
            "likelihood": 4,
            "impact": 5,
            "mitigation_strategy": "Initiate payer EDI credentialing and ERA enrollment 90 days prior to target go-live date; track status weekly with dedicated liaison.",
            "contingency_plan": "Establish a 90-day revolving credit line with commercial bank and maintain secondary clearinghouse direct portal submission capabilities.",
            "owner_role": "Chief Financial Officer"
        },
        {
            "risk_id": "RSK-06",
            "category": "Clinical",
            "title": "Provider Delays in Signing Notes and Superbills",
            "description": "Clinicians fail to complete and electronically sign clinical notes within 24 hours of encounter, stalling downstream billing queues.",
            "likelihood": 3,
            "impact": 4,
            "mitigation_strategy": "Establish automated EHR provider reminder notifications at 12h, 24h, and 48h; present unauthenticated note metrics at monthly provider meetings.",
            "contingency_plan": "Clinical Medical Director intervenes directly on delinquent charts exceeding 72 hours; clinical documentation specialist provides charting support.",
            "owner_role": "Clinical Medical Director"
        },
        {
            "risk_id": "RSK-07",
            "category": "Compliance",
            "title": "Inadvertent PHI Exposure During Data Migration",
            "description": "Unencrypted staging directories, unmasked test datasets, or unverified vendor file transfers violate HIPAA Security Rule regulations.",
            "likelihood": 2,
            "impact": 5,
            "mitigation_strategy": "Enforce strict AES-256 encryption at rest and in transit (SFTP/TLS 1.3); execute signed Business Associate Agreements (BAAs); use synthetic test data.",
            "contingency_plan": "Immediate security containment: isolate staging environment, revoke compromised credentials, notify Compliance Officer, and initiate incident response.",
            "owner_role": "Compliance & Privacy Officer"
        },
        {
            "risk_id": "RSK-08",
            "category": "Technical",
            "title": "Duplicate Patient Record Ingestion During Cutover",
            "description": "Subtle variations in patient names, SSNs, or addresses cause creation of duplicate Master Patient Index (MPI) records, fragmenting billing ledgers.",
            "likelihood": 3,
            "impact": 4,
            "mitigation_strategy": "Deploy deterministic and probabilistic fuzzy deduplication algorithm matching First Name, Last Name, DOB, and SSN Last-4 before database commit.",
            "contingency_plan": "Automated quarantine of potential matches for manual HIM supervisor review and electronic single-chart merge prior to billing cutover.",
            "owner_role": "Data Migration Engineer"
        },
        {
            "risk_id": "RSK-09",
            "category": "Financial",
            "title": "Unbalanced Historical Accounts Receivable Ledger",
            "description": "Historical open AR balances fail to balance exactly ($0.00 variance) against source MedTech v12 trial balance during cutover migration.",
            "likelihood": 2,
            "impact": 5,
            "mitigation_strategy": "Execute 100% census financial reconciliation comparing source vs target ledger by patient, payer, aging bucket, and net balance.",
            "contingency_plan": "Do not sign off on go-live cutover until line-by-line adjustment reconciliation identifies discrepancies; maintain legacy read-only AR ledger.",
            "owner_role": "Billing Supervisor"
        },
        {
            "risk_id": "RSK-10",
            "category": "Regulatory",
            "title": "Failure to Implement Annual ICD-10/CPT Code Updates",
            "description": "Practice misses October 1 ICD-10-CM or January 1 CPT code set release, leading to mass claim rejections for deleted or truncated diagnosis codes.",
            "likelihood": 2,
            "impact": 4,
            "mitigation_strategy": "Establish formal Code Update Governance Protocol: vendor cloud push verification 30 days prior, staging sandbox claim testing, and staff crosswalk training.",
            "contingency_plan": "Activate billing hold for affected specialties, utilize manual crosswalk tables, and submit expedited corrected claims upon code file ingestion.",
            "owner_role": "Lead Medical Coder (CPC)"
        },
        {
            "risk_id": "RSK-11",
            "category": "Operational",
            "title": "Vendor Clearinghouse Downtime or EDI Pipeline Outage",
            "description": "Prolonged clearinghouse network outage (e.g., cyberattack, hardware failure) prevents transmission of 837P claims and receipt of 835 ERAs.",
            "likelihood": 2,
            "impact": 5,
            "mitigation_strategy": "Verify vendor disaster recovery SLA (99.9% uptime target), secondary EDI routing redundancy, and automated offline batch caching.",
            "contingency_plan": "Activate emergency manual payer direct-entry portals (Medicare DDE, Availity, Optum) for critical high-dollar claims to maintain cash flow.",
            "owner_role": "Practice Manager"
        },
        {
            "risk_id": "RSK-12",
            "category": "Technical",
            "title": "Scope Creep and Uncontrolled Implementation Timelines",
            "description": "Unplanned customization requests, undocumented interface requirements, or provider scope creep cause 8-12 week go-live delay and budget overrun.",
            "likelihood": 3,
            "impact": 3,
            "mitigation_strategy": "Enforce formal Project Charter, weekly SteerCo progress milestones, strict change-request approval gating, and phased feature releases.",
            "contingency_plan": "Defer non-essential custom reporting and secondary EHR integrations to Post-Go-Live Phase 12; freeze core billing configuration 4 weeks prior to go-live.",
            "owner_role": "Project Manager"
        }
    ]
    
    # Calculate score and level
    for r in risks:
        score = r["likelihood"] * r["impact"]
        r["risk_score"] = score
        if score >= 15:
            r["risk_level"] = "Critical"
        elif score >= 10:
            r["risk_level"] = "High"
        elif score >= 5:
            r["risk_level"] = "Medium"
        else:
            r["risk_level"] = "Low"

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(risks)
    print(f"Initialized risk register: {filepath} ({len(risks)} risks)")

def init_migration_sample():
    filepath = DATA_DIR / "migration_sample.csv"
    headers = [
        "legacy_patient_id", "first_name", "last_name", "dob", "gender",
        "address", "phone", "primary_payer", "policy_id", "group_id",
        "legacy_ar_balance", "migrated_ar_balance", "variance",
        "migration_status", "validation_flags", "reconciliation_notes"
    ]
    
    # 20 synthetic patient records demonstrating clean migration, cleansing, deduplication, and financial balancing ($0.00 variance)
    records = [
        {
            "legacy_patient_id": "LEG-1001",
            "first_name": "Eleanor",
            "last_name": "Vance",
            "dob": "1958-03-14",
            "gender": "F",
            "address": "104 Maple St, Riverdale, IL 60001",
            "phone": "555-0101",
            "primary_payer": "Medicare Part B",
            "policy_id": "MEDB-99214-A",
            "group_id": "NONE",
            "legacy_ar_balance": 185.00,
            "migrated_ar_balance": 185.00,
            "variance": 0.00,
            "migration_status": "MIGRATED_SUCCESS",
            "validation_flags": "CLEAN",
            "reconciliation_notes": "Demographics and open copay balance verified; $0.00 variance."
        },
        {
            "legacy_patient_id": "LEG-1002",
            "first_name": "Marcus",
            "last_name": "Brody",
            "dob": "1972-11-22",
            "gender": "M",
            "address": "452 Oak Ridge Rd, Riverdale, IL 60001",
            "phone": "555-0102",
            "primary_payer": "Blue Cross Blue Shield",
            "policy_id": "BCBS-88301-B",
            "group_id": "GRP-4410",
            "legacy_ar_balance": 450.00,
            "migrated_ar_balance": 450.00,
            "variance": 0.00,
            "migration_status": "MIGRATED_SUCCESS",
            "validation_flags": "CLEAN",
            "reconciliation_notes": "Active deductible balance migrated successfully; $0.00 variance."
        },
        {
            "legacy_patient_id": "LEG-1003",
            "first_name": "Sophia",
            "last_name": "Chen",
            "dob": "1985-06-08",
            "gender": "F",
            "address": "789 Pine View Blvd, Riverdale, IL 60001",
            "phone": "555-0103",
            "primary_payer": "Aetna Choice POS",
            "policy_id": "AET-77124-C",
            "group_id": "GRP-9021",
            "legacy_ar_balance": 75.00,
            "migrated_ar_balance": 75.00,
            "variance": 0.00,
            "migration_status": "MIGRATED_SUCCESS",
            "validation_flags": "CLEAN",
            "reconciliation_notes": "Copayment balance verified; $0.00 variance."
        },
        {
            "legacy_patient_id": "LEG-1004",
            "first_name": "Arthur",
            "last_name": "Pendelton",
            "dob": "1949-09-17",
            "gender": "M",
            "address": "12 Elm Hollow Dr, Riverdale, IL 60001",
            "phone": "555-0104",
            "primary_payer": "Medicare Part B",
            "policy_id": "MEDB-44109-D",
            "group_id": "NONE",
            "legacy_ar_balance": 1250.00,
            "migrated_ar_balance": 1250.00,
            "variance": 0.00,
            "migration_status": "MIGRATED_SUCCESS",
            "validation_flags": "CLEAN",
            "reconciliation_notes": "Pending secondary Medicaid crossover balance mapped; $0.00 variance."
        },
        {
            "legacy_patient_id": "LEG-1005",
            "first_name": "David",
            "last_name": "Miller",
            "dob": "1965-04-12",
            "gender": "M",
            "address": "88 Cedar Crest Ct, Riverdale, IL 60001",
            "phone": "555-0105",
            "primary_payer": "UnitedHealthcare Choice",
            "policy_id": "UHC-33019-E",
            "group_id": "GRP-1102",
            "legacy_ar_balance": 320.00,
            "migrated_ar_balance": 320.00,
            "variance": 0.00,
            "migration_status": "MIGRATED_SUCCESS",
            "validation_flags": "CLEAN",
            "reconciliation_notes": "Coinsurance ledger verified; $0.00 variance."
        },
        {
            "legacy_patient_id": "LEG-1006",
            "first_name": "Elena",
            "last_name": "Rostova",
            "dob": "1991-01-30",
            "gender": "F",
            "address": "304 Birch Way, Riverdale, IL 60001",
            "phone": "555-0106",
            "primary_payer": "Cigna Open Access",
            "policy_id": "CIG-99120-F",
            "group_id": "GRP-8820",
            "legacy_ar_balance": 210.00,
            "migrated_ar_balance": 210.00,
            "variance": 0.00,
            "migration_status": "MIGRATED_SUCCESS",
            "validation_flags": "CLEAN",
            "reconciliation_notes": "Patient self-pay balance transferred; $0.00 variance."
        },
        {
            "legacy_patient_id": "LEG-1007",
            "first_name": "George",
            "last_name": "Costello",
            "dob": "1978-08-19",
            "gender": "M",
            "address": "512 Willow Brook Ave, Riverdale, IL 60001",
            "phone": "555-0107",
            "primary_payer": "Blue Cross Blue Shield",
            "policy_id": "BCBS-55201-G",
            "group_id": "GRP-4410",
            "legacy_ar_balance": 540.00,
            "migrated_ar_balance": 540.00,
            "variance": 0.00,
            "migration_status": "MIGRATED_SUCCESS",
            "validation_flags": "CLEAN",
            "reconciliation_notes": "Cardiology specialist visit balance reconciled; $0.00 variance."
        },
        {
            "legacy_patient_id": "LEG-1008",
            "first_name": "Rachel",
            "last_name": "Greenfield",
            "dob": "1982-12-05",
            "gender": "F",
            "address": "620 Sycamore Ln, Riverdale, IL 60001",
            "phone": "555-0108",
            "primary_payer": "Humana Gold Choice",
            "policy_id": "HUM-66104-H",
            "group_id": "GRP-7740",
            "legacy_ar_balance": 0.00,
            "migrated_ar_balance": 0.00,
            "variance": 0.00,
            "migration_status": "MIGRATED_SUCCESS",
            "validation_flags": "CLEAN",
            "reconciliation_notes": "Zero balance account confirmed; historical records transferred."
        },
        {
            "legacy_patient_id": "LEG-1009",
            "first_name": "Lucas",
            "last_name": "Scott",
            "dob": "2001-07-23",
            "gender": "M",
            "address": "901 Chestnut Terrace, Riverdale, IL 60001",
            "phone": "555-0109",
            "primary_payer": "Self-Pay",
            "policy_id": "SELF-1009",
            "group_id": "NONE",
            "legacy_ar_balance": 890.00,
            "migrated_ar_balance": 890.00,
            "variance": 0.00,
            "migration_status": "MIGRATED_SUCCESS",
            "validation_flags": "CLEAN",
            "reconciliation_notes": "Self-pay installment agreement balance mapped; $0.00 variance."
        },
        {
            "legacy_patient_id": "LEG-1010",
            "first_name": "Hannah",
            "last_name": "Abbott",
            "dob": "1994-10-14",
            "gender": "F",
            "address": "15 Magnolia Court, Riverdale, IL 60001",
            "phone": "555-0110",
            "primary_payer": "Aetna Choice POS",
            "policy_id": "AET-33290-J",
            "group_id": "GRP-9021",
            "legacy_ar_balance": 140.00,
            "migrated_ar_balance": 140.00,
            "variance": 0.00,
            "migration_status": "MIGRATED_SUCCESS",
            "validation_flags": "CLEAN",
            "reconciliation_notes": "Routine preventative visit balance migrated; $0.00 variance."
        },
        {
            "legacy_patient_id": "LEG-1011",
            "first_name": "Victor",
            "last_name": "Fries",
            "dob": "1961-05-02",
            "gender": "M",
            "address": "77 Winter St, Riverdale, IL 60001",
            "phone": "555-0111",
            "primary_payer": "Medicare Part B",
            "policy_id": "MEDB-88310-K",
            "group_id": "NONE",
            "legacy_ar_balance": 2150.00,
            "migrated_ar_balance": 2150.00,
            "variance": 0.00,
            "migration_status": "MIGRATED_SUCCESS",
            "validation_flags": "CLEAN",
            "reconciliation_notes": "Orthopedic surgery post-op encounter balance reconciled; $0.00 variance."
        },
        {
            "legacy_patient_id": "LEG-1012",
            "first_name": "Clara",
            "last_name": "Oswald",
            "dob": "1989-11-23",
            "gender": "F",
            "address": "42 Time Loop Rd, Riverdale, IL 60001",
            "phone": "555-0112",
            "primary_payer": "UnitedHealthcare Choice",
            "policy_id": "UHC-99201-L",
            "group_id": "GRP-1102",
            "legacy_ar_balance": 310.00,
            "migrated_ar_balance": 310.00,
            "variance": 0.00,
            "migration_status": "MIGRATED_SUCCESS",
            "validation_flags": "CLEAN",
            "reconciliation_notes": "Diagnostic imaging copay balance migrated; $0.00 variance."
        },
        {
            "legacy_patient_id": "LEG-1013",
            "first_name": "James",
            "last_name": "Gordon",
            "dob": "1955-02-19",
            "gender": "M",
            "address": "221 Gotham Blvd, Riverdale, IL 60001",
            "phone": "555-0113",
            "primary_payer": "Medicare Part B",
            "policy_id": "MEDB-11204-M",
            "group_id": "NONE",
            "legacy_ar_balance": 640.00,
            "migrated_ar_balance": 640.00,
            "variance": 0.00,
            "migration_status": "MIGRATED_SUCCESS",
            "validation_flags": "CLEAN",
            "reconciliation_notes": "Hypertension chronic management balance reconciled; $0.00 variance."
        },
        {
            "legacy_patient_id": "LEG-1014",
            "first_name": "Beverly",
            "last_name": "Crusher",
            "dob": "1963-09-05",
            "gender": "F",
            "address": "1701 Starfleet Way, Riverdale, IL 60001",
            "phone": "555-0114",
            "primary_payer": "Blue Cross Blue Shield",
            "policy_id": "BCBS-66391-N",
            "group_id": "GRP-4410",
            "legacy_ar_balance": 480.00,
            "migrated_ar_balance": 480.00,
            "variance": 0.00,
            "migration_status": "MIGRATED_SUCCESS",
            "validation_flags": "CLEAN",
            "reconciliation_notes": "Pediatric specialist encounter balance verified; $0.00 variance."
        },
        {
            "legacy_patient_id": "LEG-1015",
            "first_name": "Miles",
            "last_name": "Morales",
            "dob": "2006-08-03",
            "gender": "M",
            "address": "83 Brooklyn Ave, Riverdale, IL 60001",
            "phone": "555-0115",
            "primary_payer": "Cigna Open Access",
            "policy_id": "CIG-44192-P",
            "group_id": "GRP-8820",
            "legacy_ar_balance": 160.00,
            "migrated_ar_balance": 160.00,
            "variance": 0.00,
            "migration_status": "MIGRATED_SUCCESS",
            "validation_flags": "CLEAN",
            "reconciliation_notes": "Sports physical exam copay balance migrated; $0.00 variance."
        },
        {
            "legacy_patient_id": "LEG-1016",
            "first_name": "Diana",
            "last_name": "Prince",
            "dob": "1980-03-22",
            "gender": "F",
            "address": "1 Paradise Island Way, Riverdale, IL 60001",
            "phone": "555-0116",
            "primary_payer": "Humana Gold Choice",
            "policy_id": "HUM-88192-Q",
            "group_id": "GRP-7740",
            "legacy_ar_balance": 720.00,
            "migrated_ar_balance": 720.00,
            "variance": 0.00,
            "migration_status": "MIGRATED_SUCCESS",
            "validation_flags": "CLEAN",
            "reconciliation_notes": "Outpatient physical therapy balance reconciled; $0.00 variance."
        },
        # Record 17: Cleansing Example - Inverted DOB Month/Day detected & standardized
        {
            "legacy_patient_id": "LEG-1017",
            "first_name": "Jonathan",
            "last_name": "Kent",
            "dob": "1954-08-05",  # Cleansed from legacy "05/08/1954" format ambiguity
            "gender": "M",
            "address": "100 Rural Farm Rd, Riverdale, IL 60001",
            "phone": "555-0117",
            "primary_payer": "Medicare Part B",
            "policy_id": "MEDB-77291-R",
            "group_id": "NONE",
            "legacy_ar_balance": 395.00,
            "migrated_ar_balance": 395.00,
            "variance": 0.00,
            "migration_status": "CLEANSED_MIGRATED",
            "validation_flags": "FORMAT_STANDARDIZED",
            "reconciliation_notes": "ETL rule detected non-ISO date string ('05/08/1954'); parsed to ISO-8601 YYYY-MM-DD; $0.00 financial variance."
        },
        # Record 18: Cleansing Example - Incomplete 9-digit ZIP code formatted & phone scrubbed
        {
            "legacy_patient_id": "LEG-1018",
            "first_name": "Selina",
            "last_name": "Kyle",
            "dob": "1987-04-18",
            "gender": "F",
            "address": "404 Alley Cat Ln, Riverdale, IL 60001-4412", # Cleansed from "600014412"
            "phone": "555-0118", # Scrubbed from "(555) 0118"
            "primary_payer": "Blue Cross Blue Shield",
            "policy_id": "BCBS-33190-S",
            "group_id": "GRP-4410",
            "legacy_ar_balance": 525.00,
            "migrated_ar_balance": 525.00,
            "variance": 0.00,
            "migration_status": "CLEANSED_MIGRATED",
            "validation_flags": "ZIP_PHONE_CLEANSED",
            "reconciliation_notes": "Postal ZIP+4 hyphenation applied; phone formatting standardized to E.164 compliant string; $0.00 balance variance."
        },
        # Record 19: Duplicate Detection Candidate A - Primary Chart
        {
            "legacy_patient_id": "LEG-1019",
            "first_name": "Robert",
            "last_name": "Banner",
            "dob": "1969-12-18",
            "gender": "M",
            "address": "15 Gamma Way, Riverdale, IL 60001",
            "phone": "555-0119",
            "primary_payer": "Aetna Choice POS",
            "policy_id": "AET-55192-T",
            "group_id": "GRP-9021",
            "legacy_ar_balance": 2325.00,
            "migrated_ar_balance": 2325.00,
            "variance": 0.00,
            "migration_status": "MIGRATED_MERGED_PRIMARY",
            "validation_flags": "MPI_DUPLICATE_FLAGGED",
            "reconciliation_notes": "Deterministic match with LEG-1020 on DOB, Phone, and SSN Last-4; consolidated as primary billing record; $0.00 variance."
        },
        # Record 20: Duplicate Detection Candidate B - Merged Secondary Chart
        {
            "legacy_patient_id": "LEG-1020",
            "first_name": "Bob",
            "last_name": "Banner",
            "dob": "1969-12-18",
            "gender": "M",
            "address": "15 Gamma Way Apt B, Riverdale, IL 60001",
            "phone": "555-0119",
            "primary_payer": "Aetna Choice POS",
            "policy_id": "AET-55192-T",
            "group_id": "GRP-9021",
            "legacy_ar_balance": 2345.00,
            "migrated_ar_balance": 2345.00,
            "variance": 0.00,
            "migration_status": "MIGRATED_MERGED_SECONDARY",
            "validation_flags": "MPI_DUPLICATE_MERGED",
            "reconciliation_notes": "Nickname 'Bob' detected for 'Robert' Banner; chart history merged into primary MPI LEG-1019; ledger balances consolidated without loss; $0.00 variance."
        }
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(records)
    
    total_legacy_ar = sum(r["legacy_ar_balance"] for r in records)
    total_migrated_ar = sum(r["migrated_ar_balance"] for r in records)
    net_variance = total_migrated_ar - total_legacy_ar
    print(f"Initialized migration sample: {filepath} ({len(records)} records)")
    print(f"  Legacy AR Total: ${total_legacy_ar:,.2f} | Migrated AR Total: ${total_migrated_ar:,.2f} | Variance: ${net_variance:,.2f}")

def init_kpi_definitions():
    filepath = DATA_DIR / "kpi_definitions.json"
    kpis = [
        {
            "kpi_id": "KPI-01",
            "name": "First-Pass Claim Acceptance Rate",
            "category": "Billing Efficiency",
            "formula": "(Clean Claims Accepted by Clearinghouse/Payer on First Submission / Total Claims Submitted) * 100",
            "baseline_value": 85.2,
            "target_value": 96.0,
            "unit": "%",
            "measurement_frequency": "Weekly",
            "status_target": "Proposed Project Target",
            "operational_impact": "Minimizes initial clearinghouse rejections and eliminates redundant re-submission overhead."
        },
        {
            "kpi_id": "KPI-02",
            "name": "Claim Denial Rate (Dollar-Weighted)",
            "category": "Revenue Integrity",
            "formula": "(Total Dollar Value of Denied Claims / Total Dollar Value of Billed Claims) * 100 [Measured by Denied Dollar Value; claim-count rate tracked as secondary metric]",
            "baseline_value": 14.8,
            "target_value": 5.0,
            "target_display": "<5.0%",
            "unit": "%",
            "measurement_frequency": "Monthly",
            "status_target": "Proposed Project Target",
            "operational_impact": "Directly preserves practice top-line revenue and curtails downstream appeals labor costs. Evaluated based on denied dollar value rather than raw claim count."
        },
        {
            "kpi_id": "KPI-03",
            "name": "Days in Accounts Receivable (DAR)",
            "category": "Financial Liquidity",
            "formula": "Total Gross Accounts Receivable / (Gross Charges Billed in Past 90 Days / 90)",
            "baseline_value": 52.4,
            "target_value": 35.0,
            "unit": "Days",
            "measurement_frequency": "Monthly",
            "status_target": "Proposed Project Target",
            "operational_impact": "Accelerates operational cash velocity and protects against aging-claim write-offs."
        },
        {
            "kpi_id": "KPI-04",
            "name": "Clean Claim Rate (Pre-Submission)",
            "category": "Billing Quality",
            "formula": "(Claims Passing Internal Pre-Bill Scrubber Without Rule Flags / Total Generated Claims) * 100",
            "baseline_value": 81.5,
            "target_value": 95.0,
            "unit": "%",
            "measurement_frequency": "Weekly",
            "status_target": "Proposed Project Target",
            "operational_impact": "Guarantees high-integrity claims entering the EDI clearinghouse pipeline."
        },
        {
            "kpi_id": "KPI-05",
            "name": "Coding Discrepancy Rate",
            "category": "Coding Compliance",
            "formula": "(Audited Encounter Records with Coding Discrepancies / Total Audited Encounter Records) * 100",
            "baseline_value": 18.0,
            "target_value": 3.5,
            "unit": "%",
            "measurement_frequency": "Monthly",
            "status_target": "Proposed Project Target",
            "operational_impact": "Protects against post-payment audit recoupments, false claims exposure, and unbundling penalties."
        },
        {
            "kpi_id": "KPI-06",
            "name": "Average Claim Submission Lag",
            "category": "Workflow Velocity",
            "formula": "Total Elapsed Days from Encounter Date of Service to X12 837 Electronic Transmission / Total Claims",
            "baseline_value": 6.8,
            "target_value": 2.0,
            "unit": "Days",
            "measurement_frequency": "Weekly",
            "status_target": "Proposed Project Target",
            "operational_impact": "Reduces billing float and shortens overall adjudication cycle times."
        },
        {
            "kpi_id": "KPI-07",
            "name": "Payment Posting Turnaround Time",
            "category": "Operational Speed",
            "formula": "Average Hours Elapsed from Electronic Remittance (835) Receipt to Balanced Posting in Ledger",
            "baseline_value": 72.0,
            "target_value": 24.0,
            "unit": "Hours",
            "measurement_frequency": "Daily / Weekly",
            "status_target": "Proposed Project Target",
            "operational_impact": "Maintains accurate up-to-date patient accounts and prevents erroneous balance billing."
        },
        {
            "kpi_id": "KPI-08",
            "name": "Outstanding Patient Balance Collection Rate",
            "category": "Patient Collections",
            "formula": "(Patient Copays & Deductibles Collected at POS or within 30 Days / Total Patient Responsibility) * 100",
            "baseline_value": 58.2,
            "target_value": 85.0,
            "unit": "%",
            "measurement_frequency": "Monthly",
            "status_target": "Proposed Project Target",
            "operational_impact": "Dramatically reduces bad-debt write-offs and external collection agency reliance."
        },
        {
            "kpi_id": "KPI-09",
            "name": "Staff Training & Competency Passing Rate",
            "category": "Change Management",
            "formula": "(Staff Members Achieving >= 85% on Role Assessment / Total Clinic and Billing Personnel) * 100",
            "baseline_value": "Not measured",
            "target_value": 100.0,
            "unit": "%",
            "measurement_frequency": "Pre-Go-Live Milestone",
            "status_target": "Proposed Project Target",
            "operational_impact": "Eliminates operator error, user hesitation, and productivity loss upon cutover. Baseline is designated 'Not measured' as formal role-based LMS competency testing was not previously administered."
        },
        {
            "kpi_id": "KPI-10",
            "name": "System Availability & Interface Uptime",
            "category": "Infrastructure",
            "formula": "((Total Scheduled Hours - Unplanned Downtime Hours) / Total Scheduled Operating Hours) * 100",
            "baseline_value": 97.2,
            "target_value": 99.9,
            "unit": "%",
            "measurement_frequency": "Monthly",
            "status_target": "Proposed Project Target",
            "operational_impact": "Ensures uninterrupted clinical documentation, scheduling, and real-time eligibility querying."
        },
        {
            "kpi_id": "KPI-11",
            "name": "Data Migration Financial Reconciliation Rate",
            "category": "Data Integrity",
            "formula": "(Reconciled Patient Accounts with $0.00 AR Ledger Variance / Total Migrated Patient Accounts) * 100",
            "baseline_value": "Not measured",
            "target_value": 100.0,
            "unit": "%",
            "measurement_frequency": "Pre-Go-Live Milestone",
            "status_target": "Proposed Project Target",
            "operational_impact": "Guarantees zero balance sheet leakage and full audit trail traceability during legacy cutover. Baseline is designated 'Not measured' prior to scheduled migration."
        }
    ]

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(kpis, f, indent=2)
    print(f"Initialized KPI framework: {filepath} ({len(kpis)} KPIs)")

def init_training_curriculum():
    filepath = DATA_DIR / "training_curriculum.json"
    curriculum = {
        "curriculum_title": "Role-Based Medical Billing System Integration Training Program",
        "audience": "Evergreen Valley Family Medicine & Multi-Specialty Clinic Staff",
        "passing_grade_percent": 85.0,
        "modules": [
            {
                "module_id": "MOD-01",
                "target_role": "Front-Desk Coordinators & Patient Access",
                "title": "Front-Desk Master: Registration, Real-Time Eligibility & Point-of-Service Collections",
                "duration_hours": 8.0,
                "learning_objectives": [
                    "Master digital intake scanning and OCR document validation.",
                    "Execute and interpret real-time X12 270/271 insurance eligibility responses.",
                    "Identify inactive coverage, HMO primary care physician assignment gaps, and prior auth flags.",
                    "Calculate and collect exact patient copayments and deductible portions at check-in.",
                    "Enforce the zero-tolerance demographic duplicate prevention protocol."
                ],
                "practical_exercises": [
                    "Simulate 5 patient intake registrations with demographic anomaly detection.",
                    "Perform real-time eligibility inquiry on 3 commercial and 2 Medicare policies.",
                    "Process point-of-service copayment transaction and generate electronic receipt."
                ]
            },
            {
                "module_id": "MOD-02",
                "target_role": "Clinical Providers (MD, DO, NP, PA) & Medical Assistants",
                "title": "Clinical Documentation Integrity, Charge Slip Generation & Unsigned Note Governance",
                "duration_hours": 6.0,
                "learning_objectives": [
                    "Navigate structured EHR clinical documentation templates and smart phrases.",
                    "Select appropriate E/M service levels based on current applicable Medical Decision Making (MDM) or total time guidance, verified against encounter date of service and authorized CPT coding rules.",
                    "Complete electronic charge capture review before encounter closing.",
                    "Understand the clinical and financial consequences of unsigned notes and coding omissions.",
                    "Adhere to the mandatory 24-hour electronic signature compliance deadline."
                ],
                "practical_exercises": [
                    "Document a simulated complex Type 2 Diabetes encounter with 99214 MDM justification.",
                    "Review and sign an electronic charge slip with attached ICD-10 and CPT codes.",
                    "Respond to an automated EHR query regarding missing clinical documentation."
                ]
            },
            {
                "module_id": "MOD-03",
                "target_role": "Certified Medical Coders (CPC / CCS)",
                "title": "Advanced Real-Time Code Validation, NCCI Edits & Payer Edit Governance",
                "duration_hours": 12.0,
                "learning_objectives": [
                    "Configure and maintain the pre-bill validation rule engine.",
                    "Analyze and resolve NCCI Procedure-to-Procedure (PTP) edits and Medically Unlikely Edits (MUE).",
                    "Audit clinical records for medical necessity documentation supporting high-level E/M and minor procedures.",
                    "Apply CPT modifiers (-25, -59, -LT, -RT) strictly in accordance with CMS coding guidelines.",
                    "Execute the formal Provider Clarification Query protocol without leading the clinician."
                ],
                "practical_exercises": [
                    "Audit 5 complex outpatient encounters flagged by the scrubber for NCCI edit conflicts.",
                    "Draft a compliant, non-leading provider clarification query for an undocumented joint injection.",
                    "Test annual ICD-10-CM code update crosswalks in the sandbox environment."
                ]
            },
            {
                "module_id": "MOD-04",
                "target_role": "Billing Specialists & Payment Posting Staff",
                "title": "Electronic Claim Transmission (837P), Clearinghouse Reject Queues & ERA 835 Posting",
                "duration_hours": 12.0,
                "learning_objectives": [
                    "Manage daily electronic batch submissions of X12 837P professional claims.",
                    "Interpret clearinghouse 999 acknowledgments and 277CA claim acceptance reports.",
                    "Work the real-time clearinghouse rejection worklist with under-24-hour turnaround.",
                    "Oversee automated X12 835 Remittance Advice auto-posting and contractual write-off balancing.",
                    "Direct secondary crossover claims and generate clean electronic patient statements."
                ],
                "practical_exercises": [
                    "Correct and resubmit 3 claims rejected at the clearinghouse for NPI/taxonomy mismatches.",
                    "Post a simulated 835 ERA batch with contractual adjustments and reconcile to bank deposit.",
                    "Initiate an electronic appeal package for an improper medical necessity denial."
                ]
            },
            {
                "module_id": "MOD-05",
                "target_role": "Practice Managers, Compliance Officers & RCM Supervisors",
                "title": "Executive RCM Analytics, Denial Root-Cause Management & Regulatory Compliance",
                "duration_hours": 8.0,
                "learning_objectives": [
                    "Monitor the 11 key RCM integration KPIs across weekly and monthly executive dashboards.",
                    "Conduct root-cause denial analysis by CARC/RARC codes and provider documentation trends.",
                    "Oversee user access security controls, HIPAA audit log monitoring, and role-based permissions.",
                    "Audit the annual coding update release schedule and verify practice management fee schedules.",
                    "Maintain the integration risk register and coordinate quarterly disaster recovery simulations."
                ],
                "practical_exercises": [
                    "Analyze a monthly RCM dashboard and formulate an intervention plan for a 12% denial surge.",
                    "Perform a quarterly HIPAA audit log review of electronic PHI chart access records.",
                    "Calculate financial reconciliation variance across historical migration ledgers."
                ]
            }
        ],
        "assessment_questions": [
            {
                "question_id": "Q-01",
                "target_role": "Front-Desk Coordinators",
                "question": "When a real-time X12 271 eligibility inquiry returns a response indicating 'Inactive Policy / Coverage Terminated', what is the immediate mandatory protocol for front-desk staff?",
                "options": [
                    "Allow the patient to see the provider and bill the insurance anyway hoping it is retroactive.",
                    "Verify coverage details with the payer, check for alternative active insurance or secondary coverage, explain available billing and payment options to the patient, and adhere to the practice's approved financial policy.",
                    "Cancel the appointment immediately without discussing options with the patient.",
                    "Assign a fictional policy number and route the claim to the billing supervisor."
                ],
                "correct_option_index": 1,
                "explanation": "Front-desk staff must immediately verify coverage status with the payer, check for secondary or alternative active insurance policies, explain billing options clearly to the patient, and adhere to the practice's approved financial policy rather than automatically demanding credit card payment or immediately cancelling the visit.",
                "guideline_reference": "HFMA Patient Access Best Practices & CMS COB Guidelines"
            },
            {
                "question_id": "Q-02",
                "target_role": "Clinical Providers",
                "question": "Under current applicable Evaluation and Management (E/M) office or other outpatient visit guidelines, what documentation criteria determine code selection for a high-complexity established patient encounter (e.g., CPT 99215) when selecting a level of service based on Medical Decision Making (MDM)?",
                "options": [
                    "Documentation of a comprehensive 14-system review of systems and comprehensive past family/social history.",
                    "Meeting or exceeding the criteria for High complexity in at least two of the three MDM elements (Number and Complexity of Problems Addressed, Amount and/or Complexity of Data to be Reviewed and Analyzed, and Risk of Complications and/or Morbidity or Mortality of Patient Management), following applicable date-of-service guidance.",
                    "A rigid requirement that all three MDM elements meet the high-complexity threshold simultaneously.",
                    "Physician documented encounter time of at least 15 minutes, irrespective of the clinical problems addressed or data reviewed."
                ],
                "correct_option_index": 1,
                "explanation": "Under applicable E/M guidelines for office and outpatient visits, code selection based on Medical Decision Making requires meeting or exceeding the required level of complexity in at least two of the three MDM elements: (1) Number and Complexity of Problems Addressed, (2) Amount and/or Complexity of Data to be Reviewed and Analyzed, and (3) Risk of Complications and/or Morbidity or Mortality of Patient Management. Total time on the date of encounter is an alternate scoring basis. Specific thresholds and scoring definitions must be checked against the encounter date of service and authorized CPT guidance.",
                "guideline_reference": "Applicable AMA CPT & CMS Evaluation and Management (E/M) Coding Guidelines (verified by Date of Service)"
            },
            {
                "question_id": "Q-03",
                "target_role": "Medical Coders",
                "question": "When a minor surgical procedure (e.g., CPT 20610 Arthrocentesis) is performed on the same date of service as a significant, separately identifiable evaluation and management visit (CPT 99214), what modifier must be appended and where?",
                "options": [
                    "Modifier -59 appended to CPT 20610.",
                    "Modifier -25 appended to CPT 99214.",
                    "Modifier -51 appended to CPT 99214.",
                    "Modifier -76 appended to CPT 20610."
                ],
                "correct_option_index": 1,
                "explanation": "Modifier -25 is appended to the E/M code (99214) to designate a significant, separately identifiable evaluation and management service performed by the same physician on the same day as a minor surgical procedure.",
                "guideline_reference": "CMS NCCI Policy Manual, Chapter 1, Section E (Modifiers -25 and -59)"
            },
            {
                "question_id": "Q-04",
                "target_role": "Billing Specialists",
                "question": "What is the primary operational purpose of the pre-bill 'Hard-Stop' validation rule in the integrated practice management software?",
                "options": [
                    "To generate an informational banner that billing staff can permanently ignore.",
                    "To block the electronic generation and transmission of an X12 837P claim until fatal compliance errors (such as missing provider signature or invalid ICD-10 code) are rectified.",
                    "To automatically delete the encounter record from the database.",
                    "To change the assigned CPT code to a lower-paying service without human review."
                ],
                "correct_option_index": 1,
                "explanation": "Hard-stop validation rules completely prevent non-compliant or fatally flawed claims from entering the clearinghouse pipeline, eliminating downstream rejections and audit exposure.",
                "guideline_reference": "AAPC Compliance Audit Standards & WEDI Pre-Bill Best Practices"
            },
            {
                "question_id": "Q-05",
                "target_role": "Data Migration Staff",
                "question": "During legacy practice management data migration, why is a $0.00 financial reconciliation variance target established between the legacy accounts receivable trial balance and the target system ledger?",
                "options": [
                    "To satisfy a statutory $0.00 variance threshold specifically mandated by AICPA SOC 2 Type II criteria.",
                    "As a proposed migration accounting and data-integrity control to verify that all patient balances and open insurance claims are completely accounted for without loss, duplication, or unauthorized write-offs.",
                    "Because modern relational database management systems cannot physically commit unequal ledger transactions.",
                    "It is an optional guideline that can be bypassed if the overall trial balance variance is under $5,000."
                ],
                "correct_option_index": 1,
                "explanation": "Achieving a $0.00 financial reconciliation variance is a proposed internal migration accounting and data-integrity control. SOC 2 evaluates an organization's controls against applicable Trust Services Criteria; it does not prescribe a universal $0.00 accounts-receivable migration variance. This control establishes that legacy open balances, unallocated credits, and insurance claims transferred into the new PM system without ledger variance or unapproved write-offs, maintaining general ledger auditability.",
                "guideline_reference": "Healthcare Revenue Cycle Accounting Controls & HFMA Financial Data Governance Principles"
            },
            {
                "question_id": "Q-06",
                "target_role": "Practice Managers",
                "question": "What is the industry-standard definition and proposed integration target for 'Days in Accounts Receivable' (DAR) in a high-performing multi-specialty outpatient practice?",
                "options": [
                    "Total gross charges divided by 30 days; target: 90 days.",
                    "Total gross open AR divided by average daily billed charges; target: under 35 days.",
                    "Total claims submitted in a year; target: 365 days.",
                    "Number of days staff work per month; target: 20 days."
                ],
                "correct_option_index": 1,
                "explanation": "Days in AR equals Total Gross AR divided by Average Daily Billed Charges (Gross Charges / 90 days). A target under 35 days reflects a healthy, liquid revenue cycle.",
                "guideline_reference": "MGMA Performance and Productivity Benchmarks"
            },
            {
                "question_id": "Q-07",
                "target_role": "Medical Coders",
                "question": "When an annual ICD-10-CM code set update takes effect on October 1, how should encounters with dates of service on or after October 1 that use deleted codes be handled?",
                "options": [
                    "Submitted with the old code because the patient was diagnosed earlier.",
                    "Flagged by pre-bill scrubber hard-stops and crosswalked to the newly effective specific ICD-10-CM code for the current fiscal year.",
                    "Automatically converted to unlisted diagnosis code R69.",
                    "Written off as non-billable charity care."
                ],
                "correct_option_index": 1,
                "explanation": "ICD-10-CM codes are strictly governed by the Date of Service. Encounters occurring on or after October 1 must use the valid code set for that fiscal year; deleted codes result in immediate claim rejections.",
                "guideline_reference": "CMS & CDC National Center for Health Statistics (NCHS) ICD-10-CM Official Guidelines"
            },
            {
                "question_id": "Q-08",
                "target_role": "Billing Specialists",
                "question": "What does Claim Adjustment Reason Code (CARC) 16 signify when received on an electronic remittance advice (X12 835)?",
                "options": [
                    "Claim lacks information or has submission/billing error(s) which are needed for adjudication.",
                    "Procedure code is inconsistent with the modifier used.",
                    "Service not covered under the patient's benefit plan.",
                    "Payment was made to an out-of-network provider."
                ],
                "correct_option_index": 0,
                "explanation": "CARC 16 denotes: 'Claim/service lacks information or has submission/billing error(s) which is needed for adjudication.' Accompanied by Remittance Advice Remark Codes (RARC) specifying the exact missing element.",
                "guideline_reference": "X12 / Washington Publishing Company (WPC) CARC/RARC Standard Code List"
            },
            {
                "question_id": "Q-09",
                "target_role": "Compliance Officers",
                "question": "Under the HIPAA Security Rule (45 CFR Part 164, Subpart C), what is the regulatory structure governing the protection of electronic Protected Health Information (ePHI) transmitted over electronic communications networks?",
                "options": [
                    "Transmission security is completely optional for covered entities with fewer than 50 healthcare workers.",
                    "Transmission security safeguards are a required standard under 45 CFR § 164.312(e)(1), while encryption under § 164.312(e)(2)(ii) is an addressable implementation specification (e.g., implemented via modern protocols such as TLS 1.3 as a proposed technical safeguard).",
                    "Federal statutory law strictly mandates TLS 1.3 encryption and explicitly criminalizes all alternative cryptographic cipher suites.",
                    "Covered entities may transmit unencrypted ePHI across public networks provided patient social security numbers are redacted."
                ],
                "correct_option_index": 1,
                "explanation": "Under 45 CFR § 164.312(e)(1), transmission security is a required standard to guard against unauthorized access to ePHI transmitted over electronic communications networks. However, encryption under § 164.312(e)(2)(ii) is classified as an 'addressable' implementation specification rather than an inflexible statutory mandate. Covered entities must assess whether encryption is reasonable and appropriate, implementing robust protocols such as TLS 1.3 as a proposed technical standard or implementing equivalent alternative safeguards.",
                "guideline_reference": "45 CFR § 164.312(e) (HIPAA Security Rule: Transmission Security Standards & Addressable Implementation Specifications)"
            },
            {
                "question_id": "Q-10",
                "target_role": "Practice Managers",
                "question": "If an automated claim scrubber detects a potential medical necessity gap between a procedure and diagnosis code, what is the proper operational resolution?",
                "options": [
                    "Alter the diagnosis code to a covered diagnosis without reviewing medical records.",
                    "Route the encounter to a certified medical coder for clinical record review and, if necessary, issue a non-leading clarification query to the provider.",
                    "Delete the procedure from the claim and bill only the office visit.",
                    "Submit the claim anyway and wait for the payer to deny it."
                ],
                "correct_option_index": 1,
                "explanation": "Never change codes to match coverage policies without clinical documentation support. A certified coder must review the chart and query the clinician if necessary to ensure coding compliance.",
                "guideline_reference": "AHIMA & AAPC Standards of Ethical Coding"
            }
        ]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(curriculum, f, indent=2)
    print(f"Initialized training curriculum & assessment: {filepath} ({len(curriculum['modules'])} modules, {len(curriculum['assessment_questions'])} questions)")

if __name__ == "__main__":
    init_software_comparison()
    init_risk_register()
    init_migration_sample()
    init_kpi_definitions()
    init_training_curriculum()
    print("All Week 4 reference data initialized successfully.")
