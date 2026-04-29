# Roadmap

Prioritized roadmap to make this the de facto learning and implementation reference for agentic security.

---

## Phase 1: Foundation & Credibility ✅

### 1.1 Extract testable defense logic from notebooks → `src/` ✅
- Defense functions live in `src/agentic_security/defenses/` (YARA, vector similarity, dual LLM, typed extraction, ML classifier, canary tokens, delimiters, dry-run, tool validation, CaMeL, output validation, XML tagging)
- Attack simulations in `src/agentic_security/attacks/`
- Notebooks import from `src/`

### 1.2 Automated test suite ✅
- 13 test files in `tests/` covering all defenses and multi-agent attacks
- Each defense tested against injection variants and legitimate inputs

### 1.3 Working benchmark ✅
- `benchmark/run.py` runs all deterministic defenses against the attack corpus
- Outputs technique × attack variant → pass/fail matrix (rich table or JSON)

### 1.4 CI pipeline ✅
- GitHub Actions: lint (`ruff`), test (`pytest`), benchmark smoke test
- Runs on Python 3.10, 3.11, 3.12

---

## Phase 2: Content Depth ✅

### 2.1 Prompt engineering section ✅
- Delimiters, system prompt hardening, instruction hierarchy, sandwich defense, XML tagging
- All in `notebooks/2_prompt_engineering/`

### 2.2 CaMeL / capability-based security ✅
- `src/agentic_security/defenses/camel.py`
- Notebook: `notebooks/4_secure_architecture_software/5_camel.py`

### 2.3 Multi-agent attack scenarios ✅
- RAG poisoning, delegation attacks, plugin supply-chain
- `src/agentic_security/attacks/multi_agent.py`
- Notebook: `notebooks/0_vulnerabilities/3_multi_agent_attacks.py`

### 2.4 MCP / tool-use protocol security ✅
- `src/agentic_security/defenses/tool_validation.py`
- Notebook: `notebooks/4_secure_architecture_software/4_tool_validation.py`

### 2.5 Curated evaluation dataset ✅
- `data/injection_dataset.json`

---

## Phase 2.5: Agentic Security Landscape (2026 Update) ✅

### 2.5.1 OWASP Agentic Top 10 (2026) alignment ✅
- Attack taxonomy updated with 8 new attack vectors (ASI01–ASI10 mapping)
- References updated across README, PRINCIPLES, and docs

### 2.5.2 MCP security defenses ✅
- `src/agentic_security/defenses/mcp_security.py` — tool poisoning detection, rug pull detection, config scanning
- Tests in `tests/test_mcp_security.py`

### 2.5.3 Memory poisoning defenses ✅
- `src/agentic_security/defenses/memory_security.py` — memory guard, namespace isolation, provenance tracking
- Tests in `tests/test_memory_security.py`

### 2.5.4 Tools landscape update ✅
- Added 8 new tools: DeepTeam, Guardrails AI, OpenAI Guardrails, MCP-Scan, Docker MCP Gateway, Agentic Radar, Giskard, Invariant Guardrails
- Updated acquisition status: Lakera (Check Point), Protect AI (Palo Alto Networks)

### 2.5.5 Dataset expansion ✅
- Added multilingual injection samples (French, German, Japanese, Spanish, Russian)
- Added MCP tool poisoning samples
- Added memory poisoning, second-order injection, and supply chain samples
- New categories: tool_poisoning, memory_poisoning, second_order, supply_chain

---

## Phase 3: Docs & Ecosystem (Current)

### 3.1 GitHub Pages site ✅
- MkDocs Material setup complete
- Guide and reference pages written
- Reference docs migrated

### 3.2 Write guide pages ✅
- [x] Vulnerabilities (`docs/guide/0_vulnerabilities.md`)
- [x] Detection (`docs/guide/1_detection.md`)
- [x] Prompt Engineering (`docs/guide/2_prompt_engineering.md`)
- [x] Isolation (`docs/guide/3_isolation.md`)
- [x] Secure Architecture (`docs/guide/4_secure_architecture.md`)
- [x] Defense in Depth (`docs/guide/5_defense_in_depth.md`)
- [x] Framework Integration (`docs/guide/6_integration.md`)
- [x] Securing Pre-Packaged Agents (`docs/guide/7_securing_prepackaged_agents.md`)

### 3.3 More framework integrations
- [x] Pydantic AI
- [x] LangChain
- [ ] LlamaIndex

### 3.4 Remove stale CI job ✅
- [x] Remove `guide-sync` job from `.github/workflows/ci.yml` (was for the old markdown export)
- [x] Remove stale `scripts/` directory (export_guide.py, export_guide.sh, export_diagrams.mjs, node_modules)

---

## Phase 4: Polish

### 4.1 Repo hygiene
- [x] Fix `pyproject.toml` author
- [ ] Export diagrams to SVG from Excalidraw sources
- [x] Fix stale doc paths after `docs/` reorganization

### 4.2 Stretch goals
- [ ] Translations
- [ ] Video walkthroughs
- [ ] Interactive hosted demo (e.g., on HuggingFace Spaces)
