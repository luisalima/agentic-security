# Isolation (Infrastructure Level)

Before changing agent code, **restrict what a compromised agent can do**. This is the lowest-hanging fruit in agentic security — you can apply it to off-the-shelf agents you don't control.

!!! tip "Try the notebooks"
    For runnable examples, see [`notebooks_securing_guide/3_isolation_infra_level/`](https://github.com/luisalima/agentic-security/tree/main/notebooks_securing_guide/3_isolation_infra_level).

---

## The Core Principle

> **Assume the agent will be compromised. Limit the damage.**

Instead of trusting the agent to behave correctly, constrain its environment so that even malicious behavior can't cause catastrophic harm.

| Approach | Requires code changes? | Works with packaged agents? |
|----------|----------------------|---------------------------|
| **Isolation** (this section) | No | ✅ Yes |
| Software architecture (next section) | Yes | ❌ No |

You can containerize, sandbox, and restrict any agent — even one you downloaded as a binary. Software defenses like dual LLM or dry-run evaluation require modifying the agent's code.

!!! info "Start here. Add software defenses later."

---

## The Isolation Layers

```
┌─────────────────────────────────────────────┐
│  1. LEAST PRIVILEGE                         │
│  Only grant the minimum tools & permissions │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│  2. CONTAINER / VM SANDBOX                  │
│  Run agent in restricted environment        │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│  3. NETWORK ISOLATION                       │
│  Limit what the agent can reach             │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│  4. SECRET & FILESYSTEM SCOPING             │
│  Only expose what's needed for the task     │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│  5. MONITORING & KILL SWITCH                │
│  Observe, rate-limit, and terminate         │
└─────────────────────────────────────────────┘
```

---

## 1. Principle of Least Privilege

Only give the agent the tools it actually needs:

```python
# ❌ Bad: agent has access to everything
tools = [read_file, write_file, execute_code, send_email, delete_db, ...]

# ✅ Good: scoped to the task
tools = [read_file, summarize]  # summarization agent doesn't need write access
```

For MCP servers, only connect the servers relevant to the task. Review each tool's permissions before granting access.

---

## 2. Container / VM Sandboxing

Run agents in isolated environments:

```bash
# Docker with restricted capabilities
docker run --rm \
  --cap-drop=ALL \
  --read-only \
  --memory=512m \
  --cpus=1 \
  --network=restricted \
  agent-image

# gVisor for stronger isolation
docker run --runtime=runsc ...

# Firecracker microVMs for maximum isolation
firectl --kernel=vmlinux --root-drive=agent.ext4
```

!!! note "Choosing a sandbox"
    **Docker + `--cap-drop=ALL`** is the easiest starting point. **gVisor** adds a user-space kernel that intercepts syscalls for stronger isolation. **Firecracker** provides full VM-level isolation with minimal overhead — used by AWS Lambda in production.

---

## 3. Network Isolation

Restrict outbound network access:

```bash
# Allow only specific endpoints
iptables -A OUTPUT -d api.openai.com -p tcp --dport 443 -j ACCEPT
iptables -A OUTPUT -d internal-api.company.com -p tcp --dport 443 -j ACCEPT
iptables -A OUTPUT -j DROP  # block everything else
```

This prevents data exfiltration even if the agent is fully compromised.

---

## 4. Secret & Filesystem Scoping

```bash
# Mount only the directories the agent needs
docker run -v /data/inbox:/inbox:ro \    # read-only input
           -v /data/output:/output:rw \  # write-only output
           agent-image

# Never mount: ~/.ssh, ~/.aws, ~/.config, /etc/passwd
# Never pass: broad API keys, admin tokens
# Do pass: scoped, short-lived, task-specific tokens
```

!!! danger "Common mistake"
    Mounting your home directory or passing long-lived admin credentials into an agent container defeats every other isolation layer.

---

## 5. Monitoring & Kill Switch

```python
# Rate-limit tool calls
MAX_TOOL_CALLS = 10
if tool_call_count > MAX_TOOL_CALLS:
    terminate_agent("Tool call limit exceeded")

# Monitor for anomalous patterns
if action.tool == "send_email" and action_count["send_email"] > 3:
    terminate_agent("Unusual email sending pattern")

# Time-bound execution
TIMEOUT = 300  # 5 minutes max
```

---

## Real-World Examples

| Platform | Isolation Approach |
|----------|-------------------|
| **Amp** | Runs code in sandboxed containers, explicit tool approval |
| **OpenAI Codex** | Cloud sandboxes with no internet access by default |
| **Devin** | Containerized dev environments with scoped permissions |
| **AWS Lambda** | Firecracker microVMs, short-lived, minimal permissions |

---

## What Isolation Can't Do

Isolation limits the **blast radius** but doesn't prevent:

- The agent producing **wrong but plausible output** (hallucinations)
- **Social engineering** through generated text
- Misuse of **legitimately granted tools** (e.g., sending a misleading email via an allowed `send_email` tool)

For those, you need the [software-level defenses](4_secure_architecture.md) in the next section.

---

## References

- **OWASP GenAI (2025)** — [Top 10 for LLM Applications v2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) — LLM06: Excessive Agency
- **Google** — [Securing Agentic AI: A Comprehensive Framework](https://services.google.com/fh/files/misc/securing_agentic_ai_a_comprehensive_framework.pdf)
- **AWS** — [Firecracker: Lightweight Virtualization for Serverless Computing](https://www.usenix.org/conference/nsdi20/presentation/agache)
- **gVisor** — [Container Runtime Sandbox](https://gvisor.dev/)
