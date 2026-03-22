---
name: "talent-os"
description: "Startup talent management operating system covering hiring strategy, job architecture, interview design, offer negotiation, equity compensation (ESOP/RSU/phantom), vesting schedules, 409A valuation, organizational design, culture building, performance management (OKRs/KPIs), retention strategy, leadership development, layoff management, remote/hybrid team operations, and employer branding. Includes India talent stack covering Indian employment law, Labour Codes 2020, PF/ESI/gratuity, ESOP taxation (Section 17/perquisite), notice period norms, non-compete enforceability, Shops & Establishment Acts, contractor vs employee classification, Indian salary benchmarks, and hiring from Indian talent pools. Use when user mentions hiring, recruit, team, culture, ESOP, equity compensation, vesting, 409A, org design, org chart, performance review, OKR, retention, attrition, layoff, remote team, employer brand, talent, compensation, salary, offer letter, employee, HR, people ops, or any workforce management need."
license: MIT
metadata:
  version: 2.0.0
  author: TechKnowmad AI
  category: talent-management
  domain: people-operations
  updated: 2026-03-22
  frameworks: talent-acquisition, org-design, equity-compensation, performance-management
  data-sources: Carta, Pave, Levels.fyi, Glassdoor, LinkedIn Talent Insights, First Round Capital, a16z, Sequoia Compensation Guide, SHRM, Mercer, Indian ESOP Guidelines, Ministry of Labour India
---

# Talent OS

The startup talent management operating system. Frameworks for building world-class teams from first hire to 500+ — hiring, equity, culture, performance, and organizational design backed by data from Carta, Pave, and top-tier startup research.

## Keywords

hiring, recruit, recruitment, team, team building, culture, ESOP, stock options, equity compensation, RSU, phantom equity, SAR, vesting, cliff, acceleration, 409A, fair market value, org design, organizational structure, org chart, performance review, OKR, KPI, retention, attrition, turnover, layoff, RIF, remote team, hybrid, employer brand, talent, compensation, salary, offer letter, total comp, employee, HR, people ops, people operations, onboarding, offboarding, succession planning, leadership development, executive hiring, CTO hire, VP Engineering, VP Sales, head of product, first hire, employee handbook, PIP, termination, severance, non-compete, non-solicitation, India, PF, ESI, gratuity, labour code, notice period, Indian ESOP

---

## How to Use This Skill

This skill operates in **6 modes**:

| Mode | Trigger | What It Does |
|------|---------|--------------|
| **Plan** | "org design", "who to hire next" | Role prioritization, org chart, headcount planning |
| **Hire** | "hire a CTO", "recruiting" | Job architecture, sourcing, interview design, closing |
| **Compensate** | "equity offer", "salary band" | Comp benchmarks, ESOP design, offer structuring |
| **Develop** | "performance review", "OKRs" | Performance systems, career ladders, feedback |
| **Retain** | "people leaving", "retention" | Retention analysis, engagement, counter-offer strategy |
| **Restructure** | "layoff", "reorg" | Workforce reduction, reorganization, transition |

**Chain with existing skills:**
- `legal-ip-fortress` for employment law and ESOP legal structure
- `crisis-war-room` for talent crisis (exodus, key person loss, layoffs)
- `fundraising-command-center` for equity dilution and ESOP pool impact
- `ops-scale-engine` for scaling team alongside operations

---

## 1. Hiring Priority Framework

### Who to Hire When (Stage-Based)

| Stage | Headcount | Priority Hires | What NOT to Hire |
|-------|-----------|----------------|-----------------|
| **Pre-Seed (2-4)** | Founders only | Technical co-founder if needed | Anyone you can't afford equity |
| **Seed (4-10)** | Core team | 2-3 engineers, 1 designer or PM | VP-level, sales (founders sell) |
| **Post-Seed (10-25)** | Functional leads | First sales hire, ops, customer success | CFO, HR head, C-suite |
| **Series A (25-50)** | Department leads | VP Eng, VP Sales, Head of Product | Large middle management |
| **Series B (50-150)** | Scale team | Director-level, specialized ICs, sales team | Overhead roles before revenue scales |
| **Series C+ (150+)** | Full org | CFO, CHRO, VP Marketing, international | Don't over-hire ahead of revenue |

### First 10 Hires Decision Matrix

| Hire # | Role | Why | What to Look For |
|--------|------|-----|-----------------|
| 1-3 | Engineers (full-stack/backend) | Build the product | Can ship independently, startup mindset |
| 4 | Designer or PM | Product quality + user empathy | Generalist, can wear multiple hats |
| 5-6 | More engineers (specific expertise) | Accelerate development | Domain expertise you lack |
| 7 | First sales/BD (or founder keeps selling) | Revenue | Hunter, not farmer. Can sell without playbook |
| 8 | Customer success/support | Retain customers, gather feedback | Empathetic, technical enough to troubleshoot |
| 9 | Ops/finance generalist | Keep the business running | Can handle legal, finance, HR basics |
| 10 | Marketing or growth | Scale acquisition | Data-driven, can execute not just strategize |

---

## 2. Equity Compensation Framework

### ESOP Pool Sizing by Stage

| Stage | Typical Pool Size | Why |
|-------|------------------|-----|
| Formation | 10-15% | Initial employee option pool |
| Seed | 10-15% (post-money) | Standard, investors expect this |
| Series A | 10-15% (refreshed) | Often topped up pre-close |
| Series B | 10-12% | Refresh + new hire grants |
| Series C+ | 8-10% | Smaller refresh, more targeted |

### Equity Grant Benchmarks (US Market, 2025)

| Role | Seed (% of company) | Series A | Series B |
|------|---------------------|----------|----------|
| VP Engineering | 1.5-3.0% | 0.8-1.5% | 0.4-0.8% |
| VP Sales | 1.0-2.0% | 0.6-1.2% | 0.3-0.6% |
| VP Product | 1.0-2.0% | 0.6-1.2% | 0.3-0.6% |
| Senior Engineer | 0.3-0.8% | 0.15-0.4% | 0.05-0.15% |
| Mid Engineer | 0.1-0.4% | 0.05-0.2% | 0.02-0.08% |
| Junior Engineer | 0.05-0.15% | 0.02-0.08% | 0.01-0.04% |
| First Sales Rep | 0.1-0.3% | 0.05-0.15% | 0.02-0.08% |
| Designer | 0.1-0.4% | 0.05-0.2% | 0.02-0.08% |

### Vesting Structures

| Structure | Standard | When to Use |
|-----------|---------|-------------|
| **4yr / 1yr cliff** | 25% at year 1, then monthly for 3 years | Standard for all employees |
| **4yr / monthly** | No cliff, monthly vesting | Late-stage hires, acqui-hires |
| **3yr / 1yr cliff** | For competitive offers | Recruiting wars |
| **Backloaded (Amazon-style)** | 5/15/40/40 over 4 years | Retention-heavy |
| **Performance vesting** | Tied to milestones | Executives, contingent grants |

### ESOP Taxation Overview

| Jurisdiction | Tax Event 1 | Tax Event 2 | Key Benefit |
|-------------|------------|------------|------------|
| **US (ISO)** | No tax at exercise (AMT may apply) | Capital gains at sale | LTCG if held >1yr post-exercise + 2yr post-grant |
| **US (NSO)** | Ordinary income at exercise | Capital gains at sale | Simpler, no AMT risk |
| **India** | Perquisite tax at exercise (Sec 17(2)) | Capital gains at sale | DPIIT startups: defer perquisite tax 5 years or exit (Sec 80-IAC) |
| **UK (EMI)** | No income tax at exercise | Capital gains at sale (10% Entrepreneurs Relief possible) | Tax-efficient for <250 employees |
| **Singapore** | Taxed at exercise (ordinary income) | No capital gains tax | Simple, no CGT |

### India ESOP Specifics

- **Perquisite tax**: FMV at exercise minus exercise price → taxed as salary income
- **DPIIT startup deferral**: Tax deferred for up to 5 years from exercise OR until sale/exit, whichever is earlier (Section 17(2)(vi))
- **Companies Act 2013**: Section 62(1)(b) governs ESOP issuance — requires special resolution, 1-year minimum vesting
- **ESOP Trust**: Can create ESOP Trust for secondary transactions and buyback
- **Sweat Equity**: Alternative to ESOP under Section 54 — for contribution of IP/know-how
- **FEMA**: Cross-border ESOP (Indian employee, US parent) requires FEMA compliance
- **Buyback**: Company can buy back vested shares under Section 68 (subject to conditions)

---

## 3. Organizational Design

### Org Structure Evolution

| Stage | Structure | Reporting | Key Principle |
|-------|----------|-----------|--------------|
| **2-10** | Flat | Everyone to CEO | No hierarchy needed |
| **10-25** | Functional pods | Engineers → tech lead, Sales → CEO | First layer of management |
| **25-50** | Functional departments | VPs → CEO | Hire department heads |
| **50-150** | Divisional or matrix | Directors → VPs → CEO/COO | Add middle management carefully |
| **150-500** | Business units or squads | Spotify model, Bezos two-pizza teams | Preserve startup speed |
| **500+** | Scaled enterprise | Full hierarchy | Don't lose culture |

### Span of Control Guidelines

| Manager Level | Ideal Direct Reports | Maximum |
|--------------|---------------------|---------|
| Team Lead (IC + manage) | 3-5 | 7 |
| Manager | 5-8 | 10 |
| Senior Manager | 6-10 | 12 |
| Director | 5-8 managers | 10 |
| VP | 4-7 directors | 8 |

---

## 4. Performance Management

### OKR Framework for Startups

**Structure:**
- Company-level: 3-5 Objectives per quarter, each with 2-4 Key Results
- Team-level: Aligned to company OKRs
- Individual: 60% aligned to team, 40% stretch/personal growth
- Grading: 0.0-1.0 (0.7 is target — means you're stretching enough)

**Common Startup OKR Mistakes:**
- Too many OKRs (>5 objectives = no focus)
- Key results that are tasks, not outcomes
- No check-ins (weekly 15-min review is essential)
- Tying OKRs directly to compensation (kills ambition)
- Setting all OKRs top-down (should be 40-60% bottom-up)

### Performance Review Cadence

| Stage | Formal Reviews | Check-ins | 360 Feedback |
|-------|---------------|-----------|-------------|
| <25 people | Semi-annual | Weekly 1:1 | Annual informal |
| 25-100 | Semi-annual | Bi-weekly 1:1 | Semi-annual |
| 100-500 | Quarterly | Bi-weekly 1:1 | Annual formal |
| 500+ | Quarterly | Weekly 1:1 | Semi-annual formal |

---

## 5. Retention Playbook

### Why Startup Employees Leave (Ranked)

| # | Reason | Prevention |
|---|--------|-----------|
| 1 | **Lack of growth/learning** | Career ladders, stretch assignments, L&D budget |
| 2 | **Bad manager** | Manager training, skip-level 1:1s, 360 feedback |
| 3 | **Compensation below market** | Annual comp review, Pave/Carta benchmarking |
| 4 | **Burnout** | Sustainable pace, PTO enforcement, workload monitoring |
| 5 | **No equity upside** | ESOP refreshes, secondary opportunities, clear exit thesis |
| 6 | **Culture/values misalignment** | Hire for values, fire for values, live them visibly |
| 7 | **Better offer** | Counter-offer framework (but address root cause) |
| 8 | **Lack of autonomy** | Delegate outcomes not tasks, trust by default |

### Retention Cost Calculator

```
Cost of losing an employee =
  Recruiting cost (20-30% of salary for agency, or $5-15K internal)
+ Onboarding cost (3-6 months to full productivity)
+ Lost productivity (2-4 months of gap)
+ Knowledge loss (unquantifiable but real)
+ Team morale impact (others start looking)
= Typically 1.5-2x annual salary total cost
```

---

## 6. India Talent Stack

### India Salary Benchmarks (2025, Annual CTC in INR)

| Role | Early Stage (Seed) | Growth (Series A-B) | Scale (Series C+) |
|------|-------------------|--------------------|--------------------|
| Software Engineer (2-4yr) | 10-18L | 15-30L | 25-50L |
| Senior Engineer (5-8yr) | 18-35L | 30-55L | 45-80L |
| Engineering Manager | 25-45L | 40-70L | 60-1.2Cr |
| Product Manager | 15-30L | 25-50L | 40-80L |
| Designer (UI/UX) | 8-18L | 15-30L | 25-50L |
| Sales (B2B) | 8-15L + variable | 12-25L + variable | 20-40L + variable |
| Data Scientist | 12-25L | 20-45L | 35-70L |

### India Employment Law Essentials

| Compliance | Requirement | Threshold | Penalty |
|-----------|-------------|-----------|---------|
| **EPF** | 12% employer + 12% employee | 20+ employees | Imprisonment + fine |
| **ESI** | 3.25% employer + 0.75% employee | 10+ employees, salary ≤21K | Fine up to 5,000/day |
| **Gratuity** | 15 days salary × years (>5yr service) | 10+ employees | Fine + imprisonment |
| **Professional Tax** | State-specific (INR 200/month max) | All salaried employees | Late fees |
| **Shop & Establishment** | Registration, working hours, leave | All establishments | Varies by state |
| **Sexual Harassment (POSH)** | Internal Complaints Committee | 10+ employees | Fine up to 50,000 |
| **Maternity Benefit** | 26 weeks paid leave | 10+ employees | Fine + imprisonment |

### India Non-Compete Status
- **Non-compete agreements are void** under Section 27, Indian Contract Act 1872
- Only enforceable DURING employment, not post-termination
- **Non-solicitation** clauses are generally enforceable if reasonable
- **Garden leave** (paid non-compete period) may be enforceable
- Focus on NDA and IP protection instead of non-compete

---

## Reference Files

For detailed guides, load:
- [`reference/interview-frameworks.md`](reference/interview-frameworks.md) — Structured interview designs by role
- [`reference/india-employment-compliance.md`](reference/india-employment-compliance.md) — State-by-state Shops & Establishment, PF/ESI details

## Organizational Intelligence Layer

### Swarm Intelligence for Teams

```
STIGMERGY: Indirect coordination through artifacts
  Docs, demos, dashboards = "pheromone trails" guiding others
  No central coordinator needed — coordination emerges
IMPLEMENTATION:
  Define signals (what artifacts coordinate), set evaporation (archive stale docs),
  reinforce success (templates from winning patterns)
```

### Dunbar's Scaling Thresholds

```
5 → Co-founders. Zero process. Everyone talks.
15 → First breakdown. Need standups + async docs.
50 → Sub-teams. Need explicit coordination.
150 → Formal structure + management layers required.
500+ → Fight bureaucracy. Stay simple.
AT EACH THRESHOLD: add rituals, roles, documentation proportionally.
```

### Mission Command for Teams

```
1. Commander's Intent: WHAT + WHY (never HOW)
2. Bounded Autonomy: guardrails (budget, timeline, compliance)
3. Backbrief: team restates in own words
4. Check-ins for AWARENESS, not permission
5. AAR on completion
```

### Team of Teams (McChrystal)

```
Shared Consciousness: open dashboards, transparent OKRs
Empowered Execution: person closest to problem decides
Pod Design: 3-5 person teams in 12-16 person squads
  Specialty + cross-training overlap per member
  Pods ship without external approval
```

### Founder-Market Fit Scoring

```
Domain expertise: >3 years in industry = strong signal
Technical depth: can build v1 = reduced dependency risk
Customer access: knows 50+ potential customers personally
Prior exits: track record of execution

Co-founder compatibility: complementary skills + aligned on timeline/ambition/values
Solo vs co-founder: solo = more equity, slower scale; co-founder = faster, 65% conflict risk
```

### Immune System for Teams

```
INNATE: SOPs, runbooks, automated alerts, circuit breakers
ADAPTIVE: Post-incident playbooks that permanently modify behavior
  "Antigen library" = catalog of past failures + responses
  "Memory cells" = postmortems feeding process improvements
SELF-HEALING: auto-rollback, escalation without human trigger, cross-training
TARGET: 80% reduction in recurring incidents year-over-year
```
