---
title: "Bounding PR Size — Split a Sweep by Surface"
description: Bounds how large a PR may be when it opens, including narrow LOC and atomicity exceptions.
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
   in its runtime error text. Rule 4's 20-file cap normally holds every PR far below it.
3. **Split PRs run sequentially from one reused worktree**, never one per PR — land a slice,
   fast-forward from `origin/main`, open the next. This preserves merge precondition (c): each
   slice is reviewed against a base already on `main`, not stacked on an unmerged sibling. See
   [Worktree Specification](./worktree-specification.md#worktree-specification) and
   [Worktree Cap](./worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule).

4. **Every PR here is human-readable — there are no machine-only PRs.** Apply
   [Addition Limits and Plan-Document Exemption](./prs-open-at-delivery-boundaries-pr-size-addition-limits.md):
   independently cap handwritten code/program-type additions at **500** and other/document-type
   additions at **1,000**, count deletions as zero, and cap hand-authored files at **20**. That
   child defines file categories, generated-mirror exclusions, and the only plan-document cases
   that waive the two LOC ceilings.
   **Use one PR for as much of one natural, independently stable seam as fits.** Split only at a
   real seam when its applicable limit would otherwise be exceeded.
5. **A slice must be self-consistent on `main` the moment it merges** — see
   [The Atomicity Exception](./prs-open-at-delivery-boundaries-pr-size-atomicity.md), which pairs a
   convention with the binding that executes it. That broader exception may exceed any rule-4
   bound; the linked plan-document exemption waives only the two added-line ceilings.

**Enforcement disposition — unenforced by decision.** No deterministic gate classifies every
handwritten file or decides whether a plan diff is initial establishment or a pure move. The PR
template exposes the category totals and any exemption claim for author and reviewer inspection.

**See**: [What Every PR Body Must Carry](./prs-open-at-delivery-boundaries-pr-body.md).
