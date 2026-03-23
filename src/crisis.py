"""
Crisis War Room — severity scoring and protocol routing.

Implements the 14-crisis severity calculator and runway assessment logic
described in skills/crisis-war-room/SKILL.md.
"""

from __future__ import annotations

import math
from typing import Optional

from .models import (
    CrisisAssessment,
    CrisisSeverity,
    CrisisType,
    RunwayAssessment,
)

# Severity thresholds (1-10 scale)
_SEVERITY_THRESHOLDS: list[tuple[float, CrisisSeverity]] = [
    (8.0, CrisisSeverity.BLACK),
    (6.0, CrisisSeverity.RED),
    (4.0, CrisisSeverity.ORANGE),
    (2.0, CrisisSeverity.YELLOW),
    (0.0, CrisisSeverity.WATCH),
]

# Runway → severity mapping (months)
_RUNWAY_MAP: list[tuple[float, CrisisSeverity, str, list[str]]] = [
    (
        12.0,
        CrisisSeverity.WATCH,
        "Optimize, don't panic",
        ["Monitor burn rate monthly", "Continue current growth plan"],
    ),
    (
        6.0,
        CrisisSeverity.YELLOW,
        "Begin fundraise or path to profitability",
        [
            "Initiate fundraising conversations",
            "Model path to profitability",
            "Identify discretionary cuts",
        ],
    ),
    (
        3.0,
        CrisisSeverity.ORANGE,
        "Emergency cost cuts + bridge raise",
        [
            "Freeze all non-essential spend",
            "Launch bridge raise immediately",
            "Cut variable costs 20-30%",
            "Accelerate AR collection",
        ],
    ),
    (
        1.0,
        CrisisSeverity.RED,
        "War room: survival mode",
        [
            "Freeze ALL hiring immediately",
            "Reduce founder salaries to minimum",
            "Negotiate 60-90 day vendor deferrals",
            "Call every investor for emergency bridge",
            "Evaluate asset sales",
        ],
    ),
    (
        0.0,
        CrisisSeverity.BLACK,
        "Wind-down or Hail Mary",
        [
            "Consult attorney — fiduciary duties",
            "Prepare wind-down plan",
            "Evaluate acqui-hire options",
            "Communicate transparently with team and investors",
        ],
    ),
]

# Protocol descriptions for each crisis type
_CRISIS_PROTOCOLS: dict[CrisisType, str] = {
    CrisisType.CASH_CRISIS: "Execute 72-Hour Cash Crisis Protocol: freeze spend, assess position, communicate to board",
    CrisisType.COFOUNDER_CONFLICT: "Assess conflict level (1-5), engage mediator if Level 3+, protect IP and company interests",
    CrisisType.PMF_LOSS: "Run PMF Health Dashboard check, execute 8-week recovery protocol",
    CrisisType.REVENUE_LOSS: "Customer recovery protocol: immediate outreach, root cause, retention offer",
    CrisisType.TALENT_EXODUS: "Retention emergency: 1:1s with all key players, compensation review, culture fix",
    CrisisType.REGULATORY: "Engage specialized legal counsel immediately, preserve all documents (litigation hold)",
    CrisisType.DATA_BREACH: "Execute P0 Breach Protocol: contain, assess, notify within 72h (GDPR) / 6h (CERT-In)",
    CrisisType.PR_CRISIS: "Apply SCARF framework: Secure → Clarify → Acknowledge → Remediate → Follow-up",
    CrisisType.PRODUCT_FAILURE: "War room: customer communication, engineering all-hands, SLA remediation",
    CrisisType.COMPETITIVE: "Competitive triage: accelerate differentiators, win-back campaign, pricing review",
    CrisisType.BOARD_CONFLICT: "Rally allies, demonstrate metrics, engage independent board member as mediator",
    CrisisType.KEY_PERSON: "Bus factor assessment, immediate knowledge transfer, succession plan activation",
    CrisisType.MARKET_MACRO: "Extend runway, pivot to defensible segments, strengthen customer relationships",
    CrisisType.FORCED_SHUTDOWN: "Execute 90-Day Graceful Shutdown Timeline: board vote → notify → dissolve",
}


def _validate_factor(value: float, name: str) -> float:
    """Validate a crisis factor score is between 1 and 5."""
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number, got {type(value).__name__}")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    if not (1.0 <= value <= 5.0):
        raise ValueError(f"{name} must be between 1 and 5, got {value}")
    return float(value)


def calculate_severity(
    crisis_type: CrisisType,
    runway_impact: float,
    revenue_impact: float,
    team_impact: float,
    reputation_impact: float,
    legal_impact: float,
) -> CrisisAssessment:
    """
    Calculate crisis severity using the weighted scoring model.

    Each factor is scored 1-5 and weighted:
    - runway_impact: 30%
    - revenue_impact: 25%
    - team_impact: 15%
    - reputation_impact: 15%
    - legal_impact: 15%

    The weighted average is multiplied by 2 to produce a 1-10 severity score.

    Args:
        crisis_type: The type of crisis being assessed.
        runway_impact: Score 1-5 for how many months of runway this consumes.
        revenue_impact: Score 1-5 for % of revenue at risk.
        team_impact: Score 1-5 for risk of departures or morale collapse.
        reputation_impact: Score 1-5 for customer/investor perception damage.
        legal_impact: Score 1-5 for fines, lawsuits, compliance violations.

    Returns:
        CrisisAssessment with severity score, level, and recommendations.

    Raises:
        TypeError: If crisis_type is not a CrisisType or factors are not numbers.
        ValueError: If any factor is outside 1-5 range.
    """
    if not isinstance(crisis_type, CrisisType):
        raise TypeError(
            f"crisis_type must be a CrisisType, got {type(crisis_type).__name__}"
        )

    ri = _validate_factor(runway_impact, "runway_impact")
    rev = _validate_factor(revenue_impact, "revenue_impact")
    ti = _validate_factor(team_impact, "team_impact")
    rep = _validate_factor(reputation_impact, "reputation_impact")
    li = _validate_factor(legal_impact, "legal_impact")

    weighted_avg = (ri * 0.30 + rev * 0.25 + ti * 0.15 + rep * 0.15 + li * 0.15)
    score = round(weighted_avg * 2, 2)  # Scale to 1-10

    # Determine severity level
    level = CrisisSeverity.WATCH
    for threshold, sev in _SEVERITY_THRESHOLDS:
        if score >= threshold:
            level = sev
            break

    # Build recommendations
    protocol = _CRISIS_PROTOCOLS.get(crisis_type, "Engage relevant specialist immediately")
    recommendations = [protocol]

    if score >= 8.0:
        recommendations.append("72-hour decision cycle — activate war room NOW")
        recommendations.append("All-hands response: CEO, board, legal counsel")
    elif score >= 6.0:
        recommendations.append("Daily war room — assign crisis commander")
        recommendations.append("2-week action plan with daily checkpoints")
    elif score >= 4.0:
        recommendations.append("Weekly war room — active management required")
        recommendations.append("Escalation matrix: who is accountable for each action?")
    else:
        recommendations.append("Monitor — set weekly review cadence")

    return CrisisAssessment(
        crisis_type=crisis_type,
        severity_score=score,
        severity_level=level,
        runway_impact=ri,
        revenue_impact=rev,
        team_impact=ti,
        reputation_impact=rep,
        legal_impact=li,
        recommendations=recommendations,
    )


def assess_runway(
    cash_on_hand: float,
    monthly_burn: float,
) -> RunwayAssessment:
    """
    Assess startup cash runway and return severity + action protocol.

    Args:
        cash_on_hand: Total available cash in any currency unit.
        monthly_burn: Monthly cash burn (must be positive).

    Returns:
        RunwayAssessment with severity, protocol description, and immediate actions.

    Raises:
        TypeError: If inputs are not numbers.
        ValueError: If cash_on_hand is negative or monthly_burn is not positive.
    """
    if not isinstance(cash_on_hand, (int, float)):
        raise TypeError(f"cash_on_hand must be a number, got {type(cash_on_hand).__name__}")
    if not isinstance(monthly_burn, (int, float)):
        raise TypeError(f"monthly_burn must be a number, got {type(monthly_burn).__name__}")
    if not math.isfinite(cash_on_hand):
        raise ValueError("cash_on_hand must be a finite number")
    if not math.isfinite(monthly_burn):
        raise ValueError("monthly_burn must be a finite number")
    if cash_on_hand < 0:
        raise ValueError(f"cash_on_hand must be non-negative, got {cash_on_hand}")
    if monthly_burn <= 0:
        raise ValueError(f"monthly_burn must be positive, got {monthly_burn}")

    months = cash_on_hand / monthly_burn

    severity = CrisisSeverity.WATCH
    protocol = "Optimize, don't panic"
    actions: list[str] = []

    for threshold, sev, proto, acts in _RUNWAY_MAP:
        if months >= threshold:
            severity = sev
            protocol = proto
            actions = acts
            break

    return RunwayAssessment(
        months_remaining=round(months, 2),
        monthly_burn=monthly_burn,
        cash_on_hand=cash_on_hand,
        severity=severity,
        protocol=protocol,
        immediate_actions=actions,
    )
