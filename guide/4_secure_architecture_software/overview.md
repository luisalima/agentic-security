---
title: Overview
marimo-version: 0.16.1
width: medium
---

# Level 3: Secure Agentic Architecture

When detection and prompt engineering aren't enough, you need **architectural separation**.
These patterns fundamentally change how your system handles untrusted content.

## The Core Principle

> **The privileged component should never see raw untrusted content.**

Instead of trying to make one LLM resist manipulation, separate concerns:
- One component processes untrusted data (no tools)
- Another component has tools (never sees raw data)
- A controller validates what flows between them

<!-- DIAGRAM: diagrams/secure_architecture_overview.excalidraw -->

```python {.marimo}
import marimo as mo
```

## The Three Patterns

| Pattern | Key Idea | Complexity | Protection |
|---------|----------|------------|------------|
| **Dual LLM** | Quarantined LLM (no tools) + Privileged LLM (tools, no raw data) | Medium | High |
| **Typed Extraction** | Schema constraints as firewall—payload can't fit | Medium | High |
| **Dry-Run Evaluation** | Plan → Evaluate → Execute with approval | Medium-High | High |

These patterns come from academic research:
- **Dual LLM** — [Simon Willison](https://simonwillison.net/2023/Apr/25/dual-llm-pattern/), 2023
- **Typed Extraction** — [StruQ](https://arxiv.org/abs/2402.06363), 2024
- **Capability-Based** — [Google DeepMind CaMeL](https://arxiv.org/abs/2503.18813), 2025
<!---->
## Why Architecture Matters

**Prompt engineering** tries to make the LLM behave correctly.

**Architecture** makes incorrect behavior impossible (or at least much harder).

```
Prompt Engineering:  "Please don't follow malicious instructions"
                          ↓
                     LLM decides
                          ↓
                     Maybe works?

Architecture:        Untrusted data → Quarantined LLM → Structured data
                                                               ↓
                                          Privileged LLM ← Controller
                                               ↓
                                          Tool execution

                     Payload has no path to reach the tools
```
<!---->
## When to Use Architectural Patterns

| Use Case | Recommended Pattern |
|----------|---------------------|
| Processing emails/documents with tool access | Dual LLM |
| Extracting structured data from untrusted sources | Typed Extraction |
| High-stakes actions (payments, deletions) | Dry-Run Evaluation |
| Maximum security | All three combined |

## Tradeoffs

| Factor | Detection | Prompt Eng | Architecture |
|--------|-----------|------------|--------------|
| **Implementation effort** | Low | Low | Medium-High |
| **Latency** | +10-50ms | +0ms | +100-500ms (2x LLM calls) |
| **Cost** | +10-20% | +0% | +100% (2x LLM calls) |
| **Protection level** | ~95% | ~98% | ~99%+ |
<!---->
## Notebooks in This Section

```bash
marimo edit notebooks_securing_guide/4_secure_architecture_software/1_dual_llm.py          # 1. Quarantined + Privileged LLM separation
marimo edit notebooks_securing_guide/4_secure_architecture_software/2_typed_extraction.py   # 2. Schema constraints as firewall
marimo edit notebooks_securing_guide/4_secure_architecture_software/3_dry_run.py            # 3. Plan → Evaluate → Execute
marimo edit notebooks_securing_guide/4_secure_architecture_software/4_tool_validation.py    # 4. Tool & MCP manifest validation
marimo edit notebooks_securing_guide/4_secure_architecture_software/5_camel.py              # 5. CaMeL capability-based security
```

---

## Also Worth Knowing: IBAC

**Intent-Based Access Control** ([ibac.dev](https://ibac.dev)) derives per-request permissions
from the user's explicit intent and enforces them via [OpenFGA](https://openfga.dev) before every tool call.
Conceptually similar to output validation + capability scoping, but backed by a real authorization engine.

| Strength | Limitation |
|----------|-----------|
| Enforcement is deterministic (outside the LLM) | Intent parser is itself an LLM — susceptible to injection |
| ~9ms per auth check, TTL-based expiry | 33% automated utility in strict mode (heavy escalation) |
| 100% security on AgentDojo (strict mode) | Single benchmark; "no dual-LLM" claim is debatable |

Promising approach, but the "prompt injection becomes irrelevant" claim overstates it —
the intent parser *is* the attack surface. Worth watching as the research matures.

---

## References

- **Simon Willison** — [The Dual LLM Pattern](https://simonwillison.net/2023/Apr/25/dual-llm-pattern/)
- **Chen et al. (2025)** — [StruQ: Defending Against Prompt Injection with Structured Queries](https://arxiv.org/abs/2402.06363)
- **Google DeepMind** — [CaMeL: Defeating Prompt Injections by Design](https://arxiv.org/abs/2503.18813)
- **Jordan Potti (2026)** — [IBAC: Intent-Based Access Control](https://ibac.dev) — FGA-backed capability scoping
- **OWASP GenAI (2025)** — [Top 10 for LLM Applications v2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) — LLM01: Prompt Injection, LLM06: Excessive Agency
- **OWASP** — [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)

---

**Previous:** `notebooks_securing_guide/2_prompt_engineering/overview.py` — Hardening prompts
**Next:** `notebooks_securing_guide/5_defense_in_depth/` — Layering everything