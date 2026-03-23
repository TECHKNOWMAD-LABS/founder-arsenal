"""Tests for src/crisis.py — crisis severity scoring and runway assessment."""

import math
import pytest

from src.crisis import calculate_severity, assess_runway
from src.models import (
    CrisisAssessment,
    CrisisSeverity,
    CrisisType,
    RunwayAssessment,
)


class TestCalculateSeverity:
    """Tests for calculate_severity()."""

    # ---- Happy-path ----

    def test_mid_severity(self, sample_crisis_factors):
        result = calculate_severity(CrisisType.CASH_CRISIS, **sample_crisis_factors)
        assert isinstance(result, CrisisAssessment)
        assert result.crisis_type == CrisisType.CASH_CRISIS
        # All factors = 3 → weighted_avg = 3.0 → score = 6.0 → RED
        assert result.severity_score == pytest.approx(6.0, abs=0.1)
        assert result.severity_level == CrisisSeverity.RED

    def test_max_severity(self, high_severity_factors):
        result = calculate_severity(CrisisType.DATA_BREACH, **high_severity_factors)
        # runway=5(30%), revenue=5(25%), team=4(15%), rep=4(15%), legal=5(15%)
        # = (1.5+1.25+0.6+0.6+0.75) = 4.7 * 2 = 9.4 → BLACK
        assert result.severity_score > 8.0
        assert result.severity_level == CrisisSeverity.BLACK

    def test_min_severity(self, low_severity_factors):
        # All factors = 1 → weighted_avg = 1.0 → score = 2.0 → threshold >= 2.0 → YELLOW
        result = calculate_severity(CrisisType.KEY_PERSON, **low_severity_factors)
        assert result.severity_score == pytest.approx(2.0, abs=0.1)
        assert result.severity_level == CrisisSeverity.YELLOW

    def test_all_crisis_types(self, sample_crisis_factors):
        for ct in CrisisType:
            result = calculate_severity(ct, **sample_crisis_factors)
            assert result.crisis_type == ct
            assert result.severity_score > 0

    def test_has_recommendations(self, sample_crisis_factors):
        result = calculate_severity(CrisisType.CASH_CRISIS, **sample_crisis_factors)
        assert len(result.recommendations) >= 1
        assert all(isinstance(r, str) for r in result.recommendations)

    def test_black_has_war_room_rec(self, high_severity_factors):
        result = calculate_severity(CrisisType.FORCED_SHUTDOWN, **high_severity_factors)
        combined = " ".join(result.recommendations).lower()
        assert "war room" in combined or "72" in combined or "now" in combined

    # ---- Boundary values ----

    def test_factor_boundary_1(self, sample_crisis_factors):
        factors = {**sample_crisis_factors, "runway_impact": 1.0}
        result = calculate_severity(CrisisType.CASH_CRISIS, **factors)
        assert 0 < result.severity_score <= 10

    def test_factor_boundary_5(self, sample_crisis_factors):
        factors = {**sample_crisis_factors, "runway_impact": 5.0}
        result = calculate_severity(CrisisType.CASH_CRISIS, **factors)
        assert 0 < result.severity_score <= 10

    # ---- Error handling ----

    def test_raises_on_wrong_crisis_type(self, sample_crisis_factors):
        with pytest.raises(TypeError):
            calculate_severity("cash_crisis", **sample_crisis_factors)  # type: ignore

    def test_raises_on_factor_below_1(self, sample_crisis_factors):
        factors = {**sample_crisis_factors, "runway_impact": 0.5}
        with pytest.raises(ValueError):
            calculate_severity(CrisisType.CASH_CRISIS, **factors)

    def test_raises_on_factor_above_5(self, sample_crisis_factors):
        factors = {**sample_crisis_factors, "revenue_impact": 6.0}
        with pytest.raises(ValueError):
            calculate_severity(CrisisType.CASH_CRISIS, **factors)

    def test_raises_on_zero_factor(self, sample_crisis_factors):
        factors = {**sample_crisis_factors, "team_impact": 0.0}
        with pytest.raises(ValueError):
            calculate_severity(CrisisType.CASH_CRISIS, **factors)

    def test_raises_on_nan_factor(self, sample_crisis_factors):
        factors = {**sample_crisis_factors, "reputation_impact": float("nan")}
        with pytest.raises(ValueError):
            calculate_severity(CrisisType.CASH_CRISIS, **factors)

    def test_raises_on_inf_factor(self, sample_crisis_factors):
        factors = {**sample_crisis_factors, "legal_impact": float("inf")}
        with pytest.raises(ValueError):
            calculate_severity(CrisisType.CASH_CRISIS, **factors)

    def test_raises_on_string_factor(self, sample_crisis_factors):
        factors = {**sample_crisis_factors, "runway_impact": "high"}
        with pytest.raises(TypeError):
            calculate_severity(CrisisType.CASH_CRISIS, **factors)

    def test_raises_on_none_factor(self, sample_crisis_factors):
        factors = {**sample_crisis_factors, "runway_impact": None}
        with pytest.raises(TypeError):
            calculate_severity(CrisisType.CASH_CRISIS, **factors)

    # ---- Weighting logic ----

    def test_runway_has_highest_weight(self):
        """Runway impact (30%) should dominate vs other single factors (max 25%)."""
        base = dict(runway_impact=1.0, revenue_impact=3.0, team_impact=3.0,
                    reputation_impact=3.0, legal_impact=3.0)
        high_runway = dict(runway_impact=5.0, revenue_impact=3.0, team_impact=3.0,
                           reputation_impact=3.0, legal_impact=3.0)
        low_runway = calculate_severity(CrisisType.CASH_CRISIS, **base)
        high_runway_result = calculate_severity(CrisisType.CASH_CRISIS, **high_runway)
        assert high_runway_result.severity_score > low_runway.severity_score

    def test_score_is_between_2_and_10(self, sample_crisis_factors):
        """With all factors in [1,5] range, score must be in [2.0, 10.0]."""
        result = calculate_severity(CrisisType.CASH_CRISIS, **sample_crisis_factors)
        assert 2.0 <= result.severity_score <= 10.0


class TestAssessRunway:
    """Tests for assess_runway()."""

    # ---- Happy-path ----

    def test_healthy_runway(self):
        result = assess_runway(cash_on_hand=3_000_000, monthly_burn=200_000)
        assert isinstance(result, RunwayAssessment)
        assert result.months_remaining == pytest.approx(15.0, abs=0.1)
        assert result.severity == CrisisSeverity.WATCH

    def test_6_month_runway(self):
        result = assess_runway(cash_on_hand=1_200_000, monthly_burn=200_000)
        assert result.months_remaining == pytest.approx(6.0, abs=0.1)
        assert result.severity == CrisisSeverity.YELLOW

    def test_3_month_runway(self):
        result = assess_runway(cash_on_hand=600_000, monthly_burn=200_000)
        assert result.months_remaining == pytest.approx(3.0, abs=0.1)
        assert result.severity == CrisisSeverity.ORANGE

    def test_red_runway(self):
        result = assess_runway(cash_on_hand=100_000, monthly_burn=200_000)
        assert result.months_remaining == pytest.approx(0.5, abs=0.1)
        assert result.severity in (CrisisSeverity.RED, CrisisSeverity.BLACK)

    def test_has_protocol(self):
        result = assess_runway(cash_on_hand=1_000_000, monthly_burn=200_000)
        assert isinstance(result.protocol, str)
        assert len(result.protocol) > 0

    def test_has_immediate_actions(self):
        result = assess_runway(cash_on_hand=300_000, monthly_burn=200_000)
        assert isinstance(result.immediate_actions, list)
        assert len(result.immediate_actions) > 0

    def test_cash_preserved_in_result(self):
        result = assess_runway(cash_on_hand=500_000, monthly_burn=100_000)
        assert result.cash_on_hand == 500_000
        assert result.monthly_burn == 100_000

    # ---- Error handling ----

    def test_raises_on_negative_cash(self):
        with pytest.raises(ValueError):
            assess_runway(cash_on_hand=-100, monthly_burn=10_000)

    def test_raises_on_zero_burn(self):
        with pytest.raises(ValueError):
            assess_runway(cash_on_hand=1_000_000, monthly_burn=0)

    def test_raises_on_negative_burn(self):
        with pytest.raises(ValueError):
            assess_runway(cash_on_hand=1_000_000, monthly_burn=-5000)

    def test_raises_on_string_cash(self):
        with pytest.raises(TypeError):
            assess_runway(cash_on_hand="1000000", monthly_burn=10_000)  # type: ignore

    def test_raises_on_none_burn(self):
        with pytest.raises(TypeError):
            assess_runway(cash_on_hand=1_000_000, monthly_burn=None)  # type: ignore

    def test_raises_on_nan_cash(self):
        with pytest.raises(ValueError):
            assess_runway(cash_on_hand=float("nan"), monthly_burn=10_000)

    def test_raises_on_inf_burn(self):
        with pytest.raises(ValueError):
            assess_runway(cash_on_hand=1_000_000, monthly_burn=float("inf"))

    # ---- Edge cases ----

    def test_zero_cash(self):
        result = assess_runway(cash_on_hand=0, monthly_burn=10_000)
        assert result.months_remaining == 0.0
        assert result.severity == CrisisSeverity.BLACK

    def test_very_large_numbers(self):
        result = assess_runway(cash_on_hand=1_000_000_000, monthly_burn=1_000_000)
        assert result.months_remaining == pytest.approx(1000.0, abs=0.1)

    def test_fractional_months(self):
        result = assess_runway(cash_on_hand=150_000, monthly_burn=100_000)
        assert result.months_remaining == pytest.approx(1.5, abs=0.01)
