[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](CONTRIBUTING.md)

# Founder Arsenal

Unified founder operating system for TechKnowmad AI. Eight integrated skills covering every domain of startup operations — auto-dispatched from a single entry point.

## Features

- **Auto-dispatch routing** — describe your problem in plain language; the dispatcher routes to the right skill without manual selection
- **Full-stack India coverage** — DPIIT, SEBI, RBI, FEMA, Companies Act 2013, GST, Labour Codes, angel tax, state startup policies for all 28 states
- **Crisis-ready protocols** — 14 crisis types with severity scoring, war room playbooks, and stakeholder communication templates
- **Capital stack coverage** — pre-seed through Series D+, IPO readiness, SAFE/convertible notes, venture debt, SBIR/EIC grants, crowdfunding
- **People + legal in one system** — ESOP/RSU structuring, 409A valuation, patent strategy, GDPR/DPDP compliance, and employment law
- **Reference intelligence** — curated valuation benchmarks, investor psychology, India grants master list, and capital instruments guide

## Skills

| Skill | Domain | Coverage |
|-------|--------|----------|
| [fundraising-command-center](skills/fundraising-command-center/) | Capital | Pre-seed → Series D+, IPO, DPIIT, India grants, alternative capital |
| [crisis-war-room](skills/crisis-war-room/) | Crisis | 14 crisis types, war room protocols, India regulatory crisis |
| [legal-ip-fortress](skills/legal-ip-fortress/) | Legal/IP | Patents, trademarks, contracts, GDPR, DPDP, FEMA, Companies Act |
| [gtm-revenue-engine](skills/gtm-revenue-engine/) | Revenue | GTM, pricing, PLG/SLG, India D2C/SaaS, WhatsApp, GeM |
| [talent-os](skills/talent-os/) | People | Hiring, ESOP, OKRs, Labour Codes, India salary benchmarks |
| [founder-resilience](skills/founder-resilience/) | Wellbeing | Burnout, decision fatigue, peak performance, crisis support |
| [ops-scale-engine](skills/ops-scale-engine/) | Operations | SOPs, KPIs, GST, TDS, FSSAI, supply chain, India ops |
| [governance-compliance-shield](skills/governance-compliance-shield/) | Governance | Board, SOC2, ISO, ESG, Companies Act, MCA, SEBI LODR |

## Quick Start

**Prerequisites:** Claude Code with skills support, Python 3.12 or Node 22.

**Install:**

```bash
git clone https://github.com/techknowmad/founder-arsenal.git
cd founder-arsenal
```

**Load the skill in Claude Code:**

Add `SKILL.md` as a skill in your Claude Code settings, then start a conversation:

```
"Help me prepare for a Series A raise — we're at $800K ARR, B2B SaaS, India-based"
```

The dispatcher reads intent and routes automatically. No manual skill selection required.

**More examples:**

```
"Co-founder wants to leave mid-product-build"
→ crisis-war-room + legal-ip-fortress

"Design our ESOP scheme for a 12-person team"
→ talent-os + legal-ip-fortress

"We had a data breach — what do we do in the next 72 hours?"
→ crisis-war-room + legal-ip-fortress

"Enter the India market from the US"
→ gtm-revenue-engine + ops-scale-engine
```

## Architecture

```
founder-arsenal/
├── SKILL.md                         # Root dispatcher — single entry point
├── skills/
│   ├── fundraising-command-center/  # Capital raising, investor relations
│   ├── crisis-war-room/             # Crisis response, pivot frameworks
│   ├── legal-ip-fortress/           # IP, contracts, regulatory compliance
│   ├── gtm-revenue-engine/          # Go-to-market, pricing, sales ops
│   ├── talent-os/                   # Hiring, compensation, org design
│   ├── founder-resilience/          # Mental health, cognitive performance
│   ├── ops-scale-engine/            # SOPs, metrics, operational scaling
│   └── governance-compliance-shield/ # Board, audit, ESG, governance
└── reference/
    ├── capital-instruments.md        # SAFE, convertible notes, term sheet guide
    ├── india-foundations-directory.md
    ├── india-fundraising-stack.md
    ├── india-govt-schemes-master.md
    ├── india-sector-grants.md
    ├── investor-psychology.md
    └── valuation-benchmarks.md
```

The root `SKILL.md` acts as a dispatcher: it classifies intent from the user's message and forwards to the matching sub-skill. Sub-skills are self-contained and can also be loaded directly.

## Requirements

- Claude Code with skills support
- Python 3.12 / Node 22 (for tooling scripts)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for branch conventions, test requirements, and PR process.

## License

MIT — see [LICENSE](LICENSE)

---

Built by [TechKnowMad Labs](https://techknowmad.ai)
