# Business Requirements: PR Review Rule Convergence

## Goal

Make review effort proportionate to behavior-changing risk while retaining a clear, bounded path to
merge and a rigorous response to credential exposure.

## Rationale

The current universal three-cycle review requirement consumes specialist capacity for text-only work
that is already checked by `.github/workflows/pr-quality-gate.yml`. Conversely, a complex executable
diff may need more than three review/fix passes; without an explicit cycle-six learning trigger, the
maintainer gets no reusable explanation of slow convergence.

## Business Impact

- Maintainers spend specialist-review effort on changed executable behavior instead of prose-only
  delivery, while the named CI workflow remains the merge gate for the latter.
- A difficult executable change produces reusable evidence and an idea for improving convergence rather
  than silently consuming more review cycles.
- A confirmed secret leak has a containment and reachable-history response that does not reproduce the
  exposed material in new records.

## Affected Roles

- **Repository maintainer**: chooses the correct PR route and observes the final merge conditions.
- **PR-review orchestrator and specialists**: classify diffs, run only eligible cycles, and capture
  convergence evidence.
- **Repo-rules maker**: propagates canonical instructions, generated bindings, and the portable
  cross-repository manifest.
- **Security responder**: executes the documented containment and remediation flow without retaining
  secret values in evidence.

## Success Metrics

- An agent can classify a PR from its diff and determine one merge path without knowing whether the
  change originated from `plans/`.
- An eligible PR cannot merge while Medium, High, or Critical code findings remain; the loop ends no
  later than cycle seven.
- A non-eligible PR can merge without specialist review after its named quality workflow is green.
- A secret incident has a credential-safe, executable containment and history-remediation route.
- Public, private, and Primer governance consumers receive the applicable equivalent rules through
  documented public-first companion deliveries.

## Risks and Mitigations

| Risk                                                                     | Mitigation                                                                                                                                                         |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Ambiguous executable-config classification produces inconsistent reviews | Define the classifier by behavior, require the scout to record its evidence, and treat uncertainty as eligible.                                                    |
| Seven cycles normalize unresolved defects                                | Make seven a ceiling, never a permission to merge with code M/H/C findings; capture why convergence was slow starting at cycle six.                                |
| A rewrite amplifies secret exposure through logs or review text          | Never copy candidate values; use sanitized incident identifiers and silent scanners only.                                                                          |
| Separate public/private merges briefly drift                             | Prepare and validate the private companion first, merge the public canonical source, then immediately merge the private counterpart and record the reconciliation. |
| Primer drift persists because it is a delayed-sync consumer              | Include its companion delivery and live-plan retrofit in this plan after public/private reconciliation.                                                            |
| Queued CI is mistaken for a failed goal and abandoned                    | Codify contention investigation and patient cadence-based polling across all in-scope repositories.                                                                |
| The private companion is delayed by an unavailable quality check         | Apply the user's one-plan, OSE-private-only direct-push exception while retaining expected-head, secret-safety, and manifest checks.                               |
| Concurrent private PR-quality work blocks unrelated delivery             | Use a separate plan worktree from `origin/main`; do not modify or wait for foreign work.                                                                           |
| Completed plan worktrees accumulate and confuse later work               | Propagate immediate, exact-path worktree cleanup after each repository's final plan delivery.                                                                      |

## Non-Goals

- Guaranteeing removal from private clones, forks, notification emails, or uncooperative third-party
  caches.
- Replacing required branch protection or bypassing a failed workflow.
- Rewriting unrelated OSE Primer product or private-only operational documentation.
- Extending the OSE-private direct-push exception to another repository, workflow, or plan.
