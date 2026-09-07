---
description: Why weakening a failing gate is forbidden, what corner-cutting looks like, and the additive-and-own-worktree habits that prevent most destructive operations from ever arising.
when_to_use: Use when a gate, test, lint, or CI job fails and there is pressure to make it pass quickly, or when choosing between a destructive and an additive git operation.
---

# No Corner-Cutting and Preferring Additive Operations

## No Corner-Cutting — Root-Cause Orientation Is Binding

Under parallel execution the cheapest way to make a gate go green is to weaken the gate. When a gate,
test, lint, type-check, or CI job fails, **fix the cause, never the signal**.

Forbidden without explicit per-instance approval **and** a written reason recorded in the plan. As
with the Forbidden Operations table above, **this list is illustrative, not exhaustive** — _any_
action whose effect is to make a failing signal pass without addressing what it was reporting is
covered, whether or not its form appears here:

- bypassing hooks (`--no-verify`) or skipping a declared quality gate
- deleting, skipping, `.only`-narrowing, or loosening a failing test instead of fixing the code
- weakening an acceptance criterion, threshold, or lint rule so a failing check passes
- ticking a delivery checkbox without the evidence its acceptance criterion demands
- suppressing an error — a broad catch, an ignore-comment, a silenced warning — in place of a fix
- deferring a discovered preexisting failure instead of fixing it in-scope

A blocker that genuinely cannot be root-caused within scope is **escalated and recorded** — named in
the plan, with what was tried and why it is out of scope — never silently worked around. Escalating is
a legitimate outcome; quietly routing around is not.

The distinction that matters: each item above makes the _report_ green without making the _system_
correct. A suppressed error still fires in production; a narrowed test still leaves the untested path
broken; an unticked-but-ticked checkbox transfers a false completion signal to whoever reads the plan
next. On a shared machine that false signal is what another actor builds on.

## Prefer Additive, Own-Worktree Operations

Two habits prevent most of the above from ever arising:

- **Additive over destructive.** A new commit that reverses a change is recoverable; a rewrite that
  erases it is not. When both reach the same end state, take the one that leaves a trail.
- **Your own worktree only.** Operate within the worktree this unit of work created. Acting on a
  worktree you did not create requires positive evidence it is idle — not the absence of evidence
  that it is busy.

Before a long unattended run, `git worktree lock --reason=<why>` makes the intent legible to whoever
looks next. Before any bulk delete, `-n` / `--dry-run` costs nothing.
