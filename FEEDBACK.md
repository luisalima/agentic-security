# Review Feedback — Batch A (mkdocs front pages)

Format: one item per row. Status: `[ ]` open, `[x]` addressed, `[-]` won't do. Use the **Reply** line for decisions/notes.

---

## `docs/index.md`

### High

- [ ] **A1 — Revert subtitle.** Your uncommitted diff swapped "— practical defense patterns, from simple detection to..." for "with practical defense patterns, ranging from...". Em-dash is punchier; "ranging from" is filler.
  Reply: I don't want it to sound too AI-ish

- [ ] **A2 — Willison attribution buried the lede.** Line 24 now opens with "The Lethal Trifecta was coined by Simon Willison." Substance ("vulnerable if it has all three") got demoted. Suggest: `Coined by Simon Willison: your AI agent is vulnerable if it has all three.` Or move attribution to a parenthetical/footnote.
  Reply: ok, I like your suggestion

- [ ] **A3 — First-person voice on landing page.** Line 54 "For me, the threat model when working with AI is always:" — first-person fits `principles.md`, jars on landing page. Original "**Assume the agent can go rogue.**" was a stronger lede.
  Reply: Ok

- [ ] **A4 — Rule-of-thumb edit weakened punch.** Line 66 parenthetical buries the contrast. Suggest: `you need **deterministic controls — isolation, scoped tokens, schema validation — not better prompts.**`
  Reply: ok, but kill the em-dash

### Medium

- [ ] **A5 — Defense Levels grid omits MCP (9) and Memory (10).** New chapters are invisible from the landing page. Add a 7th card "Specialized topics" or a footer note.
  Reply: let's add, but specialized topics sounds.. bland. maybe supporting systems?

- [ ] **A6 — Cheatsheet sits inside "Defense Levels" grid** but isn't a level. Retitle the section or split into two grids (Defense Levels + Quick Refs).
  Reply: ok split into two 

- [ ] **A7 — Blast-radius cell verbose.** Line 60 "Usually yes, because it won't reach the destination" — the "approval required" Example already implies the rationale. Could be just "Usually yes."
  Reply: I was a bit confused the first time I read this.

### Low

- [ ] **A8 — Extra blank line at line 126** left over from the `<small>` deletion.
  Reply: remove

- [ ] **A9 — "externally communicate" appears twice in close succession** in the Exfiltrate card (lines 38, 44). Tighten.
  Reply: tighten

---

## `docs/principles.md`

### High

- [ ] **P1 — Typo + dead parenthetical.** Line 66 "(view instructions a suggestions)" — meant "as," and the parenthetical adds nothing. Just delete it.
  Reply: let's keep it but fix typo

- [ ] **P2 — "etc..." closes a foundational list.** Line 77 undercuts the strong four-bullet pattern of Axiom 4. Either commit to four as canonical, or add a fifth (e.g., `Don't ask the agent to keep secrets — don't put secrets in its context`).
  Reply: ok, let's cut the etc

- [ ] **P3 — Axiom 4 framing has three layered corrections.** Line 70 "deterministically remove, or rather not provide, access. As a wrapper. Not as a setting." Suggest: `Restrictions must be enforced *outside* the agent — by the surrounding system, not by the agent's own configuration. The agent itself is unreliable; the wrapper is what makes it safe.`
  Reply: ok, sounds good

- [ ] **P4 — Insider references.** `letai` (line 41) and `OpenClaw, NanoClaw` (line 119) read like inside jokes to external readers. Qualify letai ("a multi-agent orchestrator at Nubia Labs"); replace OpenClaw/NanoClaw with widely-known examples (Manus, AutoGPT, Devin) or descriptive labels.
  Reply: OpenClaw and NanoClaw are real and widespread. letai you're right. But it's at Liwala.

### Medium

- [ ] **P5 — Axiom 1 intern metaphor tangled.** Line 35 "doesn't know very well how to distinguish good from evil and who might follow instructions from anyone..." Suggest: `Treat every agent as a brilliant, eager-to-please intern who can't tell your instructions apart from instructions buried in a PDF by an attacker — and will happily follow either.`
  Reply: hmmm.. I'd keep the one I wrote

- [ ] **P6 — §4 (Pre-Packaged Agents) overlaps with `guide/7`.** Structural choice: principles = teaser + link, guide/7 = practical tables; or the inverse. Recommend principles stays short, guide/7 owns the tables.
  Reply: ok but let's update the tables if I updated smth there

- [ ] **P7 — Deep-dive links go to GitHub `.py` files**, not in-site guide chapters (lines 98, 143, 155, 161, 167, 173). Bounces readers out of the docs site at every section break. Point to guide chapter as primary, notebook as secondary.
  Reply:  I agree, let's point to guide chapter as primary

### Low

- [ ] **P8 — Mixed register.** Line 56 "It's creative. It is not optimizing for intention, but rather for task completion." Suggest: `It's creative — optimizing for task completion, not user intent.`
  Reply: lets keep what it is

- [ ] **P9 — "very dangerous" in §4 (line 121) editorializes** in a way the rest of the doc doesn't. Cut.
  Reply: ok

- [ ] **P10 — "...you get the idea" in sed/awk code block (line 53)** is casual relative to surrounding voice. End the block after `awk`; add one sentence outside it.
  Reply: ok

---

## Cross-file (the only thing I'd call a bug)

- [ ] **X1 — Defense ordering disagrees between the two pages.**
  - `index.md` "Defense Levels": Detection → Prompt Eng → Isolation → Secure Arch → Defense in Depth (curriculum order).
  - `principles.md` §5 "Implementation Path": Isolation → Software Arch → Detection → Defense in Depth (omits Prompt Eng).

  Two valid intents tangled: **reading order** vs **deployment order**. If you want both, make it explicit on principles §5 — retitle to "Implementation Order (different from the reading order)" and say so in one sentence. Otherwise readers assume one page is wrong.
  Reply: I have mixed feelings here. I would say it should be isolation, then detection, etc... WDYT?

---
