"""
Run all defense patterns and compare results.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console
from rich.table import Table

console = Console()


def run_all_patterns(provider: str = "openai"):
    """Run all patterns and collect results."""
    from patterns.pattern_00_baseline import run_baseline
    from patterns.pattern_01_delimiter import run_delimiter_defense
    from patterns.pattern_02_dual_llm import run_dual_llm_defense
    from patterns.pattern_03_typed_extraction import run_typed_extraction_defense
    from patterns.pattern_04_dry_run import run_dry_run_defense
    from patterns.pattern_05_combined import run_combined_defense

    patterns = [
        ("Baseline (no protection)", run_baseline),
        ("Random Delimiters", run_delimiter_defense),
        ("Dual LLM", run_dual_llm_defense),
        ("Typed Extraction", run_typed_extraction_defense),
        ("Dry-Run Evaluation", run_dry_run_defense),
        ("Combined Defense", run_combined_defense),
    ]

    results = []
    for name, run_fn in patterns:
        console.print(f"\n{'='*60}")
        try:
            result = run_fn(provider)
            results.append((name, result))
        except Exception as e:
            console.print(f"[red]Error running {name}: {e}[/red]")
            results.append((name, {"attack_succeeded": None, "error": str(e)}))

    # Summary table
    console.print("\n" + "=" * 60)
    console.print("\n[bold]SUMMARY[/bold]\n")

    table = Table(title="Defense Pattern Comparison")
    table.add_column("Pattern", style="cyan")
    table.add_column("Attack Blocked?", justify="center")
    table.add_column("Notes")

    for name, result in results:
        if result.get("error"):
            status = "[yellow]ERROR[/yellow]"
            notes = result["error"][:40]
        elif result.get("attack_succeeded"):
            status = "[red]NO[/red]"
            notes = f"{result.get('dangerous_actions', 0)} dangerous actions"
        else:
            status = "[green]YES[/green]"
            notes = "Attack blocked"
        
        table.add_row(name, status, notes)

    console.print(table)

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run all defense patterns")
    parser.add_argument(
        "--provider",
        default="openai",
        choices=["openai", "anthropic"],
        help="LLM provider to use",
    )
    args = parser.parse_args()

    run_all_patterns(args.provider)
