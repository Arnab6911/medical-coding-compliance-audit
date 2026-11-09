"""Data visualization module for Medical Coding Compliance Audit Simulation.

Generates high-resolution Matplotlib audit charts for compliance metrics,
severity distributions, issue breakdowns, and overall review rates.
"""

from __future__ import annotations
from typing import Dict, Any, List
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from src.models import AuditSummary, AuditSeverity


# Professional healthcare compliance color palette
COLORS = {
    "High": "#DC2626",      # Crimson / Red
    "Medium": "#F59E0B",    # Amber
    "Low": "#3B82F6",       # Blue
    "Clean": "#10B981",     # Emerald green
    "Flagged": "#EF4444",   # Red
    "Primary": "#1E3A8A",   # Deep navy
    "Background": "#F8FAFC",# Off-white
    "Text": "#1E293B",      # Slate dark
    "Muted": "#64748B"      # Slate gray
}


def plot_severity_distribution(summary: AuditSummary) -> plt.Figure:
    """Create a donut chart illustrating finding counts by severity level.

    Args:
        summary: AuditSummary with counted severities.

    Returns:
        Matplotlib Figure object.
    """
    labels = []
    sizes = []
    colors = []

    if summary.high_severity_count > 0:
        labels.append(f"High ({summary.high_severity_count})")
        sizes.append(summary.high_severity_count)
        colors.append(COLORS["High"])
    if summary.medium_severity_count > 0:
        labels.append(f"Medium ({summary.medium_severity_count})")
        sizes.append(summary.medium_severity_count)
        colors.append(COLORS["Medium"])
    if summary.low_severity_count > 0:
        labels.append(f"Low ({summary.low_severity_count})")
        sizes.append(summary.low_severity_count)
        colors.append(COLORS["Low"])

    fig, ax = plt.subplots(figsize=(5, 4), facecolor="white")

    if not sizes:
        ax.text(0.5, 0.5, "No Audit Flags\n(100% Clean)", ha="center", va="center",
                fontsize=14, color=COLORS["Clean"], weight="bold")
        ax.axis("off")
        return fig

    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct="%1.1f%%",
        startangle=140,
        pctdistance=0.75,
        wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2),
        textprops=dict(color=COLORS["Text"], fontsize=10, weight="medium")
    )

    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_weight("bold")
        autotext.set_fontsize(10)

    ax.set_title("Findings by Compliance Severity", fontsize=12, pad=15, weight="bold", color=COLORS["Primary"])
    plt.tight_layout()
    return fig


def plot_issue_categories(summary: AuditSummary) -> plt.Figure:
    """Create a horizontal bar chart of audit findings categorized by issue type.

    Args:
        summary: AuditSummary containing findings list.

    Returns:
        Matplotlib Figure object.
    """
    category_counts: Dict[str, int] = {}
    for finding in summary.findings:
        cat = finding.audit_issue
        category_counts[cat] = category_counts.get(cat, 0) + 1

    fig, ax = plt.subplots(figsize=(6, 4), facecolor="white")

    if not category_counts:
        ax.text(0.5, 0.5, "No Compliance Issues Identified", ha="center", va="center",
                fontsize=12, color=COLORS["Clean"], weight="bold")
        ax.axis("off")
        return fig

    # Sort categories descending
    sorted_cats = sorted(category_counts.items(), key=lambda x: x[1])
    categories = [k for k, _ in sorted_cats]
    counts = [v for _, v in sorted_cats]

    bars = ax.barh(categories, counts, color="#2563EB", height=0.6, edgecolor="#1D4ED8")

    # Add numeric labels to each bar
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f"{int(width)}",
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0),
                    textcoords="offset points",
                    ha="left", va="center",
                    fontsize=10, weight="bold", color=COLORS["Text"])

    ax.set_title("Audit Issues by Category", fontsize=12, pad=15, weight="bold", color=COLORS["Primary"])
    ax.set_xlabel("Number of Occurrences", fontsize=10, color=COLORS["Muted"])
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#CBD5E1")
    ax.spines["bottom"].set_color("#CBD5E1")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    plt.tight_layout()
    return fig


def plot_audit_status_breakdown(summary: AuditSummary) -> plt.Figure:
    """Create a donut chart displaying clean records vs records requiring review.

    Args:
        summary: AuditSummary with record counts.

    Returns:
        Matplotlib Figure object.
    """
    fig, ax = plt.subplots(figsize=(5, 4), facecolor="white")

    labels = [
        f"Clean ({summary.clean_records})",
        f"Requires Review ({summary.records_flagged})"
    ]
    sizes = [summary.clean_records, summary.records_flagged]
    colors = [COLORS["Clean"], COLORS["Flagged"]]

    if sum(sizes) == 0:
        ax.text(0.5, 0.5, "No Records Audited", ha="center", va="center", fontsize=12)
        ax.axis("off")
        return fig

    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.72,
        wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2),
        textprops=dict(color=COLORS["Text"], fontsize=10, weight="medium")
    )

    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_weight("bold")
        autotext.set_fontsize(10)

    ax.set_title("Encounter Audit Status", fontsize=12, pad=15, weight="bold", color=COLORS["Primary"])
    plt.tight_layout()
    return fig
