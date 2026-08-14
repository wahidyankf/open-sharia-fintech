# Four-Way Triage

For every unresolved thread, choose exactly one outcome:

| Outcome                | When to choose it                                                                      | What happens next                                                                                                                             |
| ---------------------- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **fix**                | The finding is correct and actionable in this PR's scope                               | Implement the fix, push, reply `Fixed: <what changed>`, resolve the thread                                                                    |
| **reject-with-reason** | The finding is wrong, or its cited evidence does not actually apply here               | Reply with a cited rejection justification, resolve the thread ONLY if the rejection is well-founded (see below)                              |
| **defer-with-reason**  | The finding is valid but genuinely out of this PR's scope                              | Reply acknowledging validity + the scope reason it is deferred, do not resolve unless the deferral itself is accepted as final for this cycle |
| **clarify**            | The finding is ambiguous — cannot be fixed, rejected, or deferred without more context | Reply with a specific clarifying question addressed to the maker/human, do not resolve                                                        |

## Fix Path

Implement the fix directly in the working tree, commit, and push to the PR branch. Reply on the
same thread with `Fixed: <what changed>` — a concrete, specific description of the change (file,
mechanism), not a vague "addressed" or "done".

**A finding naming a stale count or terminology change (e.g., "eight" → "nine" of something) is
fixed by a repo-wide grep for the OLD term, not just the file(s) the finding cited.** A fix
scoped to only the named occurrences reliably leaves a second, self-contradicting instance in a
file the citing specialist did not happen to read in full — this has recurred across dogfood
cycles and survived being named-and-deferred once already. Run the repo-wide grep before
replying `Fixed`, not after a later cycle re-discovers the same class of miss.

## Reject Path — A Higher Bar Than "Disagree"

Rejecting a finding requires more justification than accepting one. A rejection is valid ONLY
when it engages directly with the maker's cited evidence and explains, specifically, why that
evidence does not establish the finding — for example: the cited line no longer matches current
behavior, the cited rule does not apply to this code path, or the evidence itself is stale
relative to the pinned head SHA. **Never reply with a bare "won't fix," "disagree," or "not
needed"** — every rejection reply states the specific reason the cited evidence fails to hold.

## Defer and Clarify Paths

- **Defer**: acknowledge the finding is valid in principle, then state precisely why it sits
  outside this PR's scope (a different subsystem, a follow-up plan, an existing tracked concern)
  — with enough detail that a human reviewer can judge whether the deferral itself is reasonable.
- **Clarify**: ask a specific, answerable question when a finding's intent, scope, or expected
  fix is genuinely ambiguous. This is a request for more information, not a stalling tactic — use
  it only when fix/reject/defer cannot be determined from the finding as posted.
