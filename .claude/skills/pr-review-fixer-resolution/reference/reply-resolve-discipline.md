# Reply and Resolve Discipline (Hard Rules)

- **Reply to every unresolved thread** — none may remain both unresolved and untouched after a
  fixer pass. Every thread gets exactly one of: a fix reply, a rejection, a deferral, or a
  clarifying question.
- **Every reply opens with a machine-readable disposition block**, so a later pass over this
  repo's PR history can count outcomes without inferring them from prose. Prose alone proved
  unminable: a retrospective over PRs #225/#226/#227/#232 read 89% fixed and 0% rejected off reply
  text, unable to tell a real reject from an unstated one.

  ```html
  <!-- ose-pr-review-disposition:v1
  {"finding_id":"C3-F1","disposition":"fixed|rejected|deferred|clarify",
   "commit":"<SHA or null>","refutation_check":"<command run and its result, or null>"}
  -->
  ```

  `refutation_check` records the outcome of running the finding's refutation clause, which is what
  distinguishes a reasoned reject from a guess. **Never put file content, a secret, a token, or a
  matched literal in it or the prose around it** — this posts publicly. Record `file:line` and
  pass/fail, never what was read. See
  [rule 5](./refutation-clause-execution.md#5-publish-the-outcome-never-the-content).

- **Resolve only what was actually addressed** — call the `resolveReviewThread` GraphQL mutation
  ONLY on threads that were fixed, or whose rejection is well-founded per the higher bar in
  [four-way-triage.md](./four-way-triage.md). A `defer` thread resolves on one condition: its
  follow-up is filed and the link posted. Never resolve a `defer` or `clarify` thread on the pass
  it was posted, nor any thread this agent has not genuinely engaged with.
- **Never resolve a `fix` thread until the fix is COMMITTED AND PUSHED (HARD)** — thread state is
  not fix state. A fix left uncommitted, or committed but unpushed, leaves GitHub reporting zero
  unresolved threads on a PR still carrying the defect. This has happened. Verify against the PR's
  head, never the local tree:

  ```bash
  git status --porcelain          # no fix-related path may still be dirty
  git log origin/<pr-branch> -1   # the fix commit MUST be on the pushed branch
  gh pr diff <PR>                 # the fix MUST appear in the PR's own diff
  ```

  If the fix is not in the PR diff, reply on the thread but leave it UNRESOLVED.

- **A declined-to-touch file is a `defer` or `reject`, never a `fix`** — declining to modify a
  file this agent was told to leave alone defers or rejects the thread with the scope reason.
  Resolving it as fixed hides a live finding behind a green thread count.

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
feeds each fresh cycle the accumulated `prior` findings and their resolution state; use it to
detect repetition. A reasoned rejection does not erase a code-related
MEDIUM/HIGH/CRITICAL finding: the next eligible cycle independently verifies the evidence. If it
remains, it stays merge-blocking and the PR reaches `blocked` at the seven-cycle ceiling rather
than being handed to a human gate or silently suppressed. Capture sanitized learning at cycles
six and seven; see
[Loop-Exit and Block Rules](../../../../repo-governance/workflows/pr/pr-review-quality-gate/loop-exit-and-block-rules.md#loop-exit-and-block-rules).
