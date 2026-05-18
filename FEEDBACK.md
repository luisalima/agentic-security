# Review Feedback — Batch A (mkdocs front pages)

Format: one item per row. Status: `[ ]` open, `[x]` addressed, `[-]` won't do. Use the **Reply** line for decisions/notes.

---

## `docs/index.md`

### High

- [x] **A1 — Revert subtitle.** Your uncommitted diff swapped "— practical defense patterns, from simple detection to..." for "with practical defense patterns, ranging from...". Em-dash is punchier; "ranging from" is filler.
  Reply: I don't want it to sound too AI-ish

- [x] **A2 — Willison attribution buried the lede.** Line 24 now opens with "The Lethal Trifecta was coined by Simon Willison." Substance ("vulnerable if it has all three") got demoted. Suggest: `Coined by Simon Willison: your AI agent is vulnerable if it has all three.` Or move attribution to a parenthetical/footnote.
  Reply: ok, I like your suggestion
  Applied: replaced with the suggested phrasing.

- [x] **A3 — First-person voice on landing page.** Line 54 "For me, the threat model when working with AI is always:" — first-person fits `principles.md`, jars on landing page. Original "**Assume the agent can go rogue.**" was a stronger lede.
  Reply: Ok
  Applied: reverted lede; folded the "design so the worst case is acceptable" sentence into the same paragraph.

- [x] **A4 — Rule-of-thumb edit weakened punch.** Line 66 parenthetical buries the contrast. Suggest: `you need **deterministic controls — isolation, scoped tokens, schema validation — not better prompts.**`
  Reply: ok, but kill the em-dash
  Applied: `you need **deterministic controls (isolation, scoped tokens, schema validation), not better prompts**.` (no em-dashes)

### Medium

- [x] **A5 — Defense Levels grid omits MCP (9) and Memory (10).** New chapters are invisible from the landing page. Add a 7th card "Specialized topics" or a footer note.
  Reply: let's add, but specialized topics sounds.. bland. maybe supporting systems?
  Applied: new `## Supporting Systems` grid below Defense Levels with MCP + Memory cards.

- [x] **A6 — Cheatsheet sits inside "Defense Levels" grid** but isn't a level. Retitle the section or split into two grids (Defense Levels + Quick Refs).
  Reply: ok split into two 
  Applied: removed Cheatsheet from Defense Levels grid; added it as a bullet in Getting Started so we don't end up with 3 grids on the landing page.

- [x] **A7 — Blast-radius cell verbose.** Line 60 "Usually yes, because it won't reach the destination" — the "approval required" Example already implies the rationale. Could be just "Usually yes."
  Reply: I was a bit confused the first time I read this.
  Applied: collapsed to "Usually yes" — the Example column carries the rationale.

### Low

- [x] **A8 — Extra blank line at line 126** left over from the `<small>` deletion.
  Reply: remove
  Applied: gone (collapsed via the surrounding structural rewrite of the grids section).

- [x] **A9 — "externally communicate" appears twice in close succession** in the Exfiltrate card (lines 38, 44). Tighten.
  Reply: tighten
  Applied: `The agent can take outbound actions: send emails, make API calls, write to external services.`

---

## `docs/principles.md`

### High

- [x] **P1 — Typo + dead parenthetical.** Line 66 "(view instructions a suggestions)" — meant "as," and the parenthetical adds nothing. Just delete it.
  Reply: let's keep it but fix typo
  Applied: typo fixed, parenthetical kept.

- [x] **P2 — "etc..." closes a foundational list.** Line 77 undercuts the strong four-bullet pattern of Axiom 4. Either commit to four as canonical, or add a fifth (e.g., `Don't ask the agent to keep secrets — don't put secrets in its context`).
  Reply: ok, let's cut the etc
  Applied: removed.

- [x] **P3 — Axiom 4 framing has three layered corrections.** Line 70 "deterministically remove, or rather not provide, access. As a wrapper. Not as a setting." Suggest: `Restrictions must be enforced *outside* the agent — by the surrounding system, not by the agent's own configuration. The agent itself is unreliable; the wrapper is what makes it safe.`
  Reply: ok, sounds good
  Applied: replaced with the suggestion (commas not em-dash, given your anti-em-dash signal in A4).

- [x] **P4 — Insider references.** `letai` (line 41) and `OpenClaw, NanoClaw` (line 119) read like inside jokes to external readers. Qualify letai ("a multi-agent orchestrator at Nubia Labs"); replace OpenClaw/NanoClaw with widely-known examples (Manus, AutoGPT, Devin) or descriptive labels.
  Reply: OpenClaw and NanoClaw are real and widespread. letai you're right. But it's at Liwala.
  Applied: letai → "a multi-agent orchestrator at Liwala." OpenClaw/NanoClaw left as-is. (Note: the line referencing them was removed altogether as part of P6 — see below.)

### Medium

- [-] **P5 — Axiom 1 intern metaphor tangled.** Line 35 "doesn't know very well how to distinguish good from evil and who might follow instructions from anyone..." Suggest: `Treat every agent as a brilliant, eager-to-please intern who can't tell your instructions apart from instructions buried in a PDF by an attacker — and will happily follow either.`
  Reply: hmmm.. I'd keep the one I wrote
  Decision: keep original. Not applied.

- [x] **P6 — §4 (Pre-Packaged Agents) overlaps with `guide/7`.** Structural choice: principles = teaser + link, guide/7 = practical tables; or the inverse. Recommend principles stays short, guide/7 owns the tables.
  Reply: ok but let's update the tables if I updated smth there
  Applied: (1) ported your two table updates in `principles.md` to `guide/7` — "Isolate the environment" (now says "never with sensitive credentials") and "Separate environments" (now says "Promote from dev to staging to prod, ideally with a human in the loop"). (2) Collapsed `principles.md` §4 to a one-paragraph teaser pointing to `guide/7`. The three tables and the deep-dive link are gone from principles; all of that content now lives in (or is reachable from) guide/7.

- [x] **P7 — Deep-dive links go to GitHub `.py` files**, not in-site guide chapters (lines 98, 143, 155, 161, 167, 173). Bounces readers out of the docs site at every section break. Point to guide chapter as primary, notebook as secondary.
  Reply:  I agree, let's point to guide chapter as primary
  Applied: every deep-dive link in `principles.md` now points to a guide chapter. The §4 tool-validation link disappeared via the P6 collapse; §3 dry-run now points to `guide/4_secure_architecture.md#dry-run-evaluation`; §5 step links point to the corresponding `guide/*.md`. Each guide chapter already links to its notebook at the top, so the notebook is one click away.

### Low

- [-] **P8 — Mixed register.** Line 56 "It's creative. It is not optimizing for intention, but rather for task completion." Suggest: `It's creative — optimizing for task completion, not user intent.`
  Reply: lets keep what it is
  Decision: keep original. Not applied.

- [x] **P9 — "very dangerous" in §4 (line 121) editorializes** in a way the rest of the doc doesn't. Cut.
  Reply: ok
  Applied: removed as a side effect of the P6 collapse (the whole Personal Assistants subsection now lives in guide/7, which uses "the most dangerous class" — a categorical claim, not editorializing — so I left that alone).

- [x] **P10 — "...you get the idea" in sed/awk code block (line 53)** is casual relative to surrounding voice. End the block after `awk`; add one sentence outside it.
  Reply: ok
  Applied: dropped the "echo" entry and the "...you get the idea" line; added a sentence after the block: *"We could have kept removing tools indefinitely. With bash available, the agent will always find a workaround."*

---

## Cross-file (the only thing I'd call a bug)

- [x] **X1 — Defense ordering disagrees between the two pages.**
  - `index.md` "Defense Levels": Detection → Prompt Eng → Isolation → Secure Arch → Defense in Depth (curriculum order).
  - `principles.md` §5 "Implementation Path": Isolation → Software Arch → Detection → Defense in Depth (omits Prompt Eng).

  Two valid intents tangled: **reading order** vs **deployment order**. If you want both, make it explicit on principles §5 — retitle to "Implementation Order (different from the reading order)" and say so in one sentence. Otherwise readers assume one page is wrong.
  Reply: I have mixed feelings here. I would say it should be isolation, then detection, etc... WDYT?
  Applied: kept `index.md` numbered 1–5 in curriculum order (matches directory structure — renumbering would cascade through `guide/*.md` and `notebooks/*` paths). Rewrote `principles.md` §5 as **Implementation Order** with your preferred sequence: Isolation → Detection → Secure Architecture → Defense in Depth. Prompt Engineering dropped from the deployment list (marginal, never relied on alone). Added one sentence explaining this is the *deployment* order vs. the Guide's *reading* order so the two pages no longer look contradictory.

---
