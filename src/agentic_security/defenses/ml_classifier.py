"""
ML classifier defense for prompt injection detection.

Simulates a transformer-based injection classifier (e.g., deepset/deberta-v3-base-injection).
In production, replace SimulatedInjectionClassifier with a real model via
``transformers.pipeline("text-classification", ...)``.
"""

import re
from dataclasses import dataclass


@dataclass
class ClassificationResult:
    label: str
    score: float
    threshold: float

    @property
    def is_injection(self) -> bool:
        return self.label == "INJECTION" and self.score >= self.threshold


class SimulatedInjectionClassifier:
    """
    Simulates a prompt injection classifier.

    In production, use:
    - deepset/deberta-v3-base-injection
    - protectai/deberta-v3-base-prompt-injection
    """

    def __init__(self, threshold: float = 0.85):
        self.threshold = threshold
        self.model_name = "simulated-deberta-v3-injection"

        # Feature patterns that indicate injection (simplified)
        self.injection_signals = [
            (r"ignore\b.*\b(previous|prior|above|all)\b.*\b(instructions?|rules?)", 0.95),
            (r"(disregard|forget|override)\b.*\b(instructions?|rules?|prompt)", 0.90),
            (r"(pretend|act as if|imagine)\b.*\b(no|without)\b.*\b(rules?|restrictions?)", 0.88),
            (r"\b(DAN|jailbreak|developer mode)\b", 0.92),
            (r"(repeat|show|reveal|output)\b.*\b(system|your)\b.*\b(prompt|instructions?)", 0.85),
            (r"</?system>|</?instructions?>|\[/?INST\]", 0.90),
            (r"you are now\b.*\b(unrestricted|unfiltered|evil)", 0.93),
            (r"bypass\b.*\b(safety|security|filters?|guidelines?)", 0.91),
        ]

        # Benign patterns that reduce injection score
        self.benign_signals = [
            (r"^(what|how|why|when|where|who|can you|could you)\b", -0.3),
            (r"\b(please|thanks|thank you|help me)\b", -0.15),
            (r"\b(weather|recipe|explain|summarize|translate)\b", -0.2),
        ]

    def classify(self, text: str) -> ClassificationResult:
        """Classify text as injection or safe."""
        text_lower = text.lower()

        # Start with base score
        injection_score = 0.1

        # Check for injection signals
        for pattern, weight in self.injection_signals:
            if re.search(pattern, text_lower, re.IGNORECASE):
                injection_score = max(injection_score, weight)

        # Adjust for benign signals
        for pattern, adjustment in self.benign_signals:
            if re.search(pattern, text_lower, re.IGNORECASE):
                injection_score += adjustment

        # Clamp to [0, 1]
        injection_score = max(0.0, min(1.0, injection_score))

        if injection_score >= self.threshold:
            return ClassificationResult("INJECTION", injection_score, self.threshold)
        else:
            return ClassificationResult("SAFE", 1 - injection_score, self.threshold)
