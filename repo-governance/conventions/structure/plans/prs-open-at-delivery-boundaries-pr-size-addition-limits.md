---
title: "Bounding PR Size — Addition Targets, Limits, and Plan-Document Exemption"
description: "Defines the strong code-addition target, hard PR limits, file categories, exclusions, and the narrow plan-document LOC exemption."
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - pr-review
  - organization
created: 2026-08-25
when_to_use: "Use when assessing rule 4, documenting a natural-seam exception, or deciding whether a plan-document PR is LOC-exempt."
---

# Addition Targets, Limits, and Plan-Document Exemption (PR-Size Rule 4)

Every PR is human-readable; there are no machine-only PRs. A person must review it unaided.

## Addition Targets and File Limits

Count handwritten **added** lines and hand-authored files:

- Code/program-type additions (`C`) have a **strong recommended target of 500**, not a hard ceiling.
- Other/document-type additions (`O`) must not exceed **1,000**.
- `C` and `O` are measured independently; a mixed PR has no combined ceiling.
- Deleted lines count as zero.
- The PR must not exceed **20 hand-authored files**.

Code/program-type files include source, scripts, configuration, data, and manifests, including
`.ts`, `.fs`, and `.json`. Other/document-type files include `.md`.

Apply the binding ownership registry's longest matching declaration; directory names never decide
authorship. Exclude every added line and the file count only for a wholly `generated` file. Count
wholly `source` and `vendored` files as hand-authored. For a vendored file with a delimited
generated region, exclude only added lines inside the markers; count every outside addition and
the file itself. Thus `.codex/config.toml` always enters the file count, while only its generated
region is line-exempt.

## Natural-Seam Exception to the 500 Target

A PR may exceed `C = 500` when splitting would break one natural, cohesive delivery seam or make
the resulting units less independently reviewable, verifiable, or revertible. Exceeding 500 is not
by itself a failure. The PR body must record the measured `C`, name the seam, list viable split
points considered and why each was rejected, and state how the larger diff will be reviewed and
proved. A size-only preference, convenience, or unrelated ride-along is not an exception.

This exception changes only the 500 code target. It does not waive `O = 1,000`, the 20 hand-authored
file ceiling, the 300-file machine ceiling, surface boundaries, or scope discipline.

## Narrow Plan-Document LOC Exemption

Waive the hard other/document added-line ceiling when the **entire hand-authored diff** is one of
these:

- The initial establishment of plan documents under `plans/backlog/` or `plans/in-progress/`, plus
  the required target index update.
- A pure move between `plans/backlog/` and `plans/in-progress/` in either direction, plus the
  required index updates.

For either case, qualifying artifacts are the plan's Markdown documents and indexes plus required,
non-executable assets referenced by those documents: high-fidelity binary mockups, exported
images, and editable diagram/design sources under the plan's `assets/`. Binary assets add zero
lines but remain hand-authored files. Executable source or scripts, runtime/build/tool
configuration or manifests, automated tests or fixtures, runnable prototypes, unreferenced assets,
and unrelated files revoke the exemption even when stored below the plan directory. Apply this
same taxonomy to initial establishment and pure moves.

Later plan edits, moves involving `plans/ideas/` or `plans/done/`, non-plan content, and ride-along
changes restore the other/document ceiling. The 500 code target, 20-file cap, 300-file machine
ceiling, and PR-size rules 1-3 remain in force.

[The Atomicity Exception](./prs-open-at-delivery-boundaries-pr-size-atomicity.md) is broader: it may
exceed any rule-4 bound when splitting paired rule surfaces would make `main` inconsistent.

## Enforcement

**Enforcement disposition — unenforced by decision.** No deterministic gate can decide whether a
larger code diff is one natural seam, classify every handwritten file, or decide whether a plan diff
is initial establishment or a pure move. The PR template exposes category totals, split reasoning,
and exemption claims for author and reviewer inspection.

## Related

- [Bounding PR Size](./prs-open-at-delivery-boundaries-pr-size.md) — surface splitting and all five
  PR-size rules.
- [The Atomicity Exception](./prs-open-at-delivery-boundaries-pr-size-atomicity.md) — the broader
  correctness exception.
