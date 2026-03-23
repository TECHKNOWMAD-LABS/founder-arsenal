#!/usr/bin/env python3
"""
Example 1 — Dispatching founder queries to the right skill.

Shows how to use the auto-dispatch router to route any founder question
to the correct skill (or chain of skills) automatically.

Run with:
    python3 examples/01_dispatch_founder_query.py
"""

import sys
import os

# Allow running from repo root without installing the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.dispatcher import dispatch


def main() -> None:
    """Demonstrate intent dispatch across all 8 founder skills."""
    queries = [
        "Help me prepare for a Series A raise — we're at $2M ARR, B2B SaaS",
        "We're running out of runway — only 2 months of cash left",
        "We had a data breach last night — what do we do?",
        "Design our ESOP scheme for a 12-person team",
        "I'm feeling completely burned out and overwhelmed",
        "Help with our GST filing and operations setup",
        "Preparing for our quarterly board meeting",
        "GTM strategy for entering the India B2B SaaS market",
        "What patents should we file for our AI algorithm?",
    ]

    print("=" * 60)
    print("Founder Arsenal — Intent Dispatcher Demo")
    print("=" * 60)

    for query in queries:
        result = dispatch(query)
        if result is None:
            print(f"\nQuery: {query[:50]}...")
            print("  → No skill matched")
            continue

        print(f"\nQuery: {query[:55]}...")
        print(f"  → Primary:    {result.primary_skill.value}")
        if result.secondary_skills:
            secondary = [s.value for s in result.secondary_skills]
            print(f"     Secondary:  {', '.join(secondary)}")
        print(f"     Confidence: {result.confidence:.0%}")
        print(f"     Keywords:   {result.matched_keywords[:3]}")

    print("\n" + "=" * 60)
    print("Done. Dispatcher successfully routed all queries.")


if __name__ == "__main__":
    main()
