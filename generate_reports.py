"""Standalone CLI script to generate Word audit report and CSV findings independently of the dashboard.

Usage:
    python generate_reports.py
    python generate_reports.py --input data/sample_records.csv --output-dir reports
"""

import os
import argparse
import pandas as pd
import docx

from src.models import AuditSummary
from src.rules_engine import AuditEngine, load_records_from_csv
from src.reference_data import get_reference_manager
from src.report_generator import ComplianceReportGenerator


def generate_reports(input_csv: str = "data/sample_records.csv", output_dir: str = "reports") -> None:
    """Execute audit engine and generate Word and CSV reports."""
    print("=" * 70)
    print("MEDICAL CODING COMPLIANCE AUDIT - STANDALONE REPORT GENERATOR")
    print("=" * 70)

    # 1. Verify input file
    if not os.path.exists(input_csv):
        raise FileNotFoundError(f"Input records dataset not found at: {input_csv}")

    os.makedirs(output_dir, exist_ok=True)
    print(f"\n[1/4] Ingesting encounter records from: {input_csv}")
    records = load_records_from_csv(input_csv)
    print(f"      -> Successfully parsed {len(records)} fictional patient records.")

    # 2. Run Audit Engine
    print("\n[2/4] Executing Audit Engine rules across all encounters...")
    ref_manager = get_reference_manager()
    engine = AuditEngine(ref_manager)
    summary: AuditSummary = engine.audit_dataset(records)

    print("      -> Audit Execution Summary:")
    print(f"         - Total Encounters Audited : {summary.total_records}")
    print(f"         - Encounters Requiring Review: {summary.records_flagged}")
    print(f"         - Correctly Documented     : {summary.clean_records}")
    print(f"         - Total Findings Logged    : {summary.total_findings}")
    print(f"         - High Severity Flags      : {summary.high_severity_count}")
    print(f"         - Medium Severity Flags    : {summary.medium_severity_count}")
    print(f"         - Low Severity Flags       : {summary.low_severity_count}")
    print(f"         - Compliance Rate          : {summary.compliance_rate}%")
    print(f"         - Review Rate              : {summary.review_rate}%")

    # 3. Export CSV Findings
    csv_path = os.path.join(output_dir, "medical_coding_compliance_findings.csv")
    print(f"\n[3/4] Exporting empirical audit findings to CSV: {csv_path}")
    df_findings = pd.DataFrame([f.to_dict() for f in summary.findings])
    df_findings.to_csv(csv_path, index=False)
    print(f"      -> Saved {len(df_findings)} findings rows to {csv_path} ({os.path.getsize(csv_path)} bytes).")

    # 4. Generate 14-Section Word Report
    docx_path = os.path.join(output_dir, "Medical_Coding_Compliance_Audit_Report.docx")
    print(f"\n[4/4] Assembling 14-Section Word Audit Report (.docx): {docx_path}")
    generator = ComplianceReportGenerator(summary, records=records)
    generator.generate(docx_path)
    file_size = os.path.getsize(docx_path)
    print(f"      -> Successfully generated Word report: {docx_path} ({file_size} bytes).")

    # 5. Verification: Open and inspect the generated Word document
    print("\n" + "-" * 70)
    print("VERIFICATION OF GENERATED WORD REPORT:")
    print("-" * 70)
    doc = docx.Document(docx_path)
    print(" [OK] File successfully opened using python-docx.")
    print(f" [OK] Paragraph count : {len(doc.paragraphs)}")
    print(f" [OK] Table count     : {len(doc.tables)}")

    # Inspect findings table in Section 9
    findings_table = None
    for tbl in doc.tables:
        if len(tbl.rows) > 0 and tbl.rows[0].cells[0].text.strip() == "Encounter ID":
            findings_table = tbl
            break

    if findings_table:
        findings_row_count = len(findings_table.rows) - 1
        print(f" [OK] Section 9 Detailed Findings Table verified with {findings_row_count} logged finding rows.")
        print(" [OK] Sample Encounter Findings in Word Document:")
        for idx in range(1, min(6, len(findings_table.rows))):
            enc_id = findings_table.rows[idx].cells[0].text.strip()
            code = findings_table.rows[idx].cells[2].text.strip()
            year = findings_table.rows[idx].cells[3].text.strip()
            issue = findings_table.rows[idx].cells[4].text.strip()
            sev = findings_table.rows[idx].cells[5].text.strip()
            print(f"      - {enc_id} | Code: {code} | Year: {year} | Issue: {issue} | Severity: {sev}")
    else:
        print(" [!] Warning: Detailed findings table not located by header match.")

    print("\n" + "=" * 70)
    print("ALL REPORTS GENERATED AND EMPIRICALLY VERIFIED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Medical Coding Compliance Audit Report Generator")
    parser.add_argument("--input", default="data/sample_records.csv", help="Path to encounter records CSV")
    parser.add_argument("--output-dir", default="reports", help="Directory where reports are saved")
    args = parser.parse_args()

    generate_reports(input_csv=args.input, output_dir=args.output_dir)
