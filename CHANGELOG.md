# Changelog

All notable changes to Founder Arsenal are documented here.

Format: `## [version] — YYYY-MM-DD`

---

## [0.1.0] — 2026-03-23

### Cycle 1 — Test Coverage (0% → 96.55%)
- Added Python package: `src/` with 9 modules (dispatcher, crisis, fundraising, talent, gtm, governance, ops, resilience, models)
- 269 unit tests across 7 test files — all passing
- 96.55% test coverage (min per-module: 90%)

### Cycle 2 — Error Hardening
- Added `src/utils.py`: retry_with_backoff (3 retries, exponential backoff), sanitize_string, sanitize_positive_float, truncate_for_processing
- 41 new tests for error paths: None, empty, NaN, Inf, oversized inputs
- All 310 tests passing after hardening

### Cycle 3 — Performance
- Added `src/parallel.py`: asyncio.gather + semaphore parallel batch engine
- `batch_dispatch()`, `batch_assess_runway()` for concurrent multi-analysis
- `time_sequential()` / `time_parallel()` for benchmarking
- 23 new parallel tests

### Cycle 4 — Security
- Scanned all sources: 0 hardcoded secrets, 0 SQL injection, 0 path traversal
- Added `.gitignore` with comprehensive exclusions (secrets, .env, __pycache__)
- Added `.env.example` with API key template

### Cycle 5 — CI/CD
- Added `.github/workflows/ci.yml`: Python 3.12, ruff lint, pytest + coverage on every push/PR
- Added `.pre-commit-config.yaml`: ruff, detect-private-key, no-commit-to-main hooks

### Cycle 6 — Property-Based Testing
- 20 Hypothesis property-based tests across 8 modules
- Found and fixed 2 edge cases: factor overflow (>5.0), LTV:CAC rounding for small values
- Properties verified: score ranges, monotonicity, formula consistency, no crashes

### Cycle 7 — Examples + Docs
- `examples/01_dispatch_founder_query.py` — intent routing demo
- `examples/02_crisis_assessment.py` — crisis severity + runway assessment
- `examples/03_founder_dashboard.py` — full startup health dashboard
- All examples run end-to-end without errors

---

## [1.0.0] — 2026-03-22

### Added
- Root `SKILL.md` dispatcher routing across all 8 skills
- `skills/fundraising-command-center` v2.0.0 — pre-seed through Series D+, India fundraising stack
- `skills/crisis-war-room` — 14 crisis types, war room protocols, India regulatory crisis playbooks
- `skills/legal-ip-fortress` — entity formation, IP strategy, GDPR/DPDP, FEMA, Companies Act
- `skills/gtm-revenue-engine` — GTM, pricing, PLG/SLG, India D2C/SaaS, WhatsApp commerce, GeM
- `skills/talent-os` — hiring, ESOP, OKRs, India Labour Codes, salary benchmarks
- `skills/founder-resilience` — burnout prevention, decision fatigue, peak performance protocols
- `skills/ops-scale-engine` — SOPs, KPIs, GST/TDS, FSSAI, supply chain, India ops stack
- `skills/governance-compliance-shield` — board management, SOC2/ISO/ESG, Companies Act, SEBI LODR
- `reference/capital-instruments.md` — SAFE, CCD, CCPS, convertible notes
- `reference/india-foundations-directory.md` — incubators, accelerators, foundations
- `reference/india-fundraising-stack.md` — India capital playbook
- `reference/india-govt-schemes-master.md` — government schemes with eligibility matrix
- `reference/india-sector-grants.md` — sector-specific grant database
- `reference/investor-psychology.md` — behavioral models for investor engagement
- `reference/valuation-benchmarks.md` — 2025-2026 market comps by stage/sector
- Multi-skill chain documentation for common founder scenarios
