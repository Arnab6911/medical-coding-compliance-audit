"""Patient Invoice and Billing Statement Generator for Week 2.

Generates itemized patient billing statements after insurance adjudication:
- Displays total gross charges, insurance write-offs, payer payments, and patient responsibility.
- Transparently itemizes copay, deductible, and coinsurance amounts.
- Exports structured text invoices to week2/reports/invoices/.
"""

import os
from datetime import datetime, timedelta
from typing import List, Optional

from .models import Claim, PatientInvoice, InvoiceLineItem, BillingStage


class InvoiceGenerator:
    """Creates patient invoices and exports billing statements."""

    def __init__(self, output_dir: Optional[str] = None):
        if output_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            output_dir = os.path.join(base_dir, "reports", "invoices")

        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_invoice(self, claim: Claim) -> PatientInvoice:
        """Create PatientInvoice instance from adjudicated claim."""
        inv_number = f"INV-{claim.encounter_id[-4:]}"
        today = datetime.now()
        due = today + timedelta(days=30)

        line_items: List[InvoiceLineItem] = []
        for line in claim.lines:
            item = InvoiceLineItem(
                description=f"{line.cpt_code} - {line.cpt_description}",
                charge=line.gross_charge,
                insurance_paid=line.insurance_paid,
                adjustment=line.contractual_adjustment,
                patient_due=line.patient_responsibility
            )
            line_items.append(item)

        status = "Paid in Full ($0 Balance)" if claim.total_patient_responsibility == 0.0 else "Balance Due"

        invoice = PatientInvoice(
            invoice_number=inv_number,
            invoice_date=today.strftime("%B %d, %Y"),
            due_date=due.strftime("%B %d, %Y"),
            patient_id=claim.patient.patient_id,
            patient_name=claim.patient.name,
            patient_address=claim.patient.address,
            encounter_id=claim.encounter_id,
            date_of_service=claim.date_of_service,
            provider_name="Metropolitan Outpatient Medical Group, P.C.",
            items=line_items,
            total_charges=claim.total_gross_charge,
            insurance_payments=claim.total_insurance_paid,
            contractual_adjustments=claim.total_contractual_adjustment,
            patient_copay=claim.total_copay,
            patient_deductible=claim.total_deductible,
            patient_coinsurance=claim.total_coinsurance,
            total_balance_due=claim.total_patient_responsibility,
            status=status,
            notes=f"Processed under {claim.policy.payer_name} ({claim.policy.plan_name}). Claim ID: {claim.claim_id}."
        )

        claim.stage = BillingStage.INVOICED
        return invoice

    def export_invoice_text(self, invoice: PatientInvoice, filename: Optional[str] = None) -> str:
        """Render patient invoice as formatted text file and save to output directory."""
        if filename is None:
            filename = f"{invoice.invoice_number}.txt"

        filepath = os.path.join(self.output_dir, filename)

        lines = [
            "=" * 78,
            "METROPOLITAN OUTPATIENT MEDICAL GROUP, P.C.",
            "100 Medical Center Blvd, Suite 200 | Phone: (555) 019-2830",
            "=" * 78,
            "PATIENT BILLING STATEMENT / SUMMARY INVOICE",
            "-" * 78,
            f"Statement Number : {invoice.invoice_number}",
            f"Statement Date   : {invoice.invoice_date}",
            f"Payment Due Date : {invoice.due_date}",
            f"Account Status   : {invoice.status.upper()}",
            "-" * 78,
            "PATIENT INFORMATION:",
            f"  Patient Name   : {invoice.patient_name} (ID: {invoice.patient_id})",
            f"  Billing Address: {invoice.patient_address}",
            f"  Encounter ID   : {invoice.encounter_id} | Date of Service: {invoice.date_of_service}",
            "-" * 78,
            "ITEMIZED CHARGES & INSURANCE ADJUDICATION:",
            f"{'Description':<40} {'Billed':>9} {'Adj/Disc':>10} {'Ins Paid':>10} {'Pt Due':>8}",
            "-" * 78
        ]

        for item in invoice.items:
            desc = item.description[:38]
            lines.append(
                f"{desc:<40} ${item.charge:>8.2f} ${item.adjustment:>9.2f} ${item.insurance_paid:>9.2f} ${item.patient_due:>7.2f}"
            )

        lines.extend([
            "-" * 78,
            "ACCOUNT SUMMARY & BALANCE BREAKDOWN:",
            f"  Total Billed Charges            : ${invoice.total_charges:>9.2f}",
            f"  Less: Insurance Write-Offs / Adj: ${invoice.contractual_adjustments:>9.2f}",
            f"  Less: Insurance Payments Received: ${invoice.insurance_payments:>9.2f}",
            f"  --------------------------------------------------",
            f"  Patient Copayment Required      : ${invoice.patient_copay:>9.2f}",
            f"  Patient Deductible Applied      : ${invoice.patient_deductible:>9.2f}",
            f"  Patient Coinsurance Required    : ${invoice.patient_coinsurance:>9.2f}",
            f"  ==================================================",
            f"  TOTAL BALANCE DUE FROM PATIENT  : ${invoice.total_balance_due:>9.2f}",
            "=" * 78,
            "PAYMENT NOTICE & REGULATORY DISCLAIMER:",
            "• Payment is due within 30 days of statement date via portal, phone, or mail.",
            "• Educational Notice: This document is a simulated educational invoice created for",
            "  internship workflow demonstration. Does not reflect real patient debt or actual bills.",
            "=" * 78
        ])

        content = "\n".join(lines)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return filepath
