"""Flowchart Generator for Week 2 Medical Billing Process Simulation.

Generates a publication-grade, high-resolution workflow diagram illustrating:
1. Primary Billing Pathway:
   Patient Registration -> Insurance Verification -> Clinical Documentation ->
   Medical Coding -> Charge Capture -> Claim Scrubbing -> Claim Submission ->
   Claim Adjudication.
2. Adjudication Branching:
   - ACCEPTED: Payment Posting -> Patient Balance Calculation -> Final Invoice.
   - REJECTED: Demographic / Signature Correction -> Claim Resubmission.
   - DENIED: Denial Management & Audit -> Clinical Appeal / Write-Off.

Saves image as PNG for embedding directly into the Word report and Streamlit UI.
"""

import os
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import Optional


def generate_billing_flowchart(output_path: Optional[str] = None) -> str:
    """Render high-resolution medical billing workflow diagram and save to output_path.

    Returns the absolute filepath of the generated image.
    """
    if output_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_path = os.path.join(base_dir, "reports", "workflow_flowchart.png")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    fig, ax = plt.subplots(figsize=(15, 11), dpi=300)
    ax.set_facecolor("#F8FAFC")
    fig.patch.set_facecolor("#FFFFFF")

    # Coordinate system 0 to 100
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Title Banner
    ax.text(
        50, 96, "END-TO-END MEDICAL BILLING PROCESS WORKFLOW",
        ha="center", va="center", fontsize=16, fontweight="bold", color="#0F172A"
    )
    ax.text(
        50, 93, "Outpatient Revenue Cycle Simulation | Front-End, Mid-Revenue, and Back-End Adjudication Lifecycle",
        ha="center", va="center", fontsize=9.5, fontstyle="italic", color="#475569"
    )

    def draw_box(x, y, w, h, text, subtext, color, border_color="#1E293B"):
        """Draw rounded box with title and subtitle."""
        box = patches.FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle="round,pad=0.6,rounding_size=1.2",
            facecolor=color, edgecolor=border_color, linewidth=1.5,
            transform=ax.transData
        )
        ax.add_patch(box)
        ax.text(
            x, y + 1.1, text,
            ha="center", va="center", fontsize=9.5, fontweight="bold", color="#FFFFFF"
        )
        ax.text(
            x, y - 1.3, subtext,
            ha="center", va="center", fontsize=7.5, fontstyle="italic", color="#E2E8F0"
        )

    def draw_arrow(x1, y1, x2, y2, label="", color="#334155"):
        """Draw connecting directional arrow with optional label."""
        ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color=color, lw=2.0)
        )
        if label:
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            ax.text(
                mid_x, mid_y + 1.2, label,
                ha="center", va="center", fontsize=8, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor=color, lw=1)
            )

    # -------------------------------------------------------------------------
    # ROW 1: FRONT-END & CLINICAL DOCUMENTATION (Top horizontal row)
    # -------------------------------------------------------------------------
    draw_box(13, 83, 19, 6.5, "1. Patient Registration", "Demographics & Intake", "#1E3A8A")
    draw_arrow(22.5, 83, 27.5, 83)

    draw_box(37, 83, 19, 6.5, "2. Insurance Verification", "Eligibility & Prior Auth", "#0284C7")
    draw_arrow(46.5, 83, 51.5, 83)

    draw_box(61, 83, 19, 6.5, "3. Clinical Documentation", "Provider Chart & MDM", "#0D9488")
    draw_arrow(70.5, 83, 75.5, 83)

    draw_box(85, 83, 19, 6.5, "4. Medical Coding", "ICD-10-CM & CPT Entry", "#059669")

    # Down arrow to Row 2
    draw_arrow(85, 79.5, 85, 71.5)

    # -------------------------------------------------------------------------
    # ROW 2: MID-REVENUE CYCLE & SUBMISSION (Middle row right-to-left)
    # -------------------------------------------------------------------------
    draw_box(85, 68, 19, 6.5, "5. Charge Capture", "Fee Schedule Pricing", "#10B981")
    draw_arrow(75.5, 68, 70.5, 68)

    draw_box(61, 68, 19, 6.5, "6. Claim Scrubbing", "Pre-Bill Validation Rules", "#D97706")
    draw_arrow(51.5, 68, 46.5, 68)

    draw_box(37, 68, 19, 6.5, "7. Claim Submission", "EDI 837P Transaction", "#7C3AED")
    draw_arrow(27.5, 68, 22.5, 68)

    draw_box(13, 68, 19, 6.5, "8. Payer Adjudication", "EDI 835 Remittance / ERA", "#475569")

    # Down arrow to Decision Split
    draw_arrow(13, 64.5, 13, 56.5)

    # -------------------------------------------------------------------------
    # DECISION HUB & BRANCHING PATHWAYS
    # -------------------------------------------------------------------------
    # Decision Diamond at (13, 53)
    diamond = patches.RegularPolygon(
        (13, 53), numVertices=4, radius=4.5,
        facecolor="#F1F5F9", edgecolor="#0F172A", linewidth=2.0
    )
    ax.add_patch(diamond)
    ax.text(13, 53.5, "Payer", ha="center", va="center", fontsize=8.5, fontweight="bold")
    ax.text(13, 51.5, "Decision", ha="center", va="center", fontsize=7.5, color="#475569")

    # -------------------------------------------------------------------------
    # BRANCH A: ACCEPTED / PAID (Green flow to right)
    # -------------------------------------------------------------------------
    draw_arrow(17.5, 53, 30, 53, label="ACCEPTED / PAID", color="#059669")

    draw_box(41, 53, 19, 6.5, "9. Payment Posting", "Contractual Write-Off & EFT", "#059669")
    draw_arrow(50.5, 53, 58.5, 53)

    draw_box(68, 53, 19, 6.5, "10. Patient Responsibility", "Deductible, Copay, Coinsurance", "#0D9488")
    draw_arrow(77.5, 53, 82.5, 53)

    # Down arrow to Final Invoice
    draw_arrow(87.5, 49.5, 87.5, 38.5)
    draw_box(87.5, 35, 19, 6.5, "11. Final Patient Invoice", "Billing Statement / Due Notice", "#047857")

    # -------------------------------------------------------------------------
    # BRANCH B: REJECTED (Clearinghouse / Missing Info - Amber flow downwards)
    # -------------------------------------------------------------------------
    draw_arrow(13, 48.5, 13, 38.5, label="REJECTED (CARC 16)", color="#D97706")
    draw_box(13, 35, 20, 6.5, "Correction & Validation", "Fix Policy ID / Provider Sign", "#D97706")

    # Resubmission loop back to Claim Scrubbing
    ax.annotate(
        "", xy=(55, 65), xytext=(23, 35),
        arrowprops=dict(
            arrowstyle="->,head_width=0.4,head_length=0.6",
            color="#D97706", lw=1.8, linestyle="dashed"
        )
    )
    ax.text(
        35, 47, "Resubmit Corrected Claim", ha="center", va="center",
        fontsize=8, fontweight="bold", color="#B45309",
        bbox=dict(boxstyle="round,pad=0.2", facecolor="#FEF3C7", edgecolor="#D97706", lw=1)
    )

    # -------------------------------------------------------------------------
    # BRANCH C: DENIED (Medical Necessity / Referral - Crimson flow downwards)
    # -------------------------------------------------------------------------
    draw_arrow(17.5, 50, 48, 38.5, label="DENIED (CARC 50 / 197)", color="#DC2626")
    draw_box(53, 35, 21, 6.5, "Denial Review & Appeal", "Audit, Appeal, or Patient Hold", "#DC2626")

    # Bottom Summary Callout Box
    legend_box = patches.FancyBboxPatch(
        (5, 7), 90, 16,
        boxstyle="round,pad=0.8,rounding_size=1.0",
        facecolor="#EFF6FF", edgecolor="#3B82F6", linewidth=1.5
    )
    ax.add_patch(legend_box)
    ax.text(
        8, 20, "SIMULATION PATHWAY DEFINITIONS & REVENUE RECONCILIATION:",
        fontsize=9.5, fontweight="bold", color="#1E3A8A"
    )
    ax.text(
        8, 16.5,
        "• Primary Revenue Stream: Clean claims proceed through Charge Capture -> Scrubbing -> Submission -> Adjudication -> Posting -> Patient Invoice.",
        fontsize=8.5, color="#1E293B"
    )
    ax.text(
        8, 13.5,
        "• Scrubber / Clearinghouse Rejection Loop: Claims with invalid policy IDs or unsigned charts are corrected and re-submitted.",
        fontsize=8.5, color="#1E293B"
    )
    ax.text(
        8, 10.5,
        "• Denial Management Pathway: Claims denied for missing HMO referrals or medical necessity undergo clinical review and provider hold.",
        fontsize=8.5, color="#1E293B"
    )
    ax.text(
        8, 8.2,
        "• Foundational Billing Formula: Total Billed = Allowed Amount + Contractual Adjustment | Allowed = Insurance Paid + Patient Responsibility.",
        fontsize=8.5, fontweight="bold", color="#0F172A"
    )

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    return output_path
