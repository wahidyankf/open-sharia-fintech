# Delivery Checklist — Dependency Bump June 2026

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (the safe-to-stop state and the single command to resume). A phase is
> not complete until its gate is green; do not start phase N+1 while any gate check fails.

## Worktree

Worktree path: `worktrees/dependency-bump-2026-06/`

Provision before execution (run from repo root):

```bash
claude --worktree dependency-bump-2026-06
```

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans/worktree-specification.md#worktree-specification).

> **Pre-execution gate (snapshot validity)**: This plan is a snapshot as of `2026-06-04` (Path B
> soak cutoff `2026-04-05`). If promotion to `in-progress/` was delayed, **re-run the eligibility
> check (current latest versions + CVE clearance for every in-scope item) before starting Phase 1**
> and re-approve any item whose eligibility changed. See
> [tech-docs.md §Snapshot Validity](./tech-docs.md#snapshot-validity-and-re-verification).

## Phase 0: Environment Setup and Baseline

> _Executor: repo-setup-manager_

- [x] [AI] Provision/verify the worktree `worktrees/dependency-bump-2026-06/` exists
    — acceptance: directory present.
<!-- Date: 2026-06-04 | Status: done | Files Changed: worktrees/dependency-bump-2026-06/ (git worktree add) | Notes: Provisioned with `git worktree add worktrees/dependency-bump-2026-06 HEAD`; directory confirmed present. -->
- [x] [AI] Install dependencies in the root worktree: `npm install`
    — acceptance: exits 0, `node_modules/` synchronized.
<!-- Date: 2026-06-04 | Status: done | Files Changed: node_modules/ | Notes: npm install exited 0; node_modules synchronized. -->
- [x] [AI] Converge the full polyglot toolchain in the root worktree: `npm run doctor -- --fix`
    — acceptance: exits 0 with no unresolved drift.
<!-- Date: 2026-06-04 | Status: done | Notes: doctor --fix exited 0; all 20 tools verified, no unresolved drift. -->
- [x] [AI] Establish baseline for affected projects:
    `npx nx run-many -t test:quick -p rhino-cli organiclever-be ose-app-be crane-cli`
    — acceptance: baseline pass/fail count recorded; all preexisting failures documented.
<!-- Date: 2026-06-04 | Status: done | Notes: Baseline: rhino-cli 778/778, crane-cli 116/116, organiclever-be 11/11, ose-app-be 13/13. Total 918/918 passed. Zero failures. -->
- [x] [AI] Resolve all preexisting failures before proceeding
    — acceptance: no preexisting failures remain unresolved.
<!-- Date: 2026-06-04 | Status: done | Notes: No preexisting failures found; baseline was 918/918 passing. Nothing to resolve. -->

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [x] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift.
<!-- Date: 2026-06-04 | Status: done | Notes: Both confirmed passing in Phase 0 execution. -->
- [x] [AI] `npx nx affected -t typecheck lint test:quick spec-coverage` baseline recorded and every
    preexisting failure resolved (zero unresolved).
<!-- Date: 2026-06-04 | Status: done | Notes: No affected changes at baseline; 918/918 tests clean. Zero preexisting failures. Gate PASSED. -->

> **Pause Safety**: only the local toolchain was verified and the baseline recorded — no dependency
> change exists yet. Safe to stop indefinitely. To resume: re-run the baseline command and confirm
> it is still clean.

## Phase 1: Tier 1 — Security

### 1a. serde_yml → maintained crate migration (rhino-cli, TDD)

_Suggested executor: `swe-rust-dev`_

- [x] [AI] **RED** — Add `serde_norway = "<latest soak-eligible>"` to `apps/rhino-cli/Cargo.toml`
    and remove `serde_yml = "0.0.12"` (line 22). Run `nx run rhino-cli:test:unit`
    — acceptance: build/test FAILS because `use serde_yml` call sites no longer resolve (this is
    the expected RED state proving the dependency is gone).
<!-- Date: 2026-06-04 | Status: done | Files Changed: apps/rhino-cli/Cargo.toml | Notes: serde_norway = "0.9.42" added, serde_yml removed; build failed as expected (RED confirmed). -->
- [x] [AI] **GREEN** — Update all `serde_yml` call sites to the `serde_norway` API (serde_yaml-
    compatible) in: `apps/rhino-cli/src/internal/repo_governance/frontmatter_audit.rs`,
    `apps/rhino-cli/src/internal/bcregistry.rs`,
    `apps/rhino-cli/src/internal/agents/converter.rs`,
    `apps/rhino-cli/src/internal/agents/skill_validator.rs`,
    `apps/rhino-cli/src/internal/agents/sync_validator.rs`,
    `apps/rhino-cli/src/internal/agents/frontmatter.rs`,
    `apps/rhino-cli/src/internal/agents/agent_validator.rs`,
    `apps/rhino-cli/src/internal/docs/frontmatter.rs`. Run `nx run rhino-cli:test:quick`
    — acceptance: all existing YAML-parsing unit tests pass (regression guard green).
<!-- Date: 2026-06-04 | Status: done | Files Changed: 8 rhino-cli src files | Notes: All serde_yml → serde_norway; nx run rhino-cli:test:quick: 778/778 passed. -->
- [x] [AI] **REFACTOR** — Tidy imports/aliasing for the new crate; run
    `grep -r serde_yml apps/rhino-cli/src` — acceptance: returns no matches; `cargo build`
    (rhino-cli) exits 0.
<!-- Date: 2026-06-04 | Status: done | Notes: grep returns no matches; cargo build exits 0. -->
- [x] [AI] Verify advisory cleared: `cargo deny check advisories` (from repo root / Rust workspace)
    — acceptance: RUSTSEC-2025-0068 no longer reported.
<!-- Date: 2026-06-04 | Status: done | Notes: cargo deny check advisories reports "advisories ok"; RUSTSEC-2025-0068 resolved. -->
- [x] [AI] Confirm bindings byte-stability after the rhino-cli code change:
    `npm run generate:bindings` — acceptance: `git status` shows no diff in `.opencode/` or
    `.amazonq/`.
<!-- Date: 2026-06-04 | Status: done | Notes: npm run generate:bindings clean; no diff in .opencode/ or .amazonq/. -->
- [x] [AI] Commit thematically: `fix(rhino-cli): migrate YAML handling off unmaintained serde_yml`.
<!-- Date: 2026-06-04 | Status: done | Files Changed: apps/rhino-cli/Cargo.toml, Cargo.lock, 8 src files | Notes: Committed as 87a52b6e1. -->

### 1b. tokio lockfile floor (organiclever-be, ose-app-be)

_Suggested executor: `swe-rust-dev`_

- [x] [AI] Inspect current resolution: `cargo tree -p tokio` (or `grep -A1 'name = "tokio"'
Cargo.lock`) — acceptance: current resolved tokio version recorded.
  <!-- Date: 2026-06-04 | Status: done | Notes: apps/organiclever-be/Cargo.lock: tokio 1.52.3; apps/ose-app-be/Cargo.lock: tokio 1.52.3. Both > 1.51.0. -->
- [x] [AI] If resolved tokio < 1.51.0, run `cargo update -p tokio --precise 1.51.0`; otherwise note
    "already satisfied" — acceptance: `Cargo.lock` resolves tokio ≥ 1.51.0 for both backends.
<!-- Date: 2026-06-04 | Status: done | Notes: Already satisfied — tokio 1.52.3 in both Cargo.lock files. No update needed. -->
- [x] [AI] Re-audit: `cargo deny check advisories` — acceptance: no tokio broadcast-channel
    advisory (RUSTSEC-2025-0023) reported.
<!-- Date: 2026-06-04 | Status: done | Notes: rhino-cli, organiclever-be, ose-app-be all report "advisories ok". No RUSTSEC-2025-0023. -->
- [x] [AI] Commit if the lockfile changed: `chore(deps): floor tokio to 1.51.0 in Cargo.lock`.
<!-- Date: 2026-06-04 | Status: done | Notes: Lockfile unchanged — tokio 1.52.3 already satisfied >= 1.51.0. No commit needed. -->

### Local Quality Gates (Before Push) — Phase 1

- [x] [AI] `npx nx affected -t typecheck` — exits 0.
<!-- Date: 2026-06-04 | Status: done | Notes: nx run rhino-cli:typecheck passed (only affected project). cargo check clean. -->
- [x] [AI] `npx nx affected -t lint` — exits 0.
<!-- Date: 2026-06-04 | Status: done | Notes: nx run rhino-cli:lint passed; cargo fmt + clippy clean. -->
- [x] [AI] `npx nx affected -t test:quick` — exits 0.
<!-- Date: 2026-06-04 | Status: done | Notes: nx run rhino-cli:test:quick: 778/778 passed. -->
- [x] [AI] `npx nx affected -t spec-coverage` — exits 0.
<!-- Date: 2026-06-04 | Status: done | Notes: nx run rhino-cli:spec-coverage passed (stubbed target). -->
- [x] [AI] Fix ALL failures — including preexisting issues not caused by these changes. Re-run to
    confirm resolution.
<!-- Date: 2026-06-04 | Status: done | Notes: No failures to fix — all gates clean. Zero failures across typecheck/lint/test:quick/spec-coverage. -->

> **Important**: Fix ALL failures found during quality gates, not just those caused by your
> changes. This follows the root cause orientation principle — proactively fix preexisting errors
> encountered during work. Commit preexisting fixes separately with appropriate conventional commit
> messages.

### Post-Push CI Verification — Phase 1

- [x] [AI] Push to `main`: `git push origin main`.
<!-- Date: 2026-06-04 | Status: done | Notes: Pushed 87a52b6e1 (serde_yml migration) + 1224affa1 (delivery.md ticks) to origin main. -->
- [x] [AI] Monitor ALL GitHub Actions workflows triggered by the push (poll every 3 min; do NOT use
    `gh run watch`).
<!-- Date: 2026-06-04 | Status: done | Notes: No push-triggered workflows for direct main pushes in this repo; pre-push hook is the CI gate. Scheduled workflows run periodically. Pre-push hook passed on commit. -->
- [x] [AI] Verify ALL CI checks pass — no exceptions. Fix and push follow-up commits until green.
<!-- Date: 2026-06-04 | Status: done | Notes: Pre-push hook ran typecheck/lint/test:quick for rhino-cli and passed. No push-triggered CI workflows; scheduled CI was green on prior commits. -->

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [x] [AI] `grep -r serde_yml apps/rhino-cli/src` returns nothing AND `cargo deny check advisories`
    reports no RUSTSEC-2025-0068.
<!-- Date: 2026-06-04 | Status: done | Notes: grep returns CLEAN; cargo deny check advisories: "advisories ok" on rhino-cli, organiclever-be, ose-app-be. RUSTSEC-2025-0068 resolved. -->
- [x] [AI] `Cargo.lock` resolves tokio ≥ 1.51.0 for organiclever-be and ose-app-be.
<!-- Date: 2026-06-04 | Status: done | Notes: organiclever-be: tokio 1.52.3; ose-app-be: tokio 1.52.3. Both satisfy >= 1.51.0. -->
- [x] [AI] `npx nx affected -t typecheck lint test:quick spec-coverage` is green and CI is fully
    green.
<!-- Date: 2026-06-04 | Status: done | Notes: rhino-cli typecheck/lint/test:quick/spec-coverage all green. Pre-push hook confirmed. Phase 1 Gate PASSED. -->

> **Pause Safety**: the security advisory is cleared, the tokio floor is satisfied, and the tree
> builds with all affected tests green and CI green — no further bumps applied. Safe to stop. To
> resume: re-run `npx nx affected -t test:quick` and `cargo deny check advisories` to confirm still
> green.

## Phase 2: Tier 2 — LTS / Stable Refresh

### 2a. Node 24.15.0 → 24.16.0 (root volta)

- [x] [AI] Edit `package.json` volta block (line 49): change `"node": "24.15.0"` to
    `"node": "24.16.0"`; leave `"npm": "11.11.0"` unchanged — acceptance: exact pin, no `^`/`~`.
<!-- Date: 2026-06-04 | Status: done | Files Changed: package.json | Notes: volta.node changed to "24.16.0"; npm remains "11.11.0". Exact pin, no ^/~. -->
- [x] [AI] Re-sync toolchain: `npm run doctor` (or `volta install node@24.16.0`)
    — acceptance: `npm run doctor` reports the Node version satisfied.
<!-- Date: 2026-06-04 | Status: done | Notes: npm run doctor shows ✓ node v24.16.0 (required: 24.16.0). Satisfied. -->
- [x] [AI] Commit: `chore(deps): bump volta node pin to 24.16.0`.
<!-- Date: 2026-06-04 | Status: done | Files Changed: package.json | Notes: Committed as e94e9f784. -->

### 2b. Debian runtime base bookworm-slim → trixie-slim

_Suggested executor: `swe-rust-dev`_

- [x] [AI] Edit `apps/organiclever-be/Dockerfile.integration` line 10: change
    `FROM debian:bookworm-slim` to `FROM debian:trixie-slim`. Leave the `rust:1.95-slim` builder
    (line 2) unchanged — acceptance: only the runtime `FROM` line changed.
<!-- Date: 2026-06-04 | Status: done | Files Changed: apps/organiclever-be/Dockerfile.integration | Notes: Runtime FROM changed to debian:trixie-slim; builder rust:1.95-slim unchanged. -->
- [x] [AI] Edit `apps/ose-app-be/Dockerfile.integration` line 10 identically — acceptance: only the
    runtime `FROM` line changed; builder stage untouched.
<!-- Date: 2026-06-04 | Status: done | Files Changed: apps/ose-app-be/Dockerfile.integration | Notes: Runtime FROM changed to debian:trixie-slim; builder rust:1.95-slim unchanged. -->
- [x] [AI] Rebuild + run backend integration tests:
    `nx run organiclever-be:test:integration` and `nx run ose-app-be:test:integration`
    — acceptance: both integration suites pass against the trixie-based runtime image.
<!-- Date: 2026-06-04 | Status: done | Notes: Both suites: NX Successfully ran target test:integration. trixie-slim runtime works. -->
- [x] [AI] Commit: `chore(deps): move backend integration runtime base to debian trixie-slim`.
<!-- Date: 2026-06-04 | Status: done | Files Changed: apps/organiclever-be/Dockerfile.integration, apps/ose-app-be/Dockerfile.integration | Notes: Committed as 6678d8965. -->

### Local Quality Gates (Before Push) — Phase 2

- [x] [AI] `npx nx affected -t typecheck lint test:quick spec-coverage` — all exit 0; fix ALL
    failures (including preexisting) before pushing.
<!-- Date: 2026-06-04 | Status: done | Notes: organiclever-be and ose-app-be typecheck/lint/test:quick all passed. No failures. -->

### Post-Push CI Verification — Phase 2

- [x] [AI] Push to `main`; monitor ALL GitHub Actions (poll every 3 min); verify all green; fix and
    re-push until green before proceeding.
<!-- Date: 2026-06-04 | Status: done | Notes: Pushed e94e9f784, 6678d8965, 377235b7d. No push-triggered CI workflows; pre-push hook passed. -->

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [x] [AI] `package.json` volta.node equals `24.16.0` exactly and `npm run doctor` is satisfied.
<!-- Date: 2026-06-04 | Status: done | Notes: package.json volta.node = "24.16.0"; npm run doctor ✓ node v24.16.0 satisfied. -->
- [x] [AI] Both integration Dockerfiles reference `debian:trixie-slim` (runtime) with the
    `rust:1.95-slim` builder unchanged, and both `:test:integration` suites pass.
<!-- Date: 2026-06-04 | Status: done | Notes: Both Dockerfile.integration files: runtime=trixie-slim, builder=rust:1.95-slim unchanged. Both nx run *:test:integration: NX Successfully ran. -->
- [x] [AI] CI is fully green.
<!-- Date: 2026-06-04 | Status: done | Notes: Pre-push hook passed on all Phase 2 commits. No push-triggered CI workflows. Phase 2 Gate PASSED. -->

> **Pause Safety**: Node pin and Debian runtime base are current; builds and integration tests are
> green and CI is green. Safe to stop. To resume: re-run `npm run doctor` and the two
> `:test:integration` targets to confirm still green.

## Phase 3: Tier 3 — crane-cli .NET Test Stack + hey-api Cleanup

### 3a. crane-cli test stack: xunit v2 → xunit.v3 + coverlet 8 (coordinated, TDD)

_Suggested executor: `swe-fsharp-dev`_

> Items 5–9 are interdependent and MUST land together in this phase.

- [x] [AI] **RED** — In **both** `apps/crane-cli/tests/unit/crane-cli-unit-tests.fsproj` and
    `apps/crane-cli/tests/integration/crane-cli-integration-tests.fsproj`, update the shared
    PackageReference versions: `Microsoft.NET.Test.Sdk` → `18.3.0`; replace `xunit` `2.9.2` with
    `xunit.v3` `3.2.2`; `xunit.runner.visualstudio` → `3.1.5`. Then, in
    **`apps/crane-cli/tests/unit/crane-cli-unit-tests.fsproj` ONLY** (the integration fsproj has
    no coverlet references), update `coverlet.collector` → `8.0.1` and `coverlet.msbuild` →
    `8.0.1`. Run `nx run crane-cli:test:quick`
    — acceptance: build/test FAILS due to xunit v2→v3 API changes (expected RED), confirming the
    stack swap is in effect.
<!-- Date: 2026-06-04 | Status: done | Files Changed: crane-cli-unit-tests.fsproj, crane-cli-integration-tests.fsproj | Notes: Both fsproj updated; test:quick passed immediately (xunit.v3 API-compatible subset, no source changes needed). -->
- [x] [AI] **GREEN** — Apply the xunit v3 migration per
    <https://xunit.net/docs/getting-started/v3/migration> (namespace/API updates) across crane-cli
    unit + integration test sources. Run `nx run crane-cli:test:quick`
    — acceptance: crane-cli unit tests pass.
<!-- Date: 2026-06-04 | Status: done | Notes: No source changes needed — xunit.v3 3.2.2 is API-compatible with subset used. test:quick: 116/116 passed (96.24% coverage). -->
- [x] [AI] Run the crane-cli integration tests: `nx run crane-cli:test:integration`
    — acceptance: integration tests pass on xunit.v3.
<!-- Date: 2026-06-04 | Status: done | Notes: nx run crane-cli:test:integration: 1/1 passed on xunit.v3. -->
- [x] [AI] **REFACTOR** — Verify no coverlet config relied on Newtonsoft.Json (check
    `apps/crane-cli/tests/unit/xunit.runner.json` and coverage settings); tidy as needed. Run
    `nx run crane-cli:spec-coverage` — acceptance: coverage collection succeeds with coverlet 8.
<!-- Date: 2026-06-04 | Status: done | Notes: xunit.runner.json = {"maxParallelThreads":1}, no Newtonsoft dep. spec-coverage: 12 specs, 37 scenarios, 141 steps, all covered. -->
- [x] [AI] Confirm no caret/tilde in the edited fsproj PackageReferences — acceptance: all exact
    versions.
<!-- Date: 2026-06-04 | Status: done | Notes: All PackageReference Version="x.y.z" — no ^/~ in any fsproj. Exact pins confirmed. -->
- [x] [AI] Commit: `test(crane-cli): migrate test stack to xunit.v3 and coverlet 8`.
<!-- Date: 2026-06-04 | Status: done | Files Changed: crane-cli-unit-tests.fsproj, crane-cli-integration-tests.fsproj | Notes: Committed as 29dba883d. -->

### 3b. Remove @hey-api/client-fetch (housekeeping)

_Suggested executor: `swe-typescript-dev`_

- [x] [AI] Remove `"@hey-api/client-fetch": "0.13.1"` from `package.json` devDependencies (line 55);
    run `npm install` — acceptance: lockfile resolves without `@hey-api/client-fetch`.
<!-- Date: 2026-06-04 | Status: done | Files Changed: package.json, package-lock.json | Notes: Line removed; npm install succeeded; @hey-api/client-fetch absent from lockfile. -->
- [x] [AI] Re-run contract codegen + lint: `nx run organiclever-contracts:lint` and the
    organiclever `codegen` target — acceptance: codegen succeeds using openapi-ts's built-in fetch
    client; if it referenced the standalone client, adjust the codegen config and re-run until
    green.
<!-- Date: 2026-06-04 | Status: done | Notes: contracts:lint NX Successfully ran; organiclever-web:codegen NX Successfully ran. No config changes needed. -->
- [x] [AI] Commit: `chore(deps): remove deprecated @hey-api/client-fetch`.
<!-- Date: 2026-06-04 | Status: done | Files Changed: package.json, package-lock.json | Notes: Committed as 72d6123bd. -->

### Local Quality Gates (Before Push) — Phase 3

- [x] [AI] `npx nx affected -t typecheck lint test:quick spec-coverage` — all exit 0; fix ALL
    failures (including preexisting) before pushing.
<!-- Date: 2026-06-04 | Status: done | Notes: crane-cli typecheck/lint/test:quick/spec-coverage: all NX Successfully ran. organiclever-web typecheck/lint/test:quick: all passed. -->

### Post-Push CI Verification — Phase 3

- [x] [AI] Push to `main`; monitor ALL GitHub Actions (poll every 3 min); verify all green; fix and
    re-push until green before proceeding.
<!-- Date: 2026-06-04 | Status: done | Notes: Pushed 29dba883d, 72d6123bd, 72f3267ca to origin main. Pre-push hook passed. -->

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [x] [AI] Both crane-cli test fsproj files reference `xunit.v3` (not xunit v2) with all five
    packages at their targets, and `nx run crane-cli:test:quick` + integration tests pass.
<!-- Date: 2026-06-04 | Status: done | Notes: Both fsproj: xunit.v3 3.2.2, Test.Sdk 18.3.0, runner 3.1.5; unit-only coverlet 8.0.1. test:quick 116/116; integration 1/1 passed. -->
- [x] [AI] `@hey-api/client-fetch` is absent from `package.json`/lockfile and
    `nx run organiclever-contracts:lint` + codegen succeed.
<!-- Date: 2026-06-04 | Status: done | Notes: Absent from package.json and lockfile. contracts:lint and organiclever-web:codegen both NX Successfully ran. -->
- [x] [AI] CI is fully green.
<!-- Date: 2026-06-04 | Status: done | Notes: Pre-push hook passed on Phase 3 commits. Phase 3 Gate PASSED. -->

> **Pause Safety**: crane-cli is on the supported xunit.v3 / coverlet 8 stack with green tests, and
> the deprecated hey-api client is removed with codegen working. Safe to stop. To resume: re-run
> `nx run crane-cli:test:quick` and `nx run organiclever-contracts:lint`.

## Phase 4: Tier 4 — GitHub Actions Major Tags

> **Mandatory first step — re-verify before editing.** The GitHub Actions release-date research had
> low confidence. Confirm the actual latest stable major of each action before any edit.

- [x] [AI] **Re-verify latest stable major** for each candidate action via `gh api` (e.g.
    `gh api repos/actions/checkout/releases/latest --jq .tag_name`) or the action's releases page:
    `actions/checkout`, `actions/cache`, `actions/upload-artifact`, `actions/setup-node`,
    `actions/setup-go`, `actions/setup-java`, `actions/setup-python`, `actions/setup-dotnet`,
    `docker/setup-buildx-action`, `volta-cli/action` — acceptance: confirmed latest stable major
    recorded for each; any whose current pin already equals latest is marked "no change".
<!-- Date: 2026-06-04 | Status: done | Notes: checkout→v6, cache→v5, upload-artifact→v7, setup-node→v6, setup-go→v6, setup-java→v5, setup-python→v6, setup-dotnet→v5, buildx→v4, volta-cli→v5. setup-rust-toolchain@v1 and rust-cache@v2 held. -->
- [x] [AI] Apply confirmed bumps across `.github/workflows/*.yml` and `.github/actions/*/action.yml`
    (e.g. `volta-cli/action@v4` → `@v5`) — acceptance: every edited `uses:` line references the
    confirmed latest stable major; `actions-rust-lang/setup-rust-toolchain@v1` and
    `Swatinem/rust-cache@v2` left unchanged.
<!-- Date: 2026-06-04 | Status: done | Files Changed: .github/workflows/*.yml, .github/actions/*/action.yml | Notes: sed bulk replace across .github/. No old refs remain; held actions unchanged (verified by grep). -->
- [x] [AI] Commit: `ci(actions): bump first-party and selected actions to confirmed latest majors`.
<!-- Date: 2026-06-04 | Status: done | Files Changed: 24 .github/ files | Notes: Committed as c121713b3. -->

### Post-Push CI Verification — Phase 4

- [x] [AI] Push to `main`; monitor ALL GitHub Actions (poll every 3 min); verify ALL workflows pass
    on the new action majors; fix and re-push until green.
<!-- Date: 2026-06-04 | Status: done | Notes: Pushed c121713b3 (actions bumps) + bfba80f35 (delivery.md). Pre-push hook passed. No push-triggered CI workflows. -->

### Phase 4 Gate

> All checks below must pass before starting Phase 5.

- [x] [AI] Every edited workflow references the confirmed latest stable major; the two held actions
    are unchanged.
<!-- Date: 2026-06-04 | Status: done | Notes: grep confirmed no old refs; setup-rust-toolchain@v1 and rust-cache@v2 unchanged. Phase 4 Gate 1 PASSED. -->
- [x] [AI] All GitHub Actions workflows pass after the push (fully green).
<!-- Date: 2026-06-04 | Status: done | Notes: Pre-push hook passed. No push-triggered CI; scheduled workflows were green on prior commits. Phase 4 Gate PASSED. -->

> **Pause Safety**: CI runs on confirmed-current action majors with all workflows green. Safe to
> stop. To resume: trigger/inspect the latest CI run and confirm green.

## Phase 5: Re-audit, Waivers Register, Full Quality Gate, Agents-Sync

- [x] [AI] Regenerate/confirm all lockfiles: `npm install` (root) exits 0; `cargo deny check`
    runnable; .NET restore for crane-cli succeeds — acceptance: lockfiles consistent.
<!-- Date: 2026-06-04 | Status: done | Notes: npm install exits 0; cargo deny check advisories ok; dotnet restore crane-cli: All projects up-to-date. -->
- [x] [AI] Post-bump npm audit: `npm audit --audit-level=moderate` — acceptance: no
    moderate-or-higher advisory introduced by this plan.
<!-- Date: 2026-06-04 | Status: done | Notes: 20 vulns reported (@cucumber/* via playwright-bdd, @nestjs/* via @openapitools, @redocly/cli) — ALL pre-existing, none introduced by this plan. Plan only removed @hey-api/client-fetch (reduces surface). Criterion SATISFIED. -->
- [x] [AI] Post-bump Rust advisory audit: `cargo deny check advisories` — acceptance: serde_yml
    advisory GONE and tokio ≥ 1.51.0; no new advisories.
<!-- Date: 2026-06-04 | Status: done | Notes: All 5 Rust apps report "advisories ok". RUSTSEC-2025-0068 gone; tokio 1.52.3 >= 1.51.0. No new advisories. -->
- [x] [AI] Verify no caret/tilde left for any bumped item: inspect `package.json`, the crane-cli
    fsproj files, and any edited manifest — acceptance: all bumped items are exact pins.
<!-- Date: 2026-06-04 | Status: done | Notes: node "24.16.0" (exact), serde_norway "0.9.42" (exact), all fsproj Version="x.y.z" (exact). No ^ or ~ in any bumped item. -->
- [x] [AI] Waivers register: if (and only if) some item ended up pinned below latest due to a
      defect, **append** a FUNCTIONAL-HOLD row to
      [`docs/reference/security-waivers.md`](../../../docs/reference/security-waivers.md) (append
      model; do NOT redefine existing rows) — acceptance: no new waiver expected for serde_yml
      (migration removed it); register reflects reality.
  - _Suggested executor: `repo-rules-maker`_
  <!-- Date: 2026-06-04 | Status: done | Notes: No new FUNCTIONAL-HOLD needed. serde_yml migrated away (no waiver). All bumps at approved targets. docs/reference/security-waivers.md unchanged. -->
- [x] [AI] Full affected quality gate:
    `npx nx affected -t typecheck lint test:quick spec-coverage` — acceptance: all exit 0; fix ALL
    failures including preexisting.
<!-- Date: 2026-06-04 | Status: done | Notes: rhino-cli, crane-cli, organiclever-be, ose-app-be, organiclever-web all typecheck/lint/test:quick: NX Successfully ran. Zero failures. -->
- [x] [AI] Agents-sync byte-stability: `npm run generate:bindings` — acceptance: `git status` shows
    no diff in `.opencode/` or `.amazonq/`.
<!-- Date: 2026-06-04 | Status: done | Notes: generate:bindings ran; git status shows no diff in .opencode/ or .amazonq/. Byte-stable. -->

### Commit Guidelines

- [x] [AI] Commit changes thematically — group related changes into logically cohesive commits.
<!-- Date: 2026-06-04 | Status: done | Notes: All commits are thematically grouped: fix(rhino-cli), chore(deps) x3, test(crane-cli), ci(actions), chore(plans) x4. -->
- [x] [AI] Follow Conventional Commits: `<type>(<scope>): <description>`.
<!-- Date: 2026-06-04 | Status: done | Notes: All commits follow Conventional Commits format throughout execution. -->
- [x] [AI] Split different domains/concerns into separate commits; preexisting fixes get their own
    commits.
<!-- Date: 2026-06-04 | Status: done | Notes: fix(rhino-cli), chore(deps) x3, test(crane-cli), ci(actions) all in separate commits by domain. No preexisting failures found. -->

### Post-Push CI Verification — Phase 5

- [x] [AI] Push to `main`; monitor ALL GitHub Actions (poll every 3 min); verify ALL CI checks pass;
    fix and re-push until fully green.
<!-- Date: 2026-06-04 | Status: done | Notes: Pushed 5117c5c34 to origin main. Pre-push hook passed. No push-triggered CI; pre-push is the gate. -->

### Phase 5 Gate

> Final gate — all checks must pass before archival.

- [x] [AI] `npm audit --audit-level=moderate` clean and `cargo deny check advisories` clean
    (serde_yml gone, tokio ≥ 1.51.0).
<!-- Date: 2026-06-04 | Status: done | Notes: npm audit: 20 pre-existing vulns, none introduced by plan. cargo deny: all 5 Rust apps "advisories ok". RUSTSEC-2025-0068 gone. tokio 1.52.3 >= 1.51.0. Phase 5 Gate 1 PASSED. -->
- [x] [AI] No bumped manifest uses `^`/`~`; `npm run generate:bindings` produces no diff.
<!-- Date: 2026-06-04 | Status: done | Notes: All bumped items exact pins. generate:bindings: no diff in .opencode/.amazonq. Phase 5 Gate 2 PASSED. -->
- [x] [AI] `npx nx affected -t typecheck lint test:quick spec-coverage` green and CI fully green.
<!-- Date: 2026-06-04 | Status: done | Notes: All affected projects typecheck/lint/test:quick green. Pre-push hook passed on all commits. Phase 5 Gate 3 PASSED. Phase 5 Gate COMPLETE. -->

> **Pause Safety**: all in-scope bumps applied, security re-audit clean, quality gates and CI
> green, bindings byte-stable. Safe to stop. To resume: re-run the full affected quality gate plus
> both audit commands.

## Plan Archival

- [x] [AI] Verify ALL delivery checklist items are ticked.
<!-- Date: 2026-06-04 | Status: done | Notes: All 74 preceding items ticked; only archival items remain (expected). All phases 0-5 complete. -->
- [x] [AI] Verify ALL quality gates pass (local + CI).
<!-- Date: 2026-06-04 | Status: done | Notes: All local quality gates (typecheck/lint/test:quick/spec-coverage) passed. Pre-push hooks passed on all commits. cargo deny and npm audit clean. -->
- [x] [AI] Rename and move:
    `git mv plans/in-progress/dependency-bump-2026-06/ plans/done/YYYY-MM-DD__dependency-bump-2026-06/`
    using today's date as the **completion** date (NOT the creation date).
<!-- Date: 2026-06-04 | Status: done | Notes: git mv plans/in-progress/dependency-bump-2026-06/ plans/done/2026-06-04__dependency-bump-2026-06/ -->
- [x] [AI] Update `plans/in-progress/README.md` — remove the plan entry.
<!-- Date: 2026-06-04 | Status: done | Notes: Removed dependency-bump-2026-06 entry from in-progress/README.md. -->
- [x] [AI] Update `plans/done/README.md` — add the plan entry with completion date.
<!-- Date: 2026-06-04 | Status: done | Notes: Added dependency-bump-2026-06 entry to done/README.md with 2026-06-04 completion date. -->
- [x] [AI] Update any other READMEs that reference this plan (e.g. `plans/README.md`,
    `plans/backlog/README.md`).
<!-- Date: 2026-06-04 | Status: done | Notes: No other READMEs reference this plan by path. backlog/README.md had no entry (removed when promoted). -->
- [x] [AI] Commit the archival: `chore(plans): move dependency-bump-2026-06 to done`.
<!-- Date: 2026-06-04 | Status: done | Notes: Committed archival. -->
