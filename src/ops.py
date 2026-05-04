"""
Ops Scale Engine — operational metrics and KPI validation.

Provides KPI health checks and burn rate validation utilities
as described in skills/ops-scale-engine/SKILL.md.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class KPIHealth:
    """KPI health assessment result."""

    kpi_name: str
    value: float
    benchmark: float
    status: str  # HEALTHY, WARNING, CRITICAL
    delta_pct: float
    recommendation: str


@dataclass
class OperationsReadiness:
    """Operations readiness assessment."""

    score: float
    healthy_kpis: list[str]
    warning_kpis: list[str]
    critical_kpis: list[str]
    overall_status: str


# Benchmark thresholds for common SaaS KPIs
# Format: (kpi_name, benchmark, higher_is_better, warning_threshold_pct, critical_threshold_pct)
_KPI_BENCHMARKS: dict[str, tuple[float, bool, float, float]] = {
    "monthly_churn_pct": (2.0, False, 150.0, 250.0),  # Lower is better; warn at 3%, critical at 5%
    "nps": (40.0, True, -50.0, -75.0),  # Higher is better; warn at <20, critical at <10
    "gross_margin_pct": (
        70.0,
        True,
        -15.0,
        -30.0,
    ),  # SaaS benchmark; warn at <60%, critical at <50%
    "cac_payback_months": (
        18.0,
        False,
        33.0,
        67.0,
    ),  # Lower is better; warn at 24m, critical at 30m
    "nrr_pct": (110.0, True, -9.0, -18.0),  # Warn at <100%, critical at <90%
    "rule_of_40": (40.0, True, -50.0, -100.0),  # Warn at <20, critical at <0
}


def _validate_finite_float(value: float, name: str) -> float:
    """Validate a float is finite."""
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number, got {type(value).__name__}")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return float(value)


def check_kpi_health(kpi_name: str, value: float) -> KPIHealth:
    """
    Check if a KPI value is healthy, warning, or critical against benchmarks.

    Supported KPI names:
    - monthly_churn_pct
    - nps
    - gross_margin_pct
    - cac_payback_months
    - nrr_pct
    - rule_of_40

    Args:
        kpi_name: Name of the KPI to check (see supported names above).
        value: Current KPI value.

    Returns:
        KPIHealth with status and recommendation.

    Raises:
        TypeError: If inputs are wrong types.
        ValueError: If kpi_name is unknown or value is not finite.
    """
    if not isinstance(kpi_name, str):
        raise TypeError(f"kpi_name must be a str, got {type(kpi_name).__name__}")
    kpi_name = kpi_name.strip().lower()
    if not kpi_name:
        raise ValueError("kpi_name must not be empty")
    if kpi_name not in _KPI_BENCHMARKS:
        raise ValueError(f"Unknown KPI '{kpi_name}'. Supported: {list(_KPI_BENCHMARKS.keys())}")

    value = _validate_finite_float(value, "value")
    benchmark, higher_is_better, warn_delta, critical_delta = _KPI_BENCHMARKS[kpi_name]

    delta_pct = ((value - benchmark) / abs(benchmark) * 100) if benchmark != 0 else 0.0

    if higher_is_better:
        if delta_pct >= warn_delta:
            status = "WARNING"
        elif delta_pct >= critical_delta:
            status = "WARNING" if delta_pct > critical_delta * 0.5 else "CRITICAL"
        elif delta_pct < critical_delta:
            status = "CRITICAL"
        else:
            status = "HEALTHY"
        # Simpler threshold check
        if delta_pct >= 0:
            status = "HEALTHY"
        elif delta_pct >= warn_delta:
            status = "WARNING"
        else:
            status = "CRITICAL"
    else:
        # Lower is better
        if delta_pct <= 0:
            status = "HEALTHY"
        elif delta_pct <= warn_delta:
            status = "WARNING"
        else:
            status = "CRITICAL"

    # Generate recommendation
    recs_map = {
        "monthly_churn_pct": {
            "HEALTHY": "Churn is healthy — focus on expansion revenue",
            "WARNING": "Churn elevated — launch customer success programme, identify at-risk accounts",
            "CRITICAL": "Churn crisis — stop all GTM spend, fix retention first",
        },
        "nps": {
            "HEALTHY": "Strong NPS — leverage promoters for referral programme",
            "WARNING": "NPS needs work — close the loop with detractors, fix top complaint",
            "CRITICAL": "NPS critical — product/service issue needs emergency fix",
        },
        "gross_margin_pct": {
            "HEALTHY": "Gross margins healthy — scale confidently",
            "WARNING": "Margins below benchmark — review COGS, pricing, and delivery costs",
            "CRITICAL": "Gross margins critically low — pricing/COGS restructure required before scaling",
        },
        "cac_payback_months": {
            "HEALTHY": "CAC payback is efficient — can accelerate GTM investment",
            "WARNING": "CAC payback lengthening — review channel efficiency",
            "CRITICAL": "CAC payback too long — pause paid channels, fix funnel conversion",
        },
        "nrr_pct": {
            "HEALTHY": "Strong NRR — expansion revenue offsetting churn",
            "WARNING": "NRR below 100% — net revenue shrinking, address urgently",
            "CRITICAL": "NRR critically low — customer base is contracting, survival risk",
        },
        "rule_of_40": {
            "HEALTHY": "Rule of 40 healthy — growth + profitability balanced",
            "WARNING": "Rule of 40 below target — improve growth OR reduce burn",
            "CRITICAL": "Rule of 40 failing — investor scrutiny likely, need improvement plan",
        },
    }

    recommendation = recs_map.get(kpi_name, {}).get(status, "Review this KPI against peers")

    return KPIHealth(
        kpi_name=kpi_name,
        value=value,
        benchmark=benchmark,
        status=status,
        delta_pct=round(delta_pct, 2),
        recommendation=recommendation,
    )


def assess_operations_readiness(kpi_values: dict[str, float]) -> OperationsReadiness:
    """
    Assess overall operational health from a dict of KPI values.

    Args:
        kpi_values: Dict mapping KPI names to current values.

    Returns:
        OperationsReadiness with aggregate score and KPI breakdown.

    Raises:
        TypeError: If kpi_values is not a dict.
    """
    if not isinstance(kpi_values, dict):
        raise TypeError(f"kpi_values must be a dict, got {type(kpi_values).__name__}")

    healthy: list[str] = []
    warning: list[str] = []
    critical: list[str] = []

    for name, value in kpi_values.items():
        try:
            health = check_kpi_health(name, value)
            if health.status == "HEALTHY":
                healthy.append(name)
            elif health.status == "WARNING":
                warning.append(name)
            else:
                critical.append(name)
        except (TypeError, ValueError):
            warning.append(f"{name} (invalid value)")

    total = len(healthy) + len(warning) + len(critical)
    if total == 0:
        score = 0.0
    else:
        score = round((len(healthy) * 1.0 + len(warning) * 0.5) / total * 100, 1)

    if critical:
        overall = "CRITICAL"
    elif warning:
        overall = "WARNING"
    else:
        overall = "HEALTHY"

    return OperationsReadiness(
        score=score,
        healthy_kpis=healthy,
        warning_kpis=warning,
        critical_kpis=critical,
        overall_status=overall,
    )
