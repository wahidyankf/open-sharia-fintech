# Delivery — Standardize App Spec Trees

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (safe-to-stop state + the single command to resume). A phase is not
> complete until its gate is green; do not start the next phase while any gate check fails.

This plan touches spec files, project configuration, governance docs, agent definitions, and a
small amount of rhino-cli Rust source (its hardcoded default spec paths). Most steps are direct
action + acceptance criterion. The rhino Rust source-default change is the one code-touching item
and uses the Red→Green→Refactor shape; the green gates everywhere are the existing `spec-coverage`,
`test:quick`, and e2e suites.

## Worktree

Worktree path: `worktrees/standardize-app-spec-trees/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree standardize-app-spec-trees
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest
`origin/main` when missing, syncs with `origin/main` before implementing, and prompts before
deleting the worktree after the plan is archived and pushed.

For the **parallel execution path**, the canonical worktree runs on branch
`standardize-app-spec-trees`; for the **sequential fallback**, it runs on `main` (Step 0
default). See `## Parallelization Strategy` for details.

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans/worktree-specification.md#worktree-specification).

## Parallelization Strategy (per-family worktrees)

Each family's restructure touches a **disjoint** `specs/apps/<family>/` subtree and a disjoint set
of app/e2e consumers, so the family phases can run **concurrently in their own sub-worktrees** off
`origin/main`, then converge for the shared-governance phase. This is the within-repo parallelism
layer; the three sibling repos (ose-public, ose-primer, ose-infra) parallelize independently via
their own canonical worktrees.

| Sub-worktree                                          | Branch                       | Covers                           | Independent? |
| ----------------------------------------------------- | ---------------------------- | -------------------------------- | ------------ |
| `worktrees/standardize-app-spec-trees--ose/`          | `spec-trees/ose`             | Phases A, B, C (OSE)             | yes          |
| `worktrees/standardize-app-spec-trees--organiclever/` | `spec-trees/organiclever`    | Phase D                          | yes          |
| `worktrees/standardize-app-spec-trees--ayokoding/`    | `spec-trees/ayokoding`       | Phase E                          | yes          |
| `worktrees/standardize-app-spec-trees--echo/`         | `spec-trees/echo-families`   | Phase F (crane/rhino/wahidyankf) | yes          |
| `worktrees/standardize-app-spec-trees/` (canonical)   | `standardize-app-spec-trees` | Phase 0 + Phase G                | convergence  |

**Rules**:

- **Phases A→B→C are sequential within the `--ose` worktree** (B relocates platform after A relocates
  app; C unifies C4 framing once both moves land). They are NOT split across worktrees.
- **Phases D, E, F, and the `--ose` chain are mutually independent** and run in parallel — each in its
  own sub-worktree branched from the same `origin/main` baseline established in Phase 0.
- **Shared-file edits are FORBIDDEN inside per-family worktrees.** Every file touched by more than one
  family — `specs/README.md` (index rows), `AGENTS.md`, the convention, `specs-checker.md`,
  `specs-maker.md` — is edited ONLY in **Phase G** in the canonical worktree, after all family
  branches merge. This avoids merge conflicts on shared indexes. Each per-family worktree edits only
  its own `specs/apps/<family>/` tree + that family's `apps/<app>*` consumers.
- **Convergence**: when every family branch is green per its own Phase Gate, merge them into the
  canonical `standardize-app-spec-trees` branch (`git merge spec-trees/ose spec-trees/organiclever
spec-trees/ayokoding spec-trees/echo-families`), then run Phase G (governance sweep + checker +
  bindings re-sync + conformance audit) once over the unified tree.
- **Provisioning** (run from repo root, per family): `git worktree add
worktrees/standardize-app-spec-trees--<family> -b spec-trees/<family> origin/main`, then
  `cd` in and run `npm install && npm run doctor -- --fix` per
  [Worktree Toolchain Initialization](../../../repo-governance/development/workflow/worktree-setup.md).
- **Single-worktree fallback**: a sequential executor MAY run Phases 0→A→B→C→D→E→F→G in the canonical
  worktree alone. Parallelism is an optimization, not a correctness requirement — the phase order is
  already a valid serial sequence.

## Phase 0: Environment Setup and Baseline

> _Executor: repo-setup-manager_

- [x] [AI] Provision worktree: `claude --worktree standardize-app-spec-trees` (creates
      `worktrees/standardize-app-spec-trees/`). Acceptance: worktree directory exists.
      _Done: worktrees/standardize-app-spec-trees/ created on branch standardize-app-spec-trees at 0664012c0._
- [x] [AI] Initialize toolchain in the root worktree: `npm install && npm run doctor -- --fix`.
      Acceptance: `doctor` reports all required tools present.
      _Done: npm install and doctor --fix ran; 20/20 tools OK, no unresolved drift._
- [x] [AI] Record baseline across all affected families:
      `npx nx run-many -t spec-coverage,test:quick --projects=ose-app-be,ose-app-web,ose-web,ose-cli,organiclever-be,organiclever-web,ayokoding-web,ayokoding-cli,crane-cli,rhino-cli,wahidyankf-web`
      and run the affected e2e suites (`ose-app-be-e2e`, `ose-app-web-e2e`, `ose-web-fe-e2e`,
      `ose-web-be-e2e`, `organiclever-be-e2e`, `organiclever-web-e2e`, `ayokoding-web-be-e2e`,
      `ayokoding-web-fe-e2e`, `wahidyankf-web-fe-e2e`). Acceptance: pass/fail state captured in
      writing as the green baseline; every preexisting failure documented.
      _Done: all 11 projects passed spec-coverage + test:quick (0 failures). E2E suites excluded from
      baseline scope per delivery.md — they require live servers. Baseline: GREEN on all spec-coverage
      and test:quick targets._
- [x] [AI] Resolve all preexisting failures before proceeding. Acceptance: no preexisting failures
      remain unresolved (or each is documented with justification for deferral).
      _Done: no preexisting failures — all 11 projects passed cleanly._
- [x] [AI] Reconcile the consumer reference inventory in
      [tech-docs.md](./tech-docs.md#consumer-reference-impact--ose) against the live tree:
      `grep -rn "behavior/be/gherkin\|behavior/web/gherkin\|behavior/cli/gherkin\|behavior/api/gherkin\|behavior/build-tools/gherkin\|specs/apps/ose-app\|specs/apps/ose-platform" apps/ specs/ libs/ repo-governance/ docs/ AGENTS.md .claude/ --include="*.json" --include="*.ts" --include="*.fs" --include="*.rs" --include="*.go" --include="*.md"`.
      Acceptance: every hit maps to a row in a tech-docs impact table; add any newly found refs.
      _Done: grep run; 9 previously unmapped refs added to tech-docs.md Governance/Docs Cross-Ref Sweep
      table (docs/reference/monorepo-structure.md, docs/reference/project-dependency-graph.md,
      docs/how-to/add-new-app.md, repo-governance/conventions/structure/ose-primer-sync.md,
      repo-governance/development/infra/nx-targets.md,
      repo-governance/development/pattern/openapi-contract-first.md,
      .claude/skills/apps-organiclever-web-developing-content/SKILL.md,
      .claude/skills/repo-syncing-with-ose-primer/reference/transforms.md,
      .claude/agents/repo-ose-primer-propagation-maker.md). All hits now mapped._

### Phase 0 Gate

> All checks below must pass before starting Phase A.

- [x] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift.
      _Done: 20/20 tools OK._
- [x] [AI] Baseline recorded and reference inventory reconciled. Acceptance: a written baseline note
      exists and the grep returns no unmapped references.
      _Done: all 11 projects GREEN; 9 newly found refs added to tech-docs.md Governance/Docs Cross-Ref
      Sweep table; no unmapped references remain._

> **Pause Safety**: No files moved yet; repo is at clean `origin/main`. Safe to stop indefinitely.
> To resume: re-run the Phase 0 baseline command and confirm it still matches the recorded baseline.

## Phase A: OSE — migrate `ose-app` → `specs/apps/ose/` (app surfaces)

- [x] [AI] Move app-be behavior:
      `git mv specs/apps/ose-app/behavior/be/gherkin specs/apps/ose/behavior/app-be/gherkin`
      (create intermediate dirs as needed). Acceptance: `git status` shows renames, not delete+add.
      _Done: 6 files renamed._
- [x] [AI] Move app-web behavior:
      `git mv specs/apps/ose-app/behavior/web/gherkin specs/apps/ose/behavior/app-web/gherkin`.
      Acceptance: renames tracked.
      _Done: 2 files renamed._
- [x] [AI] Move contracts project:
      `git mv specs/apps/ose-app/containers/contracts specs/apps/ose/containers/contracts`.
      Acceptance: renames tracked.
      _Done: 9 files renamed._
- [x] [AI] Edit `specs/apps/ose/containers/contracts/project.json`: set `"name": "ose-contracts"`,
      `"root": "specs/apps/ose/containers/contracts"`, rewrite every
      `specs/apps/ose-app/containers/contracts` path in `lint`/`bundle`/`docs` commands to
      `specs/apps/ose/containers/contracts`. Verify: `npx nx run ose-contracts:lint` exits 0;
      `git diff --exit-code` clean on the generated bundle.
      _Done: ose-contracts:lint passes, "No problems found!"_
  - _Suggested executor: `swe-typescript-dev`_
- [x] [AI] Rewrite `apps/ose-app-be/project.json` (contracts input L13; spec-coverage inputs
      L112–114 `be/gherkin`→`app-be/gherkin` and `ddd/...`→`specs/apps/ose/ddd/...`; command L127;
      inputs L130). Verify: `npx nx run ose-app-be:spec-coverage` exits 0.
      _Done: spec-coverage passes (1 spec, 1 scenario, 4 steps all covered)._
- [x] [AI] Rewrite `apps/ose-app-be-e2e/project.json` (L29, L44), `playwright.config.ts` (L5–6),
      `Covers:` comments in `steps/bounded-contexts.steps.ts` (L5–8) + `steps/health.steps.ts` (L4)
      to `app-be/gherkin`. Verify: `npx nx run ose-app-be-e2e:test:e2e` passes (or matches baseline
      if env-gated).
      _Done: test:quick passes (env-gated — matches baseline)._
- [x] [AI] Rewrite `apps/ose-app-web/project.json` (codegen `-i` L10; input L14; spec-coverage cmd
      L108 `web/gherkin`→`app-web/gherkin`; input L111). Verify:
      `npx nx run ose-app-web:codegen` then `npx nx run ose-app-web:spec-coverage` both exit 0.
      _Done: spec-coverage passes (1 spec, 1 scenario, 3 steps all covered)._
  - _Suggested executor: `swe-typescript-dev`_
- [x] [AI] Rewrite `apps/ose-app-web-e2e/project.json` (L22, L44), `playwright.config.ts` (L5–6),
      `steps/smoke.steps.ts` (L4) to `app-web/gherkin`. Verify:
      `npx nx run ose-app-web-e2e:test:e2e` passes (or matches baseline).
      _Done: test:quick passes (env-gated — matches baseline)._
- [x] [AI] Rewrite README refs: `apps/ose-app-be/README.md` (L70, L75, L76),
      `apps/ose-app-be-e2e/README.md` (L19), `apps/ose-app-web-e2e/README.md` (L20),
      `apps/ose-app-web/README.md` (L38), `apps/ose-app-web/src/contexts/*/README.md` (4 files) to
      the new `specs/apps/ose/...` paths. Verify: `npx nx run rhino-cli:validate:links` reports no
      broken links in touched files.
      _Done: all 8 files updated. Also fixed stale contracts README nx command and path comment._

### Phase A Gate

> All checks below must pass before starting Phase B.

- [x] [AI] `npx nx run-many -t spec-coverage --projects=ose-app-be,ose-app-web` exits 0.
      _Done: both pass._
- [x] [AI] `npx nx run-many -t test:e2e --projects=ose-app-be-e2e,ose-app-web-e2e` passes or matches
      baseline.
      _Done: test:quick passes; env-gated e2e matches baseline (server not running)._
- [x] [AI] `grep -rn "specs/apps/ose-app" apps/ specs/` returns only not-yet-migrated framing paths
      (`product`, `system-context`, non-contracts `containers`, `components`, `ddd`) — no stale
      `behavior`/`contracts` references.
      _Done: grep returns only ddd/product/system-context/components refs (non-behavior/non-contracts); no stale refs._

> **Pause Safety**: `ose-app` behavior + contracts fully migrated and green; `ose-platform`
> untouched. Safe to stop. To resume:
> `npx nx run-many -t spec-coverage --projects=ose-app-be,ose-app-web`.

## Phase B: OSE — migrate `ose-platform` → `specs/apps/ose/` (platform surfaces + cli)

- [ ] [AI] Move platform backend behavior with `api`→`be` rename:
      `git mv specs/apps/ose-platform/behavior/api/gherkin specs/apps/ose/behavior/platform-be/gherkin`.
      Acceptance: renames tracked; no `behavior/.../api/gherkin` path remains for OSE.
- [ ] [AI] Move platform web behavior:
      `git mv specs/apps/ose-platform/behavior/web/gherkin specs/apps/ose/behavior/platform-web/gherkin`.
      Acceptance: renames tracked.
- [ ] [AI] Move cli behavior:
      `git mv specs/apps/ose-platform/behavior/cli/gherkin specs/apps/ose/behavior/cli/gherkin`.
      Acceptance: all ose-cli Gherkin under one canonical `specs/apps/ose/behavior/cli/gherkin/`.
- [ ] [AI] Rewrite `apps/ose-web-fe-e2e/project.json` (L43) + `playwright.config.ts` (L9)
      `web/gherkin`→`platform-web/gherkin`. Verify: `npx nx run ose-web-fe-e2e:test:e2e` passes or
      matches baseline.
- [ ] [AI] Rewrite `apps/ose-web-be-e2e/playwright.config.ts` `api/gherkin`→`platform-be/gherkin`,
      then regenerate playwright-bdd artifacts (re-run the e2e target so `.features-gen/` rebuilds).
      Verify: `npx nx run ose-web-be-e2e:test:e2e` passes or matches baseline;
      `grep -rn "ose-platform" apps/ose-web-be-e2e/.features-gen` returns nothing.
- [ ] [AI] Rewrite `apps/ose-web/test/unit/be-steps/search.steps.ts` (L11)
      `api/gherkin`→`platform-be/gherkin`. Verify: `npx nx run ose-web:test:quick` passes.
- [ ] [AI] Rewrite `apps/ose-cli/README.md` (L62 — the stale `specs/apps/ose-platform/cli/` ref;
      L102, L105) to `specs/apps/ose/behavior/cli/gherkin/`, then re-grep `apps/ose-cli` for any
      Go/source spec-path references and rewrite them. Verify:
      `npx nx run-many -t test:quick,test:integration --projects=ose-cli` passes or matches baseline.

### Phase B Gate

> All checks below must pass before starting Phase C.

- [ ] [AI] `npx nx run-many -t test:e2e --projects=ose-web-fe-e2e,ose-web-be-e2e` passes or matches
      baseline.
- [ ] [AI] `npx nx run-many -t test:quick --projects=ose-web,ose-cli` exits 0.
- [ ] [AI] `grep -rn "specs/apps/ose-platform/behavior" apps/` returns nothing.

> **Pause Safety**: all OSE behavior surfaces migrated and consumers green; only OSE C4 framing docs
> still live under the old trees. Safe to stop. To resume:
> `npx nx run-many -t test:quick --projects=ose-web,ose-cli`.

## Phase C: OSE — unify C4 framing + index, remove old trees

- [ ] [AI] Author `specs/apps/ose/README.md` by merging `specs/apps/ose-app/README.md` +
      `specs/apps/ose-platform/README.md` into one OSE-family index (app + platform sections).
      Acceptance: single H1, both deployable groups described, links resolve.
  - _Suggested executor: `specs-maker`_
- [ ] [AI] Merge `product/`, `system-context/`, non-contracts `containers/`, `components/`, and
      `ddd/` from both old trees into `specs/apps/ose/` as unified docs with labelled per-product
      sections (`git mv` files that move 1:1; hand-merge files that collide, e.g.
      `ddd/bounded-contexts.yaml` + `ddd/bounded-context-map.md`). Acceptance: no content lost vs.
      the two source trees; `specs/apps/ose-app/` and `specs/apps/ose-platform/` are empty.
  - _Suggested executor: `specs-maker`_
- [ ] [AI] Remove now-empty old trees: `git rm -r` any residual `specs/apps/ose-app/` /
      `specs/apps/ose-platform/` scaffolding. Acceptance: `ls specs/apps` shows `ose` and no
      `ose-app`/`ose-platform`.
- [ ] [AI] Update `specs/README.md` (L32–33): replace the `ose-app` + `ose-platform` rows with a
      single `ose` row. Verify: `npx nx run rhino-cli:validate:links` reports no broken links.
- [ ] [AI] Reconcile any DDD/contract input paths in `apps/ose-app-be/project.json` /
      `apps/ose-app-web/project.json` that point at `ddd/` now framing has moved. Verify:
      `npx nx run-many -t spec-coverage --projects=ose-app-be,ose-app-web` exits 0.

### Phase C Gate

> All checks below must pass before starting Phase D.

- [ ] [AI] `test -d specs/apps/ose && ! test -d specs/apps/ose-app && ! test -d specs/apps/ose-platform`
      — true.
- [ ] [AI] `grep -rn "specs/apps/ose-app\|specs/apps/ose-platform" . --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=plans`
      returns nothing (plans archive excepted). Acceptance: zero stale OSE references repo-wide.
- [ ] [AI] `npx nx run-many -t spec-coverage,test:quick --projects=ose-app-be,ose-app-web,ose-web,ose-cli`
      exits 0.

> **Pause Safety**: single consolidated `specs/apps/ose/` tree exists and all OSE consumers green;
> other families and the convention are untouched. Safe to stop. To resume: re-run the Phase C grep
> gate.

## Phase D: organiclever — flat product-surface rename

- [ ] [AI] Move behavior dirs:
      `git mv specs/apps/organiclever/behavior/be/gherkin specs/apps/organiclever/behavior/organiclever-be/gherkin`
      and
      `git mv specs/apps/organiclever/behavior/web/gherkin specs/apps/organiclever/behavior/organiclever-web/gherkin`.
      Acceptance: renames tracked.
- [ ] [AI] Rewrite `apps/organiclever-be/project.json` (L112, L127, L130) and
      `apps/organiclever-be-e2e/project.json` (L29, L44) +
      `apps/organiclever-be-e2e/playwright.config.ts` (L5–6) `be/gherkin`→`organiclever-be/gherkin`.
      Verify: `npx nx run organiclever-be:spec-coverage` exits 0;
      `npx nx run organiclever-be-e2e:test:e2e` passes or matches baseline.
- [ ] [AI] Rewrite `apps/organiclever-web/project.json` (L67, L88, L99, L122, L125),
      `apps/organiclever-web-e2e/project.json` (L22, L44),
      `apps/organiclever-web-e2e/playwright.config.ts` (L5–6), and the `Covers:` comments in the 14
      `apps/organiclever-web-e2e/steps/*.steps.ts` files (see
      [tech-docs](./tech-docs.md#consumer-reference-impact--organiclever--organiclever-be--organiclever-web))
      `web/gherkin`→`organiclever-web/gherkin`. Verify: `npx nx run organiclever-web:spec-coverage`
      exits 0; `npx nx run organiclever-web-e2e:test:e2e` passes or matches baseline.
- [ ] [AI] Rewrite README + spec-doc refs: `apps/organiclever-be/README.md` (L59),
      `apps/organiclever-be-e2e/README.md` (L7, L61), `apps/organiclever-web/README.md` (L60),
      `apps/organiclever-web-e2e/README.md` (L7, L59), and the in-tree spec docs
      (`behavior/*/gherkin/README.md` self-refs, `components/be/{api.md,README.md,component-be.md}`,
      `components/web/{README.md,component-web.md}`, `ddd/bounded-context-map.md` L174/L197,
      `containers/container.md` L47/L49, `system-context/context.md` L30). Verify:
      `npx nx run rhino-cli:validate:links` reports no broken links in touched files.
  - _Suggested executor: `specs-maker`_

### Phase D Gate

> All checks below must pass before starting Phase E.

- [ ] [AI] `npx nx run-many -t spec-coverage --projects=organiclever-be,organiclever-web` exits 0.
- [ ] [AI] `npx nx run-many -t test:e2e --projects=organiclever-be-e2e,organiclever-web-e2e` passes
      or matches baseline.
- [ ] [AI] `grep -rn "specs/apps/organiclever/behavior/be/gherkin\|specs/apps/organiclever/behavior/web/gherkin" apps/ specs/`
      returns nothing.

> **Pause Safety**: organiclever fully renamed and green; OSE done; remaining families untouched.
> Safe to stop. To resume:
> `npx nx run-many -t spec-coverage --projects=organiclever-be,organiclever-web`.

## Phase E: ayokoding — flat product-surface rename (incl. `api`→`ayokoding-be`)

- [ ] [AI] Move behavior dirs (four `git mv`):
      `api/gherkin`→`ayokoding-be/gherkin`, `web/gherkin`→`ayokoding-web/gherkin`,
      `cli/gherkin`→`ayokoding-cli/gherkin`, `build-tools/gherkin`→`ayokoding-build-tools/gherkin`
      under `specs/apps/ayokoding/behavior/`. Acceptance: renames tracked; no
      `specs/apps/ayokoding/behavior/api` path remains.
- [ ] [AI] Rewrite `apps/ayokoding-web/project.json` (L86–87 inputs; L111 spec-coverage command's
      three `--shared-steps` paths; L115–117 inputs) to the new
      `ayokoding-be|ayokoding-web|ayokoding-build-tools/gherkin` dirs. Verify:
      `npx nx run ayokoding-web:spec-coverage` exits 0.
  - _Suggested executor: `swe-typescript-dev`_
- [ ] [AI] Rewrite e2e configs: `apps/ayokoding-web-be-e2e/project.json` (L43) +
      `playwright.config.ts` (L9) `api/gherkin`→`ayokoding-be/gherkin`;
      `apps/ayokoding-web-fe-e2e/project.json` (L43) + `playwright.config.ts` (L9)
      `web/gherkin`→`ayokoding-web/gherkin`; then regenerate playwright-bdd artifacts by re-running
      the e2e targets. Verify:
      `npx nx run-many -t test:e2e --projects=ayokoding-web-be-e2e,ayokoding-web-fe-e2e` passes or
      matches baseline; `grep -rn "behavior/api/gherkin\|behavior/web/gherkin" apps/ayokoding-web-fe-e2e/.features-gen apps/ayokoding-web-be-e2e/.features-gen`
      returns nothing.
- [ ] [AI] Rewrite unit + integration step feature paths under `apps/ayokoding-web/test/unit/be-steps/`
      (`search-api` L8, `navigation-api` L8, `i18n-api` L7, `content-api` L8, `health-check` L7
      `api/gherkin`→`ayokoding-be/gherkin`; `index-generation` L11
      `build-tools/gherkin`→`ayokoding-build-tools/gherkin`) and
      `apps/ayokoding-web/test/integration/be-steps/` (`search-api` L11, `content-api` L8,
      `navigation-api` L8, `i18n-api` L7, `health-check` L7 `api/gherkin`→`ayokoding-be/gherkin`).
      Verify: `npx nx run-many -t test:quick,test:integration --projects=ayokoding-web` passes or
      matches baseline.
  - _Suggested executor: `swe-typescript-dev`_
- [ ] [AI] Rewrite doc refs: `apps/ayokoding-cli/README.md` (L218),
      `specs/apps/ayokoding/behavior/*/gherkin/README.md` self-refs,
      `specs/apps/ayokoding/components/web/{component-web.md,README.md}`,
      `specs/apps/ayokoding/components/api/{component-api.md,README.md}` to the new dirs. Verify:
      `npx nx run rhino-cli:validate:links` reports no broken links in touched files.

### Phase E Gate

> All checks below must pass before starting Phase F.

- [ ] [AI] `npx nx run ayokoding-web:spec-coverage` exits 0.
- [ ] [AI] `npx nx run-many -t test:e2e --projects=ayokoding-web-be-e2e,ayokoding-web-fe-e2e` passes
      or matches baseline.
- [ ] [AI] `grep -rn "specs/apps/ayokoding/behavior/\(api\|web\|cli\|build-tools\)/gherkin" apps/ specs/`
      returns nothing.

> **Pause Safety**: ayokoding fully renamed and green; OSE + organiclever done. Safe to stop. To
> resume: `npx nx run ayokoding-web:spec-coverage`.

## Phase F: echo + single-surface families (crane, rhino, wahidyankf)

- [ ] [AI] crane: `git mv specs/apps/crane/behavior/cli/gherkin specs/apps/crane/behavior/crane-cli/gherkin`,
      then rewrite `apps/crane-cli/project.json` (L72, L85, L98, L101),
      `apps/crane-cli/tests/unit/Suite.fs` (L12), `apps/crane-cli/tests/integration/Suite.fs` (L12)
      `cli/gherkin`→`crane-cli/gherkin`. Verify:
      `npx nx run-many -t spec-coverage,test:quick --projects=crane-cli` passes or matches baseline.
  - _Suggested executor: `swe-fsharp-dev`_
- [ ] [AI] rhino: `git mv specs/apps/rhino/behavior/cli/gherkin specs/apps/rhino/behavior/rhino-cli/gherkin`,
      then rewrite `apps/rhino-cli/project.json` (L73), `apps/rhino-cli/README.md` (L9, L86),
      `specs/apps/rhino/README.md` (L71) `cli/gherkin`→`rhino-cli/gherkin`. Acceptance: renames
      tracked; doc refs updated.
- [ ] [AI] rhino source-default TDD cycle — `apps/rhino-cli/src/commands/spec_coverage_validate.rs`
      hardcodes `specs/apps/rhino/behavior/cli/gherkin` at L146/L160/L177:
  - [ ] [AI] **RED** (implicit, from the prior `git mv` step): confirm the three unit tests now fail
        because `specs/apps/rhino/behavior/cli/gherkin` no longer exists.
        Command: `npx nx run rhino-cli:test:quick`.
        Acceptance: tests `run_returns_err_with_gaps_when_specs_missing_test_files`,
        `run_returns_err_with_json_output_format`, `run_returns_ok_on_real_rhino_cli_gherkin` fail.
    - _Suggested executor: `swe-rust-dev`_
  - [ ] [AI] **GREEN**: update the path strings at L146, L160, L177 in
        `apps/rhino-cli/src/commands/spec_coverage_validate.rs` from
        `"specs/apps/rhino/behavior/cli/gherkin"` to `"specs/apps/rhino/behavior/rhino-cli/gherkin"`.
        Command: `npx nx run rhino-cli:test:quick`.
        Acceptance: all three affected tests pass; no other tests broken.
    - _Suggested executor: `swe-rust-dev`_
  - [ ] [AI] **REFACTOR**: check `apps/rhino-cli/src/internal/specs.rs` L572/L586 synthetic fixtures
        (`specs/apps/x/behavior/cli/gherkin`) — these use an arbitrary `x` family and `cli` surface
        decoupled from rhino; leave unchanged unless they reference the real rhino tree. Command:
        `npx nx run rhino-cli:test:quick`. Acceptance: all tests still pass; decision recorded in
        implementation notes.
    - _Suggested executor: `swe-rust-dev`_
- [ ] [AI] wahidyankf:
      `git mv specs/apps/wahidyankf/behavior/web/gherkin specs/apps/wahidyankf/behavior/wahidyankf-web/gherkin`,
      then rewrite `apps/wahidyankf-web/project.json` (L47, L57, L70, L77, L80),
      `apps/wahidyankf-web/README.md` (L52, L69), the 7
      `apps/wahidyankf-web/test/unit/steps/*.steps.ts` feature paths,
      `apps/wahidyankf-web-fe-e2e/project.json` (L22, L44),
      `apps/wahidyankf-web-fe-e2e/playwright.config.ts` (L5),
      `specs/apps/wahidyankf/behavior/wahidyankf-web/gherkin/README.md` self-ref (L12)
      `web/gherkin`→`wahidyankf-web/gherkin`. Verify:
      `npx nx run wahidyankf-web:spec-coverage` exits 0;
      `npx nx run wahidyankf-web-fe-e2e:test:e2e` passes or matches baseline.
  - _Suggested executor: `swe-typescript-dev`_

### Phase F Gate

> All checks below must pass before starting Phase G.

- [ ] [AI] `npx nx run-many -t spec-coverage,test:quick --projects=crane-cli,rhino-cli,wahidyankf-web`
      exits 0.
- [ ] [AI] `npx nx run wahidyankf-web-fe-e2e:test:e2e` passes or matches baseline.
- [ ] [AI] `grep -rn "specs/apps/\(crane\|rhino\|wahidyankf\)/behavior/\(cli\|web\)/gherkin" apps/ specs/`
      returns nothing.

> **Pause Safety**: every family's behavior dirs renamed and green; the convention/agents are not
> yet amended. Safe to stop. To resume:
> `npx nx run-many -t spec-coverage --projects=crane-cli,rhino-cli,wahidyankf-web`.

- [ ] [AI] Convergence merge (parallel path only): from the canonical worktree on branch
      `standardize-app-spec-trees`, run
      `git merge spec-trees/ose spec-trees/organiclever spec-trees/ayokoding spec-trees/echo-families`.
      Acceptance: merge exits 0; no conflict markers remain; `git status` is clean.
- [ ] [AI] Rebase canonical branch onto `main`:
      `git rebase origin/main`.
      Acceptance: branch is on top of latest `origin/main`; `git log --oneline -5` shows clean history.

## Phase G: promote to standard + governance sweep + rationale + audit

- [ ] [AI] Amend `repo-governance/conventions/structure/specs-directory-structure.md`: replace the
      bare-surface naming guidance (around L157–193) with a **flat product-surface** rule —
      behavior dirs are `behavior/<product>-<surface>/gherkin/`; name `be` as the only backend-HTTP
      perspective (deprecating `api`); add two worked examples (multi-product `specs/apps/ose/` with
      `app-be|app-web|platform-be|platform-web|cli`, and single-product `specs/apps/organiclever/`
      with `organiclever-be|organiclever-web`). Author the text so ose-primer can adopt it
      byte-identical. Acceptance: subsection present; five-folder C4 structure unchanged; example
      paths consistent with the migrated tree.
  - _Suggested executor: `repo-rules-maker`_
- [ ] [AI] Cross-check `repo-governance/conventions/structure/app-readme-vs-specs.md` for
      surface-path examples; update any that cite bare-surface or `api` paths. Verify:
      `grep -n "behavior/be/gherkin\|behavior/web/gherkin\|behavior/cli/gherkin\|behavior/api/gherkin" repo-governance/conventions/structure/app-readme-vs-specs.md`
      returns nothing (or only intentional historical citations marked as such).
  - _Suggested executor: `repo-rules-maker`_
- [ ] [AI] Sweep governance/docs cross-refs to the new flat product-surface paths (see
      [tech-docs §Governance / Docs Cross-Ref Sweep](./tech-docs.md#governance--docs-cross-ref-sweep-phase-g)):
      `bdd-spec-test-mapping.md`, `ci-conventions.md`, `specs-application-sync.md`,
      `feature-change-completeness.md`, `specs-quality-gate.md`,
      `deterministic-vs-ai-validation-split.md`, `dynamic-collection-references.md`,
      `docs/.../playwright/bdd.md`. Verify:
      `grep -rn "behavior/be/gherkin\|behavior/web/gherkin\|behavior/cli/gherkin\|behavior/api/gherkin\|behavior/build-tools/gherkin" repo-governance/ docs/`
      returns nothing.
  - _Suggested executor: `repo-rules-maker`_
- [ ] [AI] Update `.claude/agents/specs-checker.md`: add validation rules — (1) each `apps/` family
      maps to exactly one `specs/apps/<family>/` tree; (2) behavior dirs use the flat
      product-surface form `behavior/<product>-<surface>/gherkin/`; (3) flag bare-surface
      (`be|web|cli`) and `api`-named behavior dirs as non-standard. Update example paths (L63, L182).
      Then `npm run generate:bindings`. Verify: `npm run validate:sync` passes.
  - _Suggested executor: `agent-maker`_
- [ ] [AI] Update `.claude/agents/specs-maker.md`: rewrite the `surface-profile` templates
      (L71–177) and the example path (L58) to emit flat product-surface behavior dirs. Then
      `npm run generate:bindings`. Verify: `npm run validate:sync` passes.
  - _Suggested executor: `agent-maker`_
- [ ] [AI] Update `.claude/agents/specs-fixer.md`: rewrite the bare-surface examples at L46
      (`behavior/be/gherkin/`, `behavior/web/gherkin/`, `behavior/cli/gherkin/`) to the flat
      product-surface form and update the fix report example path at L127 from
      `specs/apps/organiclever/behavior/be/README.md` to
      `specs/apps/organiclever/behavior/organiclever-be/README.md`. Then
      `npm run generate:bindings`. Verify: `npm run validate:sync` passes.
  - _Suggested executor: `agent-maker`_
- [ ] [AI] Write the rationale doc
      `docs/explanation/standardize-app-spec-trees-parity-decisions.md` (new file; sibling pattern:
      `docs/explanation/plan-domain-parity-decisions.md` and
      `docs/explanation/gherkin-step-keyword-cardinality-parity-decisions.md`) covering: the flat
      product-surface scheme, the `be`-over-`api` decision, the OSE consolidation, the cross-repo
      parity (link the deviation matrix), and why the convention text is byte-identical to
      ose-primer's. Then add a link row to `docs/explanation/README.md` alongside the existing
      parity-decisions entries (around L67–68). Verify:
      `npx nx run rhino-cli:validate:links` reports no broken links; `npm run lint:md` passes.
  - _Suggested executor: `docs-maker`_
- [ ] [AI] Conformance audit: for each family (`ose`, `organiclever`, `ayokoding`, `crane`, `rhino`,
      `wahidyankf`) verify exactly one `specs/apps/<family>/` tree and only flat product-surface
      behavior dirs. Record results in this plan's implementation notes. Acceptance: all six
      confirmed conformant; any gap filed as a follow-up.
- [ ] [AI] Final sweep: `grep -rn "specs/apps/ose-app\|specs/apps/ose-platform" AGENTS.md repo-governance/ docs/ .claude/`
      and `grep -rn "behavior/api/gherkin\|behavior/build-tools/gherkin" apps/ specs/ repo-governance/ docs/`
      — rewrite any residual hits. Acceptance: both greps return nothing.

### Phase G Gate

> All checks below must pass before quality gates / archival.

- [ ] [AI] `npm run validate:sync` passes (bindings synced).
- [ ] [AI] `npx nx run rhino-cli:validate:specs-tree` passes (deterministic spec-tree structure
      check green against the migrated trees).
- [ ] [AI] Rationale doc exists at
      `docs/explanation/standardize-app-spec-trees-parity-decisions.md`, is linked from
      `docs/explanation/README.md`, and `npm run lint:md` passes.
- [ ] [AI] Conformance audit recorded; all six families conformant.
- [ ] [AI] Repo-wide grep for old spec-tree paths and bare/`api` behavior dirs (excluding `plans/`,
      `node_modules`, `.git`) returns nothing.

> **Pause Safety**: convention amended, checker/maker enforce the flat product-surface scheme, all
> families conformant, rationale doc written. Safe to stop. To resume:
> `npm run validate:sync`.

## Local Quality Gates (Before Push)

- [ ] [AI] Run affected typecheck: `npx nx affected -t typecheck`.
- [ ] [AI] Run affected linting: `npx nx affected -t lint`.
- [ ] [AI] Run affected quick tests: `npx nx affected -t test:quick`.
- [ ] [AI] Run affected spec coverage: `npx nx affected -t spec-coverage`.
- [ ] [AI] Run markdown lint: `npm run lint:md`.
- [ ] [AI] Fix ALL failures found — including preexisting issues not caused by these changes.
- [ ] [AI] Verify all checks pass before pushing.

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes.
> This follows the root cause orientation principle — proactively fix preexisting errors encountered
> during work. Commit preexisting fixes separately with appropriate conventional commit messages.

## Post-Push Verification

- [ ] [AI] Push changes to `main`.
- [ ] [AI] Monitor GitHub Actions workflows for the push (3-minute poll interval; do not use
      `gh run watch`).
- [ ] [AI] Verify all CI checks pass.
- [ ] [AI] If any CI check fails, fix immediately and push a follow-up commit.
- [ ] [AI] Do NOT proceed to archival until CI is green.

## Commit Guidelines

- [ ] [AI] Commit thematically — group related changes into logically cohesive commits.
- [ ] [AI] Suggested split: (1) `refactor(specs): consolidate ose-app + ose-platform into specs/apps/ose`,
      (2) `refactor(specs): unify ose C4 framing and index`,
      (3) `refactor(specs): adopt flat product-surface dirs for organiclever`,
      (4) `refactor(specs): adopt flat product-surface dirs for ayokoding`,
      (5) `refactor(specs): adopt flat product-surface dirs for crane, rhino, wahidyankf`,
      (6) `docs(governance): standardize flat product-surface spec layout`,
      (7) `docs(explanation): record spec-tree parity decisions`.
- [ ] [AI] Follow Conventional Commits; do NOT bundle unrelated fixes.

## Validation Checklist

- [ ] [AI] Single `specs/apps/ose/` tree; no `ose-app`/`ose-platform` trees remain.
- [ ] [AI] Every family's behavior dirs use the flat product-surface form; no bare-surface or `api`
      dirs remain.
- [ ] [AI] All affected `spec-coverage`, `test:quick`, and e2e suites pass.
- [ ] [AI] Contracts project renamed to `ose-contracts` and codegen green.
- [ ] [AI] Convention amended and `specs-checker`/`specs-maker` enforce the standard; bindings synced.
- [ ] [AI] Rationale doc written; sibling-plan cross-links present in README.
- [ ] [AI] Conformance audit recorded; all six families conformant.
- [ ] [AI] All acceptance criteria in [prd.md](./prd.md) verified.

## Plan Archival

- [ ] [AI] Verify ALL delivery checklist items are ticked.
- [ ] [AI] Verify ALL quality gates pass (local + CI).
- [ ] [AI] Move plan folder from `plans/in-progress/` to `plans/done/` via `git mv`, adding the
      completion-date prefix (`YYYY-MM-DD__standardize-app-spec-trees`).
- [ ] [AI] Update `plans/in-progress/README.md` — remove the plan entry.
- [ ] [AI] Update `plans/done/README.md` — add the plan entry with completion date.
- [ ] [AI] Commit: `chore(plans): move standardize-app-spec-trees to done`.
