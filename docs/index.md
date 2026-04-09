# Agentic Security

**The definitive guide to securing AI agents against prompt injection.**

AI agents are vulnerable to prompt injection attacks. This is especially concerning since they can take actions and access (and edit) private information. This guide provides practical defense patterns — from simple detection to secure multi-agent architectures.

> **Start here:** [Principles](principles.md) — The mental model for agentic security, before you touch any code.

---

## The Problem

Your AI agent is vulnerable if it has the **Lethal Trifecta**:

1. **Tool Access** — Can take real-world actions
2. **Untrusted Input** — Processes external data (emails, documents, web, RAG)
3. **Sensitive Context** — Has access to credentials, PII, or private data

Unlike traditional injection attacks (SQL injection, XSS), there's no equivalent to parameterized queries for LLMs. Instructions and data flow through the same channel.

---

## Threat Model

Your threat model is simple: **the agent can go rogue.** Ask yourself: *if this agent is fully compromised right now, what's the worst that can happen?*

| Blast Radius | Example | Acceptable? |
|-------------|---------|-------------|
| Agent sends 1 email to wrong person | Scoped token, approval required | Usually yes |
| Agent exfiltrates all contacts | Full contact access, outbound network | Usually no |
| Agent pushes malicious code to prod | Git credentials, CI/CD access | Never |
| Agent deletes database | DB write credentials in env | Never |

**If the blast radius is unacceptable, you need more isolation — not better prompts.**

→ Full threat modeling guide: [Threat Model](reference/threat_model.md)

---

## Defense Levels

| Level | Approach | What Changes | Protection |
|-------|----------|--------------|------------|
| **1. Detection** | Filter malicious inputs | Add a library | ~95% |
| **2. Prompt Engineering** | Harden the prompt | Change prompts | +marginal |
| **3. Isolation (Infra)** | Containers, network, permissions | Wrap the agent | +significant |
| **4. Secure Architecture (Software)** | Dual LLM, dry-run, typed extraction | Redesign system | +significant |
| **5. Defense in Depth** | Layer everything | Full investment | ~99%* |

*Nothing is 100%. The goal is raising the bar high enough to deter attacks and limit blast radius.

---

## Getting Started

Explore the [Guide](guide/0_vulnerabilities.md) to understand each defense level, or jump to the [Cheatsheet](reference/cheatsheet.md) for a quick reference.

For runnable code examples, see the [notebooks](https://github.com/luisalima/agentic-security/tree/main/notebooks) in the repository.
