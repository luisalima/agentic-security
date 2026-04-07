#!/usr/bin/env bash
# Export Marimo notebooks (.py) → guide markdown (.md)
#
# Usage:
#   ./scripts/export_guide.sh          # export all notebooks
#   ./scripts/export_guide.sh --check  # check for drift (CI mode)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
NOTEBOOKS_DIR="$REPO_ROOT/notebooks"
GUIDE_DIR="$REPO_ROOT/guide"
CHECK_MODE=false

if [[ "${1:-}" == "--check" ]]; then
    CHECK_MODE=true
fi

drift_found=false

while IFS= read -r notebook; do
    # notebooks/3_secure_architecture/2_typed_extraction.py → 3_secure_architecture/2_typed_extraction
    rel="${notebook#"$NOTEBOOKS_DIR/"}"
    stem="${rel%.py}"
    md_file="$GUIDE_DIR/${stem}.md"

    if $CHECK_MODE; then
        # Use a temp dir so marimo gets the right filename for the title
        tmp_dir="$(mktemp -d)"
        tmp_file="$tmp_dir/$(basename "$md_file")"
        marimo export md "$notebook" -o "$tmp_file" -f 2>/dev/null
        if ! diff -q "$tmp_file" "$md_file" >/dev/null 2>&1; then
            echo "DRIFT: $rel → guide/${stem}.md"
            diff --unified=3 "$md_file" "$tmp_file" || true
            drift_found=true
        fi
        rm -rf "$tmp_dir"
    else
        mkdir -p "$(dirname "$md_file")"
        marimo export md "$notebook" -o "$md_file" -f 2>/dev/null
        echo "exported: guide/${stem}.md"
    fi
done < <(find "$NOTEBOOKS_DIR" -name '*.py' -type f | sort)

if $CHECK_MODE && $drift_found; then
    echo ""
    echo "ERROR: Guide markdown is out of sync with notebooks."
    echo "Run './scripts/export_guide.sh' to regenerate."
    exit 1
elif $CHECK_MODE; then
    echo "✅ Guide markdown is in sync with notebooks."
fi
