---
title: "Resume Reconciliation (Disk Is Truth)"
description: Defines how execution rebuilds the Task list from delivery.md when resuming, and how to handle Task-list/checkbox divergence.
when_to_use: Use when resuming plan execution in a new conversation, or when the Task list and delivery.md disagree.
---

# Resume Reconciliation (disk is truth)

When execution begins (or re-begins in a new conversation), disk state wins:

1. Read delivery.md top-to-bottom FIRST.
2. For every `- [x]` — skip, count as done.
3. For every `- [ ]` — `TaskCreate` one task in reading order.
4. If stale tasks from a prior run disagree with disk (e.g., task `completed` but checkbox `- [ ]`), delete the stale list and rebuild from current delivery.md.
5. Flag any `- [x]` lacking implementation notes — possible silent batch-tick; the user may want to audit before continuing.
6. **Resolve the plan path against the worktree, not the primary checkout.** For any plan whose delivery mode provisions a dedicated worktree (`worktree-to-pr`, `worktree-to-origin-main`), the worktree's copy of the plan folder is the ONLY authoritative on-disk location — it is the copy on the branch that becomes the PR. A same-named plan folder may still exist under the primary checkout's `plans/in-progress/` (e.g., left over from before the worktree was provisioned); reading or editing that copy instead is a silent-divergence trap — edits there never reach the branch, since the primary checkout isn't what gets pushed. If the same plan folder exists with uncommitted changes in BOTH the primary checkout and the worktree, treat it as a hard anomaly: stop, reconcile which content is accurate (verify independently against commit history / PR state, don't assume either copy), merge the genuinely-verified content into the worktree's copy, and flag the primary checkout's stray copy to the user for cleanup.

7. **Rebuild the file-touch ledger before touching anything.** Disk-is-truth settles _what is done_; it does not settle _who did it_. A resumed run sees a dirty tree that may mix your prior work with a concurrent actor's, and the delivery checklist cannot distinguish them. Recover your ledger from the plan's implementation-notes `Files Changed` blocks and your session transcript. Until it is rebuilt, treat every modified and untracked path as foreign — no staging, no reverting, no cleanup. See [File-Touch Discipline](../../../development/practice/file-touch-discipline.md).

## Divergence handling

If a task is `completed` but the checkbox is `- [ ]`, OR a checkbox is `- [x]` but the matching task is not `completed`, state is inconsistent. Stop, reconcile disk vs list (disk wins), then resume.
