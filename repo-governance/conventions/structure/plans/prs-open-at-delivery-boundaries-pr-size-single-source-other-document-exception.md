---
title: "Single-Source Other/Document Natural-Seam Exception"
description: "Defines the narrow O=1,100 exception for an indivisible, existing canonical source."
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - pr-review
  - organization
created: 2026-08-31
when_to_use: "Use when one existing other/document source alone exceeds the default O=1,000 limit."
---

# Single-Source Other/Document Natural-Seam Exception

`O = 1,000` is the hard default. One named delivery binding may instead reach `O = 1,100` only when
one existing, non-generated other/document source alone exceeds 1,000 lines and must become exactly
one canonical, non-generated behavior or contract target. The delivery contains only that
source-to-target semantic change and required delivery-state artifacts; no neighbouring behavior,
contract, or convenience change may ride along.

Before implementation, the plan record and prospective size gate state the current source line count,
exact source and target, finite allocation, semantic/build-validity constraint, every rejected viable
split, review/proof approach, recovery, and matching PR declaration. Final delivery remeasures the
whole diff and rejects `O > 1,100`, a source at or below 1,000, a missing record or allocation, an
additional semantic change, or a stale/mismatched PR declaration. The PR body repeats the measurement,
seam, rejected splits, proof, and recovery.

This exception does not waive the 300-file ceiling, default file budget, surface/scope rules,
verification, or recovery. A smaller canonical target, a generated source, a convenience grouping, or
a split rejected only to reduce PR count or effort is not eligible.

## Enforcement

**Enforcement disposition — unenforced by decision.** A gate can measure source and `O` counts and
require the record, but cannot determine semantic indivisibility. Authors and reviewers inspect it.

## Related

- [Addition Limits, File-Budget Exception, and Plan-Document Exemption](./prs-open-at-delivery-boundaries-pr-size-addition-limits.md)
  — parent Rule-4 convention and the default limit.
