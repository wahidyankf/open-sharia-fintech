---
title: "Enforcement and Exceptions"
description: How the pre-push hook and plan-checker enforce TDD, and the five kinds of change TDD does not apply to.
category: explanation
subcategory: development
tags:
  - development
  - workflow
  - tdd
  - testing
  - red-green-refactor
created: 2026-05-02
when_to_use: Use when checking whether TDD's enforcement mechanism would catch a given gap, or whether a change qualifies for an exception.
---

# Enforcement and Exceptions

## Enforcement

The pre-push hook runs `test:quick` for affected projects before every push. A code change with
no accompanying test will not be caught by the hook (the hook cannot detect missing tests), but
a test written first and then made to pass produces the artifact the hook checks. TDD is an
intent-level rule — CI is the safety net, not the primary enforcement mechanism.

The `plan-checker` enforces the plan-creation side: delivery checklist items that ship code
without TDD-shaped steps are flagged as HIGH findings.

## Exceptions

TDD does not apply to the following:

- **Pure documentation and markdown edits**: README updates, governance rule text, `docs/` content,
  plan documents. No test target covers prose.
- **Generated or codegen output**: Files produced by `nx run [project]:codegen` or similar
  generator targets. The generator's own tests cover the output; you do not write tests for
  generated files directly.
- **Trivial typo or comment fixes**: A one-character typo correction in a comment or string
  literal does not warrant a new test. The existing suite already covers the behavior.
- **Exploratory spikes**: Throwaway code written to learn an API or validate a hypothesis. Spikes
  are deleted before merging; they never enter `main`.
- **Configuration-only changes**: Changing a value in `nx.json`, `.prettierrc`, or
  `tsconfig.base.json` where no executable behavior is being altered.

Keep the exception list short. When in doubt, write the test first.
