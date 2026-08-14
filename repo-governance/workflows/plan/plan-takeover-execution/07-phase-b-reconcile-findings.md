---
title: "Phase B — Reconcile Findings Into One Decision"
description: Defines the four buckets (nothing found, already delivered, live in-flight, anomaly) Phase A's findings classify into for each candidate repo.
when_to_use: Use when classifying a repo's discovered evidence into a single bucket before takeover or cleanup can proceed.
---

# Phase B — Reconcile Findings Into One Decision (Sequential, Hard Gate)

For each repo, classify Phase A's findings into exactly **one** bucket. A repo whose evidence matches
more than one bucket, or contradicts itself, is a **hard anomaly** — stop and escalate to the user
with the raw evidence attached; never guess past it.

- **Bucket 1 — Nothing found.** No worktree, branch, PR, or plan-folder trace anywhere. Nothing to
  take over in this repo; Phase E starts it fresh via `plan-execution.md`'s own Step 0 provisioning.
- **Bucket 2 — Already delivered.** The plan folder lives under `plans/done/` on `origin/main`, and
  every PR found (if any) shows `MERGED`. Nothing to take over — surface this to the user, since the
  current invocation may itself be stale (the plan may need no further execution here at all).
- **Bucket 3 — Live in-flight work.** A worktree and/or branch and/or open PR exists, the found
  `delivery.md` shows partial `- [x]` progress, and no signal contradicts another. This is the
  **takeover target** for that repo.
- **Bucket 4 — Anomaly.** Any of: a worktree with no matching branch (orphaned by an earlier
  `git branch -D`); a pushed branch with no worktree and no PR (provisioned, worked, then abandoned
  mid-session); two or more independent worktrees/branches for the same plan-identifier in one repo;
  or a plan folder present in `plans/in-progress/` on `origin/main` with no worktree, branch, or PR
  referencing it anywhere (this can legitimately be plan-docs-only work committed straight to `main`
  under the plan-docs-on-main carve-out — confirm that reading with the user before treating it as an
  anomaly, since it may simply be correct).

More than one repo landing in Bucket 3 is not itself an anomaly — a multi-repo-parity-style plan can
have genuinely independent per-repo progress. Record each repo's takeover target independently; Phase
E hands off to `plan-execution.md` once per Bucket-3 (or fresh Bucket-1) repo.

Emit the full reconciliation table (repo → bucket → evidence) to the user and to the takeover-report
before Phase C begins.
