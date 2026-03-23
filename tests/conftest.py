"""
Shared fixtures and mock helpers for Founder Arsenal tests.
"""

import pytest

from src.models import CrisisType, SkillName


# ---------------------------------------------------------------------------
# Common data fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_crisis_factors():
    """Mid-severity crisis factor values (1-5 scale, all set to 3)."""
    return {
        "runway_impact": 3.0,
        "revenue_impact": 3.0,
        "team_impact": 3.0,
        "reputation_impact": 3.0,
        "legal_impact": 3.0,
    }


@pytest.fixture
def high_severity_factors():
    """High-severity crisis factor values."""
    return {
        "runway_impact": 5.0,
        "revenue_impact": 5.0,
        "team_impact": 4.0,
        "reputation_impact": 4.0,
        "legal_impact": 5.0,
    }


@pytest.fixture
def low_severity_factors():
    """Low-severity crisis factor values."""
    return {
        "runway_impact": 1.0,
        "revenue_impact": 1.0,
        "team_impact": 1.0,
        "reputation_impact": 1.0,
        "legal_impact": 1.0,
    }


@pytest.fixture
def series_a_company():
    """Typical Series A company parameters."""
    return {
        "arr_usd": 2_000_000,
        "growth_rate_pct": 150.0,
        "nrr_pct": 115.0,
        "monthly_burn": 250_000,
        "cash_on_hand": 3_000_000,
    }


@pytest.fixture
def healthy_kpis():
    """Healthy SaaS KPI values."""
    return {
        "monthly_churn_pct": 1.5,
        "nps": 55.0,
        "gross_margin_pct": 75.0,
        "cac_payback_months": 14.0,
        "nrr_pct": 120.0,
    }


@pytest.fixture
def crisis_queries():
    """Sample founder queries that should route to crisis-war-room."""
    return [
        "We're running out of runway — only 2 months left",
        "Our co-founder wants to leave mid-product-build",
        "We had a data breach last night",
        "Major PR disaster — TechCrunch wrote a hit piece",
    ]


@pytest.fixture
def fundraising_queries():
    """Sample queries that should route to fundraising."""
    return [
        "Help me prepare for a Series A raise — $2M ARR, 150% growth",
        "What's a fair valuation for our seed round?",
        "We're thinking about DPIIT recognition for angel tax exemption",
    ]


@pytest.fixture
def valid_esop_params():
    """Standard ESOP vesting parameters."""
    return {
        "total_options": 10000,
        "vesting_months": 48,
        "cliff_months": 12,
    }
