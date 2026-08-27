---
title: "Phase A — Discover Every Trace of This Plan: Plan-Identifier and Repo Set"
description: Covers Phase A steps A0 through A1 — resolving the plan-identifier, checking for a handover document lead, and resolving the candidate repo set.
when_to_use: Use when starting discovery for a plan-takeover-execution run, before probing any repo for worktrees, branches, or PRs.
---

# Phase A — Discover Every Trace of This Plan: Plan-Identifier and Repo Set (Sequential per Repo, Hard Gate)

**Continuation-state gate (before A0).** Before delivery state or any resumed action, every takeover
and continuation — handover or not — re-reads canonical instructions and reconciles active rule
decisions under
[Continuation-State Integrity](../../../development/agents/agent-workflow-orchestration/continuation-state-integrity.md).
Stop on unresolved conflicts.

**A0. Resolve the plan-identifier.** `plan-path` may point at `plans/backlog/<slug>/`,
`plans/in-progress/<slug>/`, a dated `plans/done/<date>__<slug>/`, or — if no local folder exists at
all in the current repo — a bare slug/plan-identifier string. The plan-identifier is the folder's
bare slug (no date prefix), the same string that builds the `worktrees/<plan-identifier>/` path per
the [Worktree Path Convention](../../../conventions/structure/worktree-path.md) and, by the convention
already used in multi-repo-parity plans, branch names across repos.

**A0.5. Check for a handover document first — a lead, never a substitute.** Before the repo/artifact
probes below, look in the current repo for the default filename/folder
`local-tmp/handovers/<date>__<plan-identifier>-implementation.md` (glob:
`local-tmp/handovers/*__<plan-identifier>-implementation.md`) — the same default
[`plan-handover-execution.md`](../plan-handover-execution.md)'s frontmatter `outputs.handover-doc`
declares; the two workflows are kept in sync on this one default, changed in both places together if
ever changed. If more than one date
exists for the same plan-identifier, use the most recent by filename date. When found, read it as a
**fast, informal lead** that can narrow and accelerate Phase A2's probes (which repos to check first,
which worktree/branch to expect, which gotchas to watch for) — it is gitignored, local-only, and can
be stale the moment another actor has touched the plan since it was written, so it never substitutes
for A2's own ground-truth verification. Nothing found here is itself evidence; treat it exactly as you
would a colleague's verbal summary — useful context, independently checked before acting on it. Absence
of a handover document is a non-event, not an anomaly — most plans will never have one.

Add handover rule decisions to this record and reconcile again before A1; a handover never triggers
or replaces the gate.

**A1. Resolve the candidate repo set.** Always include: the current repo, plus `ose-private`
whenever it exists as a sibling checkout reachable from the same parent directory as
this repo (per [Related Repositories](../../../../docs/reference/related-repositories.md)) — this is a
**floor, not a ceiling**. If the plan's own `README.md`/`delivery.md` names other repos in its scope
(an explicit "Affected subrepos and apps" table, or a multi-repo-parity companion plan), add those
too. A handover document found in A0.5 naming other repos also widens this set. `TaskCreate` one
discovery task per (repo × artifact-class) pair before probing begins.

**Continued in** [Phase A — Per-Repo Probes and Persistence](./phase-a-discovery-per-repo-probes-and-persistence.md) for the ordered per-repo probe list (A2) and the persist-as-you-go rule (A3).
