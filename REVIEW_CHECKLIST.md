# Review Checklist

## Top-Level Docs

| Status | File | Notes |
|--------|------|-------|
| [ ] | `README.md` | |
| [ ] | `PRINCIPLES.md` | |
| [ ] | `CONTRIBUTING.md` | |
| [ ] | `CHANGELOG.md` | |
| [ ] | `ROADMAP.md` | |

## 0 — Vulnerabilities (Notebooks)

| Status | File | Notes |
|--------|------|-------|
| [ ] | `notebooks/0_vulnerabilities/1_baseline.py` | |
| [ ] | `notebooks/0_vulnerabilities/2_multi_turn_attacks.py` | |
| [ ] | `notebooks/0_vulnerabilities/3_multi_agent_attacks.py` | |
| [ ] | `notebooks/0_vulnerabilities/4_case_studies.py` | |

## 1 — Detection (Notebooks)

| Status | File | Notes |
|--------|------|-------|
| [ ] | `notebooks/1_detection/overview.py` | |
| [ ] | `notebooks/1_detection/1_yara_detection.py` | |
| [ ] | `notebooks/1_detection/2_vector_similarity.py` | |
| [ ] | `notebooks/1_detection/3_ml_classifier.py` | |
| [ ] | `notebooks/1_detection/4_llm_as_judge.py` | |
| [ ] | `notebooks/1_detection/5_canary_tokens.py` | |

## 2 — Prompt Engineering (Notebooks)

| Status | File | Notes |
|--------|------|-------|
| [ ] | `notebooks/2_prompt_engineering/overview.py` | |
| [ ] | `notebooks/2_prompt_engineering/1_delimiters.py` | |
| [ ] | `notebooks/2_prompt_engineering/2_system_prompt_hardening.py` | |
| [ ] | `notebooks/2_prompt_engineering/3_instruction_hierarchy.py` | |
| [ ] | `notebooks/2_prompt_engineering/4_sandwich_defense.py` | |
| [ ] | `notebooks/2_prompt_engineering/5_xml_tagging.py` | |

## 3 — Isolation Infra-Level (Notebooks)

| Status | File | Notes |
|--------|------|-------|
| [ ] | `notebooks/3_isolation_infra_level/overview.py` | |

## 4 — Secure Architecture Software (Notebooks)

| Status | File | Notes |
|--------|------|-------|
| [ ] | `notebooks/4_secure_architecture_software/overview.py` | |
| [ ] | `notebooks/4_secure_architecture_software/1_dual_llm.py` | |
| [ ] | `notebooks/4_secure_architecture_software/2_typed_extraction.py` | |
| [ ] | `notebooks/4_secure_architecture_software/3_dry_run.py` | |
| [ ] | `notebooks/4_secure_architecture_software/4_tool_validation.py` | |
| [ ] | `notebooks/4_secure_architecture_software/5_camel.py` | |
| [ ] | `notebooks/4_secure_architecture_software/6_mcp_security.py` | New — tool poisoning, rug pulls, config scanning |
| [ ] | `notebooks/4_secure_architecture_software/7_memory_security.py` | New — memory guard, namespace isolation, audit |

## 5 — Defense in Depth (Notebooks)

| Status | File | Notes |
|--------|------|-------|
| [ ] | `notebooks/5_defense_in_depth/overview.py` | |
| [ ] | `notebooks/5_defense_in_depth/combined.py` | |

## 6 — Integration (Notebooks)

| Status | File | Notes |
|--------|------|-------|
| [ ] | `notebooks/6_integration/overview.py` | |
| [ ] | `notebooks/6_integration/langchain_integration.py` | |
| [ ] | `notebooks/6_integration/pydantic_ai_integration.py` | |

## Docs Site (MkDocs / GitHub Pages)

| Status | File | Notes |
|--------|------|-------|
| [ ] | `docs/index.md` | |
| [ ] | `docs/principles.md` | |
| [ ] | `docs/guide/0_vulnerabilities.md` | Populated from notebooks |
| [ ] | `docs/guide/1_detection.md` | Populated from notebooks |
| [ ] | `docs/guide/1b_observability.md` | |
| [ ] | `docs/guide/2_prompt_engineering.md` | Populated from notebooks |
| [ ] | `docs/guide/3_isolation.md` | Populated from notebooks |
| [ ] | `docs/guide/4_secure_architecture.md` | Populated from notebooks |
| [ ] | `docs/guide/5_defense_in_depth.md` | Populated from notebooks |
| [ ] | `docs/guide/6_integration.md` | Populated from notebooks |
| [ ] | `docs/guide/7_securing_prepackaged_agents.md` | |
| [ ] | `docs/guide/8_enterprise_zero_trust.md` | |
| [ ] | `docs/guide/9_mcp_security.md` | New — MCP tool poisoning, rug pulls, supply chain |
| [ ] | `docs/guide/10_memory_security.md` | New — memory poisoning, namespace isolation, provenance |
| [ ] | `docs/reference/tools.md` | |
| [ ] | `docs/reference/attack_taxonomy.md` | |
| [ ] | `docs/reference/threat_model.md` | |
| [ ] | `docs/reference/cheatsheet.md` | |
| [ ] | `docs/reference/architecture.md` | |
| [ ] | `docs/reference/tradeoffs.md` | |
| [ ] | `docs/reference/references.md` | |

## Scripts & Config

| Status | File | Notes |
|--------|------|-------|
| [ ] | `mkdocs.yml` | |
| [ ] | `pyproject.toml` | |
| [ ] | `.gitignore` | |
| [ ] | `.github/workflows/ci.yml` | |
| [ ] | `.github/workflows/docs.yml` | |

## Source Code — Defenses

| Status | File | Notes |
|--------|------|-------|
| [ ] | `src/agentic_security/defenses/camel.py` | |
| [ ] | `src/agentic_security/defenses/canary_tokens.py` | |
| [ ] | `src/agentic_security/defenses/delimiters.py` | |
| [ ] | `src/agentic_security/defenses/dry_run.py` | |
| [ ] | `src/agentic_security/defenses/dual_llm.py` | |
| [ ] | `src/agentic_security/defenses/mcp_security.py` | New — MCP tool poisoning, rug pull detection |
| [ ] | `src/agentic_security/defenses/memory_security.py` | New — memory guard, namespace isolation |
| [ ] | `src/agentic_security/defenses/ml_classifier.py` | |
| [ ] | `src/agentic_security/defenses/output_validation.py` | |
| [ ] | `src/agentic_security/defenses/tool_validation.py` | |
| [ ] | `src/agentic_security/defenses/typed_extraction.py` | |
| [ ] | `src/agentic_security/defenses/vector_similarity.py` | |
| [ ] | `src/agentic_security/defenses/xml_tagging.py` | |
| [ ] | `src/agentic_security/defenses/yara_detection.py` | |

## Source Code — Attacks & Core

| Status | File | Notes |
|--------|------|-------|
| [ ] | `src/agentic_security/attacks/multi_agent.py` | |
| [ ] | `src/agentic_security/llm.py` | |
| [ ] | `src/agentic_security/scenario.py` | |

## Tests

| Status | File | Notes |
|--------|------|-------|
| [ ] | `tests/test_camel.py` | |
| [ ] | `tests/test_canary_tokens.py` | |
| [ ] | `tests/test_delimiters.py` | |
| [ ] | `tests/test_dry_run.py` | |
| [ ] | `tests/test_dual_llm.py` | |
| [ ] | `tests/test_mcp_security.py` | New — 14 tests |
| [ ] | `tests/test_memory_security.py` | New — 16 tests |
| [ ] | `tests/test_ml_classifier.py` | |
| [ ] | `tests/test_multi_agent.py` | |
| [ ] | `tests/test_output_validation.py` | |
| [ ] | `tests/test_tool_validation.py` | |
| [ ] | `tests/test_typed_extraction.py` | |
| [ ] | `tests/test_vector_similarity.py` | |
| [ ] | `tests/test_yara_detection.py` | |

## Data & Benchmark

| Status | File | Notes |
|--------|------|-------|
| [ ] | `data/injection_dataset.json` | Updated — 14 new samples, 4 new categories |
| [ ] | `benchmark/run.py` | |
