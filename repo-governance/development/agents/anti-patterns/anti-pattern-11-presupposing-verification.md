---
title: "Anti-Pattern 11: Verification Prompts That Presuppose Their Conclusion"
description: "Describes the anti-pattern of a verification prompt whose wording presupposes the answer it should be checking."
category: explanation
subcategory: development
tags:
  - ai-agents
  - anti-patterns
  - development
  - best-practices
created: 2025-11-23
when_to_use: Use when writing or reviewing a verification prompt that a checker or fixer agent will run.
---

# Anti-Pattern 11: Verification Prompts That Presuppose Their Conclusion

**Problem**: A verification or re-review prompt asserts the answer it wants confirmed. The reviewing
agent, having no license to disagree, manufactures consensus — it finds evidence for the stated
hypothesis and stops looking.

**Bad Example:**

```markdown
The previous fix to `plan-checker.md` introduced a regression in the merge-gate guard.
Confirm the regression and describe it.
```

**Solution**: State the hypothesis as a hypothesis, explicitly license the negative finding, and
name agreement itself as a failure mode:

```markdown
Hypothesis (may be WRONG — treat it as a lead, not a conclusion): the previous fix to
`plan-checker.md` introduced a regression in the merge-gate guard.

Investigate independently. Reporting "the hypothesis is wrong, and here is the evidence" is a
FULLY VALID and equally valuable outcome. Reflexive agreement is the failure mode being guarded
against — if the guard is sound, say so and cite why, then keep looking for defects elsewhere.
```

**Rationale:**

- A prompt that presupposes its conclusion measures compliance, not correctness.
- Explicitly licensing the negative finding is what makes an independent verification pass
  independent — observed in practice to redirect a reviewer from a false lead onto a real defect
  elsewhere in the same file.
- This applies to every re-review, self-check, and fixer re-validation prompt, not only to
  formal review cycles.
