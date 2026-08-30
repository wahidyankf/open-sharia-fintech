---
title: "Examples"
description: "PASS examples of knowledge capture."
category: explanation
subcategory: development
tags:
  - knowledge-capture
  - learnings
  - plans
  - triage
  - safety-gates
  - post-mortems
created: 2026-07-05
when_to_use: "Use for a correct knowledge-capture example."
---

# Examples

## PASS: Learning routed inline (non-code, small)

```markdown
## Learning: worktree-setup doc omitted a step

- **Context**: Provisioning the worktree for this plan required an undocumented
  `npm run doctor -- --fix` re-run after a stale toolchain cache.
- **Observation**: `repo-governance/development/workflow/worktree-setup.md` did not mention this
  re-run step.
- **Why it might generalize**: the next plan author will hit the same stale-cache surprise.

**Routing**: `repo-governance/development/workflow/worktree-setup.md` (non-code, small) — routed
INLINE, landed in commit `abc1234` of this plan.
```

## PASS: Learning filed as a two-pager (code, mandatory)

```markdown
## Learning: rhino-cli doctor command silently swallows a missing-tool exit code

- **Context**: Noticed while running `npm run doctor -- --fix` during Phase 0.
- **Observation**: a missing tool that fails to install still reports "0 warnings" in the summary
  line.
- **Why it might generalize**: a future contributor could believe their toolchain is healthy when
  it is not — the system would not catch this without a code fix.

**Routing**: `apps/rhino-cli` (code) — ALWAYS filed as a two-pager, never straight to
`plans/backlog/`. Filed at `plans/ideas/q2-not-urgent-important/fix-doctor-silent-tool-failure.md`.
NOT landed inline in this plan's PR.
```

## PASS: Learning discarded (fails the litmus)

```markdown
## Learning: the executor personally found Nx's cache output confusing at first

- **Context**: Ran `nx affected` for the first time in this session.
- **Observation**: took a moment to parse the cache-hit summary.
- **Litmus**: no durable surface would change behavior by routing this — it is a one-time
  orientation moment, not a gap in documentation (the docs already explain cache output).

**Routing**: discard — not generalizable; existing docs already cover this, no gap found.
```

## PASS: Explicit "none" escape

```markdown
No generalizable learnings — this plan renamed one file and updated its three inbound links; no
new pattern, rule, or gap surfaced during execution.
```
