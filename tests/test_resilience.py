"""Tests for src/resilience.py — burnout assessment."""

import pytest

from src.resilience import assess_burnout, BurnoutAssessment


class TestAssessBurnout:
    """Tests for assess_burnout()."""

    # ---- Happy-path ----

    def test_low_burnout(self):
        result = assess_burnout(
            sleep_hours_per_night=8.0,
            work_hours_per_week=45.0,
            days_since_last_break=7.0,
            decision_fatigue_score=2.0,
            social_isolation_score=2.0,
            loss_of_meaning_score=2.0,
        )
        assert isinstance(result, BurnoutAssessment)
        assert result.risk_level == "LOW"
        assert result.score < 30

    def test_severe_burnout(self):
        result = assess_burnout(
            sleep_hours_per_night=4.0,
            work_hours_per_week=90.0,
            days_since_last_break=120.0,
            decision_fatigue_score=9.0,
            social_isolation_score=9.0,
            loss_of_meaning_score=9.0,
        )
        assert result.risk_level == "SEVERE"
        assert result.score >= 75

    def test_moderate_burnout(self):
        result = assess_burnout(
            sleep_hours_per_night=6.5,
            work_hours_per_week=65.0,
            days_since_last_break=40.0,
            decision_fatigue_score=6.0,
            social_isolation_score=5.0,
            loss_of_meaning_score=5.0,
        )
        assert result.risk_level in ("MODERATE", "HIGH")

    def test_score_0_to_100(self):
        result = assess_burnout(7, 50, 14, 5, 5, 5)
        assert 0.0 <= result.score <= 100.0

    def test_has_immediate_actions(self):
        result = assess_burnout(4, 90, 100, 9, 9, 9)
        assert len(result.immediate_actions) > 0

    def test_has_week_protocol(self):
        result = assess_burnout(4, 90, 100, 9, 9, 9)
        assert len(result.week_protocol) > 0

    def test_primary_drivers_list(self):
        result = assess_burnout(4, 90, 100, 9, 9, 9)
        assert isinstance(result.primary_drivers, list)

    def test_severe_has_multiple_actions(self):
        result = assess_burnout(4, 90, 100, 9, 9, 9)
        assert len(result.immediate_actions) >= 2

    def test_low_sleep_identified_as_driver(self):
        result = assess_burnout(
            sleep_hours_per_night=3.5,
            work_hours_per_week=40.0,
            days_since_last_break=7.0,
            decision_fatigue_score=1.0,
            social_isolation_score=1.0,
            loss_of_meaning_score=1.0,
        )
        assert "Sleep deprivation" in result.primary_drivers

    # ---- Boundary values ----

    def test_zero_days_since_break(self):
        result = assess_burnout(8, 40, 0, 1, 1, 1)
        assert result.score >= 0

    def test_score_1_on_fatigue_scores(self):
        result = assess_burnout(8, 40, 7, 1, 1, 1)
        assert result.risk_level == "LOW"

    def test_score_10_on_fatigue_scores(self):
        result = assess_burnout(4, 80, 90, 10, 10, 10)
        assert result.risk_level in ("SEVERE", "HIGH")

    # ---- Error handling ----

    def test_raises_on_negative_sleep(self):
        with pytest.raises(ValueError):
            assess_burnout(-1, 50, 7, 5, 5, 5)

    def test_raises_on_sleep_above_24(self):
        with pytest.raises(ValueError):
            assess_burnout(25, 50, 7, 5, 5, 5)

    def test_raises_on_negative_work_hours(self):
        with pytest.raises(ValueError):
            assess_burnout(8, -10, 7, 5, 5, 5)

    def test_raises_on_negative_days_break(self):
        with pytest.raises(ValueError):
            assess_burnout(8, 50, -1, 5, 5, 5)

    def test_raises_on_fatigue_below_1(self):
        with pytest.raises(ValueError):
            assess_burnout(8, 50, 7, 0, 5, 5)

    def test_raises_on_fatigue_above_10(self):
        with pytest.raises(ValueError):
            assess_burnout(8, 50, 7, 11, 5, 5)

    def test_raises_on_string_sleep(self):
        with pytest.raises(TypeError):
            assess_burnout("7", 50, 7, 5, 5, 5)  # type: ignore

    def test_raises_on_none_work_hours(self):
        with pytest.raises(TypeError):
            assess_burnout(7, None, 7, 5, 5, 5)  # type: ignore

    def test_raises_on_nan_sleep(self):
        with pytest.raises(ValueError):
            assess_burnout(float("nan"), 50, 7, 5, 5, 5)

    def test_raises_on_inf_days(self):
        with pytest.raises(ValueError):
            assess_burnout(7, 50, float("inf"), 5, 5, 5)
