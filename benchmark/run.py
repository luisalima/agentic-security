"""
Benchmark: Comparative evaluation of deterministic defense patterns.

Runs all deterministic defenses against the INJECTION_VARIANTS attack corpus
and legitimate inputs, producing a technique × attack variant → pass/fail matrix.

Usage:
    python benchmark/run.py          # Rich table output
    python benchmark/run.py --json   # JSON output
"""

import argparse
import json
import sys
from abc import ABC, abstractmethod
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from agentic_security.defenses.canary_tokens import CanaryTokens
from agentic_security.defenses.ml_classifier import SimulatedInjectionClassifier
from agentic_security.defenses.output_validation import OutputValidator
from agentic_security.defenses.vector_similarity import SimpleVectorDB
from agentic_security.defenses.yara_detection import SimpleYaraScanner
from agentic_security.scenario import INJECTION_VARIANTS

LEGITIMATE_INPUTS = [
    "What is the weather in Paris?",
    "Please summarize this document for me.",
    "Can you help me write a poem about nature?",
    "Schedule a meeting for next Tuesday at 3pm.",
    "The project is on track for delivery next week.",
]


# ---------------------------------------------------------------------------
# Defense adapters
# ---------------------------------------------------------------------------


class DefenseAdapter(ABC):
    name: str
    note: str = ""

    @abstractmethod
    def detect(self, text: str) -> bool:
        """Return True if the text is flagged as an attack."""


class YaraAdapter(DefenseAdapter):
    name = "YARA"

    def __init__(self) -> None:
        self.scanner = SimpleYaraScanner()

    def detect(self, text: str) -> bool:
        return len(self.scanner.scan(text)) > 0


class VectorAdapter(DefenseAdapter):
    name = "Vector"

    def __init__(self) -> None:
        self.db = SimpleVectorDB()

    def detect(self, text: str) -> bool:
        is_attack, _ = self.db.is_attack(text)
        return is_attack


class MLAdapter(DefenseAdapter):
    name = "ML"

    def __init__(self) -> None:
        self.classifier = SimulatedInjectionClassifier()

    def detect(self, text: str) -> bool:
        return self.classifier.classify(text).is_injection


class CanaryAdapter(DefenseAdapter):
    name = "Canary"
    note = "Detects prompt leakage, not injection"

    def detect(self, text: str) -> bool:
        ct = CanaryTokens()
        _modified, token = ct.add_canary("You are a helpful assistant.")
        leaked, _ = ct.check_response(text)
        return leaked


class OutputAdapter(DefenseAdapter):
    name = "Output"
    note = "Validates tool calls post-execution"

    def __init__(self) -> None:
        self.validator = OutputValidator()

    def detect(self, text: str) -> bool:
        # Simulate: if an injection succeeded, the LLM would call send_email
        # to an unknown address. We check if that call would be blocked.
        valid, _ = self.validator.validate_tool_call(
            "send_email", {"to": "attacker@evil.com", "subject": "pwned", "body": text}
        )
        return not valid

    def detect_legit(self, text: str) -> bool:
        # For legitimate inputs, simulate a normal tool call to a known contact.
        # Output validation should allow it (no false positive).
        valid, _ = self.validator.validate_tool_call(
            "send_email", {"to": "alice@company.com", "subject": "Re: hello", "body": text}
        )
        return not valid


# Delimiters are preventive-only — no detection method.
DELIMITER_NOTE = "Delimiters (Spotlighting): preventive only — instructs the LLM to treat wrapped content as data, not commands. Not included in detection benchmark."

# ---------------------------------------------------------------------------
# Benchmark runner
# ---------------------------------------------------------------------------

DETECTION_DEFENSES: list[DefenseAdapter] = [
    YaraAdapter(),
    VectorAdapter(),
    MLAdapter(),
    CanaryAdapter(),
    OutputAdapter(),
]


def truncate(text: str, length: int = 60) -> str:
    text = text.replace("\n", " ").strip()
    if len(text) <= length:
        return text
    return text[: length - 1] + "…"


def run_benchmark() -> dict:
    """Run all defenses against all attacks and legitimate inputs.

    Returns a dict with 'attacks', 'legit', and 'summary' keys.
    """
    attack_results: list[dict] = []
    for variant in INJECTION_VARIANTS:
        row: dict = {"text": variant}
        for defense in DETECTION_DEFENSES:
            row[defense.name] = defense.detect(variant)
        attack_results.append(row)

    legit_results: list[dict] = []
    for inp in LEGITIMATE_INPUTS:
        row = {"text": inp}
        for defense in DETECTION_DEFENSES:
            detect_fn = getattr(defense, "detect_legit", defense.detect)
            row[defense.name] = detect_fn(inp)
        legit_results.append(row)

    summary: list[dict] = []
    for defense in DETECTION_DEFENSES:
        detected = sum(1 for r in attack_results if r[defense.name])
        false_pos = sum(1 for r in legit_results if r[defense.name])
        summary.append(
            {
                "defense": defense.name,
                "note": defense.note,
                "detected": detected,
                "total_attacks": len(INJECTION_VARIANTS),
                "detection_rate": detected / len(INJECTION_VARIANTS) if INJECTION_VARIANTS else 0,
                "false_positives": false_pos,
                "total_legit": len(LEGITIMATE_INPUTS),
                "false_positive_rate": false_pos / len(LEGITIMATE_INPUTS)
                if LEGITIMATE_INPUTS
                else 0,
            }
        )

    return {
        "attacks": attack_results,
        "legit": legit_results,
        "summary": summary,
        "delimiter_note": DELIMITER_NOTE,
    }


def render_rich(results: dict) -> None:
    console = Console()

    console.print()
    console.print(
        Panel(
            "[bold]Agentic Security — Defense Benchmark[/bold]",
            expand=False,
        )
    )

    # --- Attack Detection Matrix ---
    attack_table = Table(title="Attack Detection Matrix", show_lines=True)
    attack_table.add_column("Attack Variant", style="cyan", max_width=60)
    for defense in DETECTION_DEFENSES:
        header = defense.name
        if defense.note:
            header += " [dim]¹[/dim]"
        attack_table.add_column(header, justify="center")

    for row in results["attacks"]:
        cells = [truncate(row["text"])]
        for defense in DETECTION_DEFENSES:
            cells.append("✅" if row[defense.name] else "❌")
        attack_table.add_row(*cells)

    console.print()
    console.print(attack_table)

    # --- False Positive Matrix ---
    fp_table = Table(title="False Positive Check (Legitimate Inputs)", show_lines=True)
    fp_table.add_column("Input", style="cyan", max_width=60)
    for defense in DETECTION_DEFENSES:
        fp_table.add_column(defense.name, justify="center")

    for row in results["legit"]:
        cells = [truncate(row["text"])]
        for defense in DETECTION_DEFENSES:
            cells.append("✅" if not row[defense.name] else "⚠️")
        fp_table.add_row(*cells)

    console.print()
    console.print(fp_table)

    # --- Summary ---
    summary_table = Table(title="Summary", show_lines=True)
    summary_table.add_column("Defense", style="bold")
    summary_table.add_column("Detection Rate", justify="center")
    summary_table.add_column("False Positive Rate", justify="center")
    summary_table.add_column("Note", style="dim")

    for s in results["summary"]:
        det_pct = f"{s['detection_rate']:.0%} ({s['detected']}/{s['total_attacks']})"
        fp_pct = f"{s['false_positive_rate']:.0%} ({s['false_positives']}/{s['total_legit']})"
        summary_table.add_row(s["defense"], det_pct, fp_pct, s["note"])

    console.print()
    console.print(summary_table)

    # Delimiter note
    console.print()
    console.print(f"[dim]ℹ  {results['delimiter_note']}[/dim]")

    # Footnotes for annotated defenses
    notes = [(d.name, d.note) for d in DETECTION_DEFENSES if d.note]
    if notes:
        console.print()
        for i, (name, note) in enumerate(notes, 1):
            console.print(f"[dim]¹ {name}: {note}[/dim]")

    console.print()


def render_json(results: dict) -> None:
    output = {
        "attacks": [
            {
                "text": row["text"],
                "results": {d.name: row[d.name] for d in DETECTION_DEFENSES},
            }
            for row in results["attacks"]
        ],
        "legitimate": [
            {
                "text": row["text"],
                "results": {d.name: row[d.name] for d in DETECTION_DEFENSES},
            }
            for row in results["legit"]
        ],
        "summary": results["summary"],
        "delimiter_note": results["delimiter_note"],
    }
    print(json.dumps(output, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Agentic Security — Defense Benchmark")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    results = run_benchmark()

    if args.json:
        render_json(results)
    else:
        render_rich(results)


if __name__ == "__main__":
    main()
