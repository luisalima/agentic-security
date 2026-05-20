# Review Feedback

Format: files with all feedback addressed roll up to a single tick. Open items keep their `Reply:` line for decisions.

---

## Batch A — mkdocs front pages

- [x] **`docs/index.md`** — A1–A9 addressed (9 items, all applied).
- [x] **`docs/principles.md`** — P1, P2, P3, P4, P6, P7, P9, P10 applied; P5, P8 kept as-is per your call (10 items).
- [x] **Cross-file** — X1 (deployment order vs reading order) reconciled.

---

## Batch B — mkdocs reference layer

- [x] **`docs/reference/attack_taxonomy.md`** — B5 (bullets), B6 (lethal-trifecta wording via XB1).
- [x] **`docs/reference/threat_model.md`** — B7 (guide-chapter links), B8 (wording aligned), B9 (bucket reorder).
- [x] **`docs/reference/cheatsheet.md`** — B10 (decision tree), B11 (prompt-eng pointer), B12 (mermaid caption), plus XB1 wording.
- [x] **`docs/reference/architecture.md`** — B13 (Maturity Levels rename), B14 (threat-model teaser), B15 (Cross-Pattern Principles), B16 (Symbolic References moved to guide/4).
- [x] **`docs/reference/tradeoffs.md`** — B17 (Recommendation rewritten — software patterns layer on top of isolation/detection), B18 (Pattern 5 includes detection + isolation, caveat added).
- [x] **`docs/reference/references.md`** — B19 (inactive/archived markers).
- [x] **Cross-file (Batch B)** — XB1 (Lethal Trifecta wording propagated to `index.md`, `attack_taxonomy.md`, `cheatsheet.md`), XB2 (resolved by B13 rename + explainer sentence), XB3 (Reader/Writer Agent terminology gone via B15 deletion; canonical "Quarantined LLM / Privileged LLM" definitions live in `guide/4`), XB4 (resolved by B17).

- [x] **`docs/reference/tools.md`** — B1, B2, B4 (round 1); B3 (this round): editorial cut, replaced with a verified "Framework Security Stance" table (LangChain/LangGraph, CrewAI, AutoGen, Pydantic AI), LlamaIndex dropped per your call, AWS Bedrock Guardrails added to commercial offerings.
