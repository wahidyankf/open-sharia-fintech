---
title: "Notes"
description: Operational notes — fully automated with no human checkpoints, idempotency caveats, conservative fixing, observability, and the "agents" terminology clarification.
when_to_use: Use when clarifying this workflow's automation posture or reproducibility guarantees.
---

# Notes

- **Fully automated**: No human checkpoints, runs to completion
- **Idempotent**: Safe to run multiple times, won't break working state. Byte-deterministic output across runs only when `RHINO_AUDIT_NOW=<RFC3339>` is pinned; without the pin, `ran_at` in the preflight JSON varies per run (logical findings are still identical).
- **Conservative**: Fixer skips uncertain changes (preserves correctness)
- **Observable**: Generates audit reports for every iteration
- **Bounded**: Max-iterations prevents runaway execution

**Concurrency**: The preflight (Step 0.5) is a single binary invocation and is intrinsically parallel-safe — multiple consumers can run preflight against the same repo state without contention. Validation and fixing (Steps 1-5) are sequential. The `max-concurrency` parameter is reserved for future enhancements where multiple AI-checker validation dimensions could run concurrently against a shared preflight JSON.

**Note**: "agents" in this context refers to agent SOURCE definitions in the primary binding directory (e.g., `.claude/agents/`) — secondary directories (e.g., `.opencode/agents/`) are auto-generated.

This workflow ensures repository consistency through iterative validation and fixing, making it ideal for maintenance and quality assurance.
