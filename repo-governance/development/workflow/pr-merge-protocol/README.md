---
description: "Practice governing PR merges — merge authority comes from hardened preconditions, not a per-instance prompt; `[AI]` merges by default."
when_to_use: "Read this index to find the right PR Merge Protocol child document."
---

# PR Merge Protocol

- [Principles and Conventions Implemented](./principles-and-conventions-implemented.md) — The principles and companion conventions the PR merge protocol implements and respects. Use when tracing why the PR merge protocol exists back to the principles and conventions it respects.
- [The Rule](./the-rule.md) — The five hardened preconditions that must all hold before an AI agent or automation may merge a pull request. Use immediately before merging any pull request, to confirm all five preconditions hold.
- [Quality Gates](./quality-gates.md) — Exact-head PR CI, applicable surface gates, the universal secret check, and the no-bypass rule. Use when confirming which gates a PR must pass before merge, or when a secret exposure is suspected in a PR diff.
- [When This Applies and Scope](./when-this-applies-and-scope.md) — Which delivery modes and PR types this protocol governs, which it does not, and which agents and automation it binds. Use when determining whether a given PR, phase, or delivery mode is governed by this protocol.
- [The `worktree-to-pr` Terminal Step](./the-worktree-to-pr-terminal-step.md) — The exact-head CI, surface-gate, archival, and readiness sequence after all commits are pushed. Use when a worktree-to-pr branch needs its terminal done-definition.
- [Draft PR Lifecycle](./draft-pr-lifecycle.md) — Why every PR opens as a GitHub draft, and the four-step lifecycle from draft open through the merge that follows the precondition gate. Use when opening a PR under worktree-to-pr or main-to-pr, or when deciding whether flipping a PR to ready authorizes merging it.
- [Before Merging](./before-merging.md) — The full (a)-(e) precondition checklist an agent must confirm immediately before merging, and why the list is spelled out in full rather than abbreviated. Use as the final checklist immediately before executing a PR merge.
- [Resolving Merge Conflicts in Generated Files](./resolving-merge-conflicts-in-generated-files.md) — Why a CONFLICTING state after green CI is not necessarily a PR defect, and why a generated-file conflict must be resolved at its source. Use when a PR shows a merge conflict, especially inside a generated file.
- [Precondition Summary and When Gates Fail](./precondition-summary-and-when-gates-fail.md) — The status summary an agent presents before merging, and the fix-then-re-evaluate procedure to follow when a quality gate fails. Use when writing the merge status summary, or when a quality gate has failed and the merge is on hold.
- [Examples](./examples.md) — Worked pass/fail examples of the PR merge protocol - correct precondition-gated merges, premature merges, and a user-authorized gate bypass. Use as a reference when unsure whether a specific merge decision matches or violates this protocol.
