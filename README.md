# Agentic Security

**The definitive guide to securing AI agents against prompt injection.**

AI agents that can take actions (send emails, execute code, access APIs) are vulnerable to prompt injection attacks. This repository provides practical, runnable examples of defense patterns—from simple detection to secure multi-agent architectures.

![Mental Model](diagrams/mental_model.svg)

---

## The Problem

Your AI agent is vulnerable if it has the **Lethal Trifecta**:

1. **Tool Access** — Can take real-world actions
2. **Untrusted Input** — Processes external data (emails, documents, web, RAG)
3. **Sensitive Context** — Has access to credentials, PII, or private data

Unlike traditional injection attacks (SQL injection, XSS), there's no equivalent to parameterized queries for LLMs. Instructions and data flow through the same channel.

---

## Defense Levels

| Level | Approach | What Changes | Protection |
|-------|----------|--------------|------------|
| **1. Detection** | Filter malicious inputs | Add a library | ~95% |
| **2. Prompt Engineering** | Harden the prompt | Change prompts | +marginal |
| **3. Secure Architecture** | Isolate concerns | Redesign system | +significant |
| **4. Defense in Depth** | Layer everything | Full investment | ~99%* |

*Nothing is 100%. The goal is raising the bar high enough to deter attacks and limit blast radius.

---

## Quick Start

### Prerequisites

```bash
# Clone and setup
git clone https://github.com/luisalima/agentic-security.git
cd agentic-security
python -m venv .venv && source .venv/bin/activate
pip install -e .

# For running notebooks
pip install marimo

# For local LLM testing (optional)
# Install Ollama: https://ollama.ai
ollama pull llama3.1:8b
```

### Run a Notebook

```bash
# See the vulnerability (baseline)
marimo edit notebooks/0_baseline/baseline.py

# Try a defense pattern
marimo edit notebooks/3_secure_architecture/dual_llm.py
```

### Read the Guide

Don't want to run code? Read the [exported markdown guide](guide/index.md).

---

## Repository Structure

```
agentic-security/
├── notebooks/                   # Interactive Marimo notebooks
│   ├── 0_baseline/              # The vulnerability
│   ├── 1_detection/             # YARA, vectors, ML, canaries
│   ├── 2_prompt_engineering/    # Delimiters, hardening
│   ├── 3_secure_architecture/   # Dual LLM, typed extraction, dry-run
│   └── 4_defense_in_depth/      # Layered defense
├── guide/                       # Markdown exports (for reading)
├── docs/
│   ├── TOOLS.md                 # Library comparison
│   ├── THREAT_MODEL.md          # Attack taxonomy
│   └── CHEATSHEET.md            # One-page quick reference
├── diagrams/                    # Excalidraw visuals
└── src/agentic_security/        # Supporting code
```

---

## Learning Path

### Understand the Problem
→ [notebooks/0_baseline/](notebooks/0_baseline/) — See how easily an agent can be hijacked

### Level 1: Detection
→ [notebooks/1_detection/](notebooks/1_detection/)
- `yara_detection.py` — Fast pattern matching
- `vector_similarity.py` — Semantic similarity search
- `ml_classifier.py` — Neural network classification
- `canary_tokens.py` — Detect prompt leakage

### Level 2: Prompt Engineering  
→ [notebooks/2_prompt_engineering/](notebooks/2_prompt_engineering/)
- `delimiters.py` — Random token boundaries (Spotlighting)

### Level 3: Secure Architecture
→ [notebooks/3_secure_architecture/](notebooks/3_secure_architecture/)
- `dual_llm.py` — Quarantined + Privileged separation
- `typed_extraction.py` — Schema as firewall
- `dry_run.py` — Plan → Evaluate → Execute

### Level 4: Defense in Depth
→ [notebooks/4_defense_in_depth/](notebooks/4_defense_in_depth/)
- `combined.py` — All techniques layered together

---

## Key Insights

### What Works

- **Architectural separation** — The privileged LLM never sees raw untrusted content
- **Typed extraction** — A schema with `max_length=50` fields can't carry sophisticated payloads
- **Output validation** — Check what the LLM tries to *do*, not just what it receives
- **Dry-run evaluation** — Generate plans, evaluate them, then execute

### What Doesn't Work

- **"Just add another LLM to check"** — Same vulnerability class
- **Delimiters alone** — Easily bypassed with "ignore the delimiters"
- **Waiting for smarter models** — This is architectural, not an intelligence problem
- **Blocklist keywords** — Trivially rephrased

---

## Tools Landscape

See [docs/TOOLS.md](docs/TOOLS.md) for detailed comparison. Quick picks:

| Need | Tool |
|------|------|
| Quick start, open source | [LLM Guard](https://llm-guard.com/) |
| Self-hosted, multi-layer | [Vigil](https://github.com/deadbits/vigil-llm) |
| Enterprise, managed | [Lakera Guard](https://www.lakera.ai/) |
| Red teaming | [Garak](https://github.com/NVIDIA/garak) |

---

## Contributing

This aims to be **the** resource for agentic AI security. Contributions welcome:

- New attack patterns and defenses
- Framework integration examples (LangChain, LlamaIndex, etc.)
- Improvements to existing notebooks
- Translations

---

## References

- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [Simon Willison's Prompt Injection Series](https://simonwillison.net/series/prompt-injection/)
- [Google DeepMind CaMeL Paper](https://arxiv.org/abs/2503.18813)
- [Microsoft Spotlighting Research](https://arxiv.org/abs/2403.14720)

---

## License

MIT — Use freely, but please link back if this helped you.
