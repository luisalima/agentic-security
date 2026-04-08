# Agentic Security

**The definitive guide to securing AI agents against prompt injection.**

AI agents are vulnerable to prompt injection attacks. This is more concerning since they can take actions and "live" in spaces that can access (and edit) private information. This repository provides practical, runnable examples of defense patterns—from simple detection to secure multi-agent architectures.

> **Start here: [PRINCIPLES.md](PRINCIPLES.md)** — The mental model for agentic security, before you touch any code.

<!-- Diagram: see diagrams/mental_model.excalidraw -->

---

## The Problem

Your AI agent is vulnerable if it has the **Lethal Trifecta**:

1. **Tool Access** — Can take real-world actions
2. **Untrusted Input** — Processes external data (emails, documents, web, RAG)
3. **Sensitive Context** — Has access to credentials, PII, or private data

Unlike traditional injection attacks (SQL injection, XSS), there's no equivalent to parameterized queries for LLMs. Instructions and data flow through the same channel.

---

## Threat Model

Your threat model is simple: **the agent can go rogue.** Ask yourself: *if this agent is fully compromised right now, what's the worst that can happen?*

| Blast Radius | Example | Acceptable? |
|-------------|---------|-------------|
| Agent sends 1 email to wrong person | Scoped token, approval required | Usually yes |
| Agent exfiltrates all contacts | Full contact access, outbound network | Usually no |
| Agent pushes malicious code to prod | Git credentials, CI/CD access | Never |
| Agent deletes database | DB write credentials in env | Never |

**If the blast radius is unacceptable, you need more isolation — not better prompts.**

→ Full threat modeling guide: [docs/reference/threat_model.md](docs/reference/threat_model.md)

---

## Defense Levels

| Level | Approach | What Changes | Protection |
|-------|----------|--------------|------------|
| **1. Detection** | Filter malicious inputs | Add a library | ~95% |
| **2. Prompt Engineering** | Harden the prompt | Change prompts | +marginal |
| **3. Isolation (Infra)** | Containers, network, permissions | Wrap the agent | +significant |
| **4. Secure Architecture (Software)** | Dual LLM, dry-run, typed extraction | Redesign system | +significant |
| **5. Defense in Depth** | Layer everything | Full investment | ~99%* |

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
marimo edit notebooks_securing_guide/0_vulnerabilities/1_baseline.py

# Try a defense pattern
marimo edit notebooks_securing_guide/4_secure_architecture_software/1_dual_llm.py
```

### Read the Guide

Don't want to run code? Read the guide on [GitHub Pages](https://luisalima.github.io/agentic-security/).

---

## Repository Structure

```
agentic-security/
├── notebooks_securing_guide/                   # Interactive Marimo notebooks
│   ├── 0_vulnerabilities/        # The vulnerability
│   ├── 1_detection/             # YARA, vectors, ML, LLM-as-judge, canaries
│   ├── 2_prompt_engineering/    # Delimiters, hardening
│   ├── 3_isolation_infra_level/  # Containers, network, permissions
│   ├── 4_secure_architecture_software/  # Dual LLM, typed extraction, dry-run
│   ├── 5_defense_in_depth/      # Layered defense
│   └── 6_integration/           # LangChain, framework patterns
├── docs/                        # MkDocs site (GitHub Pages)
│   ├── guide/                   # Hand-written guide pages
│   └── reference/               # Tools, attack taxonomy, threat model, etc.
├── diagrams/                    # Excalidraw visuals
└── src/agentic_security/        # Supporting code
```

---

## Learning Path

Read the full guide on [GitHub Pages](https://luisalima.github.io/agentic-security/), or run the interactive notebooks locally with `marimo edit`.

| Level | Guide | Notebooks |
|-------|-------|-----------|
| **0. Vulnerabilities** | [The Problem](https://luisalima.github.io/agentic-security/guide/0_vulnerabilities/) | `notebooks_securing_guide/0_vulnerabilities/` |
| **1. Detection** | [Detection](https://luisalima.github.io/agentic-security/guide/1_detection/) | `notebooks_securing_guide/1_detection/` |
| **2. Prompt Engineering** | [Prompt Engineering](https://luisalima.github.io/agentic-security/guide/2_prompt_engineering/) | `notebooks_securing_guide/2_prompt_engineering/` |
| **3. Isolation (Infra)** | [Isolation](https://luisalima.github.io/agentic-security/guide/3_isolation/) | `notebooks_securing_guide/3_isolation_infra_level/` |
| **4. Secure Architecture** | [Secure Architecture](https://luisalima.github.io/agentic-security/guide/4_secure_architecture/) | `notebooks_securing_guide/4_secure_architecture_software/` |
| **5. Defense in Depth** | [Defense in Depth](https://luisalima.github.io/agentic-security/guide/5_defense_in_depth/) | `notebooks_securing_guide/5_defense_in_depth/` |
| **6. Integration** | [Framework Integration](https://luisalima.github.io/agentic-security/guide/6_integration/) | `notebooks_securing_guide/6_integration/` |

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

See [docs/reference/tools.md](docs/reference/tools.md) for detailed comparison. Quick picks:

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

---

> **Start here: [Principles](PRINCIPLES.md)** — The mental model for agentic security, before you touch any code.
