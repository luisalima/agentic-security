#!/usr/bin/env python3
"""
Export Marimo notebooks to Markdown for the guide.

Usage:
    python scripts/export_guide.py

This creates readable markdown versions of all notebooks in the guide/ folder.
"""

import subprocess
import sys
from pathlib import Path


def export_notebook(notebook_path: Path, output_path: Path) -> bool:
    """Export a single Marimo notebook to markdown."""
    try:
        result = subprocess.run(
            ["marimo", "export", "md", str(notebook_path), "-o", str(output_path)],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"  ✓ {notebook_path.name} → {output_path.name}")
            return True
        else:
            print(f"  ✗ {notebook_path.name}: {result.stderr}")
            return False
    except FileNotFoundError:
        print("Error: marimo not found. Install with: pip install marimo")
        sys.exit(1)


def main():
    repo_root = Path(__file__).parent.parent
    notebooks_dir = repo_root / "notebooks"
    guide_dir = repo_root / "guide"

    # Ensure guide directory exists
    guide_dir.mkdir(exist_ok=True)

    print("Exporting notebooks to guide/\n")

    # Process each section
    sections = [
        "0_vulnerabilities",
        "1_detection",
        "2_prompt_engineering",
        "3_isolation_infra_level",
        "4_secure_architecture_software",
        "5_defense_in_depth",
        "6_integration",
    ]

    total = 0
    exported = 0

    for section in sections:
        section_path = notebooks_dir / section
        if not section_path.exists():
            continue

        print(f"{section}/")

        # Create corresponding guide section
        guide_section = guide_dir / section
        guide_section.mkdir(exist_ok=True)

        # Export each notebook in the section
        for notebook in sorted(section_path.glob("*.py")):
            if notebook.name.startswith("_"):
                continue
            
            total += 1
            output_file = guide_section / f"{notebook.stem}.md"
            if export_notebook(notebook, output_file):
                exported += 1

    print(f"\nExported {exported}/{total} notebooks")

    # Create guide index
    create_guide_index(guide_dir, sections)


def create_guide_index(guide_dir: Path, sections: list[str]):
    """Create an index.md for the guide."""
    index_content = """# Agentic Security Guide

A comprehensive guide to securing AI agents against prompt injection and related attacks.

## How to Use This Guide

**Reading online?** Browse the markdown files in each section.

**Want to experiment?** Run the interactive [Marimo notebooks](../notebooks_securing_guide/).

## Sections

### [0. Vulnerabilities](0_vulnerabilities/)
Understanding the vulnerability: what happens with no protection.

### [1. Detection](1_detection/)
Techniques to identify malicious prompts before they reach the LLM.
- Pattern matching (YARA)
- Semantic similarity (vectors)
- ML classification
- Canary tokens

### [2. Prompt Engineering](2_prompt_engineering/)
Hardening individual LLM calls through prompt design.
- Random delimiters / Spotlighting
- System prompt hardening
- Instruction hierarchy
- Sandwich defense
- XML tagging

### [3. Isolation (Infra-Level)](3_isolation_infra_level/)
Sandboxing and isolation techniques for limiting agent capabilities.

### [4. Secure Architecture](4_secure_architecture_software/)
Architectural patterns for isolating concerns and limiting blast radius.
- Dual LLM (quarantine + privilege)
- Typed extraction (schema as firewall)
- Dry-run evaluation (plan → evaluate → execute)

### [5. Defense in Depth](5_defense_in_depth/)
Layering all techniques together for comprehensive protection.

### [6. Framework Integration](6_integration/)
Applying security patterns to real-world frameworks (LangChain, etc.).

---

## Quick Reference

| Level | Approach | Effort | Protection |
|-------|----------|--------|------------|
| Detection | Filter inputs | Drop-in | ~95% |
| Prompt Engineering | Harden prompts | Low | +5% |
| Secure Architecture | Redesign system | High | +10% |
| Defense in Depth | All of above | Highest | ~99% |

See also: [Tools Comparison](../docs/TOOLS.md) | [Attack Taxonomy](../docs/ATTACK_TAXONOMY.md) | [Threat Model](../docs/THREAT_MODEL.md)
"""

    index_path = guide_dir / "index.md"
    index_path.write_text(index_content)
    print(f"Created {index_path}")


if __name__ == "__main__":
    main()
