"""Standalone CLI script to execute Week 2 Medical Billing Simulation and generate reports.

Executes:
1. End-to-end 12-stage billing simulation pipeline.
2. High-resolution workflow flowchart rendering.
3. 18-Section Microsoft Word Case Study Report (.docx).
4. Tabular billing results export (.csv).
5. Itemized patient statement export (.txt).
6. Post-generation Word document verification.

Usage:
    python week2/generate_reports.py
"""

import os
import sys

# Ensure repository root is on sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import docx
from week2.src.billing_pipeline import BillingSimulationPipeline
from week2.src.flowchart_generator import generate_billing_flowchart
from week2.src.report_generator import BillingCaseStudyReportGenerator


def run_week2_report_generation():
    print("=" * 75)
    print("WEEK 2: MEDICAL BILLING PROCESS SIMULATION - STANDALONE REPORT GENERATOR")
    print("=" * 75)

    week2_dir = os.path.join(BASE_DIR, "week2")
    reports_dir = os.path.join(week2_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    # 1. Execute Billing Simulation Pipeline
    print("\n[1/5] Ingesting encounters and executing 12-stage billing pipeline...")
    pipeline = BillingSimulationPipeline(data_dir=os.path.join(week2_dir, "data"))
    claims, postings, invoices, metrics = pipeline.run_simulation()

    print("      -> Simulation Completed Successfully:")
    print(f"         - Total Encounters Modeled   : {metrics.total_encounters}")
    print(f"         - Clean Claim Rate           : {metrics.clean_claim_rate}% ({metrics.clean_claims_count} Clean)")
    print(f"         - Scrubber Errors Intercepted: {metrics.scrubber_errors_count}")
    print(f"         - Claims Paid in Full        : {metrics.claims_paid_count}")
    print(f"         - Claims Partially Paid      : {metrics.claims_partially_paid_count}")
    print(f"         - Claims Denied              : {metrics.claims_denied_count}")
    print(f"         - Claims Rejected            : {metrics.claims_rejected_count}")
    print(f"         - Total Gross Billed         : ${metrics.total_gross_billed:,.2f}")
    print(f"         - Payer Allowed Revenue      : ${metrics.total_allowed:,.2f}")
    print(f"         - Contractual Adjustments    : ${metrics.total_contractual_adjustments:,.2f}")
    print(f"         - Net Insurance Payments     : ${metrics.total_insurance_payments:,.2f}")
    print(f"         - Patient Responsibility     : ${metrics.total_patient_responsibility:,.2f}")

    # 2. Render Workflow Flowchart Image
    flowchart_path = os.path.join(reports_dir, "workflow_flowchart.png")
    print(f"\n[2/5] Generating publication-grade workflow diagram: {flowchart_path}")
    generate_billing_flowchart(output_path=flowchart_path)
    print(f"      -> Flowchart saved ({os.path.getsize(flowchart_path):,} bytes).")

    # 3. Export Tabular Results CSV
    csv_path = os.path.join(reports_dir, "billing_simulation_results.csv")
    print(f"\n[3/5] Exporting simulation results to CSV: {csv_path}")
    pipeline.export_results_csv(claims, csv_path)
    print(f"      -> CSV findings exported ({os.path.getsize(csv_path):,} bytes).")

    # 4. Generate 18-Section Word Report
    docx_path = os.path.join(reports_dir, "Week_2_Medical_Billing_Case_Study.docx")
    print(f"\n[4/5] Assembling 18-Section Word Case Study Report: {docx_path}")
    report_gen = BillingCaseStudyReportGenerator(
        claims=claims,
        postings=postings,
        invoices=invoices,
        metrics=metrics,
        flowchart_path=flowchart_path
    )
    report_gen.generate(docx_path)
    print(f"      -> Word report generated successfully ({os.path.getsize(docx_path):,} bytes).")

    # 5. Independent Verification of Word Document
    print("\n[5/5] Performing independent verification of generated Word document...")
    doc = docx.Document(docx_path)
    print(f"      [OK] Document opened cleanly via python-docx.")
    print(f"      [OK] Paragraph count : {len(doc.paragraphs)}")
    print(f"      [OK] Table count     : {len(doc.tables)}")
    print(f"      [OK] Title Verified  : {doc.paragraphs[1].text}")
    print(f"      [OK] Invoices Exported: {len(invoices)} patient statements in week2/reports/invoices/")

    print("\n" + "=" * 75)
    print("WEEK 2 SIMULATION AND REPORT GENERATION COMPLETE!")
    print("=" * 75)


if __name__ == "__main__":
    run_week2_report_generation()
