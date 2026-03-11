# Agentic Security Guide

A comprehensive guide to securing AI agents against prompt injection and related attacks.

## How to Use This Guide

**Reading online?** Browse the markdown files in each section.

**Want to experiment?** Run the interactive [Marimo notebooks](../notebooks/).

## Sections

### [0. Baseline](0_baseline/)
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

### [3. Secure Architecture](3_secure_architecture/)
Architectural patterns for isolating concerns and limiting blast radius.
- Dual LLM (quarantine + privilege)
- Typed extraction (schema as firewall)
- Dry-run evaluation (plan → evaluate → execute)

### [4. Defense in Depth](4_defense_in_depth/)
Layering all techniques together for comprehensive protection.

### [5. Framework Integration](5_integration/)
Applying security patterns to real-world frameworks (LangChain, etc.).

---

## Quick Reference

| Level | Approach | Effort | Protection |
|-------|----------|--------|------------|
| Detection | Filter inputs | Drop-in | ~95% |
| Prompt Engineering | Harden prompts | Low | +5% |
| Secure Architecture | Redesign system | High | +10% |
| Defense in Depth | All of above | Highest | ~99% |

See also: [Tools Comparison](../docs/TOOLS.md) | [Threat Model](../docs/THREAT_MODEL.md)
