# Founder Arsenal

The unified founder operating system for TechKnowmad AI. 8 integrated skills covering every domain of startup operations — from fundraising to crisis management, legal/IP to go-to-market, talent to governance.

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

## Structure

```
founder-arsenal/
├── SKILL.md                    # Root dispatcher
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE
├── skills/
│   ├── fundraising-command-center/
│   ├── crisis-war-room/
│   ├── legal-ip-fortress/
│   ├── gtm-revenue-engine/
│   ├── talent-os/
│   ├── founder-resilience/
│   ├── ops-scale-engine/
│   └── governance-compliance-shield/
└── reference/
    ├── capital-instruments.md
    ├── india-foundations-directory.md
    ├── india-fundraising-stack.md
    ├── india-govt-schemes-master.md
    ├── india-sector-grants.md
    ├── investor-psychology.md
    └── valuation-benchmarks.md
```

## Usage

Load `SKILL.md` as a Claude Code skill. The dispatcher routes to the right sub-skill automatically based on your message. No manual skill selection needed.

**Examples:**
- "Help me prepare for a Series A" → fundraising-command-center
- "Co-founder wants to leave" → crisis-war-room → legal-ip-fortress
- "Design our ESOP scheme" → talent-os → legal-ip-fortress
- "We had a data breach" → crisis-war-room → legal-ip-fortress
- "Enter the India market" → gtm-revenue-engine → ops-scale-engine

## Requirements

- Claude Code with skills support
- Python 3.12 / Node 22 (for any tooling scripts)

## License

MIT — see [LICENSE](LICENSE)
