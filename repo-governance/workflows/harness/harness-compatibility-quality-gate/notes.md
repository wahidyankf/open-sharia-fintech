---
title: "Notes"
description: Operational notes — Phase 0 always runs, Phase 1 is on-demand, the pre-push guard is separate and deterministic, and the workflow is idempotent and bounded.
when_to_use: Use when clarifying how this workflow relates to the pre-push binding guard or when Phase 1 actually runs.
---

# Notes

- **Phase 0 always runs**: The five deterministic parity invariants run in every execution
  regardless of `scope`, before any web research begins.
- **On-demand for Phase 1**: Phase 1 (external drift) does not run automatically on every
  push — schedule it periodically or trigger it when upstream harness changes are announced.
- **Pre-push guard is separate**: `rhino-cli harness bindings validate` (the pre-push parity
  guard) checks internal byte-level consistency deterministically and runs automatically.
- **Idempotent**: Safe to run multiple times without breaking working state.
- **Observable**: Generates audit reports for every iteration in `generated-reports/`.
- **Bounded**: `max-iterations` prevents runaway execution.
