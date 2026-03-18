import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
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
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
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
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
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
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
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
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Notebooks in This Section

    Open any notebook from the repo root:

    ```bash
    marimo edit notebooks/1_detection/1_yara_detection.py      # 1. Fast pattern matching
    marimo edit notebooks/1_detection/2_vector_similarity.py   # 2. Semantic similarity search
    marimo edit notebooks/1_detection/3_ml_classifier.py       # 3. Neural network classification
    marimo edit notebooks/1_detection/4_llm_as_judge.py        # 4. LLM evaluating for injection
    marimo edit notebooks/1_detection/5_canary_tokens.py       # 5. Detecting prompt leakage
    ```

    ---

    ## References

    - **Schulhoff et al. (2023)** — [HackAPrompt: Exposing Systemic Vulnerabilities](https://arxiv.org/abs/2311.16119)
      - Taxonomy of prompt injection techniques from competition

    - **tldrsec** — [Prompt Injection Defenses](https://github.com/tldrsec/prompt-injection-defenses)
      - Comprehensive catalog of every practical and proposed defense

    ---

    **Previous:** `../0_vulnerabilities/4_case_studies.py` — Real-world case studies
    **Next:** `../2_prompt_engineering/overview.py` — Hardening prompts
    """)
    return


if __name__ == "__main__":
    app.run()
