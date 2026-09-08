---
description: "Relates the optional cycle to its single-pass primitive and independent PR CI gate."
when_to_use: "Use when composing or evaluating explicitly requested iterative PR review."
---

# Related Workflows and Success Metrics

## Related Workflows

- [`pr-review`](../pr-review.md) — one deterministic semantic pass; the cycle's review primitive.
- [`pr-quality-gate.yml`](../../../../.github/workflows/pr-quality-gate.yml) — independent automated
  integration gate whose exact-head evidence the cycle consumes without duplicating checks.
- [`plan-execution`](../../plan/plan-execution.md) — may mention this cycle only when carrying an
  explicit user request; it never adds the cycle by default.

## Optional-Cycle Metrics

- Passes to the configured clean-streak exit.
- Percentage of explicitly requested cycles that reach their ceiling.
- Original, class-escape, and fix-induced findings by pass.
- Stale and failed pass results.

These metrics evaluate the optional cycle. They do not become repository merge requirements.
