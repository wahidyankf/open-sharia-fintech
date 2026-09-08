---
description: Covers Phase C steps 4-5 — recording an existing PR's state and CI status, and reconciling delivery.md to the discovered ground truth before Phase E hands off.
when_to_use: Use when a Bucket-3 repo already has an open PR to resume against, or when delivery.md needs to be brought in line with evidence discovered elsewhere in Phase A.
---

# Phase C — Take Over the Live Work: Recording an Existing PR and Reconciling delivery.md (Sequential per Bucket-3 Repo)

**Continued from** [Phase C — Adopt, Freshness Gate, Ledger Rebuild](./phase-c-adopt-freshness-and-ledger.md).

For each repo classified Bucket 3:

1. **If a PR already exists for this branch**, record its number, state, and CI status
   (`gh pr checks <number>`) — `plan-execution.md`'s Step 2b/2c push-and-CI logic resumes against
   this PR at the plan's next delivery boundary rather than opening a duplicate one.
2. **Reconcile `delivery.md` to the discovered ground truth before Phase E hands off.** The adopted
   copy's `delivery.md` is the resume basis, but Phase A's cross-repo search can surface completed
   work that copy doesn't yet reflect — a further-along PR found in a different repo for the same
   multi-repo-parity plan, a sibling worktree whose `delivery.md` has more `- [x]` items ticked for a
   shared checkbox, or a change that plainly landed (verified in Phase A2's diff/PR read) without its
   Atomic Sync Ritual ever completing. For every such discovered fact, apply the identical [Atomic
   Sync Ritual](../plan-execution.md#atomic-sync-ritual) `plan-execution.md` uses mid-execution — tick
   the checkbox, add an implementation-notes block citing the discovery evidence (which repo, branch,
   commit, or PR it came from), matching `TaskUpdate` — rather than leaving `delivery.md` stale and
   letting `plan-execution.md`'s own Resume Reconciliation under-count progress at Step 1. **Tick only
   from positive evidence gathered in Phase A** (a `MERGED` PR, a `- [x]` line actually present in a
   discovered copy, a diff that proves the described change already landed) — never from inference.
   A Bucket-4 anomaly the user resolved during Phase B also gets a note here, so a future resume sees
   why the state looks the way it does rather than re-discovering the same anomaly cold.
