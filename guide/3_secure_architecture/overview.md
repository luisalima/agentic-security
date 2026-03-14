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

1. **[1_dual_llm](./1_dual_llm.md)** — Quarantined + Privileged LLM separation
2. **[2_typed_extraction](./2_typed_extraction.md)** — Schema constraints as firewall
3. **[3_dry_run](./3_dry_run.md)** — Plan → Evaluate → Execute
4. **[4_tool_validation](./4_tool_validation.md)** — MCP/tool manifest validation

---

## References

- **Simon Willison** — [The Dual LLM Pattern](https://simonwillison.net/2023/Apr/25/dual-llm-pattern/)
- **StruQ** — [Defending Against Prompt Injection with Structured Queries](https://arxiv.org/abs/2402.06363)
- **Google DeepMind** — [CaMeL: Capability-based Memory for LLMs](https://arxiv.org/abs/2503.18813)

---

**Previous:** [2_prompt_engineering/](../2_prompt_engineering/) — Hardening prompts
**Next:** [4_defense_in_depth/](../4_defense_in_depth/) — Layering everything