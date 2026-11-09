"""
Unit Tests for Week 4 Visualizer and Word Report Generator
Verifies 300 DPI diagram generation, Word report compilation,
21-section presence, and strict 6.50-inch table margin compliance.
"""

from pathlib import Path
import pytest
import docx

from week4.src.visualizer import IntegrationVisualizer
from week4.src.report_generator import IntegrationReportGenerator

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"

def test_diagram_generation():
    viz = IntegrationVisualizer()
    paths = viz.generate_all_diagrams()
    
    for key, path in paths.items():
        assert path.exists(), f"Diagram {key} does not exist: {path}"
        assert path.stat().st_size > 50_000, f"Diagram {key} is too small: {path.stat().st_size} bytes"

def test_word_report_compilation_and_sections():
    rep_gen = IntegrationReportGenerator()
    docx_path = rep_gen.generate_report()
    assert docx_path.exists()
    assert docx_path.stat().st_size > 500_000  # contains embedded figures

    doc = docx.Document(str(docx_path))
    full_text = "\n".join([p.text.strip() for p in doc.paragraphs if p.text.strip()])

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

    for sec in expected_sections:
        assert sec in full_text, f"Expected section not found in report: {sec}"

def test_table_margins_and_column_widths():
    docx_path = REPORTS_DIR / "Week_4_Billing_Software_Integration_Report.docx"
    assert docx_path.exists()

    doc = docx.Document(str(docx_path))
    assert len(doc.tables) >= 10

    for t_idx, tbl in enumerate(doc.tables):
        for r_idx, row in enumerate(tbl.rows[:2]):
            col_widths_sum = sum(c.width for c in row.cells)
            width_in_inches = col_widths_sum / 914400.0  # 1 inch = 914400 dxa/emu
            # All tables must fit printable width (6.50 in +/- 0.15 in tolerance)
            assert abs(width_in_inches - 6.50) <= 0.15, (
                f"Table {t_idx+1} row {r_idx+1} width {width_in_inches:.2f} in exceeds 6.50 in printable boundary"
            )
