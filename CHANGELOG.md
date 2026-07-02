# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] — Unreleased

### Added

- **Defense modules** (`src/agentic_security/defenses/`):
  YARA detection, vector similarity, ML classifier, canary tokens,
  delimiters (Spotlighting), XML tagging, dual LLM, typed extraction,
  dry-run evaluation, output validation, tool validation, CaMeL
- **MCP security defenses** (`src/agentic_security/defenses/mcp_security.py`):
  tool description poisoning detection, rug pull detection, MCP config scanning
- **Memory poisoning defenses** (`src/agentic_security/defenses/memory_security.py`):
  memory guard with namespace isolation, provenance tracking, TTL expiration
- **Test suite** — 268 tests covering all defense modules
- **Benchmark** — Comparative defense evaluation (`benchmark/run.py`)
  with rich table and JSON output
- **Notebooks** — Interactive Marimo notebooks for every defense level
  (0–6) including vulnerabilities, detection, prompt engineering,
  secure architecture, defense in depth, and framework integration
- **MkDocs site** — Hand-written guide pages and reference docs published as the project guide
- **Reference documentation** (`docs/reference/`): tools landscape,
  attack taxonomy, threat model, cheatsheet, architecture, tradeoffs, references
- **Principles page** (`docs/principles.md`) — Core axioms and mental model for agentic security
- **Evaluation dataset** — 84 curated samples (64 injection, 20 legitimate)
  across 18 categories (`data/injection_dataset.json`), including multilingual
  injections (FR, DE, JA, ES, RU), MCP tool poisoning, memory poisoning,
  second-order injection, and supply-chain attacks
- **OWASP Agentic Top 10 (2026)** mapping in attack taxonomy
- **8 attack vectors** added to taxonomy: tool description poisoning,
  memory poisoning, rug pulls, second-order injection, cascading failures,
  identity abuse, encoding attacks, slopsquatting
- **CI pipeline** — GitHub Actions: lint, format, test, benchmark smoke test
- **Community files** — `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`,
  `.github/ISSUE_TEMPLATE/` (bug report + feature request), `.github/PULL_REQUEST_TEMPLATE.md`

### Updated

- Tools landscape covers 43 entries across detection, red-teaming, guardrails, MCP security, and AI gateways/firewalls — including DeepTeam, OpenAI Guardrails, Snyk Agent-Scan (formerly MCP-Scan), Docker MCP Gateway, Agentic Radar, Giskard, Invariant Guardrails, AgentDojo, Cisco AI Defense, Cloudflare Firewall for AI, HiddenLayer, Wiz AI-SPM, and Bishop Fox AIMap
- Acquisition status: Lakera Guard (Check Point, Sep 2025),
  Protect AI/LLM Guard (Palo Alto Networks, Jul 2025)
- References updated across README.md, docs/principles.md, docs/reference/references.md
  with 2025–2026 research, standards, and real-world incidents
- Anthropic client default bumped to `claude-sonnet-4-6` (was `claude-3-5-sonnet-20241022`)

### Infrastructure

- `uv` for dependency management with lockfile
- `ruff` for linting and formatting
- `pytest` for testing
- Marimo for interactive notebooks
- MkDocs Material for the published guide
