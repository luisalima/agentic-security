"""
LLM client abstraction for testing defense patterns.
Supports OpenAI and Anthropic APIs.
"""

import json
import os
from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class LLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    def complete(
        self,
        system: str,
        user: str,
        tools: list[dict] | None = None,
        response_format: type[BaseModel] | None = None,
    ) -> dict:
        """
        Complete a prompt.
        
        Args:
            system: System prompt
            user: User message
            tools: Optional list of tool definitions
            response_format: Optional Pydantic model for structured output
        
        Returns:
            dict with 'content' and optionally 'tool_calls'
        """
        pass


class OpenAIClient(LLMClient):
    """OpenAI API client."""

    def __init__(self, model: str = "gpt-4o-mini"):
        from openai import OpenAI

        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = model

    def complete(
        self,
        system: str,
        user: str,
        tools: list[dict] | None = None,
        response_format: type[BaseModel] | None = None,
    ) -> dict:
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]

        kwargs: dict[str, Any] = {"model": self.model, "messages": messages}

        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        if response_format:
            kwargs["response_format"] = {"type": "json_object"}
            # Add schema hint to system prompt
            schema_hint = f"\n\nRespond with JSON matching this schema:\n{response_format.model_json_schema()}"
            messages[0]["content"] += schema_hint

        response = self.client.chat.completions.create(**kwargs)
        message = response.choices[0].message

        result: dict[str, Any] = {"content": message.content or ""}

        if message.tool_calls:
            result["tool_calls"] = [
                {
                    "name": tc.function.name,
                    "arguments": json.loads(tc.function.arguments),
                }
                for tc in message.tool_calls
            ]

        return result


class AnthropicClient(LLMClient):
    """Anthropic API client."""

    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        import anthropic

        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.model = model

    def complete(
        self,
        system: str,
        user: str,
        tools: list[dict] | None = None,
        response_format: type[BaseModel] | None = None,
    ) -> dict:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": 1024,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }

        if tools:
            # Convert OpenAI tool format to Anthropic format
            anthropic_tools = []
            for tool in tools:
                func = tool.get("function", tool)
                anthropic_tools.append({
                    "name": func["name"],
                    "description": func.get("description", ""),
                    "input_schema": func.get("parameters", {"type": "object", "properties": {}}),
                })
            kwargs["tools"] = anthropic_tools

        if response_format:
            schema_hint = f"\n\nRespond with JSON matching this schema:\n{response_format.model_json_schema()}"
            kwargs["system"] += schema_hint

        response = self.client.messages.create(**kwargs)

        result: dict[str, Any] = {"content": ""}

        for block in response.content:
            if block.type == "text":
                result["content"] = block.text
            elif block.type == "tool_use":
                if "tool_calls" not in result:
                    result["tool_calls"] = []
                result["tool_calls"].append({
                    "name": block.name,
                    "arguments": block.input,
                })

        return result


class MockClient(LLMClient):
    """Mock client for testing without API calls."""

    def __init__(self, responses: list[dict] | None = None):
        self.responses = responses or []
        self.call_count = 0
        self.calls: list[dict] = []

    def complete(
        self,
        system: str,
        user: str,
        tools: list[dict] | None = None,
        response_format: type[BaseModel] | None = None,
    ) -> dict:
        self.calls.append({
            "system": system,
            "user": user,
            "tools": tools,
            "response_format": response_format,
        })

        if self.call_count < len(self.responses):
            response = self.responses[self.call_count]
            self.call_count += 1
            return response

        return {"content": "Mock response"}


def get_client(provider: str = "openai", model: str | None = None) -> LLMClient:
    """Get an LLM client by provider name."""
    if provider == "openai":
        return OpenAIClient(model=model or "gpt-4o-mini")
    elif provider == "anthropic":
        return AnthropicClient(model=model or "claude-3-5-sonnet-20241022")
    elif provider == "mock":
        return MockClient()
    else:
        raise ValueError(f"Unknown provider: {provider}")


# Tool definitions in OpenAI format
EMAIL_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email to a recipient",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Recipient email address"},
                    "subject": {"type": "string", "description": "Email subject"},
                    "body": {"type": "string", "description": "Email body"},
                },
                "required": ["to", "subject", "body"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "forward_email",
            "description": "Forward an email to another recipient",
            "parameters": {
                "type": "object",
                "properties": {
                    "email_id": {"type": "string", "description": "ID of email to forward"},
                    "to": {"type": "string", "description": "Recipient email address"},
                },
                "required": ["email_id", "to"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_email",
            "description": "Read the contents of an email",
            "parameters": {
                "type": "object",
                "properties": {
                    "email_id": {"type": "string", "description": "ID of email to read"},
                },
                "required": ["email_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "draft_reply",
            "description": "Draft a reply to an email (does not send)",
            "parameters": {
                "type": "object",
                "properties": {
                    "email_id": {"type": "string", "description": "ID of email to reply to"},
                    "body": {"type": "string", "description": "Reply body"},
                },
                "required": ["email_id", "body"],
            },
        },
    },
]

# Read-only tools (for quarantined LLM)
READ_ONLY_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_email",
            "description": "Read the contents of an email",
            "parameters": {
                "type": "object",
                "properties": {
                    "email_id": {"type": "string", "description": "ID of email to read"},
                },
                "required": ["email_id"],
            },
        },
    },
]
