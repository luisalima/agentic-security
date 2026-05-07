# Injection Evaluation Dataset

Curated dataset of prompt injection attacks and legitimate inputs for benchmarking agentic security defenses.

## Overview

| Metric | Count |
|--------|-------|
| **Total samples** | 84 |
| **Injection attacks** | 64 |
| **Legitimate inputs** | 20 |

### Injection categories

| Category | Count | Difficulty range |
|----------|-------|-----------------|
| `instruction_override` | 11 | easy–hard |
| `encoding_obfuscation` | 6 | medium–hard |
| `fake_system_message` | 5 | medium–hard |
| `social_engineering` | 5 | hard |
| `delimiter_escape` | 5 | medium–hard |
| `prompt_extraction` | 5 | easy–medium |
| `context_manipulation` | 5 | hard |
| `tool_manipulation` | 5 | medium–hard |
| `data_exfiltration` | 5 | medium–hard |
| `multi_step` | 4 | medium–hard |
| `tool_poisoning` | 3 | hard |
| `memory_poisoning` | 2 | hard |
| `second_order` | 2 | hard |
| `supply_chain` | 1 | medium |

Eight samples originate from `INJECTION_VARIANTS` in `src/agentic_security/scenario.py` (marked with `"source": "INJECTION_VARIANTS"`).

### Legitimate categories

| Category | Count | Difficulty range |
|----------|-------|-----------------|
| `question` | 4 | easy |
| `task_request` | 5 | easy–medium |
| `security_discussion` | 5 | easy–hard |
| `edge_case` | 6 | medium–hard |

Five samples originate from `LEGITIMATE_INPUTS` in `benchmark/run.py` (marked with `"source": "LEGITIMATE_INPUTS"`).

## File format

```json
{
  "metadata": { "name": "...", "version": "...", "categories": { ... } },
  "samples": [
    {
      "id": "inj-001",
      "text": "The attack or legitimate text",
      "label": "injection | legitimate",
      "category": "instruction_override | question | ...",
      "difficulty": "easy | medium | hard",
      "description": "What this sample tests",
      "source": "(optional) origin in the codebase"
    }
  ]
}
```

## Usage

Load the dataset in Python:

```python
import json
from pathlib import Path

dataset = json.loads(Path("data/injection_dataset.json").read_text())

attacks = [s for s in dataset["samples"] if s["label"] == "injection"]
legit = [s for s in dataset["samples"] if s["label"] == "legitimate"]

# Filter by category or difficulty
hard_attacks = [s for s in attacks if s["difficulty"] == "hard"]
```

Run the existing benchmark against this dataset:

```python
from benchmark.run import DETECTION_DEFENSES

for sample in dataset["samples"]:
    for defense in DETECTION_DEFENSES:
        flagged = defense.detect(sample["text"])
        print(f"{sample['id']} | {defense.name}: {'🚨' if flagged else '✅'}")
```

## Contributing new samples

1. Add entries to the `samples` array in `injection_dataset.json`.
2. Use the next available ID (`inj-051`, `leg-021`, etc.).
3. Include all required fields: `id`, `text`, `label`, `category`, `difficulty`, `description`.
4. For injection samples, ensure the attack is realistic — something that could appear in a real email or user message.
5. For legitimate samples, prefer inputs that could trigger false positives (security discussions, forwarding requests, etc.).
6. Update the counts in this README.
7. Run `python benchmark/run.py` to verify defenses still behave as expected.
