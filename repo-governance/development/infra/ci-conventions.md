---
title: CI/CD Conventions
description: Central reference for CI/CD conventions in the multi-language Nx monorepo, covering git hooks, testing standards, Docker patterns, GitHub Actions structure, and naming rules
category: explanation
subcategory: development
tags:
  - ci-cd
  - git-hooks
  - github-actions
  - docker
  - testing
  - nx
  - coverage
created: 2026-03-31
---

# CI/CD Conventions

Central reference for CI/CD conventions across the multi-language Nx monorepo. This document defines
the standards that apply to all apps regardless of language or framework: git hook behaviour, test
level definitions, coverage thresholds, Docker patterns, GitHub Actions structure, and naming rules.

## Principles Implemented/Respected

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**:
  Every hook step, target name, workflow file, and Docker layer is explicitly documented. No
  implicit behaviour is tolerated — if something runs in CI, it is declared in a workflow file; if
  something runs in a hook, it is declared in the hook script.

- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**:
  Pre-commit, commit-msg, and pre-push hooks enforce quality automatically on every developer
  machine. Reusable workflows and composite actions keep CI logic DRY, so adding a new app variant
  requires only a thin per-variant file calling shared logic.

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**:
  Three hook stages, three test levels, one canonical naming scheme. Per-variant test workflows are
  kept to ~40 lines each by delegating to reusable workflows.

## Conventions Implemented/Respected

- **[File Naming Convention](../../conventions/structure/file-naming.md)**: Workflow files,
  composite action directories, infra directories, and specs directories all follow the naming
  patterns defined in this convention.

- **[Nx Target Standards](./nx-targets.md)**: The targets referenced in this document
  (`test:unit`, `test:integration`, `test:e2e`, `test:quick`, `lint`, `typecheck`) use the
  canonical names and caching rules defined in `nx-targets.md`.

- **[Three-Level Testing Standard](../quality/three-level-testing-standard.md)**: Test level
  definitions (unit, integration, E2E) and the isolation rules enforced here derive from the
  authoritative three-level testing standard.

- **[No Secrets in Git Convention](../../conventions/security/no-secrets-in-committed-files.md)**: The
  no-hardcoded-secrets rule for CI workflows is one enforcement point of the broader hard iron rule
  that no system secret may ever be committed to any git-tracked file.

## Git Hooks Standard

All developer machines run three Husky hooks. Hook logic is implemented via `rhino-cli` subcommands
to keep the raw hook files thin and testable.

### pre-commit

The pre-commit hook delegates entirely to `rhino-cli git pre-commit`, which executes these steps in
order:

| Step | Action                                                                                         | Failure Mode                |
| ---- | ---------------------------------------------------------------------------------------------- | --------------------------- |
| 1    | Validate `.claude/` and `.opencode/` config (YAML, tools, model, skills, semantic equivalence) | Blocks commit               |
| 2    | Validate `docker-compose` files found in staged changes                                        | Blocks commit               |
| 3    | Run `nx affected run-pre-commit` (format checks, lightweight per-project hooks)                | Warn only — does not block  |
| 4    | Stage `ayokoding-www` content files (auto-generated link data)                                 | N/A (staging step)          |
| 5    | Run lint-staged (format all staged files by language)                                          | Blocks commit               |
| 6    | Sync app `package-lock.json` files                                                             | Blocks commit if sync fails |
| 7    | Validate docs file naming convention across staged files                                       | Blocks commit               |
| 8    | Validate markdown links in staged files                                                        | Blocks commit               |
| 9    | Lint all markdown files (`markdownlint-cli2`)                                                  | Blocks commit               |

**Lint-staged language formatters (step 5)**:

| Language / File Type                              | Formatter       |
| ------------------------------------------------- | --------------- |
| JavaScript, TypeScript, JSON, YAML, CSS, Markdown | Prettier        |
| Rust                                              | `rustfmt`       |
| F# / C#                                           | `dotnet format` |

### commit-msg

The commit-msg hook runs `commitlint` to enforce the [Conventional Commits](https://www.conventionalcommits.org/) format.

**Required format**: `<type>(<scope>): <description>`

Valid types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`, `revert`.

The scope is optional but recommended. The description must use imperative mood and must not end
with a period.

### pre-push

The pre-push hook runs two commands in sequence:

```bash
nx affected -t typecheck lint test:quick specs:coverage --parallel=cores-1
npm run lint:md
```

`nx affected` computes which projects changed since the merge base and runs only those projects.
`--parallel=cores-1` reserves one core for system responsiveness. `lint:md` runs
`markdownlint-cli2` over all markdown files as a final gate. `specs:coverage` validates that every
Gherkin step has a matching step definition and is compulsory for all apps and E2E runners.

If the pre-push hook times out, warm the Nx cache first:

```bash
npx nx affected -t typecheck lint test:quick specs:coverage
```

Then push again — the cached results make the second run fast.

After the baseline gate, the hook conditionally runs the naming validators when the push range
touches the relevant trees:

- `nx run rhino-cli:naming:harness-validation` — fires when `.claude/agents/**` or `.opencode/agents/**` changed
- `nx run rhino-cli:naming:workflows-validation` — fires when `repo-governance/workflows/**` changed

Both are cacheable, so no-op pushes pay near-zero cost. The CI quality-gate workflow also runs
both targets unconditionally on every PR against `main` to catch drift from hand-edited files
that bypassed the local hook.

## Nx Target Naming and Caching Rules

This document uses the canonical target names defined in [Nx Target Standards](./nx-targets.md).
Refer to that document for:

- The full required target set per project type
- Caching rules per target (`cache: true` / `cache: false`)
- Input declarations required for correct cache invalidation
- The four-dimension tag scheme for `project.json`

Key targets referenced throughout this document:

| Target             | Summary                                                         |
| ------------------ | --------------------------------------------------------------- |
| `test:quick`       | Fast pre-push gate: `test:unit` + coverage validation           |
| `test:unit`        | Isolated unit tests, all dependencies mocked, coverage measured |
| `test:integration` | Real infrastructure, no HTTP layer, not cacheable               |
| `test:e2e`         | Full stack via Playwright, not cacheable                        |
| `lint`             | Static analysis                                                 |
| `typecheck`        | Type verification without producing artifacts                   |

## Three-Level Testing Definitions

The three levels apply universally across all project types. The isolation boundary at each level
is fixed — only the step implementation details change per language and framework.

| Level                                | Dependencies                | HTTP Layer                     | Coverage      | Nx Cache       |
| ------------------------------------ | --------------------------- | ------------------------------ | ------------- | -------------- |
| **Unit** (`test:unit`)               | All mocked                  | None — call functions directly | Measured here | `cache: true`  |
| **Integration** (`test:integration`) | Real infra (DB, filesystem) | None — no HTTP dispatch        | Not measured  | `cache: false` |
| **E2E** (`test:e2e`)                 | All real                    | Real HTTP via Playwright       | Not measured  | `cache: false` |

For the full definition including architecture diagrams, Docker infrastructure requirements, and
per-backend implementation patterns, see the
[Three-Level Testing Standard](../quality/three-level-testing-standard.md).

## App-Type-Specific Test Manifestations

Each app type implements the three levels according to its domain. The table below shows how each
app type realises each level.

| App Type                                          | Unit (`test:unit`)                                    | Integration (`test:integration`)                                              | E2E (`test:e2e`)                                     |
| ------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------------------------------- | ---------------------------------------------------- |
| **BE API** (`organiclever-be`)                    | BDD, mocked repos, calls service fns directly         | Real PostgreSQL via docker-compose, calls service fns directly (no HTTP)      | Playwright, real HTTP + real PostgreSQL              |
| **FE** (`organiclever-app-web`)                   | Vitest, all API calls mocked (MSW / mock services)    | MSW with real DOM; in-process mocking only                                    | Playwright against running FE + BE                   |
| **CLI** (`*-cli`)                                 | `cargo test`, all I/O mocked via dependency injection | `cargo test` with real filesystem via tmp fixtures, real HTTP via mock server | Not applicable                                       |
| **Content platform** (`ayokoding-www`, `ose-www`) | Vitest, components and tRPC routes mocked             | MSW, in-process mocking                                                       | Playwright BE E2E (`*-be-e2e`) + FE E2E (`*-fe-e2e`) |
| **Library** (`rust-commons`)                      | `cargo test`, mock closures                           | `cargo test` with real filesystem fixtures, cacheable                         | Not applicable                                       |
| **E2E runner** (`*-e2e`)                          | Not applicable                                        | Not applicable                                                                | Playwright — this project IS the E2E suite           |

## Gherkin Consumption Matrix

All testable projects must consume Gherkin specifications at every applicable test level. E2E
runner projects ARE the Gherkin consumers at the E2E level.

| App Type                    | Unit consumes Gherkin                                                  | Integration consumes Gherkin | E2E consumes Gherkin                 |
| --------------------------- | ---------------------------------------------------------------------- | ---------------------------- | ------------------------------------ |
| BE API (`organiclever-be`)  | Yes — `specs/apps/organiclever/behavior/organiclever-be/gherkin/`      | Yes — same specs             | Yes — same specs                     |
| FE (`organiclever-app-web`) | Yes — `specs/apps/organiclever/behavior/organiclever-app-web/gherkin/` | Yes — same specs             | Yes — via `organiclever-app-web-e2e` |
| CLI (`*-cli`)               | Yes — `specs/apps/{domain}/behavior/<product>-cli/gherkin/`            | Yes — same specs             | Not applicable                       |
| Content platform            | Yes — project-local specs                                              | Yes — same specs             | Yes — via `*-be-e2e` / `*-fe-e2e`    |
| Library                     | Yes — library-specific specs                                           | Yes — same specs             | Not applicable                       |
| E2E runner                  | Not applicable                                                         | Not applicable               | Yes — consumes shared specs          |

## Coverage Threshold Rationale

Coverage thresholds are enforced by the native `test:coverage` Nx target as part of `test:quick`.
Thresholds differ by project type to reflect the realistic upper bound achievable through mocked
unit tests.

| Threshold | App Types                                                | Rationale                                                                                                                                                                       |
| --------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **90%**   | BE API backends (`organiclever-be`), CLI apps, Rust libs | Core business logic with high mock isolation. Service functions operate on pure data structures; 90% is achievable without heroic effort.                                       |
| **80%**   | Content platforms (`ayokoding-www`, `ose-www`)           | Significant UI rendering code and Next.js route handlers that are harder to unit-test. Some RSC rendering paths are excluded by design.                                         |
| **70%**   | FE apps (`organiclever-app-web`)                         | API, auth, and query layers are mocked by design; the mock boundaries limit what can be covered by unit tests. Lower threshold reflects this intentional architecture decision. |

Coverage is measured via the appropriate reporter for each language and converted to LCOV or
JaCoCo XML. Coverage enforcement runs inside each project's native `test:coverage` Nx target. See
`CLAUDE.md` for the exact command per language.

## Docker Conventions

### Dockerfile Template

All production Dockerfiles follow a multi-stage pattern:

```dockerfile
# syntax=docker/dockerfile:1

# ── Stage 1: dependency manifest layer ──────────────────────────────────────
# Copy only manifest files first so this layer is cached across code changes.
FROM base-image AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

# ── Stage 2: build ──────────────────────────────────────────────────────────
FROM deps AS builder
COPY . .
RUN npm run build

# ── Stage 3: production runtime ─────────────────────────────────────────────
FROM base-image AS runner
WORKDIR /app

# OCI standard image labels
LABEL org.opencontainers.image.source="https://github.com/open-sharia-enterprise/open-sharia-enterprise"
LABEL org.opencontainers.image.description="App description"

# Run as non-root user
RUN addgroup --system --gid 1001 appgroup \
  && adduser --system --uid 1001 appuser
COPY --from=builder --chown=appuser:appgroup /app/dist ./dist
USER appuser

EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1

CMD ["node", "dist/main.js"]
```

**Key requirements**:

- **Multi-stage**: Separate dependency installation, build, and runtime stages.
- **Dependency-manifest-first layer ordering**: Copy `package.json` / lock file before source
  code so Docker layer cache survives code-only changes.
- **Non-root user**: All containers run as a non-root system user.
- **HEALTHCHECK with `wget`**: Use `wget` for health checks — never `curl`. Many minimal base
  images (Alpine, distroless) include `wget` but not `curl`.
- **OCI LABEL**: Every production image must carry `org.opencontainers.image.source` and
  `org.opencontainers.image.description` labels.

### Docker Compose Patterns

Three docker-compose file roles exist per app:

| Role            | Path                                        | Purpose                                                               |
| --------------- | ------------------------------------------- | --------------------------------------------------------------------- |
| **Dev**         | `infra/dev/{app}/docker-compose.yml`        | Local development services (databases, message queues, etc.)          |
| **Integration** | `apps/{app}/docker-compose.integration.yml` | Real infrastructure for `test:integration` (PostgreSQL + test runner) |
| **CI overlay**  | `infra/dev/{app}/docker-compose.ci.yml`     | Overrides for CI environment (no volume mounts, deterministic ports)  |

All compose files must pass `docker compose config` without errors before merging. The CI overlay
is applied with `-f docker-compose.yml -f docker-compose.ci.yml` to keep dev and CI configs DRY.

### `.dockerignore` Pattern

Use broad exclusions with narrow inclusions rather than enumerating every excluded path:

```dockerignore
# Exclude everything by default
**

# Include only what the build needs
!apps/{app-name}/
!libs/
!package.json
!package-lock.json
!nx.json
!tsconfig*.json
```

Broad exclusion prevents accidentally including large directories (e.g., `node_modules`, `.git`,
`generated-reports`) that would bloat the build context and slow transfers.

## GitHub Actions Conventions

### File Organisation

| Artifact                     | Path pattern                                                | Concrete examples (after-state)                                                                                                                                              |
| ---------------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Composite action             | `.github/actions/{name}/action.yml`                         | `setup-dotnet`, `setup-node`, `setup-rust`                                                                                                                                   |
| Reusable workflow            | `.github/workflows/_reusable-{purpose}.yml`                 | `_reusable-www-test-local-deploy.yml`, `_reusable-app-test-local-deploy-stag.yml`, `_reusable-app-test-stag.yml`, `_reusable-be-build-deploy.yml`                            |
| www deploy workflow          | `.github/workflows/{domain}-www-test-local-deploy-prod.yml` | `ose-www-test-local-deploy-prod.yml`, `ayokoding-www-test-local-deploy-prod.yml`, `organiclever-www-test-local-deploy-prod.yml`, `wahidyankf-www-test-local-deploy-prod.yml` |
| App staging workflow         | `.github/workflows/{domain}-app-test-local-deploy-stag.yml` | `organiclever-app-test-local-deploy-stag.yml`, `ose-app-test-local-deploy-stag.yml`                                                                                          |
| App staging-gate workflow    | `.github/workflows/{domain}-app-test-stag.yml`              | `organiclever-app-test-stag.yml`, `ose-app-test-stag.yml`                                                                                                                    |
| Backend build+deploy         | `.github/workflows/{domain}-be-build-deploy-stag.yml`       | `organiclever-be-build-deploy-stag.yml`, `ose-be-build-deploy-stag.yml`                                                                                                      |
| Cross-cutting quality gate   | `.github/workflows/pr-quality-gate.yml`                     | `pr-quality-gate.yml` (replaces `pr-quality-gate.yml`)                                                                                                                       |
| Cross-cutting env validation | `.github/workflows/validate-env.yml`                        | `validate-env.yml` (replaces `commons-env-validate.yml`)                                                                                                                     |

The 16-workflow after-state consists of 4 reusables, 4 www workflows, 2 app local-deploy-stag, 2
app test-stag-deploy-prod, 2 be-build-deploy-stag, and 2 cross-cutting workflows. The stale files
`pr-quality-gate.yml`, `commons-env-validate.yml`, `validate-markdown.yml`,
`test-and-deploy-*.yml`, `test-*-web-staging.yml`, `deploy-*-to-production.yml`,
`publish-images.yml`, and `test-crane-cli-integration.yml` are removed by this plan. Markdown
validation is folded into lint-staged (per-file validators) and the `md-links` job in
`pr-quality-gate.yml` — no standalone `markdown-validate.yml` workflow.

The underscore prefix on reusable workflows (`_reusable-*.yml`) visually separates shared
infrastructure from top-level entry-point workflows in the GitHub Actions UI.

### Composite Actions

Each language or tool that requires non-trivial setup lives in its own composite action under
`.github/actions/{name}/action.yml`. A composite action encapsulates:

- Tool version pinning (via Volta, `setup-dotnet`, etc.)
- Dependency caching configuration
- Any post-setup verification steps

When adding a new language to the monorepo, create a corresponding composite action before wiring
the language into any workflow.

**Examples**:

```
.github/actions/setup-dotnet/action.yml
.github/actions/setup-node/action.yml
.github/actions/setup-rust/action.yml
```

### Reusable Workflows

Reusable workflows live in `.github/workflows/_reusable-{purpose}.yml` and are called via
`workflow_call`. They contain the actual job definitions (checkout, setup, test execution, artifact
upload). Per-variant test workflows stay thin (~40 lines) by calling these reusable workflows with
variant-specific inputs.

**Examples**:

```
.github/workflows/_reusable-www-test-local-deploy.yml
.github/workflows/_reusable-app-test-local-deploy-stag.yml
.github/workflows/_reusable-app-test-stag.yml
.github/workflows/_reusable-be-build-deploy.yml
```

### CRON Schedule

Scheduled service workflows run twice daily aligned to WIB (UTC+7). The app tier uses a
**staggered** schedule — `*-app-test-local-deploy-stag` fires first to produce the staging deploy,
then `*-app-test-stag` fires **2.5 hours later** once Vercel and coralpolyp have
settled. The www tier is independent and runs after both app-tier passes.

`*-be-build-deploy-stag` is **not** scheduled — it fires on push to the `stag-*-be` branch, which
the `*-app-test-local-deploy-stag` deploy job force-pushes on success.

| Pipeline                       | WIB           | UTC           | Rationale                                                           |
| ------------------------------ | ------------- | ------------- | ------------------------------------------------------------------- |
| `*-app-test-local-deploy-stag` | 03:00 / 15:00 | 20:00 / 08:00 | Earliest — produces the staging deploy the later stag-gate verifies |
| `*-app-test-stag`              | 05:30 / 17:30 | 22:30 / 10:30 | **+2.5 h** after staging, so Vercel + coralpolyp have rolled out    |
| `*-www-test-local-deploy-prod` | 06:00 / 18:00 | 23:00 / 11:00 | Independent of the app tier (direct www test → prod deploy)         |

### 5-Track Parallel CRON

Each scheduled test run executes five parallel tracks:

| Track | Nx Target / Command             | Notes                                                                               |
| ----- | ------------------------------- | ----------------------------------------------------------------------------------- |
| 1     | `lint`                          | Static analysis across all affected projects (includes static a11y for UI projects) |
| 2     | `typecheck`                     | Type verification                                                                   |
| 3     | `test:quick`                    | Unit tests + coverage validation                                                    |
| 4     | `specs:coverage`                | Validates Gherkin step coverage for all apps and E2E runners                        |
| 5     | `test:integration` → `test:e2e` | Sequential: integration then E2E per service                                        |

Tracks 1–4 run in parallel. Track 5 sequences integration before E2E within each service but
services themselves run in parallel across matrix entries.

## Naming Conventions

Workflow filenames follow the domain-first `{domain}-{action-chain}` grammar. The `{action-chain}`
encodes ordered execution phases left-to-right (e.g., `test-local-deploy-stag`). See
[GitHub Actions Workflow Naming Convention](./github-actions-workflow-naming.md) for the complete
grammar, allowed tokens, and the rule that the workflow `name:` field must mirror the filename.

| Entity                    | Pattern                                                                                   | Example                                                     |
| ------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Backend app               | `{domain}-be` or `{domain}-be-{lang}-{framework}`                                         | `organiclever-be`                                           |
| Frontend app              | `{domain}-app-web`                                                                        | `organiclever-app-web`                                      |
| www site app              | `{domain}-www`                                                                            | `organiclever-www`                                          |
| Infra dev directory       | `infra/dev/{app-name}/`                                                                   | `infra/dev/organiclever-be/`                                |
| Specs directory           | See [Specs Directory Structure](../../conventions/structure/specs-directory-structure.md) | `specs/apps/organiclever/behavior/organiclever-be/gherkin/` |
| Reusable workflow         | `_reusable-{purpose}.yml`                                                                 | `_reusable-app-test-local-deploy-stag.yml`                  |
| www deploy workflow       | `{domain}-www-test-local-deploy-prod.yml`                                                 | `organiclever-www-test-local-deploy-prod.yml`               |
| App staging workflow      | `{domain}-app-test-local-deploy-stag.yml`                                                 | `organiclever-app-test-local-deploy-stag.yml`               |
| App staging-gate workflow | `{domain}-app-test-stag.yml`                                                              | `organiclever-app-test-stag.yml`                            |
| BE build+deploy workflow  | `{domain}-be-build-deploy-stag.yml`                                                       | `organiclever-be-build-deploy-stag.yml`                     |
| Cross-cutting workflow    | `{group}-{action-chain}.yml`                                                              | `pr-quality-gate.yml`, `validate-env.yml`                   |
| Composite action          | `.github/actions/{name}/action.yml`                                                       | `.github/actions/setup-rust/action.yml`                     |

## Adding a New App to CI

Follow this checklist in order when adding a new app variant to the monorepo.

1. Create the app in `apps/{name}/` with a `project.json` that declares all mandatory Nx targets
   for its project type (see [Nx Target Standards](./nx-targets.md) for the required target set).
2. Add Nx tags to `project.json` using the four-dimension scheme: `type:`, `platform:`, `lang:`,
   `domain:`.
3. Create `infra/dev/{name}/` containing `docker-compose.yml`, `docker-compose.ci.yml`, and
   `.env.example`.
4. Write Dockerfiles (`Dockerfile` for production, `Dockerfile.integration` if the integration
   tests run in a container).
5. Create the specs directory following the
   [Specs Directory Structure Convention](../../conventions/structure/specs-directory-structure.md)
   and add at least one `.feature` file.
6. Wire Gherkin consumption in unit tests using the appropriate BDD runner for the language (godog,
   Cucumber, SpecFlow, etc.).
7. Create a per-variant test workflow at `.github/workflows/test-{name}.yml` calling the
   appropriate reusable workflow(s).
8. If the app uses a new language, create a composite action at
   `.github/actions/setup-{lang}/action.yml` before wiring it into any workflow.
9. Add language detection to the PR quality gate workflow so `nx affected` picks up the new
   project type.
10. Update the coverage section of `CLAUDE.md` with the new app's threshold and validate command.

## E2E Test Pairing Rule

Each app pairs with dedicated E2E runner projects for end-to-end testing.

| App Type                                           | E2E Pairing                                    |
| -------------------------------------------------- | ---------------------------------------------- |
| Backend (`organiclever-be`, `ayokoding-www`, etc.) | Dedicated `*-be-e2e` Playwright runner project |
| Frontend (`organiclever-app-web`, etc.)            | Dedicated `*-fe-e2e` Playwright runner project |
| Content platforms                                  | Both `*-be-e2e` and `*-fe-e2e` runners         |

Each product app has its own dedicated E2E runner (`*-be-e2e`, `*-fe-e2e`) scoped to that product's
scenarios.

## Environment Variable Standard

Every app with runtime configuration must satisfy these requirements:

- **`.env.example` in `infra/dev/{app}/`**: Documents all required and optional environment
  variables with placeholder values and inline comments explaining each variable.
- **`env_file` directive in docker-compose**: Compose services load environment variables via
  `env_file: .env` rather than hardcoding values in the `environment:` block.
- **`.env*.local` in `.gitignore`**: Local override files (`.env.local`, `.env.development.local`,
  etc.) must never be committed. The root `.gitignore` must include `**/.env*.local`.
- **No hardcoded secrets in CI workflows**: GitHub Actions workflows must reference secrets via
  `${{ secrets.SECRET_NAME }}`. Plain-text credentials must never appear in workflow YAML files,
  even in non-production environments. This is one enforcement point of the broader
  [No Secrets in Git Convention](../../conventions/security/no-secrets-in-committed-files.md), which is the
  hard iron rule governing all git-tracked files in this repository.

When a new variable is added to an app, the developer must update `.env.example` in the same
commit. CI will fail if the app starts without the variable, surfacing the omission early.

## CI/toolchain Parity Checklist

Seven workstream invariants define the converged toolchain across all repositories. Any deviation
must be recorded here with a justification; undocumented deviations are always bugs.

### Invariant A — CI Workflow Shape

| Requirement                                                                                                                                                | Enforced by                                                         |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| All `checkout` steps use `actions/checkout@v6`                                                                                                             | `actionlint` + PR quality gate                                      |
| Workflow filenames follow the `{domain}-{action-chain}.yml` grammar (see [GitHub Actions Workflow Naming Convention](./github-actions-workflow-naming.md)) | `actionlint` syntax check; code review                              |
| Non-TypeScript projects use `nx affected` (not `run-many`) in PR gate                                                                                      | `pr-quality-gate.yml` structure                                     |
| Per-variant test workflows call reusable workflows (thin callers, ≤40 lines each)                                                                          | Code review; reusable workflow structure                            |
| All entry-point workflows carry a `concurrency` block: `${{ github.workflow }}-${{ github.ref }}`                                                          | `actionlint`; PR quality gate                                       |
| CI lint jobs named after the tool they run: `shellcheck`, `hadolint`, `actionlint`                                                                         | `pr-quality-gate.yml` job keys                                      |
| Specs-gate job runs `specs:structure-validation` and `specs:gherkin-cardinality-validation` (spec-file links covered by `links:validation` gate)           | `pr-quality-gate.yml` specs-gate job                                |
| Full quality gate runs on every PR event (`opened`/`synchronize`/`reopened`) **and** on every push to `main`                                               | `pr-quality-gate.yml` `on.push` trigger                             |
| App-tier scheduled workflows use staggered 2× WIB cadence: `*-app-test-local-deploy-stag` at 03:00/15:00, `*-app-test-stag` at 05:30/17:30 (+2.5 h)        | `*-app-test-local-deploy-stag.yml` and `*-app-test-stag-*.yml` CRON |
| www-tier scheduled workflows run at 06:00/18:00 WIB (23:00/11:00 UTC)                                                                                      | `*-www-test-local-deploy-prod.yml` CRON expressions                 |

Note: `rhino-cli:naming:workflows-validation` validates `repo-governance/workflows/*.md` naming
only — it does **not** validate `.github/workflows/` filenames.

### Invariant B — Git Hook Lifecycle

Three Husky hooks, each with a fixed shape:

| Hook         | Required steps (in order)                                                                                                                                           |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `commit-msg` | `commitlint --edit "$1"` — enforces Conventional Commits format                                                                                                     |
| `pre-commit` | `npx nx run rhino-cli:env:validation` → `rhino-cli git pre-commit` (validate configs, format staged, validate links, lint markdown, shellcheck/hadolint/actionlint) |
| `pre-push`   | `npx nx affected -t typecheck lint test:quick specs:coverage --parallel=<cores-1>` → `npm run lint:md` → conditional naming validators (harness + workflows)        |

Conditional pre-push naming validators:

- `nx run rhino-cli:naming:harness-validation` — fires when `.claude/agents/**` or `.opencode/agents/**` changed
- `nx run rhino-cli:naming:workflows-validation` — fires when `repo-governance/workflows/**` changed

### Invariant B2 — No Heavy Tests in Fast Gates

`test:integration` and `test:e2e` are heavy (docker-compose, Playwright, real services). They run
**only** in the scheduled tiered pipelines and must never appear on the fast feedback path. See
tech-docs §"Fast-gate test policy" for the rationale and the current compliance state.

| Surface                           | Runs                                                            | `test:integration` / `test:e2e`? |
| --------------------------------- | --------------------------------------------------------------- | -------------------------------- |
| `.husky/pre-commit`               | `nx affected -t test:quick`                                     | **never**                        |
| `.husky/pre-push`                 | `typecheck`, `lint`, `test:quick`, `specs:coverage`             | **never**                        |
| `pr-quality-gate` (PR gate)       | `typecheck`, `lint`, `test:quick`, `specs:coverage` + lint jobs | **never**                        |
| `*-test-local-*` (CRON scheduled) | `test:integration` + `test:e2e` via docker-compose              | **yes**                          |
| `*-test-stag-*` (CRON scheduled)  | `test:e2e` against deployed staging                             | **yes**                          |

Any workflow that wires `test:integration` or `test:e2e` into a `pull_request` or `push` trigger
(rather than a `schedule` trigger) violates this invariant and must be corrected or removed before
merging. The deletion of `test-crane-cli-integration.yml` (which ran `crane-cli:test:integration`
on `pull_request`) was the remediation action that eliminated the last known violation.

### Invariant C — rhino-cli Hexagonal Architecture

Source tree layout:

| Layer                     | Path                  | Constraint                                      |
| ------------------------- | --------------------- | ----------------------------------------------- |
| Domain (pure)             | `src/domain/`         | No I/O; no `std::fs`, no HTTP, no env reads     |
| Application (use cases)   | `src/application/`    | Calls domain; injects infrastructure via trait  |
| Infrastructure (adapters) | `src/infrastructure/` | All I/O lives here (filesystem, network, env)   |
| CLI (inbound adapter)     | `src/commands/`       | Parses CLI args; delegates to application layer |

No file in `src/domain/` may import from `src/infrastructure/`. Violations fail `clippy`.

### Invariant D — rhino-cli Command Surface (Union Superset)

All callers (pre-push hook, CI workflows, `package.json` scripts) must use the canonical command
form `rhino {group} {verb} [{noun}]`. The `validate:*` prefix used before P10 is abolished.

Deprecated prefix→canonical mapping reference:

| Old (abolished)                            | Canonical                            |
| ------------------------------------------ | ------------------------------------ |
| `validate:env`                             | `env:validation`                     |
| `validate:links`                           | `links:validation`                   |
| `validate:mermaid`                         | `mermaid:validation`                 |
| `validate:heading-hierarchy`               | `headings:hierarchy-validation`      |
| `validate:specs-tree`                      | `specs:tree-validation`              |
| `validate:specs-counts`                    | `specs:counts-validation`            |
| `validate:specs-adoption`                  | `specs:adoption-validation`          |
| `validate:naming-agents`                   | `naming:harness-validation`          |
| `validate:naming-workflows`                | `naming:workflows-validation`        |
| `validate:repo-governance-vendor-audit`    | `governance:vendor-audit-validation` |
| `validate:cross-vendor-parity`             | `cross-vendor:parity-validation`     |
| `validate:harness-bindings` (package.json) | `harness:bindings-validation`        |

### Invariant E — Nx Target Naming (`{domain}:{work}`)

Governance, validation, lint, and format targets use the `{domain}:{work}` scheme.
`spec-coverage` is renamed `specs:coverage` repo-wide.

Rust-specific renames applied to all Rust `project.json` files:

| Old name     | New name             |
| ------------ | -------------------- |
| `fmt:check`  | `format:check`       |
| `check:msrv` | `compat:min-version` |
| `deny:check` | `deps:audit`         |

The full naming rationale and complete target catalog are documented in
[Nx Target Standards](./nx-targets.md).

### Invariant F — Governance Documentation Currency

All documentation in `repo-governance/` must reflect the converged toolchain. After any P10-class
rename or command-surface change, update:

1. `repo-governance/development/infra/ci-conventions.md` (this file) — pre-push section + checklist
2. `repo-governance/development/infra/nx-targets.md` — target name tables + `{domain}:{work}` naming section
3. `AGENTS.md` — Cross-Language Lint Gates section + rhino-cli command surface
4. `apps/rhino-cli/README.md` — command surface table + hexagonal layout diagram
5. Any index READMEs that reference renamed targets

Stale `validate:*` or `spec-coverage` references in any of the above are bugs caught by
`rhino-cli:links:validation` fragment checks and by the Parity Checklist gate in the plan delivery
process.

### Invariant G — Mermaid State Diagram Validation

`stateDiagram-v2` and `stateDiagram` (v1) diagrams are subject to the same width and label rules
as flowchart diagrams:

- **Width**: State node count contributes to the diagram width calculation. Diagrams exceeding
  the width limit must be split or redesigned.
- **Label length**: State display names and transition edge labels are limited to 30 characters.
  Use abbreviations or split composite states when labels exceed this limit.

Both rules are enforced by `rhino-cli:mermaid:validation`, which scans the entire repo (excluding
`plans/done/`, `apps/ayokoding-www/content/`, and the standard noise-skip set).

### Affected-First PR-Gate Principle

The PR quality gate runs `nx affected` for all per-project checks so only changed projects pay
the cost of typecheck, lint, test, and coverage on each PR. Whole-repo checks that cannot be
scoped to affected projects are an explicit exception and must be justified.

| Check                       | Target / Command                               | Why whole-repo                                                           |
| --------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------ |
| Markdown linting            | `npm run lint:md`                              | Links reference cross-project paths; partial scans miss broken links     |
| Mermaid validation          | `rhino-cli:mermaid:validation`                 | Width rules apply across all `.md` files; a fix in one breaks another    |
| Link validation             | `rhino-cli:links:validation`                   | Cross-project and external links must resolve globally                   |
| Heading hierarchy           | `rhino-cli:headings:hierarchy-validation`      | Cross-file anchor references cannot be validated in isolation            |
| Harness naming              | `rhino-cli:naming:harness-validation`          | Agent catalog is a global registry; partial scan misses naming conflicts |
| Workflow naming             | `rhino-cli:naming:workflows-validation`        | Workflow registry is global                                              |
| Governance vendor audit     | `rhino-cli:governance:vendor-audit-validation` | Scans `repo-governance/` globally for vendor-specific content leakage    |
| Cross-vendor parity         | `rhino-cli:cross-vendor:parity-validation`     | All three harness binding trees are compared; scoping breaks the diff    |
| Harness bindings validation | `npm run harness:bindings-validation`          | Binding parity is a whole-repo property; partial sync leaves gaps        |
| Env validation              | `rhino-cli:env:validation`                     | All `.env.example` files checked against a global schema                 |

Any new whole-repo check added to CI or pre-push must be listed here with its justification before
it lands.
