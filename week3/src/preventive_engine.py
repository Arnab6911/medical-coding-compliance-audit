"""Preventive controls and continuous improvement engine for Week 3 billing simulation."""

from typing import Dict, List, Optional, Any

from .models import (
    BillingScenario, DetectionFinding, PreventiveControl
)


class PreventiveEngine:
    """Maps billing error categories to systemic, operational, and clinical preventive controls

    to prevent recurring claim denials and regulatory non-compliance.
    """

    def __init__(self, error_categories_meta: Optional[Dict[str, Any]] = None):
        self.error_categories_meta = error_categories_meta or {}
        self.controls_catalog = self._build_controls_catalog()

    def _build_controls_catalog(self) -> Dict[str, PreventiveControl]:
        """Build comprehensive catalog of preventive controls across all error dimensions."""
        return {
            "ERR_ICD_INCORRECT": PreventiveControl(
                error_code="ERR_ICD_INCORRECT",
                control_name="Automated Acute vs. Chronic Diagnostic Code Cross-Checks",
                description="Configure EHR and coding encoder with algorithmic validation rules flagging chronic condition codes (e.g., M23.23) when clinical text explicitly documents acute trauma, twisting injuries, or initial encounters.",
                responsible_department="Health Information Management (HIM) / Medical Coding",
                implementation_frequency="Pre-Bill Scrubbing (Real-Time per Encounter)",
                ehr_hard_stop=True,
                expected_benefit="Reduces recurrence risk for medical necessity rejections and decreases claim rework.",
                regulatory_or_best_practice="ICD-10-CM Official Guidelines Section I.B (General Coding Guidelines)."
            ),
            "ERR_ICD_SPECIFICITY": PreventiveControl(
                error_code="ERR_ICD_SPECIFICITY",
                control_name="EHR Specificity Prompter & Manifestation Linking",
                description="Deploy clinical documentation prompts alerting coders and clinicians when an unspecified diagnostic code (.9) is selected despite documented laboratory staging (e.g., eGFR staging for CKD) or anatomical laterality.",
                responsible_department="Clinical Documentation Improvement (CDI) & Coding",
                implementation_frequency="Concurrent Chart Review / Daily Encoder Scans",
                ehr_hard_stop=False,
                expected_benefit="Maximizes risk-adjustment accuracy (HCC coding) and helps prevent payer requests for medical records.",
                regulatory_or_best_practice="CMS Risk Adjustment and ICD-10-CM Combination Coding Mandates."
            ),
            "ERR_CPT_INCORRECT": PreventiveControl(
                error_code="ERR_CPT_INCORRECT",
                control_name="Practice Management Established Patient History Verification",
                description="Integrate automated billing rules crosswalking CPT selection against the Master Patient Index appointment ledger to block new patient preventive codes (99381-99387) for patients with visits within 36 months.",
                responsible_department="Patient Access & Charge Entry",
                implementation_frequency="Point of Charge Entry (Real-Time)",
                ehr_hard_stop=True,
                expected_benefit="Helps prevent avoidable CPT downcoding and initial vs established patient denials.",
                regulatory_or_best_practice="AMA CPT Evaluation and Management Services Guidelines – Patient Status Definition."
            ),
            "ERR_DUPLICATE_BILLING": PreventiveControl(
                error_code="ERR_DUPLICATE_BILLING",
                control_name="Algorithmic Duplicate Charge Suppression & Batch Interlock",
                description="Implement an automated pre-submission rule that flags and suppresses identical CPT codes billed on the same patient, date of service, and provider unless an appropriate repeat/distinct modifier (e.g., 59/76/XS) is verified.",
                responsible_department="Revenue Cycle IT & Central Billing Office",
                implementation_frequency="Continuous Pre-Bill Batch Auditing",
                ehr_hard_stop=True,
                expected_benefit="Substantially reduces CARC 18 duplicate billing denials and helps mitigate compliance overpayment risks.",
                regulatory_or_best_practice="Medicare Claims Processing Manual Pub 100-04 Chapter 1 Section 80."
            ),
            "ERR_EM_UNSUPPORTED": PreventiveControl(
                error_code="ERR_EM_UNSUPPORTED",
                control_name="Provider Medical Decision Making (MDM) Coaching & Template Guardrails",
                description="Establish mandatory provider documentation coaching on 2021/2023 AMA E/M guidelines, combined with EHR note templates calculating MDM complexity based on documented problems, data reviewed, and clinical risk.",
                responsible_department="Physician Advisory Committee & Coding Compliance",
                implementation_frequency="Quarterly Provider Coaching & Monthly Chart Sampling",
                ehr_hard_stop=False,
                expected_benefit="Mitigates payer downcoding takebacks (CARC 150) and defends against False Claims Act exposure for upcoding.",
                regulatory_or_best_practice="AMA/CMS 2021/2023 Office/Outpatient E/M Documentation Standards."
            ),
            "ERR_SIGNATURE_MISSING": PreventiveControl(
                error_code="ERR_SIGNATURE_MISSING",
                control_name="EHR Electronic Signature Enforcement & Billing Lock",
                description="Configure the electronic health record system to prohibit billing charge release on progress notes with 'Draft' status, requiring multi-factor clinician authentication with cryptographically verified timestamps.",
                responsible_department="Clinical Operations & Health Informatics",
                implementation_frequency="Automated System Gatekeeper (Real-Time)",
                ehr_hard_stop=True,
                expected_benefit="Supports early detection of unauthenticated records and helps prevent signature-related claim delays and recoupments.",
                regulatory_or_best_practice="Medicare Program Integrity Manual Pub 100-08 Chapter 3 Section 3.3.2.4."
            ),
            "ERR_DOCUMENTATION_MISSING": PreventiveControl(
                error_code="ERR_DOCUMENTATION_MISSING",
                control_name="Procedural Charge-Note Mandatory Binding",
                description="Enforce architectural coupling in the EHR requiring a completed and signed procedural template (including consent, anatomical site, technique, and pathology requisition) before a surgical CPT charge can post to the ledger.",
                responsible_department="Clinical Staff & HIM / Medical Records",
                implementation_frequency="Point of Care Encounter Finalization",
                ehr_hard_stop=True,
                expected_benefit="Reduces Additional Documentation Requests (ADRs) for unrecorded procedures and helps prevent unsubstantiated billing.",
                regulatory_or_best_practice="CMS Conditions of Coverage – Medical Record Documentation Completeness."
            ),
            "ERR_SUBSCRIBER_INFO": PreventiveControl(
                error_code="ERR_SUBSCRIBER_INFO",
                control_name="Master Patient Index (MPI) Mandatory Guarantor Linkage for Minors",
                description="Configure patient registration software to mandate verified primary subscriber ID and relationship codes for all patients under 18 years of age, preventing pediatric dependents from being submitted as primary policyholders.",
                responsible_department="Patient Access & Front-Desk Intake",
                implementation_frequency="At Every Patient Registration & Check-In",
                ehr_hard_stop=True,
                expected_benefit="Reduces clearinghouse 277CA Loop 2000B syntax rejections and supports first-pass reimbursement.",
                regulatory_or_best_practice="HIPAA ANSI ASC X12N 837P Implementation Guide Section 2.3.1."
            ),
            "ERR_DEMOGRAPHIC_TYPO": PreventiveControl(
                error_code="ERR_DEMOGRAPHIC_TYPO",
                control_name="Real-Time 270/271 Eligibility Verification with ID Cross-Matching",
                description="Implement automated electronic 270/271 eligibility inquiries at appointment scheduling and 48 hours prior to service, cross-referencing payer demographic databases against government-issued photo identification.",
                responsible_department="Patient Registration & Pre-Service Verification",
                implementation_frequency="48 Hours Pre-Service and Day of Encounter",
                ehr_hard_stop=False,
                expected_benefit="Significantly reduces demographic mismatch rejections (CARC 31) and shortens Days in A/R.",
                regulatory_or_best_practice="HFMA Patient Financial Communications Best Practices."
            ),
            "ERR_AUTH_REFERRAL_MISSING": PreventiveControl(
                error_code="ERR_AUTH_REFERRAL_MISSING",
                control_name="Specialist Appointment Scheduling Referral Gatekeeper",
                description="Deploy an electronic referral tracking module that prohibits specialist appointment confirmation without an active, verified Primary Care Physician (PCP) referral number linked in the practice management system.",
                responsible_department="Central Scheduling & Referral Coordination",
                implementation_frequency="Point of Scheduling & 24 Hours Pre-Visit",
                ehr_hard_stop=True,
                expected_benefit="Substantially reduces non-reimbursable HMO CARC 197 authorization denials and helps protect in-network revenue.",
                regulatory_or_best_practice="Commercial Managed Care HMO Provider Network Operating Agreements."
            ),
            "ERR_MEDICAL_NECESSITY": PreventiveControl(
                error_code="ERR_MEDICAL_NECESSITY",
                control_name="Point-of-Order Clinical Decision Support (CDS) for LCD/NCD",
                description="Implement an EHR clinical decision support tool that checks diagnostic orders (e.g., chest radiography) against Medicare Local Coverage Determinations (LCDs) in real time, alerting physicians when ordered tests lack covered indications.",
                responsible_department="Physician Leadership & Quality Compliance",
                implementation_frequency="Point of Computerized Physician Order Entry (CPOE)",
                ehr_hard_stop=False,
                expected_benefit="Helps prevent non-covered diagnostic testing denials (CARC 50) and ensures proper clinical documentation of symptoms.",
                regulatory_or_best_practice="Medicare Claims Processing Manual Pub 100-04 Chapter 23 Section 30."
            ),
            "ERR_MODIFIER_APPLICATION": PreventiveControl(
                error_code="ERR_MODIFIER_APPLICATION",
                control_name="Automated NCCI Edit Scrubber & Modifier 25 Validation",
                description="Incorporate CMS National Correct Coding Initiative (NCCI) edit tables into the pre-bill claim scrubber, prompting coders to verify separate E/M documentation before releasing dual-service claims (minor surgery + E/M).",
                responsible_department="HIM / Coding & Billing Pre-Scrubber",
                implementation_frequency="Continuous Pre-Bill Claim Review",
                ehr_hard_stop=False,
                expected_benefit="Supports appropriate reimbursement for separate E/M services while helping prevent unbundled procedure denials (CARC 97).",
                regulatory_or_best_practice="CMS NCCI Policy Manual for Medicare Services Chapter 1 Section E."
            ),
            "ERR_UNITS_QUANTITY": PreventiveControl(
                error_code="ERR_UNITS_QUANTITY",
                control_name="Pre-Bill Medically Unlikely Edit (MUE) Range Verification",
                description="Configure charge entry software with CMS Medically Unlikely Edit (MUE) tables and time-to-unit calculators, blocking submission of hydration/infusion codes exceeding maximum daily unit allowances.",
                responsible_department="Charge Capture & Billing Audit",
                implementation_frequency="Point of Charge Entry & Batch Scrubber",
                ehr_hard_stop=True,
                expected_benefit="Helps prevent CARC 151 unit-threshold denials and reduces charge entry transcription errors.",
                regulatory_or_best_practice="CMS Medically Unlikely Edits (MUE) Operating Policy."
            ),
            "ERR_COB_ROUTING": PreventiveControl(
                error_code="ERR_COB_ROUTING",
                control_name="Annual Coordination of Benefits (COB) & MSP Screening Intake",
                description="Require all patients age 65 and older to complete an electronic Medicare Secondary Payer (MSP) questionnaire annually, automatically establishing Medicare Part B as primary and commercial policies as secondary.",
                responsible_department="Front-Desk Intake & Central Billing Office",
                implementation_frequency="Annual Intake Update & Pre-Service Verification",
                ehr_hard_stop=True,
                expected_benefit="Reduces recurrence risk for CARC 22 wrong-primary payer denials and supports prompt primary claim submission.",
                regulatory_or_best_practice="Medicare Secondary Payer (MSP) Manual Pub 100-05 Chapter 3."
            ),
            "ERR_CALCULATION_BALANCE": PreventiveControl(
                error_code="ERR_CALCULATION_BALANCE",
                control_name="Practice Management Strict Waterfall Calculation Engine",
                description="Program the practice management billing ledger with strict mathematical cost-sharing algorithms enforcing: Insurer Paid + Patient Due = Contractual Allowed Amount, prohibiting double-counting of copays and deductibles.",
                responsible_department="Patient Financial Services & Billing Systems IT",
                implementation_frequency="Real-Time Ledger Transaction Processing",
                ehr_hard_stop=True,
                expected_benefit="Enforces compliance with federal balance-billing regulations, reducing patient billing complaints and overcharge risks.",
                regulatory_or_best_practice="No Surprises Act (Consolidated Appropriations Act 2021) & In-Network Contracts."
            ),
            "ERR_SUBMISSION_REJECTED": PreventiveControl(
                error_code="ERR_SUBMISSION_REJECTED",
                control_name="Clearinghouse Gateway Pre-Submission Syntax Validation & NPI Audit",
                description="Implement an automated EDI test harness that parses outgoing ANSI ASC X12N 837P batch envelopes for mandatory Loop 2010AA NPI numbers and taxonomy codes before releasing batches to clearinghouses.",
                responsible_department="Billing IT & Revenue Cycle Clearinghouse Operations",
                implementation_frequency="Daily Outbound EDI Batch Release",
                ehr_hard_stop=True,
                expected_benefit="Supports high first-pass clearinghouse acceptance and helps prevent avoidable 277CA syntax rejections.",
                regulatory_or_best_practice="WPC ASC X12N 837 Professional 005010X222A1 Implementation Standards."
            ),
            "QUERY_NO_ERROR": PreventiveControl(
                error_code="QUERY_NO_ERROR",
                control_name="Audit Query Sampling Threshold Optimization",
                description="Periodically tune automated compliance auditing algorithms to incorporate clinical acuity parameters, reducing unnecessary administrative holds on validated acute emergency E/M encounters.",
                responsible_department="Compliance & Internal Audit",
                implementation_frequency="Semi-Annual Audit Rule Refinement",
                ehr_hard_stop=False,
                expected_benefit="Reduces administrative audit workload by 30% without compromising compliance oversight.",
                regulatory_or_best_practice="OIG Compliance Program Guidance for Third-Party Medical Billing Companies."
            ),
            "QUERY_PENDING_DOCS": PreventiveControl(
                error_code="QUERY_PENDING_DOCS",
                control_name="External Document Intake & EHR Indexing SLA",
                description="Establish a formal Service Level Agreement (SLA) requiring outside clinical consultation notes and laboratory reports to be scanned and indexed into the EHR within 24 hours of receipt before appointment check-in.",
                responsible_department="Medical Records / Health Information Management",
                implementation_frequency="Daily Incoming Document Queue Processing",
                ehr_hard_stop=False,
                expected_benefit="Ensures comprehensive clinical record availability for clinical care and billing compliance.",
                regulatory_or_best_practice="AHIMA Clinical Documentation Integrity Best Practice Guidelines."
            )
        }

    def get_control_for_scenario(self, scenario: BillingScenario) -> PreventiveControl:
        """Fetch corresponding preventive control for a given scenario's error category."""
        return self.controls_catalog.get(
            scenario.error_category,
            PreventiveControl(
                error_code=scenario.error_category,
                control_name=f"Standard Operational Control ({scenario.error_category})",
                description=scenario.preventive_measure,
                responsible_department="Revenue Cycle Management",
                implementation_frequency="Periodic Operational Review",
                ehr_hard_stop=False,
                expected_benefit="Reduces billing exceptions and improves billing compliance.",
                regulatory_or_best_practice="Standard Healthcare Billing Operational Practices."
            )
        )

    def get_control_by_code(self, error_code: str) -> PreventiveControl:
        """Fetch preventive control by error category code."""
        return self.controls_catalog.get(
            error_code,
            PreventiveControl(
                error_code=error_code,
                control_name=f"Standard Operational Control ({error_code})",
                description="Standard operational review and control.",
                responsible_department="Revenue Cycle Management",
                implementation_frequency="Periodic Operational Review",
                ehr_hard_stop=False,
                expected_benefit="Reduces billing exceptions.",
                regulatory_or_best_practice="Standard Healthcare Billing Operational Practices."
            )
        )

    def get_all_controls(self) -> List[PreventiveControl]:
        """Return full list of all preventive controls across the organization."""
        return list(self.controls_catalog.values())
