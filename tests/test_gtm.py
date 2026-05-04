"""Tests for src/gtm.py — GTM unit economics calculators."""

import pytest

from src.gtm import (
    BurnMultiple,
    UnitEconomics,
    calculate_burn_multiple,
    calculate_unit_economics,
    classify_gtm_motion,
)


class TestCalculateUnitEconomics:
    """Tests for calculate_unit_economics()."""

    # ---- Happy-path ----

    def test_excellent_economics(self):
        result = calculate_unit_economics(
            cac=1000,
            monthly_revenue_per_customer=500,
            gross_margin_pct=80,
            avg_customer_lifetime_months=24,
        )
        assert isinstance(result, UnitEconomics)
        assert result.ltv > result.cac
        assert result.ltv_cac_ratio >= 3.0
        assert result.rating in ("EXCELLENT", "GOOD")

    def test_poor_economics(self):
        result = calculate_unit_economics(
            cac=10000,
            monthly_revenue_per_customer=100,
            gross_margin_pct=50,
            avg_customer_lifetime_months=12,
        )
        assert result.ltv_cac_ratio < 1.0
        assert result.rating == "POOR"
        assert len(result.recommendations) > 0

    def test_ltv_formula(self):
        # LTV = monthly_revenue * gross_margin * lifetime
        result = calculate_unit_economics(
            cac=500,
            monthly_revenue_per_customer=100,
            gross_margin_pct=70,
            avg_customer_lifetime_months=24,
        )
        expected_ltv = 100 * 0.70 * 24
        assert result.ltv == pytest.approx(expected_ltv, abs=0.01)

    def test_payback_formula(self):
        # payback = CAC / (monthly_revenue * gross_margin)
        result = calculate_unit_economics(
            cac=1000,
            monthly_revenue_per_customer=200,
            gross_margin_pct=75,
            avg_customer_lifetime_months=36,
        )
        expected_payback = 1000 / (200 * 0.75)
        assert result.payback_months == pytest.approx(expected_payback, abs=0.1)

    def test_ltv_cac_ratio_formula(self):
        result = calculate_unit_economics(
            cac=500,
            monthly_revenue_per_customer=100,
            gross_margin_pct=80,
            avg_customer_lifetime_months=12,
        )
        expected_ltv = 100 * 0.80 * 12
        expected_ratio = expected_ltv / 500
        assert result.ltv_cac_ratio == pytest.approx(expected_ratio, abs=0.01)

    def test_recommendations_not_empty(self):
        result = calculate_unit_economics(
            cac=1000,
            monthly_revenue_per_customer=100,
            gross_margin_pct=60,
            avg_customer_lifetime_months=18,
        )
        assert len(result.recommendations) > 0

    # ---- Error handling ----

    def test_raises_on_zero_cac(self):
        with pytest.raises(ValueError):
            calculate_unit_economics(0, 100, 70, 12)

    def test_raises_on_negative_mrpc(self):
        with pytest.raises(ValueError):
            calculate_unit_economics(500, -100, 70, 12)

    def test_raises_on_gm_above_100(self):
        with pytest.raises(ValueError):
            calculate_unit_economics(500, 100, 110, 12)

    def test_raises_on_negative_gm(self):
        with pytest.raises(ValueError):
            calculate_unit_economics(500, 100, -10, 12)

    def test_raises_on_zero_lifetime(self):
        with pytest.raises(ValueError):
            calculate_unit_economics(500, 100, 70, 0)

    def test_raises_on_string_cac(self):
        with pytest.raises(TypeError):
            calculate_unit_economics("1000", 100, 70, 12)  # type: ignore

    def test_raises_on_nan_gm(self):
        with pytest.raises(ValueError):
            calculate_unit_economics(500, 100, float("nan"), 12)

    def test_raises_on_inf_lifetime(self):
        with pytest.raises(ValueError):
            calculate_unit_economics(500, 100, 70, float("inf"))


class TestCalculateBurnMultiple:
    """Tests for calculate_burn_multiple()."""

    def test_efficient(self):
        result = calculate_burn_multiple(net_new_arr=2_000_000, net_burn=1_000_000)
        assert result.multiple == pytest.approx(0.5, abs=0.01)
        assert result.status == "Efficient"

    def test_acceptable(self):
        result = calculate_burn_multiple(net_new_arr=1_000_000, net_burn=1_200_000)
        assert result.multiple == pytest.approx(1.2, abs=0.01)
        assert result.status == "Acceptable"

    def test_concerning(self):
        result = calculate_burn_multiple(net_new_arr=1_000_000, net_burn=1_700_000)
        assert result.status == "Concerning"

    def test_dangerous(self):
        result = calculate_burn_multiple(net_new_arr=1_000_000, net_burn=2_500_000)
        assert result.status == "Dangerous"

    def test_critical(self):
        result = calculate_burn_multiple(net_new_arr=1_000_000, net_burn=4_000_000)
        assert result.status == "Critical"

    def test_action_not_empty(self):
        result = calculate_burn_multiple(1_000_000, 3_000_000)
        assert len(result.action) > 0

    def test_returns_burn_multiple(self):
        result = calculate_burn_multiple(1_000_000, 2_000_000)
        assert isinstance(result, BurnMultiple)

    # ---- Error handling ----

    def test_raises_on_zero_arr(self):
        with pytest.raises(ValueError):
            calculate_burn_multiple(0, 1_000_000)

    def test_raises_on_zero_burn(self):
        with pytest.raises(ValueError):
            calculate_burn_multiple(1_000_000, 0)

    def test_raises_on_negative_arr(self):
        with pytest.raises(ValueError):
            calculate_burn_multiple(-1_000_000, 1_000_000)

    def test_raises_on_string_burn(self):
        with pytest.raises(TypeError):
            calculate_burn_multiple(1_000_000, "2M")  # type: ignore

    def test_raises_on_nan(self):
        with pytest.raises(ValueError):
            calculate_burn_multiple(float("nan"), 1_000_000)


class TestClassifyGTMMotion:
    """Tests for classify_gtm_motion()."""

    def test_plg_low_deal(self):
        result = classify_gtm_motion(avg_deal_size_usd=500, avg_sales_cycle_days=1)
        assert "PLG" in result["motion"] or "Self-Serve" in result["motion"]

    def test_smb_mid_deal(self):
        result = classify_gtm_motion(avg_deal_size_usd=5_000, avg_sales_cycle_days=30)
        assert "SMB" in result["motion"]

    def test_mid_market(self):
        result = classify_gtm_motion(avg_deal_size_usd=50_000, avg_sales_cycle_days=90)
        assert "Mid-Market" in result["motion"]

    def test_enterprise(self):
        result = classify_gtm_motion(avg_deal_size_usd=500_000, avg_sales_cycle_days=180)
        assert "Enterprise" in result["motion"]

    def test_has_channels(self):
        result = classify_gtm_motion(1000, 7)
        assert len(result["recommended_channels"]) > 0

    def test_has_description(self):
        result = classify_gtm_motion(10_000, 30)
        assert len(result["description"]) > 0

    def test_returns_dict(self):
        result = classify_gtm_motion(5_000, 14)
        assert isinstance(result, dict)
        assert "motion" in result
        assert "description" in result
        assert "recommended_channels" in result

    # ---- Error handling ----

    def test_raises_on_zero_deal_size(self):
        with pytest.raises(ValueError):
            classify_gtm_motion(0, 30)

    def test_raises_on_zero_cycle(self):
        with pytest.raises(ValueError):
            classify_gtm_motion(10_000, 0)

    def test_raises_on_negative_deal(self):
        with pytest.raises(ValueError):
            classify_gtm_motion(-1000, 30)

    def test_raises_on_string_deal(self):
        with pytest.raises(TypeError):
            classify_gtm_motion("5000", 30)  # type: ignore

    def test_raises_on_nan_cycle(self):
        with pytest.raises(ValueError):
            classify_gtm_motion(5_000, float("nan"))
