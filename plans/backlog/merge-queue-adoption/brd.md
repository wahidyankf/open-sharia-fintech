# Business Requirements — Merge-Queue Adoption

## Business Goal

Make **merge-precondition (c)** — "the PR branch is non-destructively up to date with `origin/main` at
merge time" — hold **under concurrent `worktree-to-pr` merges**, not only when PRs merge one at a time,
by adopting a **merge queue** in every sibling repo **where the platform makes one available**, without
weakening any of the other four merge preconditions and without an agent ever changing repository
security settings.

## Repo Scope — Three-Repo Parity (conditional on availability)

The merge-queue CI trigger and the `pr-merge-protocol.md` reword are **shared scaffolding** (governance

- CI harness) that normally stays in parity across `ose-public`, `ose-primer`, and `ose-infra`, the
  same posture as the prior `standardize-repo-toolchain-parity` and `lint-safety-parity` 3-repo plans
  [Repo-grounded — AGENTS.md §Related Repositories]. **Enablement**, however, is gated on **repository
  owner type** — organization vs personal (User) account — which is the actual GitHub-documented
  discriminator, not repository visibility or account plan tier:

> "Any team that is part of a **managed organization** with public repositories and GitHub Enterprise
> Cloud users will be able to enable this feature on their respective repository."
> — [GitHub Blog: "GitHub Merge Queue is generally available"](https://github.blog/news-insights/product-news/github-merge-queue-is-generally-available/)
> [Web-cited, accessed 2026-07-23]

- **`ose-public`** — personal (User)-owned; **queue unavailable today**; source of truth; scaffolding
  authored and validated here first regardless.
- **`ose-primer`** — personal (User)-owned; **queue unavailable today**; receives identical scaffolding.
- **`ose-infra`** — personal (User)-owned, private; **queue unavailable today** — and, unlike the
  original premise, this is **not** a plan-tier gap fixable by a billing upgrade; it is the same
  organization-ownership gate as the two public repos.

Live verification (`gh api repos/<owner>/<repo> --jq '.owner.type'`) against all three repos returns
`User` for each [Repo-grounded — verified 2026-07-23]. **All three repos resolve to the same
unavailable state today** — this is a single shared blocker (decision **MQ-1**), not three independent
per-repo gaps of differing severity.

Business rationale for the conditional posture: the gate that guards `main` should be identical
wherever the platform allows it. Because the unavailability is now known to be **identical across all
three repos** (not a public-vs-private split), the CI-trigger + protocol scaffolding still lands
everywhere as forward-looking, harmless preparation (a `merge_group` trigger is inert without an
enabled queue — cited at [tech-docs.md §Rollback](./tech-docs.md#rollback)), while **enablement for all
three repos is deferred together** pending MQ-1 — migrate to
an organization, adopt a third-party queue, harden precondition (c) without a queue, or keep the status
quo. See [tech-docs.md §Open Decisions — MQ-1](./tech-docs.md#open-decisions-grill-at-execution-if-any-fork-is-live).

## Business Rationale (why this exists)

`worktree-to-pr` is the default precisely to **maximize parallelization** — independent units become
independent PRs that gate and merge independently [Repo-grounded — AGENTS.md §Delivery Mode]. That
design deliberately produces **overlapping merge windows**, which is exactly where a static per-PR
"branch up to date" check is weakest: two PRs green against the same base can both go stale the instant
the first merges, and the second can land a semantic conflict that no per-PR check caught. The busier
the parallel posture, the more real that risk.

This plan was **split out of `worktree-to-pr-hardening`**, where the queue was researched (D7/D10) but
dropped because the maintainer could not find a merge-queue toggle in the repo's branch settings. The
missing-toggle observation is itself a **business signal** — merge-queue availability is not universal;
it is gated on **repository owner type** (organization vs personal account), confirmed by live
`gh api` verification against all three repos — so the responsible move is to **confirm availability
first**, name the real blocker (MQ-1, an ownership-model decision) accurately, and let the maintainer
choose how to proceed rather than assume availability anywhere.

## Business Impact

**Pain points addressed**:

- **Concurrency-stale merges** — under parallel `worktree-to-pr`, precondition (c) can pass per-PR yet
  be violated the moment a sibling PR merges first. The queue re-validates each PR against the live
  queue head via speculative-merge CI.
- **Broken `main` from silent semantic conflicts** — two individually-green PRs can conflict
  semantically (not textually). Speculative-merge CI catches this **before** the second lands;
  auto-eviction keeps `main` green.
- **Manual rebase toil** — today, keeping (c) true under concurrency means humans/agents manually
  rebasing racing PRs. The queue automates the ordering.

**Expected benefits** (qualitative — not measured targets):

- **(c) holds under concurrency**, not just serially — an observable property once the queue is enabled.
- **`main` stays green** across concurrent merges (speculative CI + auto-eviction).
- **Less rebase babysitting** for racing PRs.

## Affected Roles (hats the solo maintainer wears; agents that consume these files)

- **CI author** — adds the `merge_group` trigger to the workflow(s) that gate the speculative merge.
- **Governance author** — rewords `pr-merge-protocol.md` precondition (c) and writes the operations doc.
- **The Maintainer enabling the queue** — performs the `[HUMAN]` settings toggle an agent must not touch.
- **Consuming agents** — `plan-execution` and the **PR-Review Maker→Fixer Cycle** agents
  (`pr-review-maker` / `pr-review-fixer`), whose 3-cycle loop and 5-precondition gate must be preserved
  verbatim, now with (c) satisfiable by the queue.

This is a solo-maintainer repo — no sign-off ceremony; the maintainer wears each hat in sequence.

## Business-Level Success Metrics

Gut-based reasoning is used where no measurement exists yet; nothing below is an already-observed number.

- **Availability resolved, not assumed** (observable fact once executed): a per-repo availability matrix
  is recorded keyed on **owner type** (organization vs personal User account — the real gate), web-cited
  and `gh api`-verified, before any enablement.
- **(c) hardened where available** (observable fact once executed): in every repo where the queue is
  enabled, two concurrently-ready `worktree-to-pr` PRs integrate through the queue with CI on the
  speculative merge, and a PR failing queued CI is auto-evicted without breaking `main`.
- **No precondition regression** (observable fact): the other four preconditions (a), (b), (d), (e) and
  the (a)–(e) lettering are unchanged; (c) retains a manual fallback for any branch/repo without a queue.
- **Conditional deferral is explicit, not silent** (observable fact): any repo where the queue is
  unavailable carries a written deferral naming the exact owner-type limitation and the resume
  condition (MQ-1 resolution).

## Business-Scope Non-Goals

- Not re-architecting the PR-review agents (owned by `worktree-to-pr-hardening`).
- Not deciding MQ-1 (organization migration, third-party queue, non-queue hardening, or deferral) on the
  maintainer's behalf — a `[HUMAN]` ownership/vendor decision outside this plan's authority.
- Not touching preconditions (a), (b), (d), (e).
- Not provisioning a bot/GitHub-App identity.

## Business Risks and Mitigations

| Risk                                                                                      | Likelihood                           | Mitigation                                                                                                                                                 |
| ----------------------------------------------------------------------------------------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Merge queue unavailable for **all three repos** (personal-account-owned, confirmed today) | Confirmed (not merely a possibility) | Phase 0 availability matrix leads with the `.owner.type` probe; ship CI-trigger + protocol scaffolding regardless; MQ-1 records the fork and a resume path |
| Agent tempted to toggle repo security settings                                            | Low                                  | Hard rule — enablement is a `[HUMAN]` step; agent only prepares the runbook and verifies via `gh api` afterward                                            |
| `merge_group` CI overloads the self-hosted runners                                        | Medium                               | The queue **serializes** integration (fewer concurrent full-CI runs, not more); reuse existing concurrency groups                                          |
| `[AI]` automerge default breaks under a queue                                             | Medium                               | Operations doc specifies the automerge-via-queue path (`gh pr merge --auto` adds to queue); dogfooded on this plan's own PRs                               |
| Speculative-merge CI diverges from branch CI                                              | Low                                  | The `merge_group` workflow reuses the same jobs as `pull_request`; `actionlint` gate on the trigger addition                                               |
| Parity drift (docs land in some repos but not others)                                     | Low                                  | Each repo delivered via its own `worktree-to-pr` cycle from the merged `ose-public` source of truth                                                        |

The cross-cutting factual claims behind these risks live here; the corresponding **testable scenarios**
live in [prd.md §Acceptance Criteria](./prd.md#acceptance-criteria).
