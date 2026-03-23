# AGENTS.md — Autonomous Development Protocol

This file documents the Edgecraft autonomous development protocol used to
evolve the `founder-arsenal` repository from a pure-documentation skill pack
into a tested, hardened, and production-ready Python package.

## Protocol: Edgecraft v1.0

Edgecraft is a 8-cycle autonomous improvement protocol executed by a Claude
agent. Each cycle follows the RALF feedback loop:
**detect → hypothesize → act → ground → propagate**.

### Layer Prefix Convention

Every commit message starts with an Edgecraft layer prefix:

| Prefix | Meaning |
|--------|---------|
| `L0/attention:` | Signal that something requires attention |
| `L1/detection:` | Identify a gap, problem, or 0-coverage area |
| `L2/noise:` | Filter false positives, log scan results |
| `L3/sub-noise:` | Document edge cases or hypothesis findings |
| `L4/conjecture:` | State a hypothesis before measuring |
| `L5/action:` | Commit that implements a concrete change |
| `L6/grounding:` | Validate with measurements / test results |
| `L7/flywheel:` | Identify patterns applicable to other repos |

### The 8 Cycles

| Cycle | Name | Outcome |
|-------|------|---------|
| 1 | Test Coverage | 0% → 96.55% coverage, 269 tests |
| 2 | Error Hardening | Retry logic, input validation, sanitization |
| 3 | Performance | asyncio.gather parallel engine |
| 4 | Security | Secret scan, .gitignore, .env.example |
| 5 | CI/CD | GitHub Actions + pre-commit hooks |
| 6 | Property-Based Testing | 20 Hypothesis tests, 2 edge cases fixed |
| 7 | Examples + Docs | 3 working example scripts |
| 8 | Release Engineering | pyproject.toml, Makefile, CHANGELOG, tags |

## Running the Protocol

The Edgecraft Protocol is designed to be executed by an AI agent (Claude)
with access to bash, file read/write, and GitHub. The agent:

1. Explores the repo to understand structure and gaps
2. Implements changes in each cycle
3. Runs tests and fixes failures before committing
4. Pushes after each cycle for CI validation

## Agent Configuration

- **Model**: Claude Sonnet (Anthropic)
- **Tools**: bash, file operations, git
- **Commit identity**: admin@techknowmad.ai / TechKnowMad Labs
- **Test gate**: All tests must pass before any commit

## Adding New Cycles

To add a new improvement cycle, create a new section in EVOLUTION.md,
implement the changes, run `make test` to verify, and commit with the
appropriate `L5/action:` → `L6/grounding:` pair.
