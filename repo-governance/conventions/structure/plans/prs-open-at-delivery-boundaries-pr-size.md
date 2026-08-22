---
title: "Bounding PR Size — Split a Sweep by Surface"
description: Bounds how large a PR may be when it opens — one PR per propagation surface, a human-scale size bound every PR meets, and sequential slices from a single reused worktree.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - pr-review
  - organization
created: 2026-08-22
when_to_use: Use when a delivery unit's diff spans many surfaces or files and needs splitting into several PRs.
---

# Bounding PR Size — Split a Sweep by Surface

[PRs Open at Delivery Boundaries](./prs-open-at-delivery-boundaries-rules.md) says **when** a PR
opens. This says **how large** it may be when it does.

Review quality degrades on very large diffs, and this repo's own posted reviews all ran against
PRs of 15,000-56,000 lines and 160-3,524 files — far past any measured size.

1. **Split a propagation sweep into one PR per surface.** Governance text, agents plus their
   generated mirrors, specs, and plans are separate surfaces; each is independently consistent, so
   each lands on its own. Surface seams — not a line count — are the primary split.
2. **A machine ceiling sits above everything: 300 changed files**, past which a hosted AI
   code-review assistant refuses outright — **observed behavior, not a published limit**, seen
   only in its runtime error text. Rule 4 holds every PR far below it, so it never binds.
3. **Split PRs run sequentially from one reused worktree**, never one worktree per PR — land a
   slice, fast-forward the worktree from `origin/main`, open the next. This preserves merge
   precondition (c): each slice is reviewed against a base already on `main`, not stacked on an
   unmerged sibling. See
   [Worktree Specification](./worktree-specification.md#worktree-specification) and
   [Worktree Cap](./worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule).

4. **Every PR here is human-readable — there are no machine-only PRs.** A person must be able to
   review any of them unaided, so the binding bound is human-scale: **≤400 changed lines AND ≤20
   changed files, counting hand-authored files only**. Generated mirrors (`.agents/`, `.opencode/`,
   `.codex/`) enter neither count — byte-generated from `.claude/`, sync-gated, read by nobody.
5. **A slice must be self-consistent on `main` the moment it merges.** Surfaces split cleanly only
   when each states a rule the others do not. Where one rule is stated on two surfaces — a
   `repo-governance/` convention and the `.claude/` binding that executes it — those two surfaces
   are **one slice**, merged together, even past rule 4's bound. A size bound never outranks
   correctness: a `main` stating one rule two contradicting ways is worse than a large PR.

**Enforcement: none.** No gate checks these rules; they bind the author, not CI. Rule 1 is the
mechanism, rule 4 the backstop.

**Where the split is safe.** Between independent surfaces — governance versus specs versus plans —
each is separately consistent and rule 3 bounds the gap to one merge. Rule 5 marks where it is
not, learned the hard way: a `.claude/`-only slice of this convention drew five reviewer findings
for contradicting the `repo-governance/` text it left behind.

**See**: [What Every PR Body Must Carry](./prs-open-at-delivery-boundaries-pr-body.md).
