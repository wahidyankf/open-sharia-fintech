---
description: "Summary notes: three-dimensional and parallel validation, sequential fixing order, mode-based flexibility, idempotency, and the link-fix limitation."
when_to_use: "Use for a quick-reference summary of the workflow's key operating characteristics."
---

# Notes

- **Three-dimensional validation**: Ensures comprehensive documentation quality
- **Parallel validation**: Efficient checking across all dimensions (up to max-concurrency)
- **Sequential fixing**: Manages dependencies between fixers (factual → tutorial)
- **Mode-based flexibility**: Progressive quality improvement (lax → normal → strict → ocd)
- **Idempotent**: Safe to run multiple times without side effects
- **Observable**: Generates detailed audit reports for each validation dimension
- **Bounded**: Max-iterations prevents runaway execution
- **Link limitation**: Broken links require manual intervention (no auto-fix available)

**Concurrency**: Currently validates in parallel (up to max-concurrency) and fixes sequentially. The `max-concurrency` parameter controls parallel checker execution.

**Best Practice**: Run link-checker separately first (`docs-link-checker` agent) to fix broken links before running full quality gate. This prevents workflow from blocking on unfixable link issues.

This workflow ensures comprehensive documentation quality through multi-dimensional validation, iterative fixing, and mode-based progressive improvement.
