# References

Academic papers, blog posts, and resources on LLM security and prompt injection.

---

## Foundational Papers

### Prompt Injection Attacks

| Paper | Authors | Year | Key Contribution |
|-------|---------|------|------------------|
| [Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) | Greshake et al. | 2023 | Foundational paper on indirect prompt injection; attacks on Bing Chat, code assistants |
| [Ignore This Title and HackAPrompt: Exposing Systemic Vulnerabilities of LLMs through a Global Scale Prompt Hacking Competition](https://arxiv.org/abs/2311.16119) | Schulhoff et al. | 2023 | Large-scale prompt injection competition; taxonomy of attack techniques |
| [Prompt Injection attack against LLM-integrated Applications](https://arxiv.org/abs/2306.05499) | Liu et al. | 2023 | Systematic study of prompt injection in integrated applications |

### Defense Techniques

| Paper | Authors | Year | Key Contribution |
|-------|---------|------|------------------|
| [Defending LLMs against Jailbreaking Attacks via Backtranslation (Spotlighting)](https://arxiv.org/abs/2403.14720) | Microsoft Research | 2024 | Random delimiter defense; reduces attack success from >50% to <2% |
| [StruQ: Defending Against Prompt Injection with Structured Queries](https://arxiv.org/abs/2402.06363) | Chen et al. | 2024 | Structured data extraction as defense |
| [CaMeL: Capability-based Memory for LLMs](https://arxiv.org/abs/2503.18813) | Google DeepMind | 2025 | Capability-based security architecture; typed data flow |
| [Jatmo: Prompt Injection Defense by Task-Specific Finetuning](https://arxiv.org/abs/2312.17673) | Piet et al. | 2023 | Fine-tuning models to resist injection |

### Jailbreaking & Red Teaming

| Paper | Authors | Year | Key Contribution |
|-------|---------|------|------------------|
| [Garak: A Framework for Security Probing Large Language Models](https://arxiv.org/abs/2406.11036) | NVIDIA | 2024 | Comprehensive LLM vulnerability scanner |
| [Universal and Transferable Adversarial Attacks on Aligned Language Models](https://arxiv.org/abs/2307.15043) | Zou et al. | 2023 | Automated adversarial suffix generation |
| [Do Anything Now: Characterizing and Evaluating In-The-Wild Jailbreak Prompts on LLMs](https://arxiv.org/abs/2308.03825) | Shen et al. | 2023 | Analysis of jailbreak techniques in the wild |

---

## Key Blog Posts & Articles

### Simon Willison's Prompt Injection Series
Essential reading from the person who named and defined prompt injection:

- [Prompt injection attacks against GPT-3](https://simonwillison.net/2022/Sep/12/prompt-injection/) (2022) — Original post naming the vulnerability
- [Delimiters won't save you from prompt injection](https://simonwillison.net/2023/May/11/delimiters-wont-save-you/) (2023) — Why simple defenses fail
- [Dual LLM pattern](https://simonwillison.net/2023/Apr/25/dual-llm-pattern/) (2023) — Architectural defense pattern
- [The Dual LLM pattern for building AI assistants that can resist prompt injection](https://simonwillison.net/2023/Apr/25/dual-llm-pattern/) (2023) — Detailed implementation guide
- [Full series](https://simonwillison.net/series/prompt-injection/)

### Other Notable Posts

- [Anthropic: Many-shot jailbreaking](https://www.anthropic.com/research/many-shot-jailbreaking) (2024) — Long-context attacks
- [OpenAI: Prompt injection](https://openai.com/index/new-embedding-models-and-api-updates/) — OpenAI's acknowledgment that injection is "unlikely to ever be fully solved"

---

## Standards & Frameworks

| Resource | Organization | Description |
|----------|--------------|-------------|
| [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) | OWASP | Industry standard risk ranking; LLM01 = Prompt Injection |
| [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) | NIST | Broader AI risk guidance |
| [MITRE ATLAS](https://atlas.mitre.org/) | MITRE | Adversarial threat landscape for AI systems |

---

## Tools Documentation

| Tool | Documentation | Focus |
|------|---------------|-------|
| [Vigil](https://vigil.deadbits.ai/) | Multi-layer detection | YARA, vectors, ML, canaries |
| [LLM Guard](https://llm-guard.com/) | Runtime guardrails | Input/output scanning |
| [Garak](https://docs.garak.ai/) | Red teaming | Vulnerability probing |
| [NeMo Guardrails](https://docs.nvidia.com/nemo/guardrails/) | Dialog control | Colang DSL |
| [Rebuff](https://github.com/protectai/rebuff) | Self-hardening detection | Canary tokens |

---

## Datasets

| Dataset | Source | Description |
|---------|--------|-------------|
| [Vigil Prompt Injection Dataset](https://huggingface.co/datasets/deadbits/vigil-jailbreak-all-MiniLM-L6-v2) | deadbits | Embeddings of known attacks |
| [HackAPrompt Dataset](https://huggingface.co/datasets/hackaprompt/hackaprompt-dataset) | Schulhoff et al. | Competition submissions |
| [Jailbreak Chat](https://jailbreakchat.com/) | Community | Crowdsourced jailbreaks |

---

## Conference Talks

- **DEF CON 31** — [Hacking AI: Prompt Injection and More](https://www.youtube.com/watch?v=Sv5OLj2nVAQ) (2023)
- **Black Hat USA 2023** — [Compromising LLMs: The Indirect Prompt Injection Threat](https://www.blackhat.com/us-23/briefings/schedule/#compromising-llms-the-indirect-prompt-injection-threat-33075)

---

## Contributing

Found a relevant paper or resource? Open a PR to add it!
