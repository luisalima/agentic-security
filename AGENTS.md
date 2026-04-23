# AGENTS.md

## Project overview

Agentic Security is a learning and implementation reference for securing AI agents against prompt injection. It provides runnable defense patterns, a benchmark, and documentation.

## Environment

- **Python:** ≥3.10
- **Package manager:** `uv` (always use `uv run` to run commands)
- **Testing:** `uv run pytest`
- **Linting:** `uv run ruff check src/ tests/`
- **Docs:** `uv run mkdocs serve` (MkDocs Material)
- **Notebooks:** `uv run marimo edit notebooks/<path>.py`

## Key commands

```bash
# Install dependencies
uv sync

# Run all tests
uv run pytest

# Run tests for a specific module
uv run pytest tests/test_mcp_security.py -v

# Lint
uv run ruff check src/ tests/

# Auto-fix lint issues
uv run ruff check src/ tests/ --fix

# Run benchmark
uv run python benchmark/run.py

# Build docs
uv run mkdocs build --strict

# Serve docs locally
uv run mkdocs serve
```

## Project structure

```
src/agentic_security/
├── defenses/          # Defense implementations (YARA, dual LLM, CaMeL, MCP, memory, etc.)
├── attacks/           # Attack simulations (multi-agent scenarios)
├── llm.py             # LLM client abstraction (OpenAI, Anthropic, Ollama, Mock)
└── scenario.py        # Email assistant scenario for testing

tests/                 # One test file per defense module
notebooks/             # Marimo interactive notebooks (numbered by defense level)
docs/                  # MkDocs site (guide pages + reference docs)
benchmark/             # Comparative defense benchmark
data/                  # Curated injection dataset
```

## Conventions

- **Code style:** Ruff with line length 100, target Python 3.10
- **Type hints:** Use `from __future__ import annotations` and modern syntax (`list[str]`, `dict[str, str]`, `X | None`)
- **Data classes:** Use `@dataclass` for simple data, `pydantic.BaseModel` for validated models
- **Docstrings:** Module-level docstrings explaining purpose and attack vectors addressed. Function docstrings with Args/Returns.
- **Tests:** No LLM calls — all tests use `MockClient` or deterministic logic. Tests should pass without API keys.
- **Notebooks:** Marimo format (`.py` files). Import from `src/agentic_security/`.
- **Line length exceptions:** Notebooks, prompt templates, and injection test strings are intentionally long (configured in `pyproject.toml` per-file ignores).

## Adding a new defense

1. Create `src/agentic_security/defenses/<name>.py`
2. Create `tests/test_<name>.py` with deterministic tests
3. Add to `src/agentic_security/defenses/__init__.py`
4. Add a benchmark adapter in `benchmark/run.py` if it has a `detect(text) -> bool` interface
5. Create a guide page at `docs/guide/<name>.md` and add to `mkdocs.yml` nav
6. Optionally create a marimo notebook in the appropriate `notebooks/` subdirectory

## Important notes

- Never use `pip install` — use `uv sync` or `uv add`
- Never commit API keys or secrets
- All defenses should work without network access (deterministic/mock by default)
- The benchmark runs all deterministic defenses — no LLM calls
- After completing a discrete step, commit and push the scoped changes unless the user says otherwise
