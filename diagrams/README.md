# Diagrams

Visual diagrams for the Agentic Security guide. Most diagrams are authored in Mermaid (`mermaid/*.mmd`) and exported to SVG; a handful of older diagrams are still authored in [Excalidraw](https://excalidraw.com/) (`*.excalidraw`).

## Layout

```
diagrams/
├── *.svg              # Rendered diagrams used in docs and notebooks
├── mermaid/*.mmd      # Mermaid sources (one per SVG)
└── *.excalidraw       # Original Excalidraw sources (subset of diagrams)
```

## SVGs

The 21 SVGs in this directory:

| File | Used in |
|------|---------|
| `mental_model.svg` | README, principles |
| `lethal_trifecta.svg` | guide/0_vulnerabilities |
| `framework_gap.svg` | guide/0_vulnerabilities |
| `detection_pipeline.svg` | guide/1_detection |
| `yara_flow.svg` | guide/1_detection |
| `vector_similarity.svg` | guide/1_detection |
| `ml_classifier.svg` | guide/1_detection |
| `llm_as_judge.svg` | guide/1_detection |
| `canary_tokens.svg` | guide/1_detection |
| `prompt_engineering.svg` | guide/2_prompt_engineering |
| `delimiters.svg` | guide/2_prompt_engineering |
| `instruction_hierarchy.svg` | guide/2_prompt_engineering |
| `sandwich_defense.svg` | guide/2_prompt_engineering |
| `secure_architecture_overview.svg` | guide/4_secure_architecture |
| `dual_llm.svg` | guide/4_secure_architecture |
| `typed_extraction.svg` | guide/4_secure_architecture |
| `dry_run.svg` | guide/4_secure_architecture |
| `tool_validation.svg` | guide/4_secure_architecture |
| `camel.svg` | guide/4_secure_architecture |
| `defense_in_depth.svg` | guide/5_defense_in_depth |
| `combined_defense.svg` | guide/5_defense_in_depth |

## Editing

### Mermaid (preferred)

1. Edit the source under `mermaid/<name>.mmd`.
2. Regenerate the SVG (e.g., via `mmdc`, the [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli)):
   ```bash
   mmdc -i diagrams/mermaid/<name>.mmd -o diagrams/<name>.svg
   ```

### Excalidraw

1. Open the `.excalidraw` file at [excalidraw.com](https://excalidraw.com/).
2. Edit and save back to the file in the repo.
3. Export as SVG and replace the matching `<name>.svg`.

## Style guide

- Hand-drawn feel for Excalidraw diagrams; clean defaults for Mermaid.
- Colors:
  - Red `#e03131` — attacks, dangers, untrusted
  - Green `#2f9e44` — safe, trusted, approved
  - Blue `#1971c2` — components, LLMs
  - Yellow `#f08c00` — warnings, evaluation
  - Gray `#868e96` — neutral, data flow
- Keep diagrams small and focused. Add a legend if you introduce symbols.
