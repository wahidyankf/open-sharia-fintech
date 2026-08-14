---
title: "Enforcement"
description: "Which agents enforce this mandate and at what severity."
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
when_to_use: "Use when you need to know which agent flags a missing test."
---

# Enforcement

This mandate is enforced by the same infrastructure that enforces the specs+Gherkin two-path rule:

- **`swe-code-checker`**: Flags a code fix (a diff that removes a defect condition) that lands
  without a companion test asserting the corrected behavior. Finding severity: **HIGH**.
- **`plan-maker`**: Emits a regression-test delivery step in every bug-fix plan. The step names
  the test file path, the scenario description, and the `Given/When/Then` trigger that would have
  reproduced the bug.
- **`plan-checker`**: Flags a bug-fix plan that lacks a regression-test delivery step. Finding
  severity: **HIGH**.

Neither the agent definitions nor their prompts are edited here -- this document records that
those agents are the enforcers and what they must flag.
