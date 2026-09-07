# Plan: islamic-be-init (In Progress)

Stand up `islamic-be` — a Go/Gin REST API serving generic Islamic tools — and its Playwright
companion `islamic-be-e2e`, together with the first-class Go language lane this monorepo needs
before either project can be gated.

**Status**: In Progress
**Delivery Mode**: `worktree-to-pr`

## Context

The repository serves three product domains (`ose`, `organiclever`, `ayokoding`) across two F#
backends. Generic Islamic tooling — prayer times, qibla direction, hijri conversion — is a distinct
product with a different audience and a different runtime profile from `ose-be`'s compliance
gap-analysis API: it is stateless, cacheable, and computation-bound rather than database- and
model-bound. It earns its own deployable.

Go is **half-provisioned** here. `Brewfile` installs it, `repo-config.yml` runs `gofmt`, and
`rhino-cli test-coverage` already parses Go `cover.out` — residue from the deleted
`a-demo-be-golang-gin` demo. What is missing is load-bearing:

- `pr-quality-gate.yml` has no Go job, and `lang:go` is absent from the `typescript` and `flutter`
  jobs' exclude lists — Go targets would execute on runners with no Go toolchain.
- `scripts/behaviour-coverage.mjs` dispatches `.fs` to an F# extractor and everything else to a
  TypeScript one; Godog step registrations parse as nothing. Unit-layer Gherkin proof has no
  exemption, so this blocks the BDD contract outright.
- `lang:go`, `platform:gin`, and `domain:islamic` are outside the controlled tag vocabulary.
- `rhino-cli`'s env-contract scanner rejects `lang: go` with a hard error.

This plan closes all four before shipping either app.

## Scope

**Repositories**: `ose-public` (primary) and `ose-private` (one paired parity PR for the
byte-identical `apps/rhino-cli` change).

**New projects**: `islamic-be` (Go 1.26 / Gin, port 8402), `islamic-be-e2e` (Playwright + BDD),
`islamic-contracts` (OpenAPI 3.1 at `specs/apps/islamic/be/contracts/`).

**Platform changes**: Go CI lane, Go binding extractor, Go env-contract scanner, three tag-vocabulary
amendments, `golangci-lint` gate registration.

**Out of scope**: every Islamic-tool endpoint. v1 serves `GET /api/v1/health` and nothing else. No
CD — no GHCR publish, no `stag-islamic-be` branch, no k3s manifest.

## Approach Summary

Six delivery PRs in `ose-public` plus one parity PR in `ose-private`, lane-first so no PR ever lands
a Go target that CI cannot run:

1. **Go platform lane** — conventions, `setup-go` action, `go` CI job, exclude-list fixes,
   behaviour-coverage Go extractor.
2. **Specs corpus** — `specs/apps/islamic/be/` behaviours, architecture, and OpenAPI contract.
3. **The service** — Gin server, `oapi-codegen`-generated types and `ServerInterface`, Godog unit
   bindings, Dockerfile, dev compose.
4. **The E2E suite** — Playwright BDD against the running process.
5. **rhino-cli Go env scanner** — paired byte-identical change across both repositories.
6. **Registry and docs** — env-contract registration, port table, app map, architecture reference.

Phases 7 and 8 capture knowledge and archive the plan.

## Core Files

- [brd.md](./brd.md) — why this product line exists and what success looks like.
- [prd.md](./prd.md) — personas, user stories, Gherkin acceptance criteria, and explicit Non-Goals.
- [tech-docs.md](./tech-docs.md) — architecture, decision records, and the file-impact analysis.
- [delivery.md](./delivery.md) — the phased execution checklist and its gates.
- [learnings.md](./learnings.md) — running log drained by the Knowledge Capture phase.

## See Also

- [Plans Organization Convention](../../../repo-governance/conventions/structure/plans.md)
- [Behaviour-Driven Development](../../../repo-governance/development/behaviour-driven-development.md)
- [Nx Target Standards](../../../repo-governance/development/infra/nx-targets.md)
