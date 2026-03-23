#!/usr/bin/env python3
"""
Example 2 — Crisis War Room: assess severity and get action protocols.

Shows how to use the crisis module to score startup crises, assess
runway, and get executable playbooks.

Run with:
    python3 examples/02_crisis_assessment.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.crisis import calculate_severity, assess_runway
from src.models import CrisisType


def main() -> None:
    """Demonstrate crisis severity scoring and runway assessment."""
    print("=" * 60)
    print("Founder Arsenal — Crisis War Room Demo")
    print("=" * 60)

    # --- Scenario 1: Cash crisis ---
    print("\n[Scenario 1] Cash Crisis Assessment")
    print("-" * 40)
    assessment = calculate_severity(
        crisis_type=CrisisType.CASH_CRISIS,
        runway_impact=4.0,     # 2 months of runway → high impact
        revenue_impact=3.0,    # Revenue at risk, but some cushion
        team_impact=3.0,       # Team morale shaken
        reputation_impact=2.0, # Not yet public
        legal_impact=2.0,      # No legal issues yet
    )
    print(f"Crisis Type:     {assessment.crisis_type.value}")
    print(f"Severity Score:  {assessment.severity_score}/10")
    print(f"Severity Level:  {assessment.severity_level.value}")
    print("Recommended Actions:")
    for rec in assessment.recommendations:
        print(f"  • {rec}")

    # --- Scenario 2: Data breach ---
    print("\n[Scenario 2] Data Breach Assessment")
    print("-" * 40)
    breach = calculate_severity(
        crisis_type=CrisisType.DATA_BREACH,
        runway_impact=2.0,      # Financial hit but not runway-threatening
        revenue_impact=4.0,     # Customer churn risk is high
        team_impact=3.0,        # Engineering team stressed
        reputation_impact=5.0,  # Reputation severely damaged
        legal_impact=5.0,       # GDPR/DPDP penalties, regulatory exposure
    )
    print(f"Crisis Type:     {breach.crisis_type.value}")
    print(f"Severity Score:  {breach.severity_score}/10")
    print(f"Severity Level:  {breach.severity_level.value}")
    print("Recommended Actions:")
    for rec in breach.recommendations:
        print(f"  • {rec}")

    # --- Scenario 3: Runway Assessment ---
    print("\n[Scenario 3] Runway Assessment")
    print("-" * 40)
    scenarios = [
        (3_000_000, 200_000, "Well-funded startup"),
        (900_000, 200_000, "4.5 months runway"),
        (400_000, 200_000, "2 months — danger zone"),
        (100_000, 200_000, "< 1 month — critical"),
    ]
    for cash, burn, label in scenarios:
        result = assess_runway(cash_on_hand=cash, monthly_burn=burn)
        print(f"\n  {label}:")
        print(f"    Cash: ${cash:,.0f} | Burn: ${burn:,.0f}/mo")
        print(f"    Runway: {result.months_remaining:.1f} months → {result.severity.value}")
        print(f"    Protocol: {result.protocol}")
        if result.immediate_actions:
            print(f"    Top action: {result.immediate_actions[0]}")

    print("\n" + "=" * 60)
    print("Crisis War Room demo complete.")


if __name__ == "__main__":
    main()
