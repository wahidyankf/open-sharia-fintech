# Plan: islamic-be-init (In Progress)

Stand up `islamic-be` — a Go/Gin REST API serving generic Islamic tools — and its Playwright
companion `islamic-be-e2e`, on top of the Go language lane this monorepo still lacks.

**Status**: In Progress — planning complete; implementation has not started
**Delivery Mode**: `worktree-to-pr`
**Depends on**: `lms-init` ([PR #487](https://github.com/wahidyankf/ose-public/pull/487)) DU1 and DU2, both merged

## Context

The repository serves three product domains (`ose`, `organiclever`, `ayokoding`) across two
F#/Giraffe backends [Repo-grounded — `apps/ose-be/project.json`]. Generic Islamic tooling — prayer
times, qibla direction, hijri conversion — is a distinct product with a different audience and a
different runtime profile from `ose-be`'s compliance gap-analysis API: it is stateless, cacheable,
and computation-bound rather than database- and model-bound. It earns its own deployable.

Go is **half-provisioned** here. `Brewfile` installs it, `repo-config.yml` registers the
`format-gofmt` and `format-verify-gofmt` gate pair [Repo-grounded — `repo-config.yml:547`, `:556`],
and `rhino-cli` already parses Go `cover.out`. All of it is residue from the deleted
`a-demo-be-golang-gin` demo, and none of it is load-bearing. Four surfaces still mis-handle Go:

| Surface                                 | Verified failure mode                                                                                                                                                                                                                                                |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `.github/workflows/pr-quality-gate.yml` | No `has-go` output and no `lang:go` detect arm; the `typescript` (`:302`), `dotnet` (`:334`), and `flutter` (`:358`) jobs each select by _excluding_ known `lang:` tags, and none excludes `go` — so a Go project runs in all three, on runners with no Go toolchain |
| `scripts/behaviour-coverage.mjs`        | `BINDING_FILE` matches only `.ts`, `.tsx`, `.fs` (`:20`), and `extractBindings` dispatches `.fs` to F# and everything else to TypeScript (`:374`) — Godog registrations parse as nothing, so every scenario reports `undefined Unit binding`                         |
| `rhino-cli` `Env.fs:1592`               | The env-contract scanner returns `Error "unsupported lang: %s"` for anything but `typescript` and `fsharp`                                                                                                                                                           |
| Tag vocabulary                          | `lang:go`, `platform:gin`, and `domain:islamic` are outside the controlled vocabulary, and inventing values is a named anti-pattern                                                                                                                                  |

`Env.fs` sits at line 9 of `apps/rhino-cli/parity-manifest.sha256`, which makes the scanner change a
**two-repository delivery**.

## Why this plan depends on `lms-init`

`lms-init` [Repo-grounded — `plans/in-progress/lms-init/`] solves the same class of problem for
Java, and its first two delivery units generalize the exact seams Go needs:

- **DU1** makes the `rhino-cli` doctor tool inventory config-driven via `doctor.extra-tools`.
  `go` is absent from the hardcoded inventory today [Repo-grounded — `RepoConfig.fs:172`], and the
  `gofmt` gates declare no `doctor-tools:`, so `npm run doctor` is silent about a missing Go
  toolchain. After DU1, registering `go` is a `repo-config.yml` entry with **no `rhino-cli` change
  and no parity cost** — the saving D-4 of `lms-init` was designed to produce.
- **DU2** teaches `behaviour-coverage.mjs` a fourth language and factors the shared feature-reference
  scan into one helper, adds the `has-java` CI detect/job pattern with a `setup-java` composite
  action, and adds `tag:lang:java` to all three exclude lists. Go then follows an established
  pattern instead of inventing one, and the two plans stop colliding in the same four files.

Landing Go first would force `lms-init` to rebase every one of those seams. Landing it second makes
the Go lane roughly 40% smaller. See [`tech-docs.md`](./tech-docs.md) §2 D-0 for the full record.

## Scope

**Repositories**: `ose-public` (primary) and `ose-private` (one paired parity PR for the
byte-identical `Env.fs` change and its regenerated manifest).

**New projects**: `islamic-be` (Go 1.26 / Gin, port 8402), `islamic-be-e2e` (Playwright + BDD),
`islamic-contracts` (OpenAPI 3.1 at `specs/apps/islamic/be/contracts/`).

**Platform changes**: Go CI detect arm, job, and three exclude-list entries; `setup-go` composite
action; Go binding extractor; `golangci-lint` gate; `go` under `doctor.extra-tools`; Go
env-contract scanner; three tag-vocabulary amendments.

**Out of scope**: every Islamic-tool endpoint. v1 serves `GET /api/v1/health` and nothing else. No
CD — no GHCR publish, no `stag-islamic-be` branch, no k3s manifest.

## Approach Summary

Six delivery units in `ose-public`; DU5 additionally lands a paired PR in `ose-private`:

1. **DU1 — Go platform lane** — tag vocabulary, `setup-go`, `go` CI job, three exclude-list fixes,
   `lint-golangci` gate, `go` doctor declaration, behaviour-coverage Go extractor.
2. **DU2 — Specs corpus** — `specs/apps/islamic/be/` behaviours, architecture, OpenAPI contract.
3. **DU3 — The service** — Gin server, `oapi-codegen` types and `ServerInterface`, Godog unit
   bindings, Dockerfile, dev compose.
4. **DU4 — The E2E suite** — Playwright BDD against the running process.
5. **DU5 — rhino-cli Go env scanner** — paired byte-identical change plus regenerated
   `parity-manifest.sha256` in both repositories.
6. **DU6 — Registry and docs** — env-contract registration, port table, app map, architecture
   reference.

Phase 7 captures knowledge; Phase 8 archives the plan.

## Navigation

- [`brd.md`](./brd.md) — why this exists, who it serves, business risks and non-goals
- [`prd.md`](./prd.md) — personas, user stories, and Gherkin acceptance criteria
- [`tech-docs.md`](./tech-docs.md) — architecture, pinned versions, decisions with rejected
  alternatives, the file-impact tree, and rollback
- [`delivery.md`](./delivery.md) — the ordered, execution-grade checklist and its phase gates
- [`learnings.md`](./learnings.md) — the transient Knowledge Capture log

## Related

- `lms-init` ([PR #487](https://github.com/wahidyankf/ose-public/pull/487)) — the Java lane plan this one builds on
- [BDD standard](../../../repo-governance/development/behaviour-driven-development.md)
- [Nx Target Standards](../../../repo-governance/development/infra/nx-targets.md)
- [Cross-Repo rhino-cli Byte-Identity Standard](../../../repo-governance/development/infra/nx-targets/cache-cross-repo-byte-identity.md)
