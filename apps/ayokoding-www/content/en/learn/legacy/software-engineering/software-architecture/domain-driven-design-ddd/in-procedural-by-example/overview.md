---
title: "Overview"
weight: 10000002
date: 2026-05-20T00:00:00+07:00
draft: false
description: "Procedural variant — Domain-Driven Design through the lens of composition, structural typing, and explicit data flow without inheritance. Go (canonical, with Boyle 2022 and Three Dots Labs as reference); Rust where ownership reshapes aggregate modelling; C deliberately out-of-scope."
tags: ["ddd", "domain-driven-design", "tutorial", "by-example", "procedural", "go", "rust"]
---

**Want to apply DDD without classes, inheritance, or aggregate root encapsulation patterns?** This tutorial teaches DDD tactical and strategic patterns under the assumptions Go and Rust make: composition + structural typing + explicit data flow, no inheritance hierarchies, and (in Rust) ownership-encoded aggregate invariants.

This is an **in-progress track**. The overview and paradigm framing on this page are stable. Full beginner / intermediate / advanced example content rolls out under the [architecture-procedural-track plan](https://github.com/wahidyankf/ose-public/tree/main/plans/in-progress/architecture-procedural-track).

## Why a Procedural DDD Track

DDD was formulated in 2003 (Evans, _Domain-Driven Design_) against Java — explicitly OOP, explicitly class-based, explicitly inheritance-tolerant. The OOP track on this site teaches that canonical formulation. The FP track teaches DDD reformulated under functional programming (Wlaschin, _Domain Modeling Made Functional_) — types are the design, transitions are pure functions, effects live at the edges.

Go fits **neither** track cleanly:

- It is not OOP — no inheritance. Aggregate roots in Go are plain structs with explicit transition methods, not classes encapsulating private state behind getters.
- It is not FP — `Result<T, E>` does not exist (multi-return is the idiom), there are no ADTs (struct + type-switch is the substitute), there is no immutable-by-default discipline.

Rust is closer to FP on this axis (ADTs via `enum`, `Result<T, E>` natively, immutable by default) but adds **ownership as a domain-modelling tool** that no FP language offers — aggregate state transitions can be encoded as functions that consume the previous state, making "use the old state after transition" a compile error rather than a convention.

Authoritative references for Go DDD:

- Matthew Boyle — [_Domain-Driven Design with Golang_](https://www.oreilly.com/library/view/domain-driven-design-with/9781804613450/) (Packt, 2022) — book-length treatment with code repository at [github.com/PacktPublishing/Domain-Driven-Design-with-GoLang](https://github.com/PacktPublishing/Domain-Driven-Design-with-GoLang).
- Three Dots Labs — [DDD + CQRS + Clean Architecture in Go](https://threedots.tech/post/ddd-cqrs-clean-architecture-combined/) — most-cited open-source reference implementation combining DDD, CQRS, and clean architecture.

## What This Tutorial Will Cover

**Tactical patterns in Go (canonical) / Rust:**

- **Ubiquitous language as Go package naming + Rust module naming** — same discipline as OOP/FP tracks, different surface.
- **Value objects** — Go: small structs with constructor functions returning `(Value, error)`. Rust: tuple structs or records with `impl` blocks; smart constructors return `Result<Value, Error>`.
- **Entities** — Go: structs with ID field, exported methods for transitions, unexported fields for invariants. Rust: structs with private fields, transitions consume `self` and return a new state type (typestate) where the lifecycle is sealed.
- **Aggregates** — Go: package as aggregate boundary; only the aggregate root struct's methods are exported; collection invariants enforced via methods. Rust: ownership across the aggregate; child entities owned by root; no external `&mut` references.
- **Repositories** — Go: small interfaces (one to three methods); concrete adapter implements implicitly. Rust: `trait Repository { async fn save(&self, agg: &Aggregate) -> Result<(), Error>; }`.
- **Domain services** — Go: package-level functions or interface satisfied by stateless struct. Rust: `impl` block functions on a stateless struct.
- **Domain events** — Go: structs; published via channel or interface-method call. Rust: `enum` variants representing event types.
- **Application services** — Go: function or method on a service struct, takes repository interfaces as constructor parameters.

**Strategic patterns:**

- **Bounded contexts as Go packages / Rust modules** — single-import-path boundary, public surface controlled by capitalisation (Go) or `pub` (Rust).
- **Context maps** — explicit cross-package types translated at the boundary via dedicated translator functions.
- **Anti-Corruption Layer** — a dedicated translator package/module that consumes external DTOs and produces internal domain types.

**Sharia procurement extension (`murabaha-finance`)**:

- Same Sharia-compliant Murabaha contract modelling as the OOP and FP tracks, but with Go-idiomatic state machine using struct + method dispatch, or Rust typestate consuming `self`.

## Running Domain

Same `procurement-platform-be` Procure-to-Pay domain as the OOP and FP tracks (purchasing, supplier, receiving, invoicing, payments, murabaha-finance bounded contexts). Comparing the three tracks side-by-side is the fastest way to see what changes when DDD assumptions shift from OOP class hierarchies → FP ADT + pure transitions → procedural struct + explicit data flow.

## What This Tutorial Does NOT Cover

- **C**: a systematic literature search returned zero books or canonical repositories applying DDD to C. The gap is not incidental — DDD's tactical patterns assume language features (encapsulation, methods on types, polymorphism via interfaces or traits) that C does not provide as primitives. C appears in the FSM track (Samek) where it has canonical literature; not here.
- **Language tutorials**: Go and Rust each have their own by-example tutorials for language fundamentals.
- **Deep DDD theory**: read the [paradigm-agnostic DDD overview](/en/learn/software-engineering/software-architecture/domain-driven-design-ddd/overview) and Evans's _Domain-Driven Design_ (Addison-Wesley, 2003) for foundations.

## Sibling Tutorials

- [DDD By Example in OOP](/en/learn/software-engineering/software-architecture/domain-driven-design-ddd/in-oop-by-example/overview) — Java 21+ (canonical), Kotlin, C#, TypeScript.
- [DDD By Example in FP](/en/learn/software-engineering/software-architecture/domain-driven-design-ddd/in-fp-by-example/overview) — F# (canonical), Clojure, TypeScript, Haskell.

## Rollout Plan

Full beginner / intermediate / advanced example content authoring tracks under [`plans/in-progress/architecture-procedural-track/`](https://github.com/wahidyankf/ose-public/tree/main/plans/in-progress/architecture-procedural-track).

## Structure of Each Example (Planned)

Every example will follow the same five-part format used in the OOP and FP tracks:

1. **Brief Explanation** — what DDD concept the example demonstrates (2-3 sentences).
2. **Optional Diagram** — Mermaid diagram for context maps, aggregate boundaries, state transitions.
3. **Heavily Annotated Code** — parallel tabs: Go (canonical), Rust where the ownership story changes the modelling. `// =>` annotations at 1.0–2.25 comment lines per code line.
4. **Key Takeaway** — the core DDD principle (1-2 sentences).
5. **Why It Matters** — real-world business impact (50-100 words).
