"""
Canary tokens for detecting prompt leakage.

Canary tokens are hidden markers injected into prompts to detect prompt leakage.
If the canary appears in the output, you know the LLM revealed something it shouldn't.
"""

import secrets


class CanaryTokens:
    """Canary token generator and detector."""

    def __init__(self):
        self.active_canaries: dict[str, str] = {}

    def generate_token(self, length: int = 16) -> str:
        """Generate a random canary token."""
        return secrets.token_hex(length // 2)

    def add_canary(
        self,
        prompt: str,
        format_str: str = "<!-- CANARY:{canary} -->",
    ) -> tuple[str, str]:
        """
        Add a canary token to a prompt.

        Args:
            prompt: Original prompt
            format_str: Template containing {canary}

        Returns:
            (modified_prompt, canary_token)
        """
        token = self.generate_token()
        canary_marker = format_str.format(canary=token)

        modified = f"{canary_marker}\n{prompt}"

        self.active_canaries[token] = prompt
        return modified, token

    def check_response(self, response: str) -> tuple[bool, str | None]:
        """
        Check if response contains any active canary tokens.

        Returns:
            (leaked, token) - leaked is True if canary found
        """
        for token in self.active_canaries:
            if token in response:
                return True, token
        return False, None

    def clear(self):
        """Clear all active canaries."""
        self.active_canaries.clear()
