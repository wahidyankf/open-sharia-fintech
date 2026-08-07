---
title: "Delivery: BeaverNest Repository Consolidation"
description: Phased delivery checklist with gates for folding beaver-nest into ose-public and archiving the fourth repository
category: explanation
subcategory: plans
tags:
  - governance
  - cross-repo
  - consolidation
created: 2026-08-06
---

# Delivery Checklist: BeaverNest Repository Consolidation

This plan ports the BeaverNest product into `ose-public`, sweeps four-repo terminology to three
across the three surviving repos, and archives `beaver-nest`. Phases 0-4 execute in `ose-public`;
Phases 6-7 execute in `ose-primer` and `ose-private` respectively; Phase 8 executes against
`beaver-nest` itself. The plan folder lives only in `ose-public`.

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.

## Blocking Preconditions

This plan is the **last of three**:
`sdlc-gate-registry-enforcement` → `rhino-cli-optimization` → this plan. Both predecessors must be
archived before Phase 0 begins. See
[README.md §Ordering Constraint](./README.md#ordering-constraint) for why each blocks.

- [ ] [AI] Verify [`plans/done/2026-08-07__sdlc-gate-registry-enforcement`](../../done/2026-08-07__sdlc-gate-registry-enforcement/README.md)
      has completed — command: `test -d plans/done/*__sdlc-gate-registry-enforcement && echo COMPLETE`
      — acceptance: prints `COMPLETE`; if the folder is still under `plans/in-progress/`, **stop and
      do not begin Phase 0** (see [tech-docs.md D5](./tech-docs.md#design-decisions))
- [ ] [AI] Verify [`plans/backlog/rhino-cli-optimization`](../rhino-cli-optimization/README.md) has
      completed — command: `test -d plans/done/*__rhino-cli-optimization && echo COMPLETE` —
      acceptance: prints `COMPLETE`; if the folder is still under `plans/backlog/` or
      `plans/in-progress/`, **stop and do not begin Phase 0**
- [ ] [AI] Re-derive this checklist's `apps/rhino-cli` citations against the post-optimization tree,
      because that plan consolidates the integration-test binaries and replaces the
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml` invocation form. Its Phase 2
      and Phase 3 own repairing every citation here, and its Phase 12 gate verifies them — so this
      step is a **confirmation**, not a rewrite. Command:
      `grep -rn 'gate_specs\|cargo run --release' plans/backlog/beaver-nest-repo-consolidation/` —
      acceptance: every match names a path that exists and a command that runs

- [ ] [AI] Confirm the parity message's **three-repo** membership claim is still correct and has not
      been conflated with the **two-repo** continuously-enforced boundary. `ose-primer` is named in
      the message and synced manually on a delay; enforcement covers `ose-public` and `ose-private`
      only, per commit `a0383faed`. Both statements are true simultaneously — acceptance: the
      four→three sweep below changes membership wording only, and touches no enforcement scope

## Worktree

One worktree per repo, at the same relative path inside each repo's own working tree:

| Repo          | Worktree path (absolute)                                                        |
| ------------- | ------------------------------------------------------------------------------- |
| `ose-public`  | `/Users/wkf/ose-projects/ose-public/worktrees/beaver-nest-repo-consolidation/`  |
| `ose-primer`  | `/Users/wkf/ose-projects/ose-primer/worktrees/beaver-nest-repo-consolidation/`  |
| `ose-private` | `/Users/wkf/ose-projects/ose-private/worktrees/beaver-nest-repo-consolidation/` |

Optional manual pre-provisioning (run from each repo's own root):

```bash
claude --worktree beaver-nest-repo-consolidation
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest
`origin/main` when missing, syncs with `origin/main` before implementing, and prompts before deleting
the worktree after the plan is archived and pushed.

**Cross-repo execution note**: `plan-execution.md`'s Step 0 worktree gate provisions in the _current_
repo only. Phases 6 and 7 execute in a different repo than the one holding this plan folder, so each
requires `cd /Users/wkf/ose-projects/<repo>` first. `ose-primer` and `ose-private`'s topology (bare
repo with linked worktrees, vs. a normal working tree) is not assumed here and drifts over time —
verify it live with `git -C <repo> rev-parse --is-bare-repository` before choosing a git method there.

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans.md#worktree-specification).

## Delivery Mode: worktree-to-pr

The repo default, and required here: the change set includes F#, TypeScript, Rust, YAML, and
generated mirror files, which the `main-to-origin-main` `.md`-only restriction excludes.

Phase 0 opens no PR under this or any mode. Phases 1-2 are non-boundary phases committing to Unit 1's
branch. Phases 3, 4, 5, 6, and 7 each close a delivery unit and open exactly one PR. Phase 8 produces
changes only in `beaver-nest` — a markdown-only README edit pushed directly to that repo immediately
before it is archived — so it opens no `ose-public` PR.

**Archival-in-PR applies to `ose-public` only.** `ose-primer` and `ose-private` carry no `plans/`
entry for this work, so their PRs contain no plan-folder content. This is the ordinary cross-repo
carve-out from the
[Archival-in-PR rule](../../../repo-governance/conventions/structure/plans.md#delivery-mode).

## Parallelization Model

**DAG**: one strictly serial spine. Every phase reads what the previous phase wrote:

- Phase 1 → 2: the rename operates on the files Phase 1 copied.
- Phase 2 → 3: the gates in Phase 3 verify the wiring Phase 2 authored.
- Phase 3 → 4: the idea triage in Phase 4 renames briefs to match the app names Phase 3 froze.
- Phase 4 → 5: the sweep asserts a three-repo family, which is only true once the product has landed.
- Phase 5 → 6 → 7: **byte-identity serialization**. All three repos must converge on the identical
  `apps/rhino-cli/src/application/parity.rs` content and a matching `parity-manifest.sha256`.
  [`multi-plans-execution.md:205`](../../../repo-governance/workflows/plan/multi-plans-execution.md)
  states this boundary "cannot tolerate two concurrent divergent edits", so these three are ordered,
  not parallel.
- Phase 7 → 8: archiving is safe only once no surviving repo still references the fourth.

**Chosen N = 1** — lowered from the [Agent Workflow Orchestration
Convention](../../../repo-governance/development/agents/agent-workflow-orchestration.md)'s default
N=3. This is not a capacity judgment: the DAG has **no independent nodes to fan out**. Every phase
is blocked by its predecessor, so additional background agents would idle. The main thread executes
the spine directly.

**Cleanup is the terminal node**: worktree removal in Phase 10 depends on every delivery node.

### Delivery Boundaries

| Phase(s) | Delivery unit                            | Worktree / branch                                         | PR opens                                 |
| -------- | ---------------------------------------- | --------------------------------------------------------- | ---------------------------------------- |
| 0        | — (setup and baseline)                   | —                                                         | no                                       |
| 1-3      | BeaverNest product ported and green      | `ose-public` · `beaver-nest-repo-consolidation-port`      | yes — at Phase 3                         |
| 4        | Vision, ideas, and app-setup disposition | `ose-public` · `beaver-nest-repo-consolidation-narrative` | yes — at Phase 4                         |
| 5        | Four→three sweep, `ose-public`           | `ose-public` · `beaver-nest-repo-consolidation-sweep`     | yes — at Phase 5                         |
| 6        | Four→three sweep, `ose-primer`           | `ose-primer` · `beaver-nest-repo-consolidation-sweep`     | yes — at Phase 6                         |
| 7        | Four→three sweep, `ose-private`          | `ose-private` · `beaver-nest-repo-consolidation-sweep`    | yes — at Phase 7                         |
| 8        | Repository retirement                    | `beaver-nest` · `main` (md-only direct push)              | no — direct push, then `gh repo archive` |
| 9        | Knowledge Capture                        | `ose-public` · local `main` (plan-docs-only carve-out)    | no                                       |
| 10       | Plan Archival and cleanup                | `ose-public` · local `main` (plan-docs-only carve-out)    | no                                       |

## Phase 0: Environment Setup and Baseline

Phase 0 changes nothing reviewable. It opens no PR, pushes no branch, runs no review cycle, merges
nothing, and has no CI run of its own. Its artifacts ride Phase 3's PR.

- [ ] [AI] Provision the `ose-public` worktree — command: `claude --worktree beaver-nest-repo-consolidation`
      — acceptance: `worktrees/beaver-nest-repo-consolidation/` exists and is on a branch off the latest `origin/main`
- [ ] [AI] Initialize the toolchain in the **root** worktree, not the new one — command: `npm install && npm run doctor -- --fix`
      — acceptance: `npm run doctor` exits 0 with no missing-tool findings
- [ ] [AI] Create the Knowledge Capture scaffold at `plans/backlog/beaver-nest-repo-consolidation/learnings.md`
      — acceptance: file exists and its first heading is `# Learnings: beaver-nest-repo-consolidation`
- [ ] [AI] Record the `beaver-nest` working-tree state per [D9](./tech-docs.md#design-decisions) — command: `git -C /Users/wkf/ose-projects/beaver-nest status --porcelain > evidence/phase-0-beaver-nest-status.txt`
      — acceptance: the file is written; if any listed path falls outside the governance files this plan discards, stop and triage it before copying anything
- [ ] [AI] Enumerate the exact source path set — command: `git -C /Users/wkf/ose-projects/beaver-nest ls-files apps/beaver-nest-be apps/beaver-nest-fe apps/beaver-nest-be-e2e apps/beaver-nest-fe-e2e specs/apps/beaver-nest infra/dev/beaver-nest-app > evidence/phase-0-source-manifest.txt`
      — acceptance: the manifest is non-empty and its line count is recorded in the file-touch ledger
- [ ] [AI] Freeze a **fresh** unique-idea-brief manifest — the generic half of this set is volatile
      (both repos' `plans/ideas/` trees are under active cross-repo grooming, so the names and count
      cited in [tech-docs.md §More Detail](./tech-docs.md#more-detail) are a stale 2026-08-06
      snapshot, not an execution input)
      — command: `git -C /Users/wkf/ose-projects/beaver-nest fetch origin && comm -13 <(find plans/ideas -name '*.md' ! -name README.md -exec basename {} \; | sort -u) <(git -C /Users/wkf/ose-projects/beaver-nest ls-tree -r --name-only origin/main -- plans/ideas | grep '\.md$' | xargs -n1 basename | grep -v '^README.md$' | sort -u) > evidence/phase-0-unique-ideas-manifest.txt`
      — note: read `origin/main` with `ls-tree`, **never** `ls-files` — `ls-files` reads the local
      index, so a lagging clone would silently reproduce a stale manifest that the `diff` check in
      Phase 4 would then pass
      — acceptance: the manifest is written and lists every `beaver-nest` brief with no
      same-named counterpart in `ose-public`; the four `beaver-nest-*` product briefs appear in it
      (they exist nowhere else), and its line count is recorded in the file-touch ledger as the
      authoritative count Phase 4 triages — superseding the number 8 wherever this plan states it
- [ ] [AI] Record the pre-change baseline test run — command: `npx nx run-many -t test:quick --all > evidence/phase-0-baseline.txt 2>&1; echo "exit=$?" >> evidence/phase-0-baseline.txt`
      — acceptance: the file records the exit status; any preexisting failure is fixed before Phase 1 per Root Cause Orientation
- [ ] [AI] Record the pre-sweep four-repo reference count — command: `grep -rc 'beaver-nest' AGENTS.md README.md docs/reference repo-governance .claude apps/rhino-cli/src > evidence/phase-0-sweep-baseline.txt`
      — acceptance: the file is written and is the falsifiable "before" for Phase 5's zero-match gate

### Phase 0 Gate

> All checks below must pass before starting Phase 1. If any check fails, fix it in Phase 0 before
> proceeding.

- [ ] [AI] `npx nx run-many -t test:quick --all` — acceptance: exits 0 with zero failures
- [ ] [AI] `git status --porcelain` in the worktree — acceptance: only the five `evidence/` files written above (`phase-0-beaver-nest-status.txt`, `phase-0-source-manifest.txt`, `phase-0-unique-ideas-manifest.txt`, `phase-0-baseline.txt`, `phase-0-sweep-baseline.txt`) and `learnings.md` appear
- [ ] [AI] `test -s evidence/phase-0-source-manifest.txt && test -s evidence/phase-0-unique-ideas-manifest.txt` — acceptance: exits 0

> **Pause Safety**: a clean baseline is recorded and the source manifest is frozen. No product file
> has been copied and no repository has been modified. Safe to stop.
> To resume: `npx nx run-many -t test:quick --all`.

## Phase 1: Copy the Product Source (non-boundary)

Pure file creation — no Red→Green→Refactor required per the TDD convention's non-code carve-out.
Copies preserve content verbatim; the rename happens in Phase 2.

- [ ] [AI] Copy `apps/beaver-nest-be/` to `apps/beavernest-be/` — command: `cp -R /Users/wkf/ose-projects/beaver-nest/apps/beaver-nest-be apps/beavernest-be`
      — acceptance: `git status --porcelain apps/beavernest-be | grep -c .` matches the manifest's `apps/beaver-nest-be` line count
  - _Suggested executor: `swe-fsharp-dev`_
- [ ] [AI] Copy `apps/beaver-nest-fe/` to `apps/beavernest-app-web/` — command: `cp -R /Users/wkf/ose-projects/beaver-nest/apps/beaver-nest-fe apps/beavernest-app-web`
      — acceptance: `apps/beavernest-app-web/src/App.tsx` exists
  - _Suggested executor: `swe-typescript-dev`_
- [ ] [AI] Delete the stale Next.js artifact — command: `rm apps/beavernest-app-web/next-env.d.ts`
      — acceptance: `test ! -e apps/beavernest-app-web/next-env.d.ts` exits 0
- [ ] [AI] Copy `apps/beaver-nest-be-e2e/` to `apps/beavernest-be-e2e/` — command: `cp -R /Users/wkf/ose-projects/beaver-nest/apps/beaver-nest-be-e2e apps/beavernest-be-e2e`
      — acceptance: `apps/beavernest-be-e2e/steps/` contains 5 step files
  - _Suggested executor: `swe-e2e-dev`_
- [ ] [AI] Copy `apps/beaver-nest-fe-e2e/` to `apps/beavernest-app-web-e2e/` — command: `cp -R /Users/wkf/ose-projects/beaver-nest/apps/beaver-nest-fe-e2e apps/beavernest-app-web-e2e`
      — acceptance: `apps/beavernest-app-web-e2e/playwright.viewport.config.ts` exists
  - _Suggested executor: `swe-e2e-dev`_
- [ ] [AI] Copy the specs tree to `specs/apps/beavernest/` — command: `cp -R /Users/wkf/ose-projects/beaver-nest/specs/apps/beaver-nest specs/apps/beavernest`
      — acceptance: `find specs/apps/beavernest -name '*.feature' | grep -c .` prints `19`
- [ ] [AI] Copy the compose stack to `infra/dev/beavernest-app/` — command: `cp -R /Users/wkf/ose-projects/beaver-nest/infra/dev/beaver-nest-app infra/dev/beavernest-app`
      — acceptance: `infra/dev/beavernest-app/docker-compose.yml` exists and `infra/dev/beavernest-app/tests/` holds 16 shell tests
- [ ] [AI] Copy the brand token sheet — command: `cp /Users/wkf/ose-projects/beaver-nest/libs/web-ui-token/src/beaver-nest.css libs/web-ui-token/src/beavernest.css`
      — acceptance: `libs/web-ui-token/src/beavernest.css` exists and the four existing brand sheets are unmodified
- [ ] [AI] Copy the staging CI caller — command: `cp /Users/wkf/ose-projects/beaver-nest/.github/workflows/beaver-nest-app-test-local-deploy-stag.yml .github/workflows/beavernest-app-test-local-deploy-stag.yml`
      — acceptance: the new workflow file exists; no other workflow file is added or removed
- [ ] [AI] Confirm nothing outside the manifest was copied — command: `git status --porcelain | grep -v -e '^?? apps/beavernest' -e '^?? specs/apps/beavernest' -e '^?? infra/dev/beavernest' -e '^?? libs/web-ui-token/src/beavernest.css' -e '^?? .github/workflows/beavernest' -e '^?? evidence/' -e 'learnings.md'`
      — acceptance: prints nothing

### Phase 1 Gate

> All checks below must pass before starting Phase 2. If any check fails, fix it in Phase 1 before
> proceeding.

- [ ] [AI] `find apps/beavernest-be apps/beavernest-app-web apps/beavernest-be-e2e apps/beavernest-app-web-e2e -type f | grep -c .` — acceptance: total matches the manifest's app line count minus the one deleted `next-env.d.ts`
- [ ] [AI] `git -C /Users/wkf/ose-projects/beaver-nest status --porcelain` — acceptance: byte-identical to `evidence/phase-0-beaver-nest-status.txt`, proving the source repo was only read
- [ ] [AI] `npx nx run-many -t test:quick --all` — acceptance: exits 0; the copied trees are not yet registered as Nx projects, so existing projects must be unaffected

> **Pause Safety**: the product files exist in `ose-public` under their new paths but are not yet
> registered with Nx, renamed, or wired into any gate. They are inert — the workspace behaves exactly
> as it did at Phase 0. `beaver-nest` is unmodified. Safe to stop.
> To resume: `npx nx run-many -t test:quick --all`.

## Phase 2: Rename to the `beavernest` Domain and Wire the Workspace (non-boundary)

The identifier rename touches production F# and TypeScript source, so it runs as a Red→Green→Refactor
cycle driven by the ported tests. Configuration and index edits are direct actions.

### TDD cycle: `beavernest` identifier rename

- [ ] [AI] **RED**: Register the four copied projects with Nx by setting each `project.json`'s `name`
      to its new value (`beavernest-be`, `beavernest-app-web`, `beavernest-be-e2e`,
      `beavernest-app-web-e2e`) while leaving every internal identifier at its old `beaver-nest` value
      — command: `npx nx run beavernest-be:test:unit`
      — acceptance: the run **fails**, because F# namespaces, `implicitDependencies`, and spec paths
      still name `beaver-nest-*` projects that no longer exist
  - _Suggested executor: `swe-fsharp-dev`_
- [ ] [AI] **GREEN**: Complete the identifier rename across the four apps — F# namespaces and
      `.fsproj` names under `apps/beavernest-be/`, `implicitDependencies` in all four `project.json`
      files, the `beaver-nest-contracts` project name in
      `specs/apps/beavernest/containers/contracts/project.json` (to `beavernest-contracts`), spec
      paths in every `specs:*` target, script paths in `apps/beavernest-be/scripts/`, and env-var
      prefixes `BEAVER_NEST_BE_*` → `BEAVERNEST_BE_*` in `.env.example`, Dockerfiles, and the compose
      files under `infra/dev/beavernest-app/`
      — command: `npx nx run-many -t test:unit -p beavernest-be,beavernest-app-web`
      — acceptance: both projects' unit suites pass — 51 xUnit facts/theories and 9 Vitest cases —
      with no test skipped, narrowed, or deleted
  - _Suggested executor: `swe-fsharp-dev`_
- [ ] [AI] **REFACTOR**: Remove the residual `beaver-nest` spelling from the ported trees and correct
      the ported README's claim of a nonexistent `specs:coverage` target in `apps/beavernest-be/README.md`
      — command: `grep -rn 'beaver-nest' apps/beavernest-be apps/beavernest-app-web apps/beavernest-be-e2e apps/beavernest-app-web-e2e specs/apps/beavernest infra/dev/beavernest-app`
      — acceptance: returns zero matches, and `npx nx run-many -t test:unit -p beavernest-be,beavernest-app-web` still passes

### Workspace wiring (non-code, direct actions)

- [ ] [AI] Add the three BeaverNestBe F# projects to `open-sharia-enterprise.sln` — command: `dotnet sln open-sharia-enterprise.sln add apps/beavernest-be/src/BeaverNestBe/BeaverNestBe.fsproj apps/beavernest-be/tests/unit/BeaverNestBe.UnitTests.fsproj apps/beavernest-be/tests/integration/BeaverNestBe.IntegrationTests.fsproj`
      — acceptance: `dotnet sln open-sharia-enterprise.sln list` includes all three; `beaver-nest.sln` is **not** created
- [ ] [AI] Register the two apps in `repo-config.yml` under `coverage.projects` and
      `env-contract.surfaces` (allowlisting the renamed `BEAVERNEST_BE_*` variables), following the
      shape of the existing `ose-be` entries
      — command: `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- repo-config validate`
      — acceptance: exits 0
- [ ] [AI] Add the `beavernest:dev` script to root `package.json`, mirroring the existing per-app dev
      scripts — command: `npm run beavernest:dev -- --help || true; jq -e '.scripts["beavernest:dev"]' package.json`
      — acceptance: `jq` exits 0
- [ ] [AI] Rename the workflow's internal job and image references from `beaver-nest` to `beavernest`
      in `.github/workflows/beavernest-app-test-local-deploy-stag.yml`, and index it in
      `.github/workflows/README.md`
      — command: `actionlint .github/workflows/beavernest-app-test-local-deploy-stag.yml`
      — acceptance: exits 0 with no findings
- [ ] [AI] Add the two apps to `apps/README.md`, `docs/reference/monorepo-structure.md`,
      `docs/reference/system-architecture/applications.md`, and the Web Sites table in `AGENTS.md`
      (ports 19300 runtime / 19310 frontend dev / 19320 backend dev, no production branch)
      — command: `grep -c 'beavernest-be' AGENTS.md apps/README.md docs/reference/monorepo-structure.md docs/reference/system-architecture/applications.md`
      — acceptance: every file reports at least 1
- [ ] [AI] Create `.claude/agents/apps-beavernest-be-deployer.md` and
      `.claude/agents/apps-beavernest-app-web-deployer.md` by adapting the ported `beaver-nest`
      deployer definitions to this repo's agent conventions, and catalog both in `.claude/agents/README.md`
      — command: `test -f .claude/agents/apps-beavernest-be-deployer.md && test -f .claude/agents/apps-beavernest-app-web-deployer.md`
      — acceptance: exits 0
  - _Suggested executor: `agent-maker`_
- [ ] [AI] Regenerate the harness mirrors — command: `npm run generate:bindings && npm run validate:sync`
      — acceptance: `validate:sync` exits 0; `.opencode/`, `.cursor/`, and `.amazonq/` changes are staged in the **same** commit as their `.claude/` source

### Phase 2 Gate

> All checks below must pass before starting Phase 3. If any check fails, fix it in Phase 2 before
> proceeding.

- [ ] [AI] `npx nx show projects --json | jq -e 'index("beavernest-be") and index("beavernest-app-web") and index("beavernest-be-e2e") and index("beavernest-app-web-e2e")'` — acceptance: exits 0
- [ ] [AI] `npx nx show projects --json | jq -e 'map(select(test("beaver-nest"))) | length == 0'` — acceptance: exits 0
- [ ] [AI] `grep -rn 'beaver-nest-fe' apps libs specs infra .github .claude repo-config.yml` — acceptance: zero matches
- [ ] [AI] `npm run validate:sync` — acceptance: exits 0
- [ ] [AI] `npx nx run-many -t typecheck lint -p beavernest-be,beavernest-app-web,beavernest-be-e2e,beavernest-app-web-e2e` — acceptance: exits 0

> **Pause Safety**: the four projects are registered, renamed, and lint/typecheck-clean, and the
> harness mirrors are regenerated in sync. Tests and specs gates are not yet proven, so this is not
> yet a shippable increment — no PR opens here. `beaver-nest` is still unmodified. Safe to stop.
> To resume: `npx nx run-many -t typecheck lint -p beavernest-be,beavernest-app-web`.

## Phase 3: Prove the Ported Product Green (delivery boundary — PR #1)

- [ ] [AI] Resolve any `libs/web-ui` incompatibility surfaced by the ported frontend, per
      [D6](./tech-docs.md#design-decisions) — the app consumes `ose-public`'s `web-ui`, never
      `beaver-nest`'s divergent copy
      — command: `npx nx run beavernest-app-web:test:unit`
      — acceptance: exits 0; if the failure is a Storybook-framework or Vite-plugin version mismatch,
      pin the app's own dependency rather than modifying `libs/web-ui`, and record the pin in `learnings.md`
  - _Suggested executor: `swe-typescript-dev`_
- [ ] [AI] Verify the specs gate counts the ported features — command: `npx nx run-many -t specs:coverage -p beavernest-be,beavernest-app-web`
      — acceptance: exits 0 and the output attributes 19 feature files to the `beavernest` spec area rather than reporting it empty
- [ ] [AI] Start the compose stack — command: `docker compose -f infra/dev/beavernest-app/docker-compose.yml up -d`
      — acceptance: `docker compose -f infra/dev/beavernest-app/docker-compose.yml ps` reports the app service healthy
- [ ] [AI] Capture runtime evidence for the readiness endpoint — command: `curl -sS -i http://127.0.0.1:19300/api/v1/readiness > evidence/phase-3-readiness.txt`
      — acceptance: the file's status line is `HTTP/1.1 200` and its body contains `"status":"ready"`
- [ ] [AI] Capture runtime evidence for the health endpoint — command: `curl -sS -i http://127.0.0.1:19300/api/v1/health > evidence/phase-3-health.txt`
      — acceptance: the file's status line is `HTTP/1.1 200` and its body contains `"status":"ok"`
- [ ] [AI] Run both ported E2E suites — command: `npx nx run-many -t test:e2e -p beavernest-be-e2e,beavernest-app-web-e2e`
      — acceptance: exits 0; the 15 backend and 4 frontend BDD specs pass

### Manual UI Verification (Playwright MCP) — single screen, single locale

The ported `beavernest-app-web` renders against `ose-public`'s `libs/web-ui` for the first time
([D6](./tech-docs.md#design-decisions)), and `tech-docs.md`'s Product-Level Risks table flags a
MEDIUM risk that it breaks against the older library version. Automated unit and E2E tests can pass
against a component tree that mounts but renders visually wrong, so this step is the only visual
proof in the plan. The app is single-screen and single-locale, so no locale matrix applies — run
with the compose stack from the steps above still running.

- [ ] [AI] Navigate to the running app — command: `browser_navigate` to `http://127.0.0.1:19310`
      — acceptance: `browser_navigate` returns without error
- [ ] [AI] Inspect the DOM — command: `browser_snapshot`
      — acceptance: the snapshot shows the `ReadinessPanel` component with visible, non-empty text
      content — not a blank page or an error boundary
- [ ] [AI] Check for JS errors — command: `browser_console_messages`
      — acceptance: zero `error`-level console messages
- [ ] [AI] Capture the mobile viewport — command: `browser_resize` to 375x812, then
      `browser_take_screenshot` saved to `evidence/phase-3-beavernest-app-web-mobile-375px.png`
      — acceptance: the file exists and is non-empty
- [ ] [AI] Capture the tablet viewport — command: `browser_resize` to 768x1024, then
      `browser_take_screenshot` saved to `evidence/phase-3-beavernest-app-web-tablet-768px.png`
      — acceptance: the file exists and is non-empty
- [ ] [AI] Capture the desktop viewport — command: `browser_resize` to 1280x800, then
      `browser_take_screenshot` saved to `evidence/phase-3-beavernest-app-web-desktop-1280px.png`
      — acceptance: the file exists and is non-empty
- [ ] [AI] Document the three screenshots in this checklist — embed each with
      `![BeaverNest app-web readiness screen, <viewport> viewport](./evidence/phase-3-beavernest-app-web-<viewport>-<width>px.png)`,
      each carrying alt text naming its viewport
      — command: `grep -c 'evidence/phase-3-beavernest-app-web-.*px.png)' delivery.md`
      — acceptance: prints `3` — one embed per viewport — and every referenced file exists on disk
- [ ] [AI] Stop the compose stack — command: `docker compose -f infra/dev/beavernest-app/docker-compose.yml down`
      — acceptance: `docker compose -f infra/dev/beavernest-app/docker-compose.yml ps` lists no running service

### Local Quality Gates (Before Push)

- [ ] [AI] Run affected typecheck: `npx nx affected -t typecheck`
- [ ] [AI] Run affected linting: `npx nx affected -t lint`
- [ ] [AI] Run affected quick tests: `npx nx affected -t test:quick`
- [ ] [AI] Run affected spec coverage: `npx nx affected -t specs:coverage`
- [ ] [AI] Fix ALL failures found during quality gates, not just those caused by your changes
- [ ] [AI] Verify all checks pass before pushing

### Commit Guidelines (Phase 3)

- [ ] [AI] Commit changes thematically — group related changes into logically cohesive commits
- [ ] [AI] Follow Conventional Commits format: `<type>(<scope>): <description>`, imperative mood, no trailing period
- [ ] [AI] Split different domains/concerns into separate commits — suggested split:
      `feat(beavernest-be): port BeaverNest backend into ose-public`,
      `feat(beavernest-app-web): port BeaverNest frontend into ose-public`,
      `test(beavernest): port BeaverNest e2e suites and specs`,
      `chore(config): register BeaverNest projects in repo-config and solution`,
      `chore(ci): add BeaverNest staging workflow caller`
- [ ] [AI] Do NOT bundle unrelated fixes into a single commit
- [ ] [AI] Commit and push to origin `beaver-nest-repo-consolidation-port`
- [ ] [AI] Open the draft PR — command: `gh pr create --draft --title 'feat(beavernest): port BeaverNest product into ose-public' --body-file /dev/stdin`
      — acceptance: `gh pr view --json isDraft` reports `true`

### Post-Push Verification

- [ ] [AI] Monitor the PR's GitHub Actions check run per the [CI Monitoring Convention](../../../repo-governance/development/workflow/ci-monitoring.md) — `ScheduleWakeup(120s)`, then on each wakeup a single `gh pr checks --json bucket,name,state --jq '[.[] | select(.bucket != "pass")]'` (never `gh pr checks --watch` or `gh run watch`) — repeat until the filtered output is `[]`
- [ ] [AI] Verify all CI checks pass
- [ ] [AI] If any CI check fails, fix immediately and push a follow-up commit
- [ ] [AI] Do NOT proceed to the next delivery phase until CI is green

### Phase 3 Gate

> All checks below must pass before starting Phase 4. If any check fails, fix it in Phase 3 before
> proceeding.

- [ ] [AI] `npx nx run-many -t test:quick -p beavernest-be,beavernest-app-web,beavernest-be-e2e,beavernest-app-web-e2e` — acceptance: exits 0
- [ ] [AI] `grep -c 'HTTP/1.1 200' evidence/phase-3-readiness.txt evidence/phase-3-health.txt` — acceptance: each file reports 1
- [ ] [AI] `ls evidence/phase-3-beavernest-app-web-mobile-375px.png evidence/phase-3-beavernest-app-web-tablet-768px.png evidence/phase-3-beavernest-app-web-desktop-1280px.png` — acceptance: all three screenshot files exist
- [ ] [AI] Run the PR-Review Maker→Fixer Cycle — acceptance: 3 sequential CI-gated cycles complete, the loop did not exit `escalated`, and every inline comment has a reply
- [ ] [AI] `gh pr ready` then merge — acceptance: all five [PR Merge Protocol](../../../repo-governance/development/workflow/pr-merge-protocol.md) preconditions (a)-(e) hold and the PR is merged by `[AI]`
- [ ] [AI] Fast-forward local `main` after the merge — command: `git -C /Users/wkf/ose-projects/ose-public checkout main && git pull --ff-only`
      — acceptance: `git status -sb` shows no divergence from `origin/main`

> **Pause Safety**: the BeaverNest product is merged into `ose-public` `main`, registered, green, and
> runtime-verified. `beaver-nest` still exists, unmodified, and every document still describes a
> four-repo family — internally consistent, because the sweep has not begun. Safe to stop.
> To resume: `npx nx run-many -t test:quick -p beavernest-be,beavernest-app-web`.

## Phase 4: Vision, Ideas, and App-Setup Disposition (delivery boundary — PR #2)

All steps are documentation actions — no Red→Green→Refactor required.

- [ ] [AI] Provision a fresh worktree for this unit — command: `git fetch origin && git worktree add -b beaver-nest-repo-consolidation-narrative worktrees/beaver-nest-repo-consolidation origin/main`
      (or re-provision via `claude --worktree beaver-nest-repo-consolidation`, removing the Unit 1 worktree first)
      — command: `git -C worktrees/beaver-nest-repo-consolidation merge-base --is-ancestor origin/main HEAD && git -C worktrees/beaver-nest-repo-consolidation rev-parse --abbrev-ref HEAD`
      — acceptance: the first command exits 0 (the branch contains the post-Phase-3 `origin/main`) and the second prints `beaver-nest-repo-consolidation-narrative`
- [ ] [AI] Port the product vision to `repo-governance/vision/beavernest.md`, renaming every
      `beaver-nest` identifier to `beavernest` and repointing app references to the new names
      — command: `grep -c 'beaver-nest' repo-governance/vision/beavernest.md`
      — acceptance: prints `0`
  - _Suggested executor: `repo-rules-maker`_
- [ ] [AI] Register the child vision in `repo-governance/vision/README.md` alongside the parent
      ecosystem vision, following the parent/child section shape the source repo used
      — command: `grep -c 'beavernest.md' repo-governance/vision/README.md`
      — acceptance: prints at least 1, and the existing link to `open-sharia-enterprise.md` is intact
- [ ] [AI] Re-read `plans/ideas/README.md` and re-derive the tree's current shape before triaging —
      the folder is being reorganized into Eisenhower quadrant subfolders
      (`q1-urgent-important/` … `q4-not-urgent-not-important/`), so briefs are addressed by **name**,
      not by a fixed path, and each newly filed brief must land in the correct quadrant
      — command: `find plans/ideas -mindepth 1 -maxdepth 1 -type d`
      — acceptance: the quadrant set in effect at execution time is recorded in `learnings.md`
- [ ] [AI] Re-freeze the unique-brief manifest against **current** `origin/main` in both repos before
      triaging — Phase 0's `evidence/phase-0-unique-ideas-manifest.txt` may itself have gone stale
      while Phases 1-3 ran, since both trees are under active grooming
      — command: `git -C /Users/wkf/ose-projects/beaver-nest fetch origin && comm -13 <(find plans/ideas -name '*.md' ! -name README.md -exec basename {} \; | sort -u) <(git -C /Users/wkf/ose-projects/beaver-nest ls-tree -r --name-only origin/main -- plans/ideas | grep '\.md$' | xargs -n1 basename | grep -v '^README.md$' | sort -u) > evidence/phase-4-unique-ideas-manifest.txt; diff evidence/phase-0-unique-ideas-manifest.txt evidence/phase-4-unique-ideas-manifest.txt`
      — acceptance: both manifests exist; if `diff` reports any change, the Phase 4 manifest wins and
      the delta is written into `learnings.md` with a one-line reason per added or removed brief
- [ ] [AI] Triage **every brief on `evidence/phase-4-unique-ideas-manifest.txt`** against
      `plans/ideas/README.md` and the existing briefs under Integrate-Before-You-Add, folding rather
      than duplicating where an existing brief covers the same problem. Do **not** use any brief name
      quoted elsewhere in this plan as the input set — those are a stale 2026-08-06 snapshot
      — command: `while read -r b; do echo "== $b"; grep -rl "${b%.md}" plans/ideas/ || echo "  no name-overlap"; done < evidence/phase-4-unique-ideas-manifest.txt`
      — acceptance: the number of recorded decisions in `learnings.md` equals
      `grep -c . evidence/phase-4-unique-ideas-manifest.txt`, and each decision is either a new
      distinctly-named file or a fold into a named existing brief
- [ ] [AI] Rename the four carried product briefs from `beaver-nest-*` to `beavernest-*` to match D3
      — command: `find plans/ideas -name 'beaver-nest-*.md' | grep -c .`
      — acceptance: prints `0`
- [ ] [AI] Run the Integrate-Before-You-Add scan on **both** D8 harvest candidates before filing
      either — the git-env scrub widening (`src/infrastructure/git/root.rs`, also clearing
      `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, `GIT_COMMON_DIR`) and the uppercase-root-file naming
      exemption (`src/application/docs/naming.rs`). The naming one is the live overlap risk:
      `sdlc-gate-registry-enforcement` (this plan's blocker) upstreams part of it in its own Step 3,
      and the existing brief `contributing-md-trunk-guidance-and-naming-exemption.md` in
      [`plans/ideas/`](../../ideas/README.md) already targets the same exempt-set mechanism (locate it
      by name — the `plans/ideas/` tree is being reorganized into quadrant subfolders)
      — command: `grep -rn 'naming.rs\|GIT_OBJECT_DIRECTORY\|exempt' plans/ideas/ && git log --oneline -20 -- apps/rhino-cli/src/application/docs/naming.rs apps/rhino-cli/src/infrastructure/git/root.rs`
      — acceptance: each candidate ends in exactly one of three recorded verdicts — **already
      upstreamed** (drop it), **folded** into a named existing brief, or **filed** as a new brief —
      and the verdict for each is written into `learnings.md`
- [ ] [AI] File only the candidates whose verdict was **filed**, named
      `rhino-cli-git-env-scrub-widening.md` and/or `rhino-cli-uppercase-root-file-naming-exemption.md`,
      each in the quadrant subfolder its priority warrants
      — command: `grep -c 'already upstreamed\|folded into\|filed as' learnings.md`
      — acceptance: prints `2` — one verdict per candidate — and every brief named **filed** exists,
      follows the two-pager format, and uses the relative depth its own location requires
- [ ] [AI] Index every added brief in `plans/ideas/README.md`
      — command: `find plans/ideas -name '*.md' ! -name README.md -exec basename {} \; | while read -r b; do grep -q "$b" plans/ideas/README.md || echo "MISSING $b"; done`
      — acceptance: prints nothing
- [ ] [AI] Carry the `beaver-nest-app-setup` plan folder into
      `plans/done/<merge-date>__beavernest-app-setup/`, and rewrite its `README.md` status line to
      **closed delivered-as-descoped**, naming what shipped (governance real-database rules, the
      SQLite + readiness backend, the Vite CSR migration) and what did not (Phase 6 runtime
      attestation, Phase 7 knowledge capture, Phase 8 archival, and the unsatisfiable Unit 3 PR)
      — command: `grep -c 'delivered-as-descoped' plans/done/*__beavernest-app-setup/README.md`
      — acceptance: prints at least 1
- [ ] [AI] Index the carried plan in `plans/done/README.md`
      — command: `grep -c 'beavernest-app-setup' plans/done/README.md`
      — acceptance: prints at least 1

### Local Quality Gates (Before Push)

- [ ] [AI] Run affected typecheck: `npx nx affected -t typecheck`
- [ ] [AI] Run affected linting: `npx nx affected -t lint`
- [ ] [AI] Run affected quick tests: `npx nx affected -t test:quick`
- [ ] [AI] Run affected spec coverage: `npx nx affected -t specs:coverage`
- [ ] [AI] Run the markdown gate: `npm run lint:md:fix`
- [ ] [AI] Fix ALL failures found during quality gates, not just those caused by your changes
- [ ] [AI] Verify all checks pass before pushing

### Commit Guidelines (Phase 4)

- [ ] [AI] Commit thematically — suggested split: `docs(governance): add BeaverNest product vision`,
      `docs(plans): carry BeaverNest idea briefs into ose-public`,
      `chore(plans): close beavernest-app-setup as delivered-as-descoped`
- [ ] [AI] Commit and push to origin `beaver-nest-repo-consolidation-narrative`
- [ ] [AI] Open the draft PR — acceptance: `gh pr view --json isDraft` reports `true`

### Post-Push Verification

- [ ] [AI] Monitor the PR's check run per the [CI Monitoring Convention](../../../repo-governance/development/workflow/ci-monitoring.md) — `ScheduleWakeup(120s)`, then a single `gh pr checks --json bucket,name,state --jq '[.[] | select(.bucket != "pass")]'` per wakeup (never `--watch`) — repeat until the filtered output is `[]`
- [ ] [AI] Verify all CI checks pass; fix and push a follow-up commit on any failure
- [ ] [AI] Do NOT proceed until CI is green

### Phase 4 Gate

> All checks below must pass before starting Phase 5. If any check fails, fix it in Phase 4 before
> proceeding.

- [ ] [AI] `grep -rn 'beaver-nest' repo-governance/vision/ plans/ideas/` — acceptance: zero matches
- [ ] [AI] `npm run lint:md:fix && git diff --exit-code` — acceptance: exits 0 (markdown already clean)
- [ ] [AI] Run the PR-Review Maker→Fixer Cycle — acceptance: 3 cycles complete, loop not `escalated`
- [ ] [AI] `gh pr ready` then merge — acceptance: preconditions (a)-(e) hold; merged by `[AI]`
- [ ] [AI] Fast-forward local `main` — command: `git checkout main && git pull --ff-only`
      — acceptance: no divergence from `origin/main`

> **Pause Safety**: the product, its vision, and its backlog all live in `ose-public`. `beaver-nest`
> is now fully redundant but still live and still referenced as the fourth family member — consistent,
> because the sweep has not begun. Safe to stop.
> To resume: `git -C /Users/wkf/ose-projects/ose-public log --oneline -5`.

## Phase 5: Four→Three Sweep in `ose-public` (delivery boundary — PR #3)

The `apps/rhino-cli` change touches production Rust and runs as a Red→Green→Refactor cycle. All
other steps are documentation edits.

- [ ] [AI] Provision a fresh worktree for this unit off the post-Phase-4 `origin/main`
      — command: `claude --worktree beaver-nest-repo-consolidation`
      — acceptance: the branch is `beaver-nest-repo-consolidation-sweep` off the latest `origin/main`
- [ ] [AI] Enumerate this repo's sweep targets — command: `grep -rln 'beaver-nest' AGENTS.md README.md docs repo-governance .claude apps/rhino-cli > evidence/phase-5-sweep-targets.txt`
      — acceptance: the file lists at least the 11 known targets and is recorded in the file-touch ledger

### TDD cycle: `rhino-cli` three-repo parity message

- [ ] [AI] **RED**: Update the parity-message assertion in `apps/rhino-cli/tests/gate_specs.rs` to
      expect a three-repo boundary, and add the companion scenario below to
      `specs/apps/rhino/behavior/rhino-cli/gherkin/gate/parity-manifest.feature`
      — command: `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_specs`
      — acceptance: the test **fails**, because `src/application/parity.rs` still emits the four-repo string
  - _Suggested executor: `swe-rust-dev`_

**Gherkin (binds) →** "Parity drift message names the three bound repositories" — _New scenario_

```gherkin
Scenario: Parity drift message names the three bound repositories
  Given a rhino-cli source file has drifted from the recorded parity manifest
  When the parity manifest validation reports the drift
  Then the message names ose-public, ose-primer, and ose-private
  And the message does not name beaver-nest
```

- [ ] [AI] **GREEN**: Change both four-repo strings in `apps/rhino-cli/src/application/parity.rs`
      (the drift message and the boundary description) to name exactly `ose-public`, `ose-primer`,
      and `ose-private`
      — command: `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_specs`
      — acceptance: passes, and no other `rhino-cli` test breaks
  - _Suggested executor: `swe-rust-dev`_
- [ ] [AI] **REFACTOR**: Regenerate the parity manifest and confirm no stale four-repo phrasing
      remains in the crate — command: `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- parity manifest generate && grep -rn 'and beaver-nest' apps/rhino-cli/src apps/rhino-cli/tests`
      — acceptance: `parity-manifest.sha256` is updated and the grep returns zero matches

### Governance and documentation sweep (non-code, direct actions)

- [ ] [AI] Rewrite `docs/reference/related-repositories.md` for a three-repository family — remove the
      fourth row, the "all four repos" terminology block, and the `beaver-nest` section; state that
      the family and the parity loop are now the same three-member set
      — command: `grep -c 'beaver-nest' docs/reference/related-repositories.md`
      — acceptance: prints `0`
  - _Suggested executor: `repo-rules-maker`_
- [ ] [AI] Fix the boundary contradiction in `docs/reference/sdlc-gate-standard.md` — the `rhino-cli`
      byte-identity boundary spans exactly three repositories
      — command: `grep -cE 'four (OSE |bound )?repos(itories)?' docs/reference/sdlc-gate-standard.md`
      — acceptance: prints `0` (deterministic — matches every repository-count phrasing this document
      uses (`four bound repos`, `four OSE repositories`) while excluding the unrelated "one of four
      controlled scope values" line, so a nonzero result is unambiguously a fail with no judgment
      call required)
- [ ] [AI] Update `AGENTS.md` §Related Repositories to name three repos and drop the `beaver-nest`
      fork carve-out sentence — command: `grep -c 'beaver-nest' AGENTS.md`
      — acceptance: prints `0`
- [ ] [AI] Update `README.md`'s sibling-repository list and `docs/reference/README.md`'s index line
      — command: `grep -c 'beaver-nest' README.md docs/reference/README.md`
      — acceptance: each prints `0`
- [ ] [AI] Update `repo-governance/development/practice/file-touch-discipline.md` to list three repos
      — command: `grep -c 'beaver-nest' repo-governance/development/practice/file-touch-discipline.md`
      — acceptance: prints `0`
- [ ] [AI] Update the three parity-planning workflows —
      `repo-governance/workflows/plan/multi-plans-execution.md`,
      `plan-multi-repo-parity-planning.md` (including its `default:` input value), and
      `plan-multi-repo-parity-planning-and-execution.md`
      — command: `grep -c 'beaver-nest' repo-governance/workflows/plan/multi-plans-execution.md repo-governance/workflows/plan/plan-multi-repo-parity-planning.md repo-governance/workflows/plan/plan-multi-repo-parity-planning-and-execution.md`
      — acceptance: each prints `0`
- [ ] [AI] Update `.claude/agents/social-linkedin-post-maker.md` to gather commits from three repos —
      its `description`, its post template, and its gather instruction
      — command: `grep -c 'beaver-nest' .claude/agents/social-linkedin-post-maker.md`
      — acceptance: prints `0`
  - _Suggested executor: `agent-maker`_
- [ ] [AI] Regenerate the harness mirrors — command: `npm run generate:bindings && npm run validate:sync`
      — acceptance: `validate:sync` exits 0; mirrors are staged in the same commit as their source

### Local Quality Gates (Before Push)

- [ ] [AI] Run affected typecheck: `npx nx affected -t typecheck`
- [ ] [AI] Run affected linting: `npx nx affected -t lint`
- [ ] [AI] Run affected quick tests: `npx nx affected -t test:quick`
- [ ] [AI] Run affected spec coverage: `npx nx affected -t specs:coverage`
- [ ] [AI] Fix ALL failures found during quality gates, not just those caused by your changes
- [ ] [AI] Verify all checks pass before pushing

### Commit Guidelines (Phase 5)

- [ ] [AI] Commit thematically — suggested split:
      `fix(rhino-cli): name three bound repos in the parity message`,
      `docs(reference): reduce the OSE family to three repositories`,
      `docs(repo-governance): drop beaver-nest from parity planning workflows`,
      `docs(agents): gather LinkedIn commits from three repos`
- [ ] [AI] Commit and push to origin `beaver-nest-repo-consolidation-sweep`
- [ ] [AI] Open the draft PR — acceptance: `gh pr view --json isDraft` reports `true`

### Post-Push Verification

- [ ] [AI] Monitor the PR's check run per the [CI Monitoring Convention](../../../repo-governance/development/workflow/ci-monitoring.md) — `ScheduleWakeup(120s)`, then a single `gh pr checks --json bucket,name,state --jq '[.[] | select(.bucket != "pass")]'` per wakeup (never `--watch`) — repeat until the filtered output is `[]`
- [ ] [AI] Verify all CI checks pass, including `rhino-cli-parity-audit.yml`
- [ ] [AI] If any CI check fails, fix immediately and push a follow-up commit
- [ ] [AI] Do NOT proceed until CI is green

### Phase 5 Gate

> All checks below must pass before starting Phase 6. If any check fails, fix it in Phase 5 before
> proceeding.

- [ ] [AI] `grep -rn 'beaver-nest' AGENTS.md README.md docs/reference repo-governance .claude apps/rhino-cli/src` — acceptance: zero matches
- [ ] [AI] `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- parity manifest validate` — acceptance: exits 0
- [ ] [AI] Run the PR-Review Maker→Fixer Cycle — acceptance: 3 cycles complete, loop not `escalated`
- [ ] [AI] `gh pr ready` then merge — acceptance: preconditions (a)-(e) hold; merged by `[AI]`
- [ ] [AI] Fast-forward local `main` — command: `git checkout main && git pull --ff-only`

> **Pause Safety**: `ose-public` describes a three-repository family and its `rhino-cli` emits the
> three-repo message. **The byte-identity boundary is now deliberately red** — `ose-primer` and
> `ose-private` still carry the old string. This is the intended detector, not a defect, and Phases 6
> and 7 close it. Do not leave the plan parked here for long.
> To resume: `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- parity manifest validate`.

## Phase 6: Four→Three Sweep in `ose-primer` (delivery boundary — PR #4)

Identical in substance to Phase 5, adapted to this repo's own footprint. `ose-primer` has no
`beavernest` product and no `plans/` entry for this plan.

- [ ] [AI] Change into the repo and verify topology — command: `cd /Users/wkf/ose-projects/ose-primer && git rev-parse --is-bare-repository`
      — acceptance: the output records whether the bare-repo git method applies (see [Bare Repo notes](../../../repo-governance/conventions/structure/worktree-path.md))
- [ ] [AI] Provision the worktree — command: `claude --worktree beaver-nest-repo-consolidation`
      — acceptance: the worktree exists off the latest `origin/main`
- [ ] [AI] Enumerate this repo's own sweep targets — command: `grep -rln 'beaver-nest' AGENTS.md README.md docs repo-governance .claude apps/rhino-cli > /tmp/primer-sweep-targets.txt`
      — acceptance: the list is non-empty and recorded in the file-touch ledger; a target absent here is a non-event, not a failed edit
- [ ] [AI] Apply the identical `apps/rhino-cli/src/application/parity.rs` and
      `apps/rhino-cli/tests/gate_specs.rs` content that merged in Phase 5
      — command: `diff <(git -C /Users/wkf/ose-projects/ose-public show main:apps/rhino-cli/src/application/parity.rs) apps/rhino-cli/src/application/parity.rs`
      — acceptance: prints nothing — the file is byte-identical to `ose-public`'s merged version
  - _Suggested executor: `swe-rust-dev`_
- [ ] [AI] Regenerate the parity manifest — command: `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- parity manifest generate`
      — acceptance: `parity-manifest.sha256` matches `ose-public`'s
- [ ] [AI] Apply the four→three edits to each enumerated governance and documentation target
      — command: `grep -rn 'beaver-nest' AGENTS.md README.md docs repo-governance .claude`
      — acceptance: zero matches outside `plans/done/**`
  - _Suggested executor: `repo-rules-maker`_
- [ ] [AI] Regenerate the harness mirrors — command: `npm run generate:bindings && npm run validate:sync`
      — acceptance: exits 0

### Local Quality Gates (Before Push)

- [ ] [AI] Run affected typecheck: `npx nx affected -t typecheck`
- [ ] [AI] Run affected linting: `npx nx affected -t lint`
- [ ] [AI] Run affected quick tests: `npx nx affected -t test:quick`
- [ ] [AI] Run affected spec coverage: `npx nx affected -t specs:coverage`
- [ ] [AI] Fix ALL failures found during quality gates, not just those caused by your changes
- [ ] [AI] Verify all checks pass before pushing

### Post-Push Verification

- [ ] [AI] Commit and push to origin `beaver-nest-repo-consolidation-sweep`, then open the draft PR
- [ ] [AI] Monitor the PR's check run per the [CI Monitoring Convention](../../../repo-governance/development/workflow/ci-monitoring.md) — `ScheduleWakeup(120s)`, then a single `gh pr checks --json bucket,name,state --jq '[.[] | select(.bucket != "pass")]'` per wakeup (never `--watch`) — repeat until the filtered output is `[]`
- [ ] [AI] Verify all CI checks pass; fix and push a follow-up commit on any failure
- [ ] [AI] Do NOT proceed until CI is green

### Phase 6 Gate

> All checks below must pass before starting Phase 7. If any check fails, fix it in Phase 6 before
> proceeding.

- [ ] [AI] `grep -rn 'beaver-nest' AGENTS.md README.md docs repo-governance .claude apps/rhino-cli/src` in `ose-primer` — acceptance: zero matches outside `plans/done/**`
- [ ] [AI] `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- parity manifest validate` — acceptance: exits 0
- [ ] [AI] Run the PR-Review Maker→Fixer Cycle — acceptance: 3 cycles complete, loop not `escalated`
- [ ] [AI] `gh pr ready` then merge — acceptance: preconditions (a)-(e) hold; merged by `[AI]`

> **Pause Safety**: two of three repos are swept and byte-identical. `ose-private` still carries the
> old string, so the boundary remains deliberately red. Safe to stop briefly.
> To resume: run the parity validate in each of `ose-public` and `ose-primer`.

## Phase 7: Four→Three Sweep in `ose-private` (delivery boundary — PR #5)

- [ ] [AI] Change into the repo and verify topology — command: `cd /Users/wkf/ose-projects/ose-private && git rev-parse --is-bare-repository`
      — acceptance: the output records whether the bare-repo git method applies
- [ ] [AI] Provision the worktree — command: `claude --worktree beaver-nest-repo-consolidation`
      — acceptance: the worktree exists off the latest `origin/main`
- [ ] [AI] Enumerate this repo's own sweep targets — command: `grep -rln 'beaver-nest' AGENTS.md README.md docs repo-governance .claude apps/rhino-cli > /tmp/private-sweep-targets.txt`
      — acceptance: the list is non-empty and recorded in the file-touch ledger
- [ ] [AI] Apply the identical `parity.rs` and `gate_specs.rs` content merged in Phase 5
      — command: `diff <(git -C /Users/wkf/ose-projects/ose-public show main:apps/rhino-cli/src/application/parity.rs) apps/rhino-cli/src/application/parity.rs`
      — acceptance: prints nothing
  - _Suggested executor: `swe-rust-dev`_
- [ ] [AI] Regenerate the parity manifest — command: `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- parity manifest generate`
      — acceptance: `parity-manifest.sha256` matches the other two repos'
- [ ] [AI] Apply the four→three edits to each enumerated target
      — command: `grep -rn 'beaver-nest' AGENTS.md README.md docs repo-governance .claude`
      — acceptance: zero matches outside `plans/done/**`
  - _Suggested executor: `repo-rules-maker`_
- [ ] [AI] Regenerate the harness mirrors — command: `npm run generate:bindings && npm run validate:sync`
      — acceptance: exits 0

### Local Quality Gates (Before Push)

- [ ] [AI] Run affected typecheck: `npx nx affected -t typecheck`
- [ ] [AI] Run affected linting: `npx nx affected -t lint`
- [ ] [AI] Run affected quick tests: `npx nx affected -t test:quick`
- [ ] [AI] Run affected spec coverage: `npx nx affected -t specs:coverage`
- [ ] [AI] Fix ALL failures found during quality gates, not just those caused by your changes
- [ ] [AI] Verify all checks pass before pushing

### Post-Push Verification

- [ ] [AI] Commit and push to origin `beaver-nest-repo-consolidation-sweep`, then open the draft PR
- [ ] [AI] Monitor the PR's check run per the [CI Monitoring Convention](../../../repo-governance/development/workflow/ci-monitoring.md) — `ScheduleWakeup(120s)`, then a single `gh pr checks --json bucket,name,state --jq '[.[] | select(.bucket != "pass")]'` per wakeup (never `--watch`) — repeat until the filtered output is `[]`
- [ ] [AI] Verify all CI checks pass; fix and push a follow-up commit on any failure
- [ ] [AI] Do NOT proceed until CI is green

### Phase 7 Gate

> All checks below must pass before starting Phase 8. If any check fails, fix it in Phase 7 before
> proceeding.

- [ ] [AI] `grep -rn 'beaver-nest' AGENTS.md README.md docs repo-governance .claude apps/rhino-cli/src` in `ose-private` — acceptance: zero matches outside `plans/done/**`
- [ ] [AI] Verify the byte-identity boundary is closed — command: run `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- parity manifest validate` in each of `ose-public`, `ose-primer`, `ose-private`
      — acceptance: all three exit 0 and report the same digest
- [ ] [AI] Confirm the scheduled parity audit is green — command: `gh run list --workflow=rhino-cli-parity-audit.yml --limit 1 --json conclusion`
      — acceptance: reports `success`
- [ ] [AI] Run the PR-Review Maker→Fixer Cycle — acceptance: 3 cycles complete, loop not `escalated`
- [ ] [AI] `gh pr ready` then merge — acceptance: preconditions (a)-(e) hold; merged by `[AI]`

> **Pause Safety**: all three surviving repos describe a three-repository family, and the
> byte-identity boundary is green again. `beaver-nest` still exists and is now referenced by nothing.
> This is a fully coherent stopping point — the consolidation is complete in substance even if the
> repo is never archived. Safe to stop indefinitely.
> To resume: `gh repo view wahidyankf/beaver-nest --json isArchived`.

## Phase 8: Retire the `beaver-nest` Repository

Changes land only in `beaver-nest`, as a markdown-only direct push immediately before the archive
flip. No `ose-public` PR opens. Archiving is reversible via `gh repo unarchive`
[Web-cited, GitHub Docs, accessed 2026-08-06].

- [ ] [AI] Verify every prior unit merged — command: `gh pr list --repo wahidyankf/ose-public --state merged --search 'beaver-nest-repo-consolidation' --json number,title`
      — acceptance: PRs for Phases 3, 4, and 5 are listed as merged, and the `ose-primer` / `ose-private` sweep PRs are merged in their own repos
- [ ] [AI] Confirm no surviving repo still references the fourth — command: `for r in ose-public ose-primer ose-private; do grep -rn 'beaver-nest' /Users/wkf/ose-projects/$r/AGENTS.md /Users/wkf/ose-projects/$r/README.md /Users/wkf/ose-projects/$r/docs /Users/wkf/ose-projects/$r/repo-governance; done`
      — acceptance: zero matches outside `plans/done/**`
- [ ] [AI] Rewrite `beaver-nest`'s `README.md` to a retirement notice stating the product now lives in
      `ose-public` as `apps/beavernest-be` and `apps/beavernest-app-web`, and linking to
      `https://github.com/wahidyankf/ose-public` — this follows GitHub's own pre-archive guidance to
      update the README before archiving
      — command: `grep -c 'ose-public' /Users/wkf/ose-projects/beaver-nest/README.md`
      — acceptance: prints at least 1
- [ ] [AI] Update the repository description to match — command: `gh repo edit wahidyankf/beaver-nest --description 'Archived — BeaverNest now lives in wahidyankf/ose-public'`
      — acceptance: `gh repo view wahidyankf/beaver-nest --json description` reflects the new text
- [ ] [AI] Commit and push the retirement notice to `beaver-nest` origin `main` — command: `git -C /Users/wkf/ose-projects/beaver-nest add README.md && git -C /Users/wkf/ose-projects/beaver-nest commit -m 'docs(readme): point to ose-public ahead of archival' && git -C /Users/wkf/ose-projects/beaver-nest push origin main`
      — acceptance: `git -C /Users/wkf/ose-projects/beaver-nest status -sb` shows no divergence from `origin/main`
      — note: the pre-existing uncommitted modifications recorded in `evidence/phase-0-beaver-nest-status.txt`
      are **not** committed here, whatever their count is by execution time; stage `README.md` explicitly
- [ ] [AI] Close any open issues and pull requests — command: `gh pr list --repo wahidyankf/beaver-nest --state open --json number` and `gh issue list --repo wahidyankf/beaver-nest --state open --json number`
      — acceptance: both report an empty array
- [ ] [AI] Archive the repository — command: `gh repo archive wahidyankf/beaver-nest --yes`
      — acceptance: `gh repo view wahidyankf/beaver-nest --json isArchived` reports `true`
- [ ] [AI] Verify the URL still resolves read-only — command: `curl -sS -o /dev/null -w '%{http_code}' https://github.com/wahidyankf/beaver-nest`
      — acceptance: prints `200`

### Phase 8 Gate

> All checks below must pass before starting Phase 9. If any check fails, fix it in Phase 8 before
> proceeding.

- [ ] [AI] `gh repo view wahidyankf/beaver-nest --json isArchived,visibility` — acceptance: reports `isArchived: true` and `visibility: PUBLIC`
- [ ] [AI] `npx nx run-many -t test:quick -p beavernest-be,beavernest-app-web,beavernest-be-e2e,beavernest-app-web-e2e` in `ose-public` — acceptance: exits 0, proving the product is unaffected by the archive

> **Pause Safety**: the OSE family is three repositories. BeaverNest's product, vision, and backlog
> live in `ose-public`; the fourth repository is read-only with a retirement notice, and its history
> and URL remain intact. Safe to stop.
> To resume: `gh repo view wahidyankf/beaver-nest --json isArchived`.

## Phase 9: Knowledge Capture

Executed once, in `ose-public`, on the local `main` checkout under the plan-docs-only carve-out —
no worktree, no PR.

- [ ] [AI] Triage every entry in `plans/in-progress/beaver-nest-repo-consolidation/learnings.md`
      through the [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)'s
      routing matrix — each surviving learning routes to exactly one durable home
      — command: `grep -c '^## Learning:' plans/in-progress/beaver-nest-repo-consolidation/learnings.md`
      — acceptance: every counted entry has a recorded terminal state, or the explicit escape
      `No generalizable learnings — <reason>` is present
- [ ] [AI] Apply the secret/sensitivity gate and the repo-relevance gate to every surviving entry
      — acceptance: no credential, token, or `ose-private` infra detail is routed into this public repo
- [ ] [AI] Route each small non-code learning inline in this plan's commits; file each large non-code
      learning and **every** code-homed learning as a new `plans/backlog/` plan, never inline
      — acceptance: no learning whose home is `apps/`, `libs/`, or tests was fixed inside this plan
- [ ] [AI] For any learning routed to `plans/ideas/`, scan `plans/ideas/README.md` and the existing
      briefs first and fold in rather than adding a near-duplicate
      — acceptance: the fold-or-create decision is recorded per entry
- [ ] [AI] Commit and push to origin main — command: `git add plans/ && git commit -m 'docs(plans): record knowledge-capture learnings for beaver-nest-repo-consolidation' && git push origin main`
      — acceptance: `git status -sb` shows no divergence

### Phase 9 Gate

> All checks below must pass before starting Phase 10. If any check fails, fix it in Phase 9 before
> proceeding.

- [ ] [AI] Every `learnings.md` entry reached a terminal state (routed inline / filed as backlog at a named path / discarded with a reason), or the explicit "none" escape is present
- [ ] [AI] No code-homed learning landed inline in this plan's commits
- [ ] [AI] `npm run lint:md:fix && git diff --exit-code` — acceptance: exits 0

> **Pause Safety**: every learning has a durable home and nothing depends on `learnings.md`
> surviving. The plan is substantively complete; only archival remains. Safe to stop.
> To resume: `git log --oneline -3`.

## Phase 10: Plan Archival and Cleanup

This phase's `git mv` to `plans/done/` lands as a direct push to local `main` under the
Plan-Docs-Only Carve-Out, not committed inside a PR. This is a deliberate, cited exception to the
[Archival-in-PR HARD RULE](../../../repo-governance/conventions/structure/plans.md#delivery-mode) —
see [tech-docs.md D11](./tech-docs.md#design-decisions) for why: the last `ose-public` PR is Phase
5's, and Phases 6-8 still have to land in `ose-primer`, `ose-private`, and against `beaver-nest`
before the plan is actually done, so no `ose-public` PR remains open to carry the archival commit.

### Plan Archival

- [ ] [AI] Verify ALL delivery checklist items are ticked
- [ ] [AI] Verify ALL quality gates pass (local + CI)
- [ ] [AI] Verify ALL manual assertions pass with committed evidence in `evidence/`
- [ ] [AI] Verify ALL supported locales were exercised in UI verification — **Not applicable**: this
      plan changes no screen and the ported SPA is single-locale
- [ ] [AI] Verify every rule-15 EWT/UWT/DWT defect finding is fixed — **Not applicable**: no UI
      feature change (see [tech-docs.md §Testing](./tech-docs.md#testing--verification-strategy))
- [ ] [AI] Verify every rule-16 AET defect finding is fixed — **Not applicable**: no API change
- [ ] [AI] Move the plan folder — command: `git mv plans/in-progress/beaver-nest-repo-consolidation "plans/done/$(date +%Y-%m-%d)__beaver-nest-repo-consolidation"`
      — acceptance: the folder exists under `plans/done/` with a completion-date prefix
- [ ] [AI] Update `plans/in-progress/README.md` — remove the plan entry
- [ ] [AI] Update `plans/done/README.md` — add the plan entry with its completion date
- [ ] [AI] Update any other READMEs that reference this plan
- [ ] [AI] Commit: `chore(plans): move beaver-nest-repo-consolidation to done`
- [ ] [AI] Push to origin main — command: `git push origin main`
      — acceptance: `git status -sb` shows no divergence

### Cleanup (terminal node — depends on every delivery node)

- [ ] [AI] Remove the `ose-public` worktree — command: `git worktree remove worktrees/beaver-nest-repo-consolidation`
      — acceptance: `git worktree list` no longer lists it
- [ ] [AI] Remove the `ose-primer` worktree — command: `git -C /Users/wkf/ose-projects/ose-primer worktree remove worktrees/beaver-nest-repo-consolidation`
      — acceptance: `git -C /Users/wkf/ose-projects/ose-primer worktree list` no longer lists it
- [ ] [AI] Remove the `ose-private` worktree — command: `git -C /Users/wkf/ose-projects/ose-private worktree remove worktrees/beaver-nest-repo-consolidation`
      — acceptance: `git -C /Users/wkf/ose-projects/ose-private worktree list` no longer lists it
- [ ] [HUMAN] Decide the fate of the local `/Users/wkf/ose-projects/beaver-nest` clone, which still
      holds the uncommitted modifications recorded in `evidence/phase-0-beaver-nest-status.txt`
      — acceptance: the maintainer either
      keeps it as a local archive or removes it deliberately
      — rationale for `[HUMAN]`: this directory contains uncommitted work that exists nowhere else,
      and no agent should decide to discard it

### Phase 10 Gate

> All checks below must pass before the plan is considered complete.

- [ ] [AI] `test -d plans/done/*__beaver-nest-repo-consolidation` — acceptance: exits 0
- [ ] [AI] `git worktree list` in all three repos — acceptance: none lists `beaver-nest-repo-consolidation`
- [ ] [AI] `npx nx run-many -t test:quick --all` — acceptance: exits 0

> **Pause Safety**: the plan is archived, all worktrees are removed, and the OSE family is three
> repositories. Nothing is in flight.
> To resume: nothing to resume — the plan is complete.

## Validation Checklist

- [ ] All TDD cycles complete with RED, GREEN, and REFACTOR each ticked separately
- [ ] All tests pass across the three surviving repos
- [ ] Quality standards met — typecheck, lint, test:quick, specs:coverage green
- [ ] Documentation updated — `AGENTS.md`, `README.md`, `docs/reference/`, `repo-governance/`
- [ ] Every acceptance criterion in [prd.md](./prd.md) is verified

## Related Documentation

- [README.md](./README.md) — context, scope, resolved design decisions
- [brd.md](./brd.md) — business rationale, baseline, prior art
- [prd.md](./prd.md) — user stories and Gherkin acceptance criteria
- [tech-docs.md](./tech-docs.md) — architecture, file-impact analysis, rollback
- [PR Merge Protocol](../../../repo-governance/development/workflow/pr-merge-protocol.md)
- [PR Review Quality Gate](../../../repo-governance/workflows/pr/pr-review-quality-gate.md)
- [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)
- [CI Monitoring](../../../repo-governance/development/workflow/ci-monitoring.md)
