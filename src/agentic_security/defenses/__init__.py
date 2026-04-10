"""
Defense patterns for securing AI agents against prompt injection.

Each module implements a defense technique that can be used independently
or composed together for defense-in-depth.
"""

from agentic_security.defenses.camel import (
    CaMeLPipeline,
    CapabilityPolicy,
    DataValue,
    PlannedToolCall,
    PolicyEngine,
    PolicyResult,
)
from agentic_security.defenses.canary_tokens import CanaryTokens
from agentic_security.defenses.delimiters import generate_delimiter, wrap_untrusted
from agentic_security.defenses.dry_run import (
    DryRunEvaluator,
    EvaluationResult,
    ExecutionPlan,
    PlannedAction,
)
from agentic_security.defenses.dual_llm import DualLLMProcessor
from agentic_security.defenses.mcp_security import (
    MCPScanner,
    MCPScanResult,
    MCPServerConfig,
    RugPullDetector,
    parse_mcp_config,
)
from agentic_security.defenses.ml_classifier import (
    ClassificationResult,
    SimulatedInjectionClassifier,
)
from agentic_security.defenses.output_validation import OutputValidator
from agentic_security.defenses.tool_validation import (
    ToolDefinition,
    ToolValidationResult,
    ToolValidator,
    parse_mcp_tools,
    parse_openai_tools,
)
from agentic_security.defenses.typed_extraction import EmailExtraction, extract_typed_data
from agentic_security.defenses.vector_similarity import SimpleVectorDB
from agentic_security.defenses.yara_detection import SimpleYaraScanner, YaraMatch

__all__ = [
    "CaMeLPipeline",
    "CanaryTokens",
    "CapabilityPolicy",
    "ClassificationResult",
    "DataValue",
    "DryRunEvaluator",
    "DualLLMProcessor",
    "EmailExtraction",
    "EvaluationResult",
    "MCPScanner",
    "MCPServerConfig",
    "MCPScanResult",
    "ExecutionPlan",
    "OutputValidator",
    "PlannedAction",
    "PlannedToolCall",
    "PolicyEngine",
    "PolicyResult",
    "RugPullDetector",
    "SimpleVectorDB",
    "SimpleYaraScanner",
    "SimulatedInjectionClassifier",
    "ToolDefinition",
    "ToolValidationResult",
    "ToolValidator",
    "YaraMatch",
    "extract_typed_data",
    "generate_delimiter",
    "parse_mcp_config",
    "parse_mcp_tools",
    "parse_openai_tools",
    "wrap_untrusted",
]
