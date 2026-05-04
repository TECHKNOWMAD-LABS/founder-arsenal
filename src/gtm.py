"""
GTM Revenue Engine — unit economics and go-to-market calculators.

Implements CAC/LTV/payback calculations, burn multiple scoring, and
GTM motion classification as described in skills/gtm-revenue-engine/SKILL.md.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class UnitEconomics:
    """Startup unit economics summary."""

    cac: float
    ltv: float
    ltv_cac_ratio: float
    payback_months: float
    gross_margin_pct: float
    rating: str
    recommendations: list[str]


@dataclass
class BurnMultiple:
    """Burn multiple assessment."""

    net_new_arr: float
    net_burn: float
    multiple: float
    status: str
    action: str


def _validate_positive_float(value: float, name: str) -> float:
    """Validate a float is positive and finite."""
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number, got {type(value).__name__}")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")
    return float(value)


def _validate_pct(value: float, name: str) -> float:
    """Validate a percentage is between 0 and 100."""
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number, got {type(value).__name__}")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    if not (0.0 <= value <= 100.0):
        raise ValueError(f"{name} must be between 0 and 100, got {value}")
    return float(value)


def calculate_unit_economics(
    cac: float,
    monthly_revenue_per_customer: float,
    gross_margin_pct: float,
    avg_customer_lifetime_months: float,
) -> UnitEconomics:
    """
    Calculate startup unit economics: LTV, LTV:CAC ratio, and payback period.

    Args:
        cac: Customer Acquisition Cost (in any currency).
        monthly_revenue_per_customer: Average monthly revenue per customer.
        gross_margin_pct: Gross margin percentage (0-100).
        avg_customer_lifetime_months: Average customer lifetime in months.

    Returns:
        UnitEconomics with LTV:CAC ratio, payback period, and recommendations.

    Raises:
        TypeError: If any input is not a number.
        ValueError: If any input is outside valid range.
    """
    cac = _validate_positive_float(cac, "cac")
    mrpc = _validate_positive_float(monthly_revenue_per_customer, "monthly_revenue_per_customer")
    gm = _validate_pct(gross_margin_pct, "gross_margin_pct")
    lifetime = _validate_positive_float(
        avg_customer_lifetime_months, "avg_customer_lifetime_months"
    )

    monthly_gross_profit = mrpc * (gm / 100)
    ltv = monthly_gross_profit * lifetime
    ltv_cac = ltv / cac
    payback = cac / monthly_gross_profit if monthly_gross_profit > 0 else float("inf")

    # Rating benchmarks (B2B SaaS standards)
    if ltv_cac >= 3.0 and payback <= 18:
        rating = "EXCELLENT"
        recs = ["Scale GTM aggressively — unit economics support it", "Increase CAC investment"]
    elif ltv_cac >= 2.0 and payback <= 24:
        rating = "GOOD"
        recs = ["Optimize CAC while scaling", "Focus on NRR improvements to boost LTV"]
    elif ltv_cac >= 1.0:
        rating = "ACCEPTABLE"
        recs = ["Improve retention to increase LTV", "Reduce CAC through organic/content channels"]
    else:
        rating = "POOR"
        recs = [
            "STOP scaling until unit economics improve",
            "Reduce CAC: more efficient channels",
            "Improve retention: reduce churn first",
            "Increase pricing or upsell",
        ]

    return UnitEconomics(
        cac=cac,
        ltv=round(ltv, 2),
        ltv_cac_ratio=round(ltv_cac, 2),
        payback_months=round(payback, 1),
        gross_margin_pct=gm,
        rating=rating,
        recommendations=recs,
    )


def calculate_burn_multiple(
    net_new_arr: float,
    net_burn: float,
) -> BurnMultiple:
    """
    Calculate the burn multiple: net burn / net new ARR.

    A lower burn multiple is better. >2x is concerning, >3x is critical.

    Args:
        net_new_arr: Net new Annual Recurring Revenue added in the period.
        net_burn: Net cash burned in the same period (must be positive).

    Returns:
        BurnMultiple with status and recommended action.

    Raises:
        TypeError: If inputs are not numbers.
        ValueError: If inputs are non-positive.
    """
    arr = _validate_positive_float(net_new_arr, "net_new_arr")
    burn = _validate_positive_float(net_burn, "net_burn")

    multiple = round(burn / arr, 2)

    if multiple < 1.0:
        status = "Efficient"
        action = "Maintain course — excellent capital efficiency"
    elif multiple < 1.5:
        status = "Acceptable"
        action = "Monitor closely — consider optimizing CAC channels"
    elif multiple < 2.0:
        status = "Concerning"
        action = "Begin cost optimization — target <1.5x within 90 days"
    elif multiple < 3.0:
        status = "Dangerous"
        action = "Immediate cuts needed — audit all spend, freeze non-essential hiring"
    else:
        status = "Critical"
        action = "Survival mode — cut to break-even ARR as fast as possible"

    return BurnMultiple(
        net_new_arr=arr,
        net_burn=burn,
        multiple=multiple,
        status=status,
        action=action,
    )


def classify_gtm_motion(
    avg_deal_size_usd: float,
    avg_sales_cycle_days: float,
) -> dict[str, str]:
    """
    Classify GTM motion (PLG, SMB, Mid-Market, Enterprise) based on deal economics.

    Args:
        avg_deal_size_usd: Average deal/contract value in USD.
        avg_sales_cycle_days: Average sales cycle length in days.

    Returns:
        Dict with 'motion', 'description', and 'recommended_channels'.

    Raises:
        TypeError: If inputs are not numbers.
        ValueError: If inputs are non-positive.
    """
    deal = _validate_positive_float(avg_deal_size_usd, "avg_deal_size_usd")
    cycle = _validate_positive_float(avg_sales_cycle_days, "avg_sales_cycle_days")

    if deal < 1_000:
        motion = "PLG / Self-Serve"
        description = "Product-led growth — users sign up and upgrade without sales touch"
        channels = "Content SEO, product virality, freemium, in-app upsell"
    elif deal < 10_000:
        motion = "SMB / Inside Sales"
        description = "High-velocity inside sales with short cycles and low touch"
        channels = "SDR/AE pairs, digital marketing, webinars, partner channel"
    elif deal < 100_000:
        motion = "Mid-Market"
        description = "Structured sales process with champions and multi-stakeholder deals"
        channels = "Account executives, MEDDIC/SPICED, outbound, events, CS-led expansion"
    else:
        motion = "Enterprise"
        description = "Complex multi-stakeholder deals, long cycles, procurement process"
        channels = "Named accounts, field sales, executive sponsorship, SI partnerships, RFP"

    return {
        "motion": motion,
        "description": description,
        "recommended_channels": channels,
        "avg_deal_size_usd": deal,
        "avg_sales_cycle_days": cycle,
    }
