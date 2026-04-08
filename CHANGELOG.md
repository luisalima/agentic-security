# Changelog

All notable changes to this project will be documented in this file.

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
