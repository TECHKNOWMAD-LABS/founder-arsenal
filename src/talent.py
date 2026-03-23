"""
Talent OS — ESOP calculations and org design utilities.

Implements ESOP pool sizing, vesting schedule generation, and basic
compensation benchmarking as described in skills/talent-os/SKILL.md.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class VestingSchedule:
    """ESOP/RSU vesting schedule details."""

    total_options: int
    vesting_months: int
    cliff_months: int
    monthly_vest_post_cliff: float
    cliff_vest: int
    schedule: list[tuple[int, int]] = field(default_factory=list)  # (month, cumulative_vested)


@dataclass
class ESOPPoolRecommendation:
    """ESOP pool sizing recommendation."""

    stage: str
    recommended_pool_pct: float
    min_pool_pct: float
    max_pool_pct: float
    rationale: str
    typical_grants: list[str] = field(default_factory=list)


# ESOP pool guidance by stage
_ESOP_GUIDANCE: dict[str, ESOPPoolRecommendation] = {
    "pre-seed": ESOPPoolRecommendation(
        stage="Pre-Seed",
        recommended_pool_pct=10.0,
        min_pool_pct=5.0,
        max_pool_pct=15.0,
        rationale="Small team, founders need to reserve equity for key early hires",
        typical_grants=["CTO: 2-4%", "VP Engineering: 1-2%", "First 5 engineers: 0.25-0.5% each"],
    ),
    "seed": ESOPPoolRecommendation(
        stage="Seed",
        recommended_pool_pct=12.0,
        min_pool_pct=8.0,
        max_pool_pct=18.0,
        rationale="Building core team — need equity to compete with FAANG salaries",
        typical_grants=["VP Sales: 0.5-1%", "VP Product: 0.5-1%", "Senior Engineers: 0.1-0.25%"],
    ),
    "series a": ESOPPoolRecommendation(
        stage="Series A",
        recommended_pool_pct=15.0,
        min_pool_pct=10.0,
        max_pool_pct=20.0,
        rationale="Investors typically require 15-20% option pool pre-money (dilutive to founders)",
        typical_grants=["VP Engineering: 0.3-0.5%", "Director: 0.1-0.2%", "Senior IC: 0.05-0.1%"],
    ),
    "series b": ESOPPoolRecommendation(
        stage="Series B",
        recommended_pool_pct=10.0,
        min_pool_pct=7.0,
        max_pool_pct=12.0,
        rationale="Retention-focused pool refresh — new hire grants become smaller",
        typical_grants=["VP level: 0.1-0.2%", "Director: 0.05-0.1%", "Senior IC: 0.02-0.05%"],
    ),
}


def _validate_positive_int(value: int, name: str) -> int:
    """Validate an integer is positive."""
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")
    return value


def _validate_non_negative_int(value: int, name: str) -> int:
    """Validate an integer is non-negative."""
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    if value < 0:
        raise ValueError(f"{name} must be non-negative, got {value}")
    return value


def generate_vesting_schedule(
    total_options: int,
    vesting_months: int = 48,
    cliff_months: int = 12,
) -> VestingSchedule:
    """
    Generate a standard ESOP/RSU vesting schedule.

    The standard schedule is 4-year vest with 1-year cliff: 25% vests at month 12
    (cliff), then equal monthly tranches for the remaining 36 months.

    Args:
        total_options: Total number of options/shares to vest.
        vesting_months: Total vesting period in months (default 48 = 4 years).
        cliff_months: Cliff period in months (default 12 = 1 year).

    Returns:
        VestingSchedule with month-by-month cumulative vesting.

    Raises:
        TypeError: If inputs are not integers.
        ValueError: If cliff_months >= vesting_months, or any value is non-positive.
    """
    total_options = _validate_positive_int(total_options, "total_options")
    vesting_months = _validate_positive_int(vesting_months, "vesting_months")
    cliff_months = _validate_non_negative_int(cliff_months, "cliff_months")

    if cliff_months >= vesting_months:
        raise ValueError(
            f"cliff_months ({cliff_months}) must be less than vesting_months ({vesting_months})"
        )

    # Cliff vest = proportional to cliff period
    cliff_vest = round(total_options * cliff_months / vesting_months)
    remaining = total_options - cliff_vest
    post_cliff_months = vesting_months - cliff_months
    monthly = remaining / post_cliff_months if post_cliff_months > 0 else 0.0

    schedule: list[tuple[int, int]] = []
    cumulative = 0

    for month in range(1, vesting_months + 1):
        if month < cliff_months:
            schedule.append((month, 0))
        elif month == cliff_months:
            cumulative += cliff_vest
            schedule.append((month, cumulative))
        else:
            cumulative += monthly
            schedule.append((month, round(cumulative)))

    # Ensure final entry equals total_options (handle rounding)
    if schedule:
        last_month, _ = schedule[-1]
        schedule[-1] = (last_month, total_options)

    return VestingSchedule(
        total_options=total_options,
        vesting_months=vesting_months,
        cliff_months=cliff_months,
        monthly_vest_post_cliff=round(monthly, 2),
        cliff_vest=cliff_vest,
        schedule=schedule,
    )


def get_esop_pool_recommendation(stage: str) -> ESOPPoolRecommendation:
    """
    Get ESOP pool sizing recommendation for a given fundraising stage.

    Args:
        stage: Funding stage (case-insensitive): 'Pre-Seed', 'Seed', 'Series A', 'Series B'.

    Returns:
        ESOPPoolRecommendation with sizing guidance.

    Raises:
        TypeError: If stage is not a string.
        ValueError: If stage is empty or not recognised.
    """
    if not isinstance(stage, str):
        raise TypeError(f"stage must be a str, got {type(stage).__name__}")
    stage = stage.strip()
    if not stage:
        raise ValueError("stage must not be empty")

    key = stage.lower()
    if key not in _ESOP_GUIDANCE:
        known = list(_ESOP_GUIDANCE.keys())
        raise ValueError(f"Unknown stage '{stage}'. Known stages: {known}")
    return _ESOP_GUIDANCE[key]


def calculate_dilution(
    current_shares: int,
    new_shares_issued: int,
) -> dict[str, float]:
    """
    Calculate dilution from issuing new shares.

    Args:
        current_shares: Pre-issuance total shares outstanding.
        new_shares_issued: Number of new shares being issued.

    Returns:
        Dict with pre_ownership_pct, post_ownership_pct, dilution_pct, and new_total_shares.

    Raises:
        TypeError: If inputs are not integers.
        ValueError: If any value is non-positive.
    """
    current_shares = _validate_positive_int(current_shares, "current_shares")
    new_shares_issued = _validate_positive_int(new_shares_issued, "new_shares_issued")

    new_total = current_shares + new_shares_issued
    pre_pct = 100.0
    post_pct = round(current_shares / new_total * 100, 4)
    dilution = round(pre_pct - post_pct, 4)

    return {
        "pre_ownership_pct": pre_pct,
        "post_ownership_pct": post_pct,
        "dilution_pct": dilution,
        "new_total_shares": new_total,
    }
