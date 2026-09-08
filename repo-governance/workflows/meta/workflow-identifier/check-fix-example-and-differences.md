---
description: Points to the canonical *-check-fix implementation and tabulates how it differs from a basic single-pass validation workflow.
when_to_use: Use when comparing a proposed workflow against the *-check-fix pattern, or when looking for a canonical example to copy.
---

# \*-check-fix Workflow Pattern — Example Implementation and Key Differences

## Example Implementation

See [Documentation Quality Gate](../../docs/docs-quality-gate.md) for a canonical implementation.
`rules-quality-gate` is no longer an example of this pattern — it is a
[governance gate](./governance-gate-class.md).

## Key Differences from Basic Validation Workflow

| Aspect             | Basic Validation Workflow        | \*-check-fix Workflow Pattern              |
| ------------------ | -------------------------------- | ------------------------------------------ |
| **Goal**           | Identify issues                  | Achieve zero findings                      |
| **Iteration**      | Single pass                      | Iterative until zero or max-limit          |
| **Findings Scope** | May focus on HIGH/MEDIUM only    | ALL findings (CRITICAL, HIGH, MEDIUM, LOW) |
| **Termination**    | After single check               | Zero findings or max-iterations            |
| **Quality Target** | Good enough (major issues fixed) | Perfect state (all issues fixed)           |
| **Human Approval** | May require checkpoints          | Fully automated                            |
| **Safety Limit**   | Not required                     | REQUIRED (max-iterations)                  |
