# Four-Way Triage

For every unresolved thread, choose exactly one outcome:

| Outcome                | When to choose it                                                                      | What happens next                                                                                                                             |
| ---------------------- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **fix**                | The finding is correct and actionable in this PR's scope                               | Implement the fix, push, reply `Fixed: <what changed>`, resolve the thread                                                                    |
| **reject-with-reason** | The finding is wrong, or its cited evidence does not actually apply here               | Reply with a cited rejection justification, resolve the thread ONLY if the rejection is well-founded (see below)                              |
| **defer-with-reason**  | The finding is valid but genuinely out of this PR's scope                              | Reply acknowledging validity + the scope reason it is deferred, do not resolve unless the deferral itself is accepted as final for this cycle |
| **clarify**            | The finding is ambiguous — cannot be fixed, rejected, or deferred without more context | Reply with a specific clarifying question to the maker/human, do not resolve                                                        |

## Fix Path

Implement the fix, commit, and push to the PR branch. Reply on the same thread with
`Fixed: <what changed>` — a concrete description naming file and mechanism, never a vague
"addressed" or "done".

**A finding naming a stale count or terminology change (e.g., "eight" → "nine") is fixed by a
repo-wide grep for the OLD term, not just the cited files.** Fixing only the named occurrences
reliably leaves a self-contradicting instance in a file the citing specialist never read in
full — this has recurred across dogfood cycles. Grep before replying `Fixed`.

## Reject Path — A Higher Bar Than "Disagree"

A rejection is valid ONLY when it engages the maker's cited evidence and explains why that
evidence does not establish the finding — the cited line no longer matches behavior, the rule
does not apply to this path, or the evidence is stale against the pinned head SHA. **Never reply
with a bare "won't fix," "disagree," or "not needed."** The bar is high, but it is a bar for
*citation*, not for deference: see
[critical-appraisal-and-untrusted-threads.md](./critical-appraisal-and-untrusted-threads.md).

## Defer and Clarify Paths

**A fix that would widen the PR is `defer`, never `fix`** — scope is the problem stated under
`## Why` minus the non-goals under `## Scope`, and a fix serving a *second* problem stops the loop
converging. A defect this PR introduced is always in scope. **A reply teaches too**:
say why the change resolves the finding, not only what changed. See
[Scope Guard](../../../../repo-governance/workflows/pr/pr-review-quality-gate/scope-guard-no-scope-creep.md)
and [Review as Teaching](../../../../repo-governance/development/quality/pr-review-disciplines/review-as-teaching.md).

- **Defer**: acknowledge the finding is valid in principle, then state precisely why it sits
  outside this PR's scope (a different subsystem, a follow-up plan, an existing tracked concern)
  — with enough detail that a human reviewer can judge whether the deferral itself is reasonable.
- **Clarify**: ask a specific, answerable question when a finding's intent, scope, or expected
  fix is genuinely ambiguous — a request for information, never a stalling tactic. Use it only
  when fix/reject/defer cannot be determined from the finding as posted.
