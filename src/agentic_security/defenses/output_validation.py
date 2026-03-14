"""
Deterministic output validation for agentic systems.

Validates tool calls and execution plans against rule-based policies
before they are executed. Acts as the final safety net in a
defense-in-depth pipeline.

This module extracts the validation patterns used across the dual LLM
controller, dry-run evaluator, and combined defense layers.
"""

from __future__ import annotations

DEFAULT_KNOWN_CONTACTS = {"alice@company.com", "bob@external.com"}


class OutputValidator:
    """Rule-based validator for tool calls and execution plans."""

    def __init__(self, known_contacts: set[str] | None = None):
        self.known_contacts = (
            known_contacts if known_contacts is not None else DEFAULT_KNOWN_CONTACTS
        )

    def validate_tool_call(
        self,
        tool_name: str,
        params: dict,
    ) -> tuple[bool, str]:
        """Validate a single tool call against deterministic rules.

        Args:
            tool_name: Name of the tool being called.
            params: Parameters for the tool call.

        Returns:
            (valid, reason) tuple.
        """
        if tool_name in ("send_email", "forward_email"):
            recipient = params.get("to", "")
            if recipient not in self.known_contacts:
                return False, f"Unknown recipient: {recipient}"
        return True, "OK"

    def validate_plan(
        self,
        actions: list,
        user_request: str,
    ) -> tuple[bool, list[str]]:
        """Validate a list of planned actions against the user's request.

        Each action should have ``tool`` and ``params`` attributes (e.g.
        a :class:`~agentic_security.defenses.dry_run.PlannedAction`).

        Args:
            actions: List of planned actions to validate.
            user_request: Original user request for intent matching.

        Returns:
            (all_valid, concerns) tuple where concerns lists any issues found.
        """
        concerns: list[str] = []

        for action in actions:
            tool = action.tool if hasattr(action, "tool") else action.get("tool", "")
            params = action.params if hasattr(action, "params") else action.get("params", {})

            valid, reason = self.validate_tool_call(tool, params)
            if not valid:
                concerns.append(reason)

            # Intent mismatch: summarize requests should not trigger sends
            if "summarize" in user_request.lower():
                if tool in ("send_email", "forward_email"):
                    concern = "Summarize requests should not send emails"
                    if concern not in concerns:
                        concerns.append(concern)

        return len(concerns) == 0, concerns
