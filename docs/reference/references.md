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
| [Defending Against Indirect Prompt Injection Attacks With Spotlighting](https://arxiv.org/abs/2403.14720) | Hines et al. (Microsoft) | 2024 | Random delimiter defense; reduces attack success from >50% to <2% |
| [StruQ: Defending Against Prompt Injection with Structured Queries](https://arxiv.org/abs/2402.06363) | Chen et al. | 2024 | Structured data extraction as defense |
| [CaMeL: Defeating Prompt Injections by Design](https://arxiv.org/abs/2503.18813) | Google DeepMind | 2025 | Capability-based security architecture; typed data flow |
| [Jatmo: Prompt Injection Defense by Task-Specific Finetuning](https://arxiv.org/abs/2312.17673) | Piet et al. | 2023 | Fine-tuning models to resist injection |

### Jailbreaking & Red Teaming

| Paper | Authors | Year | Key Contribution |
|-------|---------|------|------------------|
| [Garak: A Framework for Security Probing Large Language Models](https://arxiv.org/abs/2406.11036) | NVIDIA | 2024 | Comprehensive LLM vulnerability scanner |
| [Universal and Transferable Adversarial Attacks on Aligned Language Models](https://arxiv.org/abs/2307.15043) | Zou et al. | 2023 | Automated adversarial suffix generation |
| [Do Anything Now: Characterizing and Evaluating In-The-Wild Jailbreak Prompts on LLMs](https://arxiv.org/abs/2308.03825) | Shen et al. | 2023 | Analysis of jailbreak techniques in the wild |
| [Zhan et al. — Adaptive Attacks Break Defenses Against Indirect Prompt Injection (NAACL 2025)](https://doi.org/10.18653/v1/2025.findings-naacl.395) | Zhan et al. | 2025 | Adaptive attacks defeating current defenses |
| [Heverin et al. — Systematically Analysing Prompt Injection Vulnerabilities in Diverse LLM Architectures (2025)](https://doi.org/10.34190/iccws.20.1.3292) | Heverin et al. | 2025 | Systematic analysis across architectures |
| [Fu et al. — Imprompter: Tricking LLM Agents into Improper Tool Use](https://imprompter.ai/paper.pdf) | Fu et al. | 2025 | Attacks on agent tool use |
| [PoisonedRAG — Knowledge Corruption Attacks to RAG (USENIX Security 2025)](https://arxiv.org/abs/2402.07867) | Zou et al. | 2025 | 5 crafted documents can manipulate AI responses 90% of the time |

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
- [NCSC — Prompt Injection Is Not SQL Injection (Dec 2025)](https://www.ncsc.gov.uk/blog-post/prompt-injection-not-sql-injection)
- [Anthropic — Disrupting AI-Orchestrated Espionage (Sep 2025)](https://www.anthropic.com/news/disrupting-AI-espionage) — First documented AI-orchestrated cyberattack
- [Microsoft MSRC — How Microsoft Defends Against Indirect Prompt Injection (Jul 2025)](https://www.microsoft.com/en-us/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks/)
- [tldrsec — Prompt Injection Defenses (comprehensive catalog)](https://github.com/tldrsec/prompt-injection-defenses)
- [HiddenLayer — 2026 AI Threat Landscape Report](https://hiddenlayer.com/research/2026-ai-threat-landscape/)

---

## Standards & Frameworks

| Resource | Organization | Description |
|----------|--------------|-------------|
| [OWASP Top 10 for LLM Applications (2025)](https://owasp.org/www-project-top-10-for-large-language-model-applications/) | OWASP | Industry standard risk ranking; LLM01 = Prompt Injection |
| [OWASP Top 10 for Agentic Applications (2026)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | OWASP | Agentic-specific risks |
| [OWASP GenAI Data Security Risks & Mitigations (2026)](https://genai.owasp.org/resource/owasp-genai-data-security-risks-mitigations-2026/) | OWASP | Data security for GenAI |
| [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) | NIST | Broader AI risk guidance |
| [NIST AI 600-1 — Generative AI Risk Management Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) | NIST | GenAI-specific risk profile |
| [NIST SP 800-218A — Secure Software Development for GenAI](https://doi.org/10.6028/NIST.SP.800-218A) | NIST | Secure development practices for GenAI |
| [MITRE ATLAS](https://atlas.mitre.org/) | MITRE | Adversarial threat landscape for AI systems — 66 techniques, 46 subtechniques as of Oct 2025 |

---

## Tools Documentation

| Tool | Documentation | Focus |
|------|---------------|-------|
| [Vigil](https://vigil.deadbits.ai/) ⚠️ inactive since 2023 | Multi-layer detection | YARA, vectors, ML, canaries |
| [LLM Guard](https://protectai.github.io/llm-guard/) | Runtime guardrails | Input/output scanning |
| [Garak](https://docs.garak.ai/) | Red teaming | Vulnerability probing |
| [NeMo Guardrails](https://docs.nvidia.com/nemo/guardrails/) | Dialog control | Colang DSL |
| [Rebuff](https://github.com/protectai/rebuff) ⚠️ archived May 2025 | Self-hardening detection | Canary tokens |

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

## Real-World Incidents & CVEs

- [CVE-2025-34291 — Langflow RCE (CVSS 9.4)](https://nvd.nist.gov/vuln/detail/CVE-2025-34291) — AI agent framework account takeover
- [CVE-2025-32711 — Microsoft Copilot EchoLeak](https://www.securityweek.com/the-wild-wild-west-of-agentic-ai-an-attack-surface-cisos-cant-afford-to-ignore/) — First zero-click attack against an AI agent
- [CVE-2025-6514 — mcp-remote OS command injection](https://nvd.nist.gov/vuln/detail/CVE-2025-6514) — Affected 437K environments
- [Slack AI Data Exfiltration (Aug 2024)](https://www.lakera.ai/blog/agentic-ai-threats-p1) — Memory poisoning via indirect prompt injection
- [PhantomRaven Supply Chain Attack (2025)](https://socket.dev/blog/phantom-raven) — 126 malicious npm packages via slopsquatting, 86K downloads

---

## Contributing

Found a relevant paper or resource? Open a PR to add it!
