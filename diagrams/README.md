# Diagrams

Visual diagrams for the Agentic Security guide, created with [Excalidraw](https://excalidraw.com/).

## Files

| Diagram | Description | Used In |
|---------|-------------|---------|
| `mental_model.excalidraw` | Four-level defense mental model | README, guide/index |
| `detection_flow.excalidraw` | Detection pipeline (YARA → Vector → ML) | 1_detection |
| `dual_llm.excalidraw` | Quarantined + Privileged architecture | 3_secure_architecture |
| `typed_extraction.excalidraw` | Schema as firewall concept | 3_secure_architecture |
| `dry_run.excalidraw` | Plan → Evaluate → Execute flow | 3_secure_architecture |
| `defense_in_depth.excalidraw` | Layered defense overview | 4_defense_in_depth |

## How to Edit

1. Go to [excalidraw.com](https://excalidraw.com/)
2. Open the `.excalidraw` file
3. Edit and save
4. Export as SVG for embedding in markdown/notebooks

## Style Guide

- Use hand-drawn style (Excalidraw default)
- Colors:
  - Red `#e03131` - Attacks, dangers, untrusted
  - Green `#2f9e44` - Safe, trusted, approved
  - Blue `#1971c2` - Components, LLMs
  - Yellow `#f08c00` - Warnings, evaluation
  - Gray `#868e96` - Neutral, data flow
- Keep diagrams simple and focused
- Include legend if using symbols

## Exported SVGs

Place exported SVGs in this folder with `.svg` extension. Reference them in markdown:

```markdown
<!-- Diagram: see mental_model.excalidraw -->
```
