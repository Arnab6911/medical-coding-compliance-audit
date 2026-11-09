"""High-resolution publication flowchart and visual analytics generator for Week 3."""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import Dict, List, Optional, Any

from .models import SimulationBatchMetrics


def generate_resolution_flowchart(output_path: Optional[str] = None) -> str:
    """Generate a 300 DPI professional medical billing query resolution flowchart.

    Diagram represents:
    Claim/Query Received -> Identify Error Category -> Retrieve Records ->
    Verify Documentation -> Review Coding Rules -> Decision: Is Error Confirmed? ->
    YES: Root Cause -> Prepare Correction -> Provider Query if Needed ->
         Correct Claim -> Validation & Financial Checks -> Resubmit -> Verify -> Record Outcome
    NO:  Document No Error -> Close Query
    Escalation & Pending Paths included.
    """
    if output_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_path = os.path.join(base_dir, "reports", "resolution_workflow.png")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 16), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 130)
    ax.axis("off")

    # Styling constants
    BOX_BLUE = "#1E3A8A"     # Deep Navy
    BOX_LIGHT_BLUE = "#EFF6FF"
    BOX_BORDER_BLUE = "#3B82F6"
    BOX_GREEN = "#059669"    # Emerald
    BOX_LIGHT_GREEN = "#ECFDF5"
    BOX_AMBER = "#D97706"    # Amber
    BOX_LIGHT_AMBER = "#FFFBEB"
    BOX_RED = "#DC2626"      # Crimson
    TEXT_DARK = "#0F172A"

    def draw_box(x, y, w, h, title, subtitle="", bg=BOX_LIGHT_BLUE, border=BOX_BORDER_BLUE, text_color=TEXT_DARK, title_bold=True):
        rect = patches.FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle="round,pad=0.8,rounding_size=1.2",
            facecolor=bg, edgecolor=border, linewidth=2.0, zorder=2
        )
        ax.add_patch(rect)
        if subtitle:
            ax.text(x, y + 1.2, title, ha="center", va="center", fontsize=9.5, fontweight="bold" if title_bold else "normal", color=text_color, zorder=3)
            ax.text(x, y - 1.4, subtitle, ha="center", va="center", fontsize=8.0, color="#475569", zorder=3)
        else:
            ax.text(x, y, title, ha="center", va="center", fontsize=9.5, fontweight="bold" if title_bold else "normal", color=text_color, zorder=3)

    def draw_diamond(x, y, w, h, text, bg="#FEF3C7", border="#D97706", text_color="#92400E"):
        diamond = patches.Polygon(
            [[x, y + h / 2], [x + w / 2, y], [x, y - h / 2], [x - w / 2, y]],
            closed=True, facecolor=bg, edgecolor=border, linewidth=2.2, zorder=2
        )
        ax.add_patch(diamond)
        ax.text(x, y, text, ha="center", va="center", fontsize=9.5, fontweight="bold", color=text_color, zorder=3)

    def draw_arrow(x1, y1, x2, y2, label="", label_pos=(0, 0), label_color="#0F172A"):
        ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(arrowstyle="->", color="#334155", lw=2.0, shrinkA=3, shrinkB=3),
            zorder=1
        )
        if label:
            lx = (x1 + x2) / 2 + label_pos[0]
            ly = (y1 + y2) / 2 + label_pos[1]
            ax.text(lx, ly, label, fontsize=8.5, fontweight="bold", color=label_color, ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#CBD5E1", lw=1.0), zorder=4)

    # Title Banner
    banner = patches.FancyBboxPatch(
        (10, 122), 80, 6,
        boxstyle="round,pad=0.5,rounding_size=1.0",
        facecolor=BOX_BLUE, edgecolor="none", zorder=2
    )
    ax.add_patch(banner)
    ax.text(50, 125, "Billing Query Resolution & Error Analysis Workflow", ha="center", va="center", fontsize=13, fontweight="bold", color="white", zorder=3)
    ax.text(50, 123.2, "End-to-End Revenue Cycle Investigation, Corrective Action & Prevention Framework", ha="center", va="center", fontsize=8.5, color="#93C5FD", zorder=3)

    # 1. Claim/Query Received
    draw_box(50, 116, 44, 4.5, "1. Claim / Query Received", "ERA 835 denial, clearinghouse 277CA rejection, or internal audit alert")
    draw_arrow(50, 113.7, 50, 109.3)

    # 2. Identify Error Category
    draw_box(50, 107, 44, 4.5, "2. Identify Error Category", "Taxonomy classification: ICD specificity, CPT, modifier, E/M, registration, COB")
    draw_arrow(50, 104.7, 50, 100.3)

    # 3. Retrieve Records
    draw_box(50, 98, 44, 4.5, "3. Retrieve Patient & Encounter Records", "Master Patient Index (MPI), eligibility ledger, appointment record, signed chart")
    draw_arrow(50, 95.7, 50, 91.3)

    # 4. Verify Documentation
    draw_box(50, 89, 44, 4.5, "4. Verify Clinical Documentation", "Examine SOAP progress note, MDM complexity, provider signature, orders")
    draw_arrow(50, 86.7, 50, 82.3)

    # 5. Review Guidelines
    draw_box(50, 80, 44, 4.5, "5. Review ICD-10-CM / CPT / Billing Rules", "Cross-reference FY 2024 coding manuals, NCCI edits, MUE tables, LCD/NCDs")
    draw_arrow(50, 77.7, 50, 72.8)

    # 6. Decision Diamond: Is the Error Confirmed?
    draw_diamond(50, 69.5, 36, 6.5, "Is the Error Confirmed?\n(Data / Clinical Audit)")

    # NO Branch -> Document No Error -> Close Query (Right Side x=82)
    draw_arrow(68, 69.5, 82, 69.5, label="NO (Legitimate)", label_pos=(0, 1.5), label_color="#047857")
    draw_box(82, 63, 26, 4.5, "Document 'No Error Identified'", "Independent audit confirms\ncompliant coding/documentation", bg=BOX_LIGHT_GREEN, border=BOX_GREEN, text_color="#065F46")
    draw_arrow(82, 60.7, 82, 54.3)
    draw_box(82, 52, 26, 4.5, "Close Billing Query", "Release claim without alteration;\ntune audit thresholds", bg=BOX_LIGHT_GREEN, border=BOX_GREEN, text_color="#065F46")

    # YES Branch -> Identify Root Cause (Center x=36)
    draw_arrow(32, 69.5, 20, 69.5, label="YES (Defect)", label_pos=(0, 1.5), label_color="#B91C1C")
    draw_arrow(20, 69.5, 20, 62.3)
    draw_box(20, 60, 32, 4.5, "7. Identify Root Cause", "Operational classification: registration,\ncoding, clinical, IT, auth failure", bg=BOX_LIGHT_AMBER, border=BOX_AMBER, text_color="#92400E")

    draw_arrow(20, 57.7, 20, 52.3)
    draw_box(20, 50, 32, 4.5, "8. Prepare Corrective Action", "Map remediation plan, calculate\nfee adjustment, assign tasks", bg=BOX_LIGHT_AMBER, border=BOX_AMBER, text_color="#92400E")

    # Provider / Payer Query Decision (x=50, y=41)
    draw_arrow(20, 47.7, 50, 43.3)
    draw_box(50, 41, 46, 4.5, "9. Stakeholder Communication & Evidence Gathering", "Physician query for missing notes; PCP referral request; patient COB intake")

    # Secondary Branch: Escalation / Pending Docs (Left side x=15)
    draw_arrow(27, 41, 15, 41)
    draw_arrow(15, 41, 15, 33.3)
    draw_box(15, 31, 22, 4.5, "Escalate / Pending Hold", "ADR / Medical review or\nawaiting external consult records", bg="#FEF2F2", border=BOX_RED, text_color="#991B1B")

    # 10. Correct Coding / Documentation / Claim
    draw_arrow(50, 38.7, 50, 33.3)
    draw_box(50, 31, 46, 4.5, "10. Correct Coding, Documentation & Claim", "Update ICD-10/CPT, append Modifier 25, void duplicate, apply provider signature")

    # 11. Run Validation & Financial Checks
    draw_arrow(50, 28.7, 50, 23.3)
    draw_box(50, 21, 46, 4.5, "11. Validation Scrubber & Financial Reconciliation", "Execute pre-bill scrubber; verify zero fatal edits; reconcile allowable ledger balance")

    # 12. Resubmit Corrected Claim
    draw_arrow(50, 18.7, 50, 13.3)
    draw_box(50, 11, 46, 4.5, "12. Resubmit Claim (EDI 837P) / Issue Patient Statement", "Transmit replacement claim (Freq 7) or release clean hold; post ledger write-offs")

    # 13. Record Outcome & Preventive Action
    draw_arrow(50, 8.7, 50, 4.8)
    draw_box(50, 3, 52, 4.0, "13. Verify Final Resolution & Deploy Preventive Controls", "Confirm 277CA acceptance; update CDI coaching; configure EHR hard-stops", bg=BOX_BLUE, border="#1E40AF", text_color="white", title_bold=True)

    # Connect Close Query and Pending Hold to Final Record Outcome
    draw_arrow(82, 49.7, 72, 5.0)
    draw_arrow(15, 28.7, 28, 5.0)

    plt.tight_layout()
    plt.savefig(output_path, format="png", dpi=300, bbox_inches="tight")
    plt.close()

    return output_path
