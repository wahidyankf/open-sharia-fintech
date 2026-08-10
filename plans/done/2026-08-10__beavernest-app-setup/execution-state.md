# Execution State — BeaverNest App Setup

## Phase 1

### Task Status

- In progress: prepare the verified governance-only change set for its isolated delivery branch.

### Files Changed

- `plans/in-progress/beaver-nest-app-setup/execution-state.md` — created — durable Phase 1 execution-state record.
- `repo-governance/development/quality/three-level-testing-standard.md` — modified — require each backend's configured production database.
- `repo-governance/development/infra/bdd-spec-test-mapping.md` — modified — generalize database-backed BDD integration mapping.
- `repo-governance/development/infra/ci-conventions.md` — modified — make CI database guidance app-selected.
- `repo-governance/development/infra/nx-targets.md` — modified — make integration target database-neutral.
- `repo-governance/development/README.md` — modified — index the generalized rule.
- `repo-governance/development/quality/README.md` — modified — index the generalized testing standard.
- `docs/how-to/add-new-app.md` — modified — require a new app's configured production database.
- `repo-governance/development/pattern/database-audit-trail.md` — modified — establish direct parameterized SQL as a valid F# manifestation.
- `plans/in-progress/beaver-nest-app-setup/evidence/phase-0-dependency-adoption.md` — created — retain sanitized local scratch-probe dependency evidence.

- `apps/beaver-nest-fe/src/theme.test.ts` — created — RED/GREEN/REFACTOR coverage for system theme
  bootstrap, listener lifecycle, and Vite HMR cleanup.
- `apps/beaver-nest-fe/src/theme.ts` — created — external idempotent system-theme bootstrap.
- `apps/beaver-nest-fe/src/lib/readiness-client.ts` — created — same-origin readiness request boundary.
- `apps/beaver-nest-fe/src/lib/readiness-state.ts` — created — immutable closed readiness state reducer.
- `apps/beaver-nest-fe/src/components/ReadinessPanel.tsx` — created — accessible loading, ready, and
  unavailable rendering with in-place retry.
- `apps/beaver-nest-fe/src/App.tsx` — modified — render the neutral foundation-status workspace from
  shared UI components.
- `apps/beaver-nest-fe/src/test/msw/{handlers,server}.ts` — created — centralized generated-contract
  readiness fixtures and node-request lifecycle.
- `apps/beaver-nest-fe/src/test/readiness.integration.test.tsx` — created — integration coverage for
  loading, ready, unavailable, and in-place retry behavior.
- `apps/beaver-nest-fe/vitest.integration.config.ts` — created — non-cacheable integration-test Vite
  configuration.
- `infra/dev/beaver-nest-app/tests/frontend-integration-target.sh` — created — verifies the real,
  non-cacheable frontend integration target contract.
- `apps/beaver-nest-fe/oxlint.json` — modified — remove Next-specific lint configuration.
- `apps/beaver-nest-fe/vite.config.ts` — modified — proxy only `/api` to the local development backend.
- `apps/beaver-nest-fe/{Dockerfile,.dockerignore}` — modified — replace the obsolete Next container
  assumptions pending the Phase 5 combined runtime image.
- `apps/beaver-nest-fe/.env.example` — modified — remove the obsolete cross-origin frontend API base
  variable; the client now uses same-origin requests only.
- `specs/apps/beaver-nest/behavior/beaver-nest-fe/gherkin/{workspace/browser-readiness,workspace/readiness-loading,network/readiness-recovery,workspace/no-promotional-cta}.feature` — created — replace the retired hello landing behavior with workspace readiness scenarios.
- `specs/apps/beaver-nest/behavior/beaver-nest-fe/gherkin/{hello/landing-page.feature,README.md}` — deleted/modified — remove obsolete greeting/CTA behavior references.
- `apps/beaver-nest-fe/src/test/workspace.steps.ts` — created — literal shared-step registry for the workspace feature set.

### Commands and Results

- Phase 0 baseline and gate — passed with the existing Homebrew .NET runtime exported as `DOTNET_ROOT` for Fantomas.
- Phase 1 targeted Prettier, markdownlint, diff check, and audit-trail terminology scan — passed.
- Phase 1 affected quality gates, repository markdown lint, harness-sync validation, and instruction-size validation — passed; no affected Nx project target was selected for governance-only changes.
- Independent Phase 1 documentation review — five findings corrected and targeted format/lint/quality gates re-run successfully.
- Unit 1 PR review cycle 1 — two medium documentation findings corrected in `ac7043409`; required CI completed successfully.
- Unit 1 PR review cycle 2 — two medium and two low documentation findings corrected in `160bac644`; required CI completed successfully.
- Unit 1 PR review cycle 3 — one medium and one low documentation finding corrected; follow-up validation is pending the fix commit.

### Evidence

- `plans/in-progress/beaver-nest-app-setup/evidence/phase-0-dependency-adoption.md` — sanitized local scratch-probe evidence; no host-specific value retained.

## Phase 2

### Task Status

- Complete: additive SQLite, migration, recovery, listener, and environment-contract foundation is
  implemented and verified before readiness delivery.

### Files Changed

- `plans/in-progress/beaver-nest-app-setup/evidence/phase-2-dependency-adoption.md` — created — dependency policy decision record.
- `plans/in-progress/beaver-nest-app-setup/tech-docs.md` — modified — record Phase 2 package clearances.
- `docs/reference/security-waivers.md` — modified — retain the required Path C native SQLite override.
- `apps/beaver-nest-be/.env.example` — modified — declare value-free listener and SQLite contract keys.
- `apps/beaver-nest-be/Dockerfile` — modified — remove obsolete listener variable and set container-only defaults.
- `apps/beaver-nest-be/project.json` — modified — add explicit local listener, environment input, SQL cache inputs, and transitive dependency audit.
- `apps/beaver-nest-be/src/BeaverNestBe/BeaverNestBe.fsproj` — modified — exact-pinned approved persistence dependencies and migration resource registration.
- `apps/beaver-nest-be/src/BeaverNestBe/Domain/HttpConfiguration.fs` — created — pure listener configuration validation.
- `apps/beaver-nest-be/src/BeaverNestBe/Domain/DatabaseConfiguration.fs` — created — canonical durable SQLite directory validation.
- `apps/beaver-nest-be/src/BeaverNestBe/Infrastructure/Migrations.fs` — created — pre-listen DbUp migration orchestration.
- `apps/beaver-nest-be/src/BeaverNestBe/Infrastructure/Sqlite/Connection.fs` — created — SQLite settings and connection boundary.
- `apps/beaver-nest-be/src/BeaverNestBe/Infrastructure/Sqlite/Errors.fs` — created — sanitized provider error classification.
- `apps/beaver-nest-be/src/BeaverNestBe/Migrations/001-initialize.sql` — created — embedded initialization migration.
- `apps/beaver-nest-be/src/BeaverNestBe/Operations/Database.fs` — created — validated SQLite backup and restore commands.
- `apps/beaver-nest-be/src/BeaverNestBe/Program.fs` — modified — command dispatch and migration-before-listen composition.
- `apps/beaver-nest-be/tests/integration/BeaverNestBe.IntegrationTests.fsproj` — modified — register persistence integration tests.
- `apps/beaver-nest-be/tests/integration/SqliteMigrationTests.fs` — created — real migration/restart/failure coverage.
- `apps/beaver-nest-be/tests/integration/SqliteSettingsTests.fs` — created — real SQLite pragma and contention coverage.
- `apps/beaver-nest-be/tests/unit/BeaverNestBe.UnitTests.fsproj` — modified — register additive behavior bindings and tests.
- `apps/beaver-nest-be/tests/unit/Steps/PersistenceSteps.fs` — created — literal persistence feature bindings.
- `apps/beaver-nest-be/tests/unit/Steps/RecoverySteps.fs` — created — literal recovery feature bindings.
- `apps/beaver-nest-be/tests/unit/Tests/DatabaseConfigurationTests.fs` — created — database directory validation coverage.
- `apps/beaver-nest-be/tests/unit/Tests/DatabaseOperationsTests.fs` — created — backup-name validation coverage.
- `apps/beaver-nest-be/tests/unit/Tests/HttpConfigurationTests.fs` — created — listener configuration coverage.
- `apps/beaver-nest-be/tests/unit/Tests/SqliteInfrastructureTests.fs` — created — SQLite connection, migration-state, and sanitized provider-error coverage.
- `apps/rhino-cli/project.json` — modified — clear hook-provided Git context before Rhino fixture tests create isolated repositories.
- `apps/beaver-nest-be/README.md` — modified — document additive local database operations.
- `repo-config.yml` — modified — declare backend environment ownership and injection homes.
- `infra/dev/beaver-nest-app/docker-compose.ci.yml` — modified — supply only explicit disposable CI database/listener values.
- `infra/dev/beaver-nest-app/README.md` — modified — document CI environment ownership.
- `infra/dev/beaver-nest-app/tests/env-contract.sh` — created — assert backend environment contract ownership.
- `apps/rhino-cli/src/application/env/validate.rs` — modified — recognize literal F# environment wrappers and exempt only the .NET runtime-owned container signal.
- `apps/rhino-cli/tests/env.rs` — modified — cover wrapper discovery and the narrow runtime-signal exclusion.
- `specs/apps/rhino/behavior/rhino-cli/gherkin/env/env-validate-app-drift.feature` — modified — bind the scanner behavior.
- `specs/apps/beaver-nest/behavior/beaver-nest-be/gherkin/README.md` — modified — link additive behavior features.
- `specs/apps/beaver-nest/behavior/beaver-nest-be/gherkin/persistence/fresh-database.feature` — created — specify pre-listen migration.
- `specs/apps/beaver-nest/behavior/beaver-nest-be/gherkin/persistence/migration-restart.feature` — created — specify migration idempotence.
- `specs/apps/beaver-nest/behavior/beaver-nest-be/gherkin/persistence/broken-migration.feature` — created — specify sanitized startup failure.
- `specs/apps/beaver-nest/behavior/beaver-nest-be/gherkin/persistence/sqlite-settings.feature` — created — specify SQLite safety settings.
- `specs/apps/beaver-nest/behavior/beaver-nest-be/gherkin/persistence/sqlite-contention.feature` — created — specify bounded busy behavior.
- `specs/apps/beaver-nest/behavior/beaver-nest-be/gherkin/recovery/online-backup.feature` — created — specify online backup validation.
- `specs/apps/beaver-nest/behavior/beaver-nest-be/gherkin/recovery/verified-restore.feature` — created — specify verified stopped-app restore.

### Commands and Results

- Worktree initialization (`npm install`, `npm run doctor -- --fix`) — passed; lockfile ordering-only churn was restored.
- Package clearance: NVD, GitHub Advisory Database, Snyk, vendor pages, CISA KEV, and EPSS applicability reviewed; the vulnerable native SQLite transitive dependency required the recorded Path C override.
- Backend unit, integration, specification, quick, dependency-audit, environment-contract, Rhino environment validation, and exact-pin/no-ORM checks — passed.
- Linux Docker integration runner — passed all eight real SQLite and Kestrel tests.
- Coverage follow-up — passed 36 unit tests with 94.91% line coverage against the unchanged 90% threshold; migration now creates its validated directory before DbUp opens the database.
- Rhino quick gate under simulated pre-push `GIT_DIR` context — passed; fixture Git initialization is isolated from the active repository lock.

### Evidence

- `plans/in-progress/beaver-nest-app-setup/evidence/phase-2-dependency-adoption.md` — exact Path A/Path B clearance evidence.

## Phase 3

### Task Status

- In progress: readiness contract, aggregate E2E observations, final delivery ledger, and PR-quality cycle.

### Files Changed

- `specs/apps/beaver-nest/containers/contracts/openapi.yaml` — modified — add exact safe readiness contracts.
- `specs/apps/beaver-nest/containers/contracts/project.json` — modified — replace the contract test no-op.
- `specs/apps/beaver-nest/containers/contracts/tests/readiness-contract.sh` — created — assertion-only readiness contract validation.
- `specs/apps/beaver-nest/containers/contracts/README.md` — modified — document readiness contract verification.
- `apps/beaver-nest-be/src/BeaverNestBe/Domain/Readiness.fs` — modified — expose provider-independent readiness result.
- `apps/beaver-nest-be/src/BeaverNestBe/Application/ReadinessPort.fs` — created — inject bounded readiness probes.
- `apps/beaver-nest-be/src/BeaverNestBe/Api/ReadinessHandlers.fs` — created — return safe 200/503 readiness responses.
- `apps/beaver-nest-be/src/BeaverNestBe/WebApp.fs` — modified — map the readiness route.
- `apps/beaver-nest-be/src/BeaverNestBe/Program.fs` — modified — compose the real SQLite readiness probe.
- `apps/beaver-nest-be/src/BeaverNestBe/BeaverNestBe.fsproj` — modified — register readiness source compilation.
- `apps/beaver-nest-be/tests/unit/BeaverNestBe.UnitTests.fsproj` — modified — register readiness feature bindings and tests.
- `apps/beaver-nest-be/tests/unit/Steps/HealthSteps.fs` — modified — retain liveness bindings.
- `apps/beaver-nest-be/tests/unit/Steps/ReadinessSteps.fs` — created — bind readiness scenarios.
- `apps/beaver-nest-be/tests/unit/Tests/HealthHandlerTests.fs` — modified — characterize liveness response safety.
- `apps/beaver-nest-be/tests/unit/Tests/ReadinessHandlerTests.fs` — created — test safe ready and unavailable handlers.
- `apps/beaver-nest-be/tests/unit/Tests/SqliteInfrastructureTests.fs` — created — complete provider-neutral SQLite infrastructure coverage.
- `apps/beaver-nest-be/tests/integration/BeaverNestBe.IntegrationTests.fsproj` — modified — register real readiness HTTP tests.
- `apps/beaver-nest-be/tests/integration/HostBootTests.fs` — modified — avoid proxying the loopback real-host probe.
- `apps/beaver-nest-be/tests/integration/ReadinessHttpTests.fs` — created — verify real Kestrel readiness 200/503 behavior.
- `specs/apps/beaver-nest/behavior/beaver-nest-be/gherkin/health/service-health.feature` — deleted — superseded liveness feature.
- `specs/apps/beaver-nest/behavior/beaver-nest-be/gherkin/health/liveness.feature` — created — specify database-detail-free liveness.
- `specs/apps/beaver-nest/behavior/beaver-nest-be/gherkin/health/readiness-ready.feature` — created — specify current-schema readiness.
- `specs/apps/beaver-nest/behavior/beaver-nest-be/gherkin/health/readiness-unready.feature` — created — specify safe unavailable readiness.
- `apps/beaver-nest-be-e2e/steps/readiness.steps.ts` — created — bind readiness HTTP observations.
- `apps/beaver-nest-be-e2e/steps/persistence.steps.ts` — created — bind persistence observations.
- `apps/beaver-nest-be-e2e/steps/recovery.steps.ts` — created — bind recovery observations.
- `apps/beaver-nest-be-e2e/utils/readiness.ts` — created — share safe readiness response assertions.
- `apps/beaver-nest-be-e2e/README.md` — modified — replace the retired health-feature link with the current liveness feature.
- `apps/beaver-nest-be/scripts/run-e2e.sh` — modified — reuse a supplied CI backend rather than competing for its host port.
- `apps/beaver-nest-be-e2e/project.json` — modified — execute the E2E wrapper regression test as its unit target.
- `apps/beaver-nest-be-e2e/tests/run-e2e-existing-service.test.sh` — created — reproduce and guard the CI port-collision regression.
- `apps/beaver-nest-be/src/BeaverNestBe/Infrastructure/Sqlite/Connection.fs` — modified — satisfy strict typed interpolation analysis.
- `apps/beaver-nest-be/src/BeaverNestBe/Operations/Database.fs` — modified — satisfy strict typed interpolation and string-conversion analysis.
- `apps/beaver-nest-be/Dockerfile.integration` — modified — use sanitized disposable runtime defaults.
- `apps/beaver-nest-be/docker-compose.integration.yml` — modified — mount a disposable database directory.
- `apps/beaver-nest-be/scripts/run-e2e.sh` — modified — run generated E2E steps against the explicit loopback endpoint.

### Commands and Results

- Contract lint, assertion-only unit test, bundle, and backend/frontend code generation — passed.
- Backend unit/specification/quick gates — passed; behavior coverage reports 11 specs, 15 scenarios, and 64 steps.
- Backend E2E specification gate and Docker-backed E2E — passed; 13 passed with one environment-conditional unavailable-runtime skip, and no unconditional skips or coverage gaps.
- Five-project build/typecheck/lint/quick/specification matrix — passed.
- Backend coverage follow-up — passed at 94.91% line coverage with unchanged exclusions and threshold.
- Repository link validation — repair the stale backend E2E health-feature link detected by the pre-push gate.
- Heavy CI E2E failure — avoid a second Compose binding to port 19320 when CI has already started the full stack.
- PR .NET analyzer failure — add explicit interpolation formats and string result type annotations without changing SQLite behavior.
- Controlled host-loopback smoke could not keep `dotnet watch` alive because the execution sandbox rejects the required background-process priority operation; the Docker E2E and Docker integration runner provide the successful equivalent real HTTP evidence.

### Evidence

- `plans/in-progress/beaver-nest-app-setup/evidence/phase-2-dependency-adoption.md` — retained as the dependency-policy clearance and waiver record for the combined delivery unit.

### Cycle 1 Follow-Up

- `apps/beaver-nest-be/src/BeaverNestBe/Domain/Readiness.fs` — modified — align the exact runtime
  response bodies with the OpenAPI nested `components` schemas for both ready and unavailable states.
- `apps/beaver-nest-be/tests/unit/Steps/ReadinessSteps.fs` — modified — assert the exact nested ready
  and unavailable JSON contracts.
- `apps/beaver-nest-be/tests/unit/Tests/ReadinessHandlerTests.fs` — modified — regress the complete
  200 and 503 payload bodies, including unavailable component states.
- `apps/beaver-nest-be-e2e/utils/readiness.ts` — modified — require the exact nested, no-extra-fields
  readiness body in aggregate browser assertions.
- `apps/beaver-nest-be-e2e/utils/compose-runtime.ts` — created — constrain aggregate Docker/CLI probes
  to the disposable Compose runtime without a production test route or host database access.
- `apps/beaver-nest-be-e2e/steps/{readiness,persistence,recovery}.steps.ts` — modified — replace
  readiness-only false positives with disposable database inspections, an invalid-migration boot,
  configured connection checks, bounded contention, and real backup/restore CLI observations.
- `apps/beaver-nest-be/scripts/run-e2e.sh` — modified — pass the disposable Compose-project capability
  only to locally started E2E runs; externally supplied services do not gain Docker control.
- `infra/dev/beaver-nest-app/docker-compose.ci.yml` — modified — provide the disposable shared backup
  volume required by the stopped-service restore observation.
- Cycle 1 contract follow-up: backend unit tests (52 passed), backend lint, E2E typecheck, E2E lint,
  Compose rendering, existing-service wrapper regression, and `git diff --check` — passed.
- Local direct Kestrel verification remains bounded but unavailable: the targeted
  `ReadinessHttpTests` run reached xUnit test start and produced no result before an explicit 90-second
  alarm stopped it (exit 142). Those tests construct `webAppWith` directly and do not enter `Program`
  or acquire a database/service lock, so this is not evidence of double lock acquisition. The direct
  Docker E2E invocation likewise produced no output before it was stopped; neither local run is
  claimed as passed. Post-push CI must verify the changed Docker flow.

### CI Blocker Follow-Up

- `.github/workflows/_reusable-app-test-local-deploy-stag.yml` — modified — give the combined E2E
  job enough budget for Playwright operating-system dependency provisioning before either suite runs.
- Heavy CI run `30809428411` — all prerequisite gates passed; its E2E job was cancelled after the
  35-minute job timeout while `npx playwright install-deps` was still downloading Ubuntu packages.
  The log confirms neither BE nor FE E2E test had started, so this is provisioning-budget exhaustion,
  not a skipped test or application-test failure. The job limit is therefore raised to 60 minutes;
  both suites remain mandatory.

## Phase 4

### Task Status

- In progress: Vite client-rendered workspace migration and frontend behavior coverage.

### Files Changed

- `plans/in-progress/beaver-nest-app-setup/execution-state.md` — modified — initialize the Unit 3
  append-only Phase 4 ledger before implementation.
- `plans/in-progress/beaver-nest-app-setup/evidence/phase-4-dependency-adoption.md` — created —
  record required exact-pin, soak, security, KEV, EPSS, and functional-stability evidence before
  the frontend manifest and Dockerfile changes.
- `plans/in-progress/beaver-nest-app-setup/tech-docs.md` — modified — replace Phase 4 dependency
  stop-condition rows with the approved exact pins and clearance results.
- `apps/beaver-nest-fe/src/test/vite-entry.test.ts` — created — RED contract for the required static
  Vite entry files and canonical project classification.
- `apps/beaver-nest-fe/package.json` — modified — replace Next-only runtime dependencies with the
  pre-cleared exact Vite, React-plugin, and MSW pins.
- `package-lock.json` — modified — record the approved frontend manifest resolution.
- `package.json` — modified — remediate direct root tooling that prevents the required moderate-or-higher
  npm audit from passing.
- `libs/web-ui/package.json` — modified — align Storybook, Tailwind, and React-plugin peer ranges with
  the approved Vite 8 graph.
- `apps/beaver-nest-be-e2e/package.json` — modified — adopt the last 60-day-soaked patched BDD runner.
- `apps/beaver-nest-fe-e2e/package.json` — modified — adopt the same patched BDD runner.
- `docs/reference/security-waivers.md` — modified — record any necessary Path C audit remediation
  waivers before their manifest edits.
- `libs/web-ui/.storybook/{main,preview}.ts` — modified — replace the obsolete Next-specific
  Storybook adapter with the React/Vite adapter.
- `libs/web-ui/src/**/*.stories.tsx` — modified — change the Storybook type-only imports in the
  inventory-listed shared UI stories from the Next adapter to the React/Vite adapter; no story
  behavior is changed.
- `apps/beaver-nest-fe/index.html` — created — static Vite document entry without inline bootstrap
  state or server-generated data.
- `apps/beaver-nest-fe/vite.config.ts` — created — client Vite configuration and exact workspace aliases.
- `apps/beaver-nest-fe/src/main.tsx` — created — client React mount entry.
- `apps/beaver-nest-fe/src/App.tsx` — created — temporary client root for the Vite-entry GREEN step.
- `apps/beaver-nest-fe/tsconfig.json` — modified — remove Next compiler and generated-directory assumptions.
- `apps/beaver-nest-fe/vitest.config.ts` — modified — remove the retired Vite path plugin and Next-only
  coverage exclusions.
- `apps/beaver-nest-fe/project.json` — modified — replace Next dev/build/start targets with loopback Vite
  dev and static `dist` build targets, and classify the application as `platform:vite`.
- `apps/beaver-nest-fe/src/styles.css` — created — retain the client token and Tailwind style graph.
- `apps/beaver-nest-fe/{next.config.ts,src/env.ts,src/app/page.tsx,src/app/page.test.tsx,src/app/layout.tsx,src/app/error.tsx,src/app/error.test.tsx,src/app/not-found.tsx,src/app/not-found.test.tsx,src/app/icon.tsx,src/app/globals.css,src/components/AppFrame.tsx,src/components/AppShell.tsx,src/lib/greeting-client.ts,src/lib/greeting-client.test.ts,src/test/landing.steps.ts}` — deleted — exact obsolete Next-only landing surface listed in Phase 4.
- Exact final Phase 4 inventory, one repository-relative path per line, is recorded below for the
  required staging ledger.

  ```text
  apps/beaver-nest-be-e2e/package.json
  apps/beaver-nest-fe-e2e/README.md
  apps/beaver-nest-fe-e2e/package.json
  apps/beaver-nest-fe-e2e/playwright.viewport.config.ts
  apps/beaver-nest-fe-e2e/project.json
  apps/beaver-nest-fe-e2e/steps/accessibility.steps.ts
  apps/beaver-nest-fe-e2e/steps/landing.steps.ts
  apps/beaver-nest-fe-e2e/steps/workspace.steps.ts
  apps/beaver-nest-fe-e2e/tests/workspace-viewport.spec.ts
  apps/beaver-nest-fe-e2e/utils/readiness-route.ts
  apps/beaver-nest-fe/.env.example
  apps/beaver-nest-fe/Dockerfile
  apps/beaver-nest-fe/index.html
  apps/beaver-nest-fe/next.config.ts
  apps/beaver-nest-fe/oxlint.json
  apps/beaver-nest-fe/package.json
  apps/beaver-nest-fe/project.json
  apps/beaver-nest-fe/src/App.test.tsx
  apps/beaver-nest-fe/src/App.tsx
  apps/beaver-nest-fe/src/app/error.test.tsx
  apps/beaver-nest-fe/src/app/error.tsx
  apps/beaver-nest-fe/src/app/globals.css
  apps/beaver-nest-fe/src/app/icon.tsx
  apps/beaver-nest-fe/src/app/layout.tsx
  apps/beaver-nest-fe/src/app/not-found.test.tsx
  apps/beaver-nest-fe/src/app/not-found.tsx
  apps/beaver-nest-fe/src/app/page.test.tsx
  apps/beaver-nest-fe/src/app/page.tsx
  apps/beaver-nest-fe/src/components/AppFrame.tsx
  apps/beaver-nest-fe/src/components/AppShell.tsx
  apps/beaver-nest-fe/src/components/ReadinessPanel.tsx
  apps/beaver-nest-fe/src/env.ts
  apps/beaver-nest-fe/src/lib/greeting-client.test.ts
  apps/beaver-nest-fe/src/lib/greeting-client.ts
  apps/beaver-nest-fe/src/lib/readiness-client.ts
  apps/beaver-nest-fe/src/lib/readiness-state.test.ts
  apps/beaver-nest-fe/src/lib/readiness-state.ts
  apps/beaver-nest-fe/src/main.tsx
  apps/beaver-nest-fe/src/styles.css
  apps/beaver-nest-fe/src/test/landing.steps.ts
  apps/beaver-nest-fe/src/test/msw/handlers.ts
  apps/beaver-nest-fe/src/test/msw/server.ts
  apps/beaver-nest-fe/src/test/readiness.integration.test.tsx
  apps/beaver-nest-fe/src/test/vite-entry.test.ts
  apps/beaver-nest-fe/src/test/workspace.steps.ts
  apps/beaver-nest-fe/src/theme.test.ts
  apps/beaver-nest-fe/src/theme.ts
  apps/beaver-nest-fe/tsconfig.json
  apps/beaver-nest-fe/vite.config.ts
  apps/beaver-nest-fe/vitest.config.ts
  apps/beaver-nest-fe/vitest.integration.config.ts
  docs/reference/security-waivers.md
  plans/in-progress/beaver-nest-app-setup/delivery.md
  infra/dev/beaver-nest-app/tests/frontend-integration-target.sh
  libs/web-ui-token/package.json
  libs/web-ui/.storybook/main.ts
  libs/web-ui/.storybook/preview.ts
  libs/web-ui/package.json
  libs/web-ui/src/components/alert/alert.stories.tsx
  libs/web-ui/src/components/app-header/app-header.stories.tsx
  libs/web-ui/src/components/badge/badge.stories.tsx
  libs/web-ui/src/components/button/button.stories.tsx
  libs/web-ui/src/components/card/card.stories.tsx
  libs/web-ui/src/components/dialog/dialog.stories.tsx
  libs/web-ui/src/components/highlight-text/highlight-text.stories.tsx
  libs/web-ui/src/components/hue-picker/hue-picker.stories.tsx
  libs/web-ui/src/components/icon/icon.stories.tsx
  libs/web-ui/src/components/info-tip/info-tip.stories.tsx
  libs/web-ui/src/components/input/input.stories.tsx
  libs/web-ui/src/components/label/label.stories.tsx
  libs/web-ui/src/components/progress-ring/progress-ring.stories.tsx
  libs/web-ui/src/components/scroll-to-top/scroll-to-top.stories.tsx
  libs/web-ui/src/components/search-component/search-component.stories.tsx
  libs/web-ui/src/components/sheet/sheet.stories.tsx
  libs/web-ui/src/components/side-nav/side-nav.stories.tsx
  libs/web-ui/src/components/stat-card/stat-card.stories.tsx
  libs/web-ui/src/components/tab-bar/tab-bar.stories.tsx
  libs/web-ui/src/components/textarea/textarea.stories.tsx
  libs/web-ui/src/components/theme-toggle/theme-toggle.stories.tsx
  libs/web-ui/src/components/toggle/toggle.stories.tsx
  libs/web-ui/src/primitives/badge/badge.stories.tsx
  libs/web-ui/src/primitives/button/button.stories.tsx
  libs/web-ui/src/primitives/card/card.stories.tsx
  libs/web-ui/src/primitives/code-block/code-block.stories.tsx
  libs/web-ui/src/primitives/code-block/copy-button.stories.tsx
  libs/web-ui/src/primitives/command/command.stories.tsx
  libs/web-ui/src/primitives/dialog/dialog.stories.tsx
  libs/web-ui/src/primitives/dropdown-menu/dropdown-menu.stories.tsx
  libs/web-ui/src/primitives/resizable-panel/resizable-panel.stories.tsx
  libs/web-ui/src/primitives/scroll-area/scroll-area.stories.tsx
  libs/web-ui/src/primitives/separator/separator.stories.tsx
  libs/web-ui/src/primitives/sheet/sheet.stories.tsx
  libs/web-ui/src/primitives/table/table.stories.tsx
  libs/web-ui/src/primitives/tabs/tabs.stories.tsx
  libs/web-ui/src/primitives/tooltip/tooltip.stories.tsx
  package-lock.json
  package.json
  plans/in-progress/beaver-nest-app-setup/evidence/phase-4-dependency-adoption.md
  plans/in-progress/beaver-nest-app-setup/execution-state.md
  plans/in-progress/beaver-nest-app-setup/tech-docs.md
  specs/apps/beaver-nest/behavior/beaver-nest-fe/gherkin/README.md
  specs/apps/beaver-nest/behavior/beaver-nest-fe/gherkin/hello/landing-page.feature
  specs/apps/beaver-nest/behavior/beaver-nest-fe/gherkin/network/readiness-recovery.feature
  specs/apps/beaver-nest/behavior/beaver-nest-fe/gherkin/workspace/browser-readiness.feature
  specs/apps/beaver-nest/behavior/beaver-nest-fe/gherkin/workspace/no-promotional-cta.feature
  specs/apps/beaver-nest/behavior/beaver-nest-fe/gherkin/workspace/readiness-loading.feature
  ```

### Commands and Results

- Unit 3 worktree provisioning, `npm install`, and `npm run doctor -- --fix` — passed. The initial
  install reordered one existing lockfile block; that mechanical churn was restored before any
  Phase 4 dependency selection.
- Vite-entry RED contract — failed as expected because the static entry, Vite configuration, client
  entry, Vite targets, and `platform:vite` tag do not exist yet.
- Initial approved-candidate installation — rejected safely by npm with `ERESOLVE`: Vite 6.4.3 cannot
  satisfy the official React plugin 6.0.2 peer range (`^8.0.0`). No force or legacy-peer-deps override
  was used. The final Vite 8.0.16 selection is recorded as a functional hold and installed cleanly.
- Moderate-or-higher npm audit — currently fails on pre-existing root tooling and shared UI workspace
  transitive dependencies, including an incompatible Vite 8.0.13 copy from old Storybook/Tailwind peer
  ranges. The Phase 4 audit gate remains open while the documented security remediation updates the
  affected direct manifests.
- Dependency remediation — `npm audit --audit-level=moderate` now exits 0. The complete audit retains
  one low-severity upstream esbuild advisory only; it does not meet the policy's moderate threshold.
  The compatible React/Vite Storybook conversion removes the otherwise unresolvable Next advisory.
- Vite entry GREEN — `nx run beaver-nest-fe:build --skip-nx-cache` passes and emits static `dist/`; Nx
  reports loopback Vite dev/build targets, no start target, and canonical `platform:vite`.
- Client workspace behavior — FE quick gate passes (5 test files, 9 tests, 97.87% statements, 93.54%
  branches, 100% functions, and 97.82% lines); the non-cacheable MSW integration target passes; FE and
  FE E2E specification gates pass, including 4 frontend specs, 4 scenarios, 17 steps, and no E2E
  coverage gaps.
- Responsive direct-Playwright check — Vite starts successfully, but the local sandbox rejects the
  Chromium launch with `mach_port_rendezvous_mac.cc Permission denied (1100)`. No viewport assertion is
  claimed as passed locally; the required Linux CI run remains the verification environment.
- Final Phase 4 scans — the retired Next, greeting, API-base-variable, and production test-hook scans
  exit 1 as required; `git diff --check`, exact-pin verification, Dockerfile lint at warning threshold,
  and the moderate-or-higher audit pass.
- Pre-commit root-cause follow-up — the mandatory emoji convention check found the pre-existing
  `⚗️` sample label in the now-touched badge story. It is replaced with the equivalent plain-text
  `Pre-Alpha` label; no emoji violation remains in the staged Phase 4 surface.

### Evidence

- `evidence/phase-4-dependency-adoption.md` — Path B functional-hold clearance for Vite 8.0.16,
  Path B clearance for React plugin 6.0.2 and MSW 2.14.6, and Path A clearance and immutable digest
  for Node 24.16.0 Alpine. No Phase 4 package manifest or Dockerfile change was made before this
  evidence and table update.
- Completed: the Phase 4 Vite CSR workspace, behavior specs, MSW integration coverage, and isolated
  browser route fixtures are ready for the local delivery-unit commit; no Phase 4 push or PR is open.

## Phase 5

### Task Status

- In progress: same-origin production runtime, security and routing boundaries, durable container
  operations, and CI integration.

### Files Changed

- `plans/in-progress/beaver-nest-app-setup/execution-state.md` — modified — initialize the Phase 5
  append-only ledger before any Dockerfile or runtime change.
- `plans/in-progress/beaver-nest-app-setup/evidence/phase-5-container-base-images.md` — created —
  record Path A base-image pins, immutable digests, source checks, and intended `FROM` occurrences
  before Dockerfile edits.
- `plans/in-progress/beaver-nest-app-setup/tech-docs.md` — modified — replace the Phase 5 pending
  container-image rows with the selected exact tags, digests, and clearance statuses before Dockerfile
  edits.
- `infra/dev/beaver-nest-app/tests/affected-propagation.sh` — created — enforce that a changed Vite
  workspace propagates to the combined backend image project.
- `apps/beaver-nest-be/project.json` — modified — declare the production image's build-time frontend
  dependency without creating an app-to-app source import.
- `apps/beaver-nest-be/scripts/start-development.sh` — created — require a distinct external
  development SQLite directory and start only the loopback backend process.
- `infra/dev/beaver-nest-app/tests/development-ports.sh` — created — enforce the independent local
  Vite/API ports and reject an obsolete Compose reset command.
- `package.json` — modified — make the canonical local development command start the two loopback Nx
  targets rather than the production Compose topology.
- `.dockerignore` — modified — keep host artifacts out of the root build context while re-including only
  BeaverNest contract inputs needed for in-container code generation.
- `apps/beaver-nest-be/Dockerfile` — modified — build the contract and Vite output, publish the backend,
  and run the combined production runtime as `10001:10001` on `19300`.
- `apps/beaver-nest-be/Dockerfile.integration` and
  `infra/dev/beaver-nest-app/Dockerfile.be.dev` — modified — use the approved exact .NET SDK image.
- `apps/beaver-nest-fe/Dockerfile` and `infra/dev/beaver-nest-app/Dockerfile.fe.dev` — modified —
  retain only Vite build/development semantics with the approved exact Node image.
- `apps/beaver-nest-be/scripts/container-entrypoint.sh` — created — validate durable-directory ownership
  and modes before the non-root runtime starts.
- `infra/dev/beaver-nest-app/tests/{clean-image-build,container-permissions}.sh` — created — cover
  source-only image construction and fail-closed persistent-storage permissions.
- `apps/beaver-nest-be/src/BeaverNestBe/{WebApp,Program,BeaverNestBe.fsproj}.fs` — modified — begin
  combined static/routing and security-header composition.
- `apps/beaver-nest-be/src/BeaverNestBe/Api/{GreetingHandlers.fs}` and
  `apps/beaver-nest-be/src/BeaverNestBe/Domain/Greeting.fs` — deleted — begin retirement of the obsolete
  greeting surface.
- `apps/beaver-nest-be/src/BeaverNestBe/Api/{SecurityHeaders,StaticContent}.fs` — created — begin
  immutable security policy and static-routing helpers.
- `apps/beaver-nest-be/tests/unit/{BeaverNestBe.UnitTests.fsproj,Steps/BddState.fs,Steps/RoutingSteps.fs,Tests/NotFoundHandlerTests.fs,Tests/SecurityHeaderTests.fs,Tests/StaticRoutingTests.fs,Fixtures/vite/index.html,Fixtures/vite/assets/app-12345678.js}` — modified or created — cover global headers and the API/static/SPA routing boundaries.
- `apps/beaver-nest-be/tests/unit/Steps/HealthSteps.fs` — modified — remove the obsolete standalone-service binding so the specification suite has no orphaned step.
- `apps/beaver-nest-be/tests/unit/{Steps/GreetingSteps.fs,Tests/GreetingHandlerTests.fs}` — deleted —
  remove the retired greeting behavior bindings and tests.
- `specs/apps/beaver-nest/containers/contracts/{openapi.yaml,README.md,tests/readiness-contract.sh}` — modified — remove the retired greeting operation/schema and make the contract guard reject its return.
- `specs/apps/beaver-nest/behavior/beaver-nest-be/gherkin/{README.md,hello/greeting.feature,routing/*.feature}` — modified, deleted, or created — replace greeting behavior with explicit JSON API, static asset, SPA fallback, and retirement scenarios.
- `apps/beaver-nest-be/src/BeaverNestBe/Operations/Database.fs`, `Program.fs`, and
  `tests/unit/Tests/DatabaseOperationsTests.fs` — modified — add a lock-serialized live SQLite
  integrity command with focused regression coverage.
- `infra/dev/beaver-nest-app/{docker-compose.yml,docker-compose.ci.yml,scripts/{lib,preflight,operations,start}.sh,tests/{preflight,persistence,publication,operations-profile,start}.sh}` — modified or created — provide the fail-closed single-service production topology, explicit preflight, and bounded operational profiles.
- `apps/beaver-nest-{be,fe}-e2e/{project.json,scripts/run-playwright.sh}` and
  `apps/beaver-nest-be/scripts/run-e2e.sh` — modified or created — separate pure Playwright runners
  from one disposable combined-stack lifecycle owner.
- `infra/dev/beaver-nest-app/tests/{e2e-runner-ownership,development-data-isolation,token-entry,vocabulary-contract,workflow-contract}.sh` — created — preserve combined-topology contracts as executable checks.
- `specs/apps/beaver-nest/behavior/beaver-nest-be/gherkin/development/development-data-isolation.feature`
  and `apps/beaver-nest-be/tests/unit/Steps/DevelopmentSteps.fs` — created — bind the isolated local
  development SQLite requirement.
- `.github/workflows/{_reusable-app-test-local-deploy-stag,beaver-nest-app-test-local-deploy-stag,publish-images}.yml` — modified — make CI exercise one disposable combined runtime and publish the combined image for frontend or backend changes.
- `.github/workflows/{beaver-nest-app-test-stag,beaver-nest-be-build-deploy-stag}.yml` — deleted — retire unsupported standalone staging claims.
- `repo-config.yml`, `apps/beaver-nest-fe/.env.example`, and `infra/dev/beaver-nest-app/tests/env-contract.sh` — modified or deleted — make the backend template the sole runtime environment owner while retaining E2E URLs only in the CI harness registry.
- `AGENTS.md`, `docs/reference/monorepo-structure.md`, `repo-governance/development/infra/nx-targets.md`, `apps/beaver-nest-{be,fe}/README.md`, `infra/dev/beaver-nest-app/README.md`, `.github/workflows/README.md`, `libs/web-ui-token/{README.md,src/beaver-nest.css}`, and `repo-governance/development/frontend/design-tokens.md` — modified — document Vite CSR, the combined runtime, same-origin publication, and token entry points.
- `.claude/agents/apps-beaver-nest-{be,fe}-deployer.md`, `.claude/agents/apps-beaver-nest-fe-content-{maker,checker}.md`, `.claude/skills/apps-beaver-nest-fe-developing-content/SKILL.md`, `.claude/skills/swe-developing-frontend-ui/reference/brand-context.md`, and generated `.opencode/`/`.cursor/` mirrors — modified — align harness guidance with the Vite foundation-status screen and unprovisioned combined deployment target.

### Commands and Results

- MCR inspection resolves Node 24.16.0 Alpine, .NET SDK 10.0.302 Noble, and ASP.NET 10.0.10 Noble to
  the evidence-recorded immutable multi-architecture digests. The policy evidence and clearance table
  were updated before any consuming Dockerfile edit.
- Container static checks — shellcheck, hadolint, exact-version-and-digest `FROM` audit, and the scoped
  whitespace check pass. The Docker daemon probe stalled, so dynamic clean-image and permissions runs
  remain for a working Docker executor/CI; they are not claimed as locally passed.
- Backend routing and retirement checks — contract unit test, backend unit test (65 tests), backend
  specification gate (14 specs, 14 scenarios, 60 steps), frontend contract code generation, and the
  backend quick gate pass after formatting the two new F# API modules. The first specification run
  correctly exposed missing literal route bindings and an obsolete health binding; both were added or
  removed before the passing rerun.
- Operations and topology contracts — preflight, persistence, publication, operations-profile, start,
  E2E-runner ownership, development-data isolation, environment ownership, token-entry, vocabulary,
  workflow, and affected-propagation checks pass. Compose renders successfully with an explicit
  loopback/mktemp fixture and `--env-file /dev/null`; no operator file was read.
- Backend integrity extension — 66 unit tests pass. Backend specifications pass with 15 specs, 15
  scenarios, and 64 fully bound steps. Both E2E specification gates pass after retired greeting
  bindings were removed.
- CI and harness checks — `actionlint`, `npm run validate:sync`, `rhino-cli env validate`,
  `repo-config validate`, selected Markdown checks, shellcheck, and `git diff --check` pass.

### Evidence

- `evidence/phase-5-container-base-images.md` — Path A LTS selection and sanitized digest inspection.

## Phase 6

### Task Status

- Awaiting the required human-only production runtime attestation. No operator environment file, real
  address, hostname, directory path, username, or credential has been read, printed, or modified.

### Files Changed

- `plans/in-progress/beaver-nest-app-setup/execution-state.md` — modified — initialize the Phase 6
  append-only ledger before human-runtime evidence work.
- `libs/web-ui-token/project.json`, `libs/web-ui-token/vitest.config.ts`, and `package.json` —
  modified — run the unit-test command from the workspace root while preserving the library test
  root, and force the existing patched Vitest 4.1.8 resolution so the runner and Gherkin adapter
  share one module instance.
- `plans/in-progress/beaver-nest-app-setup/evidence/phase-4-dependency-adoption.md` and
  `plans/in-progress/beaver-nest-app-setup/tech-docs.md` — modified — record the renewed Vitest
  4.1.8 security clearance and shared-instance regression resolution.
- `apps/beaver-nest-be/tests/unit/BeaverNestBe.UnitTests.fsproj` — modified — force VSTest mode so
  Coverlet's MSBuild driver can instrument .NET 10 test execution.
- `apps/beaver-nest-be-e2e/README.md` and
  `plans/in-progress/beaver-nest-app-setup/evidence/phase-4-dependency-adoption.md` — modified —
  repair the retired-greeting and dependency-policy links reported by the pre-push validator.
- `AGENTS.md` — modified — replace the inline model-selection summary with its canonical policy link
  to satisfy the instruction-size gate through progressive disclosure.

### Commands and Results

- No production runtime command has been run by the AI. The local sandbox cannot satisfy the required
  real VPN/operator attestation and must not receive the operator environment file.

### Evidence

- Pending the human confirmation described in Phase 6 of `delivery.md`; any later evidence will use
  placeholders only and contain no private runtime values.
