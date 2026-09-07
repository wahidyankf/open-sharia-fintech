---
description: Reconciles the sweeper with neighbouring conventions on worktree cleanup, CI blockers, and file-touch discipline, and links to the related documentation
when_to_use: Use when a rule in another convention seems to conflict with the sweeper's behaviour, or when you need pointers to the documents this convention builds on.
---

# Reconciliation and Related Documentation

## Reconciliation with Neighbouring Rules

- **[Worktree and Artifact Cleanup](../../workflow/worktree-and-artifact-cleanup.md)** forbids any agent
  from deleting a shared cache, the shared cargo `target/` especially. That duty is **unchanged**: it
  binds agents, and the sweeper is not an agent. An artifact an agent may not delete can still
  disappear, and its disappearance is not evidence that some agent broke the rule.

- **[CI Blocker Resolution](../../quality/ci-blocker-resolution.md)** requires investigating root causes
  and never bypassing a failure. Regeneration honours it rather than evading it — the sweeper is the
  identified cause, and rebuilding is the fix, not a workaround. Only a failure that survives a clean
  rebuild is a blocker under that convention.

- **[Proactive Preexisting Error Resolution](../../practice/proactive-preexisting-error-resolution.md)**
  requires fixing preexisting errors met during work. A missing-artifact error is not one: there is no
  defect to fix, and no code change is warranted.

- **[File-Touch Discipline](../../practice/file-touch-discipline.md)**: swept paths are gitignored, so
  they never appear in `git status` and never belong on a touched-file ledger. A sweep therefore
  changes nothing an agent is accountable for.

## Related Documentation

- [Temporary Files Convention](../temporary-files.md) — the agent-owned temporary directories
  (`generated-reports/`, `local-tmp/`) that sit outside the sweeper's scope
- [Worktree and Artifact Cleanup Convention](../../workflow/worktree-and-artifact-cleanup.md) — the
  agent-side deletion gate this convention reconciles with
- [Worktree Toolchain Initialization](../../workflow/worktree-setup.md) — the provisioning commands used
  to restore a swept worktree
- [CI Blocker Resolution](../../quality/ci-blocker-resolution.md) — how a genuine blocker is handled once
  regeneration has ruled the sweeper out
- [No Machine-Specific Information in Commits](../../quality/no-machine-specific-commits.md) — why this
  convention describes behaviour rather than mechanism
- [Nx Target Standards](../nx-targets.md) — the build targets that regenerate swept output
