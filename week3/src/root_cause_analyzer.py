"""Root cause analysis engine for Week 3 billing simulation."""

from typing import Dict, List, Optional, Any

from .models import (
    BillingScenario, DetectionFinding, RootCauseAnalysis, RootCauseCategory
)


class RootCauseAnalyzer:
    """Analyzes the operational, clinical, coding, and technical root causes

    behind detected billing errors and administrative queries.
    """

    def __init__(self):
        # Mapping from error category code to primary RootCauseCategory
        self.category_map: Dict[str, RootCauseCategory] = {
            "ERR_ICD_INCORRECT": RootCauseCategory.CODING_KNOWLEDGE_ERROR,
            "ERR_ICD_SPECIFICITY": RootCauseCategory.CLINICAL_DOC_DEFICIENCY,
            "ERR_CPT_INCORRECT": RootCauseCategory.INCORRECT_CODE_SELECTION,
            "ERR_DUPLICATE_BILLING": RootCauseCategory.DUPLICATE_SUBMISSION,
            "ERR_EM_UNSUPPORTED": RootCauseCategory.CODING_KNOWLEDGE_ERROR,
            "ERR_SIGNATURE_MISSING": RootCauseCategory.CLINICAL_DOC_DEFICIENCY,
            "ERR_DOCUMENTATION_MISSING": RootCauseCategory.CLINICAL_DOC_DEFICIENCY,
            "ERR_SUBSCRIBER_INFO": RootCauseCategory.REGISTRATION_ERROR,
            "ERR_DEMOGRAPHIC_TYPO": RootCauseCategory.REGISTRATION_ERROR,
            "ERR_AUTH_REFERRAL_MISSING": RootCauseCategory.AUTHORIZATION_FAILURE,
            "ERR_MEDICAL_NECESSITY": RootCauseCategory.CLINICAL_DOC_DEFICIENCY,
            "ERR_MODIFIER_APPLICATION": RootCauseCategory.MODIFIER_UNIT_ERROR,
            "ERR_UNITS_QUANTITY": RootCauseCategory.CHARGE_CAPTURE_ERROR,
            "ERR_COB_ROUTING": RootCauseCategory.ELIGIBILITY_FAILURE,
            "ERR_CALCULATION_BALANCE": RootCauseCategory.PAYMENT_POSTING_ERROR,
            "ERR_SUBMISSION_REJECTED": RootCauseCategory.SCRUBBER_FAILURE,
            "QUERY_NO_ERROR": RootCauseCategory.COMPLIANCE_AUDIT,
            "QUERY_PENDING_DOCS": RootCauseCategory.CLINICAL_DOC_DEFICIENCY
        }

        # Stage in the revenue cycle where the defect originated
        self.stage_map: Dict[str, str] = {
            "ERR_ICD_INCORRECT": "Mid-Revenue Cycle (Medical Coding)",
            "ERR_ICD_SPECIFICITY": "Mid-Revenue Cycle (Medical Coding & Chart Review)",
            "ERR_CPT_INCORRECT": "Mid-Revenue Cycle (Charge Entry & CPT Assignment)",
            "ERR_DUPLICATE_BILLING": "Mid-Revenue Cycle (Charge Capture Batch Synchronization)",
            "ERR_EM_UNSUPPORTED": "Mid-Revenue Cycle (Provider Charting & E/M Code Selection)",
            "ERR_SIGNATURE_MISSING": "Clinical Encounter (Physician Documentation Authentication)",
            "ERR_DOCUMENTATION_MISSING": "Clinical Encounter (Procedural Documentation & EHR Indexing)",
            "ERR_SUBSCRIBER_INFO": "Front-End Revenue Cycle (Patient Registration & Demographic Intake)",
            "ERR_DEMOGRAPHIC_TYPO": "Front-End Revenue Cycle (Demographic Data Entry)",
            "ERR_AUTH_REFERRAL_MISSING": "Front-End Revenue Cycle (Insurance Referral & Authorization Verification)",
            "ERR_MEDICAL_NECESSITY": "Clinical Order Entry (Provider Test Ordering vs LCD Guidelines)",
            "ERR_MODIFIER_APPLICATION": "Mid-Revenue Cycle (Coding & NCCI Bundling Review)",
            "ERR_UNITS_QUANTITY": "Charge Capture (Data Entry & Unit Conversion)",
            "ERR_COB_ROUTING": "Front-End Revenue Cycle (Eligibility & Payer Hierarchy Intake)",
            "ERR_CALCULATION_BALANCE": "Back-End Revenue Cycle (Payment Posting & Patient Invoicing)",
            "ERR_SUBMISSION_REJECTED": "Billing Clearinghouse (EDI 837P Generation & NPI Crosswalking)",
            "QUERY_NO_ERROR": "Internal Compliance Auditing (Pre-Bill Sampling Thresholds)",
            "QUERY_PENDING_DOCS": "Clinical Chart Management (External Document Scanning & Indexing)"
        }

    def analyze_root_cause(
        self,
        scenario: BillingScenario,
        findings: Optional[List[DetectionFinding]] = None
    ) -> RootCauseAnalysis:
        """Perform root cause analysis on a scenario and return structured RCA."""
        category_code = scenario.error_category
        primary_category = self.category_map.get(category_code, RootCauseCategory.WORKFLOW_TRAINING)
        operational_stage = self.stage_map.get(category_code, "Outpatient Revenue Cycle")

        # Determine secondary contributing factors
        secondary_factors: List[str] = []
        if primary_category in [RootCauseCategory.REGISTRATION_ERROR, RootCauseCategory.ELIGIBILITY_FAILURE]:
            secondary_factors.extend([
                "Front-desk staff intake training gap",
                "Absence of real-time electronic 270/271 eligibility verification at check-in",
                "Manual data entry without secondary field validation"
            ])
        elif primary_category in [RootCauseCategory.CLINICAL_DOC_DEFICIENCY]:
            secondary_factors.extend([
                "Physician time pressure and high patient volume",
                "EHR template design failing to mandate critical fields or signature locking",
                "Incomplete external document indexing workflows"
            ])
        elif primary_category in [RootCauseCategory.CODING_KNOWLEDGE_ERROR, RootCauseCategory.INCORRECT_CODE_SELECTION]:
            secondary_factors.extend([
                "Coder familiarity with FY 2024 ICD-10-CM / CPT 2024 guideline updates",
                "Reliance on EHR default drop-down pick-lists instead of full chart review",
                "Lack of automated cross-checks between acute vs chronic codes"
            ])
        elif primary_category in [RootCauseCategory.DUPLICATE_SUBMISSION, RootCauseCategory.CHARGE_CAPTURE_ERROR]:
            secondary_factors.extend([
                "Multiple users entering charges across EHR and practice management systems",
                "Batch interface synchronization glitch",
                "Absence of Medically Unlikely Edit (MUE) validation in pre-bill scrubber"
            ])
        elif primary_category == RootCauseCategory.AUTHORIZATION_FAILURE:
            secondary_factors.extend([
                "Decoupled scheduling and authorization workflows",
                "Specialist clinic lack of direct electronic access to PCP referral portals",
                "Absence of appointment scheduling hard-stops for unconfirmed referrals"
            ])
        elif primary_category == RootCauseCategory.PAYMENT_POSTING_ERROR:
            secondary_factors.extend([
                "Practice management billing algorithm calculation error",
                "Lack of double-entry ledger balance validation prior to statement printing",
                "Inadequate billing staff auditing of secondary patient invoices"
            ])
        elif primary_category == RootCauseCategory.SCRUBBER_FAILURE:
            secondary_factors.extend([
                "Recent practice management software dictionary update",
                "Lack of synthetic EDI 837P pre-transmission test batches",
                "Unmonitored clearinghouse gateway 277CA rejection queues"
            ])
        else:
            secondary_factors.append("Routine administrative sampling threshold without clinical context")

        # Determine financial risk
        if scenario.variance_amount < 0:
            fin_risk = f"Overcharge risk of ${abs(scenario.variance_amount):.2f}; potential payer audit recoupment or refund liability."
        elif scenario.variance_amount > 0:
            fin_risk = f"Undercharge revenue degradation of ${scenario.variance_amount:.2f} if not properly captured."
        elif scenario.original_billed_amount > 0 and scenario.final_status != "No Error Identified":
            fin_risk = f"Full cash flow freeze of ${scenario.original_billed_amount:.2f} due to claim rejection, denial, or audit hold."
        else:
            fin_risk = "Zero direct financial loss; informational compliance query with zero variance."

        # Evidence required
        evidence_list = [e.strip() for e in scenario.evidence_required.split(";") if e.strip()]
        if not evidence_list:
            evidence_list = [scenario.evidence_required]

        return RootCauseAnalysis(
            scenario_id=scenario.scenario_id,
            encounter_id=scenario.encounter_id,
            primary_category=primary_category,
            secondary_factors=secondary_factors,
            operational_stage=operational_stage,
            underlying_cause=scenario.root_cause,
            financial_risk=fin_risk,
            evidence_needed=evidence_list
        )
