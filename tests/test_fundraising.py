"""Tests for src/fundraising.py — stage classification and valuation."""

import pytest

from src.fundraising import classify_stage, estimate_valuation, get_india_funding_sources
from src.models import FundraisingStage


class TestClassifyStage:
    """Tests for classify_stage()."""

    def test_pre_seed(self):
        result = classify_stage(0)
        assert result.stage == "Pre-Seed"

    def test_pre_seed_boundary(self):
        result = classify_stage(99_999)
        assert result.stage == "Pre-Seed"

    def test_seed_lower(self):
        result = classify_stage(100_000)
        assert result.stage == "Seed"

    def test_seed_upper(self):
        result = classify_stage(999_999)
        assert result.stage == "Seed"

    def test_series_a_lower(self):
        result = classify_stage(1_000_000)
        assert result.stage == "Series A"

    def test_series_a_mid(self):
        result = classify_stage(5_000_000)
        assert result.stage == "Series A"

    def test_series_b(self):
        result = classify_stage(15_000_000)
        assert result.stage == "Series B"

    def test_series_c_plus(self):
        result = classify_stage(100_000_000)
        assert result.stage == "Series C+"

    def test_returns_fundraising_stage(self):
        result = classify_stage(2_000_000)
        assert isinstance(result, FundraisingStage)

    def test_has_key_metrics(self):
        result = classify_stage(2_000_000)
        assert len(result.key_metrics) > 0

    def test_has_india_sources(self):
        result = classify_stage(2_000_000)
        assert len(result.india_sources) > 0

    # ---- Error handling ----

    def test_raises_on_negative_arr(self):
        with pytest.raises(ValueError):
            classify_stage(-1)

    def test_raises_on_string(self):
        with pytest.raises(TypeError):
            classify_stage("1M")  # type: ignore

    def test_raises_on_none(self):
        with pytest.raises(TypeError):
            classify_stage(None)  # type: ignore

    def test_raises_on_nan(self):
        with pytest.raises(ValueError):
            classify_stage(float("nan"))

    def test_raises_on_inf(self):
        with pytest.raises(ValueError):
            classify_stage(float("inf"))


class TestEstimateValuation:
    """Tests for estimate_valuation()."""

    def test_returns_three_estimates(self):
        result = estimate_valuation(2_000_000, 150.0, 115.0)
        assert "low" in result
        assert "mid" in result
        assert "high" in result

    def test_low_less_than_high(self):
        result = estimate_valuation(2_000_000, 150.0, 115.0)
        assert result["low"] < result["mid"] < result["high"]

    def test_growth_increases_valuation(self):
        low_growth = estimate_valuation(2_000_000, 50.0, 100.0)
        high_growth = estimate_valuation(2_000_000, 200.0, 100.0)
        assert high_growth["mid"] > low_growth["mid"]

    def test_nrr_increases_valuation(self):
        low_nrr = estimate_valuation(2_000_000, 100.0, 100.0)
        high_nrr = estimate_valuation(2_000_000, 100.0, 130.0)
        assert high_nrr["mid"] > low_nrr["mid"]

    def test_zero_arr_returns_zeros(self):
        result = estimate_valuation(0, 100.0, 110.0)
        assert result["mid"] == 0.0

    def test_includes_multiple(self):
        result = estimate_valuation(2_000_000, 100.0, 100.0)
        assert "multiple_used" in result
        assert result["multiple_used"] > 0

    # ---- Error handling ----

    def test_raises_on_negative_arr(self):
        with pytest.raises(ValueError):
            estimate_valuation(-1, 100.0, 100.0)

    def test_raises_on_negative_growth(self):
        with pytest.raises(ValueError):
            estimate_valuation(1_000_000, -10.0, 100.0)

    def test_raises_on_negative_nrr(self):
        with pytest.raises(ValueError):
            estimate_valuation(1_000_000, 100.0, -5.0)

    def test_raises_on_string_arr(self):
        with pytest.raises(TypeError):
            estimate_valuation("2M", 100.0, 100.0)  # type: ignore

    def test_raises_on_nan_growth(self):
        with pytest.raises(ValueError):
            estimate_valuation(1_000_000, float("nan"), 100.0)

    def test_raises_on_inf_nrr(self):
        with pytest.raises(ValueError):
            estimate_valuation(1_000_000, 100.0, float("inf"))

    def test_all_values_positive_for_positive_arr(self):
        result = estimate_valuation(1_000_000, 100.0, 110.0)
        assert result["low"] > 0
        assert result["mid"] > 0
        assert result["high"] > 0


class TestGetIndiaFundingSources:
    """Tests for get_india_funding_sources()."""

    def test_seed_returns_list(self):
        result = get_india_funding_sources("Seed")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_series_a_returns_list(self):
        result = get_india_funding_sources("Series A")
        assert isinstance(result, list)

    def test_case_insensitive(self):
        result1 = get_india_funding_sources("seed")
        result2 = get_india_funding_sources("SEED")
        result3 = get_india_funding_sources("Seed")
        assert result1 == result2 == result3

    def test_all_stages_have_sources(self):
        for stage in ["Pre-Seed", "Seed", "Series A", "Series B", "Series C+"]:
            result = get_india_funding_sources(stage)
            assert len(result) > 0, f"No sources for {stage}"

    def test_returns_strings(self):
        result = get_india_funding_sources("Seed")
        assert all(isinstance(s, str) for s in result)

    # ---- Error handling ----

    def test_raises_on_unknown_stage(self):
        with pytest.raises(ValueError):
            get_india_funding_sources("Series Z")

    def test_raises_on_empty_string(self):
        with pytest.raises(ValueError):
            get_india_funding_sources("")

    def test_raises_on_whitespace(self):
        with pytest.raises(ValueError):
            get_india_funding_sources("   ")

    def test_raises_on_none(self):
        with pytest.raises(TypeError):
            get_india_funding_sources(None)  # type: ignore

    def test_raises_on_int(self):
        with pytest.raises(TypeError):
            get_india_funding_sources(1)  # type: ignore
