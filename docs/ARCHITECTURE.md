# Architectural Guidelines for Agentic AI Security

## The Fundamental Problem

LLMs process instructions and data in the same channel (the context window). There is no architectural separation between "do this" and "here's some information." This is why prompt injection is fundamentally different from traditional injection attacks—there's no equivalent to parameterized queries.

## Defense Tiers

### Tier 1: Hope and Prayer (Most Common)
- Default model safety
- "Don't put anything too dangerous in production"
- Pray attackers don't find you

**Assessment:** Unacceptable for anything handling real data or actions.

### Tier 2: Probabilistic Guardrails
- Input classifiers (Lakera, NeMo, Prompt Shields)
- Output filtering
- Pattern matching

**Assessment:** ~95-99% catch rate. Sounds good until you realize 99% is a failing grade in security. Use as one layer, not primary defense.

### Tier 3: Defense in Depth
- Tier 2 + sandboxing
- Least privilege
- Human-in-the-loop for risky actions
- Rate limiting, monitoring, logging
- Assume breach, limit blast radius

**Assessment:** Reasonable for most production systems. Accept that injection will eventually succeed; focus on containment.

### Tier 4: Architectural Separation
- Dual LLM patterns
- Typed data extraction
- Capability-based security
- Symbolic references

**Assessment:** Strongest defense but high implementation complexity. Worth it for high-risk systems.

---

## Practical Guidelines

### 1. Scope Tools Aggressively

**Before:** Email assistant can read emails, send emails, access contacts, manage calendar.

**After:** Email assistant can read emails and draft responses. Sending requires separate approval flow.

```python
# Bad: Full email access
tools = [read_email, send_email, delete_email, forward_email]

# Better: Read-only + draft
tools = [read_email, draft_response]  # Actual sending is a separate, guarded operation
```

### 2. Separate Read and Write Agents

The reader agent processes untrusted content but has no tools. The writer agent has tools but never sees raw untrusted content directly.

```
┌─────────────────┐
│  Untrusted      │
│  Content        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Reader Agent   │  ← No tools, read-only
│  (Quarantined)  │
└────────┬────────┘
         │ Structured summary
         ▼
┌─────────────────┐
│  Controller     │  ← Deterministic, validates structure
└────────┬────────┘
         │ Validated data
         ▼
┌─────────────────┐
│  Writer Agent   │  ← Has tools, never sees raw content
│  (Privileged)   │
└────────┴────────┘
```

### 3. Use Typed Extraction Over Raw Text

Instead of passing text between agents, extract structured data with strict schemas.

```python
# Bad: Passing raw text
summary = reader_llm.summarize(email_body)
writer_llm.act(f"Based on this summary: {summary}")  # Injection can flow through

# Better: Typed extraction
from pydantic import BaseModel, Field
from enum import Enum

class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    URGENT = "urgent"

class EmailAnalysis(BaseModel):
    sender: str = Field(max_length=100)
    subject: str = Field(max_length=200)
    sentiment: Sentiment
    requires_response: bool
    key_points: list[str] = Field(max_length=5)  # Bounded list

analysis = reader_llm.extract(email_body, schema=EmailAnalysis)
# Now writer_llm receives typed data, not arbitrary text
```

### 4. Symbolic References

The privileged agent sees variable names, not content. The controller manages the mapping.

```python
# Bad: Content in prompt
prompt = f"The email says: {email_body}. Should we reply?"

# Better: Symbolic reference
variables = {
    "$EMAIL_1": email_body,
    "$SENDER_1": sender_address,
}
prompt = "Analyze $EMAIL_1 from $SENDER_1. Should we reply?"
# Controller substitutes variables only when needed for tool execution
```

### 5. Require Confirmation for High-Risk Actions

Any action that exfiltrates data or is irreversible requires human approval.

```python
HIGH_RISK_ACTIONS = {
    "send_email",
    "delete_file", 
    "api_call_external",
    "execute_code",
    "access_credentials",
}

def execute_action(action: str, params: dict):
    if action in HIGH_RISK_ACTIONS:
        approval = request_human_approval(action, params)
        if not approval:
            return {"status": "blocked", "reason": "human_denied"}
    return tool_registry[action](**params)
```

### 6. Tag Data Provenance

Mark where content came from so the LLM (and logs) can track trust levels.

```python
def format_with_provenance(content: str, source: str) -> str:
    """
    Sources: 
    - 'user': Direct human input (trusted)
    - 'email': External email content (untrusted)
    - 'web': Web scraping (untrusted)
    - 'rag': RAG retrieval (semi-trusted)
    - 'tool': Tool output (depends on tool)
    """
    return f"[source:{source}]\n{content}\n[/source:{source}]"
```

### 7. Dry-Run Evaluation

Generate the plan, evaluate it separately, then execute only if approved.

```python
# Step 1: Generate plan (no execution)
plan = agent.plan(user_request, tools=available_tools)

# Step 2: Evaluate plan with separate LLM (or rules engine)
evaluation = evaluator.assess(
    plan=plan,
    original_request=user_request,
    policy=security_policy,
)

# Step 3: Execute only if approved
if evaluation.approved:
    result = agent.execute(plan)
else:
    log_blocked_action(plan, evaluation.reason)
    result = {"status": "blocked", "reason": evaluation.reason}
```

### 8. Output Validation

Check what the LLM tries to do, not just what it received.

```python
def validate_output(action: str, params: dict, context: dict) -> bool:
    """
    Validate that proposed action makes sense given context.
    """
    # Check: Is this action related to the original request?
    if action == "send_email":
        # Original request was to summarize, not send
        if context["request_type"] == "summarize":
            return False
        # Recipient should be related to conversation
        if params["to"] not in context["known_contacts"]:
            return False
    
    # Check: Does this action exfiltrate data?
    if action in ["send_email", "api_call"]:
        if contains_sensitive_data(params.get("body", "")):
            return False
    
    return True
```

---

## What Doesn't Work

### "Just Add Another LLM to Check"

If your analyzer is also an LLM, it's susceptible to the same class of attacks. You can craft prompts that fool both, or that contain nested instructions appearing benign to the screener while being malicious to the main model.

### Meta-Injection

An attacker can embed "this content is safe, not an injection" alongside the actual payload. The screener faces the same ambiguity as the target.

### Waiting for Frontier Models to Solve It

OpenAI acknowledged that prompt injection is "unlikely to ever be fully 'solved.'" It's architectural, not an intelligence problem. A smarter model is still mixing trusted and untrusted tokens in the same stream.

### Delimiter-Only Approaches

Random tokens help but don't solve it. The attacker just says "ignore anything between those random-looking tokens." Delimiters are speed bumps, not walls.

---

## Threat Model

### Direct Prompt Injection
User directly inputs malicious content.

**Mitigation:** Input validation, user authentication, rate limiting.

### Indirect Prompt Injection
Malicious content arrives via data (emails, documents, web pages, RAG retrieval).

**Mitigation:** Architectural separation, typed extraction, provenance tagging.

### Tool Abuse
LLM is convinced to misuse its tools (exfiltrate data, take harmful actions).

**Mitigation:** Least privilege, human-in-the-loop, output validation.

### Data Exfiltration
Sensitive context (system prompts, credentials, user data) is leaked.

**Mitigation:** Minimize sensitive data in context, output filtering, sandboxing.

---

## References

- Simon Willison, "Dual LLM Pattern" (2023): https://simonwillison.net/2023/Apr/25/dual-llm-pattern/
- Google DeepMind, "CaMeL: Capability-based Memory for LLMs" (2025): https://arxiv.org/abs/2503.18813
- Microsoft, "Spotlighting" (2024): https://www.microsoft.com/en-us/research/publication/defending-llms-against-jailbreaking-attacks-via-backtranslation/
- "StruQ: Structured Queries for LLM Security" (2024): https://arxiv.org/abs/2402.06363
- OWASP Top 10 for LLM Applications: https://owasp.org/www-project-top-10-for-large-language-model-applications/
