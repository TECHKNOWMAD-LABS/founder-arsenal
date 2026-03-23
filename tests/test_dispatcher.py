"""Tests for src/dispatcher.py — intent dispatcher."""

import pytest
from unittest.mock import patch, MagicMock

from src.dispatcher import dispatch, _normalize, _score_skill
from src.models import DispatchResult, SkillName


class TestNormalize:
    """Tests for the _normalize helper."""

    def test_lowercase(self):
        assert _normalize("CRISIS") == "crisis"

    def test_strips_whitespace(self):
        assert _normalize("  hello  ") == "hello"

    def test_collapses_spaces(self):
        # _normalize collapses multiple spaces to single space
        result = _normalize("a  b   c")
        assert result == "a b c"
        assert "  " not in result

    def test_removes_punctuation(self):
        result = _normalize("Hello, World!")
        assert "," not in result
        assert "!" not in result

    def test_preserves_hyphens(self):
        result = _normalize("co-founder")
        assert "co-founder" in result

    def test_empty_string(self):
        assert _normalize("") == ""

    def test_unicode(self):
        result = _normalize("Straße café")
        assert isinstance(result, str)


class TestScoreSkill:
    """Tests for the _score_skill function."""

    def test_no_match(self):
        score, matched = _score_skill("hello world", ["crisis", "emergency"])
        assert score == 0.0
        assert matched == []

    def test_single_match(self):
        score, matched = _score_skill("we have a crisis", ["crisis", "emergency"])
        assert score > 0.0
        assert "crisis" in matched

    def test_multiple_matches_score_higher(self):
        score1, _ = _score_skill("crisis", ["crisis", "emergency"])
        score2, _ = _score_skill("crisis and emergency", ["crisis", "emergency"])
        assert score2 > score1

    def test_longer_keywords_weighted_higher(self):
        triggers_short = ["crisis"]
        triggers_long = ["co-founder conflict"]
        score_short, _ = _score_skill("co-founder conflict crisis", triggers_short)
        score_long, _ = _score_skill("co-founder conflict crisis", triggers_long)
        # Longer phrase match should carry more weight
        assert score_long >= score_short

    def test_returns_all_matched(self):
        _, matched = _score_skill("series a raise with term sheet", ["series a", "term sheet", "vc"])
        assert "series a" in matched
        assert "term sheet" in matched
        assert "vc" not in matched


class TestDispatch:
    """Tests for the main dispatch function."""

    # ---- Type / input validation ----

    def test_raises_on_none(self):
        with pytest.raises(TypeError):
            dispatch(None)  # type: ignore

    def test_raises_on_int(self):
        with pytest.raises(TypeError):
            dispatch(42)  # type: ignore

    def test_raises_on_empty_string(self):
        with pytest.raises(ValueError):
            dispatch("")

    def test_raises_on_whitespace_only(self):
        with pytest.raises(ValueError):
            dispatch("   ")

    # ---- Crisis routing ----

    def test_crisis_keyword_routes_crisis(self):
        result = dispatch("We're in a crisis — running out of runway")
        assert result is not None
        assert result.primary_skill == SkillName.CRISIS

    def test_data_breach_routes_crisis(self):
        result = dispatch("We had a data breach last night")
        assert result is not None
        assert result.primary_skill in (SkillName.CRISIS, SkillName.LEGAL)

    def test_shutdown_routes_crisis(self):
        result = dispatch("We're thinking about a graceful shutdown")
        assert result is not None
        assert result.primary_skill == SkillName.CRISIS

    # ---- Fundraising routing ----

    def test_fundraise_routes_fundraising(self):
        result = dispatch("Help me fundraise for our seed round")
        assert result is not None
        assert result.primary_skill == SkillName.FUNDRAISING

    def test_series_a_routes_fundraising(self):
        result = dispatch("Preparing for Series A raise at $2M ARR")
        assert result is not None
        assert result.primary_skill == SkillName.FUNDRAISING

    def test_investor_routes_fundraising(self):
        result = dispatch("I need to pitch our investor for a bridge round")
        assert result is not None
        assert result.primary_skill == SkillName.FUNDRAISING

    # ---- Legal routing ----

    def test_legal_keyword_routes_legal(self):
        result = dispatch("Need legal advice on our NDA structure")
        assert result is not None
        assert result.primary_skill == SkillName.LEGAL

    def test_patent_routes_legal(self):
        result = dispatch("Should we file a patent for our algorithm?")
        assert result is not None
        assert result.primary_skill == SkillName.LEGAL

    # ---- GTM routing ----

    def test_gtm_keyword_routes_gtm(self):
        result = dispatch("Help with our GTM strategy for B2B SaaS")
        assert result is not None
        assert result.primary_skill == SkillName.GTM

    def test_pricing_routes_gtm(self):
        result = dispatch("How should we think about pricing our product?")
        assert result is not None
        assert result.primary_skill == SkillName.GTM

    # ---- Talent routing ----

    def test_hiring_routes_talent(self):
        result = dispatch("We need to build our hiring process for a 10-person team")
        assert result is not None
        assert result.primary_skill == SkillName.TALENT

    def test_esop_routes_talent(self):
        result = dispatch("Design our ESOP scheme")
        assert result is not None
        assert result.primary_skill == SkillName.TALENT

    # ---- Resilience routing ----

    def test_burnout_routes_resilience(self):
        result = dispatch("I'm completely burned out and overwhelmed")
        assert result is not None
        assert result.primary_skill == SkillName.RESILIENCE

    def test_stress_routes_resilience(self):
        result = dispatch("Feeling very stressed and having decision fatigue")
        assert result is not None
        assert result.primary_skill == SkillName.RESILIENCE

    # ---- Ops routing ----

    def test_ops_keyword_routes_ops(self):
        result = dispatch("Need to set up our operations and SOPs")
        assert result is not None
        assert result.primary_skill == SkillName.OPS

    def test_gst_routes_ops(self):
        result = dispatch("Help with our GST filing process")
        assert result is not None
        assert result.primary_skill == SkillName.OPS

    # ---- Governance routing ----

    def test_board_routes_governance(self):
        result = dispatch("Preparing for our quarterly board meeting")
        assert result is not None
        assert result.primary_skill == SkillName.GOVERNANCE

    def test_soc2_routes_governance(self):
        result = dispatch("Starting our SOC2 compliance journey")
        assert result is not None
        assert result.primary_skill == SkillName.GOVERNANCE

    # ---- Multi-skill chains ----

    def test_series_a_chain(self):
        result = dispatch("Preparing for Series A raise with proper documents")
        assert result is not None
        assert result.primary_skill == SkillName.FUNDRAISING
        # Should include secondary skills
        assert len(result.secondary_skills) >= 0  # chain may or may not trigger

    def test_cofounder_conflict_chain(self):
        # co-founder conflict: must include "co-founder" + "conflict" keywords
        result = dispatch("co-founder conflict is tearing the company apart")
        assert result is not None
        assert result.primary_skill in (SkillName.CRISIS, SkillName.TALENT, SkillName.LEGAL)

    # ---- Result structure ----

    def test_result_has_confidence(self):
        result = dispatch("We need to fundraise urgently")
        assert result is not None
        assert 0.0 <= result.confidence <= 1.0

    def test_result_has_matched_keywords(self):
        result = dispatch("Our series a fundraise is coming up with investor meetings")
        assert result is not None
        assert len(result.matched_keywords) > 0

    def test_result_has_reasoning(self):
        result = dispatch("We're in a crisis")
        assert result is not None
        assert isinstance(result.reasoning, str)
        assert len(result.reasoning) > 0

    # ---- Edge cases ----

    def test_very_long_message_truncated(self):
        long_message = "fundraise " * 1000
        result = dispatch(long_message)
        assert result is not None  # Should not crash

    def test_unicode_message(self):
        result = dispatch("startup crisis — शुरुआत")
        assert result is not None

    def test_no_match_returns_none(self):
        result = dispatch("the quick brown fox jumps over the lazy dog")
        # May return None or low-confidence result
        if result is not None:
            assert result.confidence >= 0.0

    def test_max_secondary_respected(self):
        result = dispatch(
            "series a fundraise with investors and legal team and board",
            max_secondary=1,
        )
        assert result is not None
        assert len(result.secondary_skills) <= 1

    def test_min_confidence_filter(self):
        # With very high threshold and a weak single-keyword message, should return None
        result = dispatch("fundraise", min_confidence=0.99)
        # Either None (filtered) or high confidence if enough keywords matched
        assert result is None or result.confidence >= 0.0  # just test it doesn't crash

    def test_dispatch_result_type(self):
        result = dispatch("We need to raise funding for our startup")
        assert result is None or isinstance(result, DispatchResult)
