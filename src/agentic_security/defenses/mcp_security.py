"""
MCP (Model Context Protocol) security defenses.

Detects MCP-specific attack vectors:
- Tool description poisoning: hidden instructions in tool metadata
- Rug pull detection: tool definition changes after initial approval
- Cross-origin attacks: tools requesting access beyond their scope
- Supply chain risks: unsigned or unverified MCP servers

Based on:
- OWASP Top 10 for Agentic Applications (2026), ASI02 & ASI04
- Invariant Labs MCPTox research
- OWASP MCP Top 10
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field


@dataclass
class MCPServerConfig:
    """Configuration for an MCP server connection."""

    name: str
    command: str
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    tools: list[dict] = field(default_factory=list)
    url: str | None = None


@dataclass
class MCPScanResult:
    """Result of scanning an MCP server configuration."""

    server_name: str
    safe: bool
    concerns: list[str] = field(default_factory=list)
    tool_concerns: dict[str, list[str]] = field(default_factory=dict)


# Patterns indicating hidden instructions in tool descriptions
TOOL_POISONING_PATTERNS: list[str] = [
    # Instructions to perform actions
    r"\b(?:always|before|after)\s+(?:first|also|then)?\s*(?:send|email|forward|read|fetch|post|call|execute|run)\b",
    # Credential/secret access
    r"\b(?:read|get|access|retrieve|check)\s+(?:the\s+)?(?:api[_\s]?key|secret|credential|password|token|env(?:ironment)?)\b",
    # URL with data exfiltration patterns
    r"https?://[^\s]+\?[^\s]*(?:key|token|secret|data|content)=",
    # Setup/verification deception
    r"\b(?:setup|verification|activation|license)\s+(?:required|step|needed)\b",
    # Override/ignore patterns
    r"\b(?:override|ignore|bypass|skip)\s+(?:all\s+)?(?:previous\s+)?(?:instructions?|rules?|policies?)\b",
    # IMPORTANT/NOTE directives (common in poisoned descriptions)
    r"\b(?:IMPORTANT|NOTE|REQUIRED|MANDATORY)\s*:",
    # BCC/CC injection
    r"\b(?:bcc|blind.?copy|always.?cc)\b",
]

# Suspicious environment variable names that suggest credential access
SENSITIVE_ENV_VARS: set[str] = {
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_ACCESS_KEY_ID",
    "GITHUB_TOKEN",
    "GH_TOKEN",
    "DATABASE_URL",
    "DB_PASSWORD",
    "SECRET_KEY",
    "PRIVATE_KEY",
    "SSH_KEY",
    "GOOGLE_APPLICATION_CREDENTIALS",
}


class MCPScanner:
    """Scans MCP server configurations for security concerns."""

    def __init__(
        self,
        max_description_length: int = 500,
        allowed_servers: set[str] | None = None,
    ):
        self.max_description_length = max_description_length
        self.allowed_servers = allowed_servers

    def scan_server(self, server: MCPServerConfig) -> MCPScanResult:
        """Scan a single MCP server configuration for security concerns."""
        concerns: list[str] = []
        tool_concerns: dict[str, list[str]] = {}

        # Check allowlist
        if self.allowed_servers is not None and server.name not in self.allowed_servers:
            concerns.append(f"Server '{server.name}' is not in the allowed servers list")

        # Check for sensitive env vars being passed
        for env_var in server.env:
            if env_var.upper() in SENSITIVE_ENV_VARS:
                concerns.append(
                    f"Sensitive environment variable passed to server: {env_var}"
                )

        # Scan each tool definition
        for tool in server.tools:
            name = tool.get("name", "unknown")
            description = tool.get("description", "")
            tc = self._scan_tool_description(name, description)

            # Also scan inputSchema parameter descriptions
            input_schema = tool.get("inputSchema", {})
            props = input_schema.get("properties", {})
            for param_name, param_def in props.items():
                if isinstance(param_def, dict):
                    param_desc = param_def.get("description", "")
                    if param_desc:
                        param_issues = self._scan_text_for_poisoning(param_desc)
                        for issue in param_issues:
                            tc.append(f"Parameter '{param_name}': {issue}")

            if tc:
                tool_concerns[name] = tc

        return MCPScanResult(
            server_name=server.name,
            safe=len(concerns) == 0 and len(tool_concerns) == 0,
            concerns=concerns,
            tool_concerns=tool_concerns,
        )

    def _scan_tool_description(self, name: str, description: str) -> list[str]:
        """Scan a single tool description for poisoning."""
        issues: list[str] = []

        if len(description) > self.max_description_length:
            issues.append(
                f"Description length ({len(description)}) exceeds "
                f"maximum ({self.max_description_length})"
            )

        issues.extend(self._scan_text_for_poisoning(description))
        return issues

    def _scan_text_for_poisoning(self, text: str) -> list[str]:
        """Scan text for tool poisoning patterns."""
        issues: list[str] = []
        for pattern in TOOL_POISONING_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                issues.append(f"Poisoning pattern detected: '{match.group(0)}'")
        return issues

    def scan_manifest(self, servers: list[MCPServerConfig]) -> list[MCPScanResult]:
        """Scan a list of MCP server configurations."""
        return [self.scan_server(server) for server in servers]


class RugPullDetector:
    """Detects tool definition changes between sessions (rug pull attacks).

    Stores hashes of tool definitions and alerts when they change
    without explicit approval.
    """

    def __init__(self) -> None:
        self._known_hashes: dict[str, str] = {}

    def _hash_tool(self, tool: dict) -> str:
        """Create a deterministic hash of a tool definition."""
        canonical = json.dumps(tool, sort_keys=True, ensure_ascii=True)
        return hashlib.sha256(canonical.encode()).hexdigest()

    def register_tools(self, server_name: str, tools: list[dict]) -> None:
        """Register (approve) a set of tool definitions."""
        for tool in tools:
            name = tool.get("name", "unknown")
            key = f"{server_name}:{name}"
            self._known_hashes[key] = self._hash_tool(tool)

    def check_tools(self, server_name: str, tools: list[dict]) -> list[str]:
        """Check tools against registered hashes. Returns list of changed tool names."""
        changed: list[str] = []
        for tool in tools:
            name = tool.get("name", "unknown")
            key = f"{server_name}:{name}"

            current_hash = self._hash_tool(tool)

            if key in self._known_hashes:
                if self._known_hashes[key] != current_hash:
                    changed.append(name)

        return changed


def parse_mcp_config(config: dict) -> list[MCPServerConfig]:
    """Parse an MCP configuration file (e.g., ~/.cursor/mcp.json).

    Args:
        config: Parsed JSON from an MCP config file. Expected format:
            {"mcpServers": {"name": {"command": ..., "args": [...], "env": {...}}}}

    Returns:
        List of MCPServerConfig objects.
    """
    servers: list[MCPServerConfig] = []
    mcp_servers = config.get("mcpServers", {})

    for name, server_config in mcp_servers.items():
        servers.append(
            MCPServerConfig(
                name=name,
                command=server_config.get("command", ""),
                args=server_config.get("args", []),
                env=server_config.get("env", {}),
                tools=server_config.get("tools", []),
                url=server_config.get("url"),
            )
        )

    return servers
