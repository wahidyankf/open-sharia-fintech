---
description: Lists the three core practices of root cause orientation - diagnosing before acting, applying minimal impact changes, and holding to senior engineer standards.
when_to_use: Use when looking for the concrete Do/Don't practices that operationalize root cause orientation.
---

# Core Practices

## 1. Diagnose Before Acting

**Do**: Understand the actual cause of the problem before writing any fix.

**Don't**: Apply the first change that makes the symptom disappear.

```
PASS: "The test fails because the function returns nil when the input map has no key.
       I'll add a guard for the missing-key case and return a proper default."

FAIL: "The test fails. I'll catch the nil pointer and return an empty string to stop the crash."
```

**Diagnosis checklist**:

- What is the exact failure mode? (error message, wrong output, crash)
- What code path produces this failure?
- What is the root cause of that path being taken?
- Is the fix I'm considering addressing the cause or masking the symptom?

## 2. Apply Minimal Impact Changes

**Do**: Change exactly what needs to change to solve the root cause.

**Don't**: Improve adjacent code, rename things you disagree with, or refactor while fixing.

```
PASS: Fix the one function that incorrectly handles the edge case.

FAIL: Fix the function AND rename variables you find unclear AND restructure the file
      because it seemed like a good opportunity.
```

**Minimal impact rules**:

- Every changed line traces directly to the problem being solved
- Unrelated code is left in its current state, even if it could be improved
- Unrelated code improvements (style, refactoring, naming) that are noticed are mentioned, not silently applied. Exception: preexisting errors and broken state are fixed at root cause per [Proactive Preexisting Error Resolution](../../../development/practice/proactive-preexisting-error-resolution.md)
- Style preferences are not applied to unchanged lines

See [Implementation Workflow - Surgical Changes](../../../development/workflow/implementation/surgical-changes-principle.md) for detailed guidance on applying minimal impact in practice.

## 3. Hold to Senior Engineer Standards

**Do**: Ask "would a senior engineer approve this?" before declaring a task complete.

**Don't**: Ship the first solution that passes the test or satisfies the literal requirement.

```
PASS: The fix handles the immediate case, all edge cases, does not break existing behaviour,
      and does not introduce unnecessary complexity.

FAIL: The fix passes the test. Moving on.
```

**Senior engineer test questions**:

- Does this solution handle edge cases, or only the specific case that triggered the bug?
- Is this the simplest correct solution, or just the fastest one to write?
- Will this solution hold up under different conditions, or will the problem resurface?
- Does this change introduce new coupling or complexity that will need to be resolved later?
