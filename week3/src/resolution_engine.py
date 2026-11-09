"""Query resolution engine for Week 3 billing simulation."""

from typing import Dict, List, Optional, Any

from .models import (
    BillingScenario, DetectionFinding, QueryResolution, ResolutionStatus
)


class ResolutionEngine:
    """Executes a structured 9-stage resolution workflow for billing queries

    and discrepancies across outpatient patient encounters.
    """

    def __init__(self, resolution_rules: Optional[Dict[str, Any]] = None):
        self.resolution_rules = resolution_rules or {}

    def resolve_query(
        self,
        scenario: BillingScenario,
        findings: Optional[List[DetectionFinding]] = None
    ) -> QueryResolution:
        """Construct the 9-stage step-by-step resolution plan and outcome for a scenario."""
        cat_code = scenario.error_category
        proto = self.resolution_rules.get("resolution_protocols", {}).get(cat_code, {})

        # 1. Query Identification
        query_id = f"QRY-{scenario.scenario_id}-{cat_code[-6:]}"

        # 2. Resolution Steps (9-stage workflow)
        steps = proto.get("steps", [
            f"1. Query Identification: Log inquiry '{scenario.billing_query}' under ticket {query_id}.",
            f"2. Source Record Review: Inspect patient demographic intake, appointment record, and encounter {scenario.encounter_id}.",
            f"3. Supporting Documentation Verification: Review progress note narrative: '{scenario.clinical_documentation[:90]}...'.",
            f"4. Applicable Rule Evaluation: Cross-reference FY 2024 ICD-10-CM / CPT 2024 / CMS guidelines for {scenario.original_cpt}.",
            f"5. Corrective Action Plan: {scenario.recommended_action}.",
            "6. Provider/Payer Communication: Dispatch formal communication or query memo to responsible stakeholder.",
            "7. Claim Adjustment / Resubmission: Generate replacement 837P claim, void duplicate line, or release billing hold.",
            "8. Final Validation Check: Execute pre-submission claim scrubber and verify zero outstanding fatal edits.",
            f"9. Resolution Outcome: Establish case status as '{scenario.final_status.value}'."
        ])

        # 3. Required Evidence
        evidence = proto.get("required_evidence", [
            "Physician progress note",
            "Billing journal ledger",
            "Payer ERA 835 / 277CA notice"
        ])

        # 4. Required Provider or Payer Communication
        comm = self._determine_communication(scenario)

        # 5. Claim Correction or Resubmission Step
        claim_action = self._determine_claim_action(scenario)

        # 6. Final Validation Checks
        val_checks = self._determine_validation_checks(scenario)

        # 7. Financial Reconciliation Summary
        fin_recon = self._determine_financial_reconciliation(scenario)

        return QueryResolution(
            scenario_id=scenario.scenario_id,
            encounter_id=scenario.encounter_id,
            query_id=query_id,
            resolution_steps=steps,
            required_evidence=evidence,
            provider_payer_communication=comm,
            claim_action=claim_action,
            validation_checks=val_checks,
            final_status=scenario.final_status,
            financial_reconciliation=fin_recon
        )

    def _determine_communication(self, scenario: BillingScenario) -> str:
        """Determine specific stakeholder communication without fabricating approval."""
        cat = scenario.error_category
        if cat == "ERR_SIGNATURE_MISSING":
            return "Urgent Electronic Task dispatched to attending clinician in EHR: 'Progress note unsigned. Please review, authenticate, and apply electronic signature.'"
        elif cat == "ERR_DOCUMENTATION_MISSING":
            return "Formal Written Provider Query submitted to Dr. Attending: 'Please provide operative/procedure note for billed CPT 11102, or confirm procedure was not executed.'"
        elif cat == "ERR_AUTH_REFERRAL_MISSING":
            return "Referral Coordination Memo transmitted to Primary Care Physician clinic requesting retroactive specialist referral documentation for encounter."
        elif cat == "ERR_SUBSCRIBER_INFO":
            return "Patient/Guarantor Phone Outreach logged: Contact parent to obtain primary subscriber ID and policy number for dependent minor."
        elif cat == "ERR_DEMOGRAPHIC_TYPO":
            return "Patient Intake Communication: Verify government-issued photo ID to confirm legal date of birth and update Master Patient Index."
        elif cat == "ERR_COB_ROUTING":
            return "Patient Benefit Advisory dispatched: Request completed Medicare Secondary Payer (MSP) questionnaire to verify primary vs secondary coverage order."
        elif cat == "ERR_CALCULATION_BALANCE":
            return "Patient Accounting Notice & Apology Letter: Inform patient that statement was corrected to $62.40; $102.00 ledger credit applied."
        elif cat == "ERR_EM_UNSUPPORTED":
            return "Coding Quality Feedback Notification sent to clinician explaining 2021/2023 AMA MDM thresholds and downcoding to 99213."
        elif cat == "ERR_MEDICAL_NECESSITY":
            return "Compliance Audit Hold Notice to Ordering Physician: Routine chest X-ray lacks documented covered indication under Medicare LCD."
        elif cat == "QUERY_PENDING_DOCS":
            return "Medical Records Request to External Hospital: Request copy of outside rheumatology consult note and baseline autoimmune laboratory panel."
        elif cat == "QUERY_NO_ERROR":
            return "Audit Clearance Notice to Billing Dept: Independent chart audit confirms High MDM and 50 min time strictly support CPT 99215. Query closed."
        else:
            return "Internal Electronic Billing Memo: Coding correction ticket routed to billing specialist for electronic claim resubmission."

    def _determine_claim_action(self, scenario: BillingScenario) -> str:
        """Determine claim transmission or ledger action."""
        status = scenario.final_status
        if status == ResolutionStatus.RESOLVED_CORRECTED:
            return f"Submit ANSI ASC X12N 837P Replacement Claim (Claim Frequency Code 7) with corrected codes ({scenario.corrected_cpt or scenario.original_cpt})."
        elif status == ResolutionStatus.RESOLVED_DOCS:
            return "Release billing hold in practice management system and dispatch initial clean EDI 837P claim to clearinghouse."
        elif status == ResolutionStatus.PENDING_PROVIDER:
            return "Maintain strict billing hold on CPT 11102; do not transmit claim pending provider response to formal clinical documentation query."
        elif status == ResolutionStatus.PENDING_DOCS:
            return "Maintain billing hold in billing workqueue pending receipt and EHR indexing of external medical records."
        elif status == ResolutionStatus.ESCALATED:
            return "Hold claim from billing release; escalate chart to Physician Compliance Officer for final medical necessity determination."
        elif status == ResolutionStatus.NO_ERROR:
            return "Release original claim with original billing parameters (CPT 99215, $395.00) for standard payer submission."
        else:
            return "Review claim in billing workqueue for manual adjudication."

    def _determine_validation_checks(self, scenario: BillingScenario) -> List[str]:
        """Generate verification checks executed before final query closure."""
        return [
            "1. Confirm patient demographic identifiers match Master Patient Index (MPI).",
            "2. Verify ICD-10-CM codes exist in FY 2024 educational reference catalog.",
            "3. Verify CPT codes and modifiers align with CPT 2024 guidelines.",
            "4. Execute automated pre-submission claim scrubber (zero fatal edits).",
            "5. Validate that gross billed amount equals Chargemaster fee schedule rate.",
            "6. Reconcile ledger accounts to guarantee double-entry balance."
        ]

    def _determine_financial_reconciliation(self, scenario: BillingScenario) -> str:
        """Summarize financial impact and ledger reconciliation."""
        orig = scenario.original_billed_amount
        corr = scenario.corrected_billed_amount if scenario.corrected_billed_amount is not None else orig
        var = scenario.variance_amount

        if var < 0:
            return f"Original Billed: ${orig:.2f} | Corrected Billed: ${corr:.2f} | Net Adjustment: -${abs(var):.2f} (Overbilling write-off / correction)."
        elif var > 0:
            return f"Original Billed: ${orig:.2f} | Corrected Billed: ${corr:.2f} | Net Adjustment: +${var:.2f} (Recovered uncaptured revenue)."
        else:
            return f"Original Billed: ${orig:.2f} | Corrected Billed: ${corr:.2f} | Net Adjustment: $0.00 (Zero financial ledger variance)."
