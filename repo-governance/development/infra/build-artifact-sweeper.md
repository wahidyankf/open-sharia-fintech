---
title: "Build-Artifact Sweeper Convention"
description: An ambient scheduled sweeper deletes gitignored build output and caches on the host machine at any time — a missing artifact is expected environmental behaviour to regenerate and continue from, never an incident to investigate
category: explanation
subcategory: development
tags:
  - build-artifacts
  - environment
  - ai-agents
  - infrastructure
  - cleanup
created: 2026-08-05
---

# Build-Artifact Sweeper Convention

A scheduled sweeper runs on the host machine carrying these repositories. It deletes gitignored,
regenerable build output and caches on its own schedule — at any time, without coordination with any
agent, plan, session, or build in flight.

**A missing build artifact is expected. Regenerate it and continue.** It is not a defect, not another
actor's misconduct, and not something to report as a failure.

## Principles Implemented/Respected

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: The
  correct response to a vanished artifact is one cheap, reversible action — rebuild — not an
  investigation. Knowing the environment's behaviour in advance is what makes that judgement
  available at the moment of surprise.

- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: The sweeper **is**
  the root cause of a missing-artifact failure. Naming it here prevents the far more expensive
  failure mode: an agent tracing a phantom defect through code that was never wrong.

- **[Reproducibility First](../../principles/software-engineering/reproducibility.md)**: Everything
  the sweeper removes is reproducible from committed sources by a documented command. That is
  precisely why it is safe to remove, and why regeneration is a complete fix.

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: One
  environmental fact with a fixed response, rather than per-agent heuristics for distinguishing
  "suspiciously missing" from "legitimately missing".

## Conventions Implemented/Respected

- **[No Machine-Specific Information in Commits](../quality/no-machine-specific-commits.md)**: This
  convention deliberately records **no** scheduler label, script path, username, or cadence. Those
  are host-specific details that would both violate that rule and drift out of date. Agents depend on
  the sweeper's _behaviour_, never on its mechanism.

- **[Temporary Files Convention](./temporary-files.md)**: Draws the boundary between what the sweeper
  removes (regenerable build output) and the agent-owned temporary directories it does not.

- **[Worktree and Artifact Cleanup Convention](../workflow/worktree-and-artifact-cleanup.md)**: The
  plan-end gate governing what **agents** delete. This convention governs what the **environment**
  deletes. See [Reconciliation](#reconciliation-with-neighbouring-rules) — the two do not conflict.

- **[Worktree Toolchain Initialization](../workflow/worktree-setup.md)**: The provisioning commands a
  swept worktree is restored with.

## What the Sweeper May Remove

Three classes, all gitignored and all regenerable:

1. **Build output** — `target/`, `dist/`, `.next/`, `out/`, `coverage/`, and equivalents in any
   worktree or the primary checkout.
2. **Tool caches** — `.nx/cache`, `node_modules/.cache`, and equivalents.
3. **The shared cargo `target/`** — the symlinked shared Rust build directory used across worktrees.
   It is swept like any other cache, notwithstanding the agent-facing rule that no agent may delete
   it.

## What the Sweeper Never Touches

This boundary is what makes the response protocol safe. The sweeper does not remove:

- tracked files, or uncommitted edits to tracked files
- `.env*` files
- `generated-reports/` and `local-temp/`
- worktree directories themselves, or any git ref or the object store

**Anything missing outside the three removable classes is not the sweeper.** Investigate it normally —
and never assume a sweep explains lost work.

## Agent Response Protocol

When a build, test, lint, or tooling command fails because an artifact is absent:

1. **Do not** file a finding, open a plan, raise a CI blocker, or report a failure to the user.
2. **Regenerate, then retry the failed step.** `nx build <project>` for build output, `npm install`
   for dependencies, `npm run doctor -- --fix` for a swept toolchain. A first `cargo`-backed command
   after a sweep rebuilds from cold — slow is not broken.
3. **If regeneration itself fails with a filesystem error inside the artifact directory** — for
   example `No such file or directory` writing a compiled object mid-build, `couldn't create a temp
dir`, or `failed to write bytecode` — the sweep is still in progress, not finished. Retrying
   immediately re-races the same window and reliably fails again. Back off with increasing cooldowns
   before the next regeneration attempt: **3 → 5 → 8 → 12 → 17 minutes.** This is a distinct case from
   step 2's plain "artifact absent, rebuild instantly" outcome — only a build that fails _while
   running_, not one that simply starts cold, warrants the cooldown.
4. **Escalate only if** the failure still reproduces after the fifth (17-minute) attempt, or something
   outside the three removable classes is missing. Either is a real problem and this convention does
   not cover it.
5. A failure that **reproduces after a clean regeneration** is a genuine defect. Treat it normally.

## Anti-Patterns

- **Committing build output** to survive the sweeper. Build output is gitignored by design; committing
  it trades a two-minute rebuild for permanent repository weight.
- **Editing `.gitignore`** to "protect" artifacts. The sweeper's scope is gitignored regenerable
  paths; un-ignoring them corrupts the repository instead of preserving anything.
- **Filing a bug, finding, or plan** against a missing artifact.
- **Blaming a concurrent agent** for a deletion the environment performed.
- **Disabling, rescheduling, or working around the sweeper.** It exists because the disk is shared;
  circumventing it moves the cost onto everyone else.
- **Tight-looping regeneration attempts against an active sweep.** A build that fails mid-run with a
  filesystem error, not merely a cold-start rebuild, means the sweep has not finished; retrying without
  the step-3 cooldown just re-races the same window repeatedly.
- **Reaching for a destructive git recovery** — `reset --hard`, `clean -fdx`, force-removing a
  worktree — after a sweep. Nothing tracked was lost, so there is nothing to recover, and those
  operations are forbidden regardless.

## Reconciliation with Neighbouring Rules

- **[Worktree and Artifact Cleanup](../workflow/worktree-and-artifact-cleanup.md)** forbids any agent
  from deleting a shared cache, the shared cargo `target/` especially. That duty is **unchanged**: it
  binds agents, and the sweeper is not an agent. An artifact an agent may not delete can still
  disappear, and its disappearance is not evidence that some agent broke the rule.

- **[CI Blocker Resolution](../quality/ci-blocker-resolution.md)** requires investigating root causes
  and never bypassing a failure. Regeneration honours it rather than evading it — the sweeper is the
  identified cause, and rebuilding is the fix, not a workaround. Only a failure that survives a clean
  rebuild is a blocker under that convention.

- **[Proactive Preexisting Error Resolution](../practice/proactive-preexisting-error-resolution.md)**
  requires fixing preexisting errors met during work. A missing-artifact error is not one: there is no
  defect to fix, and no code change is warranted.

- **[File-Touch Discipline](../practice/file-touch-discipline.md)**: swept paths are gitignored, so
  they never appear in `git status` and never belong on a touched-file ledger. A sweep therefore
  changes nothing an agent is accountable for.

## Related Documentation

- [Temporary Files Convention](./temporary-files.md) — the agent-owned temporary directories
  (`generated-reports/`, `local-temp/`) that sit outside the sweeper's scope
- [Worktree and Artifact Cleanup Convention](../workflow/worktree-and-artifact-cleanup.md) — the
  agent-side deletion gate this convention reconciles with
- [Worktree Toolchain Initialization](../workflow/worktree-setup.md) — the provisioning commands used
  to restore a swept worktree
- [CI Blocker Resolution](../quality/ci-blocker-resolution.md) — how a genuine blocker is handled once
  regeneration has ruled the sweeper out
- [No Machine-Specific Information in Commits](../quality/no-machine-specific-commits.md) — why this
  convention describes behaviour rather than mechanism
- [Nx Target Standards](./nx-targets.md) — the build targets that regenerate swept output
