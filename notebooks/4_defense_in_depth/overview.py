import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
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
    """)
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## The Tradeoff

    | Metric | Baseline | Detection Only | Full Defense |
    |--------|----------|----------------|--------------|
    | **Latency** | 1x | 1.1x | 4-5x |
    | **Cost** | 1x | 1.1x | 4-5x |
    | **Complexity** | Low | Low | High |
    | **Protection** | ~0% | ~95% | ~99%+ |

    **Defense in depth is expensive.** Use it when the stakes justify the cost.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## When to Use Full Defense

    | ✅ Worth the complexity | ❌ Overkill |
    |-------------------------|-------------|
    | Customer-facing agents with tool access | Internal tools with trusted users |
    | Financial transactions | Low-stakes applications |
    | Healthcare/legal applications | High-volume, cost-sensitive systems |
    | Systems handling credentials/PII | Read-only assistants |
    | Where "oops" isn't acceptable | Prototype/demo systems |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Notebook

    **[combined.py](./combined.py)** — Full implementation layering all techniques

    ---

    ## The Meta-Insight

    The question isn't "is this secure?" (nothing is perfectly secure).

    The question is: **Does the protection justify the complexity and cost?**

    For most production systems, Level 2-3 (detection + some architecture) 
    provides good balance. Level 4 is for when you truly can't afford failures.

    ---

    **Previous:** [3_secure_architecture/](../3_secure_architecture/) — Architectural patterns
    """)
    return


if __name__ == "__main__":
    app.run()
