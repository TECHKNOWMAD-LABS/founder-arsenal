"""
Governance & Compliance Shield — board readiness and compliance checklist utilities.

Provides compliance scoring and board readiness assessments.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ComplianceFramework(str, Enum):
    """Supported compliance frameworks."""

    SOC2_TYPE1 = "SOC2 Type I"
    SOC2_TYPE2 = "SOC2 Type II"
    ISO27001 = "ISO 27001"
    GDPR = "GDPR"
    DPDP = "DPDP Act 2023"
    COMPANIES_ACT = "Companies Act 2013"
    SEBI_LODR = "SEBI LODR"


@dataclass
class ComplianceScore:
    """Compliance readiness score for a given framework."""

    framework: ComplianceFramework
    score: float  # 0-100
    gaps: list[str]
    quick_wins: list[str]
    estimated_effort_weeks: int


@dataclass
class BoardReadiness:
    """Board meeting readiness assessment."""

    score: float  # 0-100
    missing_items: list[str]
    recommendations: list[str]
    ready: bool


# Compliance checklist items per framework
_SOC2_CHECKLIST: list[tuple[str, str]] = [
    ("access_control", "Access control policy documented and enforced"),
    ("encryption_at_rest", "Data encryption at rest implemented"),
    ("encryption_in_transit", "TLS/HTTPS enforced for all data in transit"),
    ("audit_logs", "Audit logs enabled and retained for 12 months"),
    ("incident_response", "Incident response plan documented and tested"),
    ("vendor_management", "Third-party vendor security assessments completed"),
    ("penetration_test", "Annual penetration test conducted"),
    ("background_checks", "Employee background checks completed"),
    ("security_training", "Annual security awareness training"),
    ("change_management", "Change management process documented"),
]

_BOARD_CHECKLIST: list[tuple[str, str]] = [
    ("board_pack_sent", "Board pack sent 5+ days before meeting"),
    ("financials", "Monthly P&L, balance sheet, cash flow included"),
    ("kpi_dashboard", "KPI dashboard vs targets and prior period"),
    ("key_risks", "Top 3-5 risks with mitigations identified"),
    ("major_decisions", "Decision items clearly framed with recommendation"),
    ("previous_actions", "Previous meeting action items tracked"),
    ("cap_table", "Cap table and equity summary current"),
    ("legal_updates", "Material legal/regulatory updates flagged"),
]


def score_soc2_readiness(completed_items: list[str]) -> ComplianceScore:
    """
    Score SOC2 readiness based on completed checklist items.

    Args:
        completed_items: List of completed checklist item keys from the SOC2 checklist.

    Returns:
        ComplianceScore with gaps, quick wins, and effort estimate.

    Raises:
        TypeError: If completed_items is not a list.
    """
    if not isinstance(completed_items, list):
        raise TypeError(f"completed_items must be a list, got {type(completed_items).__name__}")

    completed_set = {str(item).lower().strip() for item in completed_items}
    all_keys = {key for key, _ in _SOC2_CHECKLIST}
    gaps = []
    quick_wins = []

    for key, description in _SOC2_CHECKLIST:
        if key not in completed_set:
            gaps.append(description)
            # These are relatively quick to implement
            if key in ("encryption_in_transit", "audit_logs", "security_training"):
                quick_wins.append(description)

    total = len(_SOC2_CHECKLIST)
    done = total - len(gaps)
    score = round(done / total * 100, 1)
    effort = max(4, len(gaps) * 3)  # ~3 weeks per gap

    return ComplianceScore(
        framework=ComplianceFramework.SOC2_TYPE1,
        score=score,
        gaps=gaps,
        quick_wins=quick_wins,
        estimated_effort_weeks=effort,
    )


def assess_board_readiness(completed_items: list[str]) -> BoardReadiness:
    """
    Assess board meeting readiness based on completed preparation items.

    Args:
        completed_items: List of completed board prep item keys.

    Returns:
        BoardReadiness with score, missing items, and recommendations.

    Raises:
        TypeError: If completed_items is not a list.
    """
    if not isinstance(completed_items, list):
        raise TypeError(f"completed_items must be a list, got {type(completed_items).__name__}")

    completed_set = {str(item).lower().strip() for item in completed_items}
    missing = []

    for key, description in _BOARD_CHECKLIST:
        if key not in completed_set:
            missing.append(description)

    total = len(_BOARD_CHECKLIST)
    done = total - len(missing)
    score = round(done / total * 100, 1)
    ready = score >= 75.0

    recs = []
    if not ready:
        recs.append("Complete missing items before proceeding with board meeting")
    if "board_pack_sent" in [k for k, _ in _BOARD_CHECKLIST if k not in completed_set]:
        recs.append("CRITICAL: Board pack must be sent 5+ days before meeting")
    if score >= 75:
        recs.append("Board prep is solid — focus on crisp narrative for decision items")

    return BoardReadiness(
        score=score,
        missing_items=missing,
        recommendations=recs,
        ready=ready,
    )
