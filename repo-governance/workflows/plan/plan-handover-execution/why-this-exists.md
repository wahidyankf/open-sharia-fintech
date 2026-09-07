---
description: Explains the two kinds of knowledge delivery.md alone can't capture — non-checkbox state and paid-for gotchas — and the three outcomes skipping a handover risks.
when_to_use: Use when justifying why a handover is worth writing instead of relying on delivery.md alone.
---

# Why This Exists

A plan spanning several sessions and several repos accumulates two kinds of knowledge that
`delivery.md`'s checkboxes alone do not capture:

- **State that isn't a checkbox** — an empty worktree provisioned but not yet used, a PR opened as a
  draft, a pause chosen deliberately rather than forced by an error. `delivery.md` records what's
  _done_; it has no place to record what's _in-progress-but-safe-to-leave_.
- **Gotchas already paid for once** — a branch-protection rule that only reveals itself when a push is
  attempted, a review-cycle escalation rule's exact trigger condition, a tool quirk discovered through
  trial and error. Without a handover, the next session re-discovers each of these the same expensive
  way the first session did.

Skipping a handover when one is warranted risks the same three outcomes
[`plan-takeover-execution.md`](../plan-takeover-execution.md) already names
for skipping discovery: re-work, abandoned state, and orphaned leftovers — this workflow prevents them
by making the state explicit before anyone has to go looking for it.
