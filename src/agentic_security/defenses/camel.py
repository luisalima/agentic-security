"""
CaMeL: Capability-based Memory for LLMs.

Implements capability-based security for agentic systems by tracking data
provenance and enforcing access control policies on tool calls. Each piece
of data carries a set of "readers" (capabilities), and each tool has a
policy specifying which readers are allowed to provide arguments.

Based on: Google DeepMind CaMeL (https://arxiv.org/abs/2503.18813).
"""

from __future__ import annotations

import json

from pydantic import BaseModel, Field

from agentic_security.llm import LLMClient


class DataValue(BaseModel):
    """A value with provenance tracking.

    Each DataValue records where the data came from (source) and which
    readers (capabilities) are allowed to consume it.
    """

    value: str
    source: str = Field(description="Origin of the data, e.g. 'user_query' or 'tool:read_email'")
    readers: set[str] = Field(
        default_factory=set,
        description="Set of capability labels allowed to read this data",
    )

    @classmethod
    def public(cls, value: str) -> DataValue:
        """Create a public data value (readable by anyone)."""
        return cls(value=value, source="user_query", readers={"public"})

    @classmethod
    def from_tool(cls, value: str, tool_name: str) -> DataValue:
        """Create a data value originating from a tool output."""
        return cls(value=value, source=f"tool:{tool_name}", readers={f"tool:{tool_name}"})


class CapabilityPolicy(BaseModel):
    """Policy for a single tool capability."""

    tool_name: str
    allowed_readers: set[str] = Field(
        description="Set of reader labels allowed to supply arguments to this tool",
    )
    description: str = ""


class PolicyResult(BaseModel):
    """Result of a policy check."""

    allowed: bool
    tool_name: str
    reason: str = ""
    violating_args: list[str] = Field(default_factory=list)


class PlannedToolCall(BaseModel):
    """A planned tool invocation with named arguments."""

    tool_name: str
    args: dict[str, str] = Field(default_factory=dict)


# Default policies for email tools
DEFAULT_POLICIES: dict[str, CapabilityPolicy] = {
    "send_email": CapabilityPolicy(
        tool_name="send_email",
        allowed_readers={"public"},
        description="Send email — only public data allowed",
    ),
    "forward_email": CapabilityPolicy(
        tool_name="forward_email",
        allowed_readers={"public"},
        description="Forward email — only public data allowed",
    ),
    "draft_reply": CapabilityPolicy(
        tool_name="draft_reply",
        allowed_readers={"public", "tool:read_email"},
        description="Draft reply — may use data from read_email",
    ),
}

NO_SIDE_EFFECT_TOOLS: set[str] = {"read_email", "search_email", "list_emails"}


class PolicyEngine:
    """Evaluates tool calls against capability policies."""

    def __init__(
        self,
        policies: dict[str, CapabilityPolicy] | None = None,
        no_side_effect_tools: set[str] | None = None,
    ):
        self.policies = policies if policies is not None else DEFAULT_POLICIES
        self.no_side_effect_tools = (
            no_side_effect_tools if no_side_effect_tools is not None else NO_SIDE_EFFECT_TOOLS
        )

    def check(self, tool_name: str, args: dict[str, DataValue]) -> PolicyResult:
        """Check whether a tool call is allowed given its argument provenance.

        Args:
            tool_name: Name of the tool to call.
            args: Mapping of argument names to DataValues with provenance.

        Returns:
            PolicyResult indicating whether the call is allowed.
        """
        # No-side-effect tools always pass
        if tool_name in self.no_side_effect_tools:
            return PolicyResult(allowed=True, tool_name=tool_name, reason="No side effects")

        # Unknown tool → block
        if tool_name not in self.policies:
            return PolicyResult(
                allowed=False,
                tool_name=tool_name,
                reason="No policy defined",
            )

        policy = self.policies[tool_name]
        violating: list[str] = []

        for arg_name, data_val in args.items():
            # An arg is allowed if ANY of its readers intersects with the policy's allowed_readers
            if not data_val.readers & policy.allowed_readers:
                violating.append(arg_name)

        if violating:
            return PolicyResult(
                allowed=False,
                tool_name=tool_name,
                reason=f"Arguments violate policy: {', '.join(violating)}",
                violating_args=violating,
            )

        return PolicyResult(allowed=True, tool_name=tool_name, reason="Policy satisfied")


PLANNER_SYSTEM_PROMPT = """\
You are a planning assistant. Generate a plan of tool calls to fulfill the user's request.

Output a JSON list of actions, each with:
- tool_name: Which tool to use
- args: Dictionary of argument name to value

Available tools: send_email, forward_email, read_email, draft_reply

Use $ref:key to reference data from previous tool outputs.
Output JSON only."""


def _parse_json_response(raw: str) -> list | dict:
    """Parse a JSON response, handling ```json code blocks."""
    text = raw
    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)


class CaMeLPipeline:
    """CaMeL capability-based security pipeline.

    Flow:
    1. LLM generates a plan (list of tool calls)
    2. Tag each argument with provenance (public vs. tool output)
    3. Policy engine checks each tool call
    4. Block if any call violates its policy
    """

    def __init__(
        self,
        client: LLMClient,
        engine: PolicyEngine | None = None,
    ):
        self.client = client
        self.engine = engine or PolicyEngine()

    def generate_plan(self, user_request: str) -> list[PlannedToolCall]:
        """Ask the LLM for a plan of tool calls."""
        response = self.client.complete(
            system=PLANNER_SYSTEM_PROMPT,
            user=user_request,
        )
        raw = _parse_json_response(response["content"])
        if isinstance(raw, dict):
            raw = [raw]
        return [PlannedToolCall(**action) for action in raw]

    def tag_args(
        self,
        call: PlannedToolCall,
        data_store: dict[str, DataValue] | None = None,
    ) -> dict[str, DataValue]:
        """Tag each argument with its provenance.

        Plain strings become public data. $ref:key references are resolved
        from the data_store.
        """
        store = data_store or {}
        tagged: dict[str, DataValue] = {}

        for arg_name, arg_val in call.args.items():
            if isinstance(arg_val, str) and arg_val.startswith("$ref:"):
                ref_key = arg_val[5:]
                if ref_key in store:
                    tagged[arg_name] = store[ref_key]
                else:
                    tagged[arg_name] = DataValue.public(arg_val)
            else:
                tagged[arg_name] = DataValue.public(str(arg_val))

        return tagged

    def run(
        self,
        user_request: str,
        tool_outputs: dict[str, str] | None = None,
    ) -> dict:
        """Run the full CaMeL pipeline.

        Args:
            user_request: What the user asked for.
            tool_outputs: Optional mapping of ref keys to raw tool output strings.
                Each is tagged as coming from a tool.

        Returns:
            dict with 'plan', 'results', and 'blocked'.
        """
        plan = self.generate_plan(user_request)

        # Build data store from tool_outputs
        data_store: dict[str, DataValue] = {}
        if tool_outputs:
            for key, value in tool_outputs.items():
                data_store[key] = DataValue.from_tool(value, "read_email")

        results: list[PolicyResult] = []
        blocked = False

        for call in plan:
            tagged = self.tag_args(call, data_store)
            result = self.engine.check(call.tool_name, tagged)
            results.append(result)
            if not result.allowed:
                blocked = True

        return {
            "plan": plan,
            "results": results,
            "blocked": blocked,
        }
