"""Tests for deterministic output validation."""

import pytest

from agentic_security.defenses.output_validation import OutputValidator


class TestValidateToolCall:
    @pytest.fixture()
    def validator(self):
        return OutputValidator()

    # ------------------------------------------------------------------
    # Dangerous tool calls should be blocked
    # ------------------------------------------------------------------

    def test_blocks_send_to_unknown(self, validator):
        valid, reason = validator.validate_tool_call(
            "send_email", {"to": "attacker@evil.com", "body": "data"}
        )
        assert not valid
        assert "Unknown recipient" in reason

    def test_blocks_forward_to_unknown(self, validator):
        valid, reason = validator.validate_tool_call(
            "forward_email", {"to": "exfil@hacker.com", "email_id": "123"}
        )
        assert not valid

    def test_blocks_unknown_tool(self, validator):
        valid, reason = validator.validate_tool_call("delete_database", {"confirm": True})
        assert not valid
        assert "not allowed" in reason.lower()

    # ------------------------------------------------------------------
    # Safe tool calls should pass
    # ------------------------------------------------------------------

    def test_allows_send_to_known_contact(self, validator):
        valid, reason = validator.validate_tool_call(
            "send_email", {"to": "alice@company.com", "body": "hi"}
        )
        assert valid
        assert reason == "OK"

    def test_allows_read_email(self, validator):
        valid, _ = validator.validate_tool_call("read_email", {"email_id": "123"})
        assert valid

    def test_allows_draft_reply(self, validator):
        valid, _ = validator.validate_tool_call("draft_reply", {"email_id": "1", "body": "ok"})
        assert valid

    # ------------------------------------------------------------------
    # Custom contacts
    # ------------------------------------------------------------------

    def test_custom_known_contacts(self):
        v = OutputValidator(known_contacts={"custom@org.com"})
        valid, _ = v.validate_tool_call("send_email", {"to": "custom@org.com"})
        assert valid

        valid, _ = v.validate_tool_call("send_email", {"to": "alice@company.com"})
        assert not valid  # Not in custom list


class TestValidatePlan:
    @pytest.fixture()
    def validator(self):
        return OutputValidator()

    def test_blocks_plan_with_unknown_recipient(self, validator):
        actions = [
            {"tool": "send_email", "params": {"to": "attacker@evil.com", "body": "data"}},
        ]
        valid, concerns = validator.validate_plan(actions, "do something")
        assert not valid
        assert len(concerns) > 0

    def test_blocks_plan_with_unknown_tool(self, validator):
        actions = [
            {"tool": "delete_database", "params": {"confirm": True}},
        ]
        valid, concerns = validator.validate_plan(actions, "clean up old records")
        assert not valid
        assert any("not allowed" in c.lower() for c in concerns)

    def test_blocks_summarize_with_send(self, validator):
        actions = [
            {"tool": "send_email", "params": {"to": "alice@company.com", "body": "hi"}},
        ]
        valid, concerns = validator.validate_plan(actions, "summarize this email")
        assert not valid
        assert any("Summarize" in c for c in concerns)

    def test_passes_safe_plan(self, validator):
        actions = [
            {"tool": "read_email", "params": {"email_id": "1"}},
        ]
        valid, concerns = validator.validate_plan(actions, "summarize this email")
        assert valid
        assert len(concerns) == 0

    def test_handles_attribute_style_actions(self, validator):
        """PlannedAction-like objects with .tool and .params attributes."""
        from agentic_security.defenses.dry_run import PlannedAction

        actions = [
            PlannedAction(tool="forward_email", reason="exfil", params={"to": "bad@evil.com"}),
        ]
        valid, concerns = validator.validate_plan(actions, "do something")
        assert not valid

    def test_empty_plan_passes(self, validator):
        valid, concerns = validator.validate_plan([], "summarize this")
        assert valid
        assert concerns == []
