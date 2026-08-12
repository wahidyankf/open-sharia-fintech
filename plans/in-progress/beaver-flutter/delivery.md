# Delivery Checklist — BeaverNest Flutter Web Client

## Executor Legend

- `[AI]` performs repository, build, test, evidence, PR, and merge actions permitted by this plan.
- No `[HUMAN]` step is required. Browser install-as-app is progressive enhancement and does not need
  a developer-controlled app-store, device, or credential gate.

## Worktree

Use `worktrees/beaver-flutter/`. It already exists on branch `beaver-flutter`; all delivery
units reuse this one worktree and switch branches only at declared delivery boundaries.

If it must be provisioned manually from a fresh primary checkout, use
`claude --worktree beaver-flutter`; then run `npm install` and `npm run doctor -- --fix` before
Phase 0. The worktree path follows the [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md).

## Delivery Mode: worktree-to-pr

This repository is branch-protected. `[AI]` opens, reviews, and merges each delivery-boundary PR
after the hardened preconditions pass.

## Quality, Commit, and CI Protocol

- [ ] [AI] In this `delivery.md`, before every delivery-boundary push, run `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push` and `npm exec nx affected -t build,test:quick,lint,specs:behavior:coverage` from the repository root for the branch's actual blast radius; save any failure diagnosis in `plans/in-progress/beaver-flutter/evidence/quality-<delivery-branch>.md` — acceptance: all relevant unit, integration, browser E2E, lint, and behavior-spec coverage gates pass; fix all failures, not only failures caused by the current change, before pushing.
- [ ] [AI] For the boundary branch/PR recorded in this `delivery.md`, commit only ledger-owned changes thematically with Conventional Commit messages, splitting unrelated domains or concerns into separate commits; run `git diff --cached --check` before each commit and record commit hashes in `plans/in-progress/beaver-flutter/evidence/commits-<delivery-branch>.md` — acceptance: each commit is reviewable as one concern and has no whitespace error or foreign file.
- [ ] [AI] After every delivery-boundary push, inspect the branch/PR recorded in this `delivery.md` with `gh run list --branch <delivery-branch> --limit 20` and `gh run view <run-id> --json status,conclusion` every two minutes; after P2's `pull_request` trigger change, inspect its `PR Quality Gate` and `beavernest-app-test-local-deploy-stag` runs and record results in `plans/in-progress/beaver-flutter/evidence/ci-<delivery-branch>.md` — acceptance: every applicable run reaches `success`; investigate and fix every failure before the boundary can merge.

## Parallelization Model

Dependency DAG: `P0 -> P1 -> P2 -> P3`. Phases are serial because P1 establishes the reproducible
toolchain and UI evidence, P2 atomically introduces the diagnostics contract with the client
replacement, and P3 closes only after the replacement is proven.

### Delivery Boundaries

| Delivery unit       | Phases | Branch/worktree                                    | Boundary and reason                                                                                                                                 |
| ------------------- | ------ | -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Flutter foundation  | P1     | `beaver-flutter-p1` in `worktrees/beaver-flutter/` | P1 establishes a reproducible, non-user-reachable Flutter foundation and complete design evidence; it is independently reviewable and safe on main. |
| Flutter Web cutover | P2     | `beaver-flutter-p2` in the same worktree           | P2 is the atomic replacement; it cannot safely split into an intermediate frontend delivery.                                                        |
| Closure             | P3     | `beaver-flutter-p3` in the same worktree           | P3 carries evidence, quality results, knowledge capture, and archival.                                                                              |

### Delivery-Boundary Integration Protocol

This protocol applies from Phase 1 onward only. The pre-phase handoff creates/switches the listed
branch; at its declared boundary, commit only ledger-owned files, push, open a draft PR against
`main`, classify changed behavior, run the PR Review Maker→Fixer cycle (up to seven CI-gated rounds,
stopping at the first clean MEDIUM/HIGH/CRITICAL result), mark ready only after CI and required
manual verification, then `[AI]` merges and records post-merge verification. Phase 0 is excluded.
The plan's strict atomic cutover is the approved exception to a feature flag; no legacy client is
shipped beside Flutter.

## Phase 0: Environment Setup and Baseline

_Executor: repo-setup-manager. No PR, push, review, merge, or CI-monitoring action occurs in this
phase._

- [ ] [AI] Record the legacy baseline in `plans/in-progress/beaver-flutter/evidence/phase-0-baseline.md` with `npm exec nx show project beavernest-app-web`, `npm exec nx run beavernest-app-web:test:quick`, and `npm exec nx run beavernest-app-web-e2e:test:quick` — acceptance: each command and pass/fail output is timestamped, and a pre-existing failure is diagnosed before P1.
- [ ] [AI] Run `flutter doctor -v`, `flutter devices`, `flutter test --help`, and `fvm --version` if available; append exact Web/browser capability and FVM availability to `evidence/phase-0-baseline.md` — acceptance: P1 has a verified Web-only command baseline without writing implementation files.
- [ ] [AI] Inspect `apps/beavernest-be/src/BeaverNestBe/Api/StaticContent.fs`, the current Dockerfile, and browser E2E scripts; record the existing cache/header and asset-fallback behavior in `evidence/phase-0-baseline.md` — acceptance: P2 has no unexamined Vite-specific hosting assumption.

### Phase 0 Gate

- [ ] [AI] All checks must pass before starting Phase 1: run `npm run doctor -- --fix` and `git status --short` — acceptance: the toolchain is green and only plan/evidence ledger files exist.

**Pause Safety:** Safe to stop after the baseline. Resume with `cd worktrees/beaver-flutter && npm exec nx run beavernest-app-web:test:quick`.

## Phase 1 Branch Handoff

- [ ] [AI] Before authoring Phase 1 changes, run `git fetch origin --prune && git switch -c beaver-flutter-p1 origin/main` in `worktrees/beaver-flutter/` — acceptance: the sole plan worktree is on a fresh `beaver-flutter-p1` branch based on the latest `origin/main`.

## Phase 1: Reproducible Flutter Foundation and Complete Design Evidence

- [ ] [AI] Provision the non-deployed Flutter foundation: from the repository root run `fvm use 3.41.5 --force --skip-pub-get && fvm install && fvm flutter create --empty --platforms web apps/beavernest-app && git check-ignore -v .fvm/flutter_sdk`; add the minimal `.fvm/flutter_sdk` rule to `.gitignore` only if that final command fails; write the selected Flutter revision and builder-image digest discovery method to `plans/in-progress/beaver-flutter/evidence/flutter-builder-lock.md` — acceptance: tracked `.fvmrc` pins Flutter 3.41.5, `.fvm/flutter_sdk` is ignored, `fvm flutter --version` matches the pin, and the new application is not registered, served, or routable.
- [ ] [AI] RED: in `apps/beavernest-app/test/generated_contract_test.dart`, write the one generator scenario below and record candidate commands/results in `plans/in-progress/beaver-flutter/evidence/dart-generator-spike.md`; run `fvm flutter test test/generated_contract_test.dart` from `apps/beavernest-app/` — acceptance: the test fails because no selected generator emits the two closed readiness variants.

- [ ] [AI] GREEN: add the selected Dart-native generator and exact lock metadata to `apps/beavernest-app/pubspec.yaml` and `pubspec.lock`, generate `apps/beavernest-app/lib/generated/`, then run `fvm flutter pub get && fvm flutter test test/generated_contract_test.dart` — acceptance: the scenario passes, generation is reproducible from `specs/apps/beavernest/containers/contracts/generated/openapi-bundled.yaml`, and the evidence records package/version/license/CVE review and rejected candidates.
- [ ] [AI] REFACTOR: remove generator-test duplication in `apps/beavernest-app/test/generated_contract_test.dart` and run `fvm dart format --output=none --set-exit-if-changed test/generated_contract_test.dart && fvm flutter test test/generated_contract_test.dart` — acceptance: the one generated-client scenario remains green with no handwritten generated models.
- [ ] [AI] Create `apps/beavernest-app/project.json`: every Flutter target has `cwd: apps/beavernest-app`; `codegen` runs `fvm dart run <selected-generator> ../../specs/apps/beavernest/containers/contracts/generated/openapi-bundled.yaml lib/generated` after `beavernest-contracts:bundle`, has `cache: true`, input `../../specs/apps/beavernest/containers/contracts/generated/openapi-bundled.yaml`, and output `lib/generated/`; `build:web` runs `fvm flutter build web`, has `cache: true`, inputs `lib/**` and `web/**`, and output `build/web`; `build` delegates to it; `analyze`, `typecheck`, and `lint` each run `fvm flutter analyze` with `cache: true` and inputs `lib/**`, `test/**`, and `analysis_options.yaml`; `test:unit` runs `fvm flutter test test` with `cache: true`; `test:coverage` runs `fvm flutter test --coverage`, reads the resulting `coverage/lcov.info` `SF:` paths, writes the verified generated-model glob to `plans/in-progress/beaver-flutter/evidence/flutter-lcov-paths.md`, and runs `cargo run --release --quiet --manifest-path ../../apps/rhino-cli/Cargo.toml -- test-coverage validate apps/beavernest-app/coverage/lcov.info 80 --exclude '<verified-generated-glob>'`; it has `cache: true`, inputs `lib/**` and `test/**`, and output `coverage/lcov.info` (80% line coverage, excluding only verified generated `lib/generated/**` entries); `test:integration` runs `fvm flutter test integration_test -d chrome` with `cache: false`, and CI installs Chrome; `test:e2e` is an explicit no-op; `specs:structure-validation`, executed from the workspace root, runs `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- specs structure validate` with `cache: true` and `specs/apps/**` inputs; `test:specs` runs only that target until P2 adds feature bindings; `test:quick` serially composes analyze, lint, unit, coverage, and structure validation. Create `apps/beavernest-app-e2e/project.json` at P2 with `test:e2e` calling `apps/beavernest-be/scripts/run-e2e.sh --frontend`, `specs:behavior:coverage` using the new feature glob and its bound widget/source paths, `specs:e2e:coverage` using the renamed suite's steps/baseline, and `test:specs` composing those three validation targets — acceptance: every Flutter command uses `fvm flutter` or `fvm dart` from the declared project cwd, affected gates see `build`/`lint`/`test:quick`, coverage must meet the stated 80% threshold with a verified exclusion, and no app Gherkin feature or user-facing code exists yet.
- [ ] [AI] Revalidate `prd.md` and `assets/README.md` against `libs/web-ui` and the legacy shell, retaining two responsive desktop/tablet/mobile visual finalists per status, diagnostics, and shortcut surface — acceptance: all asset text matches the Web-only safe-data scope and each selected visual states focus, error, and responsive behavior.

### Phase 1 Gate

- [ ] [AI] All checks must pass before starting Phase 2: run `npm exec nx run beavernest-app:test:quick`, `npm exec nx run beavernest-app:test:coverage`, `npm exec nx run beavernest-app:specs:structure-validation`, and `npm run validate:sync` — acceptance: FVM, generated Dart readiness contract, target inventory, design assets, and harness bindings validate without exposing a new endpoint before the atomic cutover.
- [ ] [AI] At the P1 boundary, follow the Delivery-Boundary Integration Protocol for `beaver-flutter-p1` — acceptance: the draft PR is green, behavior-classified, review-clean, and merged before P2 starts.

**Pause Safety:** Safe to stop with an independently merged reproducible, non-routable Flutter foundation and complete visual contract. Resume with `git fetch origin --prune && git switch -c beaver-flutter-p2 origin/main`.

## Phase 2 Branch Handoff

- [ ] [AI] After the P1 PR merges, run `git fetch origin --prune && git switch -c beaver-flutter-p2 origin/main` in `worktrees/beaver-flutter/` — acceptance: P2 starts from the merged P1 foundation on a fresh delivery branch while reusing the plan's sole worktree.

## Phase 2: Responsive Flutter Web Atomic Cutover

- [ ] [AI] RED: add `specs/apps/beavernest/behavior/beavernest-be/gherkin/diagnostics/ready.feature` and a failing 200/no-extra-field handler test under `apps/beavernest-be/tests/`; run `npm exec nx run beavernest-be:test:quick` — acceptance: no diagnostics-ready route/schema exists.

  **Gherkin (binds) →** "Ready service returns a closed safe snapshot"

  ```gherkin
  Scenario: Ready service returns a closed safe snapshot
    Given BeaverNest accepts requests with current migrations
    When I send GET "/api/v1/diagnostics"
    Then the response is 200 with only status, version, uptimeSeconds, serverTimeUtc, and readiness components
  ```

- [ ] [AI] GREEN: add the 200 OpenAPI schema/example, `DiagnosticsPort.fs`, `DiagnosticsHandlers.fs`, deterministic composition, and handler test; run `npm exec nx run beavernest-contracts:bundle && npm exec nx run beavernest-be:test:quick` — acceptance: the ready scenario passes and rejects extra/sensitive fields.
- [ ] [AI] REFACTOR: consolidate ready-response mapping and run `dotnet tool run fantomas --check apps/beavernest-be && npm exec nx run beavernest-be:test:quick` — acceptance: ready diagnostics remains deterministic and formatted.
- [ ] [AI] RED: add `specs/apps/beavernest/behavior/beavernest-be/gherkin/diagnostics/unavailable.feature` and a failing 503/no-store test under `apps/beavernest-be/tests/`; run `npm exec nx run beavernest-be:test:quick` — acceptance: the unavailable route behavior fails.

  **Gherkin (binds) →** "Unready service returns a closed unavailable snapshot"

  ```gherkin
  Scenario: Unready service returns a closed unavailable snapshot
    Given BeaverNest cannot complete its readiness probe
    When I send GET "/api/v1/diagnostics"
    Then the response is 503 with Cache-Control no-store and no internal cause
  ```

- [ ] [AI] GREEN: add the 503 OpenAPI schema/example and unavailable handler mapping; run `npm exec nx run beavernest-contracts:bundle && npm exec nx run beavernest-be:test:quick` — acceptance: the unavailable scenario passes with only its closed allow-list.
- [ ] [AI] REFACTOR: remove duplicate unavailable fixtures and run `dotnet tool run fantomas --check apps/beavernest-be && npm exec nx run beavernest-be:test:quick` — acceptance: both diagnostics scenarios remain green.
- [ ] [AI] RED: add failing 200/503 browser/API checks consuming `specs/apps/beavernest/behavior/beavernest-be/gherkin/diagnostics/{ready,unavailable}.feature` in `apps/beavernest-be-e2e/steps/diagnostics.steps.ts` and update its `e2e-coverage-baseline.json`; run `npm exec nx run beavernest-be-e2e:test:e2e` — acceptance: the existing hosted runtime cannot satisfy the new diagnostics feature steps.

  **Gherkin (binds) →** "Ready service returns a closed safe snapshot"; "Unready service returns a closed unavailable snapshot"

  ```gherkin
  Scenario: Ready service returns a closed safe snapshot
    Given BeaverNest accepts requests with current migrations
    When I send GET "/api/v1/diagnostics"
    Then the response is 200 with only status, version, uptimeSeconds, serverTimeUtc, and readiness components

  Scenario: Unready service returns a closed unavailable snapshot
    Given BeaverNest cannot complete its readiness probe
    When I send GET "/api/v1/diagnostics"
    Then the response is 503 with Cache-Control no-store and no internal cause
  ```

- [ ] [AI] GREEN: implement the diagnostics step definitions and API assertions in `apps/beavernest-be-e2e/steps/diagnostics.steps.ts`; run `npm exec nx run beavernest-be-e2e:test:e2e && npm exec nx run beavernest-be-e2e:test:specs` — acceptance: both 200/503 paths and `Cache-Control: no-store` are proven through the hosted runtime and the E2E coverage baseline accepts every diagnostics scenario.
- [ ] [AI] REFACTOR: extract shared safe-field assertions to `apps/beavernest-be-e2e/utils/diagnostics.ts`; run `npm exec nx run beavernest-be-e2e:test:e2e` — acceptance: response assertions reject forbidden and additional fields without duplicated step logic.
- [ ] [AI] RED: add the same-origin shell Gherkin and a failing widget test in `specs/apps/beavernest/behavior/beavernest-app/gherkin/workspace-shell.feature` and `apps/beavernest-app/test/workspace_shell_test.dart`; run `npm exec nx run beavernest-app:test:unit` — acceptance: the shell cannot issue the relative readiness request before the Web adapter exists.

  **Gherkin (binds) →** "Web opens the same-origin workspace"

  ```gherkin
  Scenario: Web opens the same-origin workspace
    Given the combined BeaverNest runtime is ready
    When I open the Flutter Web root route
    Then the Foundation status shell is visible before readiness resolves
    And the client requests the relative "/api/v1/readiness" route
    And the status reports Application Available, Database Ready and Schema Current
  ```

- [ ] [AI] GREEN: implement the root shell and same-origin readiness port in `apps/beavernest-app/lib/{presentation,platform/web}/`; run `npm exec nx run beavernest-app:test:unit` — acceptance: the same-origin shell scenario passes without a configurable endpoint or CORS behavior.
- [ ] [AI] REFACTOR: isolate the request adapter from the widget tree and run `npm exec nx run beavernest-app:analyze` — acceptance: only `lib/platform/web/` owns HTTP/Web imports.
- [ ] [AI] RED: add the responsive workspace Gherkin and failing widget tests in `specs/apps/beavernest/behavior/beavernest-app/gherkin/workspace.feature` and `apps/beavernest-app/test/status_dashboard_test.dart`; run `npm exec nx run beavernest-app:test:unit` — acceptance: the status shell, its three widths, and loading/unavailable states fail before widgets exist.

  **Gherkin (binds) →** "Status reflows across browser widths"

  ```gherkin
  Scenario: Status reflows across browser widths
    Given the Flutter Web workspace is ready
    When I view status at mobile, tablet, and desktop widths
    Then every readiness component is visible without horizontal scrolling
  ```

- [ ] [AI] GREEN: implement `StatusDashboard`, `ReadinessSummary`, and `BeaverNestThemeExtension` under `apps/beavernest-app/lib/presentation/`; run `npm exec nx run beavernest-app:test:unit && npm exec nx run beavernest-app:analyze` — acceptance: the responsive scenario passes with semantic colors, text, icons, and live-region states.
- [ ] [AI] REFACTOR: share layout constraints instead of breakpoint-specific screens and run `fvm dart format --output=none --set-exit-if-changed lib test && npm exec nx run beavernest-app:test:coverage` — acceptance: the workspace scenario remains green with coverage threshold met.
- [ ] [AI] RED: add retry Gherkin and a failing reducer/widget test in `specs/apps/beavernest/behavior/beavernest-app/gherkin/retry.feature` and `apps/beavernest-app/test/readiness_retry_test.dart`; run `npm exec nx run beavernest-app:test:unit` — acceptance: retry recovery fails without navigation.

  **Gherkin (binds) →** "Status refresh recovers without navigation"

  ```gherkin
  Scenario: Status refresh recovers without navigation
    Given the same-origin endpoint initially reports unavailable
    When it recovers and I activate Refresh status
    Then the status changes to Ready with a polite announcement
  ```

- [ ] [AI] GREEN: implement the same-origin readiness adapter and refresh use case in `apps/beavernest-app/lib/{application,platform/web}/`; run `npm exec nx run beavernest-app:test:unit` — acceptance: retry passes without `dart:html` or browser-storage imports in core layers.
- [ ] [AI] REFACTOR: isolate Web imports in `apps/beavernest-app/lib/platform/web/` and run `npm exec nx run beavernest-app:lint && npm exec nx run beavernest-app:typecheck` — acceptance: retry remains green and Web-only dependencies are confined.
- [ ] [AI] RED: add diagnostics Gherkin and a failing widget decoder test in `specs/apps/beavernest/behavior/beavernest-app/gherkin/diagnostics.feature` and `apps/beavernest-app/test/diagnostics_screen_test.dart`; run `npm exec nx run beavernest-app:test:unit` — acceptance: only the safe fields render and the unavailable state has no cause.

  **Gherkin (binds) →** "Client presents a safe support snapshot"

  ```gherkin
  Scenario: Client presents a safe support snapshot
    Given the combined endpoint returns the diagnostics snapshot
    When I open Diagnostics
    Then only its contracted safe fields are visible
  ```

- [ ] [AI] GREEN: regenerate `apps/beavernest-app/lib/generated/` and implement `DiagnosticsScreen` and `SupportSnapshotCard`; run `npm exec nx run beavernest-app:codegen && npm exec nx run beavernest-app:test:unit` — acceptance: the diagnostics scenario passes for both response variants.
- [ ] [AI] REFACTOR: centralize diagnostics allow-list presentation and run `fvm dart format --output=none --set-exit-if-changed lib test && npm exec nx run beavernest-app:test:coverage` — acceptance: no forbidden field can reach the visual model.
- [ ] [AI] RED: add guidance Gherkin and a failing widget test in `specs/apps/beavernest/behavior/beavernest-app/gherkin/browser-shortcut.feature` and `apps/beavernest-app/test/browser_shortcut_test.dart`; run `npm exec nx run beavernest-app:test:unit` — acceptance: the browser-dependent, online-only copy, Escape, focus trap, and return focus behavior fail before the Help card exists.

  **Gherkin (binds) →** "Browser shortcut guidance is honest and accessible"

  ```gherkin
  Scenario: Browser shortcut guidance is honest and accessible
    Given I open Help in the Flutter Web workspace
    When I open browser shortcut guidance
    Then it states browser availability and an internet connection is required
    And Escape closes it and returns focus to Help
  ```

- [ ] [AI] GREEN: implement `BrowserShortcutGuidance` in `apps/beavernest-app/lib/presentation/`; run `npm exec nx run beavernest-app:test:unit` — acceptance: the guidance scenario passes without PWA, offline, auto-update, HTTPS, or native-install claims.
- [ ] [AI] REFACTOR: validate focus order, 44 px targets, and contrast in the widget tests; add `beavernest-app:specs:behavior:coverage` to `apps/beavernest-app/project.json` with `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- specs behavior-coverage validate --shared-steps specs/apps/beavernest/behavior/beavernest-app/gherkin apps/beavernest-app`, the new `gherkin/**/*.feature` glob, and Dart test/widget inputs; update `test:specs` and `test:quick` to compose it; run `npm exec nx run beavernest-app:lint && npm exec nx run beavernest-app:test:coverage && npm exec nx run beavernest-app:test:specs` — acceptance: keyboard and pointer accessibility assertions pass and affected `specs:behavior:coverage` discovers the Flutter behavior bindings.
- [ ] [AI] RED: add `specs/apps/beavernest/behavior/beavernest-app/gherkin/cache-update.feature`, a failing hosted-bundle cache scenario in `apps/beavernest-app-web-e2e/steps/`, and a failing cache/header test in `apps/beavernest-be/tests/unit/Tests/StaticRoutingTests.fs`; run `npm exec nx run beavernest-app-web-e2e:test:e2e` — acceptance: the legacy Vite bundle and stale deployment fail the same-origin hosted test.

  **Gherkin (binds) →** "Normal navigation receives a fresh hosted Flutter bundle"

  ```gherkin
  Scenario: Normal navigation receives a fresh hosted Flutter bundle
    Given version one of the F# hosted Flutter bundle has been loaded
    When version two is deployed and I navigate normally
    Then the browser loads a coherent version two bundle without a service worker
  ```

- [ ] [AI] Inventory the candidate Flutter bundle before cache implementation: run `beavernest_cache_temp=$(mktemp -d) && npm exec nx run beavernest-app:build && find apps/beavernest-app/build/web -type f -exec shasum -a 256 {} \; | sort > "$beavernest_cache_temp/v1.sha256"`, change the version value in `apps/beavernest-app/lib/application/build_version.dart` that is deliberately rendered by the status shell, rebuild, and run `find apps/beavernest-app/build/web -type f -exec shasum -a 256 {} \; | sort > "$beavernest_cache_temp/v2.sha256" && diff -u "$beavernest_cache_temp/v1.sha256" "$beavernest_cache_temp/v2.sha256" > plans/in-progress/beaver-flutter/evidence/flutter-web-v1-v2.diff || true && rm -rf -- "$beavernest_cache_temp"`; record the filename/hash diff and the exact revalidate versus immutable map for `index.html`, bootstrap/loader/main scripts, manifests, CanvasKit, fonts, and hashed files in `plans/in-progress/beaver-flutter/evidence/flutter-web-asset-inventory.md` — acceptance: the production-consumed version value changes an observed v2 artifact, cache classifications are based on that evidence, and no un-hashed file is marked immutable.
- [ ] [AI] GREEN: atomically rename `apps/beavernest-app-web-e2e/` to `apps/beavernest-app-e2e/`, replace the Vite client with `apps/beavernest-app/`, and update `AGENTS.md` to record the user-approved `[domain]-app` future-multiplatform exception, Docker, `StaticContent.fs` using the recorded cache map, static routing tests, `apps/beavernest-be/scripts/run-e2e.sh`, workflow trigger/FVM setup/artifact paths, specs, registries, docs, infra tests, and every file in the File-Impact Analysis; run `npm exec nx run beavernest-app:build && npm exec nx run beavernest-app-e2e:test:e2e` — acceptance: the F# container serves a coherent Flutter `build/web` bundle, the naming exception is documented, and the normal-navigation cache scenario passes.
- [ ] [AI] REFACTOR: verify the recorded cache map still classifies bootstrap/manifests/unhashed files for revalidation, delete legacy TypeScript contracts/Vite packages, and run `npm exec nx run beavernest-app:test:specs && npm exec nx run beavernest-app-e2e:test:specs && rg -n 'beavernest-app-web|vite|react' AGENTS.md apps docs specs infra .github repo-config.yml package-lock.json` — acceptance: only historical plan/archive matches remain and the hosted-bundle scenario is still green.
- [ ] [AI] Start the hosted combined runtime using the safe disposable setup from `apps/beavernest-be/scripts/run-e2e.sh`: run `beavernest_fixture_root=$(mktemp -d) && beavernest_project="beavernest-manual-${RANDOM}-${RANDOM}" && install -d -m 0700 "$beavernest_fixture_root/data" "$beavernest_fixture_root/backups" && export BEAVERNEST_BE_VPN_HOST_IP=127.0.0.1 BEAVERNEST_BE_PUBLIC_PORT=19320 BEAVERNEST_BE_HOST_DATA_DIRECTORY="$beavernest_fixture_root/data" BEAVERNEST_BE_BACKUP_DIRECTORY="$beavernest_fixture_root/backups" && beavernest_compose=(docker compose --env-file /dev/null -p "$beavernest_project" -f infra/dev/beavernest-app/docker-compose.yml) && trap '"${beavernest_compose[@]}" down --remove-orphans; rm -rf -- "$beavernest_fixture_root"' EXIT && "${beavernest_compose[@]}" up -d --build beavernest-app && for beavernest_attempt in $(seq 1 120); do curl -fsS http://127.0.0.1:19320/api/v1/readiness >/dev/null && break; [ "$beavernest_attempt" -lt 120 ] || exit 1; sleep 1; done`; use Playwright MCP to `browser_navigate` to the root route, `browser_snapshot` loading, ready, and unavailable states, `browser_click` Refresh status and Diagnostics, inspect `browser_console_messages`, and `browser_take_screenshot` at mobile (<768 px), tablet (768–1023 px), and desktop (>=1024 px) widths; save `plans/in-progress/beaver-flutter/evidence/phase-2-web-{loading,ready,unavailable}-{mobile,tablet,desktop}.png` — acceptance: this single-locale application has UI-to-API-to-UI recovery, no horizontal scroll, visible keyboard focus, compliant target sizes/contrast, and only approved browser-shortcut copy.
- [ ] [AI] Run `curl --include --silent --show-error http://127.0.0.1:19320/api/v1/readiness` and `curl --include --silent --show-error http://127.0.0.1:19320/api/v1/diagnostics`; obtain the unavailable proof by running `npm exec nx run beavernest-be-e2e:test:e2e` with the existing disposable unready fixture and copy its sanitized 503 header/body assertion into `plans/in-progress/beaver-flutter/evidence/phase-2-api-diagnostics-unavailable.md`; capture the ready responses in `plans/in-progress/beaver-flutter/evidence/phase-2-api-{readiness,diagnostics-ready}.md` — acceptance: readiness succeeds, diagnostics returns respectively 200 and fixture-proven 503 with `Cache-Control: no-store`, and neither response includes path, exception, SQL, host identifier, migration name, or an extra field.
- [ ] [AI] Run the static [UI quality gate](../../../repo-governance/workflows/ui/ui-quality-gate.md) and [API quality gate](../../../repo-governance/workflows/api/api-quality-gate.md) against the P2 diff; complete their maker→checker→fixer cycles and save reports below `generated-reports/` — acceptance: both gates report no blocking findings and their evidence links to the responsive screenshots and sanitized API captures.
- [ ] [AI] Run Rule-15 web exploratory/usability/design retest and Rule-16 API exploratory retest against the running combined endpoint; append each `EWT-*`, `UWT-*`, `DWT-*`, or `AET-*` defect as an unchecked item below — acceptance: no defect remains unchecked before archival.

### Rule-15/16 Retest Follow-ups

- [ ] [AI] No findings recorded yet — replace this placeholder with each concrete tester finding, or tick it only after all testers return no defects.

### Phase 2 Gate

- [ ] [AI] All checks must pass before starting Phase 3: run `npm exec nx affected -t build,test:quick,lint,specs:behavior:coverage`, `npm exec nx run beavernest-be-e2e:test:e2e`, and `npm exec nx run beavernest-app-e2e:test:e2e` — acceptance: affected checks, behavior-spec coverage, API E2E, and Flutter Web E2E pass after the rename.
- [ ] [AI] At the P2 boundary, follow the Delivery-Boundary Integration Protocol for `beaver-flutter-p2` — acceptance: the atomic cutover PR is fully reviewed, CI-green, visual/browser evidence attached, and merged.

**Pause Safety:** Safe to stop after Flutter Web is the only client and its three browser layouts are proven. Resume with `git fetch origin --prune && git switch -c beaver-flutter-p3 origin/main`.

## Phase 3 Branch Handoff

- [ ] [AI] After the P2 PR merges, run `git fetch origin --prune && git switch -c beaver-flutter-p3 origin/main` in `worktrees/beaver-flutter/` — acceptance: P3 starts from the merged cutover on a fresh closure branch while reusing the plan's sole worktree.

## Phase 3: Knowledge Capture and Plan Closure

- [ ] [AI] Review `learnings.md`, classify every item through secret/sensitivity and repository-relevance gates, promote any code learning to a separate `plans/backlog/` plan rather than landing it inline, and compare any idea candidate with `plans/ideas/README.md` plus existing two-pagers before creating or extending a brief — acceptance: no secret, sensitive endpoint, duplicate idea, or inline code follow-up remains in the archived plan.
- [ ] [AI] Run the plan-quality-gate in strict mode twice and save reports under `generated-reports/`; apply only validated plan fixes — acceptance: two consecutive strict validations have zero CRITICAL/HIGH/MEDIUM findings.
- [ ] [AI] Update `plans/in-progress/README.md`, move the plan to `plans/done/YYYY-MM-DD__beaver-flutter/`, and update `plans/done/README.md` in the P3 branch; run `npm run lint:md:fix` and `npm run validate:sync` — acceptance: plan indexes, links, diagrams, mockup assets, and generated bindings are valid.
- [ ] [AI] At the P3 boundary, follow the Delivery-Boundary Integration Protocol for `beaver-flutter-p3` — acceptance: closure PR is reviewed, CI-green, and merged; then offer worktree cleanup to the user without deleting it silently.

### Phase 3 Gate

- [ ] [AI] All checks must pass before declaring closure: verify the archived plan, evidence, and audit reports are committed in the closure PR and `git status --short` is clean — acceptance: plan execution has a traceable terminal record.

**Pause Safety:** Safe to stop after the user is offered cleanup. Resume with `git -C worktrees/beaver-flutter status --short`.
