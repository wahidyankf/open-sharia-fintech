# Machine-Checkable Port Registry Across the Four Sibling Repos

One-line summary: replace the four independent prose port tables with one machine-readable registry
and a validator, so a colliding port allocation fails a check instead of failing a bind at runtime.

> Demoted from a full `backlog/` plan to a two-pager on 2026-08-05. The full plan folder carried a
> README, a BRD (problem/impact/success-metrics/risks), a PRD (persona, user story, two Gherkin
> scenarios, non-goals), a tech-docs investigation sketch, a one-phase gated delivery checklist, and
> an empty learnings log — all of it framing an investigation whose two central decisions (where the
> registry lives, where the validator lives) are still unmade. A two-pager is the honest shape for
> that until those are answered.
> Relocated from beaver-nest/plans/ideas/cross-repo-port-registry.md on 2026-08-06 by plan-ideas-grooming.

## Problem / context

Port allocation across the four sibling repos is documented nowhere machine-readable — only as a
prose table in each repo's own `docs/reference/monorepo-structure.md`, and only for that repo's own
apps. `ose-public`, `ose-private`, and `beaver-nest` sit side by side under one parent
directory on a single development machine and can all run concurrently, so a collision is a
cross-repo concern that no single repo's table can settle. This repo's
[Port Allocation section](https://github.com/wahidyankf/beaver-nest/blob/main/docs/reference/monorepo-structure.md#port-allocation) records
`beaver-nest-fe` on `19310` and `beaver-nest-be` on `19320`, and states the rule that BeaverNest
deliberately allocates outside every band the siblings occupy: `3000-3401` (sibling Next.js/web
apps), `8000-8302` (sibling backend services), `4222-4224` (NATS), `5432-5438` (PostgreSQL), `6006`
(Storybook), `6379` (Redis), and `9090-9411` / `14250` / `14268` / `16686` / `24224` (the
observability stack). Those two ports are load-bearing beyond the docs — they appear in
`.github/workflows/beaver-nest-app-test-local-deploy-stag.yml` as `be-port: 19320` and
`web-port: 19310`, in the generated OpenAPI bundle's `http://localhost:19320` server URL, and in the
frontend's `next dev --port 19310`. Nothing enforces that the band rule holds, and nothing catches a table
going stale. The failure mode is silent: two apps in different repos claiming the same port only
surfaces when someone tries to run both at once.

No collision has actually happened yet. What surfaced this was the near-miss discipline: the
`baseerah-repo-reset` plan verified on 2026-07-31 that `19310` and `19320` were free by running a
literal `rg -n '19310|19320'` across all three sibling working trees (exit 1, no matches) before
committing them — a manual, one-time, human-eyeball workaround, explicitly not a fix.

## Why now

The cost is currently near zero because BeaverNest has exactly two networked apps and picked a band
nobody else touches. That is precisely the cheap moment to build the registry: the correct answer is
already known, so the validator can be written against a state it must report as clean, and a
synthetic duplicate injection is the only way to see it fail. Every additional app added anywhere in
the four repos widens the surface and makes the initial enumeration more expensive. Waiting until a
collision forces the issue means building this while also debugging a bind failure.

## Prior art / precedents

- [Port Allocation in this repo's monorepo structure reference](https://github.com/wahidyankf/beaver-nest/blob/main/docs/reference/monorepo-structure.md#port-allocation)
  — the per-repo prose table and band-exclusion rule the registry would supersede.
- [baseerah-repo-reset plan](https://github.com/wahidyankf/beaver-nest/blob/main/plans/done/2026-07-31__baseerah-repo-reset/README.md) — the plan that
  allocated `19310`/`19320` and shipped the manual cross-repo verification step that stands in for
  this registry today.
- [`repo-config.yml`](https://github.com/wahidyankf/beaver-nest/blob/main/repo-config.yml) — the existing precedent for a central, validated,
  machine-readable declaration file in each repo; a candidate host for a per-repo port block.
- [plan-multi-repo-parity-planning workflow](https://github.com/wahidyankf/beaver-nest/blob/main/repo-governance/workflows/plan/plan-multi-repo-parity-planning.md)
  — the established mechanism for keeping a file in step across repos, and the obvious candidate for
  syncing a shared registry.
- [sdlc-gate-registry-enforcement](../../done/2026-08-07__sdlc-gate-registry-enforcement/README.md) —
  the plan that fulfilled and retired the sibling `tri-repo-rhino-cli-byte-identity-gate` idea; its
  `tech-docs.md` §2.8.4 answers the run-location question this brief also faces, for the
  byte-identity check specifically.

## Proposed direction (sketch)

- Enumerate every currently-allocated port across the four repos by reading each repo's
  `docs/reference/monorepo-structure.md`, and record them in one machine-readable file keyed by
  repo, app, and port.
- Add a validator that loads the registry, detects any port claimed twice, and fails with the
  colliding port and both apps' names. A clean run against today's real allocations must report zero
  collisions; a synthetic duplicate injection must report exactly that one collision.
- Candidate homes for the registry: a shared file synced through the existing parity loop, a
  `repo-config.yml` key that each repo validates independently, or a dedicated cross-repo file
  outside the parity loop.
- Candidate homes for the validator: a new `rhino-cli` subcommand, or a lightweight script wired
  into an existing Nx target such as the `repo-config.yml` validation step.

## Rough scope & non-goals

In scope: designing and placing a shared, machine-checkable port registry spanning `ose-public`,
`ose-private`, and `beaver-nest`, plus a validator runnable from any one of them, so a
new app's port allocation is checked automatically instead of by manual prose-table review.

Out of scope:

- Re-litigating `beaver-nest-be`'s (`19320`) or `beaver-nest-fe`'s (`19310`) already-allocated ports.
- Any change to those two apps.
- Changing any app's runtime port configuration — this adds a check, nothing more.

## Risks & open questions

- Where does the registry live? A shared file synced via the parity loop, a `repo-config.yml` key
  each repo checks independently, or a dedicated cross-repo file. A registry spanning repos has no
  single obvious home: the content-parity loop covers only `ose-public` and `ose-private`, and
  `beaver-nest` participates in no cross-repo boundary at all — so none of the three repos is the
  natural owner, and "shared" has no existing location to mean. (open)
- Where does the validator live — a new `rhino-cli` subcommand, or a script wired into an existing
  Nx target? (open)
- What is the enforcement point — CI-blocking on port allocation, or a checker-report warning?
  (open)
- Can a check running in a public repo read `ose-private` at all, and under what auth model? Without
  an answer, any validator either omits a quarter of the registry or cannot run in public CI. (open)
- Does the registry itself go stale the same way the four tables do? Unless entries are derived from
  each app's real configuration rather than hand-maintained, this trades four stale tables for one.
  (open)
- The undecided ownership above is a scheduling risk more than a technical one: the work is small
  once the home is picked, but it cannot start before then.

## What success looks like + promotion signal

Success: allocating a port for a new app in any of the four repos requires zero manual cross-repo
table review, and a collision is reported by an automated check naming both apps rather than by a
developer noticing a bind failure at runtime.

Promotion signal: promote to a `backlog/` plan as soon as either of two things happens — a decision
is reached on the registry's home and the `ose-private` read-access question (the two blockers that
make the rest designable), or a fifth networked app is proposed in any of the four repos, since that
is the first allocation that cannot lean on the "BeaverNest sits alone in the `193xx` band" argument.
An actual observed collision promotes it immediately and unconditionally.
