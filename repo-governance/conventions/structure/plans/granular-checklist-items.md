---
title: "Granular Checklist Actions Within Outcome Sections"
description: Requires execution-grade action checkboxes while preserving cohesive acceptance-criterion outcomes.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when writing or reviewing delivery checklist detail, action granularity, and outcome cohesion.
---

# Granular Checklist Actions Within Outcome Sections

Write `delivery.md` so a junior engineer fresh from bootcamp with no professional work experience
and no repository or stack context can execute it without chat or tribal context.
Do not assume they can infer a missing file, symbol, command, dependency, order, expected failure,
or safe stopping condition from professional experience.

Structure the checklist as cohesive outcome sections, then expose execution as granular checkboxes.
Every checkbox represents exactly one concrete, independently verifiable action. Do not hide
multiple file edits, tests, migrations, documentation changes, or verification commands behind one
omnibus checkbox merely because they contribute to one outcome. A large number of useful
checkboxes is acceptable; checklist count is not a reason to remove execution detail.

Each outcome section carries:

- the canonical acceptance-criterion ID or title;
- **Input** — trusted starting evidence, dependencies, affected scope, and prerequisites;
- **Outcome** — the observable state that must exist;
- ordered action checkboxes, each with `[AI]`, `[HUMAN]`, or `[AI+HUMAN]`, an exact affected
  path/symbol or bounded discovery rule, copyable command/inspection where applicable, expected
  observation, failure handling, and evidence destination; and
- **Proof** — the focused and regression gates that accept the whole outcome.

For code outcomes, RED, GREEN, and REFACTOR are separate granular checkboxes inside the same outcome
section. They share the canonical AC and outcome, but each remains observable and tickable. A
non-code action uses the same exact-path/command/observation detail without artificial TDD labels.

**Bad** (too coarse):

```markdown
### AC-COVERAGE-03 — Cross-format coverage

- [ ] [AI] Implement coverage merging with all formats and tests
```

**Good** (cohesive outcome, granular execution):

```markdown
### AC-COVERAGE-03 — Cross-format coverage maps merge deterministically

- **Input:** existing parsers and AC-COVERAGE-03 in `prd.md`.
- **Outcome:** same-format, cross-format, overlap, and malformed-input behavior matches the contract.
- [ ] [AI] **RED:** add same-format and cross-format failures to
      `internal/testcoverage/merge_test.go`; run `rtk nx run coverage:test:unit`; acceptance: the new
      cases fail with the missing-normalization assertion while the existing suite remains green;
      record the output in the phase evidence.
- [ ] [AI] **GREEN:** add `CoverageMap` and merge logic to `internal/testcoverage/merge.go`; rerun
      `rtk nx run coverage:test:unit`; acceptance: the new and existing focused cases pass.
- [ ] [AI] **REFACTOR:** make each parser return `CoverageMap` without changing behavior; rerun the
      focused suite and `rtk nx run coverage:test:quick`; acceptance: both commands exit zero and
      diagnostics remain stable.
- **Proof:** RED evidence plus the passing focused and regression outputs.
```

**Action-granularity test:** Can this checkbox be truthfully ticked and verified without silently
completing another distinct action? If not, split it.

**Outcome-cohesion test:** Do the actions share one acceptance criterion, observable outcome, and
proof boundary? If not, create another outcome section.

Do not create checkboxes for keystrokes, every line edit, or repeated invocations with no distinct
observation. Do not copy canonical Gherkin into delivery. Granularity exposes meaningful execution
and evidence; it does not reward checkbox count.

Outcome cohesion does not define a delivery unit or relax PR-size governance. Split delivery at the
existing independently reviewable, verifiable, revertible natural seams and apply the Delivery
Boundaries table, addition limits, and atomicity rule. Never create one PR per phase mechanically;
never use fewer checkboxes to justify an oversized PR.
