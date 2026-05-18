# Principles of Agentic Security

**Read this first.** This document gives you the mental model. The [notebooks](https://github.com/luisalima/agentic-security/tree/main/notebooks) show you the implementation.

---

## 1. The Threat Model

### The Lethal Trifecta

An AI agent becomes catastrophically vulnerable when it has **all three**:

| Factor | Example |
|--------|---------|
| **Access to private data** | Emails, files, credentials, PII, internal docs |
| **Exposure to untrusted content** | Emails, web pages, RAG documents, user uploads — any text or images controlled by a malicious attacker |
| **Ability to exfiltrate** | Send emails, make API calls, write to external services — any mechanism to externally communicate and steal data |

**Remove any one factor and the attack surface shrinks dramatically.**

The problem is that most useful agents have all three. Your coding assistant has access to your codebase, reads untrusted code from repos, and can execute commands that exfiltrate data. Your email assistant reads your private emails, processes untrusted message content, and can reply/forward messages externally. Your personal assistant knows your schedule, browses untrusted web pages, and can send messages (and sometimes make purchases) on your behalf.

**Most personal assistants and coding assistants are instances of the lethal trifecta.**

---

## 2. The Axioms

### Axiom 1: Assume all agents will be compromised

Any agent that reads untrusted data can be prompt-injected. This is not a bug, it is an inherent property of how LLMs work. Instructions and data flow through the same channel (the context window), and there is no equivalent to parameterized queries.

> Your threat model for AI is: **never trust any agent.**

Treat every agent as a very bright intern who unfortunately doesn't know very well how to distinguish good from evil and who might follow instructions from anyone, from the user and system prompt, to the attacker hiding instructions in a PDF.

### Axiom 2: Do not rely only on agent-level settings

You cannot rely on permissions baked into tools or agent configurations alone.

Real example: while building letai, an orchestrator of coding agents, the CTO agent was configured as an orchestrator that should never write code. Edit permissions were removed via the agent's settings and the prompt was fine-tuned to say "you never write code, you are the CTO".

What happened:

```
Removed Edit tool    → Agent used sed to edit files
                       "oh, I can't use Edit, let me try sed"

Removed sed          → Agent used awk with redirect
                       "sed isn't available, let me try awk"

Removed awk          → Agent tried echo with redirect
                       ...you get the idea
```

**The agent will find a way around software-level restrictions to be helpful.** It's creative. It is not optimizing for intention, but rather for task completion.

### Axiom 3: Agents ignore human override

Multiple documented cases of agents ignoring explicit "STOP" commands:

- Agents announcing they will execute a destructive action, the human typing "STOP", and the agent proceeding anyway
- Agents acknowledging the stop command and then continuing with the exact action they were told to stop
- Agents interpreting "don't do X" as context about X, then doing X

**You cannot rely on the agent respecting human-in-the-loop controls at the prompt level.** Agent output is probabilistic, not deterministic. There will be instances where even the most well designed agent will fail to comply with instructions (view instructions a suggestions).

### Axiom 4: Deterministically deny access

> The key is to **deterministically** remove, or rather not provide, access. As a **wrapper**. Not as a setting.

- Don't configure the agent to not use a tool — **don't give it the tool**
- Don't tell the agent to not access a directory — **don't mount the directory**
- Don't ask the agent to not use the network — **block the network**
- Don't rely on the agent to not read secrets — **don't inject the secrets**

etc...

**Always enforce at the infrastructure level, and never rely on the prompt level.**

---

## 3. The Pattern

For any system you're designing, split the agent into stages with hard boundaries:

```mermaid
flowchart TD
    A["1. READ & PROPOSE\nAgent can only read data and propose actions.\nNo execution capability.\n⚠️ Assume this agent IS compromised."]
    B["2. APPROVE\nHuman reviews and approves the actions.\n(Or a separate evaluator agent — this also has risks that must be addressed.)"]
    C["3. EXECUTE\nDeterministic execution of approved actions.\nAs little LLM as possible. Ideally no LLM at all."]
    A -- "proposed actions" --> B
    B -- "approved actions only" --> C
```

**Why this works:** Even if the proposer is fully compromised by a prompt injection, it can only *propose* malicious actions. The approval step catches the mismatch between user intent and proposed actions. The executor is deterministic — no LLM to manipulate.

→ *Deep dive:* [Dry-run notebook](https://github.com/luisalima/agentic-security/blob/main/notebooks/4_secure_architecture_software/3_dry_run.py)

---

## 4. Securing Pre-Packaged Agents

You don't always control the agent's code. Here's how to secure agents you can't modify.

### Coding Agents (Cursor, Windsurf, Claude Code, Amp, etc.)

These have the full trifecta: they read untrusted code, have filesystem/shell access, and see your environment variables and secrets.

| Control | How |
|---------|-----|
| **Isolate the environment** | Run in a container or VM. Never on your host machine, never with sensitive credentials |
| **Scope filesystem access** | Mount only the project directory, read-only where possible |
| **Block network** | Allow only package registries and the LLM API. Block everything else |
| **Scope secrets** | Use project-scoped tokens with minimum permissions. Never expose your main AWS/GCP credentials |
| **Review before commit** | The agent proposes changes. You review the diff. Never auto-commit + push |
| **Separate environments** | Promote from dev to staging to prod, ideally with a human in the loop |

### Personal Assistants / Agentic Loops (OpenClaw, NanoClaw, etc.)

These are very dangerous: they read your emails/messages, have access to your accounts, and can communicate externally on your behalf.

| Control | How |
|---------|-----|
| **Isolate each capability** | Reading agent in one container, sending agent in another |
| **Require approval for outbound** | Any external communication (email, message, API call) needs explicit human approval — enforced at the infrastructure level, not the prompt level |
| **Scope API access** | Read-only tokens for data access. Separate write-scoped tokens only for the executor |
| **Time-bound sessions** | Short-lived tokens that expire. No persistent credentials |
| **Monitor and rate-limit** | Alert on unusual patterns (bulk sends, new recipients, large data transfers) |
| **No credential forwarding** | The agent gets a task-scoped proxy, never your actual credentials |

### MCP Servers / Tool Providers

Any tool server the agent connects to is an extension of the attack surface.

| Control | How |
|---------|-----|
| **Audit the manifest** | Review what tools and permissions the server declares |
| **Principle of least privilege** | Only connect the MCP servers needed for the task |
| **Validate tool schemas** | Ensure tool parameters match expectations |
| **Run servers in isolation** | Each MCP server in its own container with scoped access |

→ *Deep dive:* [Tool validation notebook](https://github.com/luisalima/agentic-security/blob/main/notebooks/4_secure_architecture_software/4_tool_validation.py)

---

## 5. The Implementation Path

Start with what's easiest and works on anything, then add layers:

### Step 1: Isolation (works on any agent, no code changes)

**This is the lowest-hanging fruit.** Containerize, restrict network, scope permissions.

→ [Isolation notebooks](https://github.com/luisalima/agentic-security/tree/main/notebooks/3_isolation_infra_level)

### Step 2: Software Architecture (requires code changes)

If you're building your own agent: dual LLM, typed extraction, dry-run evaluation.

→ [Secure architecture notebooks](https://github.com/luisalima/agentic-security/tree/main/notebooks/4_secure_architecture_software)

### Step 3: Detection (layer on top)

Add input scanning, canary tokens, and monitoring.

→ [Detection notebooks](https://github.com/luisalima/agentic-security/tree/main/notebooks/1_detection)

### Step 4: Defense in Depth (combine everything)

No single defense is sufficient. Layer them.

→ [Defense in depth notebooks](https://github.com/luisalima/agentic-security/tree/main/notebooks/5_defense_in_depth)

---

## Summary

| Principle | One-liner |
|-----------|-----------|
| **Lethal Trifecta** | Private data access + untrusted content + exfiltration ability = vulnerable system |
| **Assume compromise** | Any agent that reads data can be hijacked |
| **Never trust settings** | Agents bypass software restrictions creatively |
| **Agents ignore "STOP"** | Prompt-level kill switches don't work |
| **Deterministic denial** | Enforce at infrastructure level, not prompt level |
| **Split the pipeline** | Read → Propose → Approve → Execute |
| **Isolation first** | Containers and permissions before code changes |
| **Defense in depth** | No single layer is enough |

---

**Nothing is 100% secure.** The goal is raising the bar high enough to deter attacks and limiting the blast radius when (not if) something gets through.
