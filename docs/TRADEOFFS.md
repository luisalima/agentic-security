# Pattern Tradeoffs

A practical comparison of each defense pattern.

## Quick Reference

| Pattern | Complexity | Latency | Cost | Coverage | Production-Ready |
|---------|------------|---------|------|----------|------------------|
| Baseline | None | 1x | 1x | 0% | No |
| Delimiters | Low | 1x | 1x | ~30% | Maybe |
| Dual LLM | Medium | 2x | 2x | ~70% | Yes, with caveats |
| Typed Extraction | Medium | 2x | 2x | ~80% | Yes |
| Dry-Run | High | 3x | 3x | ~85% | Yes, with caveats |
| Combined | Very High | 4-5x | 4-5x | ~95% | For high-risk only |

---

## Pattern 0: Baseline

**What it does:** Nothing. Raw untrusted content goes to LLM with full tool access.

**Protects against:** Nothing.

**When to use:** Never in production. Useful as a benchmark.

**Tradeoffs:** None—this is the vulnerable default state.

---

## Pattern 1: Random Token Delimiters

**What it does:** Wraps untrusted content in randomized delimiters. Instructs the LLM to treat content between delimiters as data, not commands.

**Protects against:**
- Naive injections that don't account for delimiters
- Attacks crafted for static delimiter patterns
- Basic instruction override attempts

**Doesn't protect against:**
- "Ignore anything between those delimiters" attacks
- Social engineering that convinces LLM the delimiters don't apply
- Multi-turn manipulation

**Implementation complexity:** Low (~20 lines of code)

**Latency impact:** None (no extra LLM calls)

**Cost impact:** None

**When to use:** As a minimal first layer. Good defense-in-depth addition.

**Honest assessment:** Raises the bar, but a determined attacker will bypass it. Think of it as a speed bump, not a wall.

---

## Pattern 2: Dual LLM (Quarantined + Privileged)

**What it does:** 
- Quarantined LLM processes untrusted content with NO tools
- Controller validates and passes sanitized output
- Privileged LLM has tools but never sees raw untrusted content

**Protects against:**
- Tool abuse via indirect injection
- Direct command execution from untrusted content
- Most data exfiltration attempts

**Doesn't protect against:**
- Information leakage through summaries (carefully crafted content that makes the summary malicious)
- Multi-turn attacks across sessions
- If quarantined LLM's summary itself contains injection

**Implementation complexity:** Medium

**Latency impact:** 2x (two LLM calls)

**Cost impact:** 2x

**When to use:** When you have tools that can take dangerous actions (send email, API calls, file writes).

**Honest assessment:** This is the pattern that actually works. The complexity is justified. Simon Willison proposed it for good reason—it's the closest thing to real isolation we have without model-level changes.

---

## Pattern 3: Typed Data Extraction

**What it does:** Extracts structured data (JSON with strict schema) instead of passing raw text. The schema constrains what information can flow between agents.

**Protects against:**
- Freeform instruction injection
- Payload hidden in text formatting
- Long-form social engineering

**Doesn't protect against:**
- Attacks that fit within schema fields
- Schema fields that can carry intent (e.g., a "notes" field)
- Enum poisoning if enums are too permissive

**Implementation complexity:** Medium

**Latency impact:** 2x

**Cost impact:** 2x (potentially less if extraction model is smaller)

**When to use:** When you can define strict schemas for the data you need. Works well for structured tasks (email triage, form processing, data extraction).

**Honest assessment:** Underrated pattern. The key insight is that a JSON schema with max_length=50 fields simply *cannot* carry a sophisticated injection. The attack surface is the schema design itself.

**Best practice:** Keep schema fields restrictive:
- Use enums instead of strings where possible
- Set strict max_length on all string fields
- Avoid "notes" or "other" catch-all fields
- Single-word fields are safer than sentences

---

## Pattern 4: Dry-Run Evaluation

**What it does:** 
1. Generate a plan of actions (don't execute)
2. Evaluate the plan with a separate system
3. Execute only if approved

**Protects against:**
- Malicious actions getting executed without review
- Actions that don't match the original request
- Obvious exfiltration attempts

**Doesn't protect against:**
- Sophisticated attacks that also fool the evaluator
- Plans that look legitimate but have malicious intent
- Evaluator prompt injection

**Implementation complexity:** High

**Latency impact:** 3x (plan + evaluate + optional execute)

**Cost impact:** 3x

**When to use:** High-stakes applications where the cost of a wrong action is significant.

**Honest assessment:** Shifts from predicting dangerous inputs to evaluating proposed outputs—which is fundamentally easier. But you're still relying on an LLM to make security decisions. Consider adding deterministic rules on top (allowlists, rate limits).

**Best practice:** The evaluator should be a different model, or at minimum a fresh context. Ideally add rule-based checks:
```python
def validate_plan(plan):
    for action in plan.actions:
        if action.tool == "send_email":
            if action.params["to"] not in ALLOWLIST:
                return False
    return True
```

---

## Pattern 5: Combined Defense

**What it does:** Layers multiple patterns:
1. Random delimiters
2. Typed extraction
3. Plan generation
4. LLM-based evaluation
5. Deterministic output validation

**Protects against:** Multiple attack vectors simultaneously. Each layer catches what previous layers miss.

**Doesn't protect against:** 
- Novel attacks designed against this specific architecture
- Supply chain attacks (malicious dependencies)
- Insider threats

**Implementation complexity:** Very high

**Latency impact:** 4-5x

**Cost impact:** 4-5x

**When to use:** High-security applications where the asset value justifies the complexity and cost.

**Honest assessment:** This is "assume breach at each layer" thinking. Each component can fail, but the combination is robust. The question is whether the operational complexity is worth it for your use case.

**When it's NOT worth it:**
- Internal tools with trusted users
- Low-stakes applications
- High-volume, cost-sensitive applications

**When it IS worth it:**
- Customer-facing agents with tool access
- Financial or healthcare applications
- Systems handling credentials or PII
- Any system where "oops" isn't acceptable

---

## The Meta-Tradeoff

All of these patterns share a fundamental tension:

**More isolation = less usefulness**

- The safest agent has no tools → useless
- The safest agent sees no untrusted data → limited
- The safest agent can't act without approval → slow

The goal isn't perfect security (impossible). It's finding the right balance for your specific:
- Threat model
- Asset value at risk
- User experience requirements
- Operational capacity

## Recommendation

For most production systems:

1. **Start with Dual LLM** (Pattern 2) as your baseline architecture
2. **Add Typed Extraction** (Pattern 3) if you can define strict schemas
3. **Add Deterministic Output Validation** always—this is cheap and catches obvious mistakes
4. **Add Human-in-the-Loop** for truly dangerous actions (irreversible, exfiltration-capable)
5. **Layer in Dry-Run Evaluation** (Pattern 4) if you have budget and latency tolerance

Skip delimiters-only (Pattern 1) as a primary defense—it's not enough alone. Use it as one layer in a stack.

Skip the full combined approach (Pattern 5) unless you're in a high-security context with the engineering capacity to maintain it.
