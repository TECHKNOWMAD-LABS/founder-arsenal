---
name: "founder-arsenal"
description: "Unified founder operating system — 8 integrated skills covering fundraising, crisis management, legal/IP, go-to-market, talent, founder resilience, operations scaling, and governance/compliance. Dispatches to the best skill automatically based on intent. Use when a founder needs end-to-end strategic support across any domain of startup operations."
license: MIT
metadata:
  version: 1.0.0
  author: TechKnowmad AI
  category: founder-operations
  domain: startup-os
  updated: 2026-03-22
  skills:
    - fundraising-command-center
    - crisis-war-room
    - legal-ip-fortress
    - gtm-revenue-engine
    - talent-os
    - founder-resilience
    - ops-scale-engine
    - governance-compliance-shield
---

# Founder Arsenal — Dispatcher

The unified founder operating system. 8 battle-tested skills, one entry point. Routes automatically based on intent — no manual skill selection required.

## Skill Registry

| Skill | Triggers | What It Does |
|-------|----------|--------------|
| [fundraising-command-center](skills/fundraising-command-center/SKILL.md) | fundraise, raise, pitch, term sheet, cap table, SAFE, DPIIT, angel tax, VC, investor | Pre-seed → Series D+, IPO, alternative capital, India fundraising stack |
| [crisis-war-room](skills/crisis-war-room/SKILL.md) | crisis, emergency, runway, pivot, shutdown, co-founder conflict, PR disaster, breach | 14 crisis types, war room protocols, stakeholder comms playbooks |
| [legal-ip-fortress](skills/legal-ip-fortress/SKILL.md) | legal, patent, trademark, contract, NDA, GDPR, DPDP, incorporation, FEMA | Entity formation, IP strategy, data privacy, M&A legal readiness |
| [gtm-revenue-engine](skills/gtm-revenue-engine/SKILL.md) | GTM, pricing, sales, CAC, LTV, PLG, enterprise, channel, WhatsApp, UPI, GeM | Market sizing, ICP, revenue ops, India GTM stack |
| [talent-os](skills/talent-os/SKILL.md) | hiring, ESOP, equity, vesting, 409A, OKR, retention, layoff, Labour Codes | Hiring strategy, org design, performance mgmt, India employment law |
| [founder-resilience](skills/founder-resilience/SKILL.md) | burnout, stressed, overwhelmed, decision fatigue, imposter syndrome, lonely | Mental health, cognitive performance, peak performance routines |
| [ops-scale-engine](skills/ops-scale-engine/SKILL.md) | operations, SOP, KPI, vendor, supply chain, GST, TDS, FSSAI, factory | Process design, metrics dashboards, India ops stack |
| [governance-compliance-shield](skills/governance-compliance-shield/SKILL.md) | board, governance, SOC2, ISO, ESG, Companies Act, MCA, SEBI LODR, CSR | Board management, audit readiness, India governance stack |

## Dispatch Logic

```
1. Classify intent from user message
2. Match triggers → select skill
3. Load skills/{skill-name}/SKILL.md
4. Execute with full context
5. Cross-reference reference/ for India-specific data
```

## Multi-Skill Chains

Some situations span multiple skills — chain them:

| Scenario | Chain |
|----------|-------|
| Raising Series A | fundraising-command-center → legal-ip-fortress → governance-compliance-shield |
| Co-founder conflict | crisis-war-room → legal-ip-fortress → founder-resilience |
| Hiring first team | talent-os → legal-ip-fortress → ops-scale-engine |
| Entering India market | gtm-revenue-engine → ops-scale-engine → governance-compliance-shield |
| Board prep | governance-compliance-shield → fundraising-command-center |

## Reference Data

Shared reference materials in `reference/`:
- `capital-instruments.md` — SAFE, CCD, CCPS, convertible notes
- `india-foundations-directory.md` — incubators, accelerators, foundations
- `india-fundraising-stack.md` — end-to-end India capital playbook
- `india-govt-schemes-master.md` — all government schemes with eligibility
- `india-sector-grants.md` — sector-specific grant database
- `investor-psychology.md` — behavioral models for investor engagement
- `valuation-benchmarks.md` — 2025-2026 market comps by stage/sector
