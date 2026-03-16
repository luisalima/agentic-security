import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Multi-Agent Attack Scenarios

    Prompt injection isn't limited to single-agent email assistants.
    Any system boundary where **untrusted text crosses into a trusted context**
    is an injection surface. This notebook demonstrates three:

    | Attack | Injection Surface | What Breaks |
    |--------|------------------|-------------|
    | **RAG Poisoning** | Retrieved documents | Agent treats doc content as instructions |
    | **Delegation** | Agent-to-agent messages | Agent B trusts forwarded content from Agent A |
    | **Plugin Supply-Chain** | Plugin metadata/descriptions | Agent follows "setup" instructions in manifests |

    All demos are **fully simulated** — no LLM required. The deterministic runners
    show exactly what a vulnerable agent would do.

    > "The attack surface of an agentic system is every boundary where
    > untrusted data enters a trusted context."
    """)
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path.cwd().parent.parent / "src"))

    from agentic_security.attacks.multi_agent import (
        MALICIOUS_DELEGATION,
        MALICIOUS_PLUGIN,
        POISONED_RAG_DOC,
        SAFE_PLUGIN,
        SAFE_RAG_DOCS,
        DelegationMessage,
        SimulatedMultiAgentTools,
        evaluate_multi_agent_defense,
        run_vulnerable_delegation,
        run_vulnerable_plugin,
        run_vulnerable_rag,
    )
    return (
        DelegationMessage,
        MALICIOUS_DELEGATION,
        MALICIOUS_PLUGIN,
        POISONED_RAG_DOC,
        SAFE_PLUGIN,
        SAFE_RAG_DOCS,
        SimulatedMultiAgentTools,
        evaluate_multi_agent_defense,
        run_vulnerable_delegation,
        run_vulnerable_plugin,
        run_vulnerable_rag,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---

    ## Attack 1: RAG Poisoning

    **The scenario:** A user asks an AI assistant to summarize internal documents.
    The retrieval system returns results from a document store that includes
    externally uploaded files. One document contains injected instructions.

    ```
    ┌──────────────┐     ┌───────────────┐     ┌──────────────────┐
    │ User Query   │────▶│  Retrieval    │────▶│  LLM Agent       │
    │ "Summarize"  │     │  System       │     │  (has tools)     │
    └──────────────┘     └───────┬───────┘     └──────┬───────────┘
                                 │                    │
                         ┌───────▼───────┐     ┌──────▼───────────┐
                         │ doc_001 ✅    │     │ Tool: send_email │
                         │ doc_002 ✅    │     │ Tool: fetch_url  │
                         │ doc_003 ❌    │     └──────────────────┘
                         │ (poisoned)    │
                         └───────────────┘
    ```

    The agent treats **all retrieved documents equally** — it cannot distinguish
    between trusted internal docs and an attacker-uploaded document.
    """)
    return


@app.cell
def _(POISONED_RAG_DOC, SAFE_RAG_DOCS, mo):
    safe_display = "\n".join(
        f"- **{d.title}** (`{d.source}`, trusted={d.trusted}): {d.content[:80]}..."
        for d in SAFE_RAG_DOCS
    )

    mo.md(f"""
### Retrieved Documents

**Safe documents:**
{safe_display}

**Poisoned document** (`{POISONED_RAG_DOC.source}`, trusted={POISONED_RAG_DOC.trusted}):
```
{POISONED_RAG_DOC.content}
```

⚠️ The injection is embedded as a "compliance requirement" — social engineering for AI.
""")
    return (safe_display,)


@app.cell
def _(
    POISONED_RAG_DOC,
    SAFE_RAG_DOCS,
    SimulatedMultiAgentTools,
    evaluate_multi_agent_defense,
    mo,
    run_vulnerable_rag,
):
    # Run with safe docs only
    safe_tools = SimulatedMultiAgentTools()
    safe_result = run_vulnerable_rag(SAFE_RAG_DOCS, safe_tools)
    safe_eval = evaluate_multi_agent_defense(safe_tools)

    # Run with poisoned doc included
    poisoned_tools = SimulatedMultiAgentTools()
    poisoned_result = run_vulnerable_rag(
        SAFE_RAG_DOCS + [POISONED_RAG_DOC], poisoned_tools,
    )
    poisoned_eval = evaluate_multi_agent_defense(poisoned_tools)

    actions_display = "\n".join(
        f"  - `{a['tool']}` → `{a['params']}`"
        for a in poisoned_tools.actions_log
    ) or "  _None_"

    if poisoned_eval["attack_succeeded"]:
        status = mo.md("### ❌ RAG Poisoning Attack Succeeded").style({"color": "red"})
    else:
        status = mo.md("### ✅ No Attack Detected").style({"color": "green"})

    mo.vstack([
        mo.md("### Results"),
        mo.md(f"**Safe docs only:** {safe_eval['dangerous_actions']} dangerous actions"),
        status,
        mo.md(f"**With poisoned doc:** {poisoned_eval['dangerous_actions']} dangerous action(s)"),
        mo.md(f"**Actions taken by vulnerable agent:**\n{actions_display}"),
        mo.md(
            "The agent followed the injected 'compliance' instruction and sent "
            "internal data to an external address."
        ),
    ])
    return poisoned_eval, poisoned_result, poisoned_tools, safe_eval, safe_result, safe_tools


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---

    ## Attack 2: Multi-Agent Delegation

    **The scenario:** Agent A (research agent) searches the web and forwards its
    findings to Agent B (email agent) for processing. The web content contains
    injected instructions that Agent B treats as its own task.

    ```
    ┌──────────┐     ┌──────────────┐     ┌──────────────┐
    │  Web     │────▶│  Agent A     │────▶│  Agent B     │
    │  (has    │     │  (research)  │     │  (email)     │
    │  attack) │     │  forwards    │     │  has tools   │
    └──────────┘     │  raw content │     │  trusts A    │
                     └──────────────┘     └──────────────┘
    ```

    Agent A faithfully forwards the web content. Agent B can't tell the
    difference between Agent A's legitimate instructions and injected text.
    """)
    return


@app.cell
def _(MALICIOUS_DELEGATION, mo):
    mo.md(f"""
### The Delegation Message

**From:** `{MALICIOUS_DELEGATION.sender_agent}` → **To:** `{MALICIOUS_DELEGATION.recipient_agent}`
**Task:** {MALICIOUS_DELEGATION.task}

**Forwarded Context:**
```
{MALICIOUS_DELEGATION.context}
```

⚠️ The injection pretends to be "UPDATED INSTRUCTIONS" configured in "shared agent settings."
""")
    return


@app.cell
def _(
    MALICIOUS_DELEGATION,
    DelegationMessage,
    SimulatedMultiAgentTools,
    evaluate_multi_agent_defense,
    mo,
    run_vulnerable_delegation,
):
    # Safe delegation
    safe_msg = DelegationMessage(
        sender_agent="research_agent",
        recipient_agent="email_agent",
        task="Draft a summary",
        context="Competitor pricing: $99/month for basic, $199/month for pro.",
    )
    safe_deleg_tools = SimulatedMultiAgentTools()
    run_vulnerable_delegation(safe_msg, safe_deleg_tools)
    safe_deleg_eval = evaluate_multi_agent_defense(safe_deleg_tools)

    # Malicious delegation
    attack_deleg_tools = SimulatedMultiAgentTools()
    run_vulnerable_delegation(MALICIOUS_DELEGATION, attack_deleg_tools)
    attack_deleg_eval = evaluate_multi_agent_defense(attack_deleg_tools)

    deleg_actions = "\n".join(
        f"  - `{a['tool']}` → `{a['params']}`"
        for a in attack_deleg_tools.actions_log
    ) or "  _None_"

    if attack_deleg_eval["attack_succeeded"]:
        deleg_status = mo.md("### ❌ Delegation Attack Succeeded").style({"color": "red"})
    else:
        deleg_status = mo.md("### ✅ No Attack Detected").style({"color": "green"})

    mo.vstack([
        mo.md("### Results"),
        mo.md(f"**Safe delegation:** {safe_deleg_eval['dangerous_actions']} dangerous actions"),
        deleg_status,
        mo.md(f"**Malicious delegation:** {attack_deleg_eval['dangerous_actions']} dangerous action(s)"),
        mo.md(f"**Actions taken by Agent B:**\n{deleg_actions}"),
    ])
    return (
        attack_deleg_eval,
        attack_deleg_tools,
        deleg_actions,
        deleg_status,
        safe_deleg_eval,
        safe_deleg_tools,
        safe_msg,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---

    ## Attack 3: Plugin Supply-Chain

    **The scenario:** An agent loads a third-party plugin from a community marketplace.
    The plugin's description contains "setup instructions" that trick the agent into
    reading secrets and sending them to an external server.

    ```
    ┌──────────────────┐     ┌──────────────┐     ┌──────────────┐
    │  Plugin Manifest │────▶│  Agent       │────▶│  read_secret │
    │  (community)     │     │  "Install    │     │  fetch_url   │
    │  has injection   │     │   plugin"    │     │  (exfiltrate)│
    └──────────────────┘     └──────────────┘     └──────────────┘
    ```

    The agent reads the plugin description as part of its context window.
    Since tool descriptions are treated as trusted instructions, the injected
    "license verification" steps are followed without question.
    """)
    return


@app.cell
def _(MALICIOUS_PLUGIN, SAFE_PLUGIN, mo):
    mo.md(f"""
### Plugin Manifests

**Safe plugin** (`{SAFE_PLUGIN.source}`):
> {SAFE_PLUGIN.description}

**Malicious plugin** (`{MALICIOUS_PLUGIN.source}`):
```
{MALICIOUS_PLUGIN.description}
```

⚠️ The "license verification" is actually credential exfiltration disguised
as a standard OAuth step.
""")
    return


@app.cell
def _(
    MALICIOUS_PLUGIN,
    SAFE_PLUGIN,
    SimulatedMultiAgentTools,
    evaluate_multi_agent_defense,
    mo,
    run_vulnerable_plugin,
):
    # Safe plugin
    safe_plugin_tools = SimulatedMultiAgentTools()
    run_vulnerable_plugin(SAFE_PLUGIN, safe_plugin_tools)
    safe_plugin_eval = evaluate_multi_agent_defense(safe_plugin_tools)

    # Malicious plugin
    attack_plugin_tools = SimulatedMultiAgentTools()
    run_vulnerable_plugin(MALICIOUS_PLUGIN, attack_plugin_tools)
    attack_plugin_eval = evaluate_multi_agent_defense(attack_plugin_tools)

    plugin_actions = "\n".join(
        f"  - `{a['tool']}` → `{a['params']}`"
        for a in attack_plugin_tools.actions_log
    ) or "  _None_"

    if attack_plugin_eval["attack_succeeded"]:
        plugin_status = mo.md("### ❌ Plugin Supply-Chain Attack Succeeded").style(
            {"color": "red"},
        )
    else:
        plugin_status = mo.md("### ✅ No Attack Detected").style({"color": "green"})

    mo.vstack([
        mo.md("### Results"),
        mo.md(f"**Safe plugin:** {safe_plugin_eval['dangerous_actions']} dangerous actions"),
        plugin_status,
        mo.md(
            f"**Malicious plugin:** {attack_plugin_eval['dangerous_actions']} dangerous action(s)",
        ),
        mo.md(f"**Actions taken by vulnerable agent:**\n{plugin_actions}"),
    ])
    return (
        attack_plugin_eval,
        attack_plugin_tools,
        plugin_actions,
        plugin_status,
        safe_plugin_eval,
        safe_plugin_tools,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---

    ## The Common Pattern

    All three attacks exploit the same fundamental flaw:

    > **Untrusted text crosses a trust boundary and is treated as instructions.**

    | Scenario | Untrusted Surface | Unsafe Outcome | Core Lesson |
    |----------|------------------|----------------|-------------|
    | RAG Poisoning | Retrieved documents | Tool calls / data exfil | Retrieved text is **data**, not instructions |
    | Delegation | Agent-to-agent handoff | Lateral privilege abuse | Other agents are **untrusted inputs** |
    | Plugin Attack | Plugin manifest/description | Secret theft / external call | Tool metadata is **prompt surface** |

    ### Defenses That Apply

    | Defense | RAG | Delegation | Plugin |
    |---------|-----|------------|--------|
    | **Typed Extraction** | ✅ Extract structured data from docs | ✅ Schema for delegation messages | — |
    | **CaMeL / Capability Tagging** | ✅ Tag doc data as untrusted | ✅ Tag forwarded content | — |
    | **Tool Validation** | — | — | ✅ Scan descriptions for injection |
    | **Output Validation** | ✅ Check tool calls against policy | ✅ Check tool calls | ✅ Block unauthorized tools |
    | **Dual LLM** | ✅ Quarantine doc processing | ✅ Quarantine forwarded content | — |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---

    ## References

    - **Greshake et al. (2023)** — [Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173)
    - **Invariant Labs (2025)** — [MCP Security Notification](https://invariantlabs.ai/blog/mcp-security)
    - **Google DeepMind (2025)** — [CaMeL: Defeating Prompt Injections by Design](https://arxiv.org/abs/2503.18813)
    - **OWASP (2025)** — [Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

    ---

    **Previous:** `multi_turn_attacks.py` — Multi-turn manipulation
    **Next:** `../1_detection/overview.py` — Detection techniques
    """)
    return


if __name__ == "__main__":
    app.run()
