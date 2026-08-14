---
title: "Applying TDD to Plans"
description: How plan-maker must express code-shipping delivery items as TDD-shaped steps, and how plan-executor and swe-*-dev agents follow TDD during execution.
category: explanation
subcategory: development
tags:
  - development
  - workflow
  - tdd
  - testing
  - red-green-refactor
created: 2026-05-02
when_to_use: Use when authoring a plan's delivery.md checklist, or when executing a delivery item that ships code.
---

# Applying TDD to Plans

## Plan Creation (plan-maker)

When `plan-maker` authors a `delivery.md` checklist, items that ship code MUST be expressed as
TDD-shaped steps. Do not write "implement X, then write tests."

Write instead:

```markdown
- [ ] Write failing test for [behavior]
- [ ] Implement [behavior] to make test pass
- [ ] Refactor implementation (keep tests green)
```

Or, when one delivery item spans multiple mini-cycles, group them explicitly:

```markdown
- [ ] TDD cycle: [feature name]
  - [ ] Red: write failing test for happy path
  - [ ] Green: implement minimum code to pass
  - [ ] Red: write failing test for error path
  - [ ] Green: implement error handling to pass
  - [ ] Refactor: clean up, remove duplication
```

Note: each nested sub-bullet is its own independent checkbox tracked by the plan-execution
workflow. The parent label (`- [ ] TDD cycle:`) is a grouping label only — it must not
substitute for the three phase items.

Acceptance criteria in `prd.md` are written as Gherkin scenarios (per the
[plan-writing-gherkin-criteria skill](../../../../.claude/skills/plan-writing-gherkin-criteria/SKILL.md)).
Those Gherkin scenarios are the natural source of the first failing tests. The chain:

```
prd.md Gherkin scenario → first failing test → minimum implementation → refactor
```

`plan-checker` will flag delivery checklist items that reference code changes without a
corresponding test-first step as a HIGH finding.

## Plan Execution

`plan-executor` (the calling context orchestrating the plan-execution workflow) and all
language-specific `swe-*-dev` agents follow TDD when implementing delivery items:

- Before writing any production code for a checklist item, write a failing test.
- Confirm the test fails for the right reason.
- Write the minimum implementation to pass.
- Refactor.
- Run the full test suite (`nx run [project]:test:quick`) to confirm no regressions.

This applies inside subrepo worktrees too. The worktree execution context does not change the
TDD requirement.
