# Roadmap

Prioritized roadmap to make this the de facto learning and implementation reference for agentic security.

---

## Phase 1: Foundation & Credibility (High Impact, Needed First)

### 1.1 Extract testable defense logic from notebooks → `src/`
- Move core defense functions (YARA detection, vector similarity, dual LLM, typed extraction, etc.) into `src/agentic_security/defenses/`
- Notebooks import from `src/` and remain the interactive learning interface
- **Why first:** Everything else (tests, benchmarks, CI) depends on having importable code

### 1.2 Automated test suite
- Test each defense against `INJECTION_VARIANTS` (and future attack datasets)
- Assert that defenses block attacks and pass legitimate inputs
- Gives contributors confidence, proves defenses work, catches regressions
- **Metric:** Each defense has ≥1 test proving it blocks the known attack corpus

### 1.3 Working benchmark
- Replace the `benchmark/run.py` stub with a real comparative benchmark
- Output: technique × attack variant → pass/fail matrix
- **This is the killer feature** — no other repo has a side-by-side defense comparison

### 1.4 CI pipeline (GitHub Actions)
- Lint (`ruff`), test (`pytest`), notebook smoke-run
- Keeps the repo trustworthy as contributions come in

---

## Phase 2: Content Depth (Fill Gaps)

### 2.1 Expand prompt engineering section
- System prompt hardening patterns
- Instruction hierarchy / priority framing
- Sandwich defense (repeat instructions after untrusted content)
- XML tagging patterns (structured prompts)
- Currently the thinnest section (only delimiters)

### 2.2 CaMeL / capability-based security notebook ✅
- Implemented in `src/agentic_security/defenses/camel.py`
- Notebook: `notebooks/4_secure_architecture_software/5_camel.py`
- Guide: `guide/4_secure_architecture_software/5_camel.md`
- Tests: `tests/test_camel.py` (25 tests)

### 2.3 Multi-agent attack scenarios ✅
- RAG poisoning, delegation attacks, plugin supply-chain
- Module: `src/agentic_security/attacks/multi_agent.py`
- Notebook: `notebooks/0_vulnerabilities/3_multi_agent_attacks.py`
- Guide: `guide/0_vulnerabilities/3_multi_agent_attacks.md`
- Tests: `tests/test_multi_agent.py` (30 tests)

### 2.4 MCP / tool-use protocol security
- Tool poisoning attacks (malicious tool descriptions)
- Permission scoping and capability restrictions
- Covers the modern agentic landscape (MCP, OpenAI function calling)

### 2.5 Curated evaluation dataset
- Ship a dataset of injection prompts + expected labels
- Enables users to benchmark their own defenses
- Could live in `data/` or `benchmark/datasets/`

---

## Phase 3: Ecosystem & Reach

### 3.1 More framework integrations
- [x] Pydantic AI — structured output, tool approval, TestModel
- [ ] LlamaIndex (future)
- CrewAI, AutoGen have less traction; deprioritized

### 3.2 Real-world case studies / CTF exercises ✅
- Clinejection, Bing/Sydney, EchoLeak case studies
- CTF resource links (Gandalf, PromptMe, Garak, HackAPrompt)
- Notebook: `notebooks/0_vulnerabilities/4_case_studies.py`
- Guide: `guide/0_vulnerabilities/4_case_studies.md`

### 3.3 CONTRIBUTING.md
- How to add new attacks, defenses, notebooks
- Code style, testing expectations, PR process

---

## Phase 4: Polish

### 4.1 Fix repo hygiene
- [x] Update `pyproject.toml` author placeholder (`"Your Name"`)
- [ ] Export diagrams to SVG (README updated to reference .excalidraw)
- [x] Fix stale notebook paths in `docs/TOOLS.md` (references `patterns/01_delimiter.py` etc.)

### 4.2 Stretch goals
- Translations
- Video walkthroughs
- Interactive hosted demo (e.g., on HuggingFace Spaces)
