---
title: "PR-Review Quality Gate — Cycle Authority and Restart Recovery"
description: "Defines live-head equality gates and durable loop-state hydration after interruption."
when_to_use: "Use before starting or resuming a review cycle, and at every boundary where stale-head output could be posted, fixed, or credited."
---

# Cycle Authority and Restart Recovery

## Rehydrate Before Choosing a Cycle

The pull request is the durable review record. On first entry and after interruption, read its
`ose-pr-review:v1` reviews, `ose-pr-review-disposition:v2` thread replies, thread-resolution state,
route record, and current checks before choosing the next cycle. Reconstruct:

- the last used cycle ordinal and configured ceiling;
- the complete probe-class register;
- every finding, disposition, cause, and unresolved state;
- the consecutive-clean-cycle streak; and
- every convergence checkpoint and its verdict.

Derive the next ordinal and remaining ceiling from that state; never initialize an existing PR as
cycle 1 or `prior = []`. Stop for explicit reconciliation if records are missing where a review
exists, malformed, duplicated, contradictory, or cannot balance. Conversation memory and local
files may help locate records but never override the PR.

## Live Head Is the Cycle Authority

The scout's pinned `head_sha` is immutable for one cycle. Query the live PR `headRefOid` and require
exact equality at three boundaries:

1. immediately before the synthesis coordinator posts the consolidated review;
2. immediately before the fixer triages or mutates the branch; and
3. after CI completes, immediately before clean-cycle or done credit. CI must belong to the exact
   live head: the fixer's verified pushed head when it changed the branch, otherwise the scout pin.
   A cycle can be clean only when that expected head still equals the scout pin.

A mismatch discards the stale cycle output and starts a fresh scout from the new head; recording a
new SHA on old results is forbidden. Before posting, discard raw/consolidated output without a
review. After posting, the fixer performs no code change: it replies that the evidence is stale,
resolves those stale-evidence threads as reasoned rejections, and the orchestrator records the
cycle as non-crediting before restart. After CI, withhold clean/done credit and restart. A posted
cycle still consumes its ordinal and ceiling; an aborted pre-post attempt does not create or reuse
finding IDs because none reached the durable record.

These checks do not replace CI. They prove that routing, security review, fixes, and clean credit
all refer to the same commit that the specialists actually reviewed.
