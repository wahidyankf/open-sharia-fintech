---
title: "Step 1: Working Tree and Branch"
description: Where a propagation run does its work — the current tree by default — and the ledger and staging discipline that make working alongside unrelated changes safe.
when_to_use: Use after intake succeeds and before any file is written, to establish where the run writes and how it keeps out of neighbouring work.
---

# Step 1: Working Tree and Branch

The run works in the **caller's current tree by default**. Propagation is usually invoked
mid-conversation, and forcing a fresh worktree for a two-line rule change costs more than the
isolation buys.

## Choosing

| `isolation` | Behaviour                                                                                                                                    |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `current`   | Work in the tree the caller is already in. The default.                                                                                      |
| `dedicated` | Create a worktree and branch for this run. Use when the rule change is large, or when the current tree holds work that must ship separately. |

Either way the run ends at a PR. `current` changes where the work happens, not how it is delivered.

## Discipline That Makes `current` Safe

Working beside unrelated changes is safe only when the run can prove which changes are its own.

1. **Open the file-touch ledger before the first write.** Every path written, renamed, or deleted
   goes on it, deletions included.
2. **Stage explicit paths from the ledger.** Never stage with a catch-all specification. A
   neighbouring tree routinely holds uncommitted work, and a catch-all sweeps it into this
   delivery.
3. **Expect the hook to widen the commit.** A formatting hook can pull an unstaged neighbour into
   the commit; commit restricted to the ledger's paths so it cannot.
4. **Reconcile at Step 8.** Compare the ledger against the repository's reported status. A path in
   one and not the other is a defect to investigate — never reconciled by editing the ledger.

## Never

- Never set or modify git identity. Verify the configured identity is the intended one before the
  first commit; a wrong identity is a human-only fix.
- Never remove or clean a worktree the run did not create.
- Never assume the repository's worktree topology. Confirm it — layouts change between runs.

## Related Documents

- [Step 6: Write and Tidy](./step-6-write-and-tidy.md) — where the ledger fills up.
- [Step 9: Delivery](./step-9-delivery-and-sibling-obligation.md) — where it is reconciled and shipped.
