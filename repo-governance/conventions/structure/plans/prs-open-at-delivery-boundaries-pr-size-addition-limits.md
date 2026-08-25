---
title: "Bounding PR Size — Addition Limits and Plan-Document Exemption"
description: "Defines PR addition counts, file categories, exclusions, and the narrow plan-document LOC exemption."
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - pr-review
  - organization
created: 2026-08-25
when_to_use: "Use when measuring a PR against rule 4 or deciding whether a plan-document PR is LOC-exempt."
---

# Addition Limits and Plan-Document Exemption (PR-Size Rule 4)

Every PR is human-readable; there are no machine-only PRs. A person must review it unaided.

## Addition and File Limits

Count handwritten **added** lines and hand-authored files:

- Code/program-type additions (`C`) must not exceed **500**.
- Other/document-type additions (`O`) must not exceed **1,000**.
- The two ceilings are independent; a mixed PR has no combined ceiling.
- Deleted lines count as zero.
- The PR must not exceed **20 hand-authored files**.

Code/program-type files include source, scripts, configuration, data, and manifests, including
`.ts`, `.fs`, and `.json`. Other/document-type files include `.md`.

Generated mirrors under `.agents/`, `.opencode/`, and `.codex/` enter no addition or file count.
They are byte-generated from `.claude/`, synchronization-gated, and not reviewed as independent
source.

## Narrow Plan-Document LOC Exemption

Waive only the two added-line ceilings when the **entire hand-authored diff** is one of these:

- The initial establishment of plan documents under `plans/backlog/` or `plans/in-progress/`, plus
  the required target index update.
- A pure move between `plans/backlog/` and `plans/in-progress/` in either direction, plus the
  required index updates.

Later plan edits, moves involving `plans/ideas/` or `plans/done/`, non-plan content, and ride-along
changes restore both ceilings. The 20-file cap, the 300-file machine ceiling, and PR-size rules 1-3
remain in force.

[The Atomicity Exception](./prs-open-at-delivery-boundaries-pr-size-atomicity.md) is broader: it may
exceed any rule-4 bound when splitting paired rule surfaces would make `main` inconsistent.

## Enforcement

**Enforcement disposition — unenforced by decision.** No deterministic gate classifies every
handwritten file or decides whether a plan diff is initial establishment or a pure move. The PR
template exposes category totals and any exemption claim for author and reviewer inspection.

## Related

- [Bounding PR Size](./prs-open-at-delivery-boundaries-pr-size.md) — surface splitting and all five
  PR-size rules.
- [The Atomicity Exception](./prs-open-at-delivery-boundaries-pr-size-atomicity.md) — the broader
  correctness exception.
