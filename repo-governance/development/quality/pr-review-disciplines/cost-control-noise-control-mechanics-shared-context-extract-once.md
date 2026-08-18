---
title: "Cost/Noise Control: Shared-Context Extract-Once (D13)"
description: "Extracting shared PR context once, and large-diff handling."
category: explanation
subcategory: development
tags:
  - pr-review
  - governance
  - agents
  - quality-gates
  - boundary-rules
created: 2026-07-23
when_to_use: "Use when a large diff needs shared-context handling."
---

# Shared-context extract-once + large-diff handling (D13)

**D13 chose NO generated-file exclusion.** Reviewers see the **full diff**, including regenerated
output such as `.opencode/agents/**`, `.amazonq/**`, `generated/**`, lock files, and minified/source-map
assets — nothing is silently filtered out before a specialist reviews it, and **CI still runs over
everything regardless** of what any reviewer chooses to skim. This is a deliberate reversal of the
alternative (auto-detecting and excluding generated files): the rationale is explicitness — a
hand-edited "generated" file is never silently missed because nothing is silently excluded.

Two mechanics keep this full-diff posture tractable rather than merely expensive:

- **Shared context, extracted once.**
  [`pr-review-scout-maker`](../../../../.claude/agents/pr-review/pr-review-scout-maker.md) assembles the PR
  metadata, linked-plan/issue context, and the full diff **once** into a single shared-context
  brief every specialist reads, rather than each specialist separately re-deriving the same context
  (which would multiply token cost by the number of specialists) — this extraction is the scout's
  job, not `pr-review-synthesis-maker`'s.
- **Scout-discretion large-diff slicing.** For a `full`-tier PR whose diff exceeds a
  specialist's comfortable context budget, `pr-review-scout-maker` MAY have specialists review
  per-domain-relevant file slices rather than the whole diff at once, recording the slicing choice
  in the shared-context brief for `pr-review-synthesis-maker` to carry into the review header it
  posts. If a diff still cannot be reviewed in one fan-out, the scout records an explicit
  "diff exceeds single-review scope — reviewed in N slices" note in the brief rather than silently
  under-covering it.
