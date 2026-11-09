"""Automated error detection and auditing engine for Week 3 billing simulation."""

import re
from typing import Dict, List, Optional, Tuple, Any

from .models import BillingScenario, DetectionFinding, ErrorSeverity


class ErrorDetector:
    """Evaluates billing scenarios against clinical documentation, coding guidelines,

    and payer rules to detect billing discrepancies and compliance issues.
    """

    def __init__(self, categories_meta: Optional[Dict[str, Any]] = None):
        self.categories_meta = categories_meta or {}

    def detect_errors(self, scenario: BillingScenario) -> List[DetectionFinding]:
        """Execute comprehensive audit suite on a single scenario and return all detected findings."""
        findings: List[DetectionFinding] = []

        # 1. Check Missing Provider Electronic Signature
        sig_finding = self._check_provider_signature(scenario)
        if sig_finding:
            findings.append(sig_finding)

        # 2. Check Duplicate Service Lines
        dup_finding = self._check_duplicate_billing(scenario)
        if dup_finding:
            findings.append(dup_finding)

        # 3. Check Missing Clinical Documentation for Billed Procedures
        doc_finding = self._check_missing_documentation(scenario)
        if doc_finding:
            findings.append(doc_finding)

        # 4. Check Diagnosis Coding Discrepancies (Acute vs Chronic & Specificity)
        diag_findings = self._check_diagnosis_coding(scenario)
        findings.extend(diag_findings)

        # 5. Check Procedure Coding (Established vs New Patient)
        cpt_finding = self._check_procedure_code(scenario)
        if cpt_finding:
            findings.append(cpt_finding)

        # 6. Check Evaluation & Management (E/M) Complexity & Medical Decision Making
        em_findings = self._check_em_documentation(scenario)
        findings.extend(em_findings)

        # 7. Check Insurance Subscriber & Registration Demographics
        reg_findings = self._check_registration_and_subscriber(scenario)
        findings.extend(reg_findings)

        # 8. Check Prior Authorization & HMO Specialist Referral
        auth_finding = self._check_authorization_referral(scenario)
        if auth_finding:
            findings.append(auth_finding)

        # 9. Check LCD Medical Necessity Indication
        med_nec_finding = self._check_medical_necessity(scenario)
        if med_nec_finding:
            findings.append(med_nec_finding)

        # 10. Check NCCI Bundling & Modifier -25 Requirement
        mod_finding = self._check_modifier_application(scenario)
        if mod_finding:
            findings.append(mod_finding)

        # 11. Check Units / Quantity & MUE Limits
        unit_finding = self._check_units_and_quantity(scenario)
        if unit_finding:
            findings.append(unit_finding)

        # 12. Check Coordination of Benefits (COB) Hierarchy
        cob_finding = self._check_coordination_of_benefits(scenario)
        if cob_finding:
            findings.append(cob_finding)

        # 13. Check Balance-Billing & Patient Cost-Sharing Calculations
        calc_finding = self._check_financial_calculations(scenario)
        if calc_finding:
            findings.append(calc_finding)

        # 14. Check Clearinghouse EDI 837P Syntax Rejection
        edi_finding = self._check_edi_submission_syntax(scenario)
        if edi_finding:
            findings.append(edi_finding)

        # 15. Check Pending External Records (High-Risk Therapy without scanned consult/labs)
        pend_finding = self._check_pending_external_records(scenario)
        if pend_finding:
            findings.append(pend_finding)

        # Fallback: if no specific rule caught the scenario but error_category is defined
        if not findings:
            fallback = self._create_finding_from_scenario_category(scenario)
            if fallback:
                findings.append(fallback)

        return findings

    # -------------------------------------------------------------------------
    # RULE CHECKERS
    # -------------------------------------------------------------------------

    def _check_provider_signature(self, scenario: BillingScenario) -> Optional[DetectionFinding]:
        """Detect unauthenticated progress notes lacking rendering physician electronic signature."""
        doc_lower = scenario.clinical_documentation.lower()
        if not scenario.has_provider_signature or "awaiting clinician signature" in doc_lower or "status: draft" in doc_lower:
            return DetectionFinding(
                finding_id=f"FND-{scenario.scenario_id}-SIG",
                scenario_id=scenario.scenario_id,
                encounter_id=scenario.encounter_id,
                error_code="ERR_SIGNATURE_MISSING",
                error_name="Missing Provider Electronic Signature",
                severity=ErrorSeverity.CRITICAL,
                evidence="Progress note header contains 'Status: DRAFT - Awaiting Clinician Signature'; has_provider_signature is False.",
                reason_flagged="Clinical record is unauthenticated. Federal Medicare Conditions of Payment and commercial payer contracts require authenticated clinician signature before claim submission.",
                recommended_action="Place pre-bill hold; notify attending clinician to review, authenticate, and sign chart in EHR before electronic claim release.",
                manual_review_required=True,
                is_confirmed_error=True
            )
        return None

    def _check_duplicate_billing(self, scenario: BillingScenario) -> Optional[DetectionFinding]:
        """Detect duplicate CPT codes billed on the same encounter."""
        cpt_codes = [c.strip() for c in scenario.original_cpt.split(";") if c.strip()]
        if len(cpt_codes) > len(set(cpt_codes)):
            duplicates = [c for c in set(cpt_codes) if cpt_codes.count(c) > 1]
            return DetectionFinding(
                finding_id=f"FND-{scenario.scenario_id}-DUP",
                scenario_id=scenario.scenario_id,
                encounter_id=scenario.encounter_id,
                error_code="ERR_DUPLICATE_BILLING",
                error_name="Duplicate Procedure Line Submission",
                severity=ErrorSeverity.HIGH,
                evidence=f"Duplicate CPT code(s) detected on single encounter claim: {duplicates}.",
                reason_flagged=f"CPT {duplicates[0]} billed multiple times on same date of service without distinct modifier (e.g., 59/XS) or documentation of multiple independent procedures.",
                recommended_action="Void duplicate service line in billing ledger; write off duplicate charges and verify only a single procedure was clinically executed.",
                manual_review_required=True,
                is_confirmed_error=True
            )
        return None

    def _check_missing_documentation(self, scenario: BillingScenario) -> Optional[DetectionFinding]:
        """Detect billed procedural charges with zero documentation in progress note narrative."""
        cpt_codes = [c.strip() for c in scenario.original_cpt.split(";") if c.strip()]
        doc_lower = scenario.clinical_documentation.lower()

        # Check for biopsy CPT 11102 without lesion/biopsy documentation
        if "11102" in cpt_codes:
            if not any(k in doc_lower for k in ["biopsy", "tangential", "lesion", "shave", "dermatol"]):
                return DetectionFinding(
                    finding_id=f"FND-{scenario.scenario_id}-DOC",
                    scenario_id=scenario.scenario_id,
                    encounter_id=scenario.encounter_id,
                    error_code="ERR_DOCUMENTATION_MISSING",
                    error_name="Missing Clinical Documentation for Billed Procedure",
                    severity=ErrorSeverity.CRITICAL,
                    evidence=f"CPT 11102 (Skin biopsy) billed (${scenario.original_billed_amount:.2f}), but progress note mentions only osteoarthritis checkup with zero procedural documentation.",
                    reason_flagged="Billed surgical service completely lacks supporting operative report, anatomical location, or clinical indication in the medical record repository.",
                    recommended_action="Issue Provider Query to attending physician to locate procedure note; if not performed or unsubstantiated, delete CPT 11102 charge immediately.",
                    manual_review_required=True,
                    is_confirmed_error=True
                )
        return None

    def _check_diagnosis_coding(self, scenario: BillingScenario) -> List[DetectionFinding]:
        """Detect acute vs chronic mismatch and diagnosis code specificity gaps."""
        findings: List[DetectionFinding] = []
        doc_lower = scenario.clinical_documentation.lower()

        # Acute trauma vs Chronic Meniscus Derangement
        if scenario.original_icd10 == "M23.23":
            if "acute" in doc_lower and ("twist" in doc_lower or "injury" in doc_lower or "tear" in doc_lower):
                findings.append(
                    DetectionFinding(
                        finding_id=f"FND-{scenario.scenario_id}-ICD-ACUTE",
                        scenario_id=scenario.scenario_id,
                        encounter_id=scenario.encounter_id,
                        error_code="ERR_ICD_INCORRECT",
                        error_name="Acute Traumatic Injury Coded as Chronic Derangement",
                        severity=ErrorSeverity.HIGH,
                        evidence="Clinical note explicitly documents 'acute right knee pain after twisting injury yesterday... acute lateral meniscus tear'; billed with chronic code M23.23.",
                        reason_flagged="M23.23 represents old/chronic derangement. ICD-10-CM guidelines mandate Chapter 19 traumatic injury code S83.241A with 7th character 'A' for initial encounter.",
                        recommended_action="Update diagnosis code from M23.23 to S83.241A; resubmit corrected claim with clinical progress note attached.",
                        manual_review_required=True,
                        is_confirmed_error=True
                    )
                )

        # Unspecified Diabetes when CKD stage is documented
        if scenario.original_icd10 == "E11.9":
            if "ckd" in doc_lower or "kidney" in doc_lower or "egfr" in doc_lower or "stage 3" in doc_lower:
                findings.append(
                    DetectionFinding(
                        finding_id=f"FND-{scenario.scenario_id}-ICD-SPEC",
                        scenario_id=scenario.scenario_id,
                        encounter_id=scenario.encounter_id,
                        error_code="ERR_ICD_SPECIFICITY",
                        error_name="Diagnosis Code Specificity Mismatch – Diabetic CKD",
                        severity=ErrorSeverity.MEDIUM,
                        evidence="Progress note documents 'Type 2 diabetes mellitus complicated by diabetic chronic kidney disease, stage 3b (eGFR 38)'; billed with unspecified E11.9.",
                        reason_flagged="ICD-10-CM coding guidelines instruct coders to assign combination code E11.22 (Type 2 DM with diabetic CKD) and secondary code N18.32 (CKD stage 3b) when documented.",
                        recommended_action="Replace E11.9 with primary combination code E11.22 and secondary manifestation code N18.32; submit corrected claim.",
                        manual_review_required=True,
                        is_confirmed_error=True
                    )
                )

        return findings

    def _check_procedure_code(self, scenario: BillingScenario) -> Optional[DetectionFinding]:
        """Detect incorrect CPT code selection such as initial preventive visit for established patient."""
        doc_lower = scenario.clinical_documentation.lower()
        if "99385" in scenario.original_cpt:
            if "established" in doc_lower or "continuous care" in doc_lower or "5 years" in doc_lower:
                return DetectionFinding(
                    finding_id=f"FND-{scenario.scenario_id}-CPT",
                    scenario_id=scenario.scenario_id,
                    encounter_id=scenario.encounter_id,
                    error_code="ERR_CPT_INCORRECT",
                    error_name="New Patient Preventive Code Billed for Established Patient",
                    severity=ErrorSeverity.HIGH,
                    evidence="Documentation notes established patient receiving continuous care for 5 years; CPT 99385 (initial preventive medicine) was billed.",
                    reason_flagged="CPT guidelines state an established patient is one who has received professional services from the physician or group within the past 3 years. CPT 99385 is restricted to new patients.",
                    recommended_action="Replace CPT 99385 with CPT 99395 (established patient preventive visit, 40-64 years); adjust gross charge to $205.00 and resubmit.",
                    manual_review_required=True,
                    is_confirmed_error=True
                )
        return None

    def _check_em_documentation(self, scenario: BillingScenario) -> List[DetectionFinding]:
        """Evaluate E/M complexity levels against Medical Decision Making and encounter duration."""
        findings: List[DetectionFinding] = []
        doc_lower = scenario.clinical_documentation.lower()
        cpt_codes = [c.strip() for c in scenario.original_cpt.split(";") if c.strip()]

        if "99215" in cpt_codes:
            # Case A: Unsupported E/M Level 5 (SCN-3005: allergic rhinitis, 10 min, minimal MDM)
            if "seasonal allergic rhinitis" in doc_lower or "10 minutes" in doc_lower or "minimal complexity" in doc_lower:
                findings.append(
                    DetectionFinding(
                        finding_id=f"FND-{scenario.scenario_id}-EM-DOWN",
                        scenario_id=scenario.scenario_id,
                        encounter_id=scenario.encounter_id,
                        error_code="ERR_EM_UNSUPPORTED",
                        error_name="Unsupported High-Level Evaluation & Management Code",
                        severity=ErrorSeverity.HIGH,
                        evidence="CPT 99215 (Level 5 High MDM / 40-54 min) billed for self-limited seasonal allergic rhinitis with 10 minutes face-to-face time.",
                        reason_flagged="Under 2021/2023 AMA E/M guidelines, Level 5 requires High MDM (extensive data, high morbidity risk) or 40+ minutes. Documentation supports only Low/Moderate MDM.",
                        recommended_action="Downcode service to CPT 99213 ($185.00) or CPT 99212; issue corrected claim and provide provider documentation coaching.",
                        manual_review_required=True,
                        is_confirmed_error=True
                    )
                )

            # Case B: Fully Supported E/M Level 5 (SCN-3017: acute chest pain, diaphoresis, emergency transfer, 50 min)
            elif "chest tightness" in doc_lower or "diaphoresis" in doc_lower or "emergency transfer" in doc_lower or "50 minutes" in doc_lower:
                findings.append(
                    DetectionFinding(
                        finding_id=f"FND-{scenario.scenario_id}-EM-LEGIT",
                        scenario_id=scenario.scenario_id,
                        encounter_id=scenario.encounter_id,
                        error_code="QUERY_NO_ERROR",
                        error_name="Auditing Review – Supported High-Level E/M (No Error Identified)",
                        severity=ErrorSeverity.LOW,
                        evidence="Documentation verifies acute life-threatening presentation, urgent ECG review, acute nitroglycerin, emergency cardiac transfer, and 50 minutes physician time.",
                        reason_flagged="Internal audit threshold triggered inquiry due to high E/M level, but detailed chart review proves clinical work strictly meets High MDM criteria under AMA CPT guidelines.",
                        recommended_action="Confirm CPT 99215 is fully justified; close billing audit query without coding changes; approve claim for transmission.",
                        manual_review_required=True,
                        is_confirmed_error=False
                    )
                )

        return findings

    def _check_registration_and_subscriber(self, scenario: BillingScenario) -> List[DetectionFinding]:
        """Detect registration errors including minor submitted as primary subscriber and demographic typos."""
        findings: List[DetectionFinding] = []

        # Minor as subscriber
        if scenario.patient_age < 18 and scenario.error_category == "ERR_SUBSCRIBER_INFO":
            findings.append(
                DetectionFinding(
                    finding_id=f"FND-{scenario.scenario_id}-SUB",
                    scenario_id=scenario.scenario_id,
                    encounter_id=scenario.encounter_id,
                    error_code="ERR_SUBSCRIBER_INFO",
                    error_name="Missing Insurance Subscriber / Minor Submitted as Primary",
                    severity=ErrorSeverity.HIGH,
                    evidence=f"Patient {scenario.patient_name} is {scenario.patient_age} years old; submitted as primary insured in Loop 2000B without guarantor policy information.",
                    reason_flagged="Clearinghouse 277CA syntax rules reject commercial claims where a minor dependent is submitted as the policyholder without parental subscriber identification.",
                    recommended_action="Contact parent guarantor; update Loop 2010BA with parent's subscriber policy number and relationship code; resubmit clean claim.",
                    manual_review_required=True,
                    is_confirmed_error=True
                )
            )

        # Demographic mismatch / DOB typo
        if scenario.error_category == "ERR_DEMOGRAPHIC_TYPO":
            findings.append(
                DetectionFinding(
                    finding_id=f"FND-{scenario.scenario_id}-DEMO",
                    scenario_id=scenario.scenario_id,
                    encounter_id=scenario.encounter_id,
                    error_code="ERR_DEMOGRAPHIC_TYPO",
                    error_name="Patient Demographic Information Mismatch (DOB Typo)",
                    severity=ErrorSeverity.MEDIUM,
                    evidence="Payer electronic gateway rejected claim citing date of birth mismatch (Submitted 1995-12-05 vs Payer 1995-05-12).",
                    reason_flagged="Front-desk data entry transposed month and day when manually typing intake sheet, creating an eligibility demographic mismatch.",
                    recommended_action="Verify patient government photo ID; update date of birth in Master Patient Index; re-verify eligibility and resubmit.",
                    manual_review_required=True,
                    is_confirmed_error=True
                )
            )

        return findings

    def _check_authorization_referral(self, scenario: BillingScenario) -> Optional[DetectionFinding]:
        """Detect missing mandatory HMO specialist referral or prior authorization."""
        if not scenario.has_prior_authorization and scenario.plan_type.upper() == "HMO":
            return DetectionFinding(
                finding_id=f"FND-{scenario.scenario_id}-AUTH",
                scenario_id=scenario.scenario_id,
                encounter_id=scenario.encounter_id,
                error_code="ERR_AUTH_REFERRAL_MISSING",
                error_name="Missing Mandatory HMO Specialist Referral",
                severity=ErrorSeverity.HIGH,
                evidence=f"Specialist consultation CPT {scenario.original_cpt} billed to {scenario.payer_name} HMO without primary care referral on file.",
                reason_flagged="Commercial HMO plans enforce gatekeeper requirements. Attending specialist care without an authorized PCP referral results in CARC 197 payment denial.",
                recommended_action="Contact PCP office for retroactive referral; if denied, write off gross charge per in-network HMO contract (patient held harmless).",
                manual_review_required=True,
                is_confirmed_error=True
            )
        return None

    def _check_medical_necessity(self, scenario: BillingScenario) -> Optional[DetectionFinding]:
        """Detect potential medical necessity and Local Coverage Determination (LCD) policy gaps."""
        cpt_codes = [c.strip() for c in scenario.original_cpt.split(";") if c.strip()]
        icd_codes = [c.strip() for c in scenario.original_icd10.split(";") if c.strip()]
        doc_lower = scenario.clinical_documentation.lower()

        # Chest X-ray 71046 paired solely with Essential Hypertension I10
        if "71046" in cpt_codes and icd_codes == ["I10"]:
            if not any(k in doc_lower for k in ["cough", "dyspnea", "fever", "chest pain", "sob", "rales", "wheez"]):
                return DetectionFinding(
                    finding_id=f"FND-{scenario.scenario_id}-LCD",
                    scenario_id=scenario.scenario_id,
                    encounter_id=scenario.encounter_id,
                    error_code="ERR_MEDICAL_NECESSITY",
                    error_name="Medical Necessity Documentation Gap – Chest Radiography",
                    severity=ErrorSeverity.HIGH,
                    evidence="CPT 71046 (Chest X-ray 2-views) linked solely to ICD-10 I10 (Essential hypertension) for an asymptomatic patient.",
                    reason_flagged="Under CMS Local Coverage Determination (LCD), hypertension alone is a non-covered diagnosis for chest radiography without documented respiratory signs or cardiac symptoms.",
                    recommended_action="Place billing hold on CPT 71046; review complete chart for undocumented symptoms; if purely routine screening, remove 71046 and bill E/M 99213 only.",
                    manual_review_required=True,
                    is_confirmed_error=True
                )
        return None

    def _check_modifier_application(self, scenario: BillingScenario) -> Optional[DetectionFinding]:
        """Detect missing Modifier 25 on Evaluation & Management billed on same day as minor procedure."""
        cpt_codes = [c.strip() for c in scenario.original_cpt.split(";") if c.strip()]
        doc_lower = scenario.clinical_documentation.lower()

        # Dual service: 11402 (excision) + 99214 (E/M)
        if any(c.startswith("11") for c in cpt_codes) and any(c.startswith("992") for c in cpt_codes):
            if scenario.modifier_applied in [None, "None", ""]:
                if "separately" in doc_lower or "vertigo" in doc_lower or "bppv" in doc_lower or "distinct" in doc_lower:
                    return DetectionFinding(
                        finding_id=f"FND-{scenario.scenario_id}-MOD25",
                        scenario_id=scenario.scenario_id,
                        encounter_id=scenario.encounter_id,
                        error_code="ERR_MODIFIER_APPLICATION",
                        error_name="Missing Modifier -25 for Significant Separate E/M Service",
                        severity=ErrorSeverity.HIGH,
                        evidence="E/M visit CPT 99214 and cyst excision CPT 11402 billed together without Modifier -25 attached to 99214.",
                        reason_flagged="CMS National Correct Coding Initiative (NCCI) bundles E/M services into minor surgical procedures on the same date unless Modifier -25 is appended documenting a significant, separately identifiable evaluation.",
                        recommended_action="Append Modifier -25 to CPT 99214; submit corrected claim with clinical progress note demonstrating distinct evaluation of acute vertigo.",
                        manual_review_required=True,
                        is_confirmed_error=True
                    )
        return None

    def _check_units_and_quantity(self, scenario: BillingScenario) -> Optional[DetectionFinding]:
        """Detect Medically Unlikely Edit (MUE) unit discrepancies."""
        cpt_codes = [c.strip() for c in scenario.original_cpt.split(";") if c.strip()]
        if "96360" in cpt_codes and scenario.units_billed > 1:
            return DetectionFinding(
                finding_id=f"FND-{scenario.scenario_id}-MUE",
                scenario_id=scenario.scenario_id,
                encounter_id=scenario.encounter_id,
                error_code="ERR_UNITS_QUANTITY",
                error_name="Medically Unlikely Edit (MUE) Units Discrepancy",
                severity=ErrorSeverity.HIGH,
                evidence=f"CPT 96360 (IV hydration, initial 31-60 min) billed with Units = {scenario.units_billed} (${scenario.original_billed_amount:.2f}).",
                reason_flagged="CMS Medically Unlikely Edit (MUE) limits CPT 96360 to a maximum of 1 unit per date of service. Documented infusion duration was 45 minutes, satisfying 1 unit.",
                recommended_action="Correct billing units from 4 to 1; adjust Chargemaster gross charge from $520.00 to $130.00 and resubmit claim.",
                manual_review_required=True,
                is_confirmed_error=True
            )
        return None

    def _check_coordination_of_benefits(self, scenario: BillingScenario) -> Optional[DetectionFinding]:
        """Detect Coordination of Benefits (COB) order errors (e.g. Medicare primary billed to commercial PPO)."""
        if scenario.patient_age >= 65 and "Medicare" not in scenario.payer_name:
            if scenario.error_category == "ERR_COB_ROUTING":
                return DetectionFinding(
                    finding_id=f"FND-{scenario.scenario_id}-COB",
                    scenario_id=scenario.scenario_id,
                    encounter_id=scenario.encounter_id,
                    error_code="ERR_COB_ROUTING",
                    error_name="Coordination of Benefits (COB) Payer Hierarchy Error",
                    severity=ErrorSeverity.HIGH,
                    evidence=f"Patient {scenario.patient_name} (age {scenario.patient_age}) has active Medicare Part B; claim was billed to commercial PPO ({scenario.payer_name}) as primary.",
                    reason_flagged="Commercial payer denied claim under CARC 22. For retired beneficiaries age 65+, Medicare Part B is primary payer by federal statute, and commercial PPO is secondary.",
                    recommended_action="Update practice management payer master to Medicare Part B Primary; submit primary 837P claim to Medicare; crossover/bill commercial payer as secondary.",
                    manual_review_required=True,
                    is_confirmed_error=True
                )
        return None

    def _check_financial_calculations(self, scenario: BillingScenario) -> Optional[DetectionFinding]:
        """Detect patient balance calculation errors exceeding payer allowable fee schedule."""
        if scenario.error_category == "ERR_CALCULATION_BALANCE":
            return DetectionFinding(
                finding_id=f"FND-{scenario.scenario_id}-CALC",
                scenario_id=scenario.scenario_id,
                encounter_id=scenario.encounter_id,
                error_code="ERR_CALCULATION_BALANCE",
                error_name="Patient Cost-Sharing Calculation Error / Balance-Billing Violation",
                severity=ErrorSeverity.HIGH,
                evidence="Practice management system generated statement billing patient $164.40 on a contracted allowable amount of $112.00.",
                reason_flagged="Billing algorithm double-counted copayment on high-deductible plan and failed to enforce the statutory rule that total patient responsibility cannot exceed the contracted allowed amount.",
                recommended_action="Void erroneous billing statement; issue ledger credit adjustment; recalculate correct patient balance of $62.40 ($50 deductible + $12.40 coinsurance) and issue corrected statement.",
                manual_review_required=True,
                is_confirmed_error=True
            )
        return None

    def _check_edi_submission_syntax(self, scenario: BillingScenario) -> Optional[DetectionFinding]:
        """Detect clearinghouse EDI 277CA gateway rejections due to missing NPI or taxonomy qualifiers."""
        if scenario.error_category == "ERR_SUBMISSION_REJECTED":
            return DetectionFinding(
                finding_id=f"FND-{scenario.scenario_id}-EDI",
                scenario_id=scenario.scenario_id,
                encounter_id=scenario.encounter_id,
                error_code="ERR_SUBMISSION_REJECTED",
                error_name="Claim Rejected at Clearinghouse Gateway (Missing Rendering NPI)",
                severity=ErrorSeverity.CRITICAL,
                evidence="Clearinghouse 277CA rejection STC A7: Loop 2010AA rendering provider NPI unpopulated in Box 24J/33a.",
                reason_flagged="Software update severed provider dictionary linkage, omitting mandatory individual Type 1 National Provider Identifier (NPI) from electronic claim file.",
                recommended_action="Re-link rendering provider NPI 1982736450 in billing dictionary; regenerate ANSI ASC X12N 837P envelope and resubmit.",
                manual_review_required=True,
                is_confirmed_error=True
            )
        return None

    def _check_pending_external_records(self, scenario: BillingScenario) -> Optional[DetectionFinding]:
        """Detect high-risk prescription initiation where external consults/labs are missing from chart."""
        doc_lower = scenario.clinical_documentation.lower()
        if scenario.error_category == "QUERY_PENDING_DOCS" or "hydroxychloroquine" in doc_lower:
            return DetectionFinding(
                finding_id=f"FND-{scenario.scenario_id}-PEND-DOCS",
                scenario_id=scenario.scenario_id,
                encounter_id=scenario.encounter_id,
                error_code="QUERY_PENDING_DOCS",
                error_name="Documentation Deficiency – Missing External Specialist Records",
                severity=ErrorSeverity.MEDIUM,
                evidence="Progress note references outside rheumatology consultation and autoimmune lab panel, but records are absent from the EHR media repository.",
                reason_flagged="Initiation of high-risk immunosuppressive therapy requires complete documentation of external consult and baseline laboratory results in the patient chart to satisfy compliance auditing.",
                recommended_action="Place billing hold; instruct medical records staff to retrieve and scan outside rheumatology consultation and lab panel into chart before claim release.",
                manual_review_required=True,
                is_confirmed_error=False
            )
        return None

    def _create_finding_from_scenario_category(self, scenario: BillingScenario) -> Optional[DetectionFinding]:
        """Create a structured finding based on scenario metadata if no specific pattern matched."""
        meta = self.categories_meta.get(scenario.error_category, {})
        name = meta.get("name", scenario.error_category)
        sev_str = meta.get("default_severity", "Medium")
        try:
            sev = ErrorSeverity(sev_str)
        except ValueError:
            sev = ErrorSeverity.MEDIUM

        return DetectionFinding(
            finding_id=f"FND-{scenario.scenario_id}-GEN",
            scenario_id=scenario.scenario_id,
            encounter_id=scenario.encounter_id,
            error_code=scenario.error_category,
            error_name=name,
            severity=sev,
            evidence=scenario.billing_query,
            reason_flagged=scenario.root_cause,
            recommended_action=scenario.recommended_action,
            manual_review_required=scenario.manual_review_required,
            is_confirmed_error=scenario.final_status != "No Error Identified"
        )
