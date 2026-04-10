# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- **MCP security defenses** (`src/agentic_security/defenses/mcp_security.py`): tool description poisoning detection, rug pull detection, MCP config scanning
- **Memory poisoning defenses** (`src/agentic_security/defenses/memory_security.py`): memory guard with namespace isolation, provenance tracking, TTL expiration
- **8 new tools** in tools landscape: DeepTeam, Guardrails AI, OpenAI Guardrails, MCP-Scan, Docker MCP Gateway, Agentic Radar, Giskard, Invariant Guardrails
- **8 new attack vectors** in attack taxonomy: tool description poisoning, memory poisoning, rug pulls, second-order injection, cascading failures, identity abuse, encoding attacks, slopsquatting
- **OWASP Agentic Top 10 (2026)** mapping in attack taxonomy
- **14 new dataset samples**: multilingual injections (FR, DE, JA, ES, RU), MCP tool poisoning, memory poisoning, second-order injection, supply chain attacks
- **New dataset categories**: tool_poisoning, memory_poisoning, second_order, supply_chain

### Updated
- Attack taxonomy aligned with OWASP Top 10 for Agentic Applications (2026)
- Tools landscape: Lakera Guard (acquired by Check Point Sep 2025), Protect AI/LLM Guard (acquired by Palo Alto Networks Jul 2025)
- References updated across README.md, PRINCIPLES.md, docs/reference/references.md with 2025-2026 research, standards, and real-world incidents
- MCP & Agentic Security Tools section added to tools reference

## [0.1.0] — Unreleased

### Added

- **Defense modules** (`src/agentic_security/defenses/`):
  YARA detection, vector similarity, ML classifier, canary tokens,
  delimiters (Spotlighting), XML tagging, dual LLM, typed extraction,
  dry-run evaluation, output validation
- **Test suite** — 141 tests covering all defense modules
- **Benchmark** — Comparative defense evaluation (`benchmark/run.py`)
  with rich table and JSON output
- **Notebooks** — Interactive Marimo notebooks for every defense level
  (0–5) including vulnerabilities, detection, prompt engineering,
  secure architecture, defense in depth, and framework integration
- **Guide** — Markdown exports of all notebooks (`guide/`)
- **Documentation**: ATTACK_TAXONOMY, THREAT_MODEL, ARCHITECTURE, TOOLS comparison,
  CHEATSHEET, TRADEOFFS, REFERENCES, ROADMAP
- **PRINCIPLES.md** — Core axioms and mental model for agentic security
- **Evaluation dataset** — 70 curated samples (50 injection, 20 legitimate)
  across 14 categories (`data/injection_dataset.json`)
- **CI pipeline** — GitHub Actions: lint, format, test, benchmark smoke test
- **CONTRIBUTING.md** — Guide for contributors

### Infrastructure

- `uv` for dependency management with lockfile
- `ruff` for linting and formatting
- `pytest` for testing
- Marimo for interactive notebooks
