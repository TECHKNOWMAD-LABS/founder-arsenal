"""Tests for src/governance.py — compliance scoring and board readiness."""

import pytest

from src.governance import (
    BoardReadiness,
    ComplianceFramework,
    ComplianceScore,
    assess_board_readiness,
    score_soc2_readiness,
)


class TestScoreSOC2Readiness:
    """Tests for score_soc2_readiness()."""

    # ---- Happy-path ----

    def test_all_complete(self):
        all_keys = [
            "access_control",
            "encryption_at_rest",
            "encryption_in_transit",
            "audit_logs",
            "incident_response",
            "vendor_management",
            "penetration_test",
            "background_checks",
            "security_training",
            "change_management",
        ]
        result = score_soc2_readiness(all_keys)
        assert isinstance(result, ComplianceScore)
        assert result.score == pytest.approx(100.0, abs=0.1)
        assert len(result.gaps) == 0

    def test_nothing_complete(self):
        result = score_soc2_readiness([])
        assert result.score == pytest.approx(0.0, abs=0.1)
        assert len(result.gaps) == 10

    def test_half_complete(self):
        half = [
            "access_control",
            "encryption_at_rest",
            "encryption_in_transit",
            "audit_logs",
            "incident_response",
        ]
        result = score_soc2_readiness(half)
        assert result.score == pytest.approx(50.0, abs=0.1)

    def test_returns_compliance_score(self):
        result = score_soc2_readiness([])
        assert isinstance(result, ComplianceScore)
        assert result.framework == ComplianceFramework.SOC2_TYPE1

    def test_quick_wins_subset_of_gaps(self):
        result = score_soc2_readiness([])
        for qw in result.quick_wins:
            assert qw in result.gaps

    def test_effort_weeks_increases_with_gaps(self):
        full = score_soc2_readiness(["access_control", "encryption_at_rest"])
        empty = score_soc2_readiness([])
        assert empty.estimated_effort_weeks > full.estimated_effort_weeks

    def test_unknown_keys_ignored(self):
        result = score_soc2_readiness(["unknown_key", "fake_item"])
        assert result.score == pytest.approx(0.0, abs=0.1)

    def test_case_sensitivity(self):
        # Keys are lowercased internally
        result_lower = score_soc2_readiness(["access_control"])
        result_upper = score_soc2_readiness(["ACCESS_CONTROL"])
        assert result_lower.score == result_upper.score

    # ---- Error handling ----

    def test_raises_on_non_list(self):
        with pytest.raises(TypeError):
            score_soc2_readiness("access_control")  # type: ignore

    def test_raises_on_none(self):
        with pytest.raises(TypeError):
            score_soc2_readiness(None)  # type: ignore

    def test_raises_on_dict(self):
        with pytest.raises(TypeError):
            score_soc2_readiness({"access_control": True})  # type: ignore

    # ---- Edge cases ----

    def test_empty_list_returns_score_object(self):
        result = score_soc2_readiness([])
        assert isinstance(result, ComplianceScore)
        assert result.score == 0.0

    def test_duplicate_keys_count_once(self):
        result = score_soc2_readiness(["access_control", "access_control"])
        single = score_soc2_readiness(["access_control"])
        assert result.score == single.score


class TestAssessBoardReadiness:
    """Tests for assess_board_readiness()."""

    def test_all_ready(self):
        all_keys = [
            "board_pack_sent",
            "financials",
            "kpi_dashboard",
            "key_risks",
            "major_decisions",
            "previous_actions",
            "cap_table",
            "legal_updates",
        ]
        result = assess_board_readiness(all_keys)
        assert isinstance(result, BoardReadiness)
        assert result.score == pytest.approx(100.0, abs=0.1)
        assert result.ready is True
        assert len(result.missing_items) == 0

    def test_nothing_ready(self):
        result = assess_board_readiness([])
        assert result.score == pytest.approx(0.0, abs=0.1)
        assert result.ready is False

    def test_75_percent_threshold(self):
        # 6 out of 8 = 75% → ready
        six_keys = [
            "board_pack_sent",
            "financials",
            "kpi_dashboard",
            "key_risks",
            "major_decisions",
            "previous_actions",
        ]
        result = assess_board_readiness(six_keys)
        assert result.score >= 75.0
        assert result.ready is True

    def test_below_threshold_not_ready(self):
        four_keys = ["board_pack_sent", "financials", "kpi_dashboard", "key_risks"]
        result = assess_board_readiness(four_keys)
        assert result.ready is False

    def test_missing_board_pack_generates_critical_rec(self):
        result = assess_board_readiness([])
        combined = " ".join(result.recommendations).upper()
        assert "CRITICAL" in combined or "board pack" in " ".join(result.recommendations).lower()

    def test_has_recommendations(self):
        result = assess_board_readiness([])
        assert len(result.recommendations) > 0

    # ---- Error handling ----

    def test_raises_on_string(self):
        with pytest.raises(TypeError):
            assess_board_readiness("board_pack_sent")  # type: ignore

    def test_raises_on_none(self):
        with pytest.raises(TypeError):
            assess_board_readiness(None)  # type: ignore
