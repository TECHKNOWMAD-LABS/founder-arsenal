"""Tests for src/ops.py — KPI health checks and operations readiness."""

import pytest

from src.ops import (
    check_kpi_health,
    assess_operations_readiness,
    KPIHealth,
    OperationsReadiness,
)


class TestCheckKPIHealth:
    """Tests for check_kpi_health()."""

    # ---- Happy-path ----

    def test_healthy_churn(self):
        result = check_kpi_health("monthly_churn_pct", 1.5)
        assert isinstance(result, KPIHealth)
        assert result.status == "HEALTHY"

    def test_warning_churn(self):
        result = check_kpi_health("monthly_churn_pct", 3.5)
        assert result.status == "WARNING"

    def test_critical_churn(self):
        result = check_kpi_health("monthly_churn_pct", 7.0)
        assert result.status == "CRITICAL"

    def test_healthy_nps(self):
        result = check_kpi_health("nps", 55)
        assert result.status == "HEALTHY"

    def test_healthy_gross_margin(self):
        result = check_kpi_health("gross_margin_pct", 75)
        assert result.status == "HEALTHY"

    def test_healthy_nrr(self):
        result = check_kpi_health("nrr_pct", 120)
        assert result.status == "HEALTHY"

    def test_unhealthy_nrr(self):
        result = check_kpi_health("nrr_pct", 85)
        assert result.status in ("WARNING", "CRITICAL")

    def test_healthy_rule_of_40(self):
        result = check_kpi_health("rule_of_40", 45)
        assert result.status == "HEALTHY"

    def test_has_recommendation(self):
        result = check_kpi_health("monthly_churn_pct", 1.5)
        assert isinstance(result.recommendation, str)
        assert len(result.recommendation) > 0

    def test_kpi_name_preserved(self):
        result = check_kpi_health("nps", 50)
        assert result.kpi_name == "nps"

    def test_value_preserved(self):
        result = check_kpi_health("gross_margin_pct", 72.5)
        assert result.value == 72.5

    def test_benchmark_set(self):
        result = check_kpi_health("monthly_churn_pct", 2.0)
        assert result.benchmark == 2.0  # benchmark for churn is 2.0%

    def test_delta_calculated(self):
        result = check_kpi_health("nps", 60)  # 50% above benchmark of 40
        assert result.delta_pct == pytest.approx(50.0, abs=1.0)

    def test_case_insensitive_kpi_name(self):
        result = check_kpi_health("MONTHLY_CHURN_PCT", 2.0)
        assert result.kpi_name == "monthly_churn_pct"

    # ---- Error handling ----

    def test_raises_on_unknown_kpi(self):
        with pytest.raises(ValueError):
            check_kpi_health("vanity_metric", 42)

    def test_raises_on_empty_kpi_name(self):
        with pytest.raises(ValueError):
            check_kpi_health("", 42)

    def test_raises_on_non_string_kpi(self):
        with pytest.raises(TypeError):
            check_kpi_health(42, 5.0)  # type: ignore

    def test_raises_on_nan_value(self):
        with pytest.raises(ValueError):
            check_kpi_health("nps", float("nan"))

    def test_raises_on_inf_value(self):
        with pytest.raises(ValueError):
            check_kpi_health("gross_margin_pct", float("inf"))

    def test_raises_on_string_value(self):
        with pytest.raises(TypeError):
            check_kpi_health("nps", "high")  # type: ignore

    def test_raises_on_none_value(self):
        with pytest.raises(TypeError):
            check_kpi_health("nps", None)  # type: ignore


class TestAssessOperationsReadiness:
    """Tests for assess_operations_readiness()."""

    def test_all_healthy(self, healthy_kpis):
        result = assess_operations_readiness(healthy_kpis)
        assert isinstance(result, OperationsReadiness)
        assert result.overall_status == "HEALTHY"
        assert len(result.healthy_kpis) > 0
        assert len(result.critical_kpis) == 0

    def test_all_critical(self):
        bad_kpis = {
            "monthly_churn_pct": 15.0,
            "nps": -20.0,
            "gross_margin_pct": 30.0,
        }
        result = assess_operations_readiness(bad_kpis)
        assert result.overall_status == "CRITICAL"

    def test_empty_dict(self):
        result = assess_operations_readiness({})
        assert isinstance(result, OperationsReadiness)
        assert result.score == 0.0

    def test_mixed_health(self):
        mixed = {
            "monthly_churn_pct": 1.0,  # healthy
            "nrr_pct": 85.0,           # critical/warning
        }
        result = assess_operations_readiness(mixed)
        assert len(result.healthy_kpis) >= 1

    def test_score_0_to_100(self, healthy_kpis):
        result = assess_operations_readiness(healthy_kpis)
        assert 0.0 <= result.score <= 100.0

    def test_invalid_kpi_values_go_to_warning(self):
        kpis = {"monthly_churn_pct": "bad_value"}
        result = assess_operations_readiness(kpis)
        assert len(result.warning_kpis) > 0

    # ---- Error handling ----

    def test_raises_on_list(self):
        with pytest.raises(TypeError):
            assess_operations_readiness(["nps", "churn"])  # type: ignore

    def test_raises_on_string(self):
        with pytest.raises(TypeError):
            assess_operations_readiness("nps=50")  # type: ignore

    def test_raises_on_none(self):
        with pytest.raises(TypeError):
            assess_operations_readiness(None)  # type: ignore
