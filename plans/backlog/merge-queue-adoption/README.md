# Merge-Queue Adoption — Harden Merge-Precondition (c) Under Concurrent Integration

> **Status**: Backlog (not started). Split out of
> [`worktree-to-pr-hardening`](../../done/2026-07-23__worktree-to-pr-hardening/README.md), where the merge queue was
> researched (decisions **D7 / D10**) but **dropped from scope** because the maintainer could not
> locate a merge-queue toggle in the repo's branch settings. This plan owns that deferred work: **first
> confirm availability, then adopt where available.** Confirmed availability is currently **"nowhere"**
> — GitHub merge queue requires organization ownership, and all three sibling repos are personal
> (User)-owned — so adoption is **blocked on decision MQ-1** (see
> [The Blocking Discovery](#the-blocking-discovery-why-this-is-its-own-plan) below) until the maintainer
> chooses how to proceed.

## Context

The repo's default delivery mode is `worktree-to-pr` [Repo-grounded — AGENTS.md §Delivery Mode], and
its whole rationale is **maximum parallelization** — N independent units become N independent PRs that
review, gate, and merge independently [Repo-grounded — AGENTS.md §Delivery Mode: "The PR is the
independent merge point"]. A PR merges only when **all five hardened merge preconditions** hold, one of
which — **precondition (c)** — requires the branch to be **non-destructively up to date with
`origin/main`** at merge time [Repo-grounded — [PR Merge Protocol](../../../repo-governance/development/workflow/pr-merge-protocol.md)].

A **static, per-PR** "branch up to date" check cannot guarantee (c) under **concurrent** merges: two
PRs each green against yesterday's `main` can both be stale against each other the instant the first
merges. The more the repo leans on its parallel-by-default posture, the more often two `worktree-to-pr`
PRs are ready to merge at overlapping times — exactly the window (c) is weakest in.

A **merge queue** closes that window: it serializes integration, runs CI on the **speculative merge
result** (the PR rebased onto the current queue head), and **auto-evicts** a PR whose queued CI fails
without breaking `main`. Each PR remains an independent merge point, so the queue is fully compatible
with the strict **1-PR ↔ 1-worktree** model.

## The Blocking Discovery (why this is its own plan)

During `worktree-to-pr-hardening` grilling, the maintainer reported: _"I can't find the settings in the
branches for the repo."_ That report turned out to be **factually correct, not a UI-navigation
mistake**: GitHub merge queue is enabled through **branch protection rules / repository rulesets**
("Require merge queue"), but the feature is gated on **repository owner type**, not visibility or plan
tier —

> "Any team that is part of a **managed organization** with public repositories and GitHub Enterprise
> Cloud users will be able to enable this feature on their respective repository."
> — [GitHub Blog: "GitHub Merge Queue is generally available"](https://github.blog/news-insights/product-news/github-merge-queue-is-generally-available/)
> [Web-cited, accessed 2026-07-23]

Merge queue is **not offered at all to repositories owned by a personal (User) GitHub account** —
public or private, any plan tier, including Enterprise Cloud on the user side. Live verification against
the three repos in this plan's scope confirms all three are personal-account-owned:

```text
gh api repos/wahidyankf/ose-public --jq '.owner.type'   → User
gh api repos/wahidyankf/ose-primer --jq '.owner.type'   → User
gh api repos/wahidyankf/ose-private  --jq '.owner.type'   → User
```

[Repo-grounded — verified 2026-07-23]

So the maintainer never found a merge-queue toggle because **there is none to find** on any of these
three repos today — not because of a branch-protection-vs-rulesets UI confusion, and not because of a
plan-tier gap on the private repo. The unlock is **organization ownership**, which none of the three
repos currently has.

This plan's **Phase 0 still investigates and records a per-repo availability matrix** (verified via
`web-researcher` + `gh api`, with the `.owner.type` probe as the primary check), because the ownership
model could change before execution and the matrix is the mechanism that would catch that. Under
**today's facts**, the matrix resolves to "unavailable — User-owned" for all three repos, which puts
**decision MQ-1** (see [tech-docs.md §Open Decisions](./tech-docs.md#open-decisions-grill-at-execution-if-any-fork-is-live))
in the maintainer's hands before any enablement work can proceed: migrate to an organization, adopt a
third-party queue that doesn't require one, harden precondition (c) with a lightweight non-queue
alternative, or keep merge queue deferred. **The CI-trigger and protocol-reword scaffolding (Phases
1–3) is still worth landing regardless of which MQ-1 option is chosen** — a `merge_group` trigger is
inert until a queue exists (the `merge_group` event only fires once a PR enters a merge queue —
[GitHub Actions docs](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#merge_group)
[Web-cited, accessed 2026-07-23]; see also [tech-docs.md §Rollback](./tech-docs.md#rollback)), and the
reworded precondition (c) keeps its manual fallback — but
**enablement (Phase 4 onward) cannot execute until MQ-1 is resolved.**

## Scope

**In scope**:

- **Availability investigation** — a per-repo merge-queue availability matrix keyed on **owner type**
  (organization vs personal User account, the actual gate — not visibility or plan tier), web-cited and
  `gh api`-verified.
- **CI trigger** — add the `merge_group` event to the CI workflow(s) that must gate the speculative
  merge, in each adopting repo's `.github/workflows/` (an `[AI]` YAML change; `actionlint`-clean).
- **Protocol reword** — update `pr-merge-protocol.md` **precondition (c)** so it is **satisfiable by
  the queue's speculative merge** where a queue is enabled, while **retaining the manual
  branch-up-to-date form as the fallback** for repos/branches without a queue. The (a)–(e) lettering
  and the other four preconditions stay verbatim.
- **Operations doc** — how the queue interacts with the 3-cycle PR-Review Maker→Fixer Cycle, the
  `[AI]` automerge default, and the 1-PR↔1-worktree model.
- **Enablement** — a per-repo `[HUMAN]` runbook to toggle the queue in repository settings (**an agent
  must not change repository security/settings**), bracketed by `[AI]` prep and `[AI]` post-enable
  verification (`gh api` + a smoke check).
- **Mechanism** — **GitHub-native merge queue** (decision carried from `worktree-to-pr-hardening` D10;
  lowest friction given the existing `gh` toolchain). Graphite/Aviator recorded as alternatives only.
- **Three-repo parity** (conditional) — the shared CI-trigger + protocol/doc scaffolding is held in
  parity across `ose-public` → `ose-primer` → `ose-private`, with **enablement conditional per repo** on
  the availability matrix and, under today's facts, on **MQ-1** resolving for all three.

**Out of scope**:

- Any `apps/`/`libs/` runtime code (this plan is CI-config + governance docs only).
- The PR-reviewer decomposition (owned by `worktree-to-pr-hardening`).
- Provisioning a bot/GitHub-App identity (separate idea).
- Changing any of the other four merge preconditions (a), (b), (d), (e).
- **Deciding MQ-1 on the maintainer's behalf** — migrating repo ownership to a GitHub organization is a
  significant `[HUMAN]` infra decision, adopting a third-party queue is a vendor decision, and both are
  outside this plan's authority to choose; the plan records the fork and a recommendation, not a
  pre-made choice.

## Navigation

- [brd.md](./brd.md) — WHY: business rationale, impact, risks, success metrics.
- [prd.md](./prd.md) — WHAT: personas, user stories, Gherkin acceptance criteria, product scope.
- [tech-docs.md](./tech-docs.md) — HOW: mechanism, availability matrix, precondition-(c) reword, CI
  trigger, the `[AI]`-automerge-via-queue interaction, research grounding, and open decisions.
- [delivery.md](./delivery.md) — DO: phased, gated delivery checklist (Delivery Mode `worktree-to-pr`).
- [learnings.md](./learnings.md) — Knowledge Capture running log.

## Delivery Mode

`worktree-to-pr` (the repo default). This plan dogfoods the very mechanism it adopts: once the queue is
enabled, this plan's own downstream propagation PRs merge **through** the queue.
