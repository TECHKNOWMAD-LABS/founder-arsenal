"""
Intent dispatcher for Founder Arsenal.

Routes natural-language founder queries to the appropriate skill(s) based on
keyword matching and confidence scoring. Supports single-skill and multi-skill
chaining.
"""

from __future__ import annotations

import re

from .models import DispatchResult, SkillName

# ---------------------------------------------------------------------------
# Keyword trigger maps — order matters for priority
# ---------------------------------------------------------------------------

_SKILL_TRIGGERS: dict[SkillName, list[str]] = {
    SkillName.FUNDRAISING: [
        "fundraise",
        "fundraising",
        "raise",
        "pitch",
        "term sheet",
        "termsheet",
        "cap table",
        "captable",
        "safe",
        "convertible",
        "dpiit",
        "angel tax",
        "vc",
        "venture capital",
        "investor",
        "valuation",
        "pre-seed",
        "seed",
        "series a",
        "series b",
        "series c",
        "ipo",
        "bridge",
        "crowdfunding",
        "grant",
        "arr",
        "revenue multiple",
    ],
    SkillName.CRISIS: [
        "crisis",
        "emergency",
        "fire",
        "disaster",
        "failing",
        "dying",
        "shutdown",
        "pivot",
        "runway",
        "burn rate",
        "co-founder conflict",
        "cofounder conflict",
        "pr disaster",
        "data breach",
        "layoff",
        "down round",
        "churn spike",
        "regulatory action",
        "legal threat",
        "lawsuit",
        "product failure",
        "outage",
        "key person",
        "nclt",
        "gst notice",
        "labor dispute",
        "insolvency",
        "bankrupt",
        "wind down",
    ],
    SkillName.LEGAL: [
        "legal",
        "patent",
        "patents",
        "file patent",
        "trademark",
        "contract",
        "nda",
        "gdpr",
        "dpdp",
        "incorporation",
        "fema",
        "ip",
        "intellectual property",
        "compliance",
        "regulatory",
        "companies act",
        "employment agreement",
        "founders agreement",
        "shareholder",
        "equity",
        "409a",
    ],
    SkillName.GTM: [
        "gtm",
        "go-to-market",
        "pricing",
        "sales",
        "cac",
        "ltv",
        "plg",
        "enterprise",
        "channel",
        "whatsapp",
        "upi",
        "gem",
        "market",
        "icp",
        "customer acquisition",
        "revenue ops",
        "product-led",
        "sales-led",
        "d2c",
        "saas",
        "b2b",
        "b2c",
    ],
    SkillName.TALENT: [
        "hiring",
        "esop scheme",
        "esop pool",
        "employee stock",
        "stock option",
        "option pool",
        "esop",
        "vesting",
        "okr",
        "retention",
        "layoff",
        "labour code",
        "labor code",
        "salary",
        "compensation",
        "org design",
        "org chart",
        "performance",
        "firing",
        "onboarding",
        "culture",
        "team",
        "recruit",
    ],
    SkillName.RESILIENCE: [
        "burnout",
        "stressed",
        "stress",
        "overwhelmed",
        "decision fatigue",
        "imposter syndrome",
        "lonely",
        "mental health",
        "wellbeing",
        "anxiety",
        "depression",
        "peak performance",
        "mindfulness",
        "founder health",
        "sleep",
        "exercise",
        "therapy",
    ],
    SkillName.OPS: [
        "operations",
        "sop",
        "kpi",
        "vendor",
        "supply chain",
        "gst",
        "tds",
        "fssai",
        "factory",
        "process",
        "metrics",
        "dashboard",
        "automation",
        "workflow",
        "ops stack",
        "finance ops",
        "accounting",
    ],
    SkillName.GOVERNANCE: [
        "board",
        "governance",
        "soc2",
        "iso",
        "esg",
        "companies act",
        "mca",
        "sebi lodr",
        "csr",
        "audit",
        "compliance",
        "director",
        "agm",
        "egm",
        "annual report",
        "statutory",
        "fiduciary",
    ],
}

# Multi-skill chains for common compound situations
_CHAIN_PATTERNS: list[tuple[list[str], list[SkillName]]] = [
    (
        ["series a", "raise"],
        [SkillName.FUNDRAISING, SkillName.LEGAL, SkillName.GOVERNANCE],
    ),
    (
        ["co-founder", "leave", "quit", "conflict"],
        [SkillName.CRISIS, SkillName.LEGAL, SkillName.RESILIENCE],
    ),
    (
        ["data breach", "breach"],
        [SkillName.CRISIS, SkillName.LEGAL],
    ),
    (
        ["esop", "stock option", "option pool"],
        [SkillName.TALENT, SkillName.LEGAL],
    ),
    (
        ["india market", "india launch", "enter india"],
        [SkillName.GTM, SkillName.OPS, SkillName.GOVERNANCE],
    ),
    (
        ["board prep", "board meeting"],
        [SkillName.GOVERNANCE, SkillName.FUNDRAISING],
    ),
    (
        ["first hire", "first team", "hire team"],
        [SkillName.TALENT, SkillName.LEGAL, SkillName.OPS],
    ),
]


def _normalize(text: str) -> str:
    """Lowercase, strip extra whitespace, remove punctuation for matching."""
    text = text.lower()
    text = re.sub(r"[^\w\s\-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _score_skill(text: str, triggers: list[str]) -> tuple[float, list[str]]:
    """
    Score how well text matches a skill's triggers.

    Returns (score, matched_keywords). Score is proportional to the number
    and specificity of matched keywords.

    Single-word triggers use word-boundary matching to avoid substring false
    positives (e.g. "sop" matching inside "esop"). Multi-word triggers use
    substring matching.
    """
    matched: list[str] = []
    for trigger in triggers:
        words = trigger.split()
        if len(words) == 1:
            # Word-boundary match for single tokens
            pattern = r"\b" + re.escape(trigger) + r"\b"
            if re.search(pattern, text):
                matched.append(trigger)
        else:
            # Phrase match for multi-word triggers
            if trigger in text:
                matched.append(trigger)
    if not matched:
        return 0.0, []
    # Longer keyword matches are more specific — weight them higher
    weight = sum(len(kw.split()) for kw in matched)
    score = weight / max(1, len(triggers))
    return score, matched


def dispatch(
    message: str,
    *,
    max_secondary: int = 2,
    min_confidence: float = 0.0,
) -> DispatchResult | None:
    """
    Dispatch a natural-language founder message to the appropriate skill(s).

    Args:
        message: The raw founder message or query.
        max_secondary: Maximum number of secondary skills to include.
        min_confidence: Minimum confidence score (0.0-1.0) to return a result.

    Returns:
        DispatchResult with primary skill and optional chain, or None if no
        skill matches above min_confidence.

    Raises:
        ValueError: If message is empty or None.
        TypeError: If message is not a string.
    """
    if not isinstance(message, str):
        raise TypeError(f"message must be a str, got {type(message).__name__}")
    message = message.strip()
    if not message:
        raise ValueError("message must not be empty")

    # Truncate extremely long messages to avoid regex backtracking issues
    text = _normalize(message[:4096])

    # Check chain patterns first (multi-skill compound situations)
    for keywords, skill_chain in _CHAIN_PATTERNS:
        if all(kw in text for kw in keywords):
            primary = skill_chain[0]
            secondary = skill_chain[1 : max_secondary + 1]
            matched = [kw for kw in keywords if kw in text]
            chain_confidence = 0.9
            if chain_confidence < min_confidence:
                continue
            return DispatchResult(
                primary_skill=primary,
                secondary_skills=secondary,
                confidence=chain_confidence,
                reasoning=f"Chain pattern matched: {keywords}",
                matched_keywords=matched,
            )

    # Score all skills
    scores: dict[SkillName, tuple[float, list[str]]] = {}
    for skill, triggers in _SKILL_TRIGGERS.items():
        score, matched = _score_skill(text, triggers)
        if score > 0:
            scores[skill] = (score, matched)

    if not scores:
        return None

    # Sort by descending score
    ranked = sorted(scores.items(), key=lambda x: x[1][0], reverse=True)
    top_skill, (top_score, top_matched) = ranked[0]

    # Normalise confidence to 0-1 range (cap at 1.0)
    confidence = min(1.0, top_score * 3)

    if confidence < min_confidence:
        return None

    # Include secondary skills (different from primary, above threshold)
    secondary: list[SkillName] = []
    for skill, (score, _) in ranked[1:]:
        if len(secondary) >= max_secondary:
            break
        if score > 0:
            secondary.append(skill)

    return DispatchResult(
        primary_skill=top_skill,
        secondary_skills=secondary,
        confidence=round(confidence, 3),
        reasoning=f"Keyword match: {top_matched[:5]}",
        matched_keywords=top_matched,
    )
