# A merge queue to hold merge-precondition (c) under concurrent integration

One-line summary: the repo's `worktree-to-pr` default deliberately produces overlapping merge windows,
which is exactly where the static per-PR "branch is up to date" check behind merge-precondition (c)
is weakest — a merge queue would close that window, but GitHub's native queue is gated on
organization ownership and all the sibling repos are personal-account-owned.

> Provenance: demoted from the full `backlog/` plan `merge-queue-adoption/` to a two-pager on
> 2026-08-05, because its execution is blocked on a `[HUMAN]` ownership decision that no plan can make
> for the maintainer. It owns the merge-queue work deferred from
> [`worktree-to-pr-hardening`](../../done/2026-07-23__worktree-to-pr-hardening/README.md), where the queue
> was researched as decisions **D7** (adopt vs. defer) and **D10** (mechanism) and then dropped from
> scope on 2026-07-23 when the maintainer could not find a merge-queue toggle in the repo's branch
> settings.

## Problem / context

The [PR Merge Protocol](../../../repo-governance/development/workflow/pr-merge-protocol.md) requires five
hardened preconditions, lettered (a) through (e), before any PR merges. Precondition **(c)** is "the
branch is non-destructively up to date with the latest `origin/main` at merge time." Today that is a
**static, per-PR** check, and a static check cannot guarantee (c) under **concurrent** merges: PR-A and
PR-B are each green against base `X`; A merges, so `main` becomes `X+A`; B is now silently stale against
`X+A` and can carry a semantic — not textual — conflict that no per-PR check ever saw. The repo's
default delivery mode is `worktree-to-pr` precisely to maximize parallelization, with each independent
unit becoming its own PR and its own merge point, so the design deliberately manufactures the exact
overlapping-window condition that (c) is weakest in. Preconditions (a), (b), (d), and (e) are unaffected
by this; only (c) has a concurrency hole.

A merge queue closes it structurally: a ready PR is **enqueued** rather than merged, the queue builds a
**speculative merge** (the PR rebased onto the current queue head), CI runs on that artifact via
GitHub's `merge_group` event, and a PR whose queued CI fails is **auto-evicted** without `main` ever
breaking. Each PR keeps its own queue entry, so the strict 1-PR ↔ 1-worktree model survives intact.

The catch, discovered during the parent plan's grilling, is that the maintainer's "I can't find the
settings" report was **factually correct, not a UI-navigation mistake**. GitHub merge queue is enabled
through a branch protection rule or a repository ruleset targeting `main` with **"Require merge queue"**
checked — but the feature is gated on **repository owner type**, not visibility and not plan tier.
Live verification on 2026-07-23 via `gh api repos/<owner>/<repo> --jq '.owner.type'` returned `User`
for `ose-public` and `ose-private` alike. There is no toggle to find, in either of them.

## Why now

Not now, honestly — and naming that is the point of demoting this. The blocker is a single shared
decision (call it **MQ-1**) about ownership model, and it sits entirely with the maintainer: migrate the
repos to a GitHub organization, adopt a third-party queue that works on user-owned repos, harden (c)
some lighter non-queue way, or keep the status quo. None of those are a docs-and-CI plan's call to make.
What keeps the idea alive is that the underlying exposure grows with the parallel posture: the more the
repo leans on `worktree-to-pr` fan-out, the more often two PRs are ready at overlapping times. There is
also a live interaction worth watching — see the promotion signal below.

## Prior art / precedents

- [`worktree-to-pr-hardening`](../../done/2026-07-23__worktree-to-pr-hardening/README.md) — the parent
  plan that established the five hardened preconditions and researched the queue (D7/D10) before
  dropping it; the first thing to re-read on promotion.
- [`standardize-repo-toolchain-parity`](../../done/2026-06-13__standardize-repo-toolchain-parity/README.md)
  — the precedent for how shared CI/governance scaffolding is held in parity across the sibling repos,
  which is the shape any propagation here would take.
- [sibling-main-ci-never-runs-on-merge](./sibling-main-ci-never-runs-on-merge.md) — the same family of
  defect: a merge-integration signal that is assumed to exist and does not.
- **GitHub-native merge queue** — the D10 mechanism choice. Availability is stated in
  [GitHub's GA announcement](https://github.blog/news-insights/product-news/github-merge-queue-is-generally-available/)
  and confirmed independently in
  [GitHub Community Discussion #51483](https://github.com/orgs/community/discussions/51483): queues are
  available on organization-owned repos, not personal-account ones, regardless of plan tier. The
  `merge_group` event is documented in the
  [GitHub Actions events reference](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#merge_group).
- **[Graphite's stack-aware queue](https://graphite.com/blog/the-first-stack-aware-merge-queue)** — the
  strongest third-party candidate; CI once on the stack head with binary-search failure isolation.
  Whether it works without a GitHub organization is **unverified** and needs a dedicated research pass
  before it could be chosen.

## Proposed direction (sketch)

- **Resolve MQ-1 first.** Everything downstream branches on it. Re-run the `.owner.type` probe as the
  primary availability check — a ruleset probe cannot distinguish "not offered" from "not configured".
- **CI trigger** — add `merge_group` to the `on:` block of whichever workflow carries the checks
  required for merge on `main` (today that is `.github/workflows/pr-quality-gate.yml`), reusing the
  existing `pull_request` job set so queued CI equals branch CI. This is `actionlint`-clean YAML and is
  **inert until a queue exists**, since `merge_group` only fires when a PR enters a queue — which makes
  it safe to land ahead of any decision.
- **Reword precondition (c)** so it is satisfiable by the queue's speculative merge where a queue is
  enabled, while **retaining the manual branch-up-to-date form as the fallback** everywhere else. The
  (a)–(e) lettering and the other four preconditions stay verbatim. Critically, (c) is restated across
  several governance surfaces that must stay congruent — `pr-merge-protocol.md` alone states it four
  times, and it is restated again in
  [`pr-review-quality-gate.md`](../../../repo-governance/workflows/pr/pr-review-quality-gate.md),
  `plan-quality-gate.md`, [`plans.md` §Delivery Mode](../../../repo-governance/conventions/structure/plans.md),
  and [`AGENTS.md` §Delivery Mode](../../../AGENTS.md). Editing only one recreates the drift those docs
  warn about.
- **Operations doc** — how a queue interacts with the three-cycle PR-Review Maker→Fixer Cycle (the
  queue runs _after_ review, as pure integration), with the `[AI]`-merges-by-default posture (with a
  queue, "merge" means "enqueue"), and with 1-PR ↔ 1-worktree.
- **Enablement is `[HUMAN]`-only** — an agent prepares the runbook and verifies afterward via `gh api`;
  an agent must never change repository security settings.

## Rough scope & non-goals

In scope: a per-repo availability matrix keyed on owner type; the `merge_group` CI trigger; the
precondition-(c) reword across every surface that restates it; a merge-queue operations doc; a
`[HUMAN]` enablement runbook bracketed by `[AI]` prep and `[AI]` verification; and parity of the shared
scaffolding across the parity repos (`ose-public`, `ose-private`) with enablement conditional per repo.

Out of scope:

- Any `apps/` or `libs/` runtime code — this is CI config plus governance docs only.
- The PR-reviewer decomposition, owned by `worktree-to-pr-hardening`.
- Provisioning a bot or GitHub-App identity — see [pr-review-bot-identity](./pr-review-bot-identity.md).
- Changing preconditions (a), (b), (d), or (e), or the (a)–(e) lettering.
- **Deciding MQ-1 on the maintainer's behalf.** Migrating repo ownership to a GitHub organization is a
  significant `[HUMAN]` infra decision and adopting a third-party queue is a vendor decision; this brief
  records the fork and a recommendation, never a pre-made choice.

## Risks & open questions

- **Which MQ-1 branch?** Organization migration (unlocks the native queue for all repos at once, but
  means a new billing entity, re-pointed remotes and CI credentials, and possible permission changes),
  a third-party queue, a lightweight non-queue guard, or continued deferral. The parent plan's own
  recommendation was **continued deferral** — it forces no decision under artificial time pressure and
  keeps the other options open. (open)
- **Does Graphite actually work on personal-account repos?** The "no organization required" premise is
  unverified and would need a `web-researcher` pass before it could be committed to. (open)
- **Does `gh pr merge --auto` reliably enqueue rather than fight the queue?** Independent reports
  (e.g. `cli/cli#5653`) suggest the behavior is not uniform across `gh` versions. This matters because
  `[AI]` automerge is the repo default; it needs a smoke check before anything relies on it. (open)
- **What would a non-queue hardening of (c) look like?** An auto-rebase-before-merge guard or a
  serialize-merges convention needs design work that has not been done. (open)
- **Runner load.** A queue _serializes_ integration, so it should mean fewer concurrent full-CI runs,
  not more — but that reasoning is untested against the self-hosted stack.
- Queued CI drifting from branch CI, and parity drift where scaffolding lands in some repos but not
  others, are both real but well-understood; reusing the `pull_request` job set and delivering each repo
  through its own cycle handles them.

## What success looks like + promotion signal

Success is narrow and checkable: precondition (c) holds under concurrency wherever a queue is enabled —
two concurrently-ready PRs integrate through the queue with CI on each speculative merge, and a PR
failing queued CI is auto-evicted without breaking `main` — while (a), (b), (d), and (e) stay verbatim
and (c) keeps a documented manual fallback for every branch and repo without a queue. Where no queue
exists, success is that the deferral is **written down, naming the exact owner-type limitation and the
resume condition**, rather than silently absent.

Promotion signal: **MQ-1 resolves to an option that unlocks a queue** — concretely, when
`gh api repos/<owner>/<repo> --jq '.owner.type'` returns `Organization` for at least one sibling repo,
or when a third-party queue is verified to work on user-owned repos. Either makes the enablement work
real rather than hypothetical.

One dependency to check before promoting, because it is genuine even though the plan has since landed:
the [`sdlc-gate-registry-enforcement`](../../done/2026-08-07__sdlc-gate-registry-enforcement/README.md)
plan **deletes `main-ci.yml` in all four repos** and folds its unique checks into the PR gate, amending the
Gate Composition Rule to `(pre-commit ∪ pre-push) == PR gate`. That plan explicitly accepts the
resulting loss: with `main-ci.yml` gone, no surface re-verifies the whole repo, and the PR gate's
`push: [main]` trigger computes affected from `github.event.before`, which covers the merged change but
**not cross-PR interaction** — "two PRs that are individually green and mutually breaking will land on
`main` with neither one's affected graph covering the other." That is the same failure mode this brief
exists to fix, now an explicitly accepted risk elsewhere. It cuts both ways: the accepted risk raises
the value of a queue, and the gate registry changes which workflow the `merge_group` trigger belongs on.
Promote only after that plan lands, and target the PR gate it leaves behind.
