---
description: "Defines live-head equality gates and durable loop-state hydration after interruption."
when_to_use: "Use before starting or resuming a review cycle, and at every boundary where stale-head output could be posted, fixed, or credited."
---

# Cycle Authority and Restart Recovery

## Rehydrate Before Choosing a Cycle

The pull request is the durable review record. On first entry and after interruption, read its
`ose-pr-review:v1` reviews, `ose-pr-review-disposition:v3` replies (plus legacy v2),
`ose-pr-review-cycle-credit:v2` events (plus legacy negative v1), thread state, route record, and
current checks. Reconstruct:

- the last used cycle ordinal and configured ceiling;
- the complete probe-class register;
- every finding, disposition, cause, and unresolved state;
- cycle-credit eligibility and the consecutive-clean-cycle streak; and
- every convergence checkpoint and its verdict.

Admit every review, disposition, extension, credit, non-convergence, and sibling-handoff object through
[Cycle Record Authentication](./cycle-record-authentication.md) first. Unauthenticated marker text
is ignored as state and during duplicate/conflict checks. Derive the next ordinal and ceiling only
from admitted records; never initialize an existing PR as cycle 1 or `prior = []`. Stop when
authenticated history is missing, malformed, duplicated, contradictory, or cannot balance.
Conversation memory and local files never override the PR.

## Live Head Is the Cycle Authority

The scout's pinned `head_sha` is immutable for one cycle. Query the live PR `headRefOid` and require
exact equality at three boundaries:

1. immediately before the synthesis coordinator posts the consolidated review;
2. immediately before the fixer triages or mutates the branch; and
3. after CI completes, immediately before clean-cycle or done credit. CI must belong to the exact
   live head: the fixer's verified pushed head when it changed the branch, otherwise the scout pin.
   A cycle can be clean only when that expected head still equals the scout pin.

A mismatch discards stale output and starts a fresh scout; recording a new SHA on old results is
forbidden. Before posting, discard output without a review or ordinal. After posting, the fixer
makes no code change and closes any obsolete threads with disposition v3
`effect: stale-cycle-only`; the orchestrator posts the independent
[cycle non-credit event](./cycle-non-credit-record.md), even when the review has zero threads.
After CI, the orchestrator posts the same `ineligible` event at the `post-ci` boundary and restarts. For
current-head suppression, every disposition from that now-ineligible cycle is treated as
`stale-cycle-only`, regardless of its recorded effect; the record remains immutable, but every
affected claim returns to the fresh scout. Each event withholds clean/done credit, breaks the clean
streak, and still consumes the posted ordinal and ceiling. `stale-cycle-only` preserves every
underlying claim for fresh-head evaluation.

These checks do not replace CI. They prove that routing, security review, fixes, and clean credit
all refer to the same commit that the specialists actually reviewed.

When all post-CI clean conditions hold, emit and read back the authenticated positive v2 event
defined in [Cycle Credit Record](./cycle-non-credit-record.md) before continuing or returning done.
Hydration derives clean streaks only from those positive events; absence of findings is not credit.
