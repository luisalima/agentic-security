---
title: Overview
marimo-version: 0.16.1
width: medium
---

# Level 4: Defense in Depth

Layer all techniques together. **Assume breach at each layer.**

## The Philosophy

No single defense is perfect. Each layer catches what the previous missed:

```
Input → Detection (YARA, ML) → ~95% blocked
          ↓ (5% bypass)
     Delimiters → ~2% bypass
          ↓ (0.1% bypass)
     Typed Extraction → Payload can't fit
          ↓
     Dry-Run Evaluation → Intent mismatch caught
          ↓
     Deterministic Validation → Unknown recipients blocked
          ↓
     Execute (if all pass)
```

<!-- DIAGRAM: diagrams/defense_in_depth.excalidraw -->

```python {.marimo}
import marimo as mo
```

## The Tradeoff

| Metric | Baseline | Detection Only | Full Defense |
|--------|----------|----------------|--------------|
| **Latency** | 1x | 1.1x | 4-5x |
| **Cost** | 1x | 1.1x | 4-5x |
| **Complexity** | Low | Low | High |
| **Protection** | ~0% | ~95% | ~99%+ |

**Defense in depth is expensive.** Use it when the stakes justify the cost.
<!---->
## When to Use Full Defense

| ✅ Worth the complexity | ❌ Overkill |
|-------------------------|-------------|
| Customer-facing agents with tool access | Internal tools with trusted users |
| Financial transactions | Low-stakes applications |
| Healthcare/legal applications | High-volume, cost-sensitive systems |
| Systems handling credentials/PII | Read-only assistants |
| Where "oops" isn't acceptable | Prototype/demo systems |
<!---->
## Notebook

**[combined.py](./combined.py)** — Full implementation layering all techniques

---

## The Meta-Insight

The question isn't "is this secure?" (nothing is perfectly secure).

The question is: **Does the protection justify the complexity and cost?**

For most production systems, Level 2-3 (detection + some architecture)
provides good balance. Level 4 is for when you truly can't afford failures.

---

**Previous:** [4_secure_architecture_software/](../4_secure_architecture_software/) — Architectural patterns