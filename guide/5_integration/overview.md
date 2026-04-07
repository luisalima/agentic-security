---
title: Overview
marimo-version: 0.16.1
width: medium
---

# Framework Integration

How to apply security patterns to real-world LLM frameworks.

## The Gap

Most frameworks (LangChain, LlamaIndex, CrewAI) focus on **capability**, not **security**.
They make it easy to build agents but leave security as an exercise for the developer.

| Framework | Focus | Security Approach |
|-----------|-------|-------------------|
| **LangChain** | Orchestration, chains, agents | "Use callbacks for DIY" |
| **Pydantic AI** | Type-safe agents, structured output | Structured output, tool approval, TestModel |
| **LlamaIndex** | RAG, data connectors | Data residency only |
| **CrewAI** | Multi-agent orchestration | "Careful guardrails" (manual) |

<!-- DIAGRAM: diagrams/framework_gap.excalidraw -->

```python {.marimo}
import marimo as mo
```

## Integration Strategies

| Strategy | Complexity | Coverage |
|----------|------------|----------|
| **Wrapper functions** | Low | Single LLM calls |
| **Custom callbacks** | Medium | Full pipeline visibility |
| **Middleware pattern** | Medium | Request/response interception |
| **Architecture redesign** | High | Full Dual LLM pattern |

The examples in this section show practical integration approaches.
<!---->
## Notebooks in This Section

1. **[langchain_integration.py](./langchain_integration.py)** — Securing LangChain agents
2. **[pydantic_ai_integration.py](./pydantic_ai_integration.py)** — Securing Pydantic AI agents

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