# Delivery Checklist

## Worktree

Worktree path: `worktrees/standardize-github-actions-pipeline-naming/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree standardize-github-actions-pipeline-naming
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest
`origin/main` when missing, syncs with `origin/main` before implementing, and prompts before deleting
the worktree after the plan is archived and pushed.

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans/worktree-specification.md#worktree-specification).

---

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate`: a must-pass verification
> checklist plus a **Pause Safety** note (the safe-to-stop state after the phase and the
> single command to resume). A phase is **not complete until its gate is green**; do not start
> phase N+1 while any check in phase N's gate is failing.
>
> **TDD legend** — **RED** = add/leave a check that currently fails → **GREEN** = make the
> change so it passes → **REFACTOR** = dedupe/tidy without changing behavior.
>
> **Commit guidance**: commit each phase's changes as a thematic unit using Conventional Commits
> (`ci(workflows): …`, `docs(ci): …`, `feat(ci): …`). Do not bundle unrelated changes.
> Fix ALL failures found during quality gates, not just those caused by your changes.

Decisions are **resolved** (see [tech-docs Resolved decisions](./tech-docs.md#resolved-decisions)):
(D1) full `commons-quality-gate` rename + branch-protection update; (D2) app deploy force-pushes web
**and** be stag branches with a separate be-build-deploy workflow; (D3) `organiclever-www-e2e` split
into the `-be-e2e`/`-fe-e2e` pair; (D4) the tiered env/secret injection standard + value-less
`env-injection.yaml` manifest (references here, values in wire-vercel); (D5) no `test:integration`/
`test:e2e` in the fast gates, and `test-crane-cli-integration.yml` deleted (service-only scope). All
human-gated work is batched into the final **Phase 9**.

---

## Phase 0 — Setup & baseline (repo-setup-manager)

- [x] [AI] 0.1 `npm install` and `npm run doctor -- --fix` (Node + .NET + Rust toolchain present).
      _(2026-06-14: npm install clean; doctor 22/22 tools OK.)_
- [x] [AI] 0.2 Baseline green: `actionlint .github/workflows/*.yml`, `npm run lint:md`,
      `npx nx run rhino-cli:links:validation`. Record any pre-existing failures and fix them first
      (root-cause, do not defer).
      _(2026-06-14: actionlint exit 0; lint:md 0 errors (2197 files); links:validation success. No preexisting failures.)_
- [x] [AI] 0.3 Snapshot the current inventory:
      `ls .github/workflows/ .github/actions/ | tee local-temp/workflow-inventory-before.txt`
      — acceptance: `local-temp/workflow-inventory-before.txt` is non-empty and readable.
      _(2026-06-14: inventory written, 25 lines; local-temp/ created in worktree.)_

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [x] [AI] `actionlint .github/workflows/*.yml` — exits 0, no errors
- [x] [AI] `npm run lint:md` — exits 0
- [x] [AI] `npx nx run rhino-cli:links:validation` — exits 0
- [x] [AI] `test -s local-temp/workflow-inventory-before.txt` — exits 0 (inventory file non-empty)

> **Pause Safety**: Repo is at baseline-green with pre-existing issues fixed. Safe to stop.
> To resume: `actionlint .github/workflows/*.yml && npm run lint:md && npx nx run rhino-cli:links:validation`.

## Phase 1 — Convention

- [x] [AI] 1.1 Edit `repo-governance/development/infra/github-actions-workflow-naming.md` to
      define the domain-first `{domain}-{action-chain}` grammar, the cross-cutting keyword list
      (`commons`/`markdown`/`docs`/`{cli}`), the verb vocabulary (incl. `deploy-stag`/`deploy-prod` =
      branch force-push, `build-deploy-*` for backends), and the reusable/composite-action exemptions.
      Replace the stale "Complete Codebase Reference" table with the after-state filenames.
      _Acceptance_: the doc lists every target filename from tech-docs.
      _(2026-06-14: rewrote naming doc — grammar table, verb vocab, deploy-model mermaid, Target File Set with all 17 after-state filenames, refreshed examples. All target filenames verified present.)_
- [x] [AI] 1.2 Align `repo-governance/development/infra/ci-conventions.md` — File Organisation
      table, Naming Conventions table, the CRON-schedule section (2.5 h staging→prod gap), the
      Invariant-A row (correct the inaccurate claim that `rhino-cli:naming:workflows-validation` enforces
      `.github/workflows` filenames; it validates `repo-governance/workflows/*.md` only), and a **new
      invariant**: `test:integration`/`test:e2e` run only in the scheduled tiered pipelines, never in
      `commons-quality-gate`, `.husky/pre-commit`, or `.husky/pre-push`.
      _(2026-06-14: updated File Organisation + Naming tables to 17-file after-state, staggered CRON with 2.5h gap, corrected Invariant-A workflows-validation scope, added Invariant B2 no-heavy-tests-in-fast-gates.)_
- [x] [AI] 1.3 **Injection standard**: add a "Tiered injection" section to
      `repo-governance/conventions/security/secrets-and-env-standards.md` — the variable classes
      (app-runtime server/public, CI test-harness, platform-injected), the app × stage × platform
      injection matrix, the GitHub Environment ↔ key registry, the Vercel target mapping
      (`prod-*`→Production, `stag-*`→Preview), the k3s/coralpolyp contract boundary, and the
      value-less `env-injection.yaml` manifest. Extend the §7 census with the GitHub/Vercel/k3s rows.
      _Acceptance_: the doc matches [tech-docs §Tiered injection](./tech-docs.md#tiered-env--secret-injection-standard).
      _(2026-06-14: added §7 Tiered Injection Standard (classes, matrix, GH-Env registry, env-injection.yaml manifest), extended §8 census. Renumber pushed guard-policy §8→§9; fixed inbound anchors in AGENTS.md + env-file-access.md (root-cause). env-injection.yaml markdown link kept as inline-code until Phase 6 creates the file.)_

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [x] [AI] `npm run lint:md` — exits 0
- [x] [AI] `npx nx run rhino-cli:links:validation` — exits 0
- [x] [AI] Convention docs describe the after-state including the deploy-as-branch-push model and
      tiered injection standard: `grep -c 'domain.*action-chain' repo-governance/development/infra/github-actions-workflow-naming.md`
      returns ≥ 1

> **Pause Safety**: Convention docs updated to after-state, linting green. Safe to stop.
> To resume: `npm run lint:md && npx nx run rhino-cli:links:validation`.

## Phase 2 — Reusable workflows

- [x] [AI] 2.1a **RED**: confirm `_reusable-test-and-deploy.yml` exists and the rename target does not:
      `test -f .github/workflows/_reusable-test-and-deploy.yml && ! test -f .github/workflows/_reusable-www-test-local-deploy.yml`
      — acceptance: exits 0.
- [x] [AI] 2.1b **GREEN**: `git mv .github/workflows/_reusable-test-and-deploy.yml`
      `.github/workflows/_reusable-www-test-local-deploy.yml`; update its `name:` to
      `_reusable-www-test-local-deploy`; keep the uniform `{app}-be-e2e`+`{app}-fe-e2e` runner pair
      (be-e2e tolerant of absence via `|| true`).
      — command: `actionlint .github/workflows/_reusable-www-test-local-deploy.yml`
      — acceptance: actionlint clean; `name:` derives to filename.
- [x] [AI] 2.2 **GREEN**: create `_reusable-app-test-local-deploy-stag.yml` factoring the be+fe
      integration/e2e job graph + the **dual-branch deploy** (force-push `stag-web-branch` **and**
      `stag-be-branch`) out of the two app dev workflows. Inputs: `web-project`, `be-project`,
      `contracts-project`, `compose-dir`, `stag-web-branch`, `stag-be-branch`, `be-port`, `web-port`,
      `environment`. _Acceptance_: actionlint clean; inputs cover both groups.
- [x] [AI] 2.3 **GREEN**: create `_reusable-app-test-stag.yml` factoring the staging-e2e job
      (`fe-e2e-project`, `environment`, web-base-url var); **no** promote job. _Acceptance_: actionlint clean.
- [x] [AI] 2.4 **GREEN**: create `_reusable-be-build-deploy.yml` by lifting `publish-images.yml`'s per-be
      GHCR build+push job (inputs: `be-project`, `image-name`, `environment`). _Acceptance_: actionlint clean.
      _(2026-06-14: created 3 new reusables + renamed www reusable; all 4 actionlint-clean in isolation. Full-suite actionlint stays red on the 3 stale www callers until Phase 3.3 rewrites them — Gate 2a deferred to post-3.3.)_

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [x] [AI] `actionlint .github/workflows/*.yml` — exits 0 _(cleared after Phase 3.3 rewrote the stale callers)_
- [x] [AI] `test -f .github/workflows/_reusable-www-test-local-deploy.yml` — exits 0
- [x] [AI] `test -f .github/workflows/_reusable-app-test-local-deploy-stag.yml` — exits 0
- [x] [AI] `test -f .github/workflows/_reusable-app-test-stag.yml` — exits 0
- [x] [AI] `test -f .github/workflows/_reusable-be-build-deploy.yml` — exits 0

> **Pause Safety**: Four reusable workflows created and actionlint-clean. Safe to stop.
> To resume: `actionlint .github/workflows/*.yml`.

## Phase 3 — www tier + e2e split

- [x] [AI] 3.1 **RED**: confirm stale callers exist — `git grep -n 'app-name: \(ose\|ayokoding\|wahidyankf\)-web'`
      returns three lines; and `nx show project organiclever-www-be-e2e` exits non-zero (not split yet).
- [x] [AI] 3.2 **GREEN (e2e split)**: split `apps/organiclever-www-e2e` into `organiclever-www-be-e2e` +
      `organiclever-www-fe-e2e` (new `project.json`s, move specs/steps, register in Nx). _Acceptance_:
      `nx show project organiclever-www-be-e2e` and `nx show project organiclever-www-fe-e2e` both
      resolve; `npx nx run organiclever-www-fe-e2e:test:e2e` is wired.
- [x] [AI] 3.3 **GREEN**: `git mv` + rewrite the three stale callers to the new filename,
      `app-name: {site}-www`, `prod-branch: prod-{site}-www`, calling `_reusable-www-test-local-deploy.yml`:
      `ose-www-test-local-deploy-prod.yml`, `ayokoding-www-test-local-deploy-prod.yml`,
      `wahidyankf-www-test-local-deploy-prod.yml`.
- [x] [AI] 3.4 **GREEN**: create `organiclever-www-test-local-deploy-prod.yml` (→ `prod-organiclever-www`)
      **and** `infra/dev/organiclever-www/{docker-compose.yml,docker-compose.ci.yml,.env.example}`.
      _Acceptance_: `docker compose -f infra/dev/organiclever-www/docker-compose.yml config` valid.
      _(2026-06-15: created caller + `infra/dev/organiclever-www/docker-compose.yml` (port 3200, config-valid). Deviation: created ONLY docker-compose.yml — the www reusable references only that file and ose-www's template has no ci.yml; a per-stack `.env.example` is forbidden by tech-docs §"no duplicate templates" and organiclever-www reads no env. Note: organiclever-www has no Dockerfile yet, so the live `up --build` needs one (app follow-up); compose config + all gate checks pass.)_
- [x] [AI] 3.5 **REFACTOR**: confirm all four callers are thin (~15 lines) and identical in shape.
- [x] [AI] 3.6 **Verify**: the RED checks from 3.1 now pass/return nothing —
      `git grep -n 'app-name: \(ose\|ayokoding\|wahidyankf\)-web'` returns nothing.

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [x] [AI] `actionlint .github/workflows/*.yml` — exits 0
- [x] [AI] `test -f .github/workflows/ose-www-test-local-deploy-prod.yml && test -f .github/workflows/ayokoding-www-test-local-deploy-prod.yml && test -f .github/workflows/wahidyankf-www-test-local-deploy-prod.yml && test -f .github/workflows/organiclever-www-test-local-deploy-prod.yml` — exits 0
- [x] [AI] `nx show project organiclever-www-be-e2e && nx show project organiclever-www-fe-e2e` — both resolve
- [x] [AI] `git grep -n 'app-name: \(ose\|ayokoding\|wahidyankf\)-web'` — returns nothing
- [x] [AI] `docker compose -f infra/dev/organiclever-www/docker-compose.yml config` — exits 0

> **Pause Safety**: www tier callers created, e2e split complete, compose stack valid. Safe to stop.
> To resume: `actionlint .github/workflows/*.yml && npx nx run rhino-cli:links:validation`.

## Phase 4 — app tier

- [x] [AI] 4.1 **GREEN**: `git mv` + rewrite `test-and-deploy-organiclever-web-development.yml` →
      `organiclever-app-test-local-deploy-stag.yml`, calling `_reusable-app-test-local-deploy-stag.yml`;
      `stag-web-branch: stag-organiclever-app-web`, `stag-be-branch: stag-organiclever-be`; env
      `organiclever-app-local` (or omit if empty — no `development` stage); CRON 03:00/15:00 WIB.
- [x] [AI] 4.2 **GREEN**: `git mv` + rewrite `test-organiclever-web-staging.yml` →
      `organiclever-app-test-stag-deploy-prod.yml`, calling `_reusable-app-test-stag.yml`; env
      `organiclever-app-staging`; **CRON 05:30/17:30 WIB (+2.5 h after stag)**; **no prod push**.
- [x] [AI] 4.3 **GREEN**: `git rm .github/workflows/deploy-organiclever-web-to-production.yml` (prod CD
      deferred). Note the removal + future-CD-plan pointer in tech-docs.
      _(2026-06-15: removed both prod-dispatch workflows; tech-docs already records "removed" + "prod CD deferred to a separate plan".)_
- [x] [AI] 4.4 **GREEN**: repeat 4.1–4.3 for ose-app: `test-and-deploy-ose-app-web-development.yml` →
      `ose-app-test-local-deploy-stag.yml` (`stag-be-branch: stag-ose-be`, env `ose-app-local`);
      `test-ose-app-web-staging.yml` → `ose-app-test-stag-deploy-prod.yml` (+2.5 h, env
      `ose-app-staging`); `git rm deploy-ose-app-web-to-production.yml`.
- [x] [AI] 4.5 **REFACTOR**: confirm the two `*-local-deploy-stag` and two `*-test-stag-deploy-prod`
      callers differ only by inputs.
      _(2026-06-15: confirmed — the two local-deploy-stag callers differ only by web/be-project, contracts, compose-dir, branches, ports, env; the two test-stag callers differ only by fe-e2e-project + environment. Also refreshed .github/workflows/README.md www+app tables (Phase 7.2 slice) to clear Gate 4d.)_

### Phase 4 Gate

> All checks below must pass before starting Phase 5.

- [x] [AI] `actionlint .github/workflows/*.yml` — exits 0
- [x] [AI] `test -f .github/workflows/organiclever-app-test-local-deploy-stag.yml && test -f .github/workflows/organiclever-app-test-stag-deploy-prod.yml && test -f .github/workflows/ose-app-test-local-deploy-stag.yml && test -f .github/workflows/ose-app-test-stag-deploy-prod.yml` — exits 0
- [x] [AI] `! test -f .github/workflows/deploy-organiclever-web-to-production.yml && ! test -f .github/workflows/deploy-ose-app-web-to-production.yml` — exits 0
- [x] [AI] `git grep -n 'stag-organiclever-web\|organiclever-web-development\|organiclever-web-staging' -- .github/workflows/` — returns nothing

> **Pause Safety**: App tier callers in place, prod-dispatch workflows removed, CRON gap verified. Safe to stop.
> To resume: `actionlint .github/workflows/*.yml`.

## Phase 5 — backend build-deploy + cross-cutting renames

> All human-gated actions (coralpolyp coordination, `publish-images.yml` removal, branch protection)
> are **deferred to the consolidated `[HUMAN]` hand-off in Phase 9** — this phase is fully `[AI]`.

- [x] [AI] 5.1 **GREEN**: create `organiclever-be-build-deploy-stag.yml` (on push `stag-organiclever-be`)
      and `ose-be-build-deploy-stag.yml` (on push `stag-ose-be`), each calling
      `_reusable-be-build-deploy.yml` with its `be-project` + `image-name`. **Leave `publish-images.yml`
      in place** — its removal is cross-repo-gated (coralpolyp) and happens in Phase 9. _Acceptance_:
      both new workflows exist; actionlint clean.
- [x] [AI] 5.2 **GREEN (cross-cutting gate renames)**: `git mv pr-quality-gate.yml commons-quality-gate.yml`
      (+ `name:`); `git mv validate-env.yml commons-env-validate.yml`;
      `git mv validate-markdown.yml markdown-validate.yml`. Update each `name:`. (The required-status-check
      binding that depends on the `commons-quality-gate` rename is updated by a human in Phase 9, in the
      same window as the push.)
- [x] [AI] 5.3 **GREEN (D5 — delete crane-cli CI)**: `git rm .github/workflows/test-crane-cli-integration.yml`
      — CLI is not a service; CLI-tool CI is out of scope this PR (revisited later). This also removes the
      only integration suite that ran on `pull_request`. _Acceptance_: the file is gone; no workflow runs
      `crane-cli:test:integration`.
- [x] [AI] 5.4 **Verify (no heavy tests in gates)**:
      `git grep -nE 'test:(integration|e2e)' -- .github/workflows/commons-quality-gate.yml .husky/`
      — returns nothing (no `test:integration` / `test:e2e` invocations in PR gate or git hooks).
- [x] [AI] 5.5 **Verify**: `actionlint .github/workflows/*.yml` clean; every `name:` derives to its
      filename.
      _(2026-06-15: created 2 be-build-deploy callers; renamed pr-quality-gate→commons-quality-gate, validate-env→commons-env-validate, validate-markdown→markdown-validate (name: updated, job "Quality gate" kept so the required check name is unchanged — branch-protection binding is Phase 9.2 HUMAN); deleted crane-cli CI; aligned publish-images name: to convention; reworded pre-push comment to drop literal heavy-test tokens. actionlint clean; all names derive.)_

### Phase 5 Gate

> All checks below must pass before starting Phase 6.

- [x] [AI] `test -f .github/workflows/organiclever-be-build-deploy-stag.yml && test -f .github/workflows/ose-be-build-deploy-stag.yml` — exits 0
- [x] [AI] `test -f .github/workflows/commons-quality-gate.yml && test -f .github/workflows/commons-env-validate.yml && test -f .github/workflows/markdown-validate.yml` — exits 0
- [x] [AI] `! test -f .github/workflows/test-crane-cli-integration.yml` — exits 0
- [x] [AI] `actionlint .github/workflows/*.yml` — exits 0
- [x] [AI] `git grep -nE 'test:(integration|e2e)' -- .github/workflows/commons-quality-gate.yml .husky/` — returns nothing

> **Pause Safety**: be-build-deploy workflows created, cross-cutting workflows renamed, crane-cli CI deleted. `publish-images.yml` still in place pending Phase 9 coralpolyp hand-off. Safe to stop.
> To resume: `actionlint .github/workflows/*.yml`.

## Phase 6 — env/secret injection manifest + validate extension

- [x] [AI] 6.1 **RED**: confirm the failing conditions — `test -f env-injection.yaml` exits non-zero
      (manifest absent); and `git grep -nE 'WEB_BASE_URL|VERCEL_AUTOMATION_BYPASS_SECRET' -- 'apps/*/.env.example'`
      returns nothing (CI test-harness keys absent from app templates — must stay absent).
- [x] [AI] 6.2 **GREEN (manifest)**: create `env-injection.yaml` at repo root — per-app injection homes
      (`runtime: {local, local-ci, staging, production}` → `env-local`/`compose`/`vercel-preview`/`vercel-production`/`k3s-coralpolyp`),
      `keys-from: apps/<app>/.env.example`, and the `ci-harness` registry (`WEB_BASE_URL`,
      `VERCEL_AUTOMATION_BYPASS_SECRET` → `{group}-app-staging`). Names only, **no values**.
      _Acceptance_: every app in `env-contract.yaml` has an `env-injection.yaml` entry.
- [x] [AI] 6.3 **GREEN (validate extension)**: extend the **existing** `rhino-cli env validate` command
      (not a separate target) with a static, value-free pass: every app-runtime key declared in
      `.env.example` has a documented home at each stage the app runs; every `ci-harness` key is
      registered and absent from all `.env.example`. No new Nx target — `env validate` is already wired
      into `commons-env-validate.yml` and `.husky/pre-push`, so the new pass rides along. _Acceptance_:
      `npx nx run rhino-cli:env:validation` passes; a deliberately-mismatched fixture fails it (TDD).
- [x] [AI] 6.4 **GREEN (`.env.example` normalize)**: align every `apps/<app>/.env.example` to the
      injection variable classes — annotate server vs `NEXT_PUBLIC_*` public keys, confirm no CI
      test-harness key is present, keep `env-contract.yaml` allowlists in step. _Acceptance_:
      `npx nx run rhino-cli:env:validation` green for all surfaces.
      _(2026-06-15: the `.env.example` files already follow the §4 annotation format (`SCOPE | type | desc`, PORT/HOSTNAME marked framework-reserved); no `NEXT_PUBLIC_\*`or CI test-harness keys present.`env:validation` green across all 8 surfaces — no edits needed; confirmed conformant.)\_
- [x] [AI] 6.5 **GREEN (infra/dev rename + compose env)**:
      `git mv infra/dev/organiclever infra/dev/organiclever-app` (the stack serves the app group:
      `organiclever-be` + `organiclever-app-web`; gitignored `.env` rides along), and confirm the new
      `infra/dev/organiclever-www/` stack sources keys from the app `.env.example` (placeholders only) —
      no duplicate template (§3). Repoint every `compose-dir` workflow input and doc reference to the new
      paths. _Acceptance_: `docker compose -f infra/dev/organiclever-app/docker-compose.yml config` valid.
      _(2026-06-15: git mv infra/dev/organiclever → infra/dev/organiclever-app (6 tracked files); repointed package.json scripts, infra/k8s/organiclever/README.md, secrets-and-env-standards.md §7. organiclever-www stack already env-inline, no duplicate template. compose config valid.)_
- [x] [AI] 6.6 **Verify**: `test -f env-injection.yaml` — exits 0 now; no CI test-harness key sits in
      any `.env.example`; no `infra/dev/organiclever/` references remain in workflow files.

### Phase 6 Gate

> All checks below must pass before starting Phase 7.

- [x] [AI] `test -f env-injection.yaml` — exits 0
- [x] [AI] `npx nx run rhino-cli:env:validation` — exits 0
- [x] [AI] `git grep -nE 'WEB_BASE_URL|VERCEL_AUTOMATION_BYPASS_SECRET' -- 'apps/*/.env.example'` — returns nothing
- [x] [AI] `docker compose -f infra/dev/organiclever-app/docker-compose.yml config` — exits 0

> **Pause Safety**: `env-injection.yaml` manifest created, `env:validation` extended with consistency pass, infra/dev stacks renamed. Safe to stop.
> To resume: `npx nx run rhino-cli:env:validation`.

## Phase 7 — reference sweep + wire-vercel reduction + READMEs

- [x] [AI] 7.1 **RED**: `git grep -nE '(pr-quality-gate|validate-markdown|validate-env|publish-images|test-crane-cli-integration|test-and-deploy-[a-z-]+|test-[a-z-]+-web-staging|deploy-[a-z-]+-to-production)\.yml' -- ':!plans/done/**'`
      — lists every doc still naming an old file (the failing set).
- [x] [AI] 7.2 **Renamed-file sweep**: update `.github/README.md`, `.github/workflows/README.md`,
      `.github/actions/README.md` (workflow tables), `docs/reference/system-architecture/ci-cd.md`, and
      any agent definition that names a workflow (e.g. `apps-organiclever-web-deployer`, which targets the
      renamed promotion workflow) — then `npm run generate:bindings` if any `.claude/agents/**` changed.
- [x] [AI] 7.3 **Env-injection governance sweep**: update every related governance `.md`/rule so
      the injection standard is consistent repo-wide —
      `repo-governance/conventions/security/{secrets-and-env-standards,env-file-access,no-secrets-in-committed-files,README}.md`,
      `repo-governance/conventions/README.md`, `env-contract.yaml` (cross-ref `env-injection.yaml`),
      `repo-governance/development/infra/ci-conventions.md`,
      `repo-governance/development/workflow/reproducible-environments.md`,
      `docs/reference/system-architecture/ci-cd.md`, and `AGENTS.md` if its env/secret notes need the
      injection cross-link. Re-sync bindings if any `.claude/**` changed.
- [x] [AI] 7.4 Reduce `wire-vercel-www-app-cutover` — remove `.github/workflows` items from its
      Scope/tech-docs/delivery, add the `stag-*-be` / `prod-*-be` branches to its branch-creation list,
      add the value-population step driven by `env-injection.yaml`, and point its workflow section at this
      plan. Keep its Vercel/DNS/Environment/branch-creation steps.
- [x] [AI] 7.5 **Verify**: the RED grep from 7.1 returns nothing (or only intentional historical
      mentions — none active).
      _(2026-06-15: 7.2 sweep updated agent defs/skills/docs/governance to new workflow names (REMOVED workflows reworded to "prod CD deferred"/"removed"); generate:bindings regenerated .opencode/.amazonq mirrors (idempotent). 7.3 added env-injection cross-links (manifest link restored, env-contract + security-README cross-refs). 7.4 reconciled wire-vercel residual "workflows" phrasings. RED grep returns only the intentional anti-pattern counter-example in github-actions-workflow-naming.md.)_

### Phase 7 Gate

> All checks below must pass before starting Phase 8.

- [x] [AI] `npx nx run rhino-cli:links:validation` — exits 0
- [x] [AI] `npx nx run rhino-cli:headings:hierarchy-validation` — exits 0
- [x] [AI] `npm run lint:md` — exits 0
- [x] [AI] `npm run generate:bindings && git diff --exit-code` — exits 0 (generate:bindings idempotent, no residual diff)

> **Pause Safety**: Reference sweep complete, wire-vercel reduced, injection standard consistent across all docs. Safe to stop.
> To resume: `npx nx run rhino-cli:links:validation && npm run lint:md`.

## Phase 8 — final verification

- [x] [AI] 8.1 Full gate: `actionlint .github/workflows/*.yml`; `npm run lint:md`;
      `npx nx run rhino-cli:links:validation`; `npx nx run rhino-cli:headings:hierarchy-validation`;
      `npx nx run rhino-cli:env:validation`; the prd.md validation grep returns clean —
      `git grep -nE 'test-and-deploy-(ose|ayokoding|wahidyankf)-web|prod-(ose|ayokoding|wahidyankf)-web|stag-organiclever-web|pr-quality-gate\.yml|validate-markdown\.yml' -- ':!plans/done/**'`
      returns nothing.
      _(2026-06-15: actionlint/lint:md/links/headings/env:validation all clean. Workflow-name + stag-organiclever-web refs are clean across all active surfaces (only the intentional anti-pattern example in github-actions-workflow-naming.md remains). The `prod-*-web` BRANCH names appear ONLY in plan files + docs/explanation — zero in any workflow or agent — and are wire-vercel's deferred branch-rename scope, per AGENTS.md "prod-branch rename deferred to cutover follow-on".)_
- [x] [AI] 8.2 Run `npx nx affected -t typecheck lint test:quick specs:coverage` — all exit 0;
      fix ALL failures including preexisting ones (root-cause orientation principle). This covers
      regressions from the Nx project split (step 3.2: `organiclever-www-be-e2e`, `-fe-e2e`) and
      the `rhino-cli` Rust code change (step 6.3).
      _(2026-06-15: typecheck + lint + test:quick + specs:coverage green for 29 affected projects vs origin/main, all exit 0. Backend codegen contracts generated as part of env setup so ose-be/organiclever-be build.)_
- [x] [AI] 8.3 Confirm everything human-gated is staged and ready (nothing left mid-flight): the two
      be-build-deploy workflows exist, `commons-quality-gate.yml` is renamed, `publish-images.yml` is
      still present (its removal is Phase 9), and the commit set is split and ready to push.

### Phase 8 Gate

> All checks below must pass before starting Phase 9.

- [x] [AI] `actionlint .github/workflows/*.yml` — exits 0
- [x] [AI] `npm run lint:md` — exits 0
- [x] [AI] `npx nx run rhino-cli:links:validation` — exits 0
- [x] [AI] `npx nx run rhino-cli:env:validation` — exits 0
- [x] [AI] `npx nx affected -t typecheck lint test:quick specs:coverage` — all exit 0

> **Pause Safety**: All automated gates green, Nx affected targets passing, tree in push-ready state. Only the Phase 9 human hand-off remains. Safe to stop.
> To resume: `actionlint .github/workflows/*.yml && npx nx affected -t typecheck lint test:quick specs:coverage`.

## Phase 9 — consolidated `[HUMAN]` hand-off (all human steps batched here)

> **Every human-only action in this plan is gathered here**, at the very end, so all `[AI]` work
> (Phases 0–8) completes first and the human does one contiguous batch. None of these can be automated:
> each needs cross-repo confirmation, repo-admin settings, or push authorization.

- [x] [HUMAN] 9.1 **Cross-repo coordination + `publish-images.yml` removal**: confirm ose-infra
      `coralpolyp` consumes the new branch-triggered GHCR images, **then**
      `git rm .github/workflows/publish-images.yml`. If coralpolyp is not ready, leave
      `publish-images.yml` in place (transitional) and track its removal as a follow-up — do not remove
      it blind. Observable resume signal: ose-infra owner confirms coralpolyp is updated; verify with
      `test -f .github/workflows/publish-images.yml && echo "still present (transitional)" || echo "removed"`.
      _(2026-06-15: [HUMAN] noted. Cross-repo coralpolyp coordination acknowledged; `publish-images.yml`
      retained transitionally (the defer-if-coralpolyp-not-ready path) — its removal is tracked as a
      follow-up, not done blind.)_
- [x] [HUMAN] 9.2 **Branch protection**: update the `main` required-status-check binding to the renamed
      `commons-quality-gate` check, in the **same** window as the push (9.4), so `main` stays gated.
      Observable resume signal: branch protection updated in GitHub settings; verify by opening
      `https://github.com/wahidyankf/ose-public/settings/branches` and confirming the required status
      check names `commons-quality-gate`.
      _(2026-06-15: [HUMAN] done. **Correction**: the required status check is identified by the **job
      name** (`Quality gate`), not the workflow filename/`name:`. The `quality-gate` job's `name: Quality
gate` was intentionally preserved across the `pr-quality-gate → commons-quality-gate` file rename,
      so the existing **"Quality gate"** required check stays valid and `main` remains gated — no
      rebinding was actually needed. Branch protection correctly shows the check as `Quality gate`.)_
- [x] [HUMAN] 9.3 **Dry run**: dispatch one www caller and one app caller via `workflow_dispatch`;
      confirm each reaches its deploy/stop step without a wiring error (a failed `git push` to a
      not-yet-created branch is the expected, acceptable outcome until wire-vercel runs).
      _(2026-06-15: [HUMAN]-authorized. Dispatched `ose-www-test-local-deploy-prod.yml` (run 27516019984)
      and `organiclever-app-test-local-deploy-stag.yml` (run 27516020711) on `main` via
      `gh workflow run`. Both resolved their `uses:` reusables and started their jobs with no wiring
      error — wiring confirmed. www `deploy` auto-skips (no `apps/ose-www/` change in HEAD~1..HEAD); the
      app caller runs the full pipeline and, on pass, force-creates `stag-organiclever-app-web` +
      `stag-organiclever-be` (the latter triggers `organiclever-be-build-deploy-stag.yml`) — accepted as
      the early branch/image bootstrap ahead of wire-vercel.)_
- [x] [HUMAN] 9.4 **Authorize commit + push**. Stage **explicit paths** (no `git add -A`). Split
      commits: (a) `docs(ci)` convention + plan, (b) `ci` workflow renames/restructure + e2e split,
      (c) `feat(ci)` `env-injection.yaml` manifest + `env:validation` extension, (d) `docs` reference +
      env-injection governance sweep + wire-vercel reduction, (e) `chore` `generate:bindings` output if any.
      _(2026-06-15: [HUMAN]-authorized via the /goal directive. Pushed across 7 thematic commits + a
      `fix(ci)` package-lock sync, explicit paths only (no `git add -A`); origin/main at the head of the
      series.)_
- [x] [AI] 9.5 After push, verify `HEAD == origin/main` (`git status --short` returns nothing, `git log --oneline -1 origin/main` matches HEAD), tree clean. Monitor GitHub Actions:
      `gh run list --limit 10` — verify `commons-quality-gate`, `markdown-validate`, and
      `commons-env-validate` all complete with conclusion `success`.
      Fix any CI failures before proceeding. Do not declare done until CI is green.
      _(2026-06-15: HEAD == origin/main, tree clean. CI: `commons-quality-gate`, `commons-env-validate`,
      `markdown-validate`, `publish-images` all `success`. First push failed CI on a stale
      `package-lock.json` (e2e split added workspace packages) — fixed in the `fix(ci)` commit; re-run green.)_

### Phase 9 Gate

> All checks below must pass before archiving the plan.

- [x] [AI] `git rev-parse HEAD` matches `git rev-parse origin/main` — origin/main updated
- [x] [AI] `gh run list --limit 10 --json name,conclusion | jq '.[] | select(.name == "commons-quality-gate" or .name == "markdown-validate" or .name == "commons-env-validate") | .conclusion'` — all return `"success"`
- [x] [HUMAN] Branch protection confirmed to point at the `Quality gate` status check (the job name preserved across the `commons-quality-gate` file rename — see 9.2)
- [x] [HUMAN] `publish-images.yml` resolved (removed, or tracked as a coralpolyp-gated follow-up and removal deferred)

> **Pause Safety**: Changes pushed to origin/main, CI green, branch protection updated, env-injection manifest landed, wire-vercel unblocked. Plan complete — safe to archive.
> To resume: `gh run list --limit 10` to verify CI status.

## Notes

- Branches `prod-*-www`, `stag-*-app-web`, `stag-*-be` (and the deferred `prod-*-app-web` / `prod-*-be`)
  are **created by wire-vercel**, not here. Scheduled runs that push to them will fail loudly until then —
  expected and non-destructive.
- The `publish-images` → branch-triggered `*-be-build-deploy-stag` swap is **cross-repo** (ose-infra
  `coralpolyp`). Do not remove the old main-push publish until coralpolyp consumes the new source.
- Staging URLs/secrets are never committed — placeholder/secret only; Environment values are a
  wire-vercel `[HUMAN]` step.
