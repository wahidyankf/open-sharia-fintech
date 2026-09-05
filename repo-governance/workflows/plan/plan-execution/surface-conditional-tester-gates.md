---
title: "Surface-Conditional Tester Gates"
description: States which quality gates a plan must run based on whether it ships a UI, an API, both, or neither.
when_to_use: Use when determining which tester gates a plan's shipped surface requires before archival.
---

# Surface-Conditional Tester Gates

Which quality gates this execution must run depends on **what surface the plan ships**. The rule
binds here at execution, exactly as it bound at authoring time (see
[plan-planning §Surface-Conditional Tester Gates](../plan-planning/surface-conditional-tester-gates.md#surface-conditional-tester-gates)),
and again as merge precondition (e) in the
[PR Merge Protocol](../../../development/workflow/pr-merge-protocol/the-rule.md).

- **UI-bearing plan** → run **both** [`ui/ui-quality-gate.md`](../../ui/ui-quality-gate.md) (static)
  and [`web/web-ux-test-fixing-planning.md`](../../web/web-ux-test-fixing-planning.md) (running triad).
- **API- or backend-bearing plan** → run [`api/api-quality-gate.md`](../../api/api-quality-gate.md).
- **Several of these** → run each set.
- **A reachable surface with no gate listed above** (a CLI, a library under `libs/`, a hook, a CI
  workflow) → **not exempt**. Exercise the changed behaviour through its own interface and record what
  was run.
- **Genuinely no reachable behaviour** → the plan MUST state the exemption explicitly in
  its chosen technical form; an executor that finds no such statement treats it as a gap, not as a pass.

**The three UI gates are complementary, never substitutes**: `plan-checker` **Step 5k** gates the
UI **design funnel** in `prd.md` (pre-build); `ui/ui-quality-gate.md` gates the **built components**
statically via `swe-ui-checker` / `swe-ui-fixer` (no browser); and
`web/web-ux-test-fixing-planning.md` gates the **running UI** via the EWT/UWT/DWT triad in a real
browser. Passing one never discharges another.
