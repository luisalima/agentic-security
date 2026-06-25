"""Helpers for redacting sensitive values from scanner findings."""

from __future__ import annotations

import re

SECRET_ASSIGNMENT_PATTERN = re.compile(
    r"\b((?:api[_\s-]?key|password|secret|token|credential)\s*(?:is|=|:)\s*)"
    r"[^&\s'\"<>]+",
    re.IGNORECASE,
)
QUERY_SECRET_PATTERN = re.compile(
    r"\b((?:api[_-]?key|key|password|secret|token|credential|data|content)=)"
    r"[^&\s'\"<>]+",
    re.IGNORECASE,
)
BEARER_TOKEN_PATTERN = re.compile(r"\b(Bearer\s+)[A-Za-z0-9._~+/=-]+", re.IGNORECASE)
DSN_CREDENTIAL_PATTERN = re.compile(r"(://)[^:\s/@]+:[^@\s]+@")
OPENAI_KEY_PATTERN = re.compile(r"\bsk-[A-Za-z0-9_-]{4,}\b")


def redact_sensitive_text(text: str) -> str:
    """Redact common secret values while preserving useful finding context."""
    redacted = SECRET_ASSIGNMENT_PATTERN.sub(r"\1[REDACTED]", text)
    redacted = QUERY_SECRET_PATTERN.sub(r"\1[REDACTED]", redacted)
    redacted = BEARER_TOKEN_PATTERN.sub(r"\1[REDACTED]", redacted)
    redacted = DSN_CREDENTIAL_PATTERN.sub(r"\1[REDACTED]@", redacted)
    redacted = OPENAI_KEY_PATTERN.sub("[REDACTED]", redacted)
    return redacted
