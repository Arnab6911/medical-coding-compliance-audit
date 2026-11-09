"""
Standalone Report & Asset Generation Script for Week 4
Usage:
    python week4/generate_reports.py

Executes:
1. Reference dataset verification
2. 300 DPI diagram generation (architecture, workflow, risk matrix)
3. 21-section Word report compilation
4. Automated programmatic inspection and integrity verification
"""

import sys
from pathlib import Path
from datetime import datetime
import docx

# Ensure repository root is in sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from week4.src.workflow import IntegrationWorkflow

def verify_report_integrity(docx_path: Path):
    """Programmatically inspects the generated Word document to verify sections, tables, and images."""
    print(f"\nVerifying Report Integrity: {docx_path}")
    if not docx_path.exists():
        raise FileNotFoundError(f"Generated report not found: {docx_path}")

    doc = docx.Document(str(docx_path))
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    
    # Expected 21 sections
    expected_sections = [
        "MEDICAL CODING & BILLING INTERNSHIP",
        "2. Executive Summary",
        "3. Introduction",
        "4. Project Objectives",
        "5. Fictional Healthcare Practice Profile",
        "6. Software Research and Comparison",
        "7. Software Selection Framework",
        "8. Proposed System Architecture",
        "9. Integration Strategy",
        "10. Data Migration Plan",
        "11. Real-Time Coding and Billing Validation",
        "12. Security, Privacy and Compliance",
        "13. Best Practices Guide",
        "14. Coding Update Governance",
        "15. Staff Training Program",
        "16. Risk Assessment and Mitigation",
        "17. Implementation Timeline",
        "18. KPI and Success Measurement",
        "19. Challenges and Lessons Learned",
        "20. Conclusion",
        "21. References"
    ]

    found_sections = []
    missing_sections = []

    full_text = "\n".join(paragraphs)
    for sec in expected_sections:
        if sec in full_text:
            found_sections.append(sec)
        else:
            missing_sections.append(sec)

    table_count = len(doc.tables)
    inline_shapes_count = 0
    for p in doc.paragraphs:
        if "graphicData" in p._p.xml:
            inline_shapes_count += 1

    print(f"  • Document Paragraphs: {len(paragraphs)}")
    print(f"  • Tables Found: {table_count}")
    print(f"  • Embedded Image Figures: {inline_shapes_count}")
    print(f"  • Verified Sections: {len(found_sections)} of {len(expected_sections)}")

    if missing_sections:
        print(f"  [WARNING] Missing sections: {missing_sections}")
    else:
        print("  [SUCCESS] All 21 required sections verified present in Word document.")

    # Check table column widths
    for t_idx, tbl in enumerate(doc.tables):
        for r_idx, row in enumerate(tbl.rows[:2]):  # sample first 2 rows
            col_widths_sum = sum(c.width for c in row.cells)
            width_in_inches = col_widths_sum / 914400.0  # 1 inch = 914400 dxa/emu
            if abs(width_in_inches - 6.50) > 0.15:
                print(f"  [MARGIN NOTICE] Table {t_idx+1} row {r_idx+1} width is {width_in_inches:.2f} inches (Target: 6.50 in)")

    print("Document structure verification complete.\n")

def main():
    print("=" * 70)
    print("WEEK 4 REPORT GENERATOR – STANDALONE EXECUTION")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    workflow = IntegrationWorkflow()
    results = workflow.run_simulation(compile_word_report=True)

    report_path = Path(results["report_path"])
    verify_report_integrity(report_path)

    print("=" * 70)
    print("SIMULATION & ASSET GENERATION SUMMARY")
    print(f"  • Practice: {results['practice_name']}")
    print(f"  • Recommended Vendor: {results['evaluation']['recommended_vendor']} (Score: {results['evaluation']['recommended_score']:.2f}/10.0)")
    print(f"  • Data Migration: {results['migration']['total_records']} records, Net Variance: ${results['migration']['net_variance']:.2f}")
    print(f"  • Validation Rules: {results['validation_rules']['total_rules']} ({results['validation_rules']['hard_stops']} Hard-Stops, {results['validation_rules']['warnings']} Warnings)")
    print(f"  • Risks Evaluated: {results['risk_assessment']['total_risks']} (Avg Score: {results['risk_assessment']['average_risk_score']})")
    print(f"  • Training Modules: {results['training']['total_modules']} ({results['training']['total_hours']:.1f} hours, {results['training']['total_questions']} questions)")
    print(f"  • Report Location: {report_path.resolve()}")
    print("=" * 70)

if __name__ == "__main__":
    main()
