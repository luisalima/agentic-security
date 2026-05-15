# Observability & Audit Trails

Detection catches malicious inputs. Observability catches malicious **behavior** — what the agent actually does with the tools it has.

Even if every defense fails, a good audit trail lets you:

- **Detect** compromise after the fact
- **Understand** what happened and what was affected
- **Recover** by knowing exactly what to undo
- **Improve** defenses based on real attack patterns

!!! info "Repo label: Defense-in-depth layer"
    Observability does not stop attacks — it lets you detect, understand, and recover from them. Treat audit trails as a supporting control alongside isolation and architectural defenses, not as a trust boundary on their own.

---

## What to Log

At a minimum, capture every tool call and its result:

| Field | Example | Why |
|-------|---------|-----|
| **Timestamp** | `2025-04-09T14:32:01Z` | Timeline reconstruction |
| **Agent/session ID** | `session-abc123` | Group related actions |
| **Tool called** | `write_file` | Know what action was taken |
| **Parameters** | `path=/etc/crontab` | Know what was targeted |
| **Result** | `success` / `blocked` | Know if it worked |
| **User who initiated** | `alice@company.com` | Accountability |

!!! warning "Don't log secrets"
    Redact API keys, tokens, passwords, and PII from logs. Log the *shape* of the action, not the sensitive content. For example, log `"wrote to .env"` but not the actual secret values.

---

## Enabling Logging in Coding Agents

Most coding agents have logging built in — it's just not always obvious where.

### Claude Code

```bash
# Logs are stored automatically
# View recent sessions:
ls ~/.claude/projects/

# Each session contains a full transcript of tool calls
```

### Amp

```bash
# Amp stores thread history with full tool call details
# Access via the Amp UI or CLI
```

### Cursor / Windsurf

These typically log to their internal databases. Check the IDE's output panel or developer tools for tool call history.

### Custom Agents

If you're building your own agent, wrap every tool call:

```python
import logging
from datetime import datetime

logger = logging.getLogger("agent.tools")

def logged_tool_call(tool_name: str, params: dict, execute_fn):
    """Wrap any tool call with logging."""
    logger.info(f"TOOL_CALL | {tool_name} | {sanitize(params)}")
    try:
        result = execute_fn(**params)
        logger.info(f"TOOL_RESULT | {tool_name} | success")
        return result
    except Exception as e:
        logger.error(f"TOOL_RESULT | {tool_name} | error | {type(e).__name__}")
        raise
```

---

## What to Watch For

### Red Flags in Tool Calls

| Pattern | What It Might Mean |
|---------|-------------------|
| `curl` or `wget` to unknown URLs | Data exfiltration |
| Writing to `~/.ssh/`, `~/.aws/`, `~/.env` | Credential tampering |
| Reading files outside the project directory | Unauthorized data access |
| Bulk file reads followed by network calls | Exfiltration sequence |
| `git push` without prior human review | Unauthorized code deployment |
| Installing unknown packages | Supply chain attack |
| Modifying CI/CD configs | Pipeline poisoning |

### Red Flags in Agent Behavior

| Pattern | What It Might Mean |
|---------|-------------------|
| Sudden spike in tool calls | Compromised agent looping |
| Tool calls at unusual hours | Automated attack |
| Accessing resources not related to the task | Lateral movement |
| Repeated failed attempts at privileged actions | Probing for access |
| Agent "explaining" why it needs more permissions | Social engineering attempt |

---

## Simple Monitoring Setup

You don't need enterprise tooling to start. A simple file-based log with periodic review goes a long way.

### Level 1: Log to File

```python
import json
from pathlib import Path
from datetime import datetime

LOG_FILE = Path("agent_audit.jsonl")

def log_action(action: dict):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        **action
    }
    with LOG_FILE.open("a") as f:
        f.write(json.dumps(entry) + "\n")
```

### Level 2: Review Script

```bash
# What did the agent do today?
cat agent_audit.jsonl | jq 'select(.tool == "write_file")' | head -20

# Any network calls?
cat agent_audit.jsonl | jq 'select(.tool | test("curl|wget|fetch|request"))' 

# Any file access outside the project?
cat agent_audit.jsonl | jq 'select(.params.path | test("^/") and (test("^/workspace") | not))'
```

### Level 3: Alerts

Set up simple alerts for high-risk patterns:

```python
HIGH_RISK_TOOLS = {"bash", "execute_code", "send_email", "git_push"}
SENSITIVE_PATHS = {".ssh", ".aws", ".env", ".git/config"}

def check_action(action: dict) -> bool:
    """Return True if action should trigger an alert."""
    if action.get("tool") in HIGH_RISK_TOOLS:
        return True
    path = action.get("params", {}).get("path", "")
    if any(s in path for s in SENSITIVE_PATHS):
        return True
    return False
```

---

## Git Is Not an Audit Trail

Git captures code changes — the *output* of the agent's work. It does **not** capture what the agent actually did:

- ❌ Files the agent read (including your secrets)
- ❌ Commands the agent executed (`curl`, `env`, `cat ~/.ssh/id_rsa`)
- ❌ Network requests the agent made
- ❌ Files the agent wrote and then deleted

An agent could exfiltrate your `.env` via a curl command and leave zero trace in the git diff. **You need tool call logging, not just version control.**

### Git Review Is Still Important

Reviewing the diff before committing is a necessary check, but it's a check on the *code*, not on the agent's behavior:

```bash
# Review code changes before committing
git diff

# Stage selectively — don't blindly add everything
git add -p
```

---

## Scaling Up

For enterprise-scale observability, audit, and compliance requirements, see [Enterprise Zero Trust](8_enterprise_zero_trust.md#audit-trails-compliance).

---

> **The cheapest incident response is the one where you know exactly what happened.** Log everything, review regularly, alert on anomalies.
