"""
Memory and context poisoning defenses for agentic systems.

Detects and prevents attacks that corrupt persistent agent memory, RAG
databases, or conversation context to influence future decisions.

Attack vectors addressed:
- Instruction injection into memory stores
- Context manipulation across sessions
- RAG document poisoning with embedded instructions
- Memory escalation (cached credentials reused by non-admin users)

Based on:
- OWASP Top 10 for Agentic Applications (2026), ASI06
- Slack AI data exfiltration incident (Aug 2024)
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta


@dataclass
class MemoryEntry:
    """A single entry in an agent's memory store."""

    key: str
    value: str
    source: str  # e.g., "user_input", "tool:read_email", "rag:document_123"
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    expires_at: datetime | None = None
    trust_level: str = "untrusted"  # "trusted", "untrusted", "verified"
    content_hash: str = ""

    def __post_init__(self):
        if not self.content_hash:
            self.content_hash = hashlib.sha256(self.value.encode()).hexdigest()[:16]


@dataclass
class MemoryScanResult:
    """Result of scanning a memory entry for poisoning."""

    key: str
    safe: bool
    concerns: list[str] = field(default_factory=list)


# Patterns indicating instruction injection in memory content
MEMORY_POISONING_PATTERNS: list[str] = [
    # Action directives hidden in content
    r"\b(?:always|from now on|in the future|going forward)\s+"
    r"(?:send|forward|email|include|cc|bcc)\b",
    # Policy/instruction override
    r"\b(?:new policy|updated policy|policy change|updated instructions?|new instructions?)\s*:",
    # Credential/secret references
    r"\b(?:api[_\s]?key|password|secret|token|credential)\s*(?:is|=|:)\s*\S+",
    # Compliance/audit deception
    r"\b(?:compliance|audit|mandatory|required by)\s+(?:requires?|step|verification)\b",
    # Role escalation
    r"\b(?:admin|administrator|root|superuser)\s+(?:access|privileges?|permissions?|rights?)\b",
    # Override patterns
    r"\b(?:override|ignore|disregard|bypass)\s+(?:all\s+)?(?:previous\s+)?(?:settings?|rules?|policies?|restrictions?)\b",
]

# Sources considered trusted by default
DEFAULT_TRUSTED_SOURCES: set[str] = {
    "user_input",
    "system",
    "admin",
}


class MemoryGuard:
    """Validates and sanitizes content before it enters agent memory.

    Implements memory isolation, provenance tracking, and poisoning detection
    to prevent persistent manipulation of agent behavior.
    """

    def __init__(
        self,
        trusted_sources: set[str] | None = None,
        default_ttl: timedelta | None = None,
        max_entry_length: int = 5000,
    ):
        self.trusted_sources = trusted_sources or DEFAULT_TRUSTED_SOURCES
        self.default_ttl = default_ttl or timedelta(hours=24)
        self.max_entry_length = max_entry_length

    def scan_entry(self, entry: MemoryEntry) -> MemoryScanResult:
        """Scan a memory entry for poisoning indicators.

        Args:
            entry: The memory entry to validate.

        Returns:
            MemoryScanResult with safety assessment and any concerns.
        """
        concerns: list[str] = []

        # Check length
        if len(entry.value) > self.max_entry_length:
            concerns.append(
                f"Entry length ({len(entry.value)}) exceeds maximum ({self.max_entry_length})"
            )

        # Check for poisoning patterns
        for pattern in MEMORY_POISONING_PATTERNS:
            match = re.search(pattern, entry.value, re.IGNORECASE)
            if match:
                concerns.append(f"Poisoning pattern detected: '{match.group(0)}'")

        # Untrusted sources get extra scrutiny
        if entry.source not in self.trusted_sources:
            if entry.trust_level != "verified":
                # Check if untrusted content contains directive-like language
                directive_patterns = [
                    r"\b(?:you must|you should|always|never|do not)\b.*"
                    r"\b(?:send|forward|email|call|execute)\b",
                    r"\b(?:step \d|instruction \d|rule \d)\b",
                ]
                for pattern in directive_patterns:
                    match = re.search(pattern, entry.value, re.IGNORECASE)
                    if match:
                        concerns.append(
                            f"Untrusted source contains directive: '{match.group(0)}'"
                        )

        return MemoryScanResult(
            key=entry.key,
            safe=len(concerns) == 0,
            concerns=concerns,
        )

    def create_safe_entry(
        self,
        key: str,
        value: str,
        source: str,
    ) -> tuple[MemoryEntry, MemoryScanResult]:
        """Create a memory entry with automatic scanning and TTL.

        Args:
            key: Memory key.
            value: Content to store.
            source: Origin of the data.

        Returns:
            Tuple of (MemoryEntry, MemoryScanResult).
        """
        trust = "trusted" if source in self.trusted_sources else "untrusted"
        entry = MemoryEntry(
            key=key,
            value=value,
            source=source,
            trust_level=trust,
            expires_at=datetime.now(UTC) + self.default_ttl,
        )
        result = self.scan_entry(entry)
        return entry, result


class MemoryStore:
    """Isolated memory store with provenance tracking and expiration.

    Provides per-session and per-user isolation to prevent cross-session
    context poisoning.
    """

    def __init__(self, guard: MemoryGuard | None = None):
        self.guard = guard or MemoryGuard()
        self._store: dict[str, dict[str, MemoryEntry]] = {}
        self._mutation_log: list[dict] = []

    def write(
        self,
        namespace: str,
        key: str,
        value: str,
        source: str,
    ) -> tuple[bool, MemoryScanResult]:
        """Write a value to memory with validation.

        Args:
            namespace: Isolation namespace (e.g., user_id, session_id).
            key: Memory key.
            value: Content to store.
            source: Origin of the data.

        Returns:
            (accepted, scan_result) — accepted is False if poisoning detected.
        """
        entry, result = self.guard.create_safe_entry(key, value, source)

        self._mutation_log.append({
            "action": "write",
            "namespace": namespace,
            "key": key,
            "source": source,
            "safe": result.safe,
            "concerns": result.concerns,
        })

        if result.safe:
            if namespace not in self._store:
                self._store[namespace] = {}
            self._store[namespace][key] = entry

        return result.safe, result

    def read(self, namespace: str, key: str) -> str | None:
        """Read a value from memory, checking expiration.

        Args:
            namespace: Isolation namespace.
            key: Memory key.

        Returns:
            The stored value, or None if not found/expired.
        """
        ns = self._store.get(namespace, {})
        entry = ns.get(key)
        if entry is None:
            return None

        if entry.expires_at and datetime.now(UTC) > entry.expires_at:
            del ns[key]
            return None

        return entry.value

    def clear_namespace(self, namespace: str) -> None:
        """Clear all entries in a namespace (session wipe)."""
        self._store.pop(namespace, None)

    def get_mutation_log(self) -> list[dict]:
        """Return the full mutation log for audit."""
        return list(self._mutation_log)

    def get_blocked_writes(self) -> list[dict]:
        """Return all writes that were blocked due to poisoning detection."""
        return [m for m in self._mutation_log if not m["safe"]]
