---
title: "TDD Shape for Delivery Checklists"
description: The mandatory three-substep RED/GREEN/REFACTOR pattern for code delivery steps, the non-code exception, and the never-combine hard rule.
category: explanation
subcategory: development
tags:
  - development
  - workflow
  - tdd
  - testing
  - red-green-refactor
created: 2026-05-02
when_to_use: Use when writing a delivery checklist item that ships code, to format it as machine-executable RED/GREEN/REFACTOR substeps.
---

# TDD Shape for Delivery Checklists

All code delivery steps in plan checklists must follow this three-substep pattern. Each substep
names an explicit file path, verbatim shell command, and a concrete acceptance criterion so the
step is machine-executable without ambiguity:

```markdown
- [ ] **RED**: Write failing test for [specific behavior]
      — command: `nx run [project]:test:unit`
      — acceptance: test fails with `[expected error message]`
- [ ] **GREEN**: Implement `[function/component]` in `[file path]`
      — command: `nx run [project]:test:unit`
      — acceptance: test passes, no other tests broken
- [ ] **REFACTOR**: Clean up [specific concern] in `[file path]`
      — command: `nx run [project]:test:unit`
      — acceptance: all tests still pass, code is cleaner
```

Non-code steps (doc edits, config changes, file creation, governance updates) do not require
RED-GREEN-REFACTOR. They use direct action + acceptance criterion instead:

```markdown
- [ ] [Action verb] `[file path]` — add/update [specific content]
      — acceptance: [concrete observable outcome]
```

**HARD RULE: Never combine RED, GREEN, and REFACTOR into a single checkbox.** Each of the three
phases must be its own `- [ ]` item in the delivery checklist. Collapsing multiple phases into
one checkbox is forbidden. Each sub-bullet in a mini-TDD nested group counts as its own
independent checkbox. `plan-checker` flags combined items as HIGH findings.

`plan-checker` flags delivery checklist items that reference code changes without this
three-substep structure as a HIGH finding.

These RED/GREEN/REFACTOR substeps are `[AI]` work — each checkbox also carries the `[AI]`/`[HUMAN]`
executor tag, and the phase they belong to ends with a `### Phase N Gate` plus a Pause Safety note,
per [Plans Organization Convention §Executor Tagging](../../../conventions/structure/plans/executor-tagging-tags-and-bias.md#executor-tagging--ai-vs-human-hard-rule)
and [§Phases as Natural Pauses With Clear Gates](../../../conventions/structure/plans/phases-as-natural-pauses.md#phases-as-natural-pauses-with-clear-gates-hard-rule).
