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

Don't want to run code? Read the [exported markdown guide](guide/index.md).

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
├── guide/                       # Markdown exports (for reading)
├── docs/
│   ├── TOOLS.md                 # Library comparison
│   ├── ATTACK_TAXONOMY.md       # Attack vectors & risk matrix
│   ├── THREAT_MODEL.md          # How to threat-model your agent
│   └── CHEATSHEET.md            # One-page quick reference
├── diagrams/                    # Excalidraw visuals
└── src/agentic_security/        # Supporting code
```

---

## Learning Path

### Understand the Problem
→ [notebooks_securing_guide/0_vulnerabilities/](notebooks_securing_guide/0_vulnerabilities/) — See how easily an agent can be hijacked
- `1_baseline.py` — Single-turn indirect prompt injection
- `2_multi_turn_attacks.py` — Crescendo, context stuffing, many-shot
- `3_multi_agent_attacks.py` — RAG poisoning, delegation attacks, plugin supply-chain
- `4_case_studies.py` — Real-world incidents: Clinejection, Bing/Sydney, EchoLeak

### Level 1: Detection
→ [notebooks_securing_guide/1_detection/](notebooks_securing_guide/1_detection/)
- `1_yara_detection.py` — Fast pattern matching
- `2_vector_similarity.py` — Semantic similarity search
- `3_ml_classifier.py` — Neural network classification
- `4_llm_as_judge.py` — LLM evaluating for injection
- `5_canary_tokens.py` — Detect prompt leakage

### Level 2: Prompt Engineering  
→ [notebooks_securing_guide/2_prompt_engineering/](notebooks_securing_guide/2_prompt_engineering/)
- `1_delimiters.py` — Random token boundaries (Spotlighting)
- `2_system_prompt_hardening.py` — Role anchoring, explicit negatives
- `3_instruction_hierarchy.py` — Priority framing (system > user > data)
- `4_sandwich_defense.py` — Repeat instructions after untrusted content
- `5_xml_tagging.py` — Structured prompts with semantic XML tags

### Level 3: Isolation (Infra-Level)
→ [notebooks_securing_guide/3_isolation_infra_level/](notebooks_securing_guide/3_isolation_infra_level/)
- `overview.py` — Containers, VMs, network isolation, least privilege, kill switches

### Level 4: Secure Architecture (Software)
→ [notebooks_securing_guide/4_secure_architecture_software/](notebooks_securing_guide/4_secure_architecture_software/)
- `1_dual_llm.py` — Quarantined + Privileged separation
- `2_typed_extraction.py` — Schema as firewall
- `3_dry_run.py` — Plan → Evaluate → Execute
- `4_tool_validation.py` — MCP/tool manifest validation
- `5_camel.py` — CaMeL capability-based security

### Level 5: Defense in Depth
→ [notebooks_securing_guide/5_defense_in_depth/](notebooks_securing_guide/5_defense_in_depth/)
- `combined.py` — All techniques layered together

### Framework Integration
→ [notebooks_securing_guide/6_integration/](notebooks_securing_guide/6_integration/)
- `langchain_integration.py` — Securing LangChain agents
- `pydantic_ai_integration.py` — Securing Pydantic AI agents

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
