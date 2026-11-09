"""Unit tests for report and artifact generation in Week 3."""

import os
import pytest
import docx
import pandas as pd
from week3.src.workflow import BillingResolutionWorkflow
from week3.src.report_generator import BillingResolutionReportGenerator
from week3.src.visualizer import generate_resolution_flowchart


@pytest.fixture(scope="module")
def run_simulation_once():
    wf = BillingResolutionWorkflow()
    return wf.run_simulation()


def test_flowchart_generation(tmp_path):
    output_png = str(tmp_path / "test_flowchart.png")
    generate_resolution_flowchart(output_path=output_png)
    assert os.path.exists(output_png)
    size = os.path.getsize(output_png)
    assert size > 100000, f"Flowchart size {size} is too small (expected >100KB)"


def test_csv_analysis_export(tmp_path, run_simulation_once):
    scenarios, findings, rcas, resolutions, controls, metrics = run_simulation_once
    wf = BillingResolutionWorkflow()
    output_csv = str(tmp_path / "test_analysis.csv")
    wf.export_analysis_csv(scenarios, resolutions, output_path=output_csv)

    assert os.path.exists(output_csv)
    df = pd.read_csv(output_csv)
    assert len(df) == 18
    assert "Scenario ID" in df.columns
    assert "Encounter ID" in df.columns
    assert "Original Billed Amount" in df.columns
    assert "Financial Variance" in df.columns
    assert "Resolution Status" in df.columns


def test_word_report_compilation_and_table_margins(tmp_path, run_simulation_once):
    scenarios, findings, rcas, resolutions, controls, metrics = run_simulation_once
    output_png = str(tmp_path / "temp_flowchart.png")
    generate_resolution_flowchart(output_path=output_png)

    output_docx = str(tmp_path / "Test_Case_Study_Report.docx")
    generator = BillingResolutionReportGenerator(
        scenarios=scenarios,
        findings=findings,
        rcas=rcas,
        resolutions=resolutions,
        controls=controls,
        metrics=metrics,
        flowchart_path=output_png
    )
    generator.generate_report(output_docx)

    assert os.path.exists(output_docx)
    doc = docx.Document(output_docx)

    # Paragraph and table volume checks
    assert len(doc.paragraphs) >= 80
    assert len(doc.tables) >= 7

    # Check title text includes student project branding
    assert "STUDENT PROJECT" in doc.paragraphs[1].text

    # Verify table column widths sum strictly to 6.50 inches (+/- 0.05)
    for idx, table in enumerate(doc.tables):
        col_widths = [cell.width.inches for cell in table.rows[0].cells]
        total_width = round(sum(col_widths), 2)
        assert abs(total_width - 6.50) < 0.05, f"Table {idx} total width {total_width} != 6.50 inches"

    # Verify all 18 scenarios are present in the document body
    full_text = "\n".join(p.text for p in doc.paragraphs)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                full_text += "\n" + cell.text

    for s in scenarios:
        assert s.scenario_id in full_text, f"Scenario {s.scenario_id} missing from report"
