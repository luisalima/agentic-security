# Contributing to Agentic Security Guide

Thanks for your interest in improving the step-by-step guide to securing AI agents against prompt injection. Every contribution matters—whether it's a new defense pattern, a novel attack variant, a typo fix, or a better explanation.

---

## What We're Looking For

| Contribution | Impact |
|--------------|--------|
| New defense patterns | Expands the catalog of practical techniques |
| New attack variants | Stress-tests existing defenses |
| Framework integrations | LangChain, LlamaIndex, PydanticAI, CrewAI, etc. |
| Notebook improvements | Better explanations, clearer examples |
| Documentation fixes | Typos, broken links, clarifications |
| Benchmark improvements | Fairer comparisons, new metrics |

---

## Development Setup

```bash
# Clone the repo
git clone https://github.com/luisalima/agentic-security.git
cd agentic-security

# Install dependencies (requires uv: https://docs.astral.sh/uv/)
uv sync --extra dev

# Activate the virtual environment
source .venv/bin/activate

# Verify everything works
uv run ruff check src/ tests/ benchmark/
uv run pytest tests/ -v --tb=short
```

[Marimo](https://marimo.io/) is included in the project dependencies, so `uv sync --extra dev` is enough to run tests, linting, and notebooks. For local LLM testing, optionally install [Ollama](https://ollama.com/) and pull a model (e.g., `ollama pull llama3.1:8b`).

---

## Project Structure

```
agentic-security/
├── src/agentic_security/
│   ├── defenses/          # Defense modules (yara, vectors, ML, canaries, etc.)
│   ├── scenario.py        # Email scenario + INJECTION_VARIANTS attack corpus
│   └── llm.py             # LLM abstraction layer
├── tests/                 # pytest tests for each defense
├── notebooks/             # Marimo interactive notebooks (by defense level)
├── docs/                  # MkDocs site — guide pages and reference docs (tools, attack taxonomy, threat model, cheatsheet, etc.)
├── benchmark/run.py       # Comparative defense benchmark
└── diagrams/              # Excalidraw diagrams
```

---

## Adding a New Defense Pattern

1. **Create the defense module** in `src/agentic_security/defenses/your_defense.py`.
   - Follow the conventions of existing modules (dataclass results, clear docstrings, a class with a main detection/defense method).
   - Keep it self-contained as deterministic as possible.

2. **Add tests** in `tests/test_your_defense.py`. Every defense test should cover:
   - **Attacks are blocked** — test against relevant `INJECTION_VARIANTS` from `scenario.py`
   - **Legitimate inputs pass through** — parametrize with safe inputs to catch false positives
   - **Edge cases** — empty input, match structure, custom configuration

   See `tests/test_yara_detection.py` for the canonical example.

3. **Optionally add a notebook** in the appropriate `notebooks/<level>/` directory, using Marimo. If you also want a hand-written explainer, add a markdown page under `docs/guide/` and link it from `mkdocs.yml`.

4. **Add a benchmark adapter** in `benchmark/run.py` if the defense is deterministic (no LLM calls).

---

## Adding a New Attack Variant

Add your injection string to `INJECTION_VARIANTS` in `src/agentic_security/scenario.py`:

```python
INJECTION_VARIANTS = [
    # ... existing variants ...
    # Your new variant — describe what technique it uses
    """Your injection payload here""",
]
```

Then run the benchmark to see how existing defenses handle it:

```bash
uv run python benchmark/run.py
```

Update any tests that reference `INJECTION_VARIANTS` by index if needed.

---

## Code Style

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting.

```bash
# Check for lint errors
uv run ruff check src/ tests/ benchmark/

# Auto-fix what's fixable
uv run ruff check --fix src/ tests/ benchmark/

# Check formatting
uv run ruff format --check src/ tests/ benchmark/

# Auto-format
uv run ruff format src/ tests/ benchmark/
```

Key settings (from `pyproject.toml`):

| Setting | Value |
|---------|-------|
| Line length | 100 |
| Target Python | 3.10+ |
| Lint rules | `E`, `F`, `I`, `W` |

Follow the conventions you see in neighboring files—docstrings on modules and classes, type hints, dataclasses for structured results.

---

## Testing

```bash
# Run all tests
uv run pytest tests/ -v --tb=short

# Run a single test file
uv run pytest tests/test_yara_detection.py -v

# Run a specific test
uv run pytest tests/test_yara_detection.py::TestSimpleYaraScanner::test_detects_instruction_bypass -v
```

Every defense should have tests that verify two things:

1. **Security** — known attacks are detected/blocked
2. **Usability** — legitimate inputs are not flagged (false positives)

CI runs tests on Python 3.10, 3.11, 3.12, and 3.13.

---

## Running the Benchmark

```bash
# Rich table output
uv run python benchmark/run.py

# JSON output (used in CI as a smoke test)
uv run python benchmark/run.py --json
```

The benchmark runs all deterministic defenses against the `INJECTION_VARIANTS` corpus and legitimate inputs, producing a technique × variant pass/fail matrix.

---

## Pull Request Process

1. **Fork and branch** — create a feature branch from `main`
2. **Make your changes** — keep PRs focused on one thing
3. **Run the checks locally:**
   ```bash
   uv run ruff check src/ tests/ benchmark/
   uv run ruff format --check src/ tests/ benchmark/
   uv run pytest tests/ -v --tb=short
   ```
4. **Open a PR** — describe what you changed and why
5. **CI must pass** — lint, format, tests, and benchmark smoke test all run automatically

---

## Reporting Security Issues

If you discover a security vulnerability in the defense implementations or infrastructure, please **do not open a public issue**. Follow the disclosure process in [SECURITY.md](SECURITY.md). We'll work with you to understand and address the issue before any public disclosure.

For general bugs or issues with the educational content, regular GitHub issues are fine.

---

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
