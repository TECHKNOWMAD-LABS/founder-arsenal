"""
Property-based tests using Hypothesis for Founder Arsenal core invariants.

Tests that:
1. Output values always within documented range
2. Serialization round-trips preserved
3. No crashes on any random valid input
"""

from __future__ import annotations

import math
import pytest
from hypothesis import given, assume, settings, HealthCheck
from hypothesis import strategies as st

from src.crisis import calculate_severity, assess_runway
from src.fundraising import classify_stage, estimate_valuation
from src.talent import generate_vesting_schedule, calculate_dilution
from src.gtm import calculate_unit_economics, calculate_burn_multiple
from src.resilience import assess_burnout
from src.dispatcher import dispatch
from src.models import CrisisType, CrisisSeverity


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

factor_1_5 = st.floats(min_value=1.0, max_value=5.0, allow_nan=False, allow_infinity=False)
positive_float = st.floats(min_value=0.001, max_value=1e12, allow_nan=False, allow_infinity=False)
pct_0_100 = st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False)
positive_int = st.integers(min_value=1, max_value=1_000_000)
non_negative_arr = st.floats(min_value=0, max_value=200_000_000, allow_nan=False, allow_infinity=False)


# ---------------------------------------------------------------------------
# Crisis module properties
# ---------------------------------------------------------------------------

class TestCrisisProperties:
    """Property-based tests for crisis module."""

    @given(
        crisis_type=st.sampled_from(list(CrisisType)),
        runway=factor_1_5,
        revenue=factor_1_5,
        team=factor_1_5,
        reputation=factor_1_5,
        legal=factor_1_5,
    )
    def test_severity_score_always_in_range(
        self, crisis_type, runway, revenue, team, reputation, legal
    ):
        """Severity score must always be in [2.0, 10.0] for valid inputs."""
        result = calculate_severity(crisis_type, runway, revenue, team, reputation, legal)
        assert 2.0 <= result.severity_score <= 10.0, (
            f"Score {result.severity_score} out of range for inputs: "
            f"runway={runway}, revenue={revenue}"
        )

    @given(
        crisis_type=st.sampled_from(list(CrisisType)),
        runway=factor_1_5,
        revenue=factor_1_5,
        team=factor_1_5,
        reputation=factor_1_5,
        legal=factor_1_5,
    )
    def test_severity_level_consistent_with_score(
        self, crisis_type, runway, revenue, team, reputation, legal
    ):
        """Severity level must be consistent with severity score thresholds."""
        result = calculate_severity(crisis_type, runway, revenue, team, reputation, legal)
        score = result.severity_score
        level = result.severity_level

        if score >= 8.0:
            assert level in (CrisisSeverity.BLACK, CrisisSeverity.RED)
        elif score >= 6.0:
            assert level in (CrisisSeverity.RED, CrisisSeverity.ORANGE)
        elif score >= 4.0:
            assert level in (CrisisSeverity.ORANGE, CrisisSeverity.YELLOW)
        elif score >= 2.0:
            assert level in (CrisisSeverity.YELLOW, CrisisSeverity.WATCH)

    @given(
        runway=st.floats(min_value=1.0, max_value=4.5, allow_nan=False, allow_infinity=False),
        revenue=st.floats(min_value=1.0, max_value=4.5, allow_nan=False, allow_infinity=False),
        team=st.floats(min_value=1.0, max_value=4.5, allow_nan=False, allow_infinity=False),
        reputation=st.floats(min_value=1.0, max_value=4.5, allow_nan=False, allow_infinity=False),
        legal=st.floats(min_value=1.0, max_value=4.5, allow_nan=False, allow_infinity=False),
    )
    def test_higher_factors_higher_score(
        self, runway, revenue, team, reputation, legal
    ):
        """Increasing all factors by 0.5 must increase the severity score."""
        low = calculate_severity(CrisisType.CASH_CRISIS, runway, revenue, team, reputation, legal)
        high = calculate_severity(
            CrisisType.CASH_CRISIS,
            runway + 0.5, revenue + 0.5, team + 0.5, reputation + 0.5, legal + 0.5
        )
        assert high.severity_score >= low.severity_score

    @given(
        cash=st.floats(min_value=0, max_value=1e9, allow_nan=False, allow_infinity=False),
        burn=positive_float,
    )
    def test_runway_months_formula(self, cash, burn):
        """months_remaining must always equal cash / burn."""
        result = assess_runway(cash_on_hand=cash, monthly_burn=burn)
        expected = cash / burn
        assert result.months_remaining == pytest.approx(expected, abs=0.01)

    @given(
        cash=st.floats(min_value=0, max_value=1e9, allow_nan=False, allow_infinity=False),
        burn=positive_float,
    )
    def test_runway_has_actions(self, cash, burn):
        """Every valid runway assessment must return at least one action."""
        result = assess_runway(cash_on_hand=cash, monthly_burn=burn)
        assert len(result.immediate_actions) >= 1


# ---------------------------------------------------------------------------
# Fundraising module properties
# ---------------------------------------------------------------------------

class TestFundraisingProperties:
    """Property-based tests for fundraising module."""

    @given(arr=non_negative_arr)
    def test_classify_stage_never_crashes(self, arr):
        """classify_stage must not crash for any non-negative finite ARR."""
        result = classify_stage(arr)
        assert result is not None
        assert len(result.stage) > 0

    @given(
        arr=non_negative_arr,
        growth=st.floats(min_value=0, max_value=10000, allow_nan=False, allow_infinity=False),
        nrr=pct_0_100,
    )
    def test_estimate_valuation_low_lt_high(self, arr, growth, nrr):
        """Valuation low must always be less than or equal to high."""
        result = estimate_valuation(arr, growth, nrr)
        assert result["low"] <= result["mid"] <= result["high"], (
            f"Valuation order violated: low={result['low']}, mid={result['mid']}, high={result['high']}"
        )

    @given(
        arr=non_negative_arr,
        growth=st.floats(min_value=0, max_value=10000, allow_nan=False, allow_infinity=False),
        nrr=pct_0_100,
    )
    def test_estimate_valuation_non_negative(self, arr, growth, nrr):
        """All valuation estimates must be non-negative."""
        result = estimate_valuation(arr, growth, nrr)
        assert result["low"] >= 0
        assert result["mid"] >= 0
        assert result["high"] >= 0

    @given(arr=non_negative_arr)
    def test_classify_and_estimate_consistent(self, arr):
        """classify_stage and estimate_valuation must handle the same ARR range."""
        stage = classify_stage(arr)
        result = estimate_valuation(arr, 100.0, 110.0)
        assert result["mid"] >= 0
        assert stage.stage is not None


# ---------------------------------------------------------------------------
# Talent module properties
# ---------------------------------------------------------------------------

class TestTalentProperties:
    """Property-based tests for talent module."""

    @given(
        total=positive_int,
        vesting=st.integers(min_value=2, max_value=96),
        cliff=st.integers(min_value=0, max_value=47),
    )
    def test_vesting_schedule_total_matches(self, total, vesting, cliff):
        """Final vested amount must always equal total_options."""
        assume(cliff < vesting)
        result = generate_vesting_schedule(total, vesting, cliff)
        _, final_vested = result.schedule[-1]
        assert final_vested == total, (
            f"Final vested {final_vested} != total {total} for "
            f"vesting={vesting}, cliff={cliff}"
        )

    @given(
        total=positive_int,
        vesting=st.integers(min_value=2, max_value=96),
        cliff=st.integers(min_value=0, max_value=47),
    )
    def test_vesting_monotonically_increases(self, total, vesting, cliff):
        """Cumulative vested must be monotonically non-decreasing."""
        assume(cliff < vesting)
        result = generate_vesting_schedule(total, vesting, cliff)
        vested_values = [v for _, v in result.schedule]
        for i in range(1, len(vested_values)):
            assert vested_values[i] >= vested_values[i - 1], (
                f"Non-monotonic at month {i}: {vested_values[i-1]} > {vested_values[i]}"
            )

    @given(
        current=positive_int,
        new=positive_int,
    )
    def test_dilution_post_ownership_lt_100(self, current, new):
        """Post-dilution ownership must always be < 100% when new shares are issued."""
        result = calculate_dilution(current, new)
        assert result["post_ownership_pct"] < 100.0

    @given(
        current=positive_int,
        new=positive_int,
    )
    def test_dilution_adds_to_100(self, current, new):
        """Pre-ownership (100%) = post_ownership + dilution."""
        result = calculate_dilution(current, new)
        assert (result["post_ownership_pct"] + result["dilution_pct"]) == pytest.approx(100.0, abs=0.01)


# ---------------------------------------------------------------------------
# GTM module properties
# ---------------------------------------------------------------------------

class TestGTMProperties:
    """Property-based tests for GTM module."""

    @given(
        cac=positive_float,
        mrpc=positive_float,
        gm=pct_0_100,
        lifetime=positive_float,
    )
    def test_unit_economics_never_crashes(self, cac, mrpc, gm, lifetime):
        """calculate_unit_economics must not crash for any valid positive inputs."""
        result = calculate_unit_economics(cac, mrpc, gm, lifetime)
        assert result is not None
        assert result.ltv >= 0

    @given(
        cac=positive_float,
        mrpc=positive_float,
        gm=pct_0_100,
        lifetime=positive_float,
    )
    def test_ltv_cac_consistency(self, cac, mrpc, gm, lifetime):
        """LTV:CAC ratio must be consistent with LTV and CAC (allowing for rounding)."""
        result = calculate_unit_economics(cac, mrpc, gm, lifetime)
        # Compute ratio from raw (un-rounded) values to avoid rounding artifact
        raw_ltv = (mrpc * (gm / 100)) * lifetime
        expected_ratio = raw_ltv / cac
        # Use relative tolerance to handle small values where abs tolerance breaks
        assert result.ltv_cac_ratio == pytest.approx(expected_ratio, rel=0.05, abs=0.01)

    @given(
        arr=positive_float,
        burn=positive_float,
    )
    def test_burn_multiple_formula(self, arr, burn):
        """Burn multiple must always equal net_burn / net_new_arr."""
        result = calculate_burn_multiple(arr, burn)
        expected = burn / arr
        assert result.multiple == pytest.approx(expected, abs=0.01)


# ---------------------------------------------------------------------------
# Dispatcher properties
# ---------------------------------------------------------------------------

class TestDispatcherProperties:
    """Property-based tests for dispatcher."""

    @given(msg=st.text(min_size=1, max_size=500, alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd", "Zs"))))
    @settings(suppress_health_check=[HealthCheck.too_slow])
    def test_dispatch_never_crashes_on_valid_text(self, msg):
        """dispatch() must not crash on any non-empty string."""
        assume(msg.strip())  # require non-whitespace
        result = dispatch(msg)
        assert result is None or hasattr(result, "primary_skill")

    @given(msg=st.text(min_size=1, max_size=1000))
    @settings(suppress_health_check=[HealthCheck.too_slow])
    def test_dispatch_confidence_in_range(self, msg):
        """If dispatch returns a result, confidence must be in [0, 1]."""
        assume(msg.strip())
        result = dispatch(msg)
        if result is not None:
            assert 0.0 <= result.confidence <= 1.0, (
                f"Confidence {result.confidence} out of [0,1] for message: {msg[:50]!r}"
            )


# ---------------------------------------------------------------------------
# Resilience module properties
# ---------------------------------------------------------------------------

class TestResilienceProperties:
    """Property-based tests for resilience module."""

    @given(
        sleep=st.floats(min_value=0, max_value=12, allow_nan=False, allow_infinity=False),
        work=st.floats(min_value=0, max_value=168, allow_nan=False, allow_infinity=False),
        days_break=st.floats(min_value=0, max_value=365, allow_nan=False, allow_infinity=False),
        df=st.floats(min_value=1, max_value=10, allow_nan=False, allow_infinity=False),
        si=st.floats(min_value=1, max_value=10, allow_nan=False, allow_infinity=False),
        lm=st.floats(min_value=1, max_value=10, allow_nan=False, allow_infinity=False),
    )
    def test_burnout_score_in_range(self, sleep, work, days_break, df, si, lm):
        """Burnout score must always be in [0, 100] for valid inputs."""
        result = assess_burnout(sleep, work, days_break, df, si, lm)
        assert 0.0 <= result.score <= 100.0, (
            f"Score {result.score} out of range"
        )

    @given(
        sleep=st.floats(min_value=0, max_value=12, allow_nan=False, allow_infinity=False),
        work=st.floats(min_value=0, max_value=168, allow_nan=False, allow_infinity=False),
        days_break=st.floats(min_value=0, max_value=365, allow_nan=False, allow_infinity=False),
        df=st.floats(min_value=1, max_value=10, allow_nan=False, allow_infinity=False),
        si=st.floats(min_value=1, max_value=10, allow_nan=False, allow_infinity=False),
        lm=st.floats(min_value=1, max_value=10, allow_nan=False, allow_infinity=False),
    )
    def test_burnout_risk_level_is_valid(self, sleep, work, days_break, df, si, lm):
        """Risk level must be one of the four documented levels."""
        result = assess_burnout(sleep, work, days_break, df, si, lm)
        assert result.risk_level in ("LOW", "MODERATE", "HIGH", "SEVERE")
