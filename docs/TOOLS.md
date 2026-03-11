# LLM Security Tools Comparison

A comprehensive comparison of tools for defending against prompt injection and other LLM security threats.

## Quick Reference

| Tool | Type | License | Best For |
|------|------|---------|----------|
| [Vigil](https://github.com/deadbits/vigil-llm) | Detection | Apache 2.0 | Self-hosted multi-layer detection |
| [LLM Guard](https://llm-guard.com/) | Guardrails | MIT | Runtime input/output scanning |
| [Garak](https://github.com/NVIDIA/garak) | Red Team | Apache 2.0 | Vulnerability scanning (NVIDIA) |
| [Rebuff](https://github.com/protectai/rebuff) | Detection | Apache 2.0 | Self-hardening canary tokens |
| [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) | Guardrails | Apache 2.0 | Dialog flow control (NVIDIA) |
| [Prompt Shields](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection) | Detection | Commercial | Azure managed service (Microsoft) |
| [Lakera Guard](https://www.lakera.ai/) | Detection | Commercial | Enterprise API (<50ms latency) |
| [Augustus](https://github.com/praetorian-inc/augustus) | Red Team | Apache 2.0 | Go-based vulnerability scanner |
| [PyRIT](https://github.com/Azure/PyRIT) | Red Team | MIT | Multi-modal red teaming (Microsoft) |
| [Promptfoo](https://github.com/promptfoo/promptfoo) | Testing | MIT | Evaluation + red teaming |

---

## Detection Tools

### Vigil
**Self-hosted prompt injection scanner with multiple detection methods**

```python
from vigil.vigil import Vigil

app = Vigil.from_config('conf/server.conf')
result = app.input_scanner.perform_scan(input_prompt="Ignore previous instructions")
```

| Scanner | Method |
|---------|--------|
| Vector DB | Similarity search against known attacks |
| YARA | Pattern matching rules (like malware detection) |
| Transformer | ML classifier (deberta-v3-base-injection) |
| Canary Tokens | Detect prompt leakage |
| Sentiment | Detect manipulation attempts |

**Pros:** Multiple detection layers, fully self-hosted, customizable YARA rules
**Cons:** Alpha stage, requires setup (YARA, embeddings)

---

### LLM Guard
**Open-source runtime guardrails by Protect AI**

```python
from llm_guard import scan_prompt, scan_output
from llm_guard.input_scanners import PromptInjection, Toxicity
from llm_guard.output_scanners import Sensitive

sanitized, results, valid = scan_prompt([PromptInjection()], prompt)
```

| Input Scanners (15) | Output Scanners (20) |
|---------------------|----------------------|
| Prompt Injection | Sensitive Data |
| PII Anonymization | Bias Detection |
| Secrets Detection | Malicious URLs |
| Toxicity | Factual Consistency |
| Invisible Text | Data Leakage |

**Pros:** Closest open-source equivalent to Lakera, MIT licensed, easy integration
**Cons:** Self-managed ML models, limited language support vs commercial

---

### Rebuff
**Self-hardening prompt injection detector by Protect AI**

```python
from rebuff import Rebuff

rb = Rebuff(api_token="...", api_url="...")
result = rb.detect_injection(user_input)
```

| Layer | Method |
|-------|--------|
| 1 | Heuristics (keyword patterns) |
| 2 | LLM-based detection |
| 3 | Vector DB (embeddings of past attacks) |
| 4 | Canary tokens (detect leakage) |

**Pros:** Self-hardening (learns from detected attacks), canary tokens built-in
**Cons:** Prototype stage, requires API setup

---

### Microsoft Prompt Shields
**Managed API service in Azure AI Content Safety**

| Shield | Detects |
|--------|---------|
| User Prompt Shield | Direct jailbreak attempts |
| Document Shield | Indirect injection in content |

| Category | Example |
|----------|---------|
| Manipulated Content | Instructions to falsify info |
| Intrusion | Unauthorized access attempts |
| Data Exfiltration | Commands to leak data |
| Encoding Attacks | Base64, ROT13 bypasses |

**Pros:** Managed service, integrated with Azure/Defender XDR, 100+ languages
**Cons:** Commercial (pay per call), closed-source detection, Azure lock-in

---

### Lakera Guard
**Enterprise prompt injection API**

- Sub-50ms latency
- 98%+ detection rate (claimed)
- 100+ languages
- 80M+ attack data points from Gandalf game

**Pros:** Fast, high accuracy, no infrastructure to manage
**Cons:** Commercial (scales with traffic), closed-source

---

## Red Team / Scanning Tools

### Garak (NVIDIA)
**LLM vulnerability scanner with 37+ probe modules**

```bash
garak --model_type openai --model_name gpt-4 --probes all
```

| Probe Category | Examples |
|----------------|----------|
| Prompt Injection | Direct, indirect, delimiter escape |
| Jailbreaks | DAN, roleplay, encoding |
| Data Extraction | Training data, PII leakage |
| Encoding | Base64, ROT13, homoglyphs |
| Malware | Code generation attempts |

**Pros:** Comprehensive probe library, 23 LLM backends, published research
**Cons:** Testing tool only (no runtime protection)

---

### Augustus (Praetorian)
**Go-based LLM vulnerability scanner**

```bash
augustus scan --provider openai --model gpt-4o --probes prompt-injection
```

- 210+ vulnerability probes
- 28 LLM providers
- Single Go binary (no Python dependencies)
- Concurrent scanning

**Pros:** Fast (Go), portable, more probes than Garak
**Cons:** Newer, less research backing

---

### PyRIT (Microsoft)
**Multi-modal AI red teaming framework**

```python
from pyrit.orchestrator import RedTeamingOrchestrator
from pyrit.prompt_converter import Base64Converter

orchestrator = RedTeamingOrchestrator(...)
await orchestrator.send_prompts_async(prompt_list)
```

| Feature | Capability |
|---------|------------|
| Modalities | Text, image, audio, video |
| Attack Types | Single-turn, multi-turn, crescendo, TAP |
| Converters | Base64, ROT13, leetspeak, homoglyphs |

**Pros:** Built by Microsoft AI Red Team (tested on Bing/Copilot), multi-modal
**Cons:** Requires orchestration setup, testing only

---

## Guardrail Frameworks

### NeMo Guardrails (NVIDIA)
**Programmable dialog guardrails using Colang DSL**

```colang
define user express greeting
  "hello"
  "hi"
  
define bot express greeting
  "Hello! How can I help you?"

define flow greeting
  user express greeting
  bot express greeting
```

| Rail Type | Purpose |
|-----------|---------|
| Input | Filter incoming prompts |
| Dialog | Control conversation flow |
| Retrieval | Guard RAG pipelines |
| Execution | Validate tool/action calls |
| Output | Filter generated responses |

**Pros:** Unique multi-turn dialog control, declarative policies
**Cons:** Learning curve (Colang), more complex setup

---

## Feature Comparison Matrix

| Feature | Vigil | LLM Guard | Garak | Rebuff | NeMo | Prompt Shields | Lakera |
|---------|-------|-----------|-------|--------|------|----------------|--------|
| Runtime Protection | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ |
| Input Scanning | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Output Scanning | ✓ | ✓ | ✗ | ✗ | ✓ | ✗ | ✓ |
| Red Teaming | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| YARA Rules | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Vector DB | ✓ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ |
| Canary Tokens | ✓ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ |
| ML Classifier | ✓ | ✓ | ✗ | ✓ | ✗ | ✓ | ✓ |
| Dialog Control | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |
| Self-Hosted | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | Enterprise |
| Open Source | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |

---

## Detection Techniques Explained

Each technique has tradeoffs. This repo includes notebooks demonstrating how they work:

| Technique | Notebook | Pros | Cons |
|-----------|----------|------|------|
| Delimiters | `patterns/01_delimiter.py` | Simple, no ML | Easily bypassed |
| Dual LLM | `patterns/02_dual_llm.py` | Strong isolation | 2x latency/cost |
| Typed Extraction | `patterns/03_typed_extraction.py` | Schema constraints | Requires modeling |
| Dry-Run Eval | `patterns/04_dry_run.py` | Validates actions | Evaluator can be fooled |
| YARA Rules | `techniques/yara_detection.py` | Fast, customizable | Only catches known patterns |
| Vector Similarity | `techniques/vector_similarity.py` | Catches variants | Requires embedding DB |
| ML Classifier | `techniques/ml_classifier.py` | Context-aware | Probabilistic |
| Canary Tokens | `techniques/canary_tokens.py` | Detects leakage | Doesn't prevent injection |

---

## Choosing the Right Tool

### For Startups / Small Teams
- **LLM Guard** - Open source, easy to start
- **Rebuff** - If you want canary tokens

### For Enterprise
- **Lakera Guard** - Managed, fast, proven
- **Prompt Shields** - If already on Azure

### For Security Teams / Pen Testing
- **Garak** - Comprehensive probe library
- **Augustus** - If you prefer Go

### For Conversational AI
- **NeMo Guardrails** - Dialog flow control

### For Research / Learning
- **This repo!** - Understand how each technique works

---

---

## The Framework Integration Gap

### Why Don't LangChain, LlamaIndex, etc. Integrate Security?

| Framework | Focus | Security Approach |
|-----------|-------|-------------------|
| **LangChain** | Orchestration, chains, agents | "Use callbacks for DIY" |
| **LlamaIndex** | RAG, data connectors | Data residency only |
| **CrewAI** | Multi-agent orchestration | "Careful guardrails" (manual) |
| **AutoGen** | Agent conversations | Human-in-the-loop |
| **Haystack** | Search pipelines | No built-in protection |

### Why This Gap Exists

1. **Different priorities** - Frameworks optimize for developer experience and capabilities, not security
2. **"Shared responsibility"** - They explicitly say security is your problem
3. **Performance concerns** - Detection adds 10-50ms latency per request
4. **Liability avoidance** - No one wants to promise security they can't guarantee
5. **Rapidly evolving threats** - New attacks appear faster than frameworks update
6. **No standard interface** - Each security tool has different APIs

### What Integration Should Look Like

```python
# Hypothetical: What LangChain COULD do
from langchain.security import PromptShield

chain = LLMChain(
    llm=llm,
    prompt=prompt,
    input_guards=[
        PromptInjectionDetector(),
        PIIScanner(),
    ],
    output_guards=[
        SensitiveDataFilter(),
        FactualityChecker(),
    ],
)
```

### Who IS Doing It Right?

| Solution | Approach |
|----------|----------|
| **NeMo Guardrails** | Security-first framework with Colang DSL |
| **Azure AI Content Safety** | Integrated into Azure OpenAI endpoints |
| **AWS Bedrock Guardrails** | Built into Bedrock API |
| **Anthropic's Constitutional AI** | Trained into the model |

### The Real Solution

Until frameworks integrate security properly, you need to:

1. **Wrap your LLM calls** with security layers (Vigil, LLM Guard)
2. **Use architectural patterns** (Dual LLM, typed extraction) 
3. **Add deterministic validation** on top of probabilistic detection
4. **Assume breach** and limit blast radius

This is why this repo exists—to teach the patterns you need to implement yourself.

---

## References

- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [Microsoft Spotlighting Paper](https://arxiv.org/abs/2403.14720)
- [Simon Willison on Prompt Injection](https://simonwillison.net/series/prompt-injection/)
- [Garak Paper](https://arxiv.org/abs/2406.11036)
