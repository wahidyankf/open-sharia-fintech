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
   in its runtime error text. Rule 4's default 20-file budget normally holds every PR far below it.
3. **Split PRs run sequentially from one reused worktree**, never one per PR — land a slice,
   fast-forward from `origin/main`, open the next. This preserves merge precondition (c): each
   slice is reviewed against a base already on `main`, not stacked on an unmerged sibling. See
   [Worktree Specification](./worktree-specification.md#worktree-specification) and
   [Worktree Cap](./worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule).

4. **Every PR here is human-readable — there are no machine-only PRs.** Apply
   [Addition Targets, Limits, and Plan-Document Exemption](./prs-open-at-delivery-boundaries-pr-size-addition-limits.md).
   Treat **500** handwritten code/program-type additions as a strong reviewability recommendation,
   not a hard ceiling. A larger code diff is valid when it remains one natural, cohesive,
   independently reviewable, verifiable, and revertible seam; declare its measured size, seam,
   rejected split alternatives, and review proof. The independent **1,000** other/document-type
   ceiling remains hard except for the child rule's bounded single-source other/document exception;
   the **300** changed-file machine ceiling remains hard. **20** hand-authored files is the
   default review budget; a named delivery may exceed it only through the child rule's exact,
   plan-and-PR-disclosed file-budget natural-seam exception. Deletions count as zero. The child
   defines file categories, generated-mirror exclusions, both natural-seam records, and the narrow
   plan-document exemption.
   **Use one PR for as much of one natural, independently stable seam as belongs together.** Split
   at a real seam, never solely to make the code counter read 500 or less.
5. **A slice must be self-consistent on `main` the moment it merges** — see
   [The Atomicity Exception](./prs-open-at-delivery-boundaries-pr-size-atomicity.md), which pairs a
   convention with the binding that executes it. That broader exception may exceed a remaining
   hard rule-4 bound; the linked plan-document exemption waives only its applicable hard LOC
   ceiling.

**Enforcement disposition — unenforced by decision.** A deterministic gate can measure the diff and
validate an exception record, but cannot decide whether a proposed split preserves a natural seam.
The PR template exposes category totals, split reasoning, and exception claims for author and
reviewer inspection.

**See**: [What Every PR Body Must Carry](./prs-open-at-delivery-boundaries-pr-body.md).
