import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Framework Integration

    How to apply security patterns to real-world LLM frameworks.

    ## The Gap

    Most frameworks (LangChain, LlamaIndex, CrewAI) focus on **capability**, not **security**.
    They make it easy to build agents but leave security as an exercise for the developer.

    | Framework | Focus | Security Approach |
    |-----------|-------|-------------------|
    | **LangChain** | Orchestration, chains, agents | "Use callbacks for DIY" |
    | **LlamaIndex** | RAG, data connectors | Data residency only |
    | **CrewAI** | Multi-agent orchestration | "Careful guardrails" (manual) |
    | **AutoGen** | Agent conversations | Human-in-the-loop |

    <!-- DIAGRAM: diagrams/framework_gap.excalidraw -->
    """)
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Integration Strategies

    | Strategy | Complexity | Coverage |
    |----------|------------|----------|
    | **Wrapper functions** | Low | Single LLM calls |
    | **Custom callbacks** | Medium | Full pipeline visibility |
    | **Middleware pattern** | Medium | Request/response interception |
    | **Architecture redesign** | High | Full Dual LLM pattern |

    The examples in this section show practical integration approaches.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Notebooks in This Section

    1. **[langchain_integration.py](./langchain_integration.py)** — Securing LangChain agents
    
    (More framework examples coming: LlamaIndex, CrewAI)

    ---

    ## The Ideal Future

    ```python
    # What integration SHOULD look like (hypothetical)
    from langchain.security import SecurityConfig

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        security=SecurityConfig(
            input_guards=[PromptInjectionDetector()],
            output_guards=[SensitiveDataFilter()],
            architecture="dual_llm",  # Automatic quarantine/privilege split
        )
    )
    ```

    Until frameworks build this in, you need to implement it yourself.

    ---

    **Previous:** [4_defense_in_depth/](../4_defense_in_depth/) — Layered defense
    """)
    return


if __name__ == "__main__":
    app.run()
