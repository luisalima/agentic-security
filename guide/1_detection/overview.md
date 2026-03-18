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

**Active tools (2025–2026):**

| Tool | Type | ML | Key Feature |
|------|------|----|-------------|
| [LLM Guard](https://llm-guard.com/) | OSS | ✓ | 15 input + 20 output scanners (ProtectAI) |
| [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) | OSS | ✓ | Dialog flow control via Colang DSL (NVIDIA) |
| [Promptfoo](https://github.com/promptfoo/promptfoo) | OSS | ✓ | Red-teaming for 50+ vulnerability types |
| [Meta Prompt Guard](https://huggingface.co/meta-llama/Prompt-Guard-86M) | Model | ✓ | Free 86M-param classifier on HuggingFace |
| [Lakera Guard](https://www.lakera.ai/) | Commercial | ✓ | Enterprise API, <50ms, 80M+ attack data points |

**Historical (archived/inactive):**

| Tool | Status | Why It Died |
|------|--------|-------------|
| [Vigil](https://github.com/deadbits/vigil-llm) | Inactive since 2023 | Solo-dev project; author joined Robust Intelligence (now Cisco) |
| [Rebuff](https://github.com/protectai/rebuff) | Archived May 2025 | ProtectAI pivoted to LLM Guard; heavy Pinecone/OpenAI dependency |

*The churn in OSS security tools is itself a lesson: detection is a moving target,
and solo-maintained projects can't keep up with evolving attacks.*

See [docs/TOOLS.md](../../docs/TOOLS.md) for detailed comparison.
<!---->
## Notebooks in This Section

1. **[1_yara_detection.py](./yara_detection.md)** — Fast pattern matching for known attacks
2. **[2_vector_similarity.py](./vector_similarity.md)** — Semantic similarity search
3. **[3_ml_classifier.py](./ml_classifier.md)** — Neural network classification
4. **[4_llm_as_judge.py](./llm_as_judge.md)** — LLM evaluating for injection
5. **[5_canary_tokens.py](./canary_tokens.md)** — Detecting prompt leakage

---

## References

- **Schulhoff et al. (2023)** — [HackAPrompt: Exposing Systemic Vulnerabilities](https://arxiv.org/abs/2311.16119)
  - Taxonomy of prompt injection techniques from competition

- **tldrsec** — [Prompt Injection Defenses](https://github.com/tldrsec/prompt-injection-defenses)
  - Comprehensive catalog of every practical and proposed defense

---

**Previous:** [0_vulnerabilities/](../0_vulnerabilities/) — The vulnerability
**Next:** [2_prompt_engineering/](../2_prompt_engineering/) — Hardening prompts
