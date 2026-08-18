# Reply and Resolve Discipline (Hard Rules)

- **Reply to every unresolved thread** — zero threads may remain both unresolved and untouched
  (no reply at all) after a fixer pass. Every thread gets exactly one of: a fix reply, a
  rejection reply, a deferral reply, or a clarifying question.
- **Resolve only what was actually addressed** — call the `resolveReviewThread` GraphQL mutation
  ONLY on threads that were fixed, or whose rejection is well-founded per the higher bar in
  [02-four-way-triage.md](./four-way-triage.md). Never resolve a `defer` or `clarify` thread
  on the same pass it was posted, and never resolve a thread this agent has not genuinely
  engaged with.
- **Never resolve a `fix` thread until the fix is COMMITTED AND PUSHED (HARD)** — thread state is
  not fix state. A fix left uncommitted in the working tree, or committed but not pushed, leaves
  GitHub reporting zero unresolved threads on a PR that still carries the blocking defect. This
  has happened in practice. Before resolving any `fix` thread, verify against the PR's head, not
  against the local tree:

  ```bash
  git status --porcelain          # no fix-related path may still be dirty
  git log origin/<pr-branch> -1   # the fix commit MUST be on the pushed branch
  gh pr diff <PR>                 # the fix MUST appear in the PR's own diff
  ```

  If the fix is not in the PR diff, reply on the thread but leave it UNRESOLVED.

- **A declined-to-touch file is a `defer` or `reject`, never a `fix`** — when this agent
  correctly declines to modify a file it was told to leave alone, that thread is deferred or
  rejected with the scope reason, not resolved as fixed. Resolving it as fixed hides a live
  finding behind a green thread count.

```bash
gh api graphql -f query='
  mutation($threadId: ID!) {
    resolveReviewThread(input: { threadId: $threadId }) {
      thread { id isResolved }
    }
  }' -f threadId="$THREAD_ID"
```

## Repeated-Finding Handling

The orchestrating
[PR-Review Maker→Fixer Cycle workflow](../../../../repo-governance/workflows/pr/pr-review-quality-gate.md)
feeds each fresh cycle the accumulated `prior` findings and their resolution state. Use that
fed-in history to detect repetition. A reasoned rejection does not erase a code-related
MEDIUM/HIGH/CRITICAL finding: the next eligible cycle independently verifies the evidence. If it
remains, it stays merge-blocking and the PR reaches `blocked` at the seven-cycle ceiling rather
than being handed to a human gate or silently suppressed. Capture sanitized learning at cycles
six and seven; see
[Loop-Exit and Block Rules](../../../../repo-governance/workflows/pr/pr-review-quality-gate/loop-exit-and-block-rules.md#loop-exit-and-block-rules).
