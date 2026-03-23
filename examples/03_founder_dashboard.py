#!/usr/bin/env python3
"""
Example 3 — Founder Dashboard: full startup health check in one pass.

Combines all modules to produce a comprehensive founder dashboard:
unit economics, ESOP design, KPI health, burnout risk, and valuation.

Run with:
    python3 examples/03_founder_dashboard.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.fundraising import classify_stage, estimate_valuation
from src.gtm import calculate_unit_economics, calculate_burn_multiple
from src.talent import generate_vesting_schedule, get_esop_pool_recommendation
from src.ops import assess_operations_readiness
from src.resilience import assess_burnout
from src.crisis import assess_runway


# --------------------------------------------------------------------------
# Startup profile (edit these to match your company)
# --------------------------------------------------------------------------
PROFILE = {
    # Company metrics
    "arr_usd": 2_400_000,          # $2.4M ARR
    "growth_rate_pct": 140.0,      # 140% YoY growth
    "nrr_pct": 118.0,              # 118% Net Revenue Retention
    "monthly_burn": 280_000,       # $280K/month burn
    "cash_on_hand": 3_360_000,     # $3.36M cash (12 months runway)
    "net_new_arr_qtly": 600_000,   # $600K new ARR this quarter
    "net_burn_qtly": 840_000,      # $840K net burn this quarter

    # GTM metrics
    "cac": 8_500,                  # $8,500 CAC
    "monthly_revenue_per_customer": 2_000,
    "gross_margin_pct": 72.0,
    "avg_customer_lifetime_months": 36,

    # KPIs
    "kpis": {
        "monthly_churn_pct": 1.8,
        "nps": 48.0,
        "gross_margin_pct": 72.0,
        "cac_payback_months": 16.0,
        "nrr_pct": 118.0,
    },

    # ESOP
    "total_shares": 10_000_000,
    "options_to_grant": 300_000,

    # Founder wellbeing
    "sleep_hours": 6.5,
    "work_hours_per_week": 68.0,
    "days_since_break": 45.0,
    "decision_fatigue": 6.0,
    "social_isolation": 4.0,
    "loss_of_meaning": 3.0,
}


def section(title: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main() -> None:
    """Print a comprehensive founder dashboard."""
    print("\n" + "█" * 60)
    print("  FOUNDER ARSENAL — STARTUP HEALTH DASHBOARD")
    print("█" * 60)

    # --- 1. Stage & Valuation ---
    section("1. Fundraising Stage & Valuation")
    stage = classify_stage(PROFILE["arr_usd"])
    valuation = estimate_valuation(
        PROFILE["arr_usd"],
        PROFILE["growth_rate_pct"],
        PROFILE["nrr_pct"],
    )
    print(f"  Stage:      {stage.stage}")
    print(f"  ARR:        ${PROFILE['arr_usd']:,.0f}")
    print(f"  Valuation:  ${valuation['low']:,.0f} — ${valuation['high']:,.0f}")
    print(f"  Multiple:   {valuation['multiple_used']:.1f}x ARR")
    print(f"  Key metrics for this stage: {', '.join(stage.key_metrics[:3])}")

    # --- 2. Runway ---
    section("2. Cash Runway")
    runway = assess_runway(PROFILE["cash_on_hand"], PROFILE["monthly_burn"])
    print(f"  Cash on hand: ${PROFILE['cash_on_hand']:,.0f}")
    print(f"  Monthly burn: ${PROFILE['monthly_burn']:,.0f}")
    print(f"  Runway:       {runway.months_remaining:.1f} months")
    print(f"  Status:       {runway.severity.value}")
    print(f"  Protocol:     {runway.protocol}")

    # --- 3. Unit Economics ---
    section("3. Unit Economics")
    ue = calculate_unit_economics(
        PROFILE["cac"],
        PROFILE["monthly_revenue_per_customer"],
        PROFILE["gross_margin_pct"],
        PROFILE["avg_customer_lifetime_months"],
    )
    bm = calculate_burn_multiple(
        PROFILE["net_new_arr_qtly"],
        PROFILE["net_burn_qtly"],
    )
    print(f"  CAC:          ${ue.cac:,.0f}")
    print(f"  LTV:          ${ue.ltv:,.0f}")
    print(f"  LTV:CAC:      {ue.ltv_cac_ratio:.2f}x  ({ue.rating})")
    print(f"  Payback:      {ue.payback_months:.1f} months")
    print(f"  Burn Multiple:{bm.multiple:.2f}x  ({bm.status})")
    print(f"  Top action:   {ue.recommendations[0]}")

    # --- 4. KPI Health ---
    section("4. KPI Health Check")
    ops = assess_operations_readiness(PROFILE["kpis"])
    print(f"  Overall:   {ops.overall_status}  (score: {ops.score:.0f}/100)")
    print(f"  Healthy:   {', '.join(ops.healthy_kpis) or 'none'}")
    if ops.warning_kpis:
        print(f"  Warning:   {', '.join(ops.warning_kpis)}")
    if ops.critical_kpis:
        print(f"  Critical:  {', '.join(ops.critical_kpis)}")

    # --- 5. ESOP ---
    section("5. ESOP Design")
    rec = get_esop_pool_recommendation("Series A")
    vest = generate_vesting_schedule(
        PROFILE["options_to_grant"],
        vesting_months=48,
        cliff_months=12,
    )
    print(f"  Stage:        {rec.stage}")
    print(f"  Recommended pool: {rec.recommended_pool_pct:.0f}% ({rec.min_pool_pct:.0f}-{rec.max_pool_pct:.0f}%)")
    print(f"  Grant size:   {PROFILE['options_to_grant']:,} options")
    print(f"  Cliff vest:   {vest.cliff_vest:,} at month 12")
    print(f"  Monthly vest: {vest.monthly_vest_post_cliff:.0f}/month after cliff")

    # --- 6. Founder Wellbeing ---
    section("6. Founder Wellbeing")
    burnout = assess_burnout(
        sleep_hours_per_night=PROFILE["sleep_hours"],
        work_hours_per_week=PROFILE["work_hours_per_week"],
        days_since_last_break=PROFILE["days_since_break"],
        decision_fatigue_score=PROFILE["decision_fatigue"],
        social_isolation_score=PROFILE["social_isolation"],
        loss_of_meaning_score=PROFILE["loss_of_meaning"],
    )
    print(f"  Risk Level:  {burnout.risk_level}  (score: {burnout.score:.0f}/100)")
    if burnout.primary_drivers:
        print(f"  Drivers:     {', '.join(burnout.primary_drivers)}")
    print(f"  Action:      {burnout.immediate_actions[0]}")

    print("\n" + "█" * 60)
    print("  Dashboard complete. All modules operational.")
    print("█" * 60 + "\n")


if __name__ == "__main__":
    main()
