---
title: "Application Examples"
description: Walks through three worked examples (bug fix, cascading failure, scope creep) contrasting symptom fixes with root cause fixes.
category: explanation
subcategory: principles
tags:
  - principles
  - root-cause
  - minimal-impact
created: 2026-03-09
when_to_use: Use when you need a worked example of applying root cause orientation to a realistic task.
---

# Application Examples

## Example 1: Bug Fix

**Situation**: A validation function rejects valid inputs in one specific case.

**FAIL - Symptom fix**:

```
Add a special case: "if input equals X, skip validation and return true"
```

This makes the test pass but hides the fact that the validation logic is wrong.

**PASS - Root cause fix**:

```
Identify why the validation rejects input X. The regex pattern is too strict - it
does not account for a valid format variant. Fix the regex to correctly accept all
valid inputs, including X.
```

## Example 2: Cascading Failure

**Situation**: A downstream service fails when the upstream returns an unexpected shape.

**FAIL - Symptom fix**:

```
Wrap the downstream call in try/catch and return a default value on failure.
```

The upstream contract is broken; swallowing the error means no one knows.

**PASS - Root cause fix**:

```
Identify that the upstream changed its response shape without updating the contract.
Fix the contract, update both sides, add a test that would catch shape mismatches
in the future.
```

## Example 3: Scope Creep

**Situation**: Fixing a bug in a payment calculation function while noticing other functions in the file could be simplified.

**FAIL - Minimal impact violation**:

```
Fix the bug AND refactor the three other functions because "they're in the same file
and I have context."
```

**PASS - Minimal impact**:

```
Fix only the payment calculation bug. Note in the PR description that other functions
in the file could be simplified in a follow-up task.
```
