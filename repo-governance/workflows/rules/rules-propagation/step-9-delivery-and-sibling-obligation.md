---
title: "Step 9: Delivery and Sibling Obligation"
description: Committing the ledger's paths, opening the PR, and recording the propagation obligation the sibling repository now carries.
when_to_use: Use once verification is clean, to ship the run and record what it leaves owed elsewhere.
---

# Step 9: Delivery and Sibling Obligation

## Commit

Stage the ledger's paths explicitly and commit restricted to them, so a formatting hook cannot
widen the commit into neighbouring work. Follow the repository's commit-message convention:
imperative mood, no trailing period, conventional type and scope.

Keep the body free of bare issue-number references — a `#`-prefixed number in a commit body parses
as a footer and trips the message gate.

## PR

Open the PR and state, for each rule: its normalized statement, its destination, its enforcement
disposition, and any supersession or eviction it caused. A reviewer who cannot see what was
displaced cannot review the displacement.

Where the run evicted an instruction-surface entry, say so in the PR body explicitly. That is the
single change in this workflow most likely to surprise a reader, because it removes something from
a file nobody edited on purpose.

## Poll, Do Not Watch

Poll the PR's checks on an interval rather than attaching to a blocking watch. Investigate a red
check at its root cause; never bypass a gate to land a rule that governs gates.

A PR reporting blocked with every check green usually carries an unresolved review thread rather
than a failing gate. Look for the thread before re-running anything.

## Sibling Obligation

One run touches one repository. Where the propagated rule is portable — governance, agent, or skill
guidance rather than something specific to this repository's contents — the run **records** an
obligation naming the sibling repository, in the PR body and as a durable note. The obligation also
records the parity objective slug, shared worktree basename, and corresponding short-lived branch
name (or mode-based `not applicable`) established at Step 1. The sibling run reuses those
names. If an identity has become unavailable, it proves an existing identity belongs to the same
delivery or selects one common alternative across both repositories before mutation.

Recorded, not executed. The sibling's propagation is its own delivery, and a rule half-applied
across two repositories is worse than a rule applied to one and known to be owed to the other.

Where the rule is genuinely local, record `sibling-obligation: none` with the reason. Silence here
is indistinguishable from an obligation that was overlooked.

Before delivery, assert that the current worktree basename and branch match the recorded identity.
This check remains one-run/one-repository and does not mutate the sibling.

## After the Merge

Where the merge advanced the integration branch without advancing the local one, fast-forward the
local branch as a terminal step. A side-tree push leaves the local integration branch silently
behind, and the next run starts from stale rules.

## Related Documents

- [Termination Criteria](./termination-criteria.md) — what counts as landed.
- [Step 8: Verification](./step-8-verification.md) — what must be clean first.
