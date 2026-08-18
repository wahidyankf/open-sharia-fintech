# Delivery Checklist — lint-safety-parity (ose-public)

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (the safe-to-stop state and the single command to resume). A phase
> is not complete until its gate is green; do not start phase N+1 while any gate check fails.

## Delivery Mode

**main-to-main** — all work in this plan is committed and pushed directly to `ose-public`'s
`origin main` (no PR, no feature branch). This is the Trunk Based Development default for
`ose-public`. `ose-public` is the upstream source of truth and is NOT bound by the ose-primer
Sync Convention draft-PR invariant (that invariant, and its approved deviation M1, applies only to
the **primer** plan, recorded in the primer plan's tech-docs). Do NOT create a PR for this plan.

> **Planning-only reminder**: This plan's terminal deliverable is the validated five-document
> plan itself. The phases below describe the EXECUTION work that a downstream plan-execution run
> will perform. Authoring this plan does not execute any config change.

## Worktree

Worktree path: `worktrees/lint-safety-parity/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree lint-safety-parity
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest
`origin/main` when missing, syncs with `origin/main` before implementing, and prompts before
deleting the worktree after the plan is archived and pushed.

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans/worktree-specification.md#worktree-specification).

---

## Phase 0: Environment Setup and Baseline

> _Executor: repo-setup-manager_

- [x] [AI] Install dependencies in the root worktree: `npm install`
      — acceptance: exits 0, `node_modules/` synchronized - _Done 2026-06-12: `npm install` exited 0; added 1553 packages, 1571 audited. `node_modules/` synchronized in worktree._
- [x] [AI] Converge the full polyglot toolchain in the root worktree: `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift (verifies .NET SDK ≥ 8 for F# TWAE) - _Done 2026-06-12: doctor reports 20/20 tools OK, 0 warning, 0 missing, "Nothing to fix". dotnet v10.0.300 (≥8 ✓ for TWAE). shellcheck/hadolint/actionlint not yet in converger — added in Phases 2–4._
- [x] [AI] Confirm the F# surface: `find apps libs -name '*.fsproj' | grep -v node_modules`
      — acceptance: lists exactly 8 `.fsproj` files (crane-be ×3, crane-cli ×3, fsharp-crane-core ×2) - _Done 2026-06-12: exactly 8 `.fsproj` found — crane-be (main+integration+unit), crane-cli (main+integration+unit), fsharp-crane-core (main+unit). Matches plan._
- [x] [AI] Confirm no active Go: `find . -name go.mod -not -path '*/node_modules/*' -not -path '*/archived/*'`
      — acceptance: prints nothing (Go only in `archived/`); confirms D10 removal is safe - _Done 2026-06-12: no active `go.mod` outside `archived/`. Confirms D10 removal is safe._
- [x] [AI] Confirm root `.golangci.yml` exists and is unreferenced by workflows/scripts:
      `test -f .golangci.yml && grep -rn 'golangci' .github scripts apps/*/project.json nx.json || true`
      — acceptance: file exists; record every reference found (expected: none active) - _Done 2026-06-12: `.golangci.yml` exists. Only `golangci` matches are in `.github/actions/setup-golang/action.yml` (composite action that installs the golangci-lint **binary**) — no reference to the `.golangci.yml` **config file** itself and no `golangci-lint run` invocation. Deeper safety grep deferred to Phase 1._
- [x] [AI] Record the F# lint baseline: `npx nx run-many -t lint --projects='tag:lang:dotnet'`
      — acceptance: baseline pass/fail recorded for crane-be, crane-cli, fsharp-crane-core - _Done 2026-06-12: all 3 dotnet projects PASS current lint (fantomas --check + fsharplint), 0 warnings each. This is the pre-TWAE baseline — analyzers + TreatWarningsAsErrors not yet active (Phase 5)._
- [x] [AI] Run the affected baseline gate and record it:
      `npx nx affected -t typecheck lint test:quick spec-coverage`
      — acceptance: baseline pass/fail count recorded; all preexisting failures documented - _Done 2026-06-12: `nx affected ... --base=origin/main` → "No tasks were run" (worktree is byte-identical to `origin/main` @ 35485043c, which was double-zero-gated and CI-green when pushed). No preexisting failures in scope._
- [x] [AI] Resolve all preexisting failures before proceeding
      — acceptance: no preexisting failures remain unresolved - _Done 2026-06-12: none to resolve — affected baseline empty and F# lint baseline 0 warnings. Nothing unresolved._

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [x] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift
- [x] [AI] The 8 `.fsproj` files and the dead-but-unreferenced `.golangci.yml` are confirmed
- [x] [AI] `npx nx affected -t typecheck lint test:quick spec-coverage` baseline recorded and every
      preexisting failure resolved (zero unresolved)

> **Pause Safety**: only the local toolchain was verified and the baseline recorded — no feature
> work exists yet. Safe to stop indefinitely. To resume: re-run the baseline command and confirm
> it is still clean.

---

## Phase 1: D10 — Remove dead `.golangci.yml`

> Smallest, lowest-risk change first (a pure deletion).

- [x] [AI] Re-confirm no active Go module references the config:
      `grep -rn 'golangci' .github .husky scripts apps libs nx.json package.json || true`
      — acceptance: no active workflow/script/Nx target references `.golangci.yml` - _Done 2026-06-12: SAFE confirmed. Zero `go.mod` anywhere in repo (Go fully removed). `ayokoding-cli`/`ose-cli` are now Rust (Cargo.toml). No `project.json` lint target invokes golangci-lint. `setup-golang` action installs the binary for 5 workflows (Go/oapi-codegen caching) but the `golang` quality-gate job's `nx run-many --projects='tag:lang:golang'` matches zero projects → `golangci-lint run` never executes. Remaining matches are ayokoding-web educational content + stale Rust-project READMEs (preexisting doc-drift, noted; `.golangci.yml` referenced as inline code, not a link → no link-check breakage)._
- [x] [AI] Delete the dead config: `git rm .golangci.yml`
      — acceptance: `test -f .golangci.yml` returns non-zero (file gone)
  - _Suggested executor: `ci-fixer`_
  - _Done 2026-06-12: `git rm .golangci.yml` → staged deletion; `test -f` returns non-zero (file gone). Trivial deletion executed directly._
- [x] [AI] Run the affected gate to confirm nothing depended on it:
      `npx nx affected -t typecheck lint test:quick spec-coverage`
      — acceptance: exits 0; no job referenced the removed file - _Done 2026-06-12: `nx affected --base=origin/main` → "No tasks were run". `.golangci.yml` is not an Nx project input; nothing depended on it._
- [x] [AI] Commit thematically: `git commit -m "chore(lint): remove dead .golangci.yml (no active Go)"`
      — acceptance: commit created with Conventional Commits format - _Done 2026-06-12: commit `5e664db` "chore(lint): remove dead .golangci.yml (no active Go)" (2 files: deletion + delivery bookkeeping). Pre-commit hooks passed._

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [x] [AI] `test -f .golangci.yml` — expected: non-zero (file removed)
- [x] [AI] `grep -rn 'golangci' .github .husky scripts nx.json` — expected: no active references
      — _Verified 2026-06-12: zero references to the `.golangci.yml` config; only the `setup-golang` action's binary-install lines match (still needed for oapi-codegen), which are not config references._
- [x] [AI] `npx nx affected -t lint` — expected: exits 0

> **Pause Safety**: the dead config is gone and nothing referenced it; the repo lints clean. Safe
> to stop. To resume: `npx nx affected -t lint`.

---

## Phase 2: D7 — Shell lint (shellcheck)

> 14 `.sh` files (excluding `.husky/_/husky.sh` vendored + `archived/**`). Clean-then-gate.

- [x] [AI] **RED**: run shellcheck across tracked shell scripts to surface the existing backlog:
      `shellcheck --severity=warning scripts/*.sh .claude/hooks/*.sh apps/rhino-cli/scripts/*.sh`
      — acceptance: command exits non-zero OR exits 0; record every finding as the cleanup backlog
      (this is the failing-gate state — the gate is not yet wired on)
  - _Suggested executor: `ci-checker`_
  - _Done 2026-06-12: scanned all 14 tracked `.sh` (excl. `husky/_/`vendored +`archived/`) at `--severity=warning` → **exit 0, zero findings**. Backlog is empty — scripts already clean. (shellcheck 0.11.0.)\_
- [x] [AI] **GREEN**: fix every shellcheck `severity=warning` finding in the affected `.sh` files
      (quote variables, fix `SC2086`/`SC2046`-class issues, add justified `# shellcheck disable=`
      with inline rationale only where genuinely needed)
      — command: `shellcheck --severity=warning scripts/*.sh .claude/hooks/*.sh apps/rhino-cli/scripts/*.sh`
      — acceptance: exits 0 (no warning-or-above findings remain)
  - _Suggested executor: `ci-fixer`_
  - _Done 2026-06-12: no fixes needed — RED scan already exits 0. GREEN satisfied vacuously._
- [x] [AI] Create `.shellcheckrc` at repo root with `shell=bash`, `external-sources=true`, and any
      justified repo-wide disables (each with an inline `# rationale:` comment)
      — acceptance: `test -f .shellcheckrc` returns 0; file documents every disable - _Done 2026-06-12: created root `.shellcheckrc` with `shell=bash`, `external-sources=true`, and a documented no-disables rationale (script set clean at warning threshold; severity applied at call site)._
- [x] [AI] **REFACTOR (flip-on)**: wire the shellcheck gate into CI — add a `shell` job to
      `.github/workflows/pr-quality-gate.yml` running
      `shellcheck --severity=warning` over the tracked script set, and register `shell` in the
      `quality-gate` job's `needs:` list and failure-check loop
      — acceptance: workflow YAML parses; the new job is listed in `quality-gate.needs`
  - _Suggested executor: `ci-fixer`_
  - _Done 2026-06-12: added always-run `shell` job (ShellCheck, warning threshold) to `pr-quality-gate.yml` after `format`; scans `git ls-files '*.sh'` minus vendored/archived. Registered `shell` in `quality-gate.needs` and the failure-check loop. (actionlint validation in Phase 4.)_
- [x] [AI] **REFACTOR (flip-on, local)**: add the shellcheck invocation to `.husky/pre-commit` (or
      `pre-push`) scoped to staged/changed `.sh` files
      — acceptance: hook file runs shellcheck; `git commit` on a clean tree succeeds - _Done 2026-06-12: added staged-`.sh` shellcheck snippet to `.husky/pre-commit` (between env-staged check and `rhino-cli git pre-commit`); runs `--severity=warning` on staged scripts when present, skips with a doctor hint otherwise (CI is the hard gate)._
- [x] [AI] Add `shellcheck` to the toolchain converger so `npm run doctor -- --fix` installs it
      (follow the existing doctor pattern; confirm the doctor config path before editing)
      — acceptance: `npm run doctor` reports shellcheck present - _Done 2026-06-12: added `parse_shellcheck_version` (checker.rs), `install_shellcheck` (brew/apt, tools.rs), and a `shellcheck` ToolDef in `tool_defs_infra()` (no version req, compare_exact). Updated the count test 20→21 (renamed `build_returns_all_known_tools`, asserts shellcheck present). Fixed a preexisting clippy `map().unwrap_or(false)` warning in `envbackup.rs` (→ `is_ok_and`) to keep `rhino-cli:lint -D warnings` green. `npm run doctor` → 21/21 OK incl. shellcheck v0.11.0._
- [x] [AI] Commit thematically: `git commit -m "ci(lint): add shellcheck gate (warning threshold)"` - _Done 2026-06-12: commit `83f4525` (gate work + delivery); preexisting clippy fix split into `b630ef5`._

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [x] [AI] `shellcheck --severity=warning scripts/*.sh .claude/hooks/*.sh apps/rhino-cli/scripts/*.sh`
      — expected: exits 0 — _Verified: exit 0 over all 14 tracked scripts._
- [x] [AI] `test -f .shellcheckrc` — expected: exits 0
- [x] [AI] `grep -q 'shell' .github/workflows/pr-quality-gate.yml` and the `shell` job is in
      `quality-gate.needs` — expected: present — _Verified: `shell` in `needs: [detect, format, shell, ...]`._

> **Pause Safety**: shell scripts are clean and the shellcheck gate is live in CI + hooks. Safe to
> stop. To resume: re-run the shellcheck command above.

---

## Phase 3: D6 — Dockerfile lint (hadolint)

> 10 app Dockerfiles under `apps/*/` (incl. 2 `Dockerfile.integration`); exclude `archived/**`.
> Executor confirms whether to also gate `infra/dev/**`. Clean-then-gate.

- [x] [AI] **RED**: run hadolint across app Dockerfiles to surface the backlog:
      `hadolint --failure-threshold warning apps/*/Dockerfile apps/*/Dockerfile.integration`
      — acceptance: record every finding as the cleanup backlog (failing-gate state, gate not wired)
  - _Suggested executor: `ci-checker`_
  - _Done 2026-06-12 (hadolint 2.14.0; scope = 10 apps/\* + 7 infra/dev/\*\* Dockerfiles — infra included for max hygiene). Warning-level backlog: **DL3003** (cd→WORKDIR) ×4 (ayokoding-web, infra ayokoding-cli/ose-cli/rhino-cli cli.dev); **DL3008** (pin apt) ×7 (crane-be, organiclever-be ×2, ose-app-be ×2 + integration, infra organiclever/ose-app be.dev); **DL3018** (pin apk) ×3 (infra cli.dev). Info-level DL3059/DL3015 don't fail at warning threshold. Plan: fix DL3003; ignore version-pinning DL3008/DL3018._
- [x] [AI] **GREEN**: fix every warning-or-above hadolint finding across the Dockerfiles (pin apt
      versions where feasible, fix `DL`-class issues; defer only truly-justified rules to the
      ignore list in the next step)
      — command: `hadolint --failure-threshold warning apps/*/Dockerfile apps/*/Dockerfile.integration`
      — acceptance: exits 0
  - _Suggested executor: `ci-fixer`_
  - _Done 2026-06-12: fixed all 4 DL3003 (`cd`→`WORKDIR`) in ayokoding-web/Dockerfile + infra/dev ayokoding-cli/ose-cli/rhino-cli cli.dev (restore `WORKDIR /app` after the scoped `go mod download`). DL3008/DL3018 ignored via config (next step). hadolint over all 17 apps+infra Dockerfiles → **exit 0** (only info-level DL3059/DL3015 remain, below warning threshold)._
- [x] [AI] Create `.hadolint.yaml` at repo root with `failure-threshold: warning`,
      `trustedRegistries: [docker.io, ghcr.io]`, and justified per-rule `ignore` entries (e.g.
      `DL3008` for dev images), each with an inline rationale comment
      — acceptance: `test -f .hadolint.yaml` returns 0 - _Done 2026-06-12: created `.hadolint.yaml` — `failure-threshold: warning`; `trustedRegistries: [docker.io, mcr.microsoft.com, ghcr.io]` (added mcr for crane-be .NET base images, else DL3026 errors); `ignored: [DL3008, DL3018]` with version-pinning-brittleness rationale._
- [x] [AI] **REFACTOR (flip-on, CI)**: add a `dockerfile` job to
      `.github/workflows/pr-quality-gate.yml` running hadolint over the app Dockerfile set, and
      register `dockerfile` in `quality-gate.needs` + the failure-check loop
      — acceptance: workflow parses; job listed in `quality-gate.needs`
  - _Suggested executor: `ci-fixer`_
  - _Done 2026-06-12: added always-run `dockerfile` job (pins hadolint v2.14.0 binary, auto-discovers `.hadolint.yaml`) after `shell`; lints `git ls-files | grep -i Dockerfile` minus archived. Registered `dockerfile` in `quality-gate.needs` + failure loop. (actionlint parse-check in Phase 4.)_
- [x] [AI] **REFACTOR (flip-on, local)**: add the hadolint invocation to `.husky/pre-commit` scoped
      to changed Dockerfiles
      — acceptance: hook runs hadolint; clean commit succeeds - _Done 2026-06-12: added staged-Dockerfile hadolint snippet to `.husky/pre-commit` (after the shellcheck snippet); runs `--failure-threshold warning` when hadolint present, skips with a doctor hint otherwise._
- [x] [AI] Add `hadolint` to the toolchain converger (doctor `--fix` installs it)
      — acceptance: `npm run doctor` reports hadolint present - _Done 2026-06-12: added `parse_hadolint_version` (checker.rs), `install_hadolint` (brew on macOS, pinned v2.14.0 binary download on Linux), and a `hadolint` ToolDef. Count test 21→22 (+hadolint assertion). `npm run doctor` → 22/22 OK incl. hadolint v2.14.0._
- [x] [AI] Commit thematically: `git commit -m "ci(lint): add hadolint gate (warning threshold)"` - _Done 2026-06-12: commit `181b8e1` (10 files: 4 Dockerfile fixes + .hadolint.yaml + CI job + hook + doctor + delivery)._

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [x] [AI] `hadolint --failure-threshold warning apps/*/Dockerfile apps/*/Dockerfile.integration`
      — expected: exits 0 — _Verified: exit 0 over all 17 apps+infra Dockerfiles (only info-level findings remain)._
- [x] [AI] `test -f .hadolint.yaml` — expected: exits 0
- [x] [AI] `dockerfile` job present in `.github/workflows/pr-quality-gate.yml` `quality-gate.needs`
      — _Verified: `needs: [..., shell, dockerfile, ...]`._

> **Pause Safety**: Dockerfiles are clean and the hadolint gate is live in CI + hooks. Safe to
> stop. To resume: re-run the hadolint command above.

---

## Phase 4: D8 — GitHub Actions lint (actionlint)

> 22 files under `.github/workflows/*.yml`. GitHub-hosted runners → runner-label config optional.
> Clean-then-gate.

- [x] [AI] **RED**: run actionlint across all workflows to surface the backlog:
      `actionlint`
      — acceptance: run from repo root; record every finding as the cleanup backlog (failing-gate
      state, gate not yet wired)
  - _Suggested executor: `ci-checker`_
  - _Done 2026-06-12 (actionlint 1.7.12, 22 workflow files). Backlog — all embedded-shellcheck findings, preexisting: SC2163 (export "$line") in \_reusable-backend-e2e; SC2034 unused `i` in \_reusable-test-and-deploy; SC2034 ×3 dead-code (FAILED/job/RESULT) in pr-quality-gate quality-gate job; SC2129 (grouped redirects) in pr-quality-gate detect + publish-images. No expression/syntax errors. My new `shell`/`dockerfile` jobs parse clean._
- [x] [AI] **GREEN**: fix every actionlint finding in `.github/workflows/*.yml` (invalid
      expressions, shell quoting in `run:` steps, deprecated syntax)
      — command: `actionlint`
      — acceptance: exits 0
  - _Suggested executor: `ci-fixer`_
  - _Done 2026-06-12: SC2163 → inline `# shellcheck disable` w/ rationale (intentional KEY=value export); SC2034 unused `i` → `for _`; SC2034 ×3 → removed dead-code loop in pr-quality-gate quality-gate job (kept the real `contains(needs.\*.result,'failure')`check); SC2129 ×2 → grouped`{ … } >> "$GITHUB*OUTPUT"`. `actionlint` → **exit 0**.*
- [x] [AI] (Optional) Create `.github/actionlint.yaml` only if self-hosted runner labels or
      config-variables need declaring; for `ose-public` (GitHub-hosted) this is likely unnecessary
      — acceptance: either the file is created with documented labels, OR the step is recorded as
      "not needed for ose-public (GitHub-hosted runners)" - _Done 2026-06-12: NOT NEEDED — ose-public CI runs entirely on GitHub-hosted `ubuntu-latest`; no self-hosted runner labels or config-variables to declare. `actionlint` passes with zero config._
- [x] [AI] **REFACTOR (flip-on, CI)**: add an `actions` job to
      `.github/workflows/pr-quality-gate.yml` running `actionlint`, and register `actions` in
      `quality-gate.needs` + the failure-check loop
      — acceptance: workflow parses; job listed in `quality-gate.needs`
  - _Suggested executor: `ci-fixer`_
  - _Done 2026-06-12: added `actions` job (pins actionlint 1.7.12 via the official `download-actionlint.bash`) after `dockerfile`; registered `actions` in `quality-gate.needs`. (The legacy dead-code `for job` loop was removed during GREEN; the real gate check is `contains(needs.*.result,'failure')`, which covers `actions` automatically.) `actionlint` exits 0 including the new job._
- [x] [AI] **REFACTOR (flip-on, local)**: add the actionlint invocation to `.husky/pre-commit`
      scoped to changed workflow files
      — acceptance: hook runs actionlint; clean commit succeeds - _Done 2026-06-12: added staged-workflow actionlint snippet to `.husky/pre-commit` (after the hadolint snippet); lints staged `.github/workflows/*.ya?ml` when actionlint present, skips with a doctor hint otherwise._
- [x] [AI] Add `actionlint` to the toolchain converger (doctor `--fix` installs it)
      — acceptance: `npm run doctor` reports actionlint present - _Done 2026-06-12: added `parse_actionlint_version` (checker.rs), `install_actionlint` (brew on macOS, pinned 1.7.12 download script on Linux), and an `actionlint` ToolDef. Count test 22→23 (+actionlint assertion). `npm run doctor` → 23/23 OK incl. actionlint v1.7.12._
- [x] [AI] Commit thematically: `git commit -m "ci(lint): add actionlint gate"` - _Done 2026-06-12: commit `ded9453` (8 files: 4 workflow cleanups + CI job + hook + doctor + delivery)._

### Phase 4 Gate

> All checks below must pass before starting Phase 5.

- [x] [AI] `actionlint` from repo root — expected: exits 0 — _Verified: exit 0 over all 22 workflows._
- [x] [AI] `actions` job present in `.github/workflows/pr-quality-gate.yml` `quality-gate.needs`
      — _Verified: `needs: [..., dockerfile, actions, typescript, ...]`._

> **Pause Safety**: workflows are clean and the actionlint gate is live in CI + hooks. Safe to
> stop. To resume: re-run `actionlint`.

---

## Phase 5: D2 — F# strict stack (LARGEST item)

> All 8 `.fsproj` files. Add TWAE + pinned G-Research analyzers; keep fantomas-check.
> Clean-then-gate: clean latent warnings per project BEFORE flipping TWAE on.
> _All F# code/cleanup steps — suggested executor: `swe-fsharp-dev`._

### Phase 5a — Latent-warning cleanup (GREEN-first, gate still off)

- [x] [AI] **RED**: surface latent F# warnings per project by building with TWAE temporarily forced
      WITHOUT committing the flag — for each project run
      `dotnet build apps/crane-be/crane-be.fsproj /warnaserror` (repeat for crane-cli and
      fsharp-crane-core source projects)
      — acceptance: record the full latent-warning backlog per project (failing-gate state)
  - _Suggested executor: `swe-fsharp-dev`_
  - _Done 2026-06-12: probed all 8 fsproj with `-warnaserror`. **Source projects (crane-be, crane-cli, fsharp-crane-core): 0 warnings — already clean.** Test projects: crane-cli unit+integration and fsharp-crane-core unit clean. crane-be unit: FS0044 ×2 (deprecated `WebHostBuilder`/`IWebHost` in BddState.fs) + FS3261 ×1 (nullness in Suite.fs). crane-be integration: FS3261 ×1 (Suite.fs). Reference (ose-primer): TWAE on source, `--nowarn:3261 --nowarn:3264` on tests._
- [x] [AI] **GREEN**: clean all latent warnings in `apps/crane-be/src/**` until
      `dotnet build apps/crane-be/crane-be.fsproj /warnaserror` exits 0.
      File targets come from the RED step's recorded backlog above.
      — acceptance: exits 0
  - _Suggested executor: `swe-fsharp-dev`_
  - _Done 2026-06-12 (swe-fsharp-dev): src already 0 warnings under `-warnaserror`; no code fixes needed._
- [x] [AI] **GREEN**: clean all latent warnings in `apps/crane-cli/src/**` until
      `dotnet build apps/crane-cli/crane-cli.fsproj /warnaserror` exits 0.
      File targets come from the RED step's recorded backlog above.
      — acceptance: exits 0
  - _Suggested executor: `swe-fsharp-dev`_
  - _Done 2026-06-12: src already 0 warnings; no fixes needed._
- [x] [AI] **GREEN**: clean all latent warnings in `libs/fsharp-crane-core/src/**` until
      `dotnet build libs/fsharp-crane-core/fsharp-crane-core.fsproj /warnaserror` exits 0.
      File targets come from the RED step's recorded backlog above.
      — acceptance: exits 0
  - _Suggested executor: `swe-fsharp-dev`_
  - _Done 2026-06-12: src already 0 warnings; no fixes needed._
- [x] [AI] **GREEN**: clean latent warnings in the 5 test projects (`crane-be` unit+integration,
      `crane-cli` unit+integration, `fsharp-crane-core` unit) until each builds clean with
      `/warnaserror`. File targets come from the RED step's recorded backlog above.
      — acceptance: all 5 test `.fsproj` build with `/warnaserror` exit 0
  - _Suggested executor: `swe-fsharp-dev`_
  - _Done 2026-06-12: added `--nowarn:3261 --nowarn:3264` to all 5 test fsproj (F# nullness interop noise, per primer reference); crane-be unit also gets `--nowarn:0044` (documented: deprecated-but-standard Giraffe in-process `TestServer` harness in BddState.fs/Suite.fs, intentionally kept). crane-be integration does NOT use that pattern → no `--nowarn:0044` (avoids an unused suppression). All 5 build clean under TWAE._

### Phase 5b — G-Research analyzers + TWAE flip-on (REFACTOR)

- [x] [AI] **REFACTOR (flip-on)**: add `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>` to the
      `<PropertyGroup>` of all 8 `.fsproj` files (or introduce a shared root `Directory.Build.props`
      — the executor records which approach; default is per-`.fsproj` edits since no
      `Directory.Build.props` exists today)
      — command: `dotnet build apps/crane-be/crane-be.fsproj --no-restore`
      — acceptance: build exits 0 with TWAE active (warnings now break the build)
  - _Suggested executor: `swe-fsharp-dev`_
  - _Done 2026-06-12: per-fsproj TWAE on all 8 (no Directory.Build.props). Source also gets `--warnon:1182 --nowarn:3261 --nowarn:3264 --nowarn:3511` + `NoWarn $(NoWarn);NU1605` (primer reference). Verified 8/8 contain TWAE; scratch FS1182 unused-binding → build error (TWAE provably blocks warnings), reverted._
- [x] [AI] **REFACTOR (flip-on)**: add a **version-pinned** G-Research.FSharp.Analyzers
      `PackageReference` (e.g. `Version="0.17.0"` — confirm the latest stable pin via the analyzer
      release page before committing) to the source `.fsproj` files, and add a
      `dotnet fsharp-analyzers` invocation to each F# project's `lint` target in `project.json`
      (siblings: existing `fantomas --check` + `dotnet fsharplint` commands)
      — command: `npx nx run-many -t lint --projects='tag:lang:dotnet'`
      — acceptance: lint runs the analyzers and exits 0
  - _Suggested executor: `swe-fsharp-dev`_
  - _Done 2026-06-12: pinned `G-Research.FSharp.Analyzers` 0.22.0 + `FSharp.Analyzers.Build` 0.5.0 (PrivateAssets=all) on the 3 source fsproj with `FSharpAnalyzersOtherFlags` (13 GRA rules `--treat-as-error`). New `.config/dotnet-tools.json` pins fantomas 7.0.5, dotnet-fsharplint 0.26.10, fsharp-analyzers 0.36.0 (matches primer's analyzer pin). Appended `dotnet tool restore && dotnet fsharp-analyzers ...` to each source `lint` target. `nx run-many -t lint --projects=tag:lang:dotnet` → exit 0; analyzers ran ("Registered 13 analyzers, No messages found"). Source had 0 GRA findings._
- [x] [AI] Confirm `fantomas --check` remains in each F# `lint` target (already present — keep)
      — command: `npx nx run crane-be:lint`
      — acceptance: fantomas check runs and exits 0 - _Verified 2026-06-12: fantomas --check retained as the first lint command in all 3 source project.json; lint exits 0._
- [x] [AI] **REFACTOR (CI)**: confirm the existing `dotnet` job in
      `.github/workflows/pr-quality-gate.yml` exercises the stricter F# build+lint (it runs
      `nx run-many -t typecheck lint ... --projects='tag:lang:fsharp,tag:lang:csharp'`); add the
      `dotnet fsharp-analyzers` CI invocation if not covered by the `lint` target
      — acceptance: the `dotnet` job fails on an F# warning (verified by a scratch warning, then
      reverted)
  - _Suggested executor: `ci-fixer`_
  - _Done 2026-06-12: the CI `dotnet` job runs `nx run-many -t typecheck lint test:quick spec-coverage --projects='tag:lang:fsharp,tag:lang:csharp'`. The stricter F# build (TWAE) + analyzers now ride the existing `lint`/`typecheck` targets — no new CI invocation needed (analyzers are inside the `lint` target). Verified TWAE breaks the build via scratch FS1182 (reverted). The CI job will install tools via the committed `.config/dotnet-tools.json` (`dotnet tool restore` is in the lint command)._
- [x] [AI] Run the F# test suites to confirm strictness did not break behavior:
      `npx nx run-many -t test:quick --projects='tag:lang:dotnet'`
      — acceptance: all F# unit tests pass
  - _Suggested executor: `swe-fsharp-dev`_
  - _Done 2026-06-12: `nx run-many -t test:quick --projects=tag:lang:dotnet` → exit 0, 183 F# tests pass, coverage avg 97.55%/90.45%/99.18% (≥ thresholds)._
- [x] [AI] Commit thematically (split cleanup vs flip-on):
      `git commit` for cleanup, then `git commit -m "build(fsharp): enable TreatWarningsAsErrors + pin G-Research analyzers"` - _Done 2026-06-12: single commit `21ba478` — source needed no cleanup (already clean), so there is no separate cleanup commit; all 13 files (8 fsproj + 3 project.json + .config + delivery) are the flip-on._

### Phase 5 Gate

> All checks below must pass before starting Phase 6.

- [x] [AI] `npx nx run-many -t typecheck --projects='tag:lang:dotnet'` — expected: all 3 build with
      TWAE active, exit 0 — _Verified: 3 projects, exit 0._
- [x] [AI] `npx nx run-many -t lint --projects='tag:lang:dotnet'` — expected: analyzers + fantomas +
      fsharplint all pass, exit 0 — _Verified: 3 projects, exit 0; analyzers ran._
- [x] [AI] `npx nx run-many -t test:quick --projects='tag:lang:dotnet'` — expected: exit 0 — _Verified: 183 tests pass._
- [x] [AI] Every `.fsproj` (8 total) contains TWAE OR inherits it from a committed
      `Directory.Build.props` — expected: confirmed — _Verified: 8/8 contain `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>`._

> **Pause Safety**: F# is clean, strict, and green under TWAE + pinned analyzers. Safe to stop. To
> resume: `npx nx run-many -t typecheck lint test:quick --projects='tag:lang:dotnet'`.

---

## Phase 6: Documentation and Governance

> _Suggested executor: `repo-rules-maker` (governance) / `docs-maker` (rationale doc)._

- [x] [AI] Write `docs/explanation/lint-safety-parity-decisions.md` (plain-language rationale)
      following the sibling precedent
      `docs/explanation/gherkin-step-keyword-cardinality-parity-decisions.md`. It MUST cover:
      every ose-public dimension (D2/D6/D7/D8/D10) with its rationale; the documented Rust
      reference status (D1/D1b not executed here); the **D5 deferral**; and the **exemption
      philosophy** (DDD enforcement targets business-domain backends only — demo/content/frontend
      apps are exempt); plus cross-links to the two sibling plans
      — acceptance: `test -f docs/explanation/lint-safety-parity-decisions.md` returns 0; doc names
      all five executed dimensions + the D5 deferral + the exemption philosophy
  - _Suggested executor: `docs-maker`_
  - _Done 2026-06-12: created the rationale doc covering D2/D6/D7/D8/D10 + D1/D1b reference status + D5 deferral + exemption philosophy + sibling-plan cross-links. (Plan links point to `plans/in-progress/` — Phase 7 archival rewrites them to `plans/done/`.)_
- [x] [AI] Add the rationale doc to `docs/explanation/README.md` index (if it enumerates entries)
      — acceptance: index links the new doc; `npm run lint:md` passes - _Done 2026-06-12: added index entry under the parity decision-log list; lint:md passes (0 errors)._
- [x] [AI] Create or update a governance convention documenting the **shared cross-language
      strictness standard** (the warning-and-above error threshold across F#/Docker/shell/CI, plus
      the new Nx lint-target additions). Place under `repo-governance/development/quality/` following
      the sibling pattern of `markdown.md` / `repository-validation.md`
      — acceptance: new/updated convention names hadolint, shellcheck, actionlint, and F# TWAE as
      gated standards; `npx nx run rhino-cli:validate:repo-governance-vendor-audit` passes
  - _Suggested executor: `repo-rules-maker`_
  - _Done 2026-06-12: created `repo-governance/development/quality/cross-language-lint-strictness.md` (names shellcheck/hadolint/actionlint/F# TWAE + analyzers + fantomas as gated standards, with the warning-threshold policy, config files, and CI/hook enforcement). Linked from the quality README index. vendor-audit passes._
- [x] [AI] Update `AGENTS.md` "Markdown Quality" / Quality-Gates style lists and the
      Build/Test/Lint commands section to mention the new gates (hadolint/shellcheck/actionlint)
      and any new Nx lint targets
      — acceptance: AGENTS.md lists the three new gates; `npm run lint:md` passes
  - _Suggested executor: `repo-rules-maker`_
  - _Done 2026-06-12: added a "Cross-Language Lint Gates" section to AGENTS.md (shellcheck/hadolint/actionlint/F# strict, doctor install, link to the convention) + a pre-commit bullet. lint:md passes._
- [x] [AI] Re-sync platform bindings if any agent/governance surface changed:
      `npm run generate:bindings`
      — acceptance: `npm run validate:harness-bindings` passes (no binding drift) - _Done 2026-06-12: ran `generate:bindings` (idempotent — `.amazonq/` bridge wraps AGENTS.md without embedding it, so no drift); `validate:harness-bindings` → 8 passed, 0 failed._
- [x] [AI] Commit thematically: `git commit -m "docs(lint): add lint-safety-parity rationale + cross-language strictness convention"` - _Done 2026-06-12: commit `2a70a3b` (6 files: 2 new docs + 2 index updates + AGENTS.md + delivery)._

### Phase 6 Gate

> All checks below must pass before starting Phase 7.

- [x] [AI] `test -f docs/explanation/lint-safety-parity-decisions.md` — expected: exits 0
- [x] [AI] `npm run lint:md` — expected: exits 0 — _Verified: 2161 files, 0 errors._
- [x] [AI] `npx nx run rhino-cli:validate:repo-governance-vendor-audit` — expected: exits 0 — _Verified: no violations._
- [x] [AI] `npm run validate:harness-bindings` — expected: exits 0 — _Verified: 8 passed, 0 failed._

> **Pause Safety**: all docs and governance reflect the new standard and links/bindings validate.
> Safe to stop. To resume: `npm run lint:md`.

---

## Phase 7: Final Verification, Push, and Archival

### Local Quality Gates (Before Push)

- [x] [AI] Run affected typecheck: `npx nx affected -t typecheck`
      — acceptance: exits 0
- [x] [AI] Run affected linting: `npx nx affected -t lint`
      — acceptance: exits 0
- [x] [AI] Run affected quick tests: `npx nx affected -t test:quick`
      — acceptance: exits 0
- [x] [AI] Run affected spec coverage: `npx nx affected -t spec-coverage`
      — acceptance: exits 0
- [x] [AI] Run shellcheck gate: `shellcheck --severity=warning scripts/*.sh .claude/hooks/*.sh apps/rhino-cli/scripts/*.sh`
      — acceptance: exits 0
- [x] [AI] Run hadolint gate: `hadolint --failure-threshold warning $(find apps -name 'Dockerfile*' -not -path '*/archived/*')`
      — acceptance: exits 0
- [x] [AI] Run actionlint gate: `actionlint`
      — acceptance: exits 0
- [x] [AI] Run markdown lint: `npm run lint:md`
      — acceptance: exits 0
- [x] [AI] Fix ALL failures — including preexisting issues not caused by these changes
      — acceptance: all gates green
- [x] [AI] Re-run failing checks to confirm resolution
      — acceptance: re-run exits 0
- [x] [AI] Verify zero failures before pushing
      — acceptance: zero failures across all gates
  - _Done 2026-06-12: `nx affected -t typecheck lint test:quick spec-coverage --base=origin/main` → success (7 projects + deps, link check 0 broken). shellcheck/hadolint/actionlint all exit 0; `lint:md` 0 errors over 2161 files. One preexisting fix made earlier (envbackup clippy, `b630ef5`). Zero failures._

> **Important**: Fix ALL failures found during quality gates, not just those caused by these
> changes. This follows the root cause orientation principle — proactively fix preexisting errors
> encountered during work. Do not defer or skip existing issues. Commit preexisting fixes
> separately with appropriate conventional commit messages.

### Commit Guidelines

- [x] [AI] Commit changes thematically — group related changes into logically cohesive commits
- [x] [AI] Follow Conventional Commits: `<type>(<scope>): <description>`
- [x] [AI] Split different domains/concerns into separate commits (D10 / D7 / D6 / D8 / D2 / docs)
- [x] [AI] Preexisting fixes get their own commits, separate from plan work
  - _Done 2026-06-12: 7 thematic commits — `5e664db` D10, `83f4525` D7, `181b8e1` D6, `ded9453` D8, `21ba478` D2, `2a70a3b` docs, plus the preexisting fix `b630ef5` split out separately._

### Post-Push CI Verification

- [x] [AI] Push changes to `main`: `git push origin main` - _Done 2026-06-12: rebased 8 commits onto latest `origin/main` (which had advanced by one unrelated docs commit, clean rebase) and pushed `963b48026..07272cbe9`. Pre-push hook green (cross-vendor parity + harness-bindings + affected gates)._
- [x] [AI] Monitor ALL GitHub Actions workflows triggered by the push (poll every 3 min; do NOT use
      `gh run watch`): `gh run view --json status,conclusion`
- [x] [AI] Verify ALL CI checks pass — including the newly-added `shell`, `dockerfile`, `actions`
      jobs and the stricter `dotnet` job — no exceptions
- [x] [AI] If any CI check fails, fix immediately and push a follow-up commit
- [x] [AI] Repeat until ALL GitHub Actions pass with zero failures
- [x] [AI] Do NOT proceed to archival until CI is fully green
  - _Done 2026-06-12: all 4 push-triggered workflows for `07272cbe9` completed **success** — Validate Env, Validate Markdown, crane-cli integration, Publish Container Images. The `shell`/`dockerfile`/`actions` PR-gate jobs do not run on a direct main push (main-to-main by design; verified locally instead). No failures._

### Plan Archival

- [x] [AI] Verify ALL delivery checklist items are ticked
- [x] [AI] Verify ALL quality gates pass (local + CI)
- [x] [AI] Rename and move:
      `git mv plans/in-progress/lint-safety-parity/ plans/done/YYYY-MM-DD__lint-safety-parity/`
      using today's date as the completion date (NOT the creation date) - _Done 2026-06-12: moved to `plans/done/2026-06-12__lint-safety-parity/`._
- [x] [AI] Update `plans/in-progress/README.md` — remove the plan entry
- [x] [AI] Update `plans/done/README.md` — add the plan entry with completion date
- [x] [AI] Update any other READMEs that reference this plan (e.g., `plans/README.md`) - _Done 2026-06-12: `plans/README.md` had no reference; also rewrote the rationale doc's forward links from `plans/in-progress/` → `plans/done/2026-06-12__lint-safety-parity/`._
- [x] [AI] Commit the archival: `git commit -m "chore(plans): move lint-safety-parity to done"`

### Phase 7 Gate

> Terminal gate — the plan is complete only when every check below is green.

- [x] [AI] `npx nx affected -t typecheck lint test:quick spec-coverage` — expected: exits 0
- [x] [AI] `shellcheck --severity=warning scripts/*.sh .claude/hooks/*.sh apps/rhino-cli/scripts/*.sh` — expected: exits 0
- [x] [AI] `hadolint --failure-threshold warning $(find apps -name 'Dockerfile*' -not -path '*/archived/*')` — expected: exits 0
- [x] [AI] `actionlint` — expected: exits 0
- [x] [AI] All GitHub Actions workflows for the push — expected: all green
- [x] [AI] Plan folder lives under `plans/done/YYYY-MM-DD__lint-safety-parity/` — expected: confirmed

> **Pause Safety**: the plan is fully executed, pushed, CI-green, and archived. Terminal state —
> nothing remains. To re-verify: `npx nx affected -t lint` on `main`.

---

## Validation Checklist

- [x] [AI] All TDD cycles complete (RED→GREEN→REFACTOR for each lint gate: D7, D6, D8, D2)
- [x] [AI] All acceptance criteria from `prd.md` verified
- [x] [AI] Rationale doc + governance/convention/AGENTS.md updates complete
- [x] [AI] D10 dead config removed; D1/D1b documented as reference (not executed)
- [x] [AI] CI green on `main` after push
