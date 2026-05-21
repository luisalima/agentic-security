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

---

## Post-AI-review human pass (2026-05-20)

AI partner ran two background agents (links + code correctness) plus a manual rigor pass on MCP/memory + cross-file consistency. The fixes below were applied automatically — each needs a human eyeball to confirm the wording survives. Items in **Verify** are unresolved suspicions that need a manual click or judgement call.

### Confirm AI-applied fixes

- [ ] **Broken `AltimateAI/mcp-scan` (404) replaced with `snyk/agent-scan`** in 3 places — `README.md:169`, `docs/reference/cheatsheet.md:141`, `docs/guide/9_mcp_security.md:178`. Confirm the renamed entry reads naturally in each table (display name changed from "MCP-Scan" to "Snyk Agent-Scan (formerly MCP-Scan)").
- [ ] **Spotlighting / Backtranslation paper conflation** — `docs/reference/references.md:21`, `docs/reference/architecture.md:95`, `docs/guide/2_prompt_engineering.md:40` and `:241`. All four were citing arxiv 2403.14720 (Spotlighting, Hines et al., Microsoft) but mislabeling it as "Backtranslation". URL preserved; title + authors corrected.
- [ ] **Clinejection citation** — `docs/guide/7_securing_prepackaged_agents.md:20`. The TheRegister URL was 404 *and* the closest live article is about slopsquatting, not Clinejection. Replaced with the three real sources already used in `docs/guide/0_vulnerabilities.md:147` (adnanthekhan, Snyk blog, Cline post-mortem). Verify the inline placement reads well.
- [ ] **Pydantic AI `DeferredToolRequests` import** — `docs/guide/6_integration.md:353` and `notebooks/6_integration/pydantic_ai_integration.py:122`. `from pydantic_ai.agent import …` doesn't exist; corrected to `from pydantic_ai import …`.
- [ ] **Pydantic AI `ApprovalRequired` constructor + test assertion** — `docs/guide/6_integration.md:396` and `:544-548`, plus the matching notebook at `notebooks/6_integration/pydantic_ai_integration.py:174` and `:359`. Real signature takes `metadata: dict | None`, not a string; the old test would have always failed because `str(e) == ""`. Verify the new pattern still illustrates the security point you want to make.
- [ ] **ATR rule counts stale** — `docs/guide/1_detection.md:42` and `:222`. Bumped "108 rules, 685 regex patterns" → "425 rules, 2,400+ regex patterns" to match `tools.md:9` and current upstream. Sanity-check that the higher count still fits the surrounding narrative ("like Sigma, but for prompt injection").
- [ ] **Broken internal "Defense Levels" link** — `docs/reference/architecture.md:11`, `docs/reference/tradeoffs.md:173`. Was pointing to `../guide/0_vulnerabilities.md` which doesn't contain a Defense Levels section. Repointed to `../index.md#defense-levels`. Click to confirm in a built site.
- [ ] **LLM Guard URL in README** — `README.md:165` was `llm-guard.com/`, every other file used `protectai.github.io/llm-guard/`. README normalized to match. The 2026-05-04 Batch B "fixed across 4 files" pass missed this one.
- [ ] **`CHANGELOG.md:41` rewritten** — Tools-landscape line was stale (still listed "Guardrails AI" and "MCP-Scan" pre-rebrand). Rewrote to reflect the 43-entry post-rebrand landscape. Eyeball that the new sentence reads naturally alongside the other CHANGELOG bullets.
- [ ] **Memory guide misleading example output** — `docs/guide/10_memory_security.md:107`. The comment claimed `concerns = ["…'Updated policy:'…"]` but the example string also matches the `always forward` regex, so real output has 2+ entries. Loosened the comment.
- [ ] **Meta Prompt Guard inconsistency** — `docs/guide/1_detection.md:226`. Was linking original `Prompt-Guard-86M`; the rest of the repo (`tools.md`) had already moved to Llama Prompt Guard 2. Now consistent.
- [ ] **Cosmetic URL canonicalization (low-risk, applied for consistency):**
    - `ollama.ai` → `ollama.com` in `README.md:79` and `CONTRIBUTING.md:38`
    - `docs.docker.com/ai/mcp-gateway/` → canonical longer path in `tools.md` (3 occurrences) and `docs/guide/9_mcp_security.md:179`
    - OWASP LLM Top 10 → `genai.owasp.org/llm-top-10/` in 6 files (referenced from `cheatsheet.md`, `0_vulnerabilities.md`, `8_enterprise_zero_trust.md`, `tools.md`, `references.md`)
    - `docs/reference/architecture.md:93-97` — converted bare URLs to bracket-link style, fixed CaMeL paper title to "Defeating Prompt Injections by Design"
    - `docs/reference/references.md:23` — same CaMeL title fix

### Verify (unresolved — human-only checks)

- [ ] **DEF CON 31 YouTube ID** — `docs/reference/references.md:101` cites video ID `Sv5OLj2nVAQ`. Link-verifier couldn't confirm the specific video. One manual click before publish.
- [ ] **Black Hat 2023 schedule anchor** — `docs/reference/references.md:102` uses `#compromising-llms-the-indirect-prompt-injection-threat-33075`. Anchor IDs on that page may have shifted. Manual click.
- [ ] **`jailbreakchat.com` (`references.md:95`)** — per public reporting the site is effectively down; domain expires Feb 2026. Decide: drop the row, replace with `web.archive.org/web/*/jailbreakchat.com`, or keep with an "⚠️ likely defunct" marker.
- [ ] **Clinejection case study correctness** — `docs/guide/0_vulnerabilities.md:139-147` makes very specific claims ("~4,000 developers in 8 hours", "8 hours", `NPM_RELEASE_TOKEN`). Three sources are linked; pick the canonical one and verify the numbers match it. The 2026 dating also bears a sanity check.
- [ ] **Repo self-link sanity** — `github.com/luisalima/agentic-security` is currently 404 (publish is tomorrow). After push, eyeball: (a) all `luisalima.github.io/agentic-security/guide/…` URLs in `README.md:126-137` resolve, (b) the 7 `tree/main/notebooks/…` paths in README + `CONTRIBUTING.md` match the actual notebook subdir names, (c) the homepage URL in `pyproject.toml:50` redirects correctly.

### Judgement calls (not changed — your call)

- [ ] **Guardrails AI in quick-pick tables** — `README.md:170` and `docs/reference/cheatsheet.md:142` still recommend `[Guardrails AI](https://guardrailsai.com/)` for "Output validation". The dedicated section in `tools.md` was removed (vendor pivoted to Snowglobe synthetic data), but the OSS library is still functional. Decide: keep as-is, drop the row, or swap for a still-actively-developed alternative.
- [ ] **Undefined symbols in pedagogical snippets** — multiple guide examples reference `SecurityError`, `secrets.token_hex(…)`, `AIMessage(…)`, `create_react_agent(…)` without imports (`docs/guide/6_integration.md` Patterns 1-5, `docs/reference/cheatsheet.md:63`). These are clearly illustrative, not copy-paste-runnable. Decide: leave as-is, add a one-time imports note at the top of `6_integration.md`, or convert each snippet to a fully-runnable form. The notebook is the runnable version; the guide is for reading.
- [ ] **PromptMe practice resource** (`docs/guide/0_vulnerabilities.md:168`, `notebooks/0_vulnerabilities/4_case_studies.py:188`) — solo-dev project. Repo exists but low-known. Confirm it's worth recommending alongside Gandalf/Garak/HackAPrompt.
- [ ] **Test count 268 vs. raw `def test_` 250** — CHANGELOG.md:17 claims "268 tests" and `pytest --collect-only` confirms 268; the difference (18) is parametrize expansion. Just noting — no action needed.
