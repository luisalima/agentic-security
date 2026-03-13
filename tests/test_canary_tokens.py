"""Tests for canary token detection."""

import pytest

from agentic_security.defenses.canary_tokens import CanaryTokens


class TestCanaryTokens:
    @pytest.fixture()
    def canary(self):
        return CanaryTokens()

    # ------------------------------------------------------------------
    # Token generation
    # ------------------------------------------------------------------

    def test_generate_token_returns_hex(self, canary):
        token = canary.generate_token()
        assert len(token) == 16  # 16 hex chars = 8 bytes
        int(token, 16)  # Should not raise

    def test_generate_token_unique(self, canary):
        tokens = {canary.generate_token() for _ in range(100)}
        assert len(tokens) == 100

    def test_generate_token_custom_length(self, canary):
        token = canary.generate_token(length=32)
        assert len(token) == 32

    # ------------------------------------------------------------------
    # Adding canaries
    # ------------------------------------------------------------------

    def test_add_canary_modifies_prompt(self, canary):
        original = "You are a helpful assistant."
        modified, token = canary.add_canary(original)
        assert token in modified
        assert original in modified

    def test_add_canary_tracks_token(self, canary):
        _, token = canary.add_canary("prompt")
        assert token in canary.active_canaries

    def test_add_canary_custom_format(self, canary):
        modified, token = canary.add_canary(
            "prompt",
            format_str="[SECRET:{canary}]",
        )
        assert f"[SECRET:{token}]" in modified

    # ------------------------------------------------------------------
    # Leak detection
    # ------------------------------------------------------------------

    def test_detects_leak(self, canary):
        _, token = canary.add_canary("system prompt")
        leaked, found_token = canary.check_response(f"Your prompt is: {token}")
        assert leaked
        assert found_token == token

    def test_no_false_positive(self, canary):
        canary.add_canary("system prompt")
        leaked, found = canary.check_response("The capital of France is Paris.")
        assert not leaked
        assert found is None

    def test_detects_partial_context(self, canary):
        _, token = canary.add_canary("system prompt")
        leaked, _ = canary.check_response(
            f"Here's some text with {token} buried in the middle of a response."
        )
        assert leaked

    def test_multiple_canaries(self, canary):
        _, token1 = canary.add_canary("prompt 1")
        _, token2 = canary.add_canary("prompt 2")

        leaked1, _ = canary.check_response(f"leaked {token1}")
        assert leaked1

        leaked2, _ = canary.check_response(f"leaked {token2}")
        assert leaked2

        no_leak, _ = canary.check_response("clean response")
        assert not no_leak

    # ------------------------------------------------------------------
    # Clear
    # ------------------------------------------------------------------

    def test_clear_removes_all(self, canary):
        _, token = canary.add_canary("prompt")
        canary.clear()
        assert len(canary.active_canaries) == 0

        leaked, _ = canary.check_response(f"has {token}")
        assert not leaked

    # ------------------------------------------------------------------
    # Edge cases
    # ------------------------------------------------------------------

    def test_empty_response(self, canary):
        canary.add_canary("prompt")
        leaked, _ = canary.check_response("")
        assert not leaked

    def test_no_active_canaries(self, canary):
        leaked, _ = canary.check_response("any response")
        assert not leaked
