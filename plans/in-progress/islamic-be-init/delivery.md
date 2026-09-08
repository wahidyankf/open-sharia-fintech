# Delivery Checklist — islamic-be-init

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.

This checklist is prospective. It does not authorize implementation, staging, committing, pushing,
opening pull requests, or changing either repository. Execute it only after the user explicitly
names this plan for execution.

Every command below is copyable verbatim. Where a value cannot be known at authoring time (a
resolved version, a generated checksum, a merged PR number), the step says how to resolve it rather
than guessing it.

## Upstream Dependency

This plan does not begin until [`lms-init`](../lms-init/README.md) has **merged** both:

- **DU1** — config-driven doctor tool inventory, landed byte-identically in `ose-public` and
  `ose-private`, with `doctor.extra-tools` present in both `repo-config.yml` files.
- **DU2** — Java language enablement, which generalizes `scripts/behaviour-coverage.mjs`, adds the
  `has-<lang>` detect/job/exclude/aggregate pattern and the `setup-java` composite action, and adds
  `tag:lang:java` to the `typescript`, `dotnet`, and `flutter` exclude lists.

Phase 0 verifies both and **stops and reports** if either is missing. It never substitutes the
upstream work. The rationale and the accepted cost are recorded in [`tech-docs.md`](./tech-docs.md)
§2 D-0.

## Delivery Mode

`worktree-to-pr`. DU1–DU4 and DU6 are `ose-public`-only. DU5 is applied independently to
`ose-public` and `ose-private`: each repository has its own branch, commits, pull request,
current-head/base CI, and merge.

`worktree-to-pr` is mandatory in `ose-public`: `main` is branch-protected including for admins, so
neither direct-push mode has an executable path there.

`[AI]` merges each pull request once exact-current-head/base `pr-quality-gate.yml`, one
authenticated clean current-head `pr-leak-review`, and the applicable surface gates all hold. No
`[HUMAN]` merge gate is declared.

## Worktree

- Public: `R-PUB:worktrees/islamic-be-init/`
- Private: `R-PRI:worktrees/islamic-be-init/` — provisioned lazily at Phase 5, the only unit that
  touches `ose-private`

### Provisioned Worktree Identity

- Public declared repository-relative route: `worktrees/islamic-be-init/`
- Public initial branch: `worktree/islamic-be-init`
- Private declared repository-relative route: `worktrees/islamic-be-init/`
- Private initial branch: `worktree/islamic-be-init`
- Created by: resolve at Phase 0 from `git worktree list --porcelain` and record here
- Created at: resolve at Phase 0 (ISO-8601 UTC); do not hardcode a timestamp while authoring

> **Branch-name note, recorded rather than hidden:** the canonical template suggests
> `<plan-identifier>-base`. This plan uses `worktree/<plan-identifier>`, which is the shape
> `claude --worktree` actually produces and the shape `lms-init` and the archived
> `2026-09-04__adopt-beavernest-test-automation` plan both record. The deviation is from the
> template, not from repository practice.
>
> The pre-existing `worktrees/ose-islamic/` checkout was an ad-hoc authoring workspace created
> before this plan existed. It is not this plan's worktree and is removed at Phase 0.

### Delivery Branch Inventory

| Branch                                | Repository    | Mode      | Lifecycle state | Proof                                                                         |
| ------------------------------------- | ------------- | --------- | --------------- | ----------------------------------------------------------------------------- |
| `worktree/ose-islamic`                | `ose-public`  | `to-pr`   | `active`        | carries the plan-authoring PR #488; record its 40-character head SHA on merge |
| `worktree/islamic-be-init`            | `ose-public`  | `pending` | `pending`       | `git worktree add` at Phase 0                                                 |
| `worktree/islamic-be-init`            | `ose-private` | `pending` | `pending`       | `git worktree add` at Phase 5                                                 |
| `islamic-be-init/du1-go-lane`         | `ose-public`  | `to-pr`   | `pending`       | record merged PR number and 40-character head SHA at DU1                      |
| `islamic-be-init/du2-specs-contracts` | `ose-public`  | `to-pr`   | `pending`       | record merged PR number and 40-character head SHA at DU2                      |
| `islamic-be-init/du3-service`         | `ose-public`  | `to-pr`   | `pending`       | record merged PR number and 40-character head SHA at DU3                      |
| `islamic-be-init/du4-e2e`             | `ose-public`  | `to-pr`   | `pending`       | record merged PR number and 40-character head SHA at DU4                      |
| `islamic-be-init/du5-rhino-go-env`    | `ose-public`  | `to-pr`   | `pending`       | record merged PR number and 40-character head SHA at DU5                      |
| `islamic-be-init/du5-rhino-go-env`    | `ose-private` | `to-pr`   | `pending`       | record merged PR number and 40-character head SHA at DU5                      |
| `islamic-be-init/du6-registry`        | `ose-public`  | `to-pr`   | `pending`       | record merged PR number and 40-character head SHA at DU6                      |

Append every plan-created delivery branch before use. Before removal, classify every entry as
delivered, unused, or retained/escalated; an active or unrecorded branch blocks cleanup.

### Cross-Repository Parity Identity

- Objective slug: `islamic-be-init`
- Common worktree basename: `islamic-be-init`

| Repository    | Corresponding short-lived branch   |
| ------------- | ---------------------------------- |
| `ose-public`  | `islamic-be-init/du5-rhino-go-env` |
| `ose-private` | `islamic-be-init/du5-rhino-go-env` |

DU1, DU2, DU3, DU4, and DU6 are `ose-public`-only and declare no parity branch.

---

## Phase 0: Environment Setup and Baseline

Phase 0 opens no pull request. Its outcome is a verified upstream state and a recorded clean
baseline.

### Upstream Verification — stop-and-report, never substitute

> **Completed 2026-09-08. Verdict: all prerequisites MET.** `lms-init` DU1 merged as `c6fffc3` and
> DU2 as #493; both were verified against the merged tree rather than by commit title. The full
> result, with every file and line number checked, is in
> [`evidence/phase-0-upstream.md`](./evidence/phase-0-upstream.md). The checkboxes below are
> retained as the re-verification procedure — re-run them if this plan is resumed after a long gap,
> since `main` moves.

- [ ] [AI] Confirm `lms-init` DU1 is merged in **both** repositories:
      `rtk gh pr list --repo wahidyankf/ose-public --state merged --search "du1-doctor-config"` and
      the same for `wahidyankf/ose-private`. Acceptance: each returns a merged PR; record both
      numbers and 40-character head SHAs in this file. If either is missing, **stop and report** —
      do not build the doctor refactor here.
- [ ] [AI] Confirm `doctor.extra-tools` exists in both `repo-config.yml` files:
      `rtk grep -n "extra-tools" repo-config.yml` in each repository. Acceptance: present in both,
      satisfying the identical-key-set parity rule. Save both outputs to
      `evidence/phase-0-extra-tools.txt`.
- [ ] [AI] Confirm `lms-init` DU2 is merged and read the shape it left behind:
      `rtk sed -n '18,22p;400,412p' scripts/behaviour-coverage.mjs`. Acceptance: `BINDING_FILE`
      includes `java` and `extractBindings` dispatches more than two languages. **Verified:** an
      `if`-chain at `:405`–`:410`, with the shared `featureReferences(source, literalPattern)`
      helper at `:302` available to reuse. DU1 adds a `.go` arm to that chain; a shape different
      from `tech-docs.md` §4.2's assumption is a stop-and-report, not a work-around.
- [ ] [AI] Confirm the CI pattern DU1 copies exists: `rtk ls .github/actions/setup-java/action.yml`
      and `rtk grep -c "tag:lang:java" .github/workflows/pr-quality-gate.yml`. Acceptance: the
      action exists and the grep reports 4 — `typescript` ×1, `dotnet` ×2, `flutter` ×1.
      **Verified.** Note what this count does _not_ include: the `java` job's own exclude list names
      no `java`, and names no `go` either — which is why Go leaks into four jobs, not three.
- [ ] [AI] Confirm `rhino-cli-parity-audit.yml` is currently green on `main`:
      `rtk gh run list --workflow rhino-cli-parity-audit.yml --limit 1 --json conclusion,url`.
      Acceptance: `conclusion` is `success`; save the URL to `evidence/phase-0-parity-audit.txt`. A
      red audit before this plan starts is somebody else's in-flight parity work — stop and report.

### Environment Setup

- [ ] [AI] Confirm the work location: run `rtk pwd` and confirm the path ends in
      `worktrees/islamic-be-init`. If it does not, run `rtk git worktree list --porcelain` from the
      `ose-public` repository root and enter the worktree whose route is `worktrees/islamic-be-init`.
- [ ] [AI] Provision `worktrees/islamic-be-init/` from current `origin/main` if absent. Acceptance:
      `rtk git worktree list --porcelain` shows the route and its branch. Record the route, branch,
      and ISO-8601 UTC creation time in the Provisioned Worktree Identity block above; no
      placeholder text remains.
- [ ] [AI] Sync the worktree: `rtk git fetch origin` then `rtk git merge --ff-only origin/main`.
      Acceptance: "Already up to date" or a fast-forward; a conflict here means stop and report,
      never force.
- [ ] [AI] Remove the superseded `worktrees/ose-islamic/` checkout once PR #488 has merged.
      Acceptance: `rtk git worktree list` no longer lists it, and the cap of one worktree per
      repository per plan holds.
- [ ] [AI] Install dependencies:
      `rtk ./hippo run --class ephemeral --disk-path . -- npm install`. Acceptance: exit code 0.
- [ ] [AI] Converge tooling: `rtk npm run doctor -- --fix`. Acceptance: exit code 0. If it cannot
      converge, capture the output in `evidence/phase-0-doctor.txt` and report before continuing —
      do not proceed on a divergent toolchain.
- [ ] [AI] Resolve every version `tech-docs.md` §5 marks "resolve at DU0" and record the resolved
      value there: Gin, Godog, and `govulncheck`. Acceptance: each row carries a concrete version
      and its resolution date, replacing the placeholder.
- [ ] [AI] Verify the Go toolchain: `rtk go version`, `rtk golangci-lint --version`, and
      `rtk oapi-codegen --version`. Acceptance: all three print versions matching `tech-docs.md` §5;
      save to `evidence/phase-0-toolchain.txt`.

### Baseline

- [ ] [AI] Run the scoped baseline
      `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run-many -t test:quick --projects=ose-be,ose-be-e2e,rhino-cli`.
      Acceptance: all three pass, or every pre-existing failure is resolved before Phase 1 begins.
      Save to `evidence/phase-0-baseline.txt`.
- [ ] [AI] Run `rtk ./hippo run --class ephemeral --disk-path . -- npm exec nx -- run rhino-cli:env:validation`.
      Acceptance: exits zero, establishing the pre-change env-contract baseline.

### Phase 0 Gate

> All checks below must pass before starting Phase 1. If any check fails, fix it in Phase 0 before
> proceeding.

- [ ] [AI] `rtk git worktree list --porcelain` — shows `worktrees/islamic-be-init/` and no
      `ose-islamic` entry
- [ ] [AI] `lms-init` DU1 and DU2 are both recorded as merged, with PR numbers and head SHAs written
      into this file
- [ ] [AI] `rtk npm run doctor` — exits 0
- [ ] [AI] `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run-many -t test:quick --projects=ose-be,ose-be-e2e,rhino-cli` — exits zero
- [ ] [AI] `rtk ./hippo run --class ephemeral --disk-path . -- npm exec nx -- run rhino-cli:env:validation` — exits zero
- [ ] [AI] `rtk go version && rtk golangci-lint --version && rtk oapi-codegen --version` — all three resolve

> **Pause Safety**: the repository is unchanged apart from this plan's own files; the upstream
> `lms-init` state is verified and recorded, a correctly named worktree exists, and the toolchain is
> confirmed. Safe to stop. To resume:
> `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run-many -t test:quick --projects=ose-be,ose-be-e2e,rhino-cli`.

## Phase 1 (DU1): Go Platform Lane

Delivery boundary. Lands every gate a Go project needs, before any Go project exists.

**Tag vocabulary (rules-propagation)**

- [ ] [AI] Run the rules-propagation workflow for the tag-vocabulary amendment: normalise the rule, scan for contradictions, and record an enforcement disposition — acceptance: the workflow's preflight output is captured in `learnings.md`
- [ ] [AI] Edit `repo-governance/development/infra/nx-targets/tag-convention-four-dimension-scheme.md`: admit `go` to `lang:`, `gin` to `platform:`, and `islamic` to `domain:` — acceptance: all three values appear in the Allowed Values column
- [ ] [AI] Edit `repo-governance/development/infra/nx-targets/tag-convention-current-tags-and-examples.md`: add rows for `islamic-be`, `islamic-be-e2e`, and `islamic-contracts` — acceptance: the three rows exist with the tag sets from `tech-docs.md`
- [ ] [AI] Verify neither file exceeds its 750-word governance budget — acceptance: `npm exec nx -- run rhino-cli:governance:word-budget` (or the equivalent gate) reports no failure for either path

**Linting gate**

- [ ] [AI] Add a `lint-golangci` entry to `repo-config.yml`'s `gates:` list with `ci` and `pre-commit` surfaces scoped to `glob: "*.go"` — acceptance: `npm exec nx -- run rhino-cli:repo-config:validation` exits zero
- [ ] [AI] Confirm the pre-existing `format-gofmt` and `format-verify-gofmt` entries still resolve and that `scripts/verify-gofmt.sh` is executable — acceptance: `ls -l scripts/verify-gofmt.sh` shows mode 755 and both gate ids appear in the registry
- [ ] [AI] Confirm no top-level key was added to `repo-config.yml` — acceptance: `diff <(git show HEAD:repo-config.yml | grep -E '^[a-z-]+:') <(grep -E '^[a-z-]+:' repo-config.yml)` reports no difference

**Doctor registration**

- [ ] [AI] Declare `go` under `repo-config.yml`'s `doctor.extra-tools` using the shape in `tech-docs.md` §2 D-9 and the Phase 0 resolved Go version — acceptance: `rtk npm run doctor` output now includes a `go` row reporting the installed version, proving the probe works on a real machine; save to `evidence/du1-doctor-go.txt`
- [ ] [AI] Confirm this added a **list item**, not a key — acceptance: `doctor.extra-tools` already existed from `lms-init` DU1 in both repositories, so the top-level key set is unchanged and `rtk ./hippo run --class ephemeral --disk-path . -- npm exec nx -- run rhino-cli:repo-config:validation` exits zero
- [ ] [AI] Confirm no `rhino-cli` source file was touched by this registration — acceptance: `rtk git status --porcelain apps/rhino-cli/` reports nothing, proving D-9's zero-parity-cost claim held

**CI job**

- [ ] [AI] Create `.github/actions/setup-go/action.yml` reading `go-version-file: apps/islamic-be/go.mod`, with module and build caching and a pinned `golangci-lint` install — acceptance: the action file parses and pins the versions named in `tech-docs.md` §5
- [ ] [AI] Edit `.github/workflows/pr-quality-gate.yml`: add `has-go` to the `detect` job outputs and a `lang:go)` case to its tag switch — acceptance: the `detect` job initialises and sets `has-go` alongside `has-ts`, `has-dotnet-projects`, and `has-dart`
- [ ] [AI] Add a `go` job gated on `has-go == 'true'` running `npx nx affected -t typecheck lint test:quick compat:min-version --exclude='tag:lang:ts,tag:lang:fsharp,tag:lang:csharp,tag:lang:rust,tag:lang:dart,tag:lang:java' --parallel=1` — acceptance: the job exists, provisions `setup-node` plus `setup-go`, and mirrors the `java` job's structure at `:365`–`:377`
- [ ] [AI] Add `tag:lang:go` to the `--exclude` list of **all four** existing language jobs — `typescript` (`:306`), `dotnet` (both `:335` and `:338`), `flutter` (`:362`), and `java` (`:377`). Each selects by excluding known tags, so omitting any one leaves Go running on a toolchain-less runner. Acceptance: `rtk grep -c "tag:lang:go" .github/workflows/pr-quality-gate.yml` reports exactly 5 — one per exclusion, counting `dotnet` twice. Compare with `rtk grep -c "tag:lang:java"`, which reports 4 for the same reason
- [ ] [AI] Give the new `go` job an exclude list naming every other language: `tag:lang:ts,tag:lang:fsharp,tag:lang:csharp,tag:lang:rust,tag:lang:dart,tag:lang:java`, modelled on the `java` job at `:377`. Acceptance: the `go` job's own list does **not** contain `tag:lang:go`
- [ ] [AI] Add the `go` job to the `quality-gate` aggregation job's `needs` list — acceptance: `needs:` names `go`, so the aggregate cannot report success while the Go job failed
- [ ] [AI] Run `rtk actionlint` — acceptance: exit code 0

**Behaviour-coverage Go extractor**

- [ ] [AI] **Read before editing**: re-read the merged `BINDING_FILE` and `extractBindings` and compare against `evidence/phase-0-extractor-shape.txt` — acceptance: the shape matches what `lms-init` DU2 left; a mismatch is a stop-and-report, not a local refactor
- [ ] [AI] **RED**: add fixtures to `scripts/behaviour-coverage.test.mjs` covering each Godog registration form plus negative cases (a regex literal in non-registration code, a commented-out registration, a backtick string that is not a step) — acceptance: `rtk npm run test:validators` fails because `.go` is not scanned; save to `evidence/du1-red-validator.txt`
- [ ] [AI] Extend `BINDING_FILE` to include `go` — acceptance: the regex admits `.go` alongside `.ts`, `.tsx`, `.fs`, and `.java`
- [ ] [AI] Add `extractGoBindings(resourceName, source)` to `scripts/behaviour-coverage.mjs` handling interpreted strings, backtick raw strings, `regexp.MustCompile` wrappers, and the `Given`/`When`/`Then` keyword-sensitive forms — acceptance: the function is exported alongside the F# and TypeScript extractors
- [ ] [AI] Extend `extractBindings` to dispatch `.go` to the new extractor — acceptance: a `.go` resource no longer falls through to `extractTypescriptBindings`
- [ ] [AI] Reuse the shared quoted-literal feature-reference helper `lms-init` DU2 factored out rather than adding a fourth near-copy — acceptance: `extractGoBindings` calls the helper; no duplicated scan is introduced
- [ ] [AI] **GREEN**: rerun `rtk npm run test:validators` — acceptance: exits zero with the new Go cases passing
- [ ] [AI] Confirm Go comment and raw-string handling does not corrupt the existing F#/TypeScript/Java paths — acceptance: the pre-existing validator tests still pass unchanged, and `rtk ./hippo run --class ephemeral --disk-path . -- npm exec nx -- affected -t test:coverage:behaviour` leaves every existing project's coverage result unchanged

**Integration**

- [ ] [AI] Commit on `islamic-be-init/du1-go-lane`, push, and open a draft PR stating the new-code cost/benefit — acceptance: the PR body names the CI leak this fixes and links `tech-docs.md` §1.4
- [ ] [AI] Poll CI every 2 minutes until `pr-quality-gate.yml` and `pr-leak-review` complete on the current head — acceptance: both report success; never use `gh run watch`
- [ ] [AI] Mark ready and merge once the hardened preconditions hold — acceptance: the PR merges to `main`

### Phase 1 Gate

> All checks below must pass before starting Phase 3. Phase 2 (DU2) may proceed in parallel.

- [ ] [AI] `npm run test:validators` — exits zero with the new Go extractor cases present
- [ ] [AI] `npm exec nx -- run rhino-cli:repo-config:validation` — exits zero
- [ ] [AI] `npm exec nx -- run-many -t test:quick --projects=ose-be,ose-be-e2e` — exits zero, proving no regression to existing lanes
- [ ] [AI] Confirm the merged `pr-quality-gate.yml` excludes `tag:lang:go` in the `typescript`, `dotnet`, `flutter`, **and** `java` jobs — acceptance: `rtk grep -c 'tag:lang:go' .github/workflows/pr-quality-gate.yml` reports 5
- [ ] [AI] `rtk npm run doctor` — reports a `go` row with a real version
- [ ] [AI] `rtk git log -1 --stat -- apps/rhino-cli/` — shows this delivery unit touched no `rhino-cli` file

> **Pause Safety**: the Go lane exists and every gate is registered, but no Go project does — the
> `go` job is correct and dormant. Nothing else changed behaviour. Safe to stop. To resume:
> `npm run test:validators`.

## Phase 2 (DU2): Specs Corpus and Contracts

Delivery boundary. Independent of DU1; may run before, after, or concurrently.

- [ ] [AI] Create `specs/apps/islamic/README.md` and `specs/apps/islamic/overview.md` following the shape of `specs/apps/ose/` — acceptance: `rhino-cli specs structure validate` accepts the new product folder
- [ ] [AI] Create `specs/apps/islamic/be/README.md` describing the corpus, and `architecture.md` with C4 context, container, and component diagrams using the accessible palette — acceptance: both files exist and every Mermaid `classDef` uses palette hex codes
- [ ] [AI] Create `specs/apps/islamic/be/behaviours/health/` with `README.md` and `health.feature` carrying the three US-1 scenarios from `prd.md` verbatim — acceptance: `npx gherkin` parses the feature and scenario names match `prd.md`
- [ ] [AI] Create `specs/apps/islamic/be/behaviours/config/` with `README.md` and `port-resolution.feature` carrying the five US-3 scenarios — acceptance: the feature parses and all five scenarios are present
- [ ] [AI] Create `specs/apps/islamic/be/contracts/openapi.yaml` (OpenAPI 3.1) with `paths/health.yaml`, `schemas/health.yaml`, and `schemas/error.yaml`, plus a README for each folder — acceptance: the root document references the fragments and every folder carries an annotated index
- [ ] [AI] Copy `.spectral.yaml` from `specs/apps/ose/be/contracts/` unchanged — acceptance: the two ruleset files are byte-identical
- [ ] [AI] Create `specs/apps/islamic/be/contracts/project.json` registering `islamic-contracts` with `lint`, `bundle`, `docs`, `typecheck`, `test:quick`, `deps:audit`, `compat:min-version`, and `specs:structure-validation` targets, plus `namedInputs.specs` — acceptance: `npx nx show project islamic-contracts` resolves
- [ ] [AI] Create `specs/apps/islamic/be/contracts/generated/README.md` explaining that bundles are generated — acceptance: the file exists and the folder is otherwise gitignored
- [ ] [AI] Commit on `islamic-be-init/du2-specs-contracts`, push, open a draft PR, poll CI every 2 minutes, and merge when green — acceptance: the PR merges to `main`

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [ ] [AI] `npm exec nx -- run islamic-contracts:lint` — bundles and Spectral-lints with zero errors
- [ ] [AI] `npm exec nx -- run islamic-contracts:test:quick` — exits zero
- [ ] [AI] `npm exec nx -- run islamic-contracts:specs:structure-validation` — exits zero
- [ ] [AI] Confirm every new Nx project declares `namedInputs.specs` — acceptance: `npx nx show project islamic-contracts --json | jq '.namedInputs.specs'` returns a non-null array

> **Pause Safety**: the specification corpus and contract exist and validate; no code implements them
> yet, which is the intended contract-first state. Safe to stop. To resume:
> `npm exec nx -- run islamic-contracts:test:quick`.

## Phase 3 (DU3): The islamic-be Service

Delivery boundary. Requires DU1 and DU2 merged.

**Module scaffold**

- [ ] [AI] Create `apps/islamic-be/go.mod` declaring `module github.com/wahidyankf/ose-public/apps/islamic-be` and `go 1.26` — acceptance: `go mod tidy` succeeds from the app directory
- [ ] [AI] Add `tools.go` pinning `github.com/oapi-codegen/oapi-codegen/v2` so the generator version is locked by the module — acceptance: `go.sum` records the generator and `go run` resolves it without a `PATH` lookup
- [ ] [AI] Create `.golangci.yml` using the **v2 schema** (`version: "2"`) enabling at minimum `errcheck`, `govet`, `staticcheck`, `ineffassign`, and `unused` — acceptance: `golangci-lint run` parses the config without a schema error
- [ ] [AI] Create `.editorconfig`, `.gitignore`, `.dockerignore`, `.env.example` (`ISLAMIC_BE_PORT=8402`), and `LICENSE` mirroring `apps/ose-be/` — acceptance: all five exist and `.env.example` is the only committed env file

**Implementation**

- [ ] [AI] Add an `islamic-be:codegen` target running `oapi-codegen` against the bundled contract into `generated-contracts/`, with `dependsOn: ["islamic-contracts:bundle"]` — acceptance: the target emits Go types and a Gin `ServerInterface`
- [ ] [AI] Implement `internal/config/port.go` with resolution order flag → `ISLAMIC_BE_PORT` → 8402, failing at startup on a malformed value and ignoring a bare `PORT` — acceptance: all five US-3 scenarios pass
- [ ] [AI] Implement `internal/health/health.go` returning 200 with `{"status":"healthy"}` and an `application/json` content type — acceptance: the two US-1 response scenarios pass
- [ ] [AI] Implement `internal/router/router.go` wiring a Gin engine that satisfies the generated `ServerInterface` and returns 404 for unknown routes — acceptance: `go build ./...` succeeds and the unknown-route scenario passes
- [ ] [AI] Implement `cmd/islamic-be/main.go` as a thin entry point delegating to `config` and `router` — acceptance: `go run ./cmd/islamic-be` serves on 8402

**Tests and bindings**

- [ ] [AI] Write co-located `*_test.go` unit tests for `internal/config`, `internal/health`, and `internal/router` — acceptance: `go test ./...` passes
- [ ] [AI] Write `internal/bdd/steps.go` registering a Godog step for every active scenario in the health and config corpora, driving the in-process engine via `net/http/httptest` — acceptance: no scenario is unbound and no step touches a real socket
- [ ] [AI] Create `behaviour-coverage.json` with the corpus root and `unit` plus `e2e` adapters, and **no** `integration` adapter — acceptance: the file declares exactly two adapters
- [ ] [AI] Create `project.json` with the target surface from `tech-docs.md` §4.1, tags `["type:app","platform:gin","lang:go","domain:islamic"]`, and `namedInputs.specs` — acceptance: `npx nx show project islamic-be` lists the targets and omits `test:integration`
- [ ] [AI] Configure `test:unit` to collect `-coverprofile=cover.out`, exclude `cmd/islamic-be/main.go` from the denominator, and fail below 99% — acceptance: the target fails when a line is deliberately left uncovered
- [ ] [AI] Implement `compat:min-version` as a real assertion that `go.mod`'s `go` directive matches the pinned version — acceptance: the target fails if the directive is edited away from the pin

**Packaging and documentation**

- [ ] [AI] Write a multi-stage `Dockerfile` on the pinned Go version — acceptance: `docker build -f apps/islamic-be/Dockerfile .` produces a runnable image
- [ ] [AI] Create `infra/dev/islamic-be/docker-compose.yml` for the service alone — acceptance: `docker compose -f infra/dev/islamic-be/docker-compose.yml up` serves the health endpoint
- [ ] [AI] Write `apps/islamic-be/README.md` covering the corpus, adapters, target names, and an explicit rationale for the omitted Integration layer — acceptance: the README states why `test:integration` is absent, as the anti-echo convention requires, and stays under the 1000-word README budget
- [ ] [AI] Commit on `islamic-be-init/du3-service`, push, open a draft PR, poll CI every 2 minutes, and merge when green — acceptance: the PR merges to `main`

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [ ] [AI] `npm exec nx -- run islamic-be:test:quick` — exits zero, including the 99% coverage floor and both static coverage validators
- [ ] [AI] `npm exec nx -- run islamic-be:lint` — `golangci-lint` reports no findings
- [ ] [AI] `npm exec nx -- run islamic-be:build` — produces `apps/islamic-be/dist/islamic-be`
- [ ] [AI] Confirm the merged PR's CI run shows the `go` job green **and** the `typescript`, `dotnet`, `flutter`, and `java` jobs not selecting any Go target — acceptance: the `go` job log lists `islamic-be` and none of the other four does; save to `evidence/du3-ci-routing.txt`
- [ ] [AI] `curl -s localhost:8402/api/v1/health` against a locally running instance — returns 200 with `{"status":"healthy"}`, captured to `evidence/phase-3-health.txt`

> **Pause Safety**: `islamic-be` builds, tests, lints, and serves its health endpoint; its Gherkin is
> bound at the Unit layer. The E2E layer is not yet implemented, so `test:coverage:e2e` reports its
> scenarios as unbound until Phase 4. Safe to stop. To resume:
> `npm exec nx -- run islamic-be:test:quick`.

## Phase 4 (DU4): The islamic-be-e2e Suite

Delivery boundary. Requires DU3 merged.

- [ ] [AI] Create `apps/islamic-be-e2e/package.json`, `tsconfig.json`, and `playwright.config.ts` mirroring `apps/ose-be-e2e/` with `bddgen` pointed at the islamic corpus — acceptance: `npx bddgen` generates test files from the health feature
- [ ] [AI] Implement `steps/backend-process.ts` starting and stopping the real `islamic-be` process on a controlled port — acceptance: the suite starts the service itself and shuts it down deterministically
- [ ] [AI] Implement `steps/health.steps.ts` and `utils/response-store.ts` binding the health scenarios over real HTTP — acceptance: all three US-1 scenarios pass against the running process
- [ ] [AI] Create `behaviour-coverage.json` with the corpus and an `e2e` adapter — acceptance: the file mirrors the `ose-be-e2e` shape
- [ ] [AI] Create `project.json` with the E2E target surface, tags `["type:e2e","platform:playwright","lang:ts","domain:islamic"]`, `implicitDependencies: ["islamic-be"]`, and `namedInputs.specs` — acceptance: the project declares no Unit or Integration target
- [ ] [AI] Decide and record whether the config scenarios need an `e2e-coverage-baseline.json` `allowedUnbound` entry, with a written reason for each — acceptance: every unbound scenario carries a stated reason or is bound
- [ ] [AI] Write `apps/islamic-be-e2e/README.md` — acceptance: it explains what the suite covers and how to run it
- [ ] [AI] Commit on `islamic-be-init/du4-e2e`, push, open a draft PR, poll CI every 2 minutes, and merge when green — acceptance: the PR merges to `main`

### Phase 4 Gate

> All checks below must pass before starting Phase 6. Phase 5 (DU5) may proceed in parallel.

- [ ] [AI] `npm exec nx -- run islamic-be-e2e:test:e2e` — all scenarios pass against a real process
- [ ] [AI] `npm exec nx -- run islamic-be-e2e:test:quick` — exits zero
- [ ] [AI] `npm exec nx -- run islamic-be:test:coverage` — every adapter reports its scenarios bound or explicitly allowed
- [ ] [AI] Capture the passing E2E run output to `evidence/phase-4-e2e.txt` — acceptance: the file records the scenario count and result

> **Pause Safety**: the full test pyramid is green — Unit bindings, E2E bindings, and static coverage
> across both. The service is complete and gated; only registry documentation and env drift-checking
> remain. Safe to stop. To resume: `npm exec nx -- run islamic-be-e2e:test:e2e`.

## Phase 5 (DU5): rhino-cli Go Env Scanner (Cross-Repository Parity)

Delivery boundary spanning two repositories, byte-identical in `apps/rhino-cli`. Independent of
DU1–DU4; gates only DU6.

### Parity Preflight — before the first mutation in either repository

- [ ] [AI] Confirm no other plan holds an open parity PR pair: `rtk gh pr list --repo wahidyankf/ose-public --state open --search "rhino-cli in:title"` and the same for `wahidyankf/ose-private`. Acceptance: neither returns an open PR touching `apps/rhino-cli`. Two concurrent pairs race on the same generated manifest — see `tech-docs.md` §1.5.
- [ ] [AI] Confirm `rhino-cli-parity-audit.yml` is green on `main`: `rtk gh run list --workflow rhino-cli-parity-audit.yml --limit 1 --json conclusion,url`. Acceptance: `conclusion` is `success`; save to `evidence/du5-parity-preflight.txt`.
- [ ] [AI] Confirm the branch name `islamic-be-init/du5-rhino-go-env` is unused in both repositories: `rtk git ls-remote --heads origin islamic-be-init/du5-rhino-go-env` in each. Acceptance: both return empty.
- [ ] [AI] Provision the private worktree. From `/Users/wkf/ose-projects/ose-private` run `claude --worktree islamic-be-init`. Acceptance: `rtk git worktree list --porcelain` in that repository lists a route ending in `worktrees/islamic-be-init`. Record it in the Provisioned Worktree Identity block above.
- [ ] [AI] Verify byte-identity is intact before touching it: `rtk diff -ru /Users/wkf/ose-projects/ose-public/worktrees/islamic-be-init/apps/rhino-cli/src /Users/wkf/ose-projects/ose-private/worktrees/islamic-be-init/apps/rhino-cli/src`. Acceptance: no differences; save to `evidence/du5-preflight-diff.txt`.

### AC-ENV-GO — `lang: go` resolves to a real scanner

- **Input:** the existing dispatch at `Env.fs:1590`–`:1592`, and `scanFsharpReads` at `Env.fs:1516` as the structural model.
- **Outcome:** an `env-contract` surface declaring `lang: go` is scanned rather than rejected.

- [ ] [AI] Enumerate `specs/apps/rhino/cli/behaviours/env/` with `rtk ls specs/apps/rhino/cli/behaviours/env/` and record the exact feature files in the execution ledger before editing — acceptance: the bounded family from `tech-docs.md` §3 is resolved to named paths
- [ ] [AI] **RED (gherkin):** add scenarios covering the Go scanner — an `os.Getenv` read is detected, an `os.LookupEnv` read is detected, a framework-owned key is filtered, and an unsupported language still errors. Run `rtk ./hippo run --class ephemeral --disk-path . -- npm exec nx -- run rhino-cli:test:coverage:behaviour`; acceptance: the new scenarios report as unbound, per the Iron Rule
- [ ] [AI] **RED (unit):** add failing unit cases to the RhinoCli unit test project beside the existing `scanFsharpReads` cases. Discover the owning file with `rtk grep -rn "scanFsharpReads" apps/rhino-cli/tests/`. Run `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run rhino-cli:test:unit`; acceptance: the new cases fail
- [ ] [AI] **GREEN (scanner):** add `scanGoReads` to `apps/rhino-cli/src/RhinoCli.Application/src/Env.fs` mirroring `scanFsharpReads`, scanning the module root (not `root/src`, which a Go module does not have) and skipping `generated-contracts/` — acceptance: the function carries the same `[<ExcludeFromCodeCoverage>]` marker and documented coverage boundary as its siblings
- [ ] [AI] **GREEN (dispatch):** add a `| "go" -> scanGoReads root` case at `Env.fs:1591` — acceptance: `lang: go` no longer returns `unsupported lang: go`
- [ ] [AI] **GREEN (bind):** bind the new scenarios and rerun both targets — acceptance: `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run rhino-cli:test:quick` exits zero with every new scenario bound

### Byte-Identity Convergence

- [ ] [AI] Copy the changed `apps/rhino-cli` sources into the private worktree so both trees are identical. Acceptance: `rtk diff -ru /Users/wkf/ose-projects/ose-public/worktrees/islamic-be-init/apps/rhino-cli/src /Users/wkf/ose-projects/ose-private/worktrees/islamic-be-init/apps/rhino-cli/src` reports no differences
- [ ] [AI] Stage the `Env.fs` and test changes in **both** worktrees, then regenerate the manifest in each with `rtk apps/rhino-cli/scripts/rhino-bin.sh parity manifest generate`. The manifest describes the **staged** tree, so it must be generated after staging and committed in the same commit as the source edit. Acceptance: `apps/rhino-cli/parity-manifest.sha256` changes in both worktrees. Never hand-edit a hash
- [ ] [AI] Confirm the two regenerated manifests are byte-identical: `rtk diff -u /Users/wkf/ose-projects/ose-public/worktrees/islamic-be-init/apps/rhino-cli/parity-manifest.sha256 /Users/wkf/ose-projects/ose-private/worktrees/islamic-be-init/apps/rhino-cli/parity-manifest.sha256`. Acceptance: no differences; save to `evidence/du5-manifest-diff.txt`
- [ ] [AI] Validate the manifest against the staged tree in each repository: `rtk apps/rhino-cli/scripts/rhino-bin.sh parity manifest validate`. Acceptance: each reports `apps/rhino-cli/parity-manifest.sha256 is current`

### Integration

- [ ] [AI] Commit in each repository on `islamic-be-init/du5-rhino-go-env` with the source edit and the regenerated manifest in **one** commit, message `feat(rhino-cli): scan Go source for environment reads`. Acceptance: `rtk git show --stat` in each lists both `Env.fs` and `parity-manifest.sha256`
- [ ] [AI] Push both branches and open a draft PR in each repository, each body stating the new-code cost/benefit and naming its counterpart PR. Acceptance: both PRs exist and cross-reference
- [ ] [AI] Poll CI every 2 minutes in both repositories until `pr-quality-gate.yml` and `pr-leak-review` complete on each current head — acceptance: all report success; never use `gh run watch`
- [ ] [AI] Merge both pull requests within the same working session, so the nightly parity audit never observes a mismatched pair. Acceptance: both merge; record each PR number and 40-character head SHA in the Delivery Branch Inventory
- [ ] [AI] Record the unconverged counterpart as a sibling obligation in `learnings.md` from the moment the first PR merges until the second does — acceptance: the entry names the outstanding repository and is cleared only when both are in

### Phase 5 Gate

> All checks below must pass before starting Phase 6.

- [ ] [AI] `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run rhino-cli:test:quick` in **both** repositories — exits zero in each
- [ ] [AI] Recursive diff of `apps/rhino-cli/src`, `project.json`, `LICENSE`, and `parity-manifest.sha256` across repositories — reports zero differences
- [ ] [AI] `rtk apps/rhino-cli/scripts/rhino-bin.sh parity manifest validate` in both — each reports the manifest is current
- [ ] [AI] `rtk gh workflow run rhino-cli-parity-audit.yml --repo wahidyankf/ose-private` completes successfully against the merged state — save the run URL to `evidence/du5-parity-audit.txt`
- [ ] [AI] Confirm both `repo-config.yml` files carry an identical top-level key set — acceptance: the schema-parity comparison reports no difference

> **Pause Safety**: both repositories carry the Go env scanner and a matching regenerated parity
> manifest byte-identically, and every existing env surface still validates. No app is registered
> with `lang: go` yet, so behaviour is unchanged. Safe to stop. To resume:
> `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run rhino-cli:test:quick`.

## Phase 6 (DU6): Registry and Documentation

Delivery boundary. Requires DU3, DU4, and DU5 merged.

- [ ] [AI] Add the `apps/islamic-be` surface to `repo-config.yml`'s `env-contract:` with `kind: app`, `lang: go`, and an allowlist entry for `APP_ENV` if the tier-selection variable is used — acceptance: `npm exec nx -- run rhino-cli:env:validation` exits zero with the new surface included
- [ ] [AI] Add `islamic-be` (port 8402) to `docs/reference/web-sites.md`'s app table and `ISLAMIC_BE_PORT` to its override table — acceptance: both tables list the service
- [ ] [AI] Confirm the Supporting Service Ports table needs no new row — acceptance: the plan's stateless decision (D-5) means no PostgreSQL or NATS host port is claimed
- [ ] [AI] Add both projects to `docs/reference/monorepo-structure.md`'s Current Apps list — acceptance: `islamic-be` and `islamic-be-e2e` appear with one-line descriptions
- [ ] [AI] Add the service to `docs/reference/system-architecture/applications.md` — acceptance: the application map includes it
- [ ] [AI] Add `islamic-be` to `apps/README.md`'s product map and `islamic-be-e2e` to its end-to-end tests table — acceptance: both tables link the new READMEs
- [ ] [AI] Update `plans/in-progress/README.md`'s Active Plans list to name this plan — acceptance: the placeholder "No plans are in progress" is replaced
- [ ] [AI] Run the documentation link check across the changed files — acceptance: no broken internal links
- [ ] [AI] Commit on `islamic-be-init/du6-registry`, push, open a draft PR, poll CI every 2 minutes, and merge when green — acceptance: the PR merges to `main`

### Phase 6 Gate

> All checks below must pass before starting Phase 7.

- [ ] [AI] `npm exec nx -- run rhino-cli:env:validation` — exits zero with `apps/islamic-be` registered and no drift finding
- [ ] [AI] `npm exec nx -- run-many -t test:quick --projects=islamic-be,islamic-be-e2e,islamic-contracts` — all three exit zero
- [ ] [AI] `npm run lint:md` — no markdownlint findings in the changed documentation
- [ ] [AI] Confirm no `.env` file other than `.env.example` was committed — acceptance: `git ls-files 'apps/islamic-be/.env*'` lists only `.env.example`

> **Pause Safety**: the service, its E2E suite, its contract, its Go lane, and every registry entry
> are complete and green in both repositories. This is the plan's functional end state. Safe to stop.
> To resume: `npm exec nx -- run-many -t test:quick --projects=islamic-be,islamic-be-e2e`.

## Phase 7: Knowledge Capture

Opens a PR only if a learning routes to a durable home in this repository.

- [ ] [AI] Run both safety gates — secret/sensitivity and repo-relevance — over every `learnings.md` entry — acceptance: each entry is cleared or removed with a stated reason
- [ ] [AI] Route each surviving entry to exactly one durable home: a convention, a doc, an agent, a skill, code, a test, or a post-mortem — acceptance: every entry names its destination
- [ ] [AI] Land small non-code routings inline in this plan's commits — acceptance: the routed content exists at its destination
- [ ] [AI] For each large non-code routing and **every** code routing, author a `plans/ideas/` two-pager only with literal user authorization; otherwise record `Reported without plan authorization` and surface it to the user — acceptance: no `plans/backlog/` folder is created directly
- [ ] [AI] Discard non-generalizable entries with a one-line reason each — acceptance: no entry is left untriaged
- [ ] [AI] If nothing generalizable emerged, record the explicit `No generalizable learnings — <reason>` escape — acceptance: the escape text is present in `learnings.md`

### Phase 7 Gate

> All checks below must pass before starting Phase 8.

- [ ] [AI] Confirm every `learnings.md` entry has reached a terminal state — routed inline, filed as a two-pager, reported without plan authorization, or discarded — acceptance: no entry lacks a disposition
- [ ] [AI] `npm run lint:md` — exits zero across any newly routed documentation

> **Pause Safety**: all knowledge is routed to durable homes; `learnings.md` holds nothing the
> repository still depends on. Safe to stop. To resume: re-read `learnings.md` and confirm every
> entry carries a disposition.

## Phase 8: Plan Archival

- [ ] [AI] Confirm every phase gate above is ticked and every PR is merged — acceptance: Phases 0 through 7 show no unticked gate item
- [ ] [AI] Reconcile the Delivery Branch Inventory: mark each branch `delivered` with its PR number and reviewed head SHA — acceptance: no branch remains `pending`
- [ ] [AI] Remove `worktrees/islamic-be-init/` and its branches after confirming nothing is uncommitted — acceptance: `git worktree list` no longer lists the route and the identity block authorizes the removal
- [ ] [AI] Update `plans/in-progress/README.md` to remove this plan from Active Plans — acceptance: the list no longer names it
- [ ] [AI] `git mv plans/in-progress/islamic-be-init/ plans/done/YYYY-MM-DD__islamic-be-init/` using the completion date — acceptance: the folder carries a date prefix
- [ ] [AI] Update the plan README status to Complete — acceptance: the status line no longer reads In Progress

### Phase 8 Gate

- [ ] [AI] `npm exec nx -- run-many -t test:quick --projects=islamic-be,islamic-be-e2e,islamic-contracts,rhino-cli` — exits zero
- [ ] [AI] `git worktree list --porcelain` — no `islamic-be-init` entry remains
- [ ] [AI] Confirm the plan folder resolves under `plans/done/` with a completion-date prefix — acceptance: the path matches `plans/done/YYYY-MM-DD__islamic-be-init/`

> **Pause Safety**: the plan is archived, the worktree is removed, and both repositories are green.
> Nothing remains in flight. To re-verify:
> `npm exec nx -- run-many -t test:quick --projects=islamic-be,islamic-be-e2e`.

## See Also

- [README.md](./README.md) — plan overview and scope.
- [tech-docs.md](./tech-docs.md) — architecture, decisions, and file-impact analysis.
- [Worktree Specification](../../../repo-governance/conventions/structure/plans/worktree-specification.md)
- [Cross-Repository Parity Identity](../../../repo-governance/development/workflow/cross-repository-parity-identity.md)
