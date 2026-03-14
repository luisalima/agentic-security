"""
YARA-like pattern matching for prompt injection detection.

A pure Python implementation of YARA-style rule scanning. In production,
use the real yara-python library (https://github.com/VirusTotal/yara-python)
for better performance with large rule sets.
"""

import re
from dataclasses import dataclass


@dataclass
class YaraMatch:
    rule_name: str
    category: str
    matched_string: str


class SimpleYaraScanner:
    """
    A simplified YARA-like scanner in pure Python.
    Real YARA would be faster for large rule sets.
    """

    def __init__(self):
        self.rules: dict[str, dict] = {}
        self._load_default_rules()

    def _load_default_rules(self):
        """Load default prompt injection detection rules."""

        self.rules["InstructionBypass"] = {
            "category": "Prompt Injection",
            "severity": "high",
            "patterns": [
                r"ignore\s+(all\s+)?previous\s+instructions?",
                r"ignore\s+(all\s+)?prior\s+instructions?",
                r"ignore\s+(all\s+)?above\s+instructions?",
                r"disregard\s+(all\s+)?previous",
                r"forget\s+(all\s+)?your\s+instructions?",
                r"ignore\s+the\s+above",
                r"do\s+not\s+follow\s+previous",
            ],
        }

        self.rules["SystemPromptExtraction"] = {
            "category": "Prompt Leakage",
            "severity": "high",
            "patterns": [
                r"repeat\s+your\s+(system\s+)?instructions?",
                r"show\s+me\s+your\s+(system\s+)?prompt",
                r"what\s+are\s+your\s+(system\s+)?rules",
                r"print\s+your\s+system\s+prompt",
                r"output\s+your\s+instructions?",
                r"reveal\s+your\s+prompt",
            ],
        }

        self.rules["RoleplayJailbreak"] = {
            "category": "Jailbreak",
            "severity": "medium",
            "patterns": [
                r"pretend\s+you\s+are\s+(?:a\s+)?(?:an\s+)?(?:evil|bad|unfiltered)",
                r"act\s+as\s+(?:a\s+)?(?:an\s+)?(?:DAN|evil|unfiltered)",
                r"you\s+are\s+now\s+(?:a\s+)?(?:an\s+)?(?:DAN|jailbroken)",
                r"enter\s+(?:DAN|developer)\s+mode",
            ],
        }

        self.rules["DelimiterEscape"] = {
            "category": "Prompt Injection",
            "severity": "high",
            "patterns": [
                r"</?(system|user|assistant|instruction)>",
                r"\[/?INST\]",
                r"```\s*(system|end)",
                r"<\|im_(start|end)\|>",
            ],
        }

    def add_rule(self, name: str, category: str, patterns: list[str], severity: str = "medium"):
        """Add a custom rule."""
        self.rules[name] = {"category": category, "patterns": patterns, "severity": severity}

    def scan(self, text: str) -> list[YaraMatch]:
        """Scan text against all rules."""
        matches = []
        text_lower = text.lower()

        for rule_name, rule_data in self.rules.items():
            for pattern in rule_data["patterns"]:
                match = re.search(pattern, text_lower, re.IGNORECASE)
                if match:
                    matches.append(
                        YaraMatch(
                            rule_name=rule_name,
                            category=rule_data["category"],
                            matched_string=match.group(0),
                        )
                    )
                    break  # One match per rule is enough

        return matches
