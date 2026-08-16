---
title: "When to Use, and Relationship to plan-execution.md"
description: States when (and when not) to run this workflow, and that it is a discovery-and-reconciliation layer in front of plan-execution.md rather than a duplicate of it.
when_to_use: Use when deciding whether a discovery layer is needed before plan-execution.md, or when scoping what this workflow specifies versus what it inherits from plan-execution.md.
---

# When to Use, and Relationship to plan-execution.md

## When to Use

- Resuming a plan after a session boundary, a crash, or a handoff, where it is unknown whether the
  plan already has partial implementation somewhere.
- A plan is suspected to have been worked concurrently by another agent, session, or human — possibly
  in a different repo, since `ose-private` is a sibling that can carry the same plan-identifier.
- Before running `plan-execution.md` cold on a plan-identifier that might already have an open PR, an
  orphaned worktree, or a `delivery.md` copy sitting in more than one location.

## When NOT to Use

- A brand-new plan that has never been worked — discovery is a guaranteed no-op; invoke
  `plan-execution.md` directly and skip the overhead.
- A plan already confirmed executing in the current, correct worktree with a live Task list in this
  same session — there is nothing to take over; continue in place.

## Relationship to plan-execution.md (no duplication)

This workflow is a **discovery-and-reconciliation layer in front of**
[`plan-execution.md`](../plan-execution.md) — the same relationship
[`multi-plans-execution.md`](../multi-plans-execution.md) has to it as a scheduling layer. Everything
about how a plan executes once its worktree is resolved — [Step 0's freshness
gate](../plan-execution.md#0-enter-the-designated-worktree-sequential-hard-gate), the [Task-Checklist
Synchronization model](../plan-execution.md#task-checklist-synchronization), the [Atomic Sync
Ritual](../plan-execution.md#atomic-sync-ritual), [Resume Reconciliation](../plan-execution/11-resume-reconciliation.md#resume-reconciliation-disk-is-truth),
the [Iron Rules](../plan-execution/12-iron-rules-1-5.md#iron-rules-non-negotiable), the PR-review cycle, and archival —
is inherited verbatim once handoff happens (Phase E). This document specifies only what a scattered,
possibly-multi-repo, possibly-already-started plan needs before that: a wider-than-single-worktree
search (Phase A), a reconciliation decision procedure (Phase B), takeover of what's found (Phase C),
and a leftover-cleanup pass (Phase D).

**Continued in** [Why This Workflow Exists](./02-why-this-workflow-exists.md) for the two failure modes this workflow prevents.
