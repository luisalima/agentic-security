"""Tests for dry-run evaluation defense."""

import json

import pytest

from agentic_security.defenses.dry_run import (
    EVALUATOR_SYSTEM_PROMPT,
    EvaluationResult,
    ExecutionPlan,
    PLANNER_SYSTEM_PROMPT,
    PlannedAction,
    DryRunEvaluator,
)
from agentic_security.llm import MockClient


class TestPlannedAction:
    def test_create(self):
        a = PlannedAction(tool="send_email", reason="reply", params={"to": "a@b.com"})
        assert a.tool == "send_email"


class TestExecutionPlan:
    def test_create_with_actions(self):
        plan = ExecutionPlan(
            summary="Summarize email",
            actions=[
                PlannedAction(tool="read_email", reason="read", params={"email_id": "1"}),
            ],
        )
        assert len(plan.actions) == 1

    def test_empty_actions(self):
        plan = ExecutionPlan(summary="Nothing to do", actions=[])
        assert len(plan.actions) == 0


class TestEvaluationResult:
    def test_approved(self):
        r = EvaluationResult(
            approved=True, risk_level="low", concerns=[], recommendation="proceed"
        )
        assert r.approved

    def test_rejected(self):
        r = EvaluationResult(
            approved=False,
            risk_level="critical",
            concerns=["exfiltration"],
            recommendation="block",
        )
        assert not r.approved


class TestDryRunDeterministicValidation:
    """Test the rule-based validation — no LLM needed."""

    @pytest.fixture()
    def evaluator(self):
        return DryRunEvaluator(client=MockClient())

    def test_blocks_send_to_unknown(self, evaluator):
        plan = ExecutionPlan(
            summary="Send email",
            actions=[
                PlannedAction(
                    tool="send_email",
                    reason="reply",
                    params={"to": "attacker@evil.com", "body": "data"},
                ),
            ],
        )
        valid, reason = evaluator.validate_plan_deterministic(plan, "send a reply")
        assert not valid
        assert "Unknown recipient" in reason

    def test_blocks_forward_to_unknown(self, evaluator):
        plan = ExecutionPlan(
            summary="Forward email",
            actions=[
                PlannedAction(
                    tool="forward_email",
                    reason="backup",
                    params={"to": "exfil@hacker.com", "email_id": "1"},
                ),
            ],
        )
        valid, reason = evaluator.validate_plan_deterministic(plan, "forward this")
        assert not valid

    def test_blocks_send_on_summarize_request(self, evaluator):
        """Even to known contacts, sending shouldn't happen for summarize requests."""
        plan = ExecutionPlan(
            summary="Summarize and send",
            actions=[
                PlannedAction(
                    tool="send_email",
                    reason="confirm",
                    params={"to": "alice@company.com", "body": "hi"},
                ),
            ],
        )
        valid, reason = evaluator.validate_plan_deterministic(
            plan, "Please summarize this email"
        )
        assert not valid
        assert "summarize" in reason.lower()

    def test_allows_read_email(self, evaluator):
        plan = ExecutionPlan(
            summary="Read email",
            actions=[
                PlannedAction(
                    tool="read_email", reason="read", params={"email_id": "1"}
                ),
            ],
        )
        valid, reason = evaluator.validate_plan_deterministic(plan, "summarize this")
        assert valid

    def test_allows_send_to_known_contact(self, evaluator):
        plan = ExecutionPlan(
            summary="Reply to Alice",
            actions=[
                PlannedAction(
                    tool="send_email",
                    reason="reply",
                    params={"to": "alice@company.com", "body": "thanks"},
                ),
            ],
        )
        valid, reason = evaluator.validate_plan_deterministic(plan, "reply to Alice")
        assert valid

    def test_empty_plan_passes(self, evaluator):
        plan = ExecutionPlan(summary="Nothing", actions=[])
        valid, reason = evaluator.validate_plan_deterministic(plan, "summarize")
        assert valid

    def test_custom_known_contacts(self):
        ev = DryRunEvaluator(
            client=MockClient(),
            known_contacts={"custom@org.com"},
        )
        plan = ExecutionPlan(
            summary="Send",
            actions=[
                PlannedAction(
                    tool="send_email",
                    reason="send",
                    params={"to": "custom@org.com", "body": "hi"},
                ),
            ],
        )
        valid, _ = ev.validate_plan_deterministic(plan, "send this")
        assert valid


class TestDryRunFullPipeline:
    def test_run_blocks_dangerous_plan(self):
        """Mock: planner returns dangerous plan, evaluator rejects it."""
        plan_json = json.dumps({
            "summary": "Forward email",
            "actions": [
                {"tool": "forward_email", "reason": "backup", "params": {"to": "evil@bad.com", "email_id": "1"}},
            ],
        })
        eval_json = json.dumps({
            "approved": False,
            "risk_level": "critical",
            "concerns": ["Unknown recipient"],
            "recommendation": "Block",
        })
        mock = MockClient(responses=[
            {"content": plan_json},
            {"content": eval_json},
        ])
        ev = DryRunEvaluator(client=mock)
        result = ev.run("summarize this email", "email content here")
        assert not result["approved"]

    def test_run_allows_safe_plan(self):
        plan_json = json.dumps({
            "summary": "Read email",
            "actions": [
                {"tool": "read_email", "reason": "read", "params": {"email_id": "1"}},
            ],
        })
        eval_json = json.dumps({
            "approved": True,
            "risk_level": "low",
            "concerns": [],
            "recommendation": "Proceed",
        })
        mock = MockClient(responses=[
            {"content": plan_json},
            {"content": eval_json},
        ])
        ev = DryRunEvaluator(client=mock)
        result = ev.run("read my email", "email content here")
        assert result["approved"]


class TestSystemPrompts:
    def test_planner_says_no_execute(self):
        assert "DO NOT execute" in PLANNER_SYSTEM_PROMPT

    def test_evaluator_strict(self):
        assert "Be strict" in EVALUATOR_SYSTEM_PROMPT
