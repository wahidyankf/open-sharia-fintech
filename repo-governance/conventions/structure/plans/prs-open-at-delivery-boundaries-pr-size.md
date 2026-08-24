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
opens. This says **how large** it may be. Review quality degrades on very large diffs, and this
repo's own posted reviews all ran against PRs of 15,000-56,000 lines and 160-3,524 files.

1. **Split a propagation sweep into one PR per surface**, except where rule 5 pairs two of them.
   Governance text, agents plus their generated mirrors, specs, and plans are separate surfaces;
   each independently consistent, so each lands on its own. **Governance text is every normative
   prose surface**, not only `repo-governance/**`: `AGENTS.md`, `CLAUDE.md` and their harness
   shims, and the issue/PR templates prompting for what a convention requires all count as the
   same surface, because a rule stated in one and not the others is the contradiction rule 5
   exists to prevent. Surface seams — not a line count — are
   the primary split.
2. **A machine ceiling sits above everything: 300 changed files**, past which a hosted AI
   code-review assistant refuses outright — **observed behavior, not a published limit**, seen only
   in its runtime error text. Rule 4 holds every PR far below it, so it never binds.
3. **Split PRs run sequentially from one reused worktree**, never one per PR — land a slice,
   fast-forward from `origin/main`, open the next. This preserves merge precondition (c): each
   slice is reviewed against a base already on `main`, not stacked on an unmerged sibling. See
   [Worktree Specification](./worktree-specification.md#worktree-specification) and
   [Worktree Cap](./worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule).

4. **Every PR here is human-readable — there are no machine-only PRs.** A person must review it
   unaided. Count handwritten lines and files: program/script lines (`P`) are at most **400**; if
   program/script and non-program lines (`N`) mix, `P + N ≤ 900` (`N ≤ 900 − P`); every PR has an
   absolute **1,000-line** ceiling; and there are at most **20 hand-authored files**. A
   documentation-only PR may reach 1,000 lines; a 100-program-line mixed PR permits 800 non-program
   lines.
   Generated mirrors (`.agents/`, `.opencode/`, `.codex/`) enter neither count — byte-generated from
   `.claude/`, sync-gated, read by nobody.
   **Use one PR for as much of one natural, independently stable seam as fits.** Split only at a
   real seam when its applicable limit would otherwise be exceeded.
5. **A slice must be self-consistent on `main` the moment it merges** — see
   [The Atomicity Exception](./prs-open-at-delivery-boundaries-pr-size-atomicity.md), which pairs a
   convention with the binding that executes it and is the one exception to rule 4.

**Enforcement: none.** No gate checks these rules; they bind the author, not CI.

**See**: [What Every PR Body Must Carry](./prs-open-at-delivery-boundaries-pr-body.md).
