"""Shared data models for Founder Arsenal."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class SkillName(str, Enum):
    """Enumeration of all available founder skills."""

    FUNDRAISING = "fundraising-command-center"
    CRISIS = "crisis-war-room"
    LEGAL = "legal-ip-fortress"
    GTM = "gtm-revenue-engine"
    TALENT = "talent-os"
    RESILIENCE = "founder-resilience"
    OPS = "ops-scale-engine"
    GOVERNANCE = "governance-compliance-shield"


class CrisisSeverity(str, Enum):
    """Crisis severity levels."""

    WATCH = "WATCH"
    YELLOW = "YELLOW"
    ORANGE = "ORANGE"
    RED = "RED"
    BLACK = "BLACK"


class CrisisType(str, Enum):
    """The 14 crisis types that kill startups."""

    CASH_CRISIS = "cash_crisis"
    COFOUNDER_CONFLICT = "cofounder_conflict"
    PMF_LOSS = "pmf_loss"
    REVENUE_LOSS = "revenue_loss"
    TALENT_EXODUS = "talent_exodus"
    REGULATORY = "regulatory"
    DATA_BREACH = "data_breach"
    PR_CRISIS = "pr_crisis"
    PRODUCT_FAILURE = "product_failure"
    COMPETITIVE = "competitive"
    BOARD_CONFLICT = "board_conflict"
    KEY_PERSON = "key_person"
    MARKET_MACRO = "market_macro"
    FORCED_SHUTDOWN = "forced_shutdown"


@dataclass
class DispatchResult:
    """Result of a skill dispatch operation."""

    primary_skill: SkillName
    secondary_skills: list[SkillName] = field(default_factory=list)
    confidence: float = 1.0
    reasoning: str = ""
    matched_keywords: list[str] = field(default_factory=list)


@dataclass
class CrisisAssessment:
    """Result of a crisis severity assessment."""

    crisis_type: CrisisType
    severity_score: float
    severity_level: CrisisSeverity
    runway_impact: float
    revenue_impact: float
    team_impact: float
    reputation_impact: float
    legal_impact: float
    recommendations: list[str] = field(default_factory=list)


@dataclass
class RunwayAssessment:
    """Cash runway assessment."""

    months_remaining: float
    monthly_burn: float
    cash_on_hand: float
    severity: CrisisSeverity
    protocol: str
    immediate_actions: list[str] = field(default_factory=list)


@dataclass
class FundraisingStage:
    """Startup fundraising stage metadata."""

    stage: str
    typical_arr_range: tuple[float, float]
    typical_raise: tuple[float, float]
    typical_valuation_multiple: float
    key_metrics: list[str] = field(default_factory=list)
    india_sources: list[str] = field(default_factory=list)
