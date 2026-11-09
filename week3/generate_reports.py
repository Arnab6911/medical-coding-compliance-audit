"""Standalone report and deliverables generation script for Week 3.

Executes the complete billing query resolution workflow, renders the 300 DPI
workflow flowchart, exports the CSV audit dataset, compiles the formal
20-section Microsoft Word case study report, and verifies document integrity.

Usage:
    python week3/generate_reports.py
"""

import os
import sys
import docx

# Ensure repository root is on sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

WEEK3_ROOT = os.path.abspath(os.path.dirname(__file__))
if WEEK3_ROOT not in sys.path:
    sys.path.insert(0, WEEK3_ROOT)

from week3.src.workflow import BillingResolutionWorkflow
from week3.src.visualizer import generate_resolution_flowchart
from week3.src.report_generator import BillingResolutionReportGenerator


def main() -> None:
    print("=" * 75)
    print("WEEK 3: BILLING QUERY RESOLUTION & ERROR ANALYSIS - REPORT GENERATOR")
    print("=" * 75)

    reports_dir = os.path.join(WEEK3_ROOT, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    # 1. Execute 6-Phase Resolution Workflow
    print("\n[1/5] Ingesting scenarios and executing resolution workflow...")
    workflow = BillingResolutionWorkflow(data_dir=os.path.join(WEEK3_ROOT, "data"))
    scenarios, findings, rcas, resolutions, controls, metrics = workflow.run_simulation()

    print(f"      -> Simulation Completed Successfully:")
    print(f"         - Total Scenarios Evaluated  : {metrics.total_scenarios}")
    print(f"         - Errors Identified / Flagged: {metrics.errors_identified_count}")
    print(f"         - Compliant ('No Error')     : {metrics.no_error_identified_count}")
    print(f"         - Claims Resolved & Corrected: {metrics.resolved_claims_count}")
    print(f"         - Pending Provider / Docs    : {metrics.pending_query_count}")
    print(f"         - Escalated for Compliance   : {metrics.escalated_review_count}")
    print(f"         - Initial Gross Billed       : ${metrics.total_original_gross_billed:,.2f}")
    print(f"         - Corrected Gross Billed     : ${metrics.total_corrected_gross_billed:,.2f}")
    print(f"         - Net Financial Variance     : ${metrics.total_financial_variance:,.2f}")

    # 2. Render 300 DPI Workflow Flowchart
    flowchart_path = os.path.join(reports_dir, "resolution_workflow.png")
    print(f"\n[2/5] Generating 300 DPI resolution workflow diagram: {flowchart_path}")
    generate_resolution_flowchart(output_path=flowchart_path)
    file_size_fc = os.path.getsize(flowchart_path)
    print(f"      -> Flowchart saved ({file_size_fc:,} bytes).")

    # 3. Export CSV Audit Dataset
    csv_path = os.path.join(reports_dir, "billing_error_analysis.csv")
    print(f"\n[3/5] Exporting error resolution dataset to CSV: {csv_path}")
    workflow.export_analysis_csv(scenarios, resolutions, output_path=csv_path)
    file_size_csv = os.path.getsize(csv_path)
    print(f"      -> CSV findings exported ({file_size_csv:,} bytes).")

    # 4. Compile 20-Section Word Report
    docx_path = os.path.join(reports_dir, "Week_3_Billing_Query_Resolution_Report.docx")
    print(f"\n[4/5] Assembling 20-Section Word Case Study Report: {docx_path}")
    generator = BillingResolutionReportGenerator(
        scenarios=scenarios,
        findings=findings,
        rcas=rcas,
        resolutions=resolutions,
        controls=controls,
        metrics=metrics,
        flowchart_path=flowchart_path
    )
    generator.generate_report(docx_path)
    file_size_docx = os.path.getsize(docx_path)
    print(f"      -> Word report generated successfully ({file_size_docx:,} bytes).")

    # 5. Programmatic Verification of Generated Deliverable
    print(f"\n[5/5] Performing independent quality verification on Word document...")
    doc = docx.Document(docx_path)
    p_count = len(doc.paragraphs)
    t_count = len(doc.tables)
    title_text = doc.paragraphs[1].text

    print(f"      [OK] Document opened cleanly via python-docx.")
    print(f"      [OK] Paragraph count : {p_count}")
    print(f"      [OK] Table count     : {t_count}")
    print(f"      [OK] Title Verified  : {title_text}")

    # Verify table column widths sum to 6.50 inches
    for t_idx, table in enumerate(doc.tables):
        col_widths = [cell.width.inches for cell in table.rows[0].cells]
        total_w = round(sum(col_widths), 2)
        assert abs(total_w - 6.50) < 0.05, f"Table {t_idx} width sum {total_w} != 6.50 inches"
    print(f"      [OK] All {t_count} tables validated to strictly fit 6.50\" page margins.")

    # Verify all scenarios are present in document text
    full_text = "\n".join([p.text for p in doc.paragraphs])
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                full_text += "\n" + cell.text

    for s in scenarios:
        assert s.scenario_id in full_text, f"Scenario {s.scenario_id} missing from Word report text"
    print(f"      [OK] All {len(scenarios)} scenarios verified present in report body.")

    print("\n" + "=" * 75)
    print("WEEK 3 SIMULATION AND REPORT GENERATION COMPLETE!")
    print("=" * 75)


if __name__ == "__main__":
    main()
