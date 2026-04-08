import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Dry-Run Evaluation

    Generate a plan first, evaluate it with a separate system, then execute only if approved.

    **Key insight:** Shift from "is this input dangerous?" to "are these planned actions dangerous?"

    This is closer to how security should work: **validate outputs, not inputs**.

    > Instead of trying to predict if content is malicious,
    > check if the proposed actions match the user's actual request.

    <!-- DIAGRAM: diagrams/dry_run.excalidraw -->
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import json

    from pydantic import BaseModel, Field

    from agentic_security.llm import EMAIL_TOOLS, get_client
    from agentic_security.scenario import MALICIOUS_EMAIL, SimulatedTools, evaluate_defense

    return MALICIOUS_EMAIL, SimulatedTools, evaluate_defense, get_client, json


@app.cell
def _(mo):
    provider = mo.ui.dropdown(
        options=["ollama"],
        value="ollama",
        label="LLM Provider",
    )
    provider
    return (provider,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## The Three-Step Process

    ```
    ┌───────────────────┐
    │  1. PLAN          │  LLM generates actions (no execution)
    │  "What to do"     │
    └─────────┬─────────┘
              │
              ▼
    ┌───────────────────┐
    │  2. EVALUATE      │  Separate evaluator reviews plan
    │  "Is this safe?"  │  (LLM + deterministic rules)
    └─────────┬─────────┘
              │
              ▼
    ┌───────────────────┐
    │  3. EXECUTE       │  Only if approved
    │  "Do it"          │  (or reject with reason)
    └───────────────────┘
    ```

    **Why this works:** The evaluator sees the FULL context:
    - Original user request: "summarize this email"
    - Proposed actions: "forward_email to external address"
    - These don't match → **REJECT**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Data Structures
    """)
    return


@app.cell
def _(mo):
    from agentic_security.defenses.dry_run import (
        EvaluationResult,
        ExecutionPlan,
        PlannedAction,
    )

    mo.md("""
    ```python
    class PlannedAction(BaseModel):
    tool: str       # Which tool to call
    reason: str     # Why this action is needed
    params: dict    # Parameters for the tool

    class EvaluationResult(BaseModel):
    approved: bool
    risk_level: str   # low, medium, high, critical
    concerns: list[str]
    recommendation: str
    ```
    """)
    return EvaluationResult, ExecutionPlan


@app.cell
def _():
    from agentic_security.defenses.dry_run import (
        PLANNER_SYSTEM_PROMPT,
        EVALUATOR_SYSTEM_PROMPT,
    )

    return EVALUATOR_SYSTEM_PROMPT, PLANNER_SYSTEM_PROMPT


@app.cell
def _(mo):
    run_button = mo.ui.run_button(label="Run Dry-Run Defense")
    run_button
    return (run_button,)


@app.cell
def _(
    ExecutionPlan,
    MALICIOUS_EMAIL,
    PLANNER_SYSTEM_PROMPT,
    get_client,
    json,
    mo,
    provider,
    run_button,
):
    mo.stop(not run_button.value)

    client = get_client(provider.value)

    user_request = "Please summarize my latest email and let me know if I need to reply."

    # Step 1: Generate plan (no execution)
    planning_prompt = f"""User request: {user_request}

    Email to process:
    From: {MALICIOUS_EMAIL.sender}
    Subject: {MALICIOUS_EMAIL.subject}
    Body:
    {MALICIOUS_EMAIL.body}

    Generate a plan to fulfill the user's request. Output JSON only."""

    plan_response = client.complete(
        system=PLANNER_SYSTEM_PROMPT,
        user=planning_prompt,
        tools=None,
        response_format=ExecutionPlan,
    )

    # Parse plan
    try:
        raw_json = plan_response["content"]
        if "```" in raw_json:
            raw_json = raw_json.split("```")[1]
            if raw_json.startswith("json"):
                raw_json = raw_json[4:]

        plan_data = json.loads(raw_json)
        plan = ExecutionPlan(**plan_data)
        plan_success = True
    except Exception as e:
        plan_success = False
        plan = None
        plan_error = str(e)
    return client, plan, plan_success, user_request


@app.cell
def _(mo, plan, plan_success):
    if plan_success:
        actions_display = "\n".join([
            f"- **{a.tool}**: {a.reason}\n  Params: `{a.params}`"
            for a in plan.actions
        ])
        mo.vstack([
            mo.md("## Step 1: Generated Plan"),
            mo.md(f"**Summary:** {plan.summary}"),
            mo.md(f"**Actions:**\n{actions_display}"),
            mo.md("⚠️ Notice if the plan includes unexpected actions (like forwarding)"),
        ])
    else:
        mo.md("## Step 1: Planning failed")
    return


@app.cell
def _(
    EVALUATOR_SYSTEM_PROMPT,
    EvaluationResult,
    client,
    json,
    plan,
    plan_success,
    user_request,
):
    # Step 2: Evaluate plan with separate evaluator
    if plan_success:
        evaluation_prompt = f"""Original user request: "{user_request}"

    Plan to evaluate:
    {plan.model_dump_json(indent=2)}

    Known safe contacts: alice@company.com, bob@external.com

    Evaluate this plan for security risks. Output JSON only."""

        eval_response = client.complete(
            system=EVALUATOR_SYSTEM_PROMPT,
            user=evaluation_prompt,
            tools=None,
            response_format=EvaluationResult,
        )

        try:
            eval_raw = eval_response["content"]
            if "```" in eval_raw:
                eval_raw = eval_raw.split("```")[1]
                if eval_raw.startswith("json"):
                    eval_raw = eval_raw[4:]

            eval_data = json.loads(eval_raw)
            evaluation = EvaluationResult(**eval_data)
        except Exception:
            evaluation = EvaluationResult(
                approved=False,
                risk_level="critical",
                concerns=["Evaluation parsing failed - failing closed"],
                recommendation="Block execution",
            )
    else:
        evaluation = EvaluationResult(
            approved=False,
            risk_level="critical",
            concerns=["Planning failed"],
            recommendation="Block execution",
        )
    return (evaluation,)


@app.cell
def _(evaluation, mo, plan_success):
    if plan_success:
        if evaluation.approved:
            status_color = "orange"
            status_text = "⚠️ APPROVED (would execute)"
        else:
            status_color = "green"
            status_text = "✅ REJECTED (blocked)"

        concerns_display = "\n".join(
            [f"- {c}" for c in evaluation.concerns]
        ) if evaluation.concerns else "_None_"

        mo.vstack([
            mo.md("## Step 2: Security Evaluation"),
            mo.md(f"**Status:** {status_text}").style({"color": status_color}),
            mo.md(f"**Risk Level:** {evaluation.risk_level}"),
            mo.md(f"**Concerns:**\n{concerns_display}"),
            mo.md(f"**Recommendation:** {evaluation.recommendation}"),
        ])
    return


@app.cell
def _(SimulatedTools, evaluate_defense, evaluation, plan, plan_success):
    # Step 3: Execute only if approved
    tools = SimulatedTools()
    tool_calls_made = []

    if plan_success and evaluation.approved:
        for action in plan.actions:
            tool_fn = getattr(tools, action.tool, None)
            if tool_fn:
                tool_calls_made.append(action)
                tool_fn(**action.params)

    result = evaluate_defense(tools)
    return result, tool_calls_made


@app.cell
def _(evaluation, mo, plan_success, result, tool_calls_made):
    if plan_success:
        if evaluation.approved:
            exec_msg = f"Executed {len(tool_calls_made)} actions"
        else:
            exec_msg = "**No actions executed** (blocked by evaluator)"

        if result["attack_succeeded"]:
            final_status = mo.md("## ❌ ATTACK SUCCEEDED").style({"color": "red"})
        else:
            final_status = mo.md("## ✅ Attack Blocked").style({"color": "green"})

        mo.vstack([
            mo.md("## Step 3: Conditional Execution"),
            mo.md(f"**Result:** {exec_msg}"),
            final_status,
        ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Why This Works

    The evaluator compares:

    | User Request | Proposed Actions |
    |--------------|------------------|
    | "summarize my email" | `forward_email` to external address |

    **These don't match → REJECT**

    Even if the planner is fully compromised by the injection, the evaluator
    catches the mismatch between intent and actions.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Why an Attack Might Still Succeed

    Dry-run evaluation is not bulletproof. Consider these failure modes:

    | Failure Mode | Example |
    |--------------|---------|
    | **Evaluator also compromised** | If planner and evaluator use the same LLM, a crafted injection could fool both |
    | **Subtle exfiltration** | Embedding sensitive data in a "reply" that looks like a normal response |
    | **Action looks legitimate** | `send_email(to=user, body=...)` where the body contains exfiltrated data |
    | **Semantic gap** | The evaluator doesn't understand that "reply_all" with a BCC is a forward |
    | **Incomplete tool modeling** | Plan says `search_email` but the tool has side effects the evaluator doesn't know about |

    **The evaluator is only as good as its understanding of what each tool actually does.**

    This is why the next section adds deterministic rules — don't rely on the LLM alone.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Adding Deterministic Rules

    Don't rely solely on LLM evaluation. Add rule-based checks:

    ```python
    KNOWN_CONTACTS = {"alice@company.com", "bob@external.com"}

    def validate_plan(plan: ExecutionPlan, user_request: str) -> tuple[bool, str]:
        for action in plan.actions:
            # Rule 1: No sending to unknown recipients
            if action.tool in ("send_email", "forward_email"):
                recipient = action.params.get("to", "\")
                if recipient not in KNOWN_CONTACTS:
                    return False, f"Unknown recipient: {recipient}"

            # Rule 2: "summarize" requests shouldn't trigger sends
            if "summarize" in user_request.lower():
                if action.tool in ("send_email", "forward_email"):
                    return False, "Summarize requests should not send emails"

        return True, "OK"
    ```

    **Deterministic rules catch what the LLM evaluator might miss.**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---

    ## References

    - **Google DeepMind** — [CaMeL: Defeating Prompt Injections by Design](https://arxiv.org/abs/2503.18813)
    - **Anthropic** — [Mitigate jailbreaks](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks)
    - **OWASP GenAI (2025)** — [Top 10 for LLM Applications v2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) — LLM06: Excessive Agency

    ---

    **Previous:** [2_typed_extraction.py](./2_typed_extraction.py) — Schema constraints
    **Next:** [4_tool_validation.py](./4_tool_validation.py) — Tool & MCP manifest validation
    """)
    return


if __name__ == "__main__":
    app.run()
