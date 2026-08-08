---
title: "BeaverNest Repository Consolidation"
description: Fold the beaver-nest product into ose-public, archive the repo, and reduce the OSE family from four repositories to three
category: explanation
subcategory: plans
tags:
  - governance
  - cross-repo
  - consolidation
  - beaver-nest
  - parity
created: 2026-08-06
---

# Plan: Fold BeaverNest Into `ose-public` and Retire the Fourth Repository

## Context

The OSE family is four repositories. Three of them — `ose-public`, `ose-primer`, `ose-private` —
form the **parity loop** whose generic content is deliberately kept aligned. The fourth,
[`beaver-nest`](https://github.com/wahidyankf/beaver-nest), sits outside that loop but is a full
family member, and every governance rule written for "all four repos" must be authored, propagated,
and verified there too.

`beaver-nest` is not an independent codebase. It shares root commit `8257d1ff4` with this repo
[Repo-grounded — `git rev-list --max-parents=0 HEAD` returns the same SHA in both trees, verified
2026-08-06], was produced by stripping a full `ose-public` clone down to its engineering harness
([`plans/done/2026-07-31__baseerah-repo-reset`](https://github.com/wahidyankf/beaver-nest) in that
repo), and was then rebranded wholesale. What it carries today is overwhelmingly **this repo's
scaffolding, drifted**:

1. **202 governance files, 200 shared with `ose-public`, of which 118 (59%) have diverged**
   [Repo-grounded — file-by-file comparison, 2026-08-06]. The overwhelming majority of that
   divergence is mechanical rename churn (`ayokoding-www`/`ose-www` → `beaver-nest-fe`/`-be` in
   prose, paths, and command examples), not genuine rule difference. A smaller class is **real
   drift where `beaver-nest` is simply behind** — it lacks the Type-soundness PR-review discipline,
   the gate-registry git-hook model, the Build-Artifact Sweeper convention, and this repo's
   `main-to-origin-main` selection-signal restriction.
2. **43 idea two-pagers, 35 of which are name-duplicates of `ose-public`'s own**
   [Repo-grounded — `comm -12` over both `plans/ideas/` listings, 2026-08-06]. Only 8 were unique at
   that measurement, and only 4 of those 8 are product-specific. **The generic half of that set is
   volatile** — both repos' `plans/ideas/` trees are under active cross-repo grooming — so Phase 0
   re-derives the manifest and the plan triages that, not this number.
3. **A fork of `apps/rhino-cli`** that has fallen behind: `src/application/parity.rs`,
   `src/commands/gate/`, and `src/commands/git/` exist only upstream
   [Repo-grounded — `diff -rq` across both trees, 2026-08-06].
4. **A product surface that is a walking skeleton.** `beaver-nest-be` exposes exactly two HTTP
   endpoints (`GET /api/v1/health`, `GET /api/v1/readiness`) over 858 lines of F#; its single
   database migration is literally `SELECT 1;` with zero domain tables. `beaver-nest-fe` is a
   single-screen Vite/React SPA of 211 lines (excluding tests and the generated OpenAPI client) whose
   own copy reads "No workspace features yet"
   [Repo-grounded — source inspection, 2026-08-06]. There is no assistant, no content builder, no
   posting helper — those are roadmap, not built.

So the fourth repository costs a full governance-propagation lane, a duplicated CI harness, a
diverging CLI fork, and a duplicated idea backlog, and in exchange holds ~1,300 lines of product
source with no shipped capability. **The maintainer's stated reason for this plan is exactly that
burden: four open repositories are too many to maintain, and three is enough.**

Consolidation also resolves a live governance contradiction. `docs/reference/sdlc-gate-standard.md`
declares `apps/rhino-cli` byte-identical across "all four bound repos", and
`apps/rhino-cli/src/application/parity.rs:557` emits that same four-repo claim at runtime — while
[`docs/reference/related-repositories.md`](../../../docs/reference/related-repositories.md) states
that `beaver-nest` carries an unbound fork and sits in neither cross-repo boundary
[Repo-grounded — all three read 2026-08-06]. Removing the fourth repo removes the contradiction
rather than papering over it.

> Requested 2026-08-06. Grilled via `AskUserQuestion` before authoring — see
> [Resolved Design Decisions](#resolved-design-decisions-from-grilling) below.

## Scope

**Repo scope**: three repositories. `ose-public` receives the ported product and hosts this plan
folder; `ose-primer` and `ose-private` receive only the terminology sweep that follows from the
family shrinking to three. `beaver-nest` is the **subject** of the plan, not a target of it — no
change lands there beyond the final archive flip.

**In scope**

- Port the BeaverNest product into `ose-public` under the repo's own naming tiers:
  `apps/beavernest-be`, `apps/beavernest-app-web`, and their two E2E pairs; the
  `specs/apps/beavernest/` tree; `infra/dev/beavernest-app/`; the staging CI caller; the three F#
  projects in `open-sharia-enterprise.sln`; and the `beavernest.css` brand token sheet.
- Port [`repo-governance/vision/beaver-nest.md`](https://github.com/wahidyankf/beaver-nest) as a
  child product vision alongside the existing ecosystem vision, and register it in
  `repo-governance/vision/README.md`.
- Port every `beaver-nest`-unique idea two-pager on the manifest Phase 0 freezes (8 at the
  2026-08-06 baseline; re-derived at execution time), folding each into an existing `ose-public`
  brief where one already covers the same problem, per the Integrate-Before-You-Add rule.
- Sweep the four-repo terminology to three across all three surviving repos — including the
  `apps/rhino-cli` string change, which must land **byte-identically** in all three.
- Archive `github.com/wahidyankf/beaver-nest` on GitHub.

**Out of scope**

- Any git-history merge. Commit history stays in the archived repository (see D1).
- `beaver-nest`'s governance tree, its `apps/rhino-cli` fork, and its 35 duplicate idea two-pagers.
  `ose-public` is upstream and authoritative for all three (see D2).
- `libs/web-ui` reconciliation. The ported frontend consumes **this** repo's `web-ui`; the
  `beaver-nest` copy's 43 divergent files are discarded, not merged.
- Building any actual BeaverNest product capability. The walking skeleton lands as-is.
- Deploying BeaverNest anywhere. `beaver-nest` has no `prod-*` or `stag-*` branch today
  [Repo-grounded — `git branch -r` shows only `origin/main` and one PR branch, 2026-08-06], and this
  plan creates none.

## Approach Summary

Four delivery units, executed in order:

1. **Port the product** into `ose-public` behind a rename from the `beaver-nest-fe`/`-be` names to
   the tier-conformant `beavernest-app-web`/`beavernest-be`, wire it into Nx, CI, and the specs
   gates, and prove the gates green. One PR.
2. **Port the narrative surface** — vision doc, unique ideas, docs registration — and record the
   `beaver-nest-app-setup` plan's disposition. One PR.
3. **Sweep four→three** across `ose-public`, then `ose-primer`, then `ose-private`. Three PRs,
   serialized on the `apps/rhino-cli` byte-identity boundary.
4. **Archive** the GitHub repository and reconcile the local checkout.

## Resolved Design Decisions (from grilling)

| ID  | Decision                                                                                                                       | Rationale                                                                                                                                                                                                                           |
| --- | ------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| D1  | **Selective file port, no git-history merge.** Copy `beaver-nest`-unique paths in as new files.                                | The two trees share a root commit but have both rewritten governance heavily since the fork; a real merge conflicts on essentially every governance file for history nobody will read. History stays readable in the archived repo. |
| D2  | **Carry product + vision + unique ideas only.** Discard the governance tree, the `rhino-cli` fork, and the 35 duplicate ideas. | `ose-public` is upstream and authoritative for all three surfaces, and is strictly ahead on each.                                                                                                                                   |
| D3  | **Single-token domain `beavernest`.** Apps become `beavernest-be`, `beavernest-app-web`, plus `-e2e` pairs.                    | `fe` is not a legal type suffix in [`file-naming.md`](../../../repo-governance/conventions/structure/file-naming.md); the single-token domain matches `ayokoding`, `organiclever`, and `wahidyankf`.                                |
| D4  | **Archive the GitHub repo, do not delete it.**                                                                                 | Keeps history, issues, and every inbound link resolving; reversible via `gh repo unarchive`. Deleting breaks links already published in this repo's docs and in past LinkedIn posts.                                                |

## Ordering Constraint

This plan is the **last of three**, executed in this order:

```text
sdlc-gate-registry-enforcement  →  optimize-cis  →  beaver-nest-repo-consolidation
```

All three touch `apps/rhino-cli`, and this plan must not start until **both** predecessors are
complete.

### `blockedBy` — `sdlc-gate-registry-enforcement`

[`plans/done/2026-08-07__sdlc-gate-registry-enforcement`](../../done/2026-08-07__sdlc-gate-registry-enforcement/README.md)
originally declared all four repos in scope, so it needed `beaver-nest` to still exist as a live,
writable repository — archiving first would have stranded its fourth track. That plan **amended its
scope on 2026-08-07** to `ose-public` and `ose-private` only, with `beaver-nest`'s Phase 5
cancelled precisely because this consolidation retires it. The ordering still holds, now for the
simpler reason that it owns `repo-config.yml`, the generated Husky shims, and the CI gate surface.

### `blockedBy` — `optimize-cis`

[`plans/in-progress/optimize-cis`](../../in-progress/optimize-cis/README.md) — successor to, and
supersedes, the `rhino-cli-optimization` idea this section originally named (deleted 2026-08-08,
absorbed into `optimize-cis`'s scope) — rewrites how `apps/rhino-cli` is built, invoked, and
lint-gated. It changes three things this plan's delivery checklist currently depends on, and **that
plan owns repairing every citation** — its Phase 2 carries explicit resolver-shim hand-off steps,
and its Phase 10 sweep (`grep -rn "cargo run --release --quiet --manifest-path apps/rhino-cli"`)
verifies every old-form command citation across the repo, including this doc, resolves:

| What changes                                                              | This plan's affected steps                                                                  |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `apps/rhino-cli/tests/gate_specs.rs` gains new RED-step integration tests | The parity-message TDD cycle's RED target and its `cargo test --test gate_specs` invocation |
| `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml`   | Four steps, including `repo-config validate` and `parity manifest generate`/`validate`      |
| `docs/reference/sdlc-gate-standard.md` invocation-form references         | Both plans edit this file for different reasons; `optimize-cis` lands first                 |

**Do not pre-emptively rewrite these steps.** Re-derive them against `apps/rhino-cli`'s actual
post-optimization state at Phase 0, since `optimize-cis`'s own phases may change the shape of the
resolver it introduces from what is described here.

Note this supersedes an earlier nuance: the predecessor plan (`rhino-cli-optimization`) scoped its
own continuous byte-identity enforcement to only two of the three repos named in `parity.rs`'s
message, with `ose-primer` named but synced manually on a delay rather than continuously enforced.
`optimize-cis` closes that gap — its own Phase 10 gate requires `parity manifest validate` to exit 0
with an identical hash in **all three** repos (`ose-public`, `ose-primer`, `ose-private`) before its
PRs merge, matching this plan's four→three `parity.rs` message rather than merely coexisting with
it. Re-verify this at Phase 0 rather than assume it, since it is `optimize-cis`'s current design,
not yet its landed state as of this writing.

## Worktree and Delivery Mode

Worktree path: `worktrees/beaver-nest-repo-consolidation/` (one per repo, at the same relative path
inside each of the three surviving repos' trees). Delivery Mode: **`worktree-to-pr`** — the repo
default, and required here because the change set includes F#, TypeScript, Rust, and generated
mirror files, which the `main-to-origin-main` `.md`-only restriction excludes.

Full declarations in [delivery.md](./delivery.md).

## Related Documentation

- [brd.md](./brd.md) — business rationale, current-state baseline, success metrics, risks
- [prd.md](./prd.md) — user stories and Gherkin acceptance criteria
- [tech-docs.md](./tech-docs.md) — architecture, design decisions, file-impact analysis, rollback
- [delivery.md](./delivery.md) — phased delivery checklist with gates
- [learnings.md](./learnings.md) — Knowledge Capture running log
- [Related Repositories](../../../docs/reference/related-repositories.md) — the four-repo definition this plan rewrites
- [Plans Organization Convention](../../../repo-governance/conventions/structure/plans.md)
- [PR Merge Protocol](../../../repo-governance/development/workflow/pr-merge-protocol.md)
