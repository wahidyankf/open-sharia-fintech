---
title: "Bounding PR Size — Addition Limits, File-Budget Exception, and Plan-Document Exemption"
description: "Defines the code target, hard PR limits, default file budget, exception, categories, exclusions, and plan-document LOC exemption."
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - pr-review
  - organization
created: 2026-08-25
when_to_use: "Use when assessing rule 4, an exception, or plan-document LOC exemption."
---

# Addition Limits, File-Budget Exception, and Plan-Document Exemption (PR-Size Rule 4)

Every PR is human-readable; there are no machine-only PRs. A person must review it unaided.

## Addition Targets and File Limits

Count handwritten **added** lines and hand-authored files:

- Code/program-type additions (`C`) have a **strong recommended target of 500**, not a hard ceiling.
- Other/document-type additions (`O`) must not exceed **1,000**.
- `C` and `O` are measured independently; a mixed PR has no combined ceiling.
- Deleted lines count as zero.
- A PR should contain no more than **20 hand-authored files**. This is the default review budget;
  the narrow [File-Budget Natural-Seam Exception](#file-budget-natural-seam-exception) may apply.

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

This exception changes only the 500 code target. It does not waive `O = 1,000`, the default
hand-authored-file budget, the 300-file machine ceiling, surface boundaries, or scope discipline.

## File-Budget Natural-Seam Exception

A named delivery binding may exceed the default 20-file budget only when its exact, finite allocation
has no smaller real boundary that remains build-valid, independently reviewable, verifiable, and
revertible. It is never plan-wide and excludes inventory/dynamic discovery, convenience, and unrelated
ride-along work.

Before implementation, the plan record and prospective size gate state: binding; `C`/`O`/hand-authored/
total counts; exact allocation; cohesive seam/build constraint; every rejected viable split; review/proof;
recovery; and matching PR declaration. Final delivery remeasures the whole diff and rejects a missing,
stale, incomplete, or mismatched record. The PR body repeats counts, seam, splits, proof, and recovery.

The exception never waives `O = 1,000`, the 300-file ceiling, surface/scope rules, verification, or
recovery. It is invalid if a smaller build-valid seam exists, allocation is not finite before editing,
or a split is rejected only to reduce PR count or effort.

## Narrow Plan-Document LOC Exemption

Waive the hard other/document added-line ceiling when the **entire hand-authored diff** is one of
these:

- The initial establishment of plan documents under `plans/backlog/` or `plans/in-progress/`, plus
  the required target index update.
- A pure move between `plans/backlog/` and `plans/in-progress/` in either direction, plus the
  required index updates.

Qualifying artifacts are plan Markdown/indexes and referenced non-executable `assets/`; binary assets
add no lines but count as files. Code, scripts, runtime config/manifests, tests/fixtures, prototypes,
unreferenced assets, and unrelated files revoke the exemption. Apply this taxonomy to both cases.

Later edits, moves involving `plans/ideas/` or `plans/done/`, non-plan content, and ride-alongs restore
the other/document ceiling. The code target, default file budget, 300-file ceiling, and rules 1-3 remain.

[The Atomicity Exception](./prs-open-at-delivery-boundaries-pr-size-atomicity.md) is broader: it may
exceed any rule-4 bound when splitting paired rule surfaces would make `main` inconsistent.

## Enforcement

**Enforcement disposition — unenforced by decision.** A gate can prove counts, allocation, and required
fields, but cannot decide whether a split preserves a natural seam. The PR template exposes the claim
for author and reviewer inspection.

## Related

- [Bounding PR Size](./prs-open-at-delivery-boundaries-pr-size.md) — surface splitting and all five
  PR-size rules.
- [The Atomicity Exception](./prs-open-at-delivery-boundaries-pr-size-atomicity.md) — the broader
  correctness exception.
