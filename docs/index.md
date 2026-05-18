---
hide:
  - navigation
  - toc
---

<div class="hero" markdown>

# Agentic Security

<p class="subtitle">
A step-by-step guide to securing AI agents against prompt injection, with defense patterns from simple detection to secure multi-agent architectures.
</p>

[:octicons-rocket-16: &nbsp; Start with Principles](principles.md){ .md-button .md-button--primary }
[:octicons-book-16: &nbsp; Read the Guide](guide/0_vulnerabilities.md){ .md-button }

</div>

---

## The Lethal Trifecta

Coined by Simon Willison: your AI agent is vulnerable if it has all three.

<div class="grid cards" markdown>

-   :material-shield-key:{ .lg .middle } __Access to Private Data__

    ---

    The agent can read your emails, files, credentials, PII — one of the most common purposes of tools.

-   :material-earth:{ .lg .middle } __Exposure to Untrusted Content__

    ---

    Text or images controlled by a malicious attacker can reach the LLM: emails, web pages, RAG documents, user uploads.

-   :material-export:{ .lg .middle } __Ability to Exfiltrate__

    ---

    The agent can take outbound actions: send emails, make API calls, write to external services.

</div>

Unlike SQL injection or XSS, there's **no parameterized-query equivalent for LLMs**. Instructions and data flow through the same channel.

---

## Threat Model, in a Nutshell

**Assume the agent can go rogue.** Ask yourself: *if this agent is fully compromised right now, what's the worst that can happen?* Then design the system so that the worst case is still acceptable.

| Blast Radius | Example | Acceptable? |
|-------------|---------|-------------|
| Agent sends 1 email to wrong person | Scoped token, approval required | Usually yes |
| Agent exfiltrates all contacts | Full contact access, outbound network | Usually no |
| Agent pushes malicious code to prod | Git credentials, CI/CD access | Never |
| Agent deletes database | DB write credentials in env | Never |

!!! tip "Rule of thumb"
    If the blast radius is unacceptable, you need **deterministic controls (isolation, scoped tokens, schema validation), not better prompts**.

→ Full threat modeling guide: [Threat Model](reference/threat_model.md)

---

## Defense Levels

<div class="grid cards" markdown>

-   :material-filter-variant:{ .lg .middle } __1. Detection__

    ---

    Filter malicious inputs before they reach your agent. Useful first layer for common attacks.

    [:octicons-arrow-right-24: Detection](guide/1_detection.md)

-   :material-text-box-edit:{ .lg .middle } __2. Prompt Engineering__

    ---

    Harden the system prompt. Marginal protection — never rely on this alone.

    [:octicons-arrow-right-24: Prompt Engineering](guide/2_prompt_engineering.md)

-   :material-cube-outline:{ .lg .middle } __3. Isolation (Infra)__

    ---

    Containers, network egress controls, least-privilege credentials. Primary blast-radius control.

    [:octicons-arrow-right-24: Isolation](guide/3_isolation.md)

-   :material-sitemap:{ .lg .middle } __4. Secure Architecture__

    ---

    Dual-LLM patterns, dry-run mode, typed extraction. Redesign the system.

    [:octicons-arrow-right-24: Secure Architecture](guide/4_secure_architecture.md)

-   :material-layers-triple:{ .lg .middle } __5. Defense in Depth__

    ---

    Layer everything. Raises attacker cost and limits single-layer failures.

    [:octicons-arrow-right-24: Defense in Depth](guide/5_defense_in_depth.md)

</div>

---

## Supporting Systems

Agents don't run in isolation. Two surrounding surfaces have their own attack patterns and defenses.

<div class="grid cards" markdown>

-   :material-toolbox-outline:{ .lg .middle } __MCP Security__

    ---

    Tool poisoning, rug pulls, and supply-chain risks in MCP servers and tool providers.

    [:octicons-arrow-right-24: MCP Security](guide/9_mcp_security.md)

-   :material-database-lock:{ .lg .middle } __Memory & Context Security__

    ---

    Memory poisoning, namespace isolation, and provenance tracking across agent runs.

    [:octicons-arrow-right-24: Memory Security](guide/10_memory_security.md)

</div>

---

## Getting Started

- :material-map: &nbsp; New here? Read the [Principles](principles.md) first, the mental model before any code.
- :material-book-multiple: &nbsp; Working through the material? Start the [Guide](guide/0_vulnerabilities.md) at Vulnerabilities.
- :material-book-open-page-variant: &nbsp; Just need the answer? Jump to the [Cheatsheet](reference/cheatsheet.md).
- :material-notebook: &nbsp; Want runnable code? See the [notebooks](https://github.com/luisalima/agentic-security/tree/main/notebooks) in the repository.
