# Review Feedback — Batch A (mkdocs front pages)

Format: one item per row. Status: `[ ]` open, `[x]` addressed, `[-]` won't do. Use the **Reply** line for decisions/notes.

---

## `docs/index.md`

- [x] **A1 — Revert subtitle.**
- [x] **A2 — Willison attribution buried the lede.**
- [x] **A3 — First-person voice on landing page.**
- [x] **A4 — Rule-of-thumb edit weakened punch.**
- [x] **A5 — Defense Levels grid omits MCP (9) and Memory (10).**
- [x] **A6 — Cheatsheet sits inside "Defense Levels" grid**
- [x] **A7 — Blast-radius cell verbose.**
- [x] **A8 — Extra blank line at line 126**
- [x] **A9 — "externally communicate" appears twice in close succession**

---

## `docs/principles.md`

- [x] **P1 — Typo + dead parenthetical.**
- [x] **P2 — "etc..." closes a foundational list.**
- [x] **P3 — Axiom 4 framing has three layered corrections.**
- [x] **P4 — Insider references.**
- [-] **P5 — Axiom 1 intern metaphor tangled.**
- [x] **P6 — §4 (Pre-Packaged Agents) overlaps with `guide/7`.**
- [x] **P7 — Deep-dive links go to GitHub `.py` files**
- [-] **P8 — Mixed register.**
- [x] **P9 — "very dangerous" in §4 (line 121) editorializes**
- [x] **P10 — "...you get the idea" in sed/awk code block (line 53)**

---

## Cross-file (Batch A)

- [x] **X1 — Defense ordering disagrees between the two pages.**

---

# Review Feedback — Batch B (mkdocs reference layer)

Files: `docs/reference/{tools, attack_taxonomy, threat_model, cheatsheet, architecture, tradeoffs, references}.md`. These define canonical descriptions for the rest of the site — where they drift, readers see two answers to the same question. Items prefixed `B`; cross-file items prefixed `XB`.

---

## `docs/reference/tools.md`

- [x] **B1 — Broken notebook paths in Detection Techniques table.**
- [x] **B2 — Vigil and Rebuff detail sections.**

### Medium

- [ ] **B3 — "Framework Integration Gap" section at the bottom** (lines 505-567) is tonally different from the rest of the file — a 60-line editorial about why frameworks don't integrate security, ending with "This is why this repo exists." Good content but doubles the file's job (tools comparison + opinion piece). Two options: (a) move to its own page (e.g., `reference/framework_integration.md` or end of `architecture.md`); (b) leave but add a short anchor explaining it's editorial framing.
  Reply: 

- [x] **B4 — "Choosing the Right Tool" audience categories.**

---

## `docs/reference/attack_taxonomy.md`

### High

- [ ] **B5 — Defense Prioritization numbering overlaps.** Lines 361-382: Must Have lists 1-5, Should Have starts at *5* and goes 5-10, Nice to Have starts at *9* and goes 9-14. Numbers double up and the reader can't tell what's in which bucket. Either restart numbering per bucket (1-5 / 1-6 / 1-6) or drop numbers and use bullets.
  Reply: let's use bullets

### Medium

- [ ] **B6 — Lethal Trifecta wording differs across the site.** This file's version (line 319: "Emails, credentials, PII, internal docs") is one of five subtly-different phrasings. See cross-file item **XB1** below for the full picture and the decision.
  Reply:

---

## `docs/reference/threat_model.md`

- [x] **B7 — References section links to GitHub notebooks**
- [x] **B8 — "more isolation — not better prompts" wording**
- [x] **B9 — "Step 4: Choose Your Controls" bucket ordering**

---

## `docs/reference/cheatsheet.md`

- [x] **B10 — Decision Tree's first question is misleading.**
- [x] **B11 — Level 2 example shows only delimiters.**
- [x] **B12 — Level 5 mermaid is one example, not canonical.**

---

## `docs/reference/architecture.md`

### High

- [ ] **B13 — "Defense Tiers" 1-4 framing conflicts with "Defense Levels" 1-5 used everywhere else.** Same class of bug as X1. Tiers (Hope and Prayer / Probabilistic Guardrails / Defense in Depth / Architectural Separation) is a maturity model; Levels (Detection / Prompt Eng / Isolation / Secure Arch / Defense in Depth) is the curriculum. Both names are useful, but "Tier 3 = Defense in Depth" and "Level 5 = Defense in Depth" overload the term.

  Options:
  1. **Rename** Tiers → "Maturity Levels" (or "Maturity Ladder") and add one sentence explaining the difference. *Cheapest, recommended.*
  2. **Drop** Tiers entirely; rework the section using existing Defense Level vocabulary.
  3. **Move** Tiers to a separate "Maturity Model" page.
  Reply: 1

- [ ] **B14 — Bottom-of-page "Threat Model" section** (lines 242-262) duplicates `threat_model.md` in a less-developed form. Collapse to a one-paragraph teaser + link.
  Reply: Yes, agreed

### Medium

- [ ] **B15 — Practical Guidelines 1-8 overlap with `tradeoffs.md` and `guide/4_secure_architecture.md`.** Same patterns (Scope Tools / Read+Write separation / Typed Extraction / Symbolic References / Confirmation / Provenance / Dry-Run / Output Validation) are described in three places. Drift risk.

  Structural question: **what is this file's unique value?** Strongest sections are "What Doesn't Work" and "Defense Tiers" (maturity ladder). Suggest scope-reducing to those two; the Practical Guidelines either deleted or collapsed to a brief "Cross-pattern principles" pointer to `guide/4`.
  Reply: Agreed. Let's add links.

- [ ] **B16 — Symbolic References is orphaned.** Section 4 of this file is the only real description of the Symbolic References pattern on the site (verified: 4 mentions here, 1 in `attack_taxonomy.md`'s defense prioritization, nowhere else). Either give it a proper home in `guide/4_secure_architecture.md` so it's not living in a reference-only page, or drop it (the CaMeL section in `guide/4` covers the same intuition).
  Reply:

---

## `docs/reference/tradeoffs.md`

### High

- [ ] **B17 — "Recommendation" omits isolation entirely.** Lines 226-238: "Start with Dual LLM as your baseline architecture" — but we just established (X1) that the deployment order is Isolation → Detection → Secure Architecture → Defense in Depth. Starting with Dual LLM is software-architecture-first and contradicts `principles.md` §5.

  Suggested rewrite: insert "Start with Isolation (works on any agent, no code changes)" as step 1, push Dual LLM to step 2 onward. Otherwise readers get different deployment advice on different pages.
  Reply:

### Medium

- [ ] **B18 — Pattern 5 "Combined Defense" doesn't include detection or isolation** (lines 173-180). It layers: delimiters → typed extraction → plan → evaluate → output validation. `cheatsheet.md` Level 5 includes detection and isolation in its example chain. Two pages, two definitions of "combined defense." Either standardize, or be explicit that this is *one* combined stack of several.
  Reply:

---

## `docs/reference/references.md`

### Medium

- [ ] **B19 — Tools Documentation table** (lines 80-86) lists Vigil and Rebuff with no inactive/archived marker. `tools.md` marks them inactive. One page saying "active," another saying "inactive" is a small credibility hit. Either add `(inactive)` / `(archived)` markers, or drop those two rows.
  Reply:

---

## Cross-file (Batch B)

- [ ] **XB1 — Lethal Trifecta wording drifts across 5 files.** Appears in `index.md`, `principles.md`, `attack_taxonomy.md`, `threat_model.md`, `cheatsheet.md`, each subtly different. Examples for "Access to Private Data":
  - `index.md`: "...emails, files, credentials, PII — one of the most common purposes of tools."
  - `principles.md`: "Emails, files, credentials, PII, internal docs"
  - `attack_taxonomy.md`: "Emails, credentials, PII, internal docs"
  - `threat_model.md`: "_List every source of private data the agent can read_" (template — fine as-is)
  - `cheatsheet.md`: "Can read your emails, files, credentials, PII"

  Recommend: pick **`principles.md`** as canonical, then have `index.md` / `attack_taxonomy.md` / `cheatsheet.md` use punchier elliptical versions — but in *identical wording* across those three. I'd lock canonical wording and propagate. Want me to do that as part of this batch?
  Reply:

- [ ] **XB2 — "Defense Tiers" vs "Defense Levels" naming.** Resolution depends on B13. If you keep both, we need one sentence somewhere (probably `architecture.md`) explaining the difference. If you drop Tiers, this is moot.
  Reply:

- [ ] **XB3 — Pattern naming consistency.** Some patterns have multiple names across the reference layer:
  - "Quarantined LLM" (tradeoffs.md, guide/4, architecture.md §1) = "Reader Agent" (architecture.md §2)
  - "Privileged LLM" (tradeoffs.md, guide/4, architecture.md §1) = "Writer Agent" (architecture.md §2)

  My vote: standardize on "Quarantined LLM" / "Privileged LLM" (matches Simon Willison's original Dual LLM post and is more precise than Reader/Writer — a privileged LLM also reads).
  Reply:

- [ ] **XB4 — Deployment-order recommendation should match across `principles.md` §5 and `tradeoffs.md` "Recommendation".** See B17 — these two currently disagree. Resolved if B17 is applied.
  Reply:

---

## My pick if you only do four things (Batch B)

1. **B13 + XB2** — decide Tiers vs Levels and write the one-sentence clarifier. One coherent ordering across the site.
2. **B17 + XB4** — fix `tradeoffs.md` Recommendation so it agrees with the X1 deployment order from Batch A.
3. **B7 + B8 + B9** — propagate the Batch A fixes (P7 link policy, A4 wording, deployment ordering) into `threat_model.md`.
4. **XB1** — lock canonical Lethal Trifecta wording. Easiest win for cross-file consistency.

The rest is opinionated polish, plus **B1** (broken links — small but worth fixing regardless).
