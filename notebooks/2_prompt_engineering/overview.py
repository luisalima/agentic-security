import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Level 2: Prompt Engineering

    Prompt engineering defenses harden **individual LLM calls** through careful
    prompt design. No architectural changes required—just smarter prompts.

    ## The Idea

    Instead of hoping the LLM will "just know" to ignore malicious content,
    we explicitly structure prompts to:

    1. **Mark boundaries** — Clearly separate trusted from untrusted content
    2. **Set expectations** — Tell the LLM what to trust and what to ignore
    3. **Reduce ambiguity** — Make the data/instruction distinction explicit

    <!-- DIAGRAM: diagrams/prompt_engineering.excalidraw -->
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Techniques

    | Technique | Description | Effectiveness |
    |-----------|-------------|---------------|
    | **Random Delimiters** | Wrap untrusted content in random tokens | Medium |
    | **System Prompt Hardening** | Role anchoring, explicit negatives, output constraints | Medium |
    | **Instruction Hierarchy** | Explicit priority levels (system > user > data) | Medium-High |
    | **Sandwich Defense** | Repeat instructions after untrusted content | Medium |
    | **XML Tagging** | Structured prompts with semantic boundaries | Medium |

    **Key insight:** All prompt engineering techniques are **probabilistic**.
    They reduce attack success rates but cannot eliminate them.
    Combine multiple techniques for best results.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Microsoft's Spotlighting Research

    Microsoft Research tested delimiter-based defenses and found:

    > "Spotlighting reduces attack success rates from >50% to <2%"
    > — [Defending Against Indirect Prompt Injection Attacks With Spotlighting](https://arxiv.org/abs/2403.14720)

    However, Simon Willison's response:

    > "Delimiters won't save you. Attackers can say 'ignore the delimiters'
    > without ever using the delimiter characters."
    > — [simonwillison.net](https://simonwillison.net/2023/May/11/delimiters-wont-save-you/)

    **Both are right.** Delimiters help significantly against naive attacks
    but sophisticated attackers can still bypass them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## When Prompt Engineering Works

    ✅ Blocking naive/automated injection attempts
    ✅ Reducing attack surface for unsophisticated attackers
    ✅ Adding friction without architectural changes
    ✅ Quick wins for existing systems

    ## When It Fails

    ❌ Sophisticated social engineering
    ❌ "Ignore the security instructions" attacks
    ❌ Multi-turn manipulation
    ❌ Attacks that exploit application-specific context
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Notebooks in This Section

    Open any notebook from the repo root:

    ```bash
    marimo edit notebooks/2_prompt_engineering/1_delimiters.py              # 1. Random token delimiters (Spotlighting)
    marimo edit notebooks/2_prompt_engineering/2_system_prompt_hardening.py # 2. Role anchoring, explicit negatives
    marimo edit notebooks/2_prompt_engineering/3_instruction_hierarchy.py   # 3. Priority framing (system > user > data)
    marimo edit notebooks/2_prompt_engineering/4_sandwich_defense.py        # 4. Repeat instructions after untrusted content
    marimo edit notebooks/2_prompt_engineering/5_xml_tagging.py             # 5. Structured prompts with semantic XML tags
    ```

    ---

    ## The Honest Truth

    Prompt engineering is **necessary but not sufficient**.

    Use it as a baseline defense, but don't rely on it alone for high-stakes applications.
    For real security, you need architectural separation (Level 3).

    ---

    ## References

    - **Hines et al. (Microsoft, 2024)** — [Defending Against Indirect Prompt Injection Attacks With Spotlighting](https://arxiv.org/abs/2403.14720)
    - **Wallace et al. (2024)** — [The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions](https://arxiv.org/abs/2404.13208)
    - **Simon Willison** — [Delimiters won't save you](https://simonwillison.net/2023/May/11/delimiters-wont-save-you/)
    - **OWASP GenAI (2025)** — [Top 10 for LLM Applications v2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) — LLM01: Prompt Injection
    - **OWASP** — [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
    - **Ferrag et al. (2026)** — [Securing LLM Agents: From Prompt Sanitization to Autonomous Red Teaming](https://doi.org/10.1016/j.iotcps.2026.03.001)

    ---

    **Previous:** `notebooks/1_detection/overview.py` — Filtering malicious inputs
    **Next:** `notebooks/3_isolation_infra_level/overview.py` — Isolation & blast radius containment
    """)
    return


if __name__ == "__main__":
    app.run()
