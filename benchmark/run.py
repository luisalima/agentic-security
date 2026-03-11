"""
Benchmark: Run all defense patterns and compare results.

TODO: Update to work with new notebook structure.
The notebooks are now Marimo apps in notebooks/ and can be run individually.

For now, run notebooks directly:
    marimo run notebooks/0_baseline/baseline.py
    marimo run notebooks/3_secure_architecture/dual_llm.py
    etc.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def main():
    print("Benchmark runner - coming soon!")
    print()
    print("For now, run notebooks individually:")
    print()
    
    notebooks_dir = Path(__file__).parent.parent / "notebooks"
    
    for section in sorted(notebooks_dir.iterdir()):
        if section.is_dir() and not section.name.startswith('.'):
            for notebook in sorted(section.glob("*.py")):
                print(f"  marimo run {notebook.relative_to(notebooks_dir.parent)}")
    
    print()
    print("Or use the export script to generate markdown:")
    print("  python scripts/export_guide.py")


if __name__ == "__main__":
    main()
