# Product Requirements — islamic-be-init

## Product Overview

`islamic-be` is a stateless HTTP service that will serve generic Islamic tools over a versioned REST
API. This delivery ships its skeleton: a Gin server, a contract-first OpenAPI 3.1 specification, a
Godog-bound Gherkin corpus, a Playwright E2E companion, and exactly one route —
`GET /api/v1/health`.

Everything that makes the service _interesting_ is deliberately absent. What ships is the shape:
the contract chain, the test pyramid, the quality gates, and the Go language lane that makes all
three enforceable.

## Personas

| Persona                | Needs from this delivery                                                                                                                  |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **Platform engineer**  | A Go project that passes every repository gate the same way an F# or TypeScript project does — no carve-outs.                             |
| **Product engineer**   | A running service with a contract, a spec corpus, and a test harness, so the first real endpoint is an addition rather than a bootstrap.  |
| **Container operator** | A liveness endpoint that answers without touching any dependency, so an orchestrator can distinguish "process up" from "process healthy". |
| **Reviewer**           | Go diffs that arrive with formatting, linting, coverage, and behaviour-binding already enforced in CI.                                    |

## User Stories

**US-1 — Liveness**
As a container operator, I want `islamic-be` to advertise its liveness over HTTP, so that an
orchestrator routes traffic only to instances that have finished starting.

**US-2 — Contract-first types**
As a product engineer, I want the service's Go request and response types generated from its OpenAPI
specification, so that a handler cannot silently drift from the published contract.

**US-3 — Configurable port**
As a developer, I want to override the listener port without editing source, so that `islamic-be`
runs alongside the other backends on one machine.

**US-4 — Gated Go**
As a platform engineer, I want Go projects formatted, linted, coverage-checked, and
behaviour-bound by the same gates as every other language, so that no Go code merges under a weaker
standard.

## Acceptance Criteria

### US-1 — Liveness

```gherkin
Feature: Islamic BE health endpoint
  As a system operator
  I want the BE to advertise liveness
  So that orchestrators can route traffic only to healthy instances

  Scenario: Health endpoint returns 200
    Given the islamic-be service is running
    When I send GET /api/v1/health
    Then the response status is 200
    And the response body has a "status" field equal to "healthy"

  Scenario: Health endpoint reports the JSON content type
    Given the islamic-be service is running
    When I send GET /api/v1/health
    Then the response "Content-Type" header starts with "application/json"

  Scenario: An unknown route is rejected
    Given the islamic-be service is running
    When I send GET /api/v1/does-not-exist
    Then the response status is 404
```

### US-2 — Contract-first types

```gherkin
Feature: Islamic BE contract conformance
  As a product engineer
  I want handlers bound to the generated contract interface
  So that a route cannot drift from the published specification

  Scenario: The OpenAPI specification bundles and lints clean
    Given the islamic-contracts specification at specs/apps/islamic/be/contracts/openapi.yaml
    When I run the islamic-contracts lint target
    Then the bundle succeeds
    And Spectral reports no errors

  Scenario: Generated types satisfy the server interface
    Given generated contract types produced by oapi-codegen
    When I build islamic-be
    Then the router's handler set satisfies the generated ServerInterface
```

### US-3 — Configurable port

```gherkin
Feature: Islamic BE port resolution
  As a developer
  I want a deterministic port-resolution order
  So that one exported variable cannot retarget every app at once

  Scenario: The default port applies when nothing is set
    Given no ISLAMIC_BE_PORT variable is set
    And no --port flag is supplied
    When the service resolves its listener port
    Then the resolved port is 8402

  Scenario: The prefixed variable overrides the default
    Given ISLAMIC_BE_PORT is set to "9402"
    When the service resolves its listener port
    Then the resolved port is 9402

  Scenario: The flag overrides the prefixed variable
    Given ISLAMIC_BE_PORT is set to "9402"
    And the --port flag is supplied with "9500"
    When the service resolves its listener port
    Then the resolved port is 9500

  Scenario: A malformed port fails at startup
    Given ISLAMIC_BE_PORT is set to "not-a-port"
    When the service resolves its listener port
    Then startup fails with a message naming ISLAMIC_BE_PORT
    And the service does not fall back to the default

  Scenario: A bare PORT variable is ignored
    Given PORT is set to "9999"
    And no ISLAMIC_BE_PORT variable is set
    When the service resolves its listener port
    Then the resolved port is 8402
```

### US-4 — Gated Go

```gherkin
Feature: Go language lane
  As a platform engineer
  I want Go projects gated like every other language
  So that no Go code merges under a weaker standard

  Scenario Outline: A Go project runs only in the Go quality gate
    Given a project tagged "lang:go"
    When the pull-request quality gate enumerates affected projects
    Then the "<job>" job excludes it
    And the "go" job includes it

    Examples:
      | job        |
      | typescript |
      | dotnet     |
      | flutter    |

  Scenario: The aggregate gate cannot pass while the Go job fails
    Given the "go" job has failed
    When the "quality-gate" aggregation job evaluates its dependencies
    Then the aggregate reports failure

  Scenario: A Go toolchain gap is reported by the doctor
    Given a machine with no Go toolchain installed
    When the developer runs the doctor command
    Then a "go" row reports the tool as missing

  Scenario: Godog step registrations count as Gherkin bindings
    Given a Go source file registering a Godog step for an active scenario
    When behaviour-coverage runs the unit adapter
    Then the scenario is reported as bound

  Scenario: An unbound active scenario fails the coverage gate
    Given an active scenario with no Godog registration and no exemption
    When behaviour-coverage runs the unit adapter
    Then the target exits non-zero and names the unbound scenario
```

## Product Scope

### In Scope

- `islamic-be`: Gin HTTP server, one route, deterministic port resolution, `Dockerfile`,
  `infra/dev/islamic-be/docker-compose.yml`, `.env.example`.
- `islamic-be-e2e`: Playwright + `playwright-bdd` suite driving the real process over HTTP.
- `islamic-contracts`: OpenAPI 3.1 specification with `lint`, `bundle`, and `docs` targets.
- `specs/apps/islamic/be/`: README, `architecture.md`, and the Gherkin corpus.
- The Go platform lane: CI detect arm, `go` job, three exclude-list entries, aggregate-gate wiring,
  `setup-go` action, tag vocabulary, `golangci-lint` gate, `go` under `doctor.extra-tools`,
  behaviour-coverage Go extractor, `rhino-cli` Go env scanner.

### Out of Scope (Non-Goals)

These are the product's future, recorded here so no reviewer mistakes their absence for an oversight
and no executor treats them as implied work:

- **Prayer times** — `GET /api/v1/prayer-times`. Needs a calculation-method decision, a solar
  algorithm choice, and a correctness-testing strategy of its own.
- **Qibla direction** — `GET /api/v1/qibla`. Needs a great-circle bearing implementation and a
  precision contract.
- **Hijri conversion** — `GET /api/v1/hijri`. Needs a calendar-variant decision (tabular versus
  sighting-based) that is a scholarly question, not an engineering one.
- **Calculation-method metadata** — the reference data those three endpoints would share.
- Persistence, caching layers, message bus, authentication, rate limiting, quotas.
- Container publication, staging branch, Kubernetes manifest, public domain.
- Client SDK generation for any consumer.
- **The config-driven doctor refactor** — delivered by [`lms-init`](../lms-init/README.md) DU1, which
  this plan depends on and does not duplicate.
- **Generalizing `extractBindings` to a multi-language dispatch** — delivered by `lms-init` DU2. This
  plan adds a `.go` arm to the dispatch that unit leaves behind.

## Product Risks

| Risk                                                                                         | Mitigation                                                                                                                |
| -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| A health-only service reads as scaffolding and reviewers question the whole delivery.        | `brd.md` carries the product rationale; this document's Non-Goals name the intended endpoints without committing to them. |
| The generated `ServerInterface` is regenerated into a shape the handler no longer satisfies. | `codegen` gates `build` and `typecheck`; a drifted handler fails compilation rather than failing at runtime.              |
| The 99% unit coverage floor is met by testing trivia rather than behaviour.                  | Every active scenario needs a Godog binding; coverage and binding are separate gates and both must pass.                  |
| Port 8402 collides with something undocumented on a developer machine.                       | Port resolution is explicit and fails loudly on a malformed value; `docs/reference/web-sites.md` records the allocation.  |

## See Also

- [brd.md](./brd.md) — business rationale and success metrics.
- [tech-docs.md](./tech-docs.md) — how the acceptance criteria are implemented.
- [delivery.md](./delivery.md) — the execution checklist.
