# Architectural Guidelines for Agentic AI Security

## The Fundamental Problem

LLMs process instructions and data in the same channel (the context window). There is no architectural separation between "do this" and "here's some information." This is why prompt injection is fundamentally different from traditional injection attacks — there's no equivalent to parameterized queries.

---

## Maturity Levels

This is an organizational *maturity model* — where teams typically sit on the security curve, in increasing order of rigor. It is distinct from the [Defense Levels](../index.md#defense-levels) in the Guide, which name specific technique categories (Detection, Prompt Engineering, Isolation, Secure Architecture, Defense in Depth). A team at any maturity level can adopt any combination of Defense Levels.

### Hope and Prayer (most common)

- Default model safety
- "Don't put anything too dangerous in production"
- Pray attackers don't find you

**Assessment:** Unacceptable for anything handling real data or actions.

### Probabilistic Guardrails

- Input classifiers (Lakera, NeMo, Prompt Shields)
- Output filtering
- Pattern matching

**Assessment:** Can catch many common attacks in benchmarks, but adaptive attacks still get through. Use as one layer, not as the primary control.

### Defense in Depth

- Everything in Probabilistic Guardrails, plus sandboxing
- Least privilege
- Human-in-the-loop for risky actions
- Rate limiting, monitoring, logging
- Assume breach, limit blast radius

**Assessment:** Reasonable for most production systems. Accept that injection will eventually succeed; focus on containment.

### Architectural Separation

- Dual LLM patterns
- Typed data extraction
- Capability-based security (CaMeL)
- Symbolic references

**Assessment:** Strongest defense but high implementation complexity. Worth it for high-risk systems.

---

## Cross-Pattern Principles

These principles apply across every pattern in [Guide §4: Secure Architecture](../guide/4_secure_architecture.md). Worth keeping front-of-mind regardless of which patterns you pick:

- **Scope tools aggressively.** Give each agent the minimum set it actually needs. An email assistant doesn't need `delete_email`; a summarizer doesn't need write tools at all.
- **Keep untrusted data and privileged actions from meeting directly.** Put a deterministic controller between them — not another LLM.
- **Prefer typed data over freeform text** between agents. Tight schemas are one practical security boundary.
- **Outbound and irreversible actions require explicit confirmation.** Never agent-decided.
- **Tag every value with its source.** Provenance is what makes capability-based policies possible.
- **Log every tool call and trust-boundary crossing.** Audit trails don't stop attacks; they're what lets you detect a compromised agent after the fact, understand the blast radius, and recover. See [Observability & Audit Trails](../guide/1b_observability.md).

For full implementations (Dual LLM, Typed Extraction, Symbolic References, Dry-Run Evaluation, Tool/MCP Validation, CaMeL), see the [Guide chapter](../guide/4_secure_architecture.md).

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

The full threat-modeling workflow lives in [Threat Model](threat_model.md). At minimum, walk through the [Lethal Trifecta](../principles.md#the-lethal-trifecta) for your system, draw your trust boundaries, and identify the blast radius of a fully compromised agent.

---

## References

- Simon Willison (2023) — [Dual LLM Pattern](https://simonwillison.net/2023/Apr/25/dual-llm-pattern/)
- Google DeepMind (2025) — [CaMeL: Defeating Prompt Injections by Design](https://arxiv.org/abs/2503.18813)
- Hines et al., Microsoft (2024) — [Defending Against Indirect Prompt Injection Attacks With Spotlighting](https://arxiv.org/abs/2403.14720)
- Chen et al. (2024) — [StruQ: Defending Against Prompt Injection with Structured Queries](https://arxiv.org/abs/2402.06363)
- OWASP — [Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)
