"""
Founder Resilience — burnout scoring and recovery protocol.

Implements a simple burnout risk assessment and recovery framework
as described in skills/founder-resilience/SKILL.md.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BurnoutAssessment:
    """Founder burnout risk assessment result."""

    score: float  # 0-100, higher = more burnt out
    risk_level: str  # LOW, MODERATE, HIGH, SEVERE
    primary_drivers: list[str]
    immediate_actions: list[str]
    week_protocol: list[str]


# Burnout factors and their weights
_BURNOUT_FACTORS: dict[str, tuple[float, str]] = {
    "sleep_hours_per_night": (0.20, "Sleep deprivation"),
    "work_hours_per_week": (0.20, "Overwork"),
    "days_since_last_break": (0.15, "No recovery time"),
    "decision_fatigue_score": (0.15, "Decision fatigue"),
    "social_isolation_score": (0.15, "Social isolation"),
    "loss_of_meaning_score": (0.15, "Loss of meaning/purpose"),
}


def _normalize_sleep(hours: float) -> float:
    """Convert sleep hours to burnout contribution (0-1 scale)."""
    # Optimal: 7-9h → 0. <5h → 1.0
    if hours >= 7:
        return 0.0
    elif hours >= 6:
        return 0.3
    elif hours >= 5:
        return 0.7
    return 1.0


def _normalize_work_hours(hours_per_week: float) -> float:
    """Convert weekly work hours to burnout contribution (0-1)."""
    if hours_per_week <= 50:
        return 0.0
    elif hours_per_week <= 60:
        return 0.3
    elif hours_per_week <= 70:
        return 0.6
    elif hours_per_week <= 80:
        return 0.8
    return 1.0


def _normalize_days_no_break(days: float) -> float:
    """Convert days without break to burnout contribution (0-1)."""
    if days <= 14:
        return 0.0
    elif days <= 30:
        return 0.3
    elif days <= 60:
        return 0.6
    elif days <= 90:
        return 0.85
    return 1.0


def _validate_score_1_10(value: float, name: str) -> float:
    """Validate a 1-10 score."""
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number, got {type(value).__name__}")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    if not (1.0 <= value <= 10.0):
        raise ValueError(f"{name} must be between 1 and 10, got {value}")
    return float(value)


def assess_burnout(
    sleep_hours_per_night: float,
    work_hours_per_week: float,
    days_since_last_break: float,
    decision_fatigue_score: float,
    social_isolation_score: float,
    loss_of_meaning_score: float,
) -> BurnoutAssessment:
    """
    Assess founder burnout risk.

    Args:
        sleep_hours_per_night: Average sleep hours per night (e.g., 6.5).
        work_hours_per_week: Weekly work hours (e.g., 70).
        days_since_last_break: Days since last real break/vacation (e.g., 45).
        decision_fatigue_score: Self-rated decision fatigue 1-10 (10 = exhausted).
        social_isolation_score: Self-rated social isolation 1-10 (10 = completely isolated).
        loss_of_meaning_score: Self-rated loss of purpose 1-10 (10 = no meaning).

    Returns:
        BurnoutAssessment with score, risk level, drivers, and recovery protocol.

    Raises:
        TypeError: If any input is not a number.
        ValueError: If scores are outside valid ranges.
    """
    if not isinstance(sleep_hours_per_night, (int, float)):
        raise TypeError(f"sleep_hours_per_night must be a number")
    if not isinstance(work_hours_per_week, (int, float)):
        raise TypeError(f"work_hours_per_week must be a number")
    if not isinstance(days_since_last_break, (int, float)):
        raise TypeError(f"days_since_last_break must be a number")
    if not math.isfinite(sleep_hours_per_night):
        raise ValueError("sleep_hours_per_night must be finite")
    if not math.isfinite(work_hours_per_week):
        raise ValueError("work_hours_per_week must be finite")
    if not math.isfinite(days_since_last_break):
        raise ValueError("days_since_last_break must be finite")
    if sleep_hours_per_night < 0 or sleep_hours_per_night > 24:
        raise ValueError(f"sleep_hours_per_night must be 0-24, got {sleep_hours_per_night}")
    if work_hours_per_week < 0:
        raise ValueError(f"work_hours_per_week must be non-negative")
    if days_since_last_break < 0:
        raise ValueError(f"days_since_last_break must be non-negative")

    df = _validate_score_1_10(decision_fatigue_score, "decision_fatigue_score")
    si = _validate_score_1_10(social_isolation_score, "social_isolation_score")
    lm = _validate_score_1_10(loss_of_meaning_score, "loss_of_meaning_score")

    # Normalise each factor to 0-1
    s_norm = _normalize_sleep(sleep_hours_per_night)
    w_norm = _normalize_work_hours(work_hours_per_week)
    b_norm = _normalize_days_no_break(days_since_last_break)
    df_norm = (df - 1) / 9  # 1-10 → 0-1
    si_norm = (si - 1) / 9
    lm_norm = (lm - 1) / 9

    weighted = (
        s_norm * 0.20
        + w_norm * 0.20
        + b_norm * 0.15
        + df_norm * 0.15
        + si_norm * 0.15
        + lm_norm * 0.15
    )
    score = round(weighted * 100, 1)

    # Identify primary drivers
    factor_scores = {
        "Sleep deprivation": s_norm,
        "Overwork": w_norm,
        "No recovery time": b_norm,
        "Decision fatigue": df_norm,
        "Social isolation": si_norm,
        "Loss of meaning": lm_norm,
    }
    primary_drivers = [k for k, v in sorted(factor_scores.items(), key=lambda x: -x[1]) if v >= 0.5]

    # Risk level
    if score >= 75:
        risk_level = "SEVERE"
        immediate = [
            "STOP — take at least 3 consecutive days completely offline",
            "Tell a trusted co-founder/advisor about your state",
            "Cancel all non-essential meetings this week",
            "Consider speaking with a therapist or coach — today",
        ]
        week_protocol = [
            "No work before 9am or after 7pm",
            "One full rest day with zero work",
            "30 minutes of physical exercise daily",
            "Delegate 3 recurring decisions to a trusted team member",
        ]
    elif score >= 50:
        risk_level = "HIGH"
        immediate = [
            "Schedule a 2-3 day break within the next 2 weeks",
            "Identify your top 3 energy drains and eliminate one",
            "Implement a hard stop at 8pm daily",
        ]
        week_protocol = [
            "Protect 1 full offline day per week",
            "Morning routine: 30 min before checking messages",
            "Weekly 1:1 with a peer founder or coach",
        ]
    elif score >= 30:
        risk_level = "MODERATE"
        immediate = [
            "Review your calendar — cancel 20% of meetings",
            "Protect morning focused work time",
        ]
        week_protocol = [
            "Daily 20-minute walk or exercise",
            "Social time with non-work friends weekly",
            "Sunday evening no-work rule",
        ]
    else:
        risk_level = "LOW"
        immediate = ["Maintain current habits — you're managing well"]
        week_protocol = [
            "Continue sleep and recovery habits",
            "Monthly check-in with this assessment",
        ]

    return BurnoutAssessment(
        score=score,
        risk_level=risk_level,
        primary_drivers=primary_drivers,
        immediate_actions=immediate,
        week_protocol=week_protocol,
    )
