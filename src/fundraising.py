"""
Fundraising Command Center — stage classification and capital stack guidance.

Implements fundraising stage classification, valuation benchmarking, and
India-specific funding source recommendations.
"""

from __future__ import annotations

import math

from .models import FundraisingStage

# Fundraising stage definitions (ARR in USD, raise in USD)
_STAGES: list[FundraisingStage] = [
    FundraisingStage(
        stage="Pre-Seed",
        typical_arr_range=(0, 100_000),
        typical_raise=(100_000, 1_000_000),
        typical_valuation_multiple=0.0,  # Pre-revenue
        key_metrics=["founding team", "market size", "prototype/MVP"],
        india_sources=[
            "DPIIT recognition",
            "Startup India seed fund",
            "Angel networks (LetsVenture, AngelList India)",
        ],
    ),
    FundraisingStage(
        stage="Seed",
        typical_arr_range=(100_000, 1_000_000),
        typical_raise=(500_000, 3_000_000),
        typical_valuation_multiple=10.0,
        key_metrics=["MoM growth", "initial retention", "early PMF signals"],
        india_sources=[
            "Blume Ventures",
            "Chiratae",
            "Kalaari",
            "100X.VC",
            "Venture Catalysts",
            "DPIIT angel tax exemption",
        ],
    ),
    FundraisingStage(
        stage="Series A",
        typical_arr_range=(1_000_000, 10_000_000),
        typical_raise=(3_000_000, 15_000_000),
        typical_valuation_multiple=8.0,
        key_metrics=["ARR", "NRR", "CAC payback", "churn", "magic number"],
        india_sources=[
            "Sequoia India",
            "Accel India",
            "Matrix Partners India",
            "Nexus VP",
            "Elevation Capital",
        ],
    ),
    FundraisingStage(
        stage="Series B",
        typical_arr_range=(10_000_000, 50_000_000),
        typical_raise=(15_000_000, 50_000_000),
        typical_valuation_multiple=6.0,
        key_metrics=["Rule of 40", "gross margin", "payback period", "GRR", "expansion revenue"],
        india_sources=[
            "Tiger Global",
            "SoftBank Vision Fund",
            "Westbridge",
            "General Atlantic",
            "TA Associates",
        ],
    ),
    FundraisingStage(
        stage="Series C+",
        typical_arr_range=(50_000_000, float("inf")),
        typical_raise=(50_000_000, 200_000_000),
        typical_valuation_multiple=5.0,
        key_metrics=[
            "market share",
            "profitability path",
            "unit economics",
            "international expansion",
        ],
        india_sources=[
            "SoftBank",
            "Temasek",
            "GIC",
            "CPPIB",
            "Warburg Pincus",
            "public markets preparation",
        ],
    ),
]


def _validate_arr(arr: float) -> float:
    """Validate ARR is a non-negative finite number."""
    if not isinstance(arr, (int, float)):
        raise TypeError(f"arr must be a number, got {type(arr).__name__}")
    if not math.isfinite(arr):
        raise ValueError("arr must be a finite number")
    if arr < 0:
        raise ValueError(f"arr must be non-negative, got {arr}")
    return float(arr)


def classify_stage(arr_usd: float) -> FundraisingStage:
    """
    Classify a startup's fundraising stage based on Annual Recurring Revenue.

    Args:
        arr_usd: Annual Recurring Revenue in USD.

    Returns:
        FundraisingStage matching the ARR band.

    Raises:
        TypeError: If arr_usd is not a number.
        ValueError: If arr_usd is negative or not finite.
    """
    arr = _validate_arr(arr_usd)
    for stage in _STAGES:
        low, high = stage.typical_arr_range
        if low <= arr < high:
            return stage
    # Fallback to last stage (Series C+)
    return _STAGES[-1]


def estimate_valuation(
    arr_usd: float,
    growth_rate_pct: float,
    nrr_pct: float = 100.0,
) -> dict[str, float]:
    """
    Estimate valuation range using ARR multiples adjusted for growth and NRR.

    The base multiple comes from stage benchmarks and is adjusted upward for
    high growth (>100% YoY) and strong NRR (>120%).

    Args:
        arr_usd: Annual Recurring Revenue in USD.
        growth_rate_pct: Year-over-year revenue growth rate (percentage, e.g., 150 for 150%).
        nrr_pct: Net Revenue Retention percentage (e.g., 120 for 120%).

    Returns:
        Dict with 'low', 'mid', and 'high' valuation estimates in USD.

    Raises:
        TypeError: If inputs are not numbers.
        ValueError: If inputs are out of valid ranges.
    """
    arr = _validate_arr(arr_usd)
    if not isinstance(growth_rate_pct, (int, float)):
        raise TypeError(f"growth_rate_pct must be a number, got {type(growth_rate_pct).__name__}")
    if not isinstance(nrr_pct, (int, float)):
        raise TypeError(f"nrr_pct must be a number, got {type(nrr_pct).__name__}")
    if not math.isfinite(growth_rate_pct):
        raise ValueError("growth_rate_pct must be finite")
    if not math.isfinite(nrr_pct):
        raise ValueError("nrr_pct must be finite")
    if growth_rate_pct < 0:
        raise ValueError(f"growth_rate_pct must be non-negative, got {growth_rate_pct}")
    if nrr_pct < 0:
        raise ValueError(f"nrr_pct must be non-negative, got {nrr_pct}")

    stage = classify_stage(arr)
    base_multiple = (
        stage.typical_valuation_multiple if stage.typical_valuation_multiple > 0 else 5.0
    )

    # Growth adjustment: +1x multiple per 50% YoY growth above 100%
    growth_bonus = max(0.0, (growth_rate_pct - 100) / 50)

    # NRR adjustment: +1x per 10 points NRR above 110%
    nrr_bonus = max(0.0, (nrr_pct - 110) / 10)

    adjusted_multiple = base_multiple + growth_bonus + nrr_bonus

    mid = arr * adjusted_multiple
    return {
        "low": round(mid * 0.75, 2),
        "mid": round(mid, 2),
        "high": round(mid * 1.35, 2),
        "multiple_used": round(adjusted_multiple, 2),
    }


def get_india_funding_sources(stage: str) -> list[str]:
    """
    Return India-specific funding sources for a given fundraising stage name.

    Args:
        stage: Stage name (case-insensitive), e.g. 'Seed', 'Series A'.

    Returns:
        List of India-specific funding source names.

    Raises:
        TypeError: If stage is not a string.
        ValueError: If stage name is empty or not recognised.
    """
    if not isinstance(stage, str):
        raise TypeError(f"stage must be a str, got {type(stage).__name__}")
    stage = stage.strip()
    if not stage:
        raise ValueError("stage must not be empty")

    stage_lower = stage.lower()
    for s in _STAGES:
        if s.stage.lower() == stage_lower:
            return list(s.india_sources)

    known = [s.stage for s in _STAGES]
    raise ValueError(f"Unknown stage '{stage}'. Known stages: {known}")
