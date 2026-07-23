---
title: "Overview"
weight: 10000003
date: 2026-05-20T00:00:00+07:00
draft: false
description: "Procedural variant of the production wiring case — Go (canonical, chi + database/sql + Three Dots Labs reference) and Rust (axum + sqlx + tokio) — showing how C4, DDD, Hexagonal Architecture, and FSM compose in real codebases without inheritance hierarchies or framework-managed DI containers"
tags:
  [
    "cases",
    "in-procedural",
    "c4-model",
    "ddd",
    "hexagonal-architecture",
    "finite-state-machine",
    "go",
    "rust",
    "procedural",
  ]
---

**You have finished the by-example tracks for C4, DDD, Hexagonal Architecture, and FSM in the procedural track. Now the question is: how do they all wire together in a real production Go or Rust codebase that ships?** This case answers that question using Go / chi / database/sql (canonical, with [Three Dots Labs](https://threedots.tech/post/ddd-cqrs-clean-architecture-combined/) as the reference architecture and [Boyle's _Domain-Driven Design with Golang_](https://www.oreilly.com/library/view/domain-driven-design-with/9781804613450/) as the book-length anchor) and Rust / axum / sqlx / tokio variants, running against the same hypothetical Procure-to-Pay procurement platform backend.

This is an **in-progress track**. The overview and paradigm framing on this page are stable. Full guide content rolls out under the [architecture-procedural-track plan](https://github.com/wahidyankf/ose-public/tree/main/plans/in-progress/architecture-procedural-track).

## How Procedural Wiring Differs From OOP and FP Cases

The OOP case (Spring Boot / ASP.NET Core / NestJS) and the FP case (Giraffe / Ring / Hono / Servant) both depend on framework-managed glue:

- **OOP case**: `@Configuration` reflection-driven DI, `@RestController` for HTTP routing, `@Transactional` for transaction boundaries, framework-managed JPA / EF Core / TypeORM repositories.
- **FP case**: Giraffe / Hono / Servant routing DSLs, composition root assembling records-of-functions, partial application as DI.

The procedural case is different:

- **Go composition root is `main.go`** — explicit constructor wiring, step-debuggable, no annotations, no reflection. The wiring is **plain code**.
- **Rust composition root is `main.rs`** — same pattern; `Arc<dyn Trait + Send + Sync>` for shared port handles across the tokio async runtime.
- **HTTP primary adapter** is a thin handler — Go: chi or echo router function; Rust: axum extractor-based handler. No framework annotations on the domain.
- **Repository adapter** uses `database/sql` (Go) or `sqlx` (Rust). Both are compile-time-checked but lighter-weight than ORMs.
- **Transaction boundaries** are explicit — `tx, _ := db.Begin(); defer tx.Rollback(); ...; tx.Commit()` (Go) or `let tx = pool.begin().await?; ...; tx.commit().await?` (Rust). No `@Transactional` annotation.
- **Async / concurrency** — Go's goroutines + channels (CSP) or Rust's tokio + async/await; neither is "monadic" in the FP sense.

## Authority Basis

- **Three Dots Labs — [DDD + CQRS + Clean Architecture in Go](https://threedots.tech/post/ddd-cqrs-clean-architecture-combined/)** — the most-cited open-source Go production reference. Combines DDD, CQRS, clean architecture, hexagonal in a real codebase.
- **Matthew Boyle — [_Domain-Driven Design with Golang_](https://www.oreilly.com/library/view/domain-driven-design-with/9781804613450/)** (Packt, 2022) — book-length Go-DDD treatment with companion repo at [github.com/PacktPublishing/Domain-Driven-Design-with-GoLang](https://github.com/PacktPublishing/Domain-Driven-Design-with-GoLang).
- **Alistair Cockburn — [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture)** (2005) — original, explicitly language-agnostic; Go's structural typing fits the definition more cleanly than Java's nominal `implements`.
- **Rob Pike — [Go at Google: Language Design in the Service of Software Engineering](https://go.dev/talks/2012/splash.article)** (2012 SPLASH keynote) — canonical statement of Go's rejection of inheritance hierarchies in favour of composition + structural typing.

## How the Four Families Compose in the Procedural Codebase

The four architecture pattern families slot together at different levels of the codebase. Go is the canonical implementation; the structural mapping applies to Rust as well:

| Family  | Go (canonical)                                                                                                                                  | Rust variant                                                                                                                                             |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **C4**  | Diagram artifacts checked in alongside source; package names match C4 Component names                                                           | Same; module paths (PascalCase) match C4 Component names                                                                                                 |
| **DDD** | Top-level packages per bounded context (`procurementplatformbe/purchasing`, etc.); aggregates as plain structs with explicit transition methods | Top-level modules per bounded context; aggregates as struct types; lifecycle as typestate or as `enum`-with-`match`                                      |
| **Hex** | `domain/` → `app/` (ports + services) → `adapter/{in,out}/` → `main.go`                                                                         | `domain/` → `app/` → `adapter/{in,out}/` → `main.rs`                                                                                                     |
| **FSM** | Aggregate state as a field (`int` / `string`) with switch-dispatch transitions; looplab/fsm for declarative workflow machines                   | Aggregate state as typestate (different struct type per state) — compile-time-enforced legal transitions; or `enum` for simpler runtime-checked machines |

## Running Domain — Procure-to-Pay Procurement Platform

Same `procurement-platform-be` Procure-to-Pay domain as the OOP and FP cases. Bounded contexts: `purchasing`, `supplier`, `receiving`, `invoicing`, `payments`, `murabaha-finance`. Cross-context events: `PurchaseOrderIssued`, `PurchaseOrderAcknowledged`, `GoodsReceived`, `InvoiceMatched`, `PaymentDisbursed`, `SupplierApproved`.

## What This Case Will Cover

**Beginner — one context = one hexagon (Go canonical, Rust where it differs):**

- Per-context package layout (`procurementplatformbe/purchasing/{domain,app,adapter}`).
- Domain types as plain Go structs / Rust structs with no framework imports.
- Application service function signatures taking small port interfaces.
- Output port as a one-method Go `interface` / Rust `trait`.
- HTTP primary adapter — chi handler / axum handler.
- Composition root in `main.go` / `main.rs` — explicit constructor wiring.

**Intermediate — wiring real infrastructure:**

- Postgres repository adapter using `database/sql` (Go) or `sqlx` (Rust).
- In-memory test adapter — struct with `map[ID]Entity` field.
- Domain event publisher port; outbox adapter pattern for at-least-once delivery.
- Cross-context Anti-Corruption Layer as a translator package/module.
- Contract code generation from OpenAPI spec.

**Advanced — production patterns:**

- docker-compose integration harness (Go: testcontainers-go; Rust: testcontainers-rs).
- Database migrations — Go: [golang-migrate](https://github.com/golang-migrate/migrate); Rust: [sqlx-cli](https://github.com/launchbadge/sqlx/tree/main/sqlx-cli).
- Banking port and payment adapter; retry decorator; circuit-breaker decorator.
- End-to-end domain event flow across four contexts.
- OpenTelemetry observability adapter — Go: [otel-go](https://github.com/open-telemetry/opentelemetry-go); Rust: [opentelemetry-rust](https://github.com/open-telemetry/opentelemetry-rust).
- `murabaha-finance` optional bounded context for Sharia-compliant procurement financing.
- Hexagonal anti-patterns (domain importing framework packages; application service instantiating adapters directly).
- Kubernetes deployment topology, configuration adapter at the deploy seam, background job adapter.

## Sibling Cases

- [In OOP](/en/learn/software-engineering/software-architecture/by-example/cases/in-oop/overview) — Java 25 / Spring Boot 4 (canonical), Kotlin, C# / ASP.NET Core, TypeScript / NestJS.
- [In FP](/en/learn/software-engineering/software-architecture/by-example/cases/in-fp/overview) — F# / Giraffe (canonical), Clojure, TypeScript / Hono, Haskell / Servant.

Comparing the three side-by-side is the fastest way to see what changes when you swap framework-driven OOP wiring → records-of-functions FP wiring → explicit-main procedural wiring.

## Rollout Plan

Full beginner / intermediate / advanced guide authoring tracks under [`plans/in-progress/architecture-procedural-track/`](https://github.com/wahidyankf/ose-public/tree/main/plans/in-progress/architecture-procedural-track).
