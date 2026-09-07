# Delivery Checklist — islamic-be-init

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.

**Delivery Mode**: `worktree-to-pr`. Every phase from 1 onward ends in a PR; Phase 0 opens none.

## Worktree

### Provisioned Worktree Identity

- Declared repository-relative route: `worktrees/islamic-be-init/`
- Initial branch: `islamic-be-init-base`
- Created by: _recorded at Phase 0_
- Created at: _recorded at Phase 0 (ISO-8601 UTC)_

> The pre-existing `worktrees/ose-islamic/` checkout was an ad-hoc authoring workspace created before
> this plan existed. It is not this plan's worktree and is removed at Phase 0.

### Cross-Repository Parity Identity

- Objective slug: `rhino-go-env-scanner`
- Worktree basename: `islamic-be-init`

| Repository    | Corresponding short-lived branch |
| ------------- | -------------------------------- |
| `ose-public`  | `islamic-be-init-rhino-go-env`   |
| `ose-private` | `islamic-be-init-rhino-go-env`   |

> Applies to Phase 5 only. Phases 1–4 and 6 are `ose-public`-only delivery units and record
> `not applicable` for the parity branch mapping.

### Delivery Branch Inventory

| Branch                         | Mode             | Lifecycle state | Proof                                   |
| ------------------------------ | ---------------- | --------------- | --------------------------------------- |
| `islamic-be-init-base`         | `provisioned`    | `pending`       | recorded at Phase 0                     |
| `islamic-be-init-go-lane`      | `worktree-to-pr` | `pending`       | Phase 1 PR                              |
| `islamic-be-init-specs`        | `worktree-to-pr` | `pending`       | Phase 2 PR                              |
| `islamic-be-init-service`      | `worktree-to-pr` | `pending`       | Phase 3 PR                              |
| `islamic-be-init-e2e`          | `worktree-to-pr` | `pending`       | Phase 4 PR                              |
| `islamic-be-init-rhino-go-env` | `worktree-to-pr` | `pending`       | Phase 5 PR pair (both repositories)     |
| `islamic-be-init-registry`     | `worktree-to-pr` | `pending`       | Phase 6 PR                              |

## Phase 0: Environment Setup and Baseline

Opens no PR. Establishes a green starting point and a correctly named worktree.

- [ ] [AI] Confirm the current checkout is clean and note the `main` SHA it is based on — acceptance: `git status` reports a clean tree and the base SHA is recorded in this file
- [ ] [AI] Provision `worktrees/islamic-be-init/` from current `main` with initial branch `islamic-be-init-base` — acceptance: `git worktree list --porcelain` shows the route and branch
- [ ] [AI] Record the creator and ISO-8601 UTC creation time in the Provisioned Worktree Identity block above — acceptance: no placeholder text remains in that block
- [ ] [AI] Remove the superseded `worktrees/ose-islamic/` checkout and its branch once this plan's files are committed — acceptance: `git worktree list` no longer lists it and the worktree cap of one per repo per plan holds
- [ ] [AI] Verify `go version` reports 1.26.x, `oapi-codegen --version` reports v2.x, and `golangci-lint --version` reports 2.x — acceptance: all three print versions matching `tech-docs.md` §5
- [ ] [AI] Confirm `apps/rhino-cli/src` is currently byte-identical with `ose-private` — acceptance: a recursive diff of `src/`, `project.json`, and `LICENSE` reports no differences
- [ ] [AI] Run the scoped baseline `npm exec nx -- run-many -t test:quick --projects=ose-be,ose-be-e2e,rhino-cli` — acceptance: all three pass, or every pre-existing failure is resolved before Phase 1 begins
- [ ] [AI] Run `npm exec nx -- run rhino-cli:env:validation` — acceptance: exits zero, establishing the pre-change env-contract baseline

### Phase 0 Gate

> All checks below must pass before starting Phase 1. If any check fails, fix it in Phase 0 before
> proceeding.

- [ ] [AI] `git worktree list --porcelain` — shows `worktrees/islamic-be-init/` on `islamic-be-init-base` and no `ose-islamic` entry
- [ ] [AI] `npm exec nx -- run-many -t test:quick --projects=ose-be,ose-be-e2e,rhino-cli` — exits zero
- [ ] [AI] `npm exec nx -- run rhino-cli:env:validation` — exits zero
- [ ] [AI] `go version && golangci-lint --version && oapi-codegen --version` — all three resolve

> **Pause Safety**: the repository is unchanged apart from this plan's own files; a correctly named
> worktree exists and the toolchain is confirmed. Safe to stop. To resume:
> `npm exec nx -- run-many -t test:quick --projects=ose-be,ose-be-e2e,rhino-cli`.

## Phase 1: Go Platform Lane

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

**CI job**

- [ ] [AI] Create `.github/actions/setup-go/action.yml` reading `go-version-file: apps/islamic-be/go.mod`, with module and build caching and a pinned `golangci-lint` install — acceptance: the action file parses and pins the versions named in `tech-docs.md` §5
- [ ] [AI] Edit `.github/workflows/pr-quality-gate.yml`: add `has-go` to the `detect` job outputs and a `lang:go)` case to its tag switch — acceptance: the `detect` job initialises and sets `has-go` alongside `has-ts`, `has-dotnet-projects`, and `has-dart`
- [ ] [AI] Add a `go` job gated on `has-go == 'true'` running `npx nx affected -t typecheck lint test:quick compat:min-version --exclude='tag:lang:ts,tag:lang:fsharp,tag:lang:csharp,tag:lang:rust,tag:lang:dart' --parallel=1` — acceptance: the job exists and provisions `setup-node` plus `setup-go`
- [ ] [AI] Add `tag:lang:go` to the `typescript` job's `--exclude` list — acceptance: the exclude list names `lang:go` and the `typescript` job can no longer select a Go project
- [ ] [AI] Add `tag:lang:go` to the `flutter` job's `--exclude` list — acceptance: the exclude list names `lang:go`
- [ ] [AI] Add the `go` job to the `quality-gate` aggregation job's `needs` and its skipped-job tolerance logic — acceptance: a PR touching no Go project still reports the aggregate gate green

**Behaviour-coverage Go extractor**

- [ ] [AI] Add `extractGoBindings(resourceName, source)` to `scripts/behaviour-coverage.mjs` handling interpreted strings, backtick raw strings, `regexp.MustCompile` wrappers, and the `Given`/`When`/`Then` keyword-sensitive forms — acceptance: the function is exported alongside the F# and TypeScript extractors
- [ ] [AI] Extend `extractBindings` to dispatch `.go` to the new extractor — acceptance: a `.go` resource no longer falls through to `extractTypescriptBindings`
- [ ] [AI] Add fixtures to `scripts/behaviour-coverage.test.mjs` covering each registration form plus negative cases (a regex literal in non-registration code, a commented-out registration, a backtick string that is not a step) — acceptance: `npm run test:validators` exits zero and the new cases fail if the extractor is reverted
- [ ] [AI] Confirm Go comment and raw-string handling does not corrupt the existing F#/TypeScript paths — acceptance: the pre-existing validator tests still pass unchanged

**Integration**

- [ ] [AI] Commit on `islamic-be-init-go-lane`, push, and open a draft PR stating the new-code cost/benefit — acceptance: the PR body names the CI leak this fixes and links `tech-docs.md` §1.4
- [ ] [AI] Poll CI every 2 minutes until `pr-quality-gate.yml` and `pr-leak-review` complete on the current head — acceptance: both report success; never use `gh run watch`
- [ ] [AI] Mark ready and merge once the hardened preconditions hold — acceptance: the PR merges to `main`

### Phase 1 Gate

> All checks below must pass before starting Phase 3. Phase 2 may proceed in parallel.

- [ ] [AI] `npm run test:validators` — exits zero with the new Go extractor cases present
- [ ] [AI] `npm exec nx -- run rhino-cli:repo-config:validation` — exits zero
- [ ] [AI] `npm exec nx -- run-many -t test:quick --projects=ose-be,ose-be-e2e` — exits zero, proving no regression to existing lanes
- [ ] [AI] Confirm the merged `pr-quality-gate.yml` excludes `tag:lang:go` in both the `typescript` and `flutter` jobs — acceptance: `grep -c 'tag:lang:go' .github/workflows/pr-quality-gate.yml` reports at least 2

> **Pause Safety**: the Go lane exists and every gate is registered, but no Go project does — the
> `go` job is correct and dormant. Nothing else changed behaviour. Safe to stop. To resume:
> `npm run test:validators`.

## Phase 2: Specs Corpus and Contracts

Delivery boundary. Independent of Phase 1; may run before, after, or concurrently.

- [ ] [AI] Create `specs/apps/islamic/README.md` and `specs/apps/islamic/overview.md` following the shape of `specs/apps/ose/` — acceptance: `rhino-cli specs structure validate` accepts the new product folder
- [ ] [AI] Create `specs/apps/islamic/be/README.md` describing the corpus, and `architecture.md` with C4 context, container, and component diagrams using the accessible palette — acceptance: both files exist and every Mermaid `classDef` uses palette hex codes
- [ ] [AI] Create `specs/apps/islamic/be/behaviours/health/` with `README.md` and `health.feature` carrying the three US-1 scenarios from `prd.md` verbatim — acceptance: `npx gherkin` parses the feature and scenario names match `prd.md`
- [ ] [AI] Create `specs/apps/islamic/be/behaviours/config/` with `README.md` and `port-resolution.feature` carrying the five US-3 scenarios — acceptance: the feature parses and all five scenarios are present
- [ ] [AI] Create `specs/apps/islamic/be/contracts/openapi.yaml` (OpenAPI 3.1) with `paths/health.yaml`, `schemas/health.yaml`, and `schemas/error.yaml`, plus a README for each folder — acceptance: the root document references the fragments and every folder carries an annotated index
- [ ] [AI] Copy `.spectral.yaml` from `specs/apps/ose/be/contracts/` unchanged — acceptance: the two ruleset files are byte-identical
- [ ] [AI] Create `specs/apps/islamic/be/contracts/project.json` registering `islamic-contracts` with `lint`, `bundle`, `docs`, `typecheck`, `test:quick`, `deps:audit`, `compat:min-version`, and `specs:structure-validation` targets, plus `namedInputs.specs` — acceptance: `npx nx show project islamic-contracts` resolves
- [ ] [AI] Create `specs/apps/islamic/be/contracts/generated/README.md` explaining that bundles are generated — acceptance: the file exists and the folder is otherwise gitignored
- [ ] [AI] Commit on `islamic-be-init-specs`, push, open a draft PR, poll CI every 2 minutes, and merge when green — acceptance: the PR merges to `main`

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [ ] [AI] `npm exec nx -- run islamic-contracts:lint` — bundles and Spectral-lints with zero errors
- [ ] [AI] `npm exec nx -- run islamic-contracts:test:quick` — exits zero
- [ ] [AI] `npm exec nx -- run islamic-contracts:specs:structure-validation` — exits zero
- [ ] [AI] Confirm every new Nx project declares `namedInputs.specs` — acceptance: `npx nx show project islamic-contracts --json | jq '.namedInputs.specs'` returns a non-null array

> **Pause Safety**: the specification corpus and contract exist and validate; no code implements them
> yet, which is the intended contract-first state. Safe to stop. To resume:
> `npm exec nx -- run islamic-contracts:test:quick`.

## Phase 3: The islamic-be Service

Delivery boundary. Requires Phases 1 and 2 merged.

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
- [ ] [AI] Commit on `islamic-be-init-service`, push, open a draft PR, poll CI every 2 minutes, and merge when green — acceptance: the PR merges to `main`

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [ ] [AI] `npm exec nx -- run islamic-be:test:quick` — exits zero, including the 99% coverage floor and both static coverage validators
- [ ] [AI] `npm exec nx -- run islamic-be:lint` — `golangci-lint` reports no findings
- [ ] [AI] `npm exec nx -- run islamic-be:build` — produces `apps/islamic-be/dist/islamic-be`
- [ ] [AI] Confirm the merged PR's CI run shows the `go` job green **and** the `typescript` job not selecting any Go target — acceptance: the `go` job log lists `islamic-be` and the `typescript` job log does not
- [ ] [AI] `curl -s localhost:8402/api/v1/health` against a locally running instance — returns 200 with `{"status":"healthy"}`, captured to `evidence/phase-3-health.txt`

> **Pause Safety**: `islamic-be` builds, tests, lints, and serves its health endpoint; its Gherkin is
> bound at the Unit layer. The E2E layer is not yet implemented, so `test:coverage:e2e` reports its
> scenarios as unbound until Phase 4. Safe to stop. To resume:
> `npm exec nx -- run islamic-be:test:quick`.

## Phase 4: The islamic-be-e2e Suite

Delivery boundary. Requires Phase 3 merged.

- [ ] [AI] Create `apps/islamic-be-e2e/package.json`, `tsconfig.json`, and `playwright.config.ts` mirroring `apps/ose-be-e2e/` with `bddgen` pointed at the islamic corpus — acceptance: `npx bddgen` generates test files from the health feature
- [ ] [AI] Implement `steps/backend-process.ts` starting and stopping the real `islamic-be` process on a controlled port — acceptance: the suite starts the service itself and shuts it down deterministically
- [ ] [AI] Implement `steps/health.steps.ts` and `utils/response-store.ts` binding the health scenarios over real HTTP — acceptance: all three US-1 scenarios pass against the running process
- [ ] [AI] Create `behaviour-coverage.json` with the corpus and an `e2e` adapter — acceptance: the file mirrors the `ose-be-e2e` shape
- [ ] [AI] Create `project.json` with the E2E target surface, tags `["type:e2e","platform:playwright","lang:ts","domain:islamic"]`, `implicitDependencies: ["islamic-be"]`, and `namedInputs.specs` — acceptance: the project declares no Unit or Integration target
- [ ] [AI] Decide and record whether the config scenarios need an `e2e-coverage-baseline.json` `allowedUnbound` entry, with a written reason for each — acceptance: every unbound scenario carries a stated reason or is bound
- [ ] [AI] Write `apps/islamic-be-e2e/README.md` — acceptance: it explains what the suite covers and how to run it
- [ ] [AI] Commit on `islamic-be-init-e2e`, push, open a draft PR, poll CI every 2 minutes, and merge when green — acceptance: the PR merges to `main`

### Phase 4 Gate

> All checks below must pass before starting Phase 6. Phase 5 may proceed in parallel.

- [ ] [AI] `npm exec nx -- run islamic-be-e2e:test:e2e` — all scenarios pass against a real process
- [ ] [AI] `npm exec nx -- run islamic-be-e2e:test:quick` — exits zero
- [ ] [AI] `npm exec nx -- run islamic-be:test:coverage` — every adapter reports its scenarios bound or explicitly allowed
- [ ] [AI] Capture the passing E2E run output to `evidence/phase-4-e2e.txt` — acceptance: the file records the scenario count and result

> **Pause Safety**: the full test pyramid is green — Unit bindings, E2E bindings, and static coverage
> across both. The service is complete and gated; only registry documentation and env drift-checking
> remain. Safe to stop. To resume: `npm exec nx -- run islamic-be-e2e:test:e2e`.

## Phase 5: rhino-cli Go Env Scanner (Cross-Repository Parity)

Delivery boundary spanning two repositories. Independent of Phases 1–4; gates only Phase 6.

> **Parity preflight**: before the first mutation in either repository, confirm the branch name
> `islamic-be-init-rhino-go-env` is available in both and that no existing branch of that name belongs
> to a different delivery. Record the probe result in `learnings.md`.

- [ ] [AI] Enumerate `specs/apps/rhino/cli/behaviours/env/` and record the exact feature files in the execution ledger before editing — acceptance: the bounded family from `tech-docs.md` §3 is resolved to named paths
- [ ] [AI] Add Gherkin scenarios covering the Go scanner: a `os.Getenv` read is detected, a `os.LookupEnv` read is detected, a framework-owned key is filtered, and an unsupported language still errors — acceptance: the scenarios parse and are unbound at first, per the Iron Rule
- [ ] [AI] Add `scanGoReads` to `apps/rhino-cli/src/RhinoCli.Application/src/Env.fs` mirroring `scanFsharpReads`, scanning the module root (not `root/src`) and skipping `generated-contracts/` — acceptance: the function carries the same `[<ExcludeFromCodeCoverage>]` marker and documented coverage boundary as its siblings
- [ ] [AI] Add a `"go" -> scanGoReads root` case to the `validateAppSurface` dispatch at `Env.fs` — acceptance: `lang: go` no longer returns `unsupported lang: go`
- [ ] [AI] Bind the new scenarios and confirm they now pass — acceptance: `npm exec nx -- run rhino-cli:test:quick` exits zero with the new scenarios bound
- [ ] [AI] Apply the identical change in `ose-private` on the same branch name — acceptance: a recursive diff of `apps/rhino-cli/src`, `project.json`, and `LICENSE` between the two repositories reports zero differences
- [ ] [AI] Open a draft PR in each repository, poll CI every 2 minutes in both, and merge each as soon as its own preconditions hold — acceptance: both merge; neither is held back to align merge times
- [ ] [AI] Record the unconverged counterpart as a sibling obligation until the second PR merges — acceptance: `learnings.md` names the outstanding repository until both are in

### Phase 5 Gate

> All checks below must pass before starting Phase 6.

- [ ] [AI] `npm exec nx -- run rhino-cli:test:quick` in **both** repositories — exits zero in each
- [ ] [AI] Recursive diff of `apps/rhino-cli/src`, `Cargo.toml` equivalents, `project.json`, and `LICENSE` across repositories — reports zero differences
- [ ] [AI] Confirm the `rhino-cli-parity-audit.yml` workflow passes on `main` in `ose-public` — acceptance: the most recent run is green
- [ ] [AI] Confirm both `repo-config.yml` files carry an identical top-level key set — acceptance: the schema-parity comparison reports no difference

> **Pause Safety**: both repositories carry the Go env scanner byte-identically and every existing
> env surface still validates. No app is registered with `lang: go` yet, so behaviour is unchanged.
> Safe to stop. To resume: `npm exec nx -- run rhino-cli:test:quick`.

## Phase 6: Registry and Documentation

Delivery boundary. Requires Phases 3, 4, and 5 merged.

- [ ] [AI] Add the `apps/islamic-be` surface to `repo-config.yml`'s `env-contract:` with `kind: app`, `lang: go`, and an allowlist entry for `APP_ENV` if the tier-selection variable is used — acceptance: `npm exec nx -- run rhino-cli:env:validation` exits zero with the new surface included
- [ ] [AI] Add `islamic-be` (port 8402) to `docs/reference/web-sites.md`'s app table and `ISLAMIC_BE_PORT` to its override table — acceptance: both tables list the service
- [ ] [AI] Confirm the Supporting Service Ports table needs no new row — acceptance: the plan's stateless decision (D-5) means no PostgreSQL or NATS host port is claimed
- [ ] [AI] Add both projects to `docs/reference/monorepo-structure.md`'s Current Apps list — acceptance: `islamic-be` and `islamic-be-e2e` appear with one-line descriptions
- [ ] [AI] Add the service to `docs/reference/system-architecture/applications.md` — acceptance: the application map includes it
- [ ] [AI] Add `islamic-be` to `apps/README.md`'s product map and `islamic-be-e2e` to its end-to-end tests table — acceptance: both tables link the new READMEs
- [ ] [AI] Update `plans/in-progress/README.md`'s Active Plans list to name this plan — acceptance: the placeholder "No plans are in progress" is replaced
- [ ] [AI] Run the documentation link check across the changed files — acceptance: no broken internal links
- [ ] [AI] Commit on `islamic-be-init-registry`, push, open a draft PR, poll CI every 2 minutes, and merge when green — acceptance: the PR merges to `main`

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
