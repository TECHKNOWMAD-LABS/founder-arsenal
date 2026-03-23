"""Tests for src/talent.py — ESOP and vesting calculations."""

import pytest

from src.talent import (
    generate_vesting_schedule,
    get_esop_pool_recommendation,
    calculate_dilution,
    VestingSchedule,
    ESOPPoolRecommendation,
)


class TestGenerateVestingSchedule:
    """Tests for generate_vesting_schedule()."""

    # ---- Happy-path ----

    def test_standard_4yr_1yr_cliff(self, valid_esop_params):
        result = generate_vesting_schedule(**valid_esop_params)
        assert isinstance(result, VestingSchedule)
        assert result.total_options == 10000
        assert result.vesting_months == 48
        assert result.cliff_months == 12

    def test_cliff_vest_is_25_percent(self, valid_esop_params):
        result = generate_vesting_schedule(**valid_esop_params)
        assert result.cliff_vest == pytest.approx(2500, abs=1)

    def test_final_cumulative_equals_total(self, valid_esop_params):
        result = generate_vesting_schedule(**valid_esop_params)
        last_month, last_vested = result.schedule[-1]
        assert last_vested == result.total_options

    def test_schedule_length_equals_vesting_months(self, valid_esop_params):
        result = generate_vesting_schedule(**valid_esop_params)
        assert len(result.schedule) == result.vesting_months

    def test_before_cliff_zero_vesting(self, valid_esop_params):
        result = generate_vesting_schedule(**valid_esop_params)
        # Months 1-11 should have 0 vested
        for month, vested in result.schedule[:11]:
            assert vested == 0, f"Month {month} should have 0 vested, got {vested}"

    def test_at_cliff_month_vesting_starts(self, valid_esop_params):
        result = generate_vesting_schedule(**valid_esop_params)
        cliff_entry = result.schedule[11]  # Month 12 (0-indexed at 11)
        assert cliff_entry[1] > 0

    def test_schedule_monotonically_increases(self, valid_esop_params):
        result = generate_vesting_schedule(**valid_esop_params)
        for i in range(1, len(result.schedule)):
            assert result.schedule[i][1] >= result.schedule[i - 1][1]

    def test_custom_vesting_period(self):
        result = generate_vesting_schedule(5000, vesting_months=36, cliff_months=6)
        assert result.vesting_months == 36
        assert result.cliff_months == 6
        assert len(result.schedule) == 36

    def test_no_cliff(self):
        result = generate_vesting_schedule(1000, vesting_months=24, cliff_months=0)
        # No cliff — should vest from month 1
        assert result.cliff_vest == 0
        # First entry should have some vesting
        first_month, first_vested = result.schedule[0]
        assert first_vested > 0

    def test_monthly_vest_positive_post_cliff(self, valid_esop_params):
        result = generate_vesting_schedule(**valid_esop_params)
        assert result.monthly_vest_post_cliff > 0

    # ---- Error handling ----

    def test_raises_on_negative_options(self):
        with pytest.raises(ValueError):
            generate_vesting_schedule(-100)

    def test_raises_on_zero_options(self):
        with pytest.raises(ValueError):
            generate_vesting_schedule(0)

    def test_raises_on_cliff_gte_vesting(self):
        with pytest.raises(ValueError):
            generate_vesting_schedule(1000, vesting_months=24, cliff_months=24)

    def test_raises_on_cliff_gt_vesting(self):
        with pytest.raises(ValueError):
            generate_vesting_schedule(1000, vesting_months=24, cliff_months=30)

    def test_raises_on_zero_vesting_months(self):
        with pytest.raises(ValueError):
            generate_vesting_schedule(1000, vesting_months=0)

    def test_raises_on_string_options(self):
        with pytest.raises(TypeError):
            generate_vesting_schedule("1000")  # type: ignore

    def test_raises_on_float_options(self):
        with pytest.raises(TypeError):
            generate_vesting_schedule(1000.5)  # type: ignore

    def test_raises_on_negative_cliff(self):
        with pytest.raises(ValueError):
            generate_vesting_schedule(1000, vesting_months=48, cliff_months=-1)


class TestGetESOPPoolRecommendation:
    """Tests for get_esop_pool_recommendation()."""

    def test_pre_seed_recommendation(self):
        result = get_esop_pool_recommendation("Pre-Seed")
        assert isinstance(result, ESOPPoolRecommendation)
        assert result.stage == "Pre-Seed"

    def test_seed_recommendation(self):
        result = get_esop_pool_recommendation("Seed")
        assert result.stage == "Seed"

    def test_series_a_recommendation(self):
        result = get_esop_pool_recommendation("Series A")
        assert result.stage == "Series A"

    def test_case_insensitive(self):
        result1 = get_esop_pool_recommendation("SEED")
        result2 = get_esop_pool_recommendation("seed")
        assert result1.stage == result2.stage

    def test_pool_pct_range_valid(self):
        for stage in ["Pre-Seed", "Seed", "Series A", "Series B"]:
            result = get_esop_pool_recommendation(stage)
            assert 0 < result.min_pool_pct <= result.recommended_pool_pct <= result.max_pool_pct

    def test_has_typical_grants(self):
        result = get_esop_pool_recommendation("Seed")
        assert len(result.typical_grants) > 0

    def test_has_rationale(self):
        result = get_esop_pool_recommendation("Series A")
        assert len(result.rationale) > 0

    # ---- Error handling ----

    def test_raises_on_unknown_stage(self):
        with pytest.raises(ValueError):
            get_esop_pool_recommendation("Series Z")

    def test_raises_on_empty_string(self):
        with pytest.raises(ValueError):
            get_esop_pool_recommendation("")

    def test_raises_on_none(self):
        with pytest.raises(TypeError):
            get_esop_pool_recommendation(None)  # type: ignore

    def test_raises_on_int(self):
        with pytest.raises(TypeError):
            get_esop_pool_recommendation(1)  # type: ignore


class TestCalculateDilution:
    """Tests for calculate_dilution()."""

    def test_basic_dilution(self):
        result = calculate_dilution(1_000_000, 200_000)
        assert result["post_ownership_pct"] == pytest.approx(83.333, abs=0.01)
        assert result["dilution_pct"] == pytest.approx(16.667, abs=0.01)
        assert result["new_total_shares"] == 1_200_000

    def test_50_percent_dilution(self):
        result = calculate_dilution(1_000_000, 1_000_000)
        assert result["post_ownership_pct"] == pytest.approx(50.0, abs=0.01)
        assert result["dilution_pct"] == pytest.approx(50.0, abs=0.01)

    def test_pre_ownership_always_100(self):
        result = calculate_dilution(500_000, 100_000)
        assert result["pre_ownership_pct"] == 100.0

    def test_new_total_correct(self):
        result = calculate_dilution(800_000, 200_000)
        assert result["new_total_shares"] == 1_000_000

    def test_small_dilution(self):
        result = calculate_dilution(10_000_000, 100_000)
        assert result["dilution_pct"] < 2.0
        assert result["post_ownership_pct"] > 98.0

    # ---- Error handling ----

    def test_raises_on_zero_current_shares(self):
        with pytest.raises(ValueError):
            calculate_dilution(0, 100_000)

    def test_raises_on_zero_new_shares(self):
        with pytest.raises(ValueError):
            calculate_dilution(1_000_000, 0)

    def test_raises_on_negative_current_shares(self):
        with pytest.raises(ValueError):
            calculate_dilution(-100, 100_000)

    def test_raises_on_string_shares(self):
        with pytest.raises(TypeError):
            calculate_dilution("1000000", 200_000)  # type: ignore

    def test_raises_on_float_shares(self):
        with pytest.raises(TypeError):
            calculate_dilution(1_000_000.5, 200_000)  # type: ignore
