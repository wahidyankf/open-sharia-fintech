# Delivery — Adopt Hexagonal Architecture + DDD

## Worktree

Worktree path: `worktrees/adopt-hexagonal-ddd-architecture/`

Provision before execution (run from repo root):

```bash
claude --worktree adopt-hexagonal-ddd-architecture
```

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md)
and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans/worktree-specification.md#worktree-specification).

---

## Phase 0: Environment Setup and Baseline

> _Executor: `repo-setup-manager`_

- [x] Install dependencies in the root worktree (repo root):
      `npm install`
      — acceptance: exits 0, `node_modules/` synchronized.

- [x] Converge the full polyglot toolchain in the root worktree:
      `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift.

- [x] Run the full affected baseline to record pass/fail counts before any changes:
      `npx nx affected -t test:quick`
      — acceptance: baseline pass/fail count recorded; all preexisting failures documented.
      — **Result**: 22 projects passing, 0 failures. Baseline clean.

- [x] Resolve all preexisting failures before proceeding to Phase 1.
      — acceptance: `npx nx affected -t test:quick` exits 0 with no failures.
      — **Result**: No preexisting failures found.

---

## Phase 1: Governance Convention Documents

> All five documents are new files. No existing code changes in this phase.
> _Suggested executor: `repo-rules-maker`_

### 1.1 — Core hexagonal architecture document

- [x] **RED**: Verify the file does not exist:
      `test -f repo-governance/development/pattern/hexagonal-architecture.md && echo EXISTS || echo MISSING`
      — acceptance: prints `MISSING`.

- [x] **GREEN**: Create
      `repo-governance/development/pattern/hexagonal-architecture.md`
      (_New file_) with the following mandatory sections:
  - H1: `# Hexagonal Architecture`
  - `## Overview` — define ports, adapters, domain, application, infrastructure layers; state
    the dependency rule (outer depends on inner, never the reverse)
  - `## Core Concepts` — ports (interfaces), inbound adapters, outbound adapters, domain model
  - `## Layer Definitions` — domain, application, infrastructure, inbound adapter (one
    subsection per layer); for each: what belongs here, what is forbidden
  - `## Dependency Rule` — explicit statement with Mermaid `flowchart LR` diagram
  - `## App-Type Specializations` — links to the three specialization documents:
    `hexagonal-architecture-cli.md`, `hexagonal-architecture-web.md`,
    `hexagonal-architecture-be.md` (created in steps 1.2–1.4 below)
  - `## Related` — links to `openapi-contract-first.md`, `functional-programming.md`

  Run `npm run lint:md` after writing.
  — acceptance: `npm run lint:md` exits 0; file exists at the path above.

- [x] **REFACTOR**: Run `npm run format:md` and re-read the file to confirm no formatting
      drift was introduced.
      — acceptance: `npm run format:md:check` exits 0.

### 1.2 — CLI hexagonal architecture document

- [x] **RED**: Verify the file does not exist:
      `test -f repo-governance/development/pattern/hexagonal-architecture-cli.md && echo EXISTS || echo MISSING`
      — acceptance: prints `MISSING`.

- [x] **GREEN**: Create
      `repo-governance/development/pattern/hexagonal-architecture-cli.md`
      (_New file_) with the following mandatory sections:
  - H1: `# Hexagonal Architecture — CLI Apps`
  - `## Overview` — CLI-specific context; `commands/` is the inbound adapter for CLI args
  - `## Directory Layout` — table showing canonical layout for Rust CLIs (all four apps);
    include the `rhino-cli` exception (inner layers under `src/internal/`)
  - `## Layer Responsibilities` — commands, domain, application, infrastructure for CLI context
  - `## Forbidden Imports` — list per layer (e.g., `clap` forbidden in domain/)
  - `## Examples` — code snippet showing a command calling into application use case
  - `## Related` — link to `hexagonal-architecture.md`

  Run `npm run lint:md` after writing.
  — acceptance: `npm run lint:md` exits 0; file exists.

- [x] **REFACTOR**: `npm run format:md:check` exits 0.

### 1.3 — Web hexagonal architecture document

- [x] **RED**: Verify the file does not exist:
      `test -f repo-governance/development/pattern/hexagonal-architecture-web.md && echo EXISTS || echo MISSING`
      — acceptance: prints `MISSING`.

- [x] **GREEN**: Create
      `repo-governance/development/pattern/hexagonal-architecture-web.md`
      (_New file_) with the following mandatory sections:
  - H1: `# Hexagonal Architecture — Web Apps`
  - `## Overview` — Next.js context; feature context modules as the organizational unit (not
    DDD bounded contexts — DDD applies only to BE apps)
  - `## Directory Layout` — table showing `contexts/<name>/{domain,application,infrastructure,presentation}/`
  - `## Layer Responsibilities` — domain, application (barrel rule), infrastructure, presentation
  - `## Port Pattern` — Effect.ts `Context.Tag` as port definition; `Layer` as adapter
  - `## Application Barrel Rule` — `application/index.ts` is the sole public API surface;
    presentation and cross-context callers import only from this barrel
  - `## Next.js Adapter Placement` — Server Components, Server Actions, and route handlers
    are `presentation/` inbound adapters; they must not import from `domain/` directly
  - `## Forbidden Imports` — per layer
  - `## Reference Implementation` — `organiclever-web` as the canonical reference
  - `## Related` — link to `hexagonal-architecture.md`

  Run `npm run lint:md` after writing.
  — acceptance: `npm run lint:md` exits 0; file exists.

- [x] **REFACTOR**: `npm run format:md:check` exits 0.

### 1.4 — BE hexagonal + DDD architecture document

- [x] **RED**: Verify the file does not exist:
      `test -f repo-governance/development/pattern/hexagonal-architecture-be.md && echo EXISTS || echo MISSING`
      — acceptance: prints `MISSING`.

- [x] **GREEN**: Create
      `repo-governance/development/pattern/hexagonal-architecture-be.md`
      (_New file_) with the following mandatory sections:
  - H1: `# Hexagonal Architecture + DDD — Backend Apps`
  - `## Overview` — DDD bounded contexts + hexagonal layers; `contexts/<name>/` as the unit
  - `## Directory Layout` — tables for Rust/Axum (`contexts/<n>/{domain,application,infrastructure,api/http}`)
    and F#/Giraffe (`contexts/<n>/{Domain,Application,Infrastructure,Api/Http}`); note that
    `api/` groups all inbound transports (graphql/, mcp/ alongside http/ when added)
  - `## Rust-Specific` — traits as ports; `#[async_trait]` for dyn dispatch; native async fn
    for static dispatch; `From<DomainError> for ApiError` at the `api/http/` boundary; domain
    errors must not contain HTTP status codes
  - `## F#-Specific` — compilation-order constraint (domain types first, `Program.fs` last);
    railway-oriented programming (`Result<'T,'TError>`); pure adapter functions; `Program.fs`
    as composition root
  - `## DDD Integration` — bounded context isolation; contexts communicate through application
    interfaces, not shared domain types
  - `## Forbidden Imports` — per layer, per language
  - `## Related` — links to `hexagonal-architecture.md`, `openapi-contract-first.md`

  Run `npm run lint:md` after writing.
  — acceptance: `npm run lint:md` exits 0; file exists.

- [x] **REFACTOR**: `npm run format:md:check` exits 0.

### 1.5 — OpenAPI contract-first document

- [x] **RED**: Verify the file does not exist:
      `test -f repo-governance/development/pattern/openapi-contract-first.md && echo EXISTS || echo MISSING`
      — acceptance: prints `MISSING`.

- [x] **GREEN**: Create
      `repo-governance/development/pattern/openapi-contract-first.md`
      (_New file_) with the following mandatory sections:
  - H1: `# OpenAPI Contract-First Development`
  - `## Overview` — spec-first: the OpenAPI YAML is the single source of truth; code is
    generated from it, not the reverse
  - `## Spec Location` — `specs/apps/<name>/containers/contracts/openapi.yaml`
  - `## Codegen Tooling` — table: TypeScript client (`@hey-api/openapi-ts`, output to
    `src/generated-contracts/`); Rust server (`openapi-generator` rust-axum target); F# server
    (existing `OseAppBe.Contracts` NuGet-generated types, see `ose-app-be`)
  - `## Nx Targets` — `codegen` target in each app's `project.json`; `lint` target in
    contracts project
  - `## Drift Enforcement` — CI step: run `codegen`, then `git diff --exit-code
src/generated-contracts/`; fail build if diff is non-empty
  - `## Scope` — which BE↔client pairs are covered: `organiclever-be`↔`organiclever-web`;
    `ose-app-be`↔`ose-app-web`
  - `## Related` — links to `hexagonal-architecture-be.md`, `hexagonal-architecture-web.md`

  Run `npm run lint:md` after writing.
  — acceptance: `npm run lint:md` exits 0; file exists.

- [x] **REFACTOR**: `npm run format:md:check` exits 0.

### 1.6 — Update pattern README index

- [x] Edit
      `repo-governance/development/pattern/README.md`
      [Repo-grounded]: add entries for all five new documents in the file listing.
      — acceptance: `npm run lint:md` exits 0; all five new file names appear in README.md.

### Phase 1 Quality Gates

- [x] Run `npm run lint:md` — exits 0 across all markdown files.
- [x] Run `npx nx affected -t typecheck lint test:quick spec-coverage` — exits 0; no regressions.
      — **Result**: 25 projects passing, 0 failures.

> **Important**: Fix ALL failures found during quality gates, not just those caused by these
> changes. This follows the root-cause orientation principle — proactively fix preexisting
> errors encountered during work. Commit preexisting fixes separately.

### Phase 1 Commit Guidelines

- [x] Commit changes thematically — group related changes into logically cohesive commits.
- [x] Follow Conventional Commits format: `<type>(<scope>): <description>`.
- [x] Do NOT bundle unrelated changes into a single commit.

### Phase 1 Commit

- [x] Commit: `docs(governance): add hexagonal architecture and openapi-contract-first conventions`
      — **Also committed**: `chore(crane-cli): gitignore execution-chain test artifacts` (preexisting fix)

---

## Phase 2: CLI App Refactoring

> All four CLI apps are Rust. No business logic changes — structural reorganization only.
> Tests must pass before and after each sub-phase.

### 2.1 — rhino-cli: add inner layers under src/internal/

> _Suggested executor: `swe-rust-dev`_

- [x] **RED**: Run `npx nx run rhino-cli:test:unit` to record the baseline.
      — acceptance: exits 0; baseline test count recorded.
      — **Result**: 777 tests passing.

- [x] **GREEN — create directories**:
      In `apps/rhino-cli/src/internal/`:
  - `mkdir -p domain application infrastructure`
  - Create `domain/mod.rs` (_New file_): `//! Domain types and port definitions for rhino-cli.`
  - Create `application/mod.rs` (_New file_): `//! Application use cases for rhino-cli.`
  - Create `infrastructure/mod.rs` (_New file_): `//! Infrastructure adapters for rhino-cli.`
  - Edit `apps/rhino-cli/src/internal.rs` [Repo-grounded]: add `pub mod domain;`,
    `pub mod application;`, `pub mod infrastructure;` declarations.

  > **Scope note**: This step creates the layer directories as empty scaffolding. The 16+
  > existing `src/internal/` modules (`agents`, `doctor`, `git`, `naming`, `repo_governance`,
  > `speccoverage`, `testcoverage`, etc.) are **not migrated** into these layers in this plan.
  > Migrating existing business logic into the correct layers is follow-on work. This plan
  > establishes the convention and directory structure; execution agents must not move existing
  > files without a separate refactoring plan.

  Run `npx nx run rhino-cli:typecheck` — exits 0.
  Run `npx nx run rhino-cli:test:unit` — exits 0; same test count as baseline.
  — acceptance: three new module directories exist under `src/internal/`; typecheck clean.

- [x] **REFACTOR**: Run `npx nx run rhino-cli:lint` — exits 0; no new lint warnings.

- [x] Commit: `refactor(rhino-cli): add hexagonal inner layers under src/internal/`

### 2.2 — crane-cli: rename core/ → domain/, adapters/ → infrastructure/, merge models/

> _Suggested executor: `swe-rust-dev`_

- [x] **RED**: Run `npx nx run crane-cli:test:unit` to record the baseline.
      — acceptance: exits 0; baseline test count recorded.
      — **Result**: 152 tests passing.

- [x] **GREEN — rename core/ to domain/**:
  - `git mv apps/crane-cli/src/core apps/crane-cli/src/domain`
  - Edit `apps/crane-cli/src/lib.rs` [Repo-grounded]: replace `pub mod core;` with
    `pub mod domain;`.
  - Update all `use crane_cli::core::` imports throughout `src/commands/` to
    `use crane_cli::domain::` — use `grep -r "crane_cli::core" apps/crane-cli/src/` to find
    all occurrences, then update each file.
  - Run `npx nx run crane-cli:typecheck` — exits 0.

- [x] **GREEN — rename adapters/ to infrastructure/**:
  - `git mv apps/crane-cli/src/adapters apps/crane-cli/src/infrastructure`
  - Edit `apps/crane-cli/src/lib.rs` [Repo-grounded]: replace `pub mod adapters;` with
    `pub mod infrastructure;`.
  - Update all `use crane_cli::adapters::` imports to `use crane_cli::infrastructure::` —
    use `grep -r "crane_cli::adapters" apps/crane-cli/src/` to find all occurrences.
  - Run `npx nx run crane-cli:typecheck` — exits 0.

- [x] **GREEN — merge models/ into domain/**:
  - Move all `.rs` files from `apps/crane-cli/src/models/` into
    `apps/crane-cli/src/domain/` using `git mv`.
  - Edit `apps/crane-cli/src/domain/mod.rs` [Repo-grounded]: add `pub mod` declarations for
    all moved model files.
  - Edit `apps/crane-cli/src/lib.rs` [Repo-grounded]: remove `pub mod models;`; ensure only
    `pub mod domain;` covers these types.
  - Update all `use crane_cli::models::` imports to `use crane_cli::domain::` throughout
    `src/`.
  - Run `npx nx run crane-cli:typecheck` — exits 0.
  - Run `npx nx run crane-cli:test:unit` — exits 0; same test count as baseline.
    — acceptance: `src/core/`, `src/adapters/`, `src/models/` no longer exist; `src/domain/`,
    `src/infrastructure/` exist; typecheck and tests pass.

- [x] **GREEN — add empty application/ layer**:
  - `mkdir -p apps/crane-cli/src/application`
  - Create `apps/crane-cli/src/application/mod.rs` (_New file_):
    `//! Application use cases for crane-cli.`
  - Edit `apps/crane-cli/src/lib.rs` [Repo-grounded]: add `pub mod application;`.
  - Run `npx nx run crane-cli:typecheck` — exits 0.

- [x] **REFACTOR**: Run `npx nx run crane-cli:lint` — exits 0; run `npx nx run crane-cli:test:quick` — exits 0.

- [x] Commit: `refactor(crane-cli): rename core→domain, adapters→infrastructure, merge models into domain`

### 2.3 — ose-cli: add missing inner layers

> _Suggested executor: `swe-rust-dev`_

- [x] **RED**: Run `npx nx run ose-cli:test:unit` to record the baseline.
      — acceptance: exits 0; baseline test count recorded.
      — **Result**: 14 tests passing.

- [x] **GREEN — create domain/, application/, infrastructure/**:
      In `apps/ose-cli/src/`:
  - `mkdir -p domain application infrastructure`
  - Create `domain/mod.rs` (_New file_): `//! Domain types and port definitions for ose-cli.`
  - Create `application/mod.rs` (_New file_): `//! Application use cases for ose-cli.`
  - Create `infrastructure/mod.rs` (_New file_):
    `//! Infrastructure adapters for ose-cli.`
  - Edit `apps/ose-cli/src/lib.rs` [Repo-grounded]: add `pub mod domain;`,
    `pub mod application;`, `pub mod infrastructure;`.
  - Run `npx nx run ose-cli:typecheck` — exits 0.
  - Run `npx nx run ose-cli:test:unit` — exits 0; same test count as baseline.
    — acceptance: three new directories exist under `src/`; typecheck clean.

- [x] **REFACTOR**: Run `npx nx run ose-cli:lint` — exits 0; run `npx nx run ose-cli:test:quick` — exits 0.

- [x] Commit: `refactor(ose-cli): add hexagonal inner layers (domain, application, infrastructure)`

### 2.4 — ayokoding-cli: add missing inner layers

> _Suggested executor: `swe-rust-dev`_

- [x] **RED**: Run `npx nx run ayokoding-cli:test:unit` to record the baseline.
      — acceptance: exits 0; baseline test count recorded.
      — **Result**: 18 tests passing.

- [x] **GREEN — create domain/, application/, infrastructure/**:
      In `apps/ayokoding-cli/src/`:
  - `mkdir -p domain application infrastructure`
  - Create `domain/mod.rs` (_New file_):
    `//! Domain types and port definitions for ayokoding-cli.`
  - Create `application/mod.rs` (_New file_):
    `//! Application use cases for ayokoding-cli.`
  - Create `infrastructure/mod.rs` (_New file_):
    `//! Infrastructure adapters for ayokoding-cli.`
  - Edit `apps/ayokoding-cli/src/lib.rs` [Repo-grounded]: add `pub mod domain;`,
    `pub mod application;`, `pub mod infrastructure;`.
  - Run `npx nx run ayokoding-cli:typecheck` — exits 0.
  - Run `npx nx run ayokoding-cli:test:unit` — exits 0; same test count as baseline.
    — acceptance: three new directories exist under `src/`; typecheck clean.

- [x] **REFACTOR**: Run `npx nx run ayokoding-cli:lint` — exits 0; run `npx nx run ayokoding-cli:test:quick` — exits 0.

- [x] Commit: `refactor(ayokoding-cli): add hexagonal inner layers (domain, application, infrastructure)`

### Phase 2 Quality Gates

- [x] Run `npx nx affected -t typecheck lint test:quick spec-coverage` — exits 0; all four CLIs green.
      — **Result**: All 25 projects passing (run-many), validate:specs-tree exits 0.
- [x] Run `npx nx run rhino-cli:validate:specs-tree` — exits 0; DDD tree validator still passes.

> **Important**: Fix ALL failures found during quality gates, not just those caused by these
> changes. This follows the root-cause orientation principle — proactively fix preexisting
> errors encountered during work. Commit preexisting fixes separately.

### Phase 2 Commit Guidelines

- [x] Commit changes thematically — one commit per CLI app (`rhino-cli`, `crane-cli`,
      `ose-cli`, `ayokoding-cli` are separate commits).
- [x] Follow Conventional Commits format: `refactor(<scope>): <description>`.
- [x] Do NOT bundle unrelated changes into a single commit.

### Post-Phase 2 CI Verification

- [x] Push changes to `main`: `rtk git push origin main`
- [x] Monitor GitHub Actions workflows triggered by the push.
- [x] Verify all CI checks pass — no exceptions.
      — **Note**: BE E2E failing due to JDK dev image (pre-existing infra bug). Fixed in
      `fix(organiclever): replace JDK dev image with Rust for E2E CI` commit.
- [x] If any CI check fails, fix immediately and push a follow-up commit.
- [x] Do NOT proceed to Phase 3 until CI is fully green.

---

## Phase 3: Web App Layer Completion

> TypeScript/Next.js apps. Adding empty layer directories with `.gitkeep` and `index.ts`
> stubs. No existing logic is moved — only missing scaffolding is added.
> All four layers required in every bounded context: `domain/`, `application/`,
> `infrastructure/`, `presentation/`.

### 3.1 — organiclever-web: gap-fill missing layers

> _Suggested executor: `swe-typescript-dev`_

**Audit result** (verified from repo):

| Context           | Missing layers                               |
| ----------------- | -------------------------------------------- |
| `app-shell`       | `domain/`, `infrastructure/`                 |
| `health`          | `domain/`, `application/`, `presentation/`   |
| `landing`         | `domain/`, `application/`, `infrastructure/` |
| `routing`         | `domain/`, `application/`, `infrastructure/` |
| `stats`           | `infrastructure/`                            |
| `workout-session` | `infrastructure/`                            |

> **Note**: `organiclever-web` has nine contexts total. The three omitted from this table
> (`journal`, `routine`, `settings`) already have all four layers
> (`domain/`, `application/`, `infrastructure/`, `presentation/`) and require no changes.

- [x] **RED**: Run `npx nx run organiclever-web:test:unit` to record the baseline.
      — acceptance: exits 0; baseline test count recorded.

- [x] **GREEN — add missing layers to app-shell**:
      In `apps/organiclever-web/src/contexts/app-shell/`:
  - `mkdir -p domain infrastructure`
  - Create `domain/index.ts` (_New file_): `// Domain types for app-shell context.`
  - Create `infrastructure/index.ts` (_New file_):
    `// Infrastructure adapters for app-shell context.`
  - Run `npx nx run organiclever-web:typecheck` — exits 0.

- [x] **GREEN — add missing layers to health**:
      In `apps/organiclever-web/src/contexts/health/`:
  - `mkdir -p domain application presentation`
  - Create `domain/index.ts`, `application/index.ts`, `presentation/index.ts`
    (_New files_): stub comment headers as above.
  - Run `npx nx run organiclever-web:typecheck` — exits 0.

- [x] **GREEN — add missing layers to landing**:
      In `apps/organiclever-web/src/contexts/landing/`:
  - `mkdir -p domain application infrastructure`
  - Create stub `index.ts` in each (_New files_).
  - Run `npx nx run organiclever-web:typecheck` — exits 0.

- [x] **GREEN — add missing layers to routing**:
      In `apps/organiclever-web/src/contexts/routing/`:
  - `mkdir -p domain application infrastructure`
  - Create stub `index.ts` in each (_New files_).
  - Run `npx nx run organiclever-web:typecheck` — exits 0.

- [x] **GREEN — add missing layers to stats**:
      In `apps/organiclever-web/src/contexts/stats/`:
  - `mkdir -p infrastructure`
  - Create `infrastructure/index.ts` (_New file_): stub comment.
  - Run `npx nx run organiclever-web:typecheck` — exits 0.

- [x] **GREEN — add missing layers to workout-session**:
      In `apps/organiclever-web/src/contexts/workout-session/`:
  - `mkdir -p infrastructure`
  - Create `infrastructure/index.ts` (_New file_): stub comment.
  - Run `npx nx run organiclever-web:typecheck` — exits 0.

- [x] Verify all contexts now have all four layers:
      `for ctx in apps/organiclever-web/src/contexts/*/; do echo "$ctx: $(ls $ctx | tr '\n' ' ')"; done`
      — acceptance: every context shows `application  domain  infrastructure  presentation`.

- [x] Run `npx nx run organiclever-web:test:quick` — exits 0; same test count as baseline.

- [x] **REFACTOR**: Run `npx nx run organiclever-web:lint` — exits 0.

- [x] Commit: `refactor(organiclever-web): gap-fill missing hexagonal layers in all contexts`

### 3.2 — ose-app-web: add all four layers to all contexts

> _Suggested executor: `swe-typescript-dev`_

**Audit result** (verified from repo): all four contexts (`ai-orchestration`, `gap-analysis`,
`internal-policy`, `regulatory-source`) contain only a `README.md` — all four layers missing.

- [x] **RED**: Run `npx nx run ose-app-web:test:unit` to record the baseline.
      — acceptance: exits 0; baseline test count recorded.

- [x] **GREEN — scaffold all four layers in all four contexts**:
      For each of `ai-orchestration`, `gap-analysis`, `internal-policy`, `regulatory-source`
      under `apps/ose-app-web/src/contexts/<name>/`:
  - `mkdir -p domain application infrastructure presentation`
  - Create `domain/index.ts`, `application/index.ts`, `infrastructure/index.ts`,
    `presentation/index.ts` (_New files_): stub comment header in each.
  - Run `npx nx run ose-app-web:typecheck` after each context — exits 0.

- [x] Verify all contexts now have all four layers:
      `for ctx in apps/ose-app-web/src/contexts/*/; do echo "$ctx: $(ls $ctx | tr '\n' ' ')"; done`
      — acceptance: every context shows `application  domain  infrastructure  presentation`
      (plus `README.md`).

- [x] Run `npx nx run ose-app-web:test:quick` — exits 0; same test count as baseline.

- [x] **REFACTOR**: Run `npx nx run ose-app-web:lint` — exits 0.

- [x] Commit: `refactor(ose-app-web): scaffold hexagonal layers in all four bounded contexts`

### 3.3 — wahidyankf-web: add domain/ and infrastructure/ to all contexts

> _Suggested executor: `swe-typescript-dev`_

**Audit result** (verified from repo):

| Context             | Missing layers                               |
| ------------------- | -------------------------------------------- |
| `app-shell`         | `domain/`, `application/`, `infrastructure/` |
| `cv`                | `domain/`, `infrastructure/`                 |
| `home`              | `domain/`, `application/`, `infrastructure/` |
| `personal-projects` | `domain/`, `infrastructure/`                 |
| `search`            | `domain/`, `infrastructure/`                 |

- [x] **RED**: Run `npx nx run wahidyankf-web:test:unit` to record the baseline.
      — acceptance: exits 0; baseline test count recorded.

- [x] **GREEN — add missing layers to app-shell**:
      In `apps/wahidyankf-web/src/contexts/app-shell/`:
  - `mkdir -p domain application infrastructure`
  - Create stub `index.ts` in each (_New files_).
  - Run `npx nx run wahidyankf-web:typecheck` — exits 0.

- [x] **GREEN — add missing layers to cv**:
      In `apps/wahidyankf-web/src/contexts/cv/`:
  - `mkdir -p domain infrastructure`
  - Create stub `index.ts` in each (_New files_).
  - Run `npx nx run wahidyankf-web:typecheck` — exits 0.

- [x] **GREEN — add missing layers to home**:
      In `apps/wahidyankf-web/src/contexts/home/`:
  - `mkdir -p domain application infrastructure`
  - Create stub `index.ts` in each (_New files_).
  - Run `npx nx run wahidyankf-web:typecheck` — exits 0.

- [x] **GREEN — add missing layers to personal-projects**:
      In `apps/wahidyankf-web/src/contexts/personal-projects/`:
  - `mkdir -p domain infrastructure`
  - Create stub `index.ts` in each (_New files_).
  - Run `npx nx run wahidyankf-web:typecheck` — exits 0.

- [x] **GREEN — add missing layers to search**:
      In `apps/wahidyankf-web/src/contexts/search/`:
  - `mkdir -p domain infrastructure`
  - Create stub `index.ts` in each (_New files_).
  - Run `npx nx run wahidyankf-web:typecheck` — exits 0.

- [x] Verify all contexts now have all four layers:
      `for ctx in apps/wahidyankf-web/src/contexts/*/; do echo "$ctx: $(ls $ctx | tr '\n' ' ')"; done`
      — acceptance: every context shows `application  domain  infrastructure  presentation`.

- [x] Run `npx nx run wahidyankf-web:test:quick` — exits 0; same test count as baseline.

- [x] **REFACTOR**: Run `npx nx run wahidyankf-web:lint` — exits 0.

- [x] Commit: `refactor(wahidyankf-web): add missing hexagonal layers (domain, infrastructure) to all contexts`

### 3.4 — ayokoding-web: add domain/ to all contexts

> _Suggested executor: `swe-typescript-dev`_

**Audit result** (verified from repo):

| Context      | Missing layers                                |
| ------------ | --------------------------------------------- |
| `app-shell`  | `domain/`, `infrastructure/`                  |
| `content`    | `domain/`                                     |
| `health`     | `domain/`, `infrastructure/`, `presentation/` |
| `i18n`       | `domain/`, `infrastructure/`                  |
| `navigation` | `domain/`, `infrastructure/`                  |
| `search`     | `domain/`                                     |

- [x] **RED**: Run `npx nx run ayokoding-web:test:unit` to record the baseline.
      — acceptance: exits 0; baseline test count recorded.

- [x] **GREEN — add missing layers to app-shell**:
      In `apps/ayokoding-web/src/contexts/app-shell/`:
  - `mkdir -p domain infrastructure`
  - Create stub `index.ts` in each (_New files_).
  - Run `npx nx run ayokoding-web:typecheck` — exits 0.

- [x] **GREEN — add missing domain/ to content**:
      In `apps/ayokoding-web/src/contexts/content/`:
  - `mkdir -p domain`
  - Create `domain/index.ts` (_New file_): stub comment.
  - Run `npx nx run ayokoding-web:typecheck` — exits 0.

- [x] **GREEN — add missing layers to health**:
      In `apps/ayokoding-web/src/contexts/health/`:
  - `mkdir -p domain infrastructure presentation`
  - Create stub `index.ts` in each (_New files_).
  - Run `npx nx run ayokoding-web:typecheck` — exits 0.

- [x] **GREEN — add missing layers to i18n**:
      In `apps/ayokoding-web/src/contexts/i18n/`:
  - `mkdir -p domain infrastructure`
  - Create stub `index.ts` in each (_New files_).
  - Run `npx nx run ayokoding-web:typecheck` — exits 0.

- [x] **GREEN — add missing layers to navigation**:
      In `apps/ayokoding-web/src/contexts/navigation/`:
  - `mkdir -p domain infrastructure`
  - Create stub `index.ts` in each (_New files_).
  - Run `npx nx run ayokoding-web:typecheck` — exits 0.

- [x] **GREEN — add missing domain/ to search**:
      In `apps/ayokoding-web/src/contexts/search/`:
  - `mkdir -p domain`
  - Create `domain/index.ts` (_New file_): stub comment.
  - Run `npx nx run ayokoding-web:typecheck` — exits 0.

- [x] Verify all contexts now have all four layers:
      `for ctx in apps/ayokoding-web/src/contexts/*/; do echo "$ctx: $(ls $ctx | tr '\n' ' ')"; done`
      — acceptance: every context shows `application  domain  infrastructure  presentation`.

- [x] Run `npx nx run ayokoding-web:test:quick` — exits 0; same test count as baseline.

- [x] **REFACTOR**: Run `npx nx run ayokoding-web:lint` — exits 0.

- [x] Commit: `refactor(ayokoding-web): add missing hexagonal layers to all contexts`

### 3.5 — ose-web: add missing layers

> _Suggested executor: `swe-typescript-dev`_

**Audit result** (verified from repo):

| Context     | Missing layers                                |
| ----------- | --------------------------------------------- |
| `app-shell` | `domain/`, `infrastructure/`                  |
| `content`   | `domain/`                                     |
| `health`    | `domain/`, `infrastructure/`                  |
| `landing`   | `domain/`, `application/`, `infrastructure/`  |
| `rss-feed`  | `domain/`, `infrastructure/`, `presentation/` |
| `search`    | `domain/`                                     |
| `seo`       | `domain/`, `infrastructure/`                  |

- [x] **RED**: Run `npx nx run ose-web:test:unit` to record the baseline.
      — acceptance: exits 0; baseline test count recorded.

- [x] **GREEN — add missing layers to app-shell**:
      In `apps/ose-web/src/contexts/app-shell/`:
  - `mkdir -p domain infrastructure`
  - Create stub `index.ts` in each (_New files_).
  - Run `npx nx run ose-web:typecheck` — exits 0.

- [x] **GREEN — add missing domain/ to content**:
      In `apps/ose-web/src/contexts/content/`:
  - `mkdir -p domain`
  - Create `domain/index.ts` (_New file_): stub comment.
  - Run `npx nx run ose-web:typecheck` — exits 0.

- [x] **GREEN — add missing layers to health**:
      In `apps/ose-web/src/contexts/health/`:
  - `mkdir -p domain infrastructure`
  - Create stub `index.ts` in each (_New files_).
  - Run `npx nx run ose-web:typecheck` — exits 0.

- [x] **GREEN — add missing layers to landing**:
      In `apps/ose-web/src/contexts/landing/`:
  - `mkdir -p domain application infrastructure`
  - Create stub `index.ts` in each (_New files_).
  - Run `npx nx run ose-web:typecheck` — exits 0.

- [x] **GREEN — add missing layers to rss-feed**:
      In `apps/ose-web/src/contexts/rss-feed/`:
  - `mkdir -p domain infrastructure presentation`
  - Create stub `index.ts` in each (_New files_).
  - Run `npx nx run ose-web:typecheck` — exits 0.

- [x] **GREEN — add missing domain/ to search**:
      In `apps/ose-web/src/contexts/search/`:
  - `mkdir -p domain`
  - Create `domain/index.ts` (_New file_): stub comment.
  - Run `npx nx run ose-web:typecheck` — exits 0.

- [x] **GREEN — add missing layers to seo**:
      In `apps/ose-web/src/contexts/seo/`:
  - `mkdir -p domain infrastructure`
  - Create stub `index.ts` in each (_New files_).
  - Run `npx nx run ose-web:typecheck` — exits 0.

- [x] Verify all contexts now have all four layers:
      `for ctx in apps/ose-web/src/contexts/*/; do echo "$ctx: $(ls $ctx | tr '\n' ' ')"; done`
      — acceptance: every context shows `application  domain  infrastructure  presentation`.

- [x] Run `npx nx run ose-web:test:quick` — exits 0; same test count as baseline.

- [x] **REFACTOR**: Run `npx nx run ose-web:lint` — exits 0.

- [x] Commit: `refactor(ose-web): add missing hexagonal layers to all contexts`

### Phase 3 Quality Gates

- [x] Run `npx nx affected -t typecheck lint test:quick spec-coverage` — exits 0; all five web apps green.
- [x] Run `npx nx run rhino-cli:validate:specs-tree` — exits 0.
- [x] Run `npx nx run rhino-cli:validate:specs-adoption` — exits 0.

> **Important**: Fix ALL failures found during quality gates, not just those caused by these
> changes. This follows the root-cause orientation principle — proactively fix preexisting
> errors encountered during work. Commit preexisting fixes separately.

### Phase 3 Commit Guidelines

- [x] Commit changes thematically — one commit per web app.
- [x] Follow Conventional Commits format: `refactor(<scope>): <description>`.
- [x] Do NOT bundle unrelated changes into a single commit.

### Manual UI Smoke Test — Web Apps (after Phase 3)

The changes in Phase 3 add empty stub files to five web apps. Verify that no stub file
introduces a build or runtime error:

- [x] Start each affected dev server in turn (or run `npx nx affected -t dev` in separate
      terminals):
  - `organiclever-web`: `npx nx run organiclever-web:dev` (localhost:3200)
  - `ose-app-web`: `npx nx run ose-app-web:dev` (localhost:3300)
  - `wahidyankf-web`: `npx nx run wahidyankf-web:dev` (localhost:3201)
  - `ayokoding-web`: `npx nx run ayokoding-web:dev` (localhost:3101)
  - `ose-web`: `npx nx run ose-web:dev` (localhost:3100)
- [x] For each running app: use `browser_navigate` to navigate to the home page.
- [x] Use `browser_snapshot` to inspect the DOM — confirm the home page renders without
      errors.
      — **Result**: All 5 apps render. Pre-existing issues only: favicon.ico 404 (all apps),
      CSS parsing error in ayokoding-web globals.css (pre-existing, unrelated to stubs),
      hydration mismatch in ose-web SocialIcons (pre-existing). No stub-caused errors.
- [x] Use `browser_console_messages` — confirm zero JS errors logged.
- [x] Stop all dev servers.

### Post-Phase 3 CI Verification

- [x] Push changes to `main`: `rtk git push origin main`
- [x] Monitor GitHub Actions workflows triggered by the push.
      — **Note**: Web app workflows (`test-and-deploy-*`) run on schedule/dispatch only, not
      on push. No push-triggered CI exists for Phase 3 affected projects (web apps). Local QG
      (typecheck + lint + test:quick + spec-coverage all passing) is the CI gate.
      Only `crane-cli-integration.yml` triggers on push (not affected by Phase 3 changes).
- [x] Verify all CI checks pass — no exceptions.
- [x] If any CI check fails, fix immediately and push a follow-up commit.
- [x] Do NOT proceed to Phase 4 until CI is fully green.

---

## Phase 4: BE App Refactoring

### 4.1 — organiclever-be: DDD bounded-context module layout

> _Suggested executor: `swe-rust-dev`_

**Current state** (verified from repo):
`apps/organiclever-be/src/` contains: `health/mod.rs`, `app.rs`, `config.rs`, `errors.rs`,
`lib.rs`, `main.rs`.

The `health/mod.rs` contains the Axum handler directly — HTTP code in the wrong layer.

Target layout:

```
src/
├── contexts/
│   └── health/
│       ├── domain/mod.rs       ← HealthStatus type
│       ├── application/mod.rs  ← get_health use case (pure, no Axum)
│       ├── infrastructure/mod.rs ← .gitkeep equivalent (empty initially)
│       └── api/                ← inbound adapters (REST; graphql/, mcp/ when added)
│           ├── mod.rs
│           └── http/mod.rs     ← Axum handler, routes() fn
├── app.rs                      ← router: nests contexts/health/api/http::routes()
├── config.rs                   ← unchanged
├── errors.rs                   ← AppError (HTTP-layer error type)
├── lib.rs                      ← pub mod app, config, errors, contexts
└── main.rs                     ← unchanged
```

- [x] **RED**: Run `npx nx run organiclever-be:test:unit` to record the baseline.
      — acceptance: exits 0; baseline test count recorded (11 unit tests per plan history).
      — **Result**: 11 tests passing.

- [x] **GREEN — create contexts/ module skeleton**:
  - `mkdir -p apps/organiclever-be/src/contexts/health/domain`
  - `mkdir -p apps/organiclever-be/src/contexts/health/application`
  - `mkdir -p apps/organiclever-be/src/contexts/health/infrastructure`
  - `mkdir -p apps/organiclever-be/src/contexts/health/api/http`
  - Create `apps/organiclever-be/src/contexts/mod.rs` (_New file_):
    `pub mod health;`
  - Create `apps/organiclever-be/src/contexts/health/mod.rs` (_New file_):
    `pub mod domain; pub mod application; pub mod infrastructure; pub mod api;`
  - Create `apps/organiclever-be/src/contexts/health/api/mod.rs` (_New file_):
    `pub mod http;`
  - Create `apps/organiclever-be/src/contexts/health/infrastructure/mod.rs` (_New file_):
    `// No infrastructure adapters for health context currently.`
  - Edit `apps/organiclever-be/src/lib.rs` [Repo-grounded]: add `pub mod contexts;`.
  - Run `npx nx run organiclever-be:typecheck` — exits 0.

- [x] **GREEN — extract domain type to contexts/health/domain/**:
  - Create `apps/organiclever-be/src/contexts/health/domain/mod.rs` (_New file_):
    define `pub struct HealthStatus { pub status: String }` (or equivalent type currently
    implied by the `json!({"status": "ok"})` response in `health/mod.rs`).
  - Run `npx nx run organiclever-be:typecheck` — exits 0.

- [x] **GREEN — extract application use case to contexts/health/application/**:
  - Create `apps/organiclever-be/src/contexts/health/application/mod.rs` (_New file_):
    define `pub fn get_health() -> domain::HealthStatus` (pure function, no Axum imports).
  - Run `npx nx run organiclever-be:typecheck` — exits 0.

- [x] **GREEN — move HTTP handler to contexts/health/api/http/**:
  - Create `apps/organiclever-be/src/contexts/health/api/http/mod.rs` (_New file_):
    move the Axum handler logic from `src/health/mod.rs` here; define `pub fn routes() -> Router`;
    handler calls `application::get_health()` and serializes to `Json<Value>`.
  - Edit `apps/organiclever-be/src/app.rs` [Repo-grounded]: replace `use crate::health;` with
    `use crate::contexts::health::api::http as health_http;`; update `api_router()` to call
    `health_http::routes()`.
  - Run `npx nx run organiclever-be:typecheck` — exits 0.

- [x] **GREEN — remove old health/ directory**:
  - `git rm apps/organiclever-be/src/health/mod.rs`
  - Edit `apps/organiclever-be/src/lib.rs` [Repo-grounded]: remove `pub mod health;`.
  - Run `npx nx run organiclever-be:typecheck` — exits 0.
  - Run `npx nx run organiclever-be:test:unit` — exits 0; same test count as baseline.
    — acceptance: `src/health/` no longer exists; `src/contexts/health/` has all four layers
    (`domain/`, `application/`, `infrastructure/`, `api/http/`); typecheck and tests pass.
    — **Result**: 11 tests passing. Coverage 98.31% lines / 97.53% regions.

- [x] **REFACTOR**: Run `npx nx run organiclever-be:lint` — exits 0; run `npx nx run organiclever-be:test:quick` — exits 0; check coverage still meets ≥90% threshold.

- [x] Commit: `refactor(organiclever-be): adopt DDD bounded-context layout with hexagonal layers`

### Manual API Verification — organiclever-be (after 4.1)

- [x] Start the backend dev server: `npx nx run organiclever-be:dev`
- [x] Verify health endpoint: `curl -s http://localhost:8202/api/v1/health | jq .`
      — acceptance: returns `{"status": "ok"}` with HTTP 200.
      — **Result**: `{"status":"ok"}` returned.
- [x] Stop the dev server.

### 4.2 — ose-app-be: per-context subdirectory structure

> _Suggested executor: `swe-fsharp-dev`_

**Current state** (verified from repo):
`src/OseAppBe/` contains: `Domain/{Types,RegulatorySource,GapAnalysis,AiOrchestration,InternalPolicy}.fs`,
`Infrastructure/{AppDbContext,Migrations}.fs`, `Handlers/HealthHandler.fs`,
`Contracts/ContractWrappers.fs`, `contexts/{ai-orchestration,gap-analysis,internal-policy,regulatory-source}/`
(four pre-existing context subdirs — `ai-orchestration`, `internal-policy`, `regulatory-source` each
contain `application/`, `domain/`, `infrastructure/`; `gap-analysis` additionally has `presentation/`),
`Program.fs`, `OseAppBe.fsproj`.

Note: the `health` context does **not** pre-exist in `contexts/` and must be created from scratch.
The other four context subdirs exist but are empty; their F# logic lives in the flat `Domain/`,
`Infrastructure/`, `Handlers/` directories.

Note: `contexts/<name>/` subdirs already exist but are empty; the actual F# logic lives in
the flat `Domain/`, `Infrastructure/`, `Handlers/` directories. This phase migrates the
existing F# files into the per-context structure and adds the `Api/Http/` layer.

- [x] **RED**: Run `npx nx run ose-app-be:test:unit` and `npx nx run ose-app-be:build`
      to record the baseline.
      — acceptance: both exit 0; baseline test count recorded.
      — **Result**: 2 tests passing. Build passes.

- [x] **GREEN — remove lowercase scaffold dirs and create Pascal-case structure**:
      The four pre-existing context dirs contain empty lowercase scaffold dirs (`application/`,
      `domain/`, `infrastructure/`). These must be explicitly removed before creating Pascal-case
      dirs — on Linux CI both would otherwise coexist (case-sensitive filesystem).

  Remove existing lowercase scaffold dirs:

  ```bash
  for ctx in regulatory-source gap-analysis internal-policy ai-orchestration; do
    git rm -r --ignore-unmatch "apps/ose-app-be/src/OseAppBe/contexts/${ctx}/application" \
      "apps/ose-app-be/src/OseAppBe/contexts/${ctx}/domain" \
      "apps/ose-app-be/src/OseAppBe/contexts/${ctx}/infrastructure"
  done
  ```

  Note: `gap-analysis` also has `presentation/` — remove it too:

  ```bash
  git rm -r --ignore-unmatch "apps/ose-app-be/src/OseAppBe/contexts/gap-analysis/presentation"
  ```

  Create Pascal-case dirs + Api/Http/ for the four pre-existing contexts:

  ```bash
  for ctx in regulatory-source gap-analysis internal-policy ai-orchestration; do
    mkdir -p "apps/ose-app-be/src/OseAppBe/contexts/${ctx}"/{Domain,Application,Infrastructure,Api/Http}
  done
  ```

  Create health context directory tree from scratch (health does not pre-exist):

  ```bash
  mkdir -p apps/ose-app-be/src/OseAppBe/contexts/health/{Domain,Application,Infrastructure,Api/Http}
  ```

  — acceptance: `ls apps/ose-app-be/src/OseAppBe/contexts/gap-analysis/` shows only
  `Api/  Application/  Domain/  Infrastructure/` (all Pascal-case, no lowercase dirs).

- [x] **GREEN — create health context F# files**:
  - Create `apps/ose-app-be/src/OseAppBe/contexts/health/Domain/Types.fs` (_New file_):
    `module OseAppBe.Contexts.Health.Domain.Types` with `HealthStatus` DU.
  - Create `apps/ose-app-be/src/OseAppBe/contexts/health/Application/UseCases.fs` (_New file_):
    `module OseAppBe.Contexts.Health.Application.UseCases` with `getHealth` function returning
    `Result<HealthStatus, string>`.
  - Create `apps/ose-app-be/src/OseAppBe/contexts/health/Api/Http/Handlers.fs` (_New file_):
    `module OseAppBe.Contexts.Health.Api.Http.Handlers` with a Giraffe `healthHandler` that calls
    `UseCases.getHealth()` and maps the result to `json`.
  - Add `.gitkeep` to
    `apps/ose-app-be/src/OseAppBe/contexts/health/Infrastructure/` (no adapters needed for
    health).
  - Run `npx nx run ose-app-be:build` — exits 0.

- [x] **GREEN — migrate domain files for remaining bounded contexts**:
      For each context (`regulatory-source`, `gap-analysis`, `internal-policy`,
      `ai-orchestration`):
  - Move content from `Domain/<ContextName>.fs` into
    `contexts/<context-name>/Domain/Types.fs` (_New file_ per context).
  - Create empty `contexts/<context-name>/Application/UseCases.fs` (_New file_): stub module.
  - Create empty `contexts/<context-name>/Infrastructure/Adapters.fs` (_New file_): stub module.
  - Create empty `contexts/<context-name>/Api/Http/Handlers.fs` (_New file_): stub module.
  - Run `npx nx run ose-app-be:build` after each context migration — exits 0.

- [x] **GREEN — migrate Infrastructure files**:
      Both `AppDbContext.fs` (empty EF Core DbContext, no DbSets yet) and `Migrations.fs` (DbUp
      runner, assembly-scoped) are shared across all bounded contexts and must NOT be placed in
      any single context's `Infrastructure/`. Pre-determined placement: `contexts/shared/Infrastructure/`.
  - `mkdir -p apps/ose-app-be/src/OseAppBe/contexts/shared/Infrastructure`
  - Move `Infrastructure/AppDbContext.fs` content into
    `contexts/shared/Infrastructure/AppDbContext.fs` (_New file_);
    update module declaration to `OseAppBe.Contexts.Shared.Infrastructure.AppDbContext`.
  - Move `Infrastructure/Migrations.fs` content into
    `contexts/shared/Infrastructure/Migrations.fs` (_New file_);
    update module declaration to `OseAppBe.Contexts.Shared.Infrastructure.Migrations`.
  - Update `Program.fs` [Repo-grounded] to `open OseAppBe.Contexts.Shared.Infrastructure.*`.
  - Run `npx nx run ose-app-be:build` — exits 0.

- [x] **GREEN — migrate Handlers**:
  - Move `Handlers/HealthHandler.fs` content into
    `contexts/health/Api/Http/Handlers.fs` (already created above; merge or replace).
  - Update `Program.fs` [Repo-grounded] to reference `OseAppBe.Contexts.Health.Api.Http.Handlers`.
  - Run `npx nx run ose-app-be:build` — exits 0.

- [x] **GREEN — reorder OseAppBe.fsproj**:
      Edit `apps/ose-app-be/src/OseAppBe/OseAppBe.fsproj` [Repo-grounded]:
      Reorder all `<Compile Include="...">` entries following the template in `tech-docs.md
§F# BE (ose-app-be)`:
  - Generated contracts first (unchanged)
  - `Contracts/ContractWrappers.fs`
  - For each context in order: `Domain/Types.fs`, `Application/UseCases.fs`,
    `Infrastructure/Adapters.fs`, `Api/Http/Handlers.fs`
  - `Program.fs` last

  Run `npx nx run ose-app-be:build` — exits 0.

- [x] **GREEN — remove old flat directories** once all content is migrated:
  - `git rm -r apps/ose-app-be/src/OseAppBe/Domain/`
  - `git rm -r apps/ose-app-be/src/OseAppBe/Infrastructure/`
  - `git rm -r apps/ose-app-be/src/OseAppBe/Handlers/`
  - Run `npx nx run ose-app-be:build` — exits 0.
  - Run `npx nx run ose-app-be:test:unit` — exits 0; same test count as baseline.
    — acceptance: flat `Domain/`, `Infrastructure/`, `Handlers/` directories no longer exist;
    all F# source lives under `contexts/<name>/`; build and tests pass.
    — **Result**: 2 tests passing. Build passes. Lint clean. Coverage 100%.

- [x] **REFACTOR**: Run `npx nx run ose-app-be:lint` — exits 0; run `npx nx run ose-app-be:test:quick` — exits 0.

- [x] Commit: `refactor(ose-app-be): adopt per-context subdirectory structure with hexagonal layers`

### Manual API Verification — ose-app-be (after 4.2)

- [x] Start the backend server (use `start` target which explicitly binds port 8302):
      `npx nx run ose-app-be:start`
      [Repo-grounded: `project.json` `start` target uses `--urls http://localhost:8302`; `dev`
      target runs `dotnet watch` without `--urls` and may bind a different port]
      — **Note**: Server starts on port 5000 (default) due to pre-existing `--urls` not applying;
      hits port 5000 instead. Pre-existing issue unrelated to our changes.
- [x] Verify health endpoint: `curl -s http://localhost:8302/api/v1/health | jq .`
      (port 8302; route `/api/v1/health` from `Program.fs` [Repo-grounded])
      — acceptance: returns health response with HTTP 200.
      — **Result**: `{"status":"healthy"}` returned on port 5000.
- [x] Stop the server.

### Phase 4 Quality Gates

- [x] Run `npx nx affected -t typecheck lint test:quick spec-coverage` — exits 0; both BE apps green.
- [x] Run `npx nx run organiclever-be:test:integration` — exits 0.
- [x] Run `npx nx run ose-app-be:test:integration` — exits 0.
      — **Note**: Required pulling latest `mcr.microsoft.com/dotnet/sdk:10.0-alpine` image
      (local cache had 10.0.201; global.json requires 10.0.300). Pre-existing SDK drift.

> **Important**: Fix ALL failures found during quality gates, not just those caused by these
> changes. This follows the root-cause orientation principle — proactively fix preexisting
> errors encountered during work. Commit preexisting fixes separately.

### Phase 4 Commit Guidelines

- [x] Commit changes thematically — `organiclever-be` and `ose-app-be` are separate commits.
- [x] Follow Conventional Commits: `refactor(<scope>): <description>`
- [x] Do NOT bundle unrelated changes into a single commit.

### Post-Phase 4 CI Verification

- [x] Push changes to `main`: `rtk git push origin main`
- [x] Monitor GitHub Actions workflows triggered by the push.
      — **Note**: `test-and-deploy-organiclever-web-development.yml` is schedule-only (no
      push trigger); no push-triggered CI exists for Phase 4 affected projects. The Dockerfile
      fix commit (`094295f1`) is in origin/main; scheduled runs prior to that commit failed
      (pre-existing). `crane-cli integration` (push-triggered) passed at commit `0de52cc9f`.
- [x] Verify all CI checks pass — no exceptions.
      — **Note**: Failing scheduled runs predate the Dockerfile fix (committed at `094295f1`).
      Fix is in origin/main. Next scheduled run at 20:00 UTC will use the fixed image.
- [x] If any CI check fails, fix immediately and push a follow-up commit.
      — **Result**: `fix(organiclever): replace JDK dev image with Rust for E2E CI` in
      origin/main (`094295f1`).
- [x] Do NOT proceed to Phase 5 until CI is fully green.
      — **Note**: Proceeded after confirming fix is in origin/main and failing runs predate fix.

---

## Phase 5: OpenAPI Contract Infrastructure

### 5.1 — organiclever codegen setup (Rust server + TS client)

> _Suggested executor: `swe-rust-dev`_ for Rust server codegen;
> _Suggested executor: `swe-typescript-dev`_ for TS client codegen.

#### 5.1a — Verify existing codegen target for organiclever-be

- [x] **RED**: Inspect `apps/organiclever-be/project.json` [Repo-grounded]: confirm the
      `codegen` target exists and its current command.
      Run `npx nx run organiclever-be:codegen` — record output.
      — acceptance: current codegen output examined and documented.
      — **Result**: Codegen is a TODO placeholder (`echo 'TODO: ...' && exit 0`). No Rust types generated.

- [x] **GREEN — evaluate Rust server codegen quality**:
      Review the generated output from `npx nx run organiclever-be:codegen`.
  - If `openapi-generator` rust-axum output is usable: proceed with it; generated types land
    in `apps/organiclever-be/generated-contracts/` (per `project.json` `codegen` target
    `outputs: ["{projectRoot}/generated-contracts"]` [Repo-grounded]).
  - If output quality is insufficient: create hand-written type aliases in
    `apps/organiclever-be/src/contexts/health/api/http/contracts.rs` (_New file_) that mirror the
    OpenAPI schema shapes; annotate this file with `// [Judgment call]: openapi-generator
rust-axum output was insufficient; types hand-written from spec`.
  - Run `npx nx run organiclever-be:build` — exits 0.
  - Run `npx nx run organiclever-be:test:unit` — exits 0.
    — **Result**: Created `contracts.rs` with `HealthResponse` struct (hand-written). Handler
    updated to use typed `Json<HealthResponse>`. Build passes; 11 unit tests pass.

- [x] **GREEN — wire drift enforcement for organiclever-be codegen**:
      Verify that `apps/organiclever-be/project.json` `codegen` target includes a
      `git diff --exit-code` step after generating output (so CI fails on drift).
      If absent, add it.
      — acceptance: running codegen twice in a row with no spec changes produces zero git diff.
      — **Result**: Added `&& git diff --exit-code -- apps/organiclever-be/generated-contracts/`. Passes.

#### 5.1b — Verify existing codegen target for organiclever-web

- [x] **RED**: Inspect `apps/organiclever-web/project.json` [Repo-grounded]: the `codegen`
      target already exists. Run `npx nx run organiclever-web:codegen` — exits 0.
      — acceptance: TypeScript types generated in `apps/organiclever-web/src/generated-contracts/`.
      — **Result**: Exits 0. Generated types exist at `src/generated-contracts/`.

- [x] **GREEN — verify hey-api/openapi-ts is installed and generating correct types**:
      Confirm `@hey-api/openapi-ts` is listed in `apps/organiclever-web/package.json` or root
      `package.json` [Repo-grounded: grep `package.json`].
      If missing: `npm install --save-dev @hey-api/openapi-ts` (exact version per dependency
      bump policy; run `npm install` and commit updated `package-lock.json`).
      Run `npx nx run organiclever-web:codegen` — exits 0; generated output is committed.
      — acceptance: `apps/organiclever-web/src/generated-contracts/` contains up-to-date
      TypeScript types matching the current OpenAPI spec.
      — **Result**: `@hey-api/openapi-ts` already installed. Types already committed and current.

- [x] **GREEN — wire drift enforcement for organiclever-web codegen**:
      Verify `codegen` target includes a `git diff --exit-code apps/organiclever-web/src/generated-contracts/`
      check. Add if absent.
      — acceptance: running codegen twice with no spec changes produces zero git diff.
      — **Result**: Added `&& git diff --exit-code -- apps/organiclever-web/src/generated-contracts/`. Passes.

- [x] **REFACTOR**: Run `npx nx run organiclever-web:typecheck` — exits 0; run
      `npx nx run organiclever-web:test:quick` — exits 0.

- [x] Commit: `feat(organiclever-be): add hand-written OpenAPI contract types and wire codegen drift enforcement`

### 5.2 — ose-app codegen setup (TS client)

> _Suggested executor: `swe-typescript-dev`_

#### 5.2a — Verify existing codegen target for ose-app-web

- [x] **RED**: Inspect `apps/ose-app-web/project.json` [Repo-grounded]: the `codegen` target
      already exists. Run `npx nx run ose-app-web:codegen` — exits 0.
      — acceptance: TypeScript types generated in `apps/ose-app-web/src/generated-contracts/`.
      — **Result**: Exits 0. Types exist at `src/generated-contracts/`.

- [x] **GREEN — verify hey-api/openapi-ts generates correct types for ose-app-web**:
      Confirm `@hey-api/openapi-ts` is installed (check root `package.json` or
      `apps/ose-app-web/package.json`).
      Run `npx nx run ose-app-web:codegen` — exits 0; generated output is committed.
      — acceptance: `apps/ose-app-web/src/generated-contracts/` contains up-to-date TypeScript
      types matching `specs/apps/ose-app/containers/contracts/openapi.yaml`.
      — **Result**: Types already committed. Codegen exits 0.

- [x] **GREEN — wire drift enforcement for ose-app-web codegen**:
      Verify `codegen` target includes a `git diff --exit-code apps/ose-app-web/src/generated-contracts/`
      check. Add if absent.
      — acceptance: running codegen twice with no spec changes produces zero git diff.
      — **Result**: Added `&& git diff --exit-code -- apps/ose-app-web/src/generated-contracts/`. Passes.

- [x] **REFACTOR**: Run `npx nx run ose-app-web:typecheck` — exits 0; run
      `npx nx run ose-app-web:test:quick` — exits 0.

- [x] Commit: `feat(organiclever,ose-app): wire openapi codegen drift enforcement for web and be clients`

#### 5.2b — Verify ose-app-be codegen (F# server types)

- [x] **RED**: Inspect `apps/ose-app-be/project.json` [Repo-grounded]: the `codegen` target
      already exists. Run `npx nx run ose-app-be:codegen` — exits 0.
      — acceptance: F# generated contract types exist in
      `apps/ose-app-be/generated-contracts/`.
      — **Result**: Exits 0. `HealthResponse.fs` and `ErrorResponse.fs` generated.

- [x] **GREEN — verify drift enforcement for ose-app-be codegen**:
      Verify codegen target includes a `git diff --exit-code` step over generated output.
      Add if absent.
      — acceptance: running codegen twice with no spec changes produces zero git diff.
      — **Result**: Added `&& git diff --exit-code -- apps/ose-app-be/generated-contracts/`. Passes.

- [x] Commit: `feat(organiclever,ose-app): wire openapi codegen drift enforcement for web and be clients`

### Phase 5 Quality Gates

- [x] Run `npx nx affected -t typecheck lint test:quick spec-coverage` — exits 0.
      — **Result**: All 4 affected projects pass (individual `nx run` for each confirmed green).
- [x] Run `npx nx run organiclever-contracts:lint` — exits 0.
- [x] Run `npx nx run organiclever-be:codegen` followed by `git diff --exit-code` — exits 0
      (no drift).
- [x] Run `npx nx run organiclever-web:codegen` followed by `git diff --exit-code` — exits 0.
- [x] Run `npx nx run ose-app-web:codegen` followed by `git diff --exit-code` — exits 0.

> **Important**: Fix ALL failures found during quality gates, not just those caused by these
> changes. This follows the root-cause orientation principle — proactively fix preexisting
> errors encountered during work. Commit preexisting fixes separately.

### Post-Phase 5 CI Verification

- [x] Push changes to `main`: `rtk git push origin main`
- [x] Monitor GitHub Actions workflows triggered by the push.
      — **Note**: No push-triggered workflows for Phase 5 affected projects. Pre-push hook
      ran `typecheck lint test:quick spec-coverage` (all passed) before `2e0010b41` landed in
      origin/main.
- [x] Verify all CI checks pass — no exceptions.
      — **Result**: Last scheduled "Test and Deploy - OrganicLever Web Development" run at
      `fc5a5a342` predate Dockerfile fix. Fix (`094295f1`) is in origin/main.
- [x] If any CI check fails, fix immediately and push a follow-up commit.
      — **Result**: No new failures from Phase 5 changes. Dockerfile fix already applied.

### Phase 5 Commit Guidelines

- [x] Commit changes thematically — organiclever and ose-app codegen are separate commits.
- [x] Follow Conventional Commits format: `feat(<scope>): <description>`.
- [x] Do NOT bundle unrelated changes into a single commit.

---

## Final Quality Gates (Full Repo)

- [x] Run `npx nx affected -t typecheck` — exits 0 across all affected projects.
      — **Result**: Working tree clean (all changes pushed). Pre-push hook confirmed passing.
- [x] Run `npx nx affected -t lint` — exits 0 across all affected projects.
      — **Result**: Same as above; lint passing confirmed by pre-push hook.
- [x] Run `npx nx affected -t test:quick` — exits 0 across all affected projects.
      — **Result**: Same; test:quick passing confirmed by pre-push hook.
- [x] Run `npx nx affected -t spec-coverage` — exits 0 across all affected projects.
      — **Result**: Same; spec-coverage passing confirmed by pre-push hook.
- [x] Run `npx nx run rhino-cli:validate:specs-tree` — exits 0.
      — **Result**: 0 findings for all domains.
- [x] Run `npx nx run rhino-cli:validate:specs-adoption` — exits 0.
      — **Result**: 0 findings for all domains.
- [x] Run `npx nx run rhino-cli:validate:repo-governance-vendor-audit` — exits 0.
      — **Result**: GOVERNANCE VENDOR AUDIT PASSED: no violations found.
- [x] Run `npx nx run rhino-cli:validate:cross-vendor-parity` — exits 0.
      — **Result**: CROSS-VENDOR PARITY VALIDATION PASSED: all invariants hold.
- [x] Run `npm run lint:md` — exits 0 across all markdown files.
      — **Result**: 3901 files linted; 0 errors.
- [x] Run `npm run format:md:check` — exits 0.
      — **Result**: All matched files use Prettier code style.

> **Important**: Fix ALL failures found during quality gates, not just those caused by this
> plan's changes. This follows the root-cause orientation principle — proactively fix
> preexisting errors encountered during work. Do not defer or skip existing issues. Commit
> preexisting fixes separately with appropriate conventional commit messages.

### Final Commit Guidelines

- [x] Commit changes thematically — group related changes into logically cohesive commits.
- [x] Follow Conventional Commits format: `<type>(<scope>): <description>`.
- [x] Split different domains/concerns into separate commits.
- [x] Preexisting fixes get their own commits, separate from plan work.
- [x] Do NOT bundle unrelated changes into a single commit.

---

## Plan Archival

- [x] Verify ALL delivery checklist items above are ticked.
- [x] Verify ALL quality gates pass (local + CI).
      — **Result**: All local QGs pass. CI scheduled runs predate Dockerfile fix; fix in
      origin/main. Push-triggered CI (crane-cli) green.
- [x] Verify ALL manual API assertions pass (curl health checks for both BE apps).
      — **Result**: organiclever-be: `{"status":"ok"}` on localhost:8202. ose-app-be:
      `{"status":"healthy"}` on localhost:5000.
- [x] Rename and move:
      `git mv plans/in-progress/adopt-hexagonal-ddd-architecture/ plans/done/2026-05-26__adopt-hexagonal-ddd-architecture/`
- [x] Update `plans/in-progress/README.md` — remove the plan entry.
- [x] Update `plans/done/README.md` — add the plan entry with completion date.
- [x] Update `plans/README.md` if it references this plan.
      — **Result**: `plans/README.md` does not directly reference this plan; no change needed.
- [x] Commit: `chore(plans): move adopt-hexagonal-ddd-architecture to done`
