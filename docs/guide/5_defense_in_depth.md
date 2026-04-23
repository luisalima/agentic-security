# Defense in Depth

Layer all techniques together. **Assume breach at each layer.**

!!! tip "Try the notebooks"
    For runnable examples, see [`notebooks/5_defense_in_depth/`](https://github.com/luisalima/agentic-security/tree/main/notebooks/5_defense_in_depth).

---

## The Philosophy

No single defense is perfect. Each layer catches what the previous missed:

```
Input → Detection (YARA, ML) → catches many common attacks
          ↓ (adaptive bypasses still exist)
     Delimiters → adds another boundary
          ↓ (still not sufficient alone)
     Typed Extraction → payload must fit schema
          ↓
     Dry-Run Evaluation → intent mismatch reviewed
          ↓
     Deterministic Validation → unknown recipients blocked
          ↓
     Execute (if all pass)
```

Even if an attacker bypasses detection, delimiters constrain what the LLM sees. Even if delimiters fail, typed extraction strips the payload. Even if extraction is tricked, the dry-run evaluator catches intent mismatch. Even if the evaluator is fooled, deterministic rules block unknown recipients. **Every layer assumes the previous one was breached.**

---

## The Five Layers

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 1: Random Delimiters                                     │
│      Mark untrusted content boundaries                          │
│  └─▶ Layer 2: Typed Extraction                                  │
│          Constrain data to strict schema                        │
│      └─▶ Layer 3: Plan Generation                               │
│              Generate actions without executing                 │
│          └─▶ Layer 4: LLM Security Evaluation                   │
│                  Evaluate plan for risks                        │
│              └─▶ Layer 5: Deterministic Validation              │
│                      Rule-based checks (known contacts, etc.)   │
│                  └─▶ Execute (only if ALL layers pass)          │
└─────────────────────────────────────────────────────────────────┘
```

### Layer-by-Layer Breakdown

| Layer | What It Does | What It Catches |
|-------|--------------|-----------------|
| **1. Delimiters** | Marks untrusted boundaries | Naive injection attempts |
| **2. Typed Extraction** | Constrains data to schema | Payload can't fit in fields |
| **3. Plan Generation** | Separates planning from execution | N/A (setup for layer 4) |
| **4. LLM Evaluation** | Reviews plan for safety | Intent mismatch, suspicious actions |
| **5. Deterministic** | Rule-based validation | Unknown recipients, policy violations |

**Even if one layer fails, others catch the attack.**

---

## The Tradeoff

| Metric | Baseline | Detection Only | Full Defense |
|--------|----------|----------------|--------------|
| **Latency** | 1x | 1.1x | 4-5x |
| **Cost** | 1x | 1.1x | 4-5x |
| **Complexity** | Low | Low | High |
| **Security Effect** | None | Limited, probabilistic filtering | Layered resilience and containment |

**Defense in depth is expensive.** Use it when the stakes justify the cost.

---

## When to Use Full Defense vs When It's Overkill

| ✅ Worth the complexity | ❌ Overkill |
|-------------------------|-------------|
| Customer-facing agents with tool access | Internal tools with trusted users |
| Financial transactions | Low-stakes applications |
| Healthcare/legal applications | High-volume, cost-sensitive systems |
| Systems handling credentials/PII | Read-only assistants |
| Where "oops" isn't acceptable | Prototype/demo systems |

---

## The Meta-Insight

The question isn't "is this secure?" — nothing is perfectly secure.

The question is: **Does the extra resilience justify the complexity and cost?**

For most production systems, detection + some architecture (Levels 2–3) provides good balance. Full defense in depth is for when you truly can't afford failures.

---

## The Cost

| Metric | Value |
|--------|-------|
| **LLM Calls** | 3-4x baseline |
| **Latency** | 4-5x baseline |
| **Complexity** | High (many moving parts) |
| **Maintenance** | Schemas, rules, evaluator prompts |

**Is it worth it?**

For most systems: No. Detection + architectural patterns provides good balance.

For high-stakes systems (payments, healthcare, credentials): Yes.

---

## References

- **Simon Willison** — [Dual LLM Pattern](https://simonwillison.net/2023/Apr/25/dual-llm-pattern/)
- **Microsoft** — [Spotlighting](https://arxiv.org/abs/2403.14720)
- **StruQ** — [Structured Queries](https://arxiv.org/abs/2402.06363)
- **Google DeepMind** — [CaMeL](https://arxiv.org/abs/2503.18813)
