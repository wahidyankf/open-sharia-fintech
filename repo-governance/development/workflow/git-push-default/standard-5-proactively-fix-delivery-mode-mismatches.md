---
description: Fix a mis-tagged or missing Delivery Mode field the moment you find one while reading delivery checklists, unless the plan is already archived.
when_to_use: Use when reading a plan's delivery checklist and it mis-tags the merge step or assumes a stale push default.
---

# Standard 5: Proactively Fix Delivery-Mode Mismatches

When working on plans or performing any task that involves reading delivery checklists, and you
encounter an existing checklist that mis-tags the merge step, omits a required `## Delivery Mode`
override, or otherwise assumes a stale push default, fix it as part of your current work. Do not defer
it.

This applies Standard 4 of
[Proactive Preexisting Error Resolution](../../practice/proactive-preexisting-error-resolution.md) to this
convention specifically: a delivery-mode mismatch in a plan you touch is an error to fix now, not flag
for later.

**Scope of "fix now"**: correct the mismatch in the checklist and, if the plan is in
`plans/in-progress/`, note the fix in the same commit message. If the plan is in `plans/done/`
(archived), leave it — historical records are read-only.
