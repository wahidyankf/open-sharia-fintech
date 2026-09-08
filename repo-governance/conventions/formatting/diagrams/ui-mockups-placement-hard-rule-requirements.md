---
description: "States the hard rule that all UI design funnel artefacts must live in prd.md, plus its enforcement mechanics."
when_to_use: "Use when deciding where to place UI mockups and funnel records in a plan, or when a plan fails the placement gate."
---

# Placement — the UI Lives in prd.md (HARD RULE): Requirements and Enforcement

All UI-design-funnel artefacts for a UI-bearing plan MUST be placed in that plan's **`prd.md`**,
not in `README.md`, `brd.md`, `tech-docs.md`, or any separate file:

- **Low-fidelity ASCII wireframes** (Diverge stage, ≥ 2 named alternatives, at least mobile +
  desktop where they differ) — inline in `prd.md`.
- **High-fidelity mockups** (Narrow stage finalists) — binary image assets live under the plan's
  `assets/` folder (e.g. `plans/in-progress/<name>/assets/ui-screen.excalidraw.png`) and are
  embedded in `prd.md` via `![alt text](./assets/…)` `![]()` image links.
- **Named selection** (Select stage) — the chosen design named explicitly, in `prd.md`.
- **Rationale / decision record** (Justify stage) — the short table of why the winner won and why
  each runner-up lost, in `prd.md`.

**Enforcement**: a UI-bearing plan whose `prd.md` does NOT contain the complete funnel record
(all four stages, embedded mockup links, at minimum both the mobile and desktop low-fi wireframes
where they differ) fails the plan quality gate. `plan-checker` Step 5k flags each missing or
misplaced element as a ledger row. The gate's repair pass scaffolds missing funnel sections directly into
`prd.md`.
