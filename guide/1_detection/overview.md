---
title: Overview
marimo-version: 0.16.1
width: medium
---

# Level 1: Detection

Detection techniques attempt to identify malicious prompts **before** they reach the LLM.
Think of this as a firewall—it filters known threats but won't catch everything.

## The Detection Pipeline

```
User Input → [YARA] → [Vector DB] → [ML Classifier] → LLM
               ↓           ↓              ↓
             Block?     Similar to     Injection
                       known attack?   probability?
```

Each layer catches different attack types. Together, they provide ~95% coverage
against known attacks—but sophisticated adversaries can still bypass detection.

<!-- DIAGRAM: diagrams/detection_pipeline.excalidraw -->

```python {.marimo}
import marimo as mo
```

## Detection Techniques

| Technique | Speed | Catches | Misses |
|-----------|-------|---------|--------|
| **YARA Rules** | <1ms | Exact patterns, known signatures | Rephrased attacks |
| **Vector Similarity** | ~10ms | Semantic variants | Novel attack types |
| **ML Classifier** | ~50ms | Context-aware patterns | Adversarial examples |
| **LLM-as-Judge** | ~200ms | Nuanced, context-aware | Meta-injection |
| **Canary Tokens** | — | Prompt leakage | Doesn't prevent injection |

**Key insight:** Detection is probabilistic. It reduces risk but cannot eliminate it.
Use detection as one layer in defense-in-depth, not as your only protection.
<!---->
## When Detection Works

✅ Blocking known attack patterns at scale
✅ Filtering obvious injection attempts
✅ Logging and monitoring for security analysis
✅ Raising the bar for unsophisticated attackers

## When Detection Fails

❌ Novel attacks not in training data
❌ Carefully crafted adversarial prompts
❌ Social engineering that looks legitimate
❌ Attacks that exploit application-specific context
<!---->
## Tools Using These Techniques

| Tool | YARA | Vectors | ML | Canaries |
|------|------|---------|----|---------|
| [Vigil](https://github.com/deadbits/vigil-llm) | ✓ | ✓ | ✓ | ✓ |
| [LLM Guard](https://llm-guard.com/) | — | — | ✓ | — |
| [Rebuff](https://github.com/protectai/rebuff) | — | ✓ | ✓ | ✓ |
| [Lakera Guard](https://www.lakera.ai/) | ? | ? | ✓ | — |

See [docs/TOOLS.md](../../docs/TOOLS.md) for detailed comparison.
<!---->
## Notebooks in This Section

1. **[yara_detection.py](./yara_detection.py)** — Fast pattern matching for known attacks
2. **[vector_similarity.py](./vector_similarity.py)** — Semantic similarity search
3. **[ml_classifier.py](./ml_classifier.py)** — Neural network classification
4. **[llm_as_judge.py](./llm_as_judge.py)** — LLM evaluating for injection
5. **[canary_tokens.py](./canary_tokens.py)** — Detecting prompt leakage

---

## References

- **Schulhoff et al. (2023)** — [HackAPrompt: Exposing Systemic Vulnerabilities](https://arxiv.org/abs/2311.16119)
  - Taxonomy of prompt injection techniques from competition

- **Vigil Documentation** — [Scanner Architecture](https://vigil.deadbits.ai/overview/use-vigil/scanners/)
  - Multi-layer detection implementation

---

**Previous:** [0_baseline/](../0_baseline/) — The vulnerability
**Next:** [2_prompt_engineering/](../2_prompt_engineering/) — Hardening prompts