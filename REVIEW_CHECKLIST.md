# Review Checklist

Tracking the file-by-file review for v0.1.0 release. Each batch is a chunk of files reviewed together; files within a batch roll up to a single tick when all items are addressed. Detailed item-by-item feedback lives in [FEEDBACK.md](FEEDBACK.md). Pre-release tasks (not file reviews) are tracked separately at the bottom.

---

## Publish-readiness punch list (cleared 2026-05-04)

All items resolved before the file-by-file review began: CI green, metadata complete, community files (`SECURITY.md`, `CODE_OF_CONDUCT.md`, issue/PR templates), repo hygiene, `CHANGELOG.md` versioning, docs workflow. Full detail in git history.

---

## File-by-file review

### Batch A — mkdocs front pages ✅

`docs/index.md`, `docs/principles.md`. Reviewed and applied. Key decisions: locked deployment-vs-curriculum order distinction; added Supporting Systems grid for MCP + Memory; collapsed `principles.md` §4 to a teaser pointing at `guide/7`. See [FEEDBACK.md](FEEDBACK.md) Batch A.

### Batch B — mkdocs reference layer ⏳

`docs/reference/{tools, attack_taxonomy, threat_model, cheatsheet, architecture, tradeoffs, references}.md`. Reviewed and applied. Key changes: canonical Lethal Trifecta wording locked across 5 files; `architecture.md` restructured (270 → 80 lines, "Defense Tiers" renamed to "Maturity Levels", Symbolic References moved to `guide/4`); `tradeoffs.md` recommendation rewritten to not endorse Dual LLM as the baseline; `tools.md` Framework Security Stance table verified against live docs (May 2026); LLM Guard URL fixed across 4 files. See [FEEDBACK.md](FEEDBACK.md) Batch B.

**Reopened 2026-05-20** — `tools.md` had a second pass: per-tool freshness audit (17 parallel agents) + landscape expansion. Quick-ref grew from 22 → 43 entries; new full sections for AgentDojo, Bishop Fox AIMap, Cloudflare Firewall for AI, Cisco AI Defense, HiddenLayer AISec, Wiz AI-SPM, Straiker; new top-level "AI Gateways & Firewalls" section covering 11 more commercial vendors; Vigil/Rebuff demoted to a "Historical / archived detectors" subsection. Material API/CLI corrections to LLM Guard, Promptfoo, Garak, Augustus, PyRIT (repo + Orchestrator→Attack rename), DeepTeam, NeMo, Invariant, Agentic Radar. MCP-Scan rebranded to Snyk Agent-Scan (Snyk acquired Invariant Labs). Meta Prompt Guard upgraded to Llama Prompt Guard 2. Guardrails AI dedicated section removed — vendor pivoted to Snowglobe synthetic data. Needs a re-read before re-ticking.

### Batch C — Guide chapters: foundations ⏳

- [ ] `docs/guide/0_vulnerabilities.md`
- [ ] `docs/guide/1_detection.md`
- [ ] `docs/guide/1b_observability.md`
- [ ] `docs/guide/2_prompt_engineering.md`
- [ ] `docs/guide/3_isolation.md`

### Batch D — Guide chapters: architecture & tail ⏳

- [ ] `docs/guide/4_secure_architecture.md` (sanity-check the Symbolic References section added in Batch B)
- [ ] `docs/guide/5_defense_in_depth.md`
- [ ] `docs/guide/6_integration.md`
- [ ] `docs/guide/7_securing_prepackaged_agents.md` (sanity-check the table updates ported in Batch B)
- [ ] `docs/guide/8_enterprise_zero_trust.md`
- [ ] `docs/guide/9_mcp_security.md` (new — extra correctness attention)
- [ ] `docs/guide/10_memory_security.md` (new — extra correctness attention)

### Batch E — GitHub-facing surfaces ⏳

- [ ] `README.md`
- [ ] `CHANGELOG.md`
- [ ] `CONTRIBUTING.md`
- [ ] `SECURITY.md`
- [ ] `CODE_OF_CONDUCT.md`

### Batch F — Notebooks: vulnerabilities + detection ⏳

- [ ] `notebooks/0_vulnerabilities/` (4 files)
- [ ] `notebooks/1_detection/` (6 files)

### Batch G — Notebooks: prompt engineering + secure architecture ⏳

- [ ] `notebooks/2_prompt_engineering/` (6 files)
- [ ] `notebooks/4_secure_architecture_software/` (8 files, incl. new MCP + memory)

### Batch H — Notebooks: isolation + defense-in-depth + integration ⏳

- [ ] `notebooks/3_isolation_infra_level/` (1 file)
- [ ] `notebooks/5_defense_in_depth/` (2 files)
- [ ] `notebooks/6_integration/` (3 files)

### Batch I — Source code ⏳

- [ ] `src/agentic_security/defenses/` (14 files)
- [ ] `src/agentic_security/attacks/multi_agent.py`
- [ ] `src/agentic_security/llm.py`, `src/agentic_security/scenario.py`

### Batch J — Tests + data + benchmark ⏳

- [ ] `tests/` (14 files)
- [ ] `data/injection_dataset.json`
- [ ] `benchmark/run.py`

### Batch K — Config, tooling, final sweep ⏳

- [ ] `mkdocs.yml`, `pyproject.toml`, `.gitignore`
- [ ] `.github/workflows/{ci,docs}.yml`
- [ ] Pre-release tasks (see below) — apply during this batch
- [ ] Final cross-cutting consistency + link sweep across the whole site

---

## Pre-release tasks (not file reviews)

Separate from the file-by-file review. Apply during Batch K.

- [ ] **Lockfile compliance in CI.** Switch `uv sync --dev` → `uv sync --locked --dev` in `.github/workflows/ci.yml` so CI fails on lockfile drift.
- [ ] **Tighten floor versions in `pyproject.toml`.** Lower bounds are 2023-vintage (`openai>=1.0.0`, `anthropic>=0.18.0`, `pydantic>=2.0.0`).
- [ ] **Supply-chain audit in CI.** Add `pip-audit` step (or equivalent).
- [ ] **Dependabot / Renovate config.** Add `.github/dependabot.yml` for `pip` + `github-actions`.
- [ ] **Static type checker.** Add `mypy` (or `pyright`) to dev deps; configure in `pyproject.toml`; run in CI; fix what it flags in `src/`.
- [ ] **(Optional) Expand ruff rules.** Currently `E`, `F`, `I`, `W`. Consider adding `S` (security), `B` (bugbear), `UP` (pyupgrade), `N` (naming), `RUF`.
- [ ] **Soften security-disclosure framing.** Collapse `CONTRIBUTING.md:181-185` to a one-liner; loosen `SECURITY.md` (5-business-day SLA, 30-day window) to match the educational-repo scope it already declares.
- [ ] **External URL sweep.** Verify links across `README.md`, `docs/`, `CONTRIBUTING.md`, `SECURITY.md`, `pyproject.toml`. Optional: wire a link checker (`lychee` / `markdown-link-check`) into CI.
