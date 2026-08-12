# Technical Design — BeaverNest Flutter Web Client

## Architecture

```mermaid
%%{init: {'theme':'base', 'themeVariables': {'primaryColor':'#0173B2','primaryTextColor':'#fff','primaryBorderColor':'#000','lineColor':'#029E73','secondaryColor':'#DE8F05','tertiaryColor':'#CC78BC'}}}%%
flowchart LR
  WEB[Flutter Web adapter] -->|relative /api| API[beavernest-be]
  WEB --> CORE[Platform-neutral Dart core]
  CORE --> UI[Responsive Flutter widgets]
  API --> SQLITE[(SQLite)]
  CONTRACT[OpenAPI 3.1 contract] --> GEN[Dart-native generator]
  GEN --> CORE
  FUTURE[Later native plan] -. adds adapters only .-> CORE
```

```mermaid
%%{init: {'theme':'base', 'themeVariables': {'primaryColor':'#0173B2','primaryTextColor':'#fff','primaryBorderColor':'#000','lineColor':'#029E73','secondaryColor':'#DE8F05','tertiaryColor':'#CC78BC'}}}%%
sequenceDiagram
  participant B as Browser
  participant W as Flutter Web adapter
  participant A as BeaverNest API
  B->>W: Load same-origin application
  W->>A: GET /api/v1/readiness
  A-->>W: 200 ready or 503 not-ready
  B->>W: Open Diagnostics
  W->>A: GET /api/v1/diagnostics
  A-->>W: Safe snapshot
```

## Future-Ready Structure

The app uses package-private boundaries that a later native plan extends rather than replaces:

- `lib/domain/`: immutable readiness and diagnostics models, URI-free result states, reducers, and
  interfaces; no Flutter platform imports.
- `lib/application/`: use cases for refresh and diagnostics; depends only on domain interfaces.
- `lib/presentation/`: responsive Flutter widgets and route-independent view models; no
  `dart:html`, browser storage, or network implementation imports.
- `lib/presentation/theme/beavernest_theme.dart`: a `ThemeExtension` for surveyed semantic
  readiness, surface, and focus tokens; it translates design intent without copying React/CSS.
- `lib/platform/web/`: same-origin HTTP client and browser integration; the sole Web-specific edge.
- `lib/generated/`: Dart OpenAPI types generated from the bundled contract; never handwritten.
- `test/`: pure domain/application tests plus widget tests; `integration_test/`: browser flow.

A later Android/macOS plan may add `lib/platform/android/` and `lib/platform/macos/`, native
endpoint configuration, and packaging. It must not change the shared status widgets, domain models,
or generated contract boundary unless a new feature requires it.

## Design Decisions

| Decision                            | Rationale                                                                                                                                                                                                                       |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Flutter Web now, native later       | Removes the legacy UI risk without bundling platform provisioning, security, and device validation into the first migration.                                                                                                    |
| Mobile-first responsive Web         | Browser phone/tablet layouts prove adaptable information hierarchy before a native plan exists.                                                                                                                                 |
| Platform-neutral core plus Web edge | Limits browser coupling and makes later adapter addition additive rather than a rewrite.                                                                                                                                        |
| Same-origin relative API            | Preserves the current combined-runtime security/deployment boundary and avoids CORS expansion.                                                                                                                                  |
| Dart-native code-generation spike   | The user selected generated OpenAPI types; the candidate must prove OpenAPI 3.1 union compatibility before it enters the toolchain.                                                                                             |
| Safe snapshot endpoint              | Adds operational context while retaining the backend's safe-response posture; it is live and non-persistent.                                                                                                                    |
| Strict atomic cutover               | User-approved exception to the default feature-flag rollout: retaining a legacy Vite/React bundle would violate the selected no-parallel-client requirement.                                                                    |
| `beavernest-app` name exception     | User-approved future-multiplatform exception to the normal `[domain]-app-web` naming tier; P2 updates `AGENTS.md` and reference inventories to record that this product identity is Flutter Web now with later native adapters. |

## Validated Build and Test Facts

| Fact                                                                                       | Evidence                                                                                                                                                                            |
| ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Flutter Web release assets are emitted by `flutter build web` to `build/web`.              | [Web-cited: Flutter documentation](https://docs.flutter.dev/platform-integration/web/building), accessed 2026-08-12; excerpt: "populates a `build/web` directory" with built files. |
| Flutter distinguishes unit, widget, and integration tests.                                 | [Web-cited: Flutter testing overview](https://docs.flutter.dev/testing/overview), accessed 2026-08-12; excerpt: Flutter documents tests at those separate layers.                   |
| Browser integration testing is supported by Flutter.                                       | [Web-cited: Flutter integration tests](https://docs.flutter.dev/testing/integration-tests), accessed 2026-08-12; excerpt: browser instructions run `flutter drive ... -d chrome`.   |
| The current repository has Flutter 3.41.5 installed but no Flutter application or FVM pin. | [Repo-grounded] `flutter --version` and repository file search on 2026-08-12.                                                                                                       |

## Dependency and Toolchain Policy

Phase 1 selects an exact Dart-native OpenAPI generator only after validating OpenAPI 3.1 input, the
`ready`/`not-ready` union, reproducible regeneration, supported Dart SDK, license, and the
repository dependency-bump safety policy. It records the selected package/version, lock evidence,
CVE review, and rejected candidates in `learnings.md`.

Commit only the FVM project configuration `.fvmrc` and any generator lock metadata; do not commit
the `.fvm/flutter_sdk` cache/symlink. All Flutter project commands call `fvm flutter` or `fvm dart`;
CI and the Docker builder run `fvm install` from the committed pin before analysis, test, and build.
Phase 1 records the selected digest-pinned Flutter builder image and its verification in
`plans/in-progress/beaver-flutter/evidence/flutter-builder-lock.md`. Extend `rhino-cli doctor` and
`repo-config.yml` only when the compatibility spike proves FVM validation can join the canonical
doctor gate without bypassing it.

## API Contract

Add `GET /api/v1/diagnostics` to the current OpenAPI 3.1 source and bundle.

- 200 `DiagnosticsReady`: a closed object (`additionalProperties: false`) with `status: "ready"`,
  string `version`, integer `uptimeSeconds` rounded down to a whole second, RFC 3339
  `serverTimeUtc`, and the existing closed readiness-component object.
- 503 `DiagnosticsUnavailable`: a closed object (`additionalProperties: false`) with
  `status: "unavailable"`, the same named readiness-component keys, and no internal cause.

Both responses set `Cache-Control: no-store`. The handler uses injected clock/version/uptime seams
for deterministic tests. The OpenAPI examples use only that allow-list, and decoder/handler tests
reject extra fields. It never returns configuration paths, exceptions, SQL, host names/addresses,
migration IDs, or stored history.

## Static Hosting

Replace the frontend Docker stage with a digest-pinned Flutter/FVM builder selected and recorded in
Phase 1. It runs `fvm install`, then the committed `fvm flutter build web`, and copies
`apps/beavernest-app/build/web/` into `wwwroot`. Before implementing cache policy, inventory the
actual `build/web` output in `evidence/flutter-web-asset-inventory.md`; only a filename proven
content-addressed receives immutable caching. `index.html`, bootstrap/loader/main scripts, manifests,
and un-hashed assets revalidate. Update `StaticContent.fs` fallback classification from this inventory.
Browser E2E must deploy v1 then v2 to the F# hosted bundle and prove a normal navigation obtains a
coherent v2 bundle, not only Flutter's development server.

## Browser Installation and Update Boundary

[Web-cited] A production PWA promoted for installation requires HTTPS (localhost/loopback is the
development exception), and Flutter no longer generates or manages a service worker by default.
Sources: [MDN installable PWA guidance](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable),
accessed 2026-08-12, excerpt: "must be served using the `https` protocol"; and
[Flutter Web FAQ](https://docs.flutter.dev/platform-integration/web/faq), accessed 2026-08-12,
excerpt: "no longer generates or manages a service worker by default."

Because the current production runtime is intentionally HTTP inside a VPN, this plan must not add a
manifest/service worker or claim PWA/offline/immediate auto-update. It adds only browser-specific
install guidance where the user agent offers it. Static bootstrap/scripts receive a revalidation cache
policy so a normal navigation can obtain a newer deployed bundle. A future private-HTTPS plan owns
the real PWA manifest, service worker, cache lifecycle, and the user-selected immediate reload
strategy.

## Test Strategy

| Layer               | Coverage                                                                                         |
| ------------------- | ------------------------------------------------------------------------------------------------ |
| Unit                | generated response mapping, status reducer, safe snapshot decoder.                               |
| Widget              | loading/ready/unavailable/retry, diagnostics, semantics, phone/tablet/desktop reflow.            |
| Backend integration | OpenAPI bundle, handler 200/503/no-store, forbidden-field regressions.                           |
| Browser integration | same-origin hosted Flutter bundle, refresh recovery, diagnostics, and responsive viewport proof. |
| Build               | `fvm flutter build web`.                                                                         |

## File-Impact Analysis

Scan-first scope is every explicit path below. P1 is non-deployed and non-routable; atomicity
applies to the live runtime/project/spec ownership at P2, not to the isolated foundation artifact.

```text
.
├── AGENTS.md [E] app catalog and platform facts
├── apps/
│   ├── README.md [E] application inventory
│   ├── beavernest-app-web/ [D] legacy React/Vite client, tests, Docker inputs
│   ├── beavernest-app-web-e2e/ [D] legacy Playwright identity and steps
│   ├── beavernest-app/ [N] Flutter Web: lib/{domain,application,presentation/theme,platform/web,generated}, test/, integration_test/, web/, project.json
│   ├── beavernest-app-e2e/ [N] renamed Playwright hosted-bundle suite, targets, steps, coverage baseline, reports
│   └── beavernest-be/
│       ├── README.md [E] Flutter Web local/runtime instructions
│       ├── src/BeaverNestBe/Api/DiagnosticsHandlers.fs [N] safe snapshot handler
│       ├── src/BeaverNestBe/Application/DiagnosticsPort.fs [N] injected snapshot boundary
│       ├── src/BeaverNestBe/{Program,WebApp}.fs [E] composition and route registration
│       ├── src/BeaverNestBe/Api/StaticContent.fs [E] Flutter cache/fallback policy
│       ├── src/BeaverNestBe/BeaverNestBe.fsproj [E] source order
│       ├── tests/unit/Tests/{DiagnosticsHandlerTests,StaticRoutingTests}.fs [N/E] safe API and cache regression tests
│       ├── tests/integration/DiagnosticsHttpTests.fs [N] 200/503/no-store contract proof
│       ├── Dockerfile [E] Flutter Web build and copy source
│       └── scripts/run-e2e.sh [E] renamed frontend suite
├── apps/beavernest-be-e2e/ [E] safe diagnostics browser assertions
├── docs/reference/{monorepo-structure.md,system-architecture/applications.md} [E] application identity
├── specs/apps/beavernest/
│   ├── containers/contracts/{openapi.yaml,generated/openapi-bundled.yaml} [E] diagnostics contract
│   ├── behavior/beavernest-app-web/ [D] Vite/React behavior identity
│   ├── behavior/beavernest-app/ [N] Flutter Web Gherkin identity
│   ├── behavior/beavernest-be/ [E] diagnostics endpoint Gherkin
│   ├── {README.md,behavior/README.md,product/README.md,components/{README.md,overview.md}} [E] names and scope
│   ├── containers/{README.md,container.md,contracts/README.md} [E] combined runtime contract
│   └── system-context/{README.md,context.md} [E] Flutter Web architecture
├── specs/README.md [E] BeaverNest product/spec inventory link
├── infra/dev/beavernest-app/{README.md,scripts/**,tests/**,docker-compose.yml,docker-compose.ci.yml} [E] local runtime and migration assertions
├── .github/workflows/{beavernest-app-test-local-deploy-stag.yml,publish-images.yml} [E] PR trigger, FVM setup, identity and artifacts
├── repo-governance/vision/beavernest.md [E] product application identity
├── {repo-config.yml,package.json,package-lock.json,.fvmrc} [E/N] project registry, dependency removal, exact FVM pin
├── plans/in-progress/README.md [E] active-plan index
└── plans/in-progress/beaver-flutter/{README.md,brd.md,prd.md,tech-docs.md,delivery.md,learnings.md,assets/**,evidence/**} [E] plan, visual contract, and evidence
```

## Rollback

Before merge, rollback is a normal PR revert. After the atomic replacement, restore the last
known-good image/commit; there is no retained legacy runtime client or feature flag. This plan stores
no client configuration, so no data migration constrains rollback.
