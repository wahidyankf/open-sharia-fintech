---
title: "The Rule"
description: "The blocking rule: every fix needs a reproducing test in the same commit/PR, no exemptions."
category: explanation
subcategory: development
tags:
  - regression
  - testing
  - bug-fix
  - quality
  - gherkin
  - specs
created: 2026-06-22
when_to_use: "Use when you need the exact wording of the mandate."
---

# The Rule

**Every fix for a discovered bug or regression MUST land with a test that reproduces the defect
in the SAME commit or PR as the fix.**

The reproducing test must:

1. **Fail** on the code as it existed before the fix (or be clearly written to target the
   defect condition -- for new code paths, document the scenario explicitly in the test description).
2. **Pass** on the fixed code.
3. **Continue to pass** on every future build without manual attention.

This rule is **BLOCKING**. There are **no exemptions** -- not for trivial fixes, not for cosmetic
defects, not for "obvious" one-liners, not for hotfixes. The form of the test adapts to the
defect type (see [Test Form by Defect Type](./test-form-by-defect-type.md)), but the obligation to
write one does not.
