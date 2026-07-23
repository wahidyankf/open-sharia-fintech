---
title: "Overview"
weight: 10000000
date: 2026-05-20T00:00:00+07:00
draft: false
description: "Procedural variant — software architecture patterns through the lens of composition, structural typing, and explicit data flow without inheritance hierarchies. Go (canonical), Rust, and C — the languages whose architecture idioms collapse to neither OOP nor FP."
tags:
  ["software-architecture", "tutorial", "by-example", "code-first", "design-patterns", "procedural", "go", "rust", "c"]
---

**Why a third track?** The OOP and FP tracks teach patterns under two assumptions that Go, Rust, and C all reject. The OOP track assumes inheritance hierarchies as the primary mechanism for polymorphism; the FP track assumes garbage-collected immutable sharing and (mostly) higher-kinded effect abstraction. None of those three assumptions fit Go (no inheritance, no HKT, mutation is normal), Rust (no inheritance, no HKT, ownership replaces GC), or C (no inheritance, no closures, no ADTs). This track teaches the same architectural patterns under the assumptions these three languages actually have: **composition, structural typing, explicit data flow, and (in Rust) ownership-encoded invariants.**

This is an **in-progress track**. The overview, paradigm framing, and language reference are stable; full beginner / intermediate / advanced example content rolls out under the [architecture-procedural-track plan](https://github.com/wahidyankf/ose-public/tree/main/plans/in-progress/architecture-procedural-track).

## What "Procedural" Means Here

The label "procedural" is shorthand for **composition + structural typing + explicit data flow, without inheritance hierarchies**. It is _not_ "C-style legacy code." The three languages on this track share the following structural commitments:

- **No inheritance hierarchies.** Methods belong to types (Go, Rust) or are free functions (C). Polymorphism is achieved via interfaces (Go), traits (Rust), or function pointers (C) — not via subclassing. Rob Pike (Google SPLASH 2012 keynote, ["Go at Google: Language Design in the Service of Software Engineering"](https://go.dev/talks/2012/splash.article)): "Type hierarchies result in brittle code."
- **Composition over inheritance, made structural.** Go and Rust both implement polymorphism without `extends`. Go uses structural typing (a type satisfies an interface by having the right methods — no declaration). Rust uses nominal traits but with `impl Trait for Type` blocks decoupled from type definitions. C uses struct-of-function-pointers (the classic "vtable" trick — see Linux kernel `struct file_operations`).
- **Explicit data flow.** Mutation is allowed (Go, Rust, C) but visible at the type level in Rust (`&mut`), and conventionally explicit in idiomatic Go (return new values rather than mutate). FP's "purity by default" is not enforced; OOP's "encapsulated mutable state" is not idiomatic either.
- **Ownership and lifetimes as a first-class architectural concern (Rust).** Resource cleanup is `Drop`, not `try-finally` or `using`. Move-on-call is the default for non-`Copy` types. This is the **one capability no FP or OOP language teaches** — and it changes how ports, repositories, state machines, and decorators are formulated.

The result: a paradigm that looks _surface-similar_ to OOP (methods, interfaces, encapsulation-by-convention) but that rejects the inheritance backbone OOP architecture depends on — and that uses explicit data flow where FP uses purity.

## Languages on This Track

| Language | Role                              | When this language is canonical                                                                                                                                                                                                                     |
| -------- | --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Go**   | Primary canonical language        | Composition + structural typing, hexagonal architecture (Go's strongest fit), DDD tactical patterns, runtime-checked FSMs, repository / port / adapter wiring                                                                                       |
| **Rust** | Systems-flavoured second language | Typestate FSMs (compile-time-enforced transitions), ownership-driven port design (consume-vs-borrow), zero-cost-abstraction architectural patterns, embedded / systems-level DDD-adjacent modelling                                                 |
| **C**    | Sidebar appearances only          | Function-pointer-table FSMs (Samek, _Practical UML Statecharts in C/C++_); kernel-style polymorphism via struct-of-function-pointers. C has no canonical DDD or hexagonal literature; appears where the procedural idiom is the canonical reference |

**Why not full C coverage?** A systematic literature search returned zero books, papers, or canonical repositories applying DDD (bounded contexts, aggregates, ubiquitous language) to C — the gap is not incidental but reflects DDD's OOP-language origins (Evans 2003). The same gap exists for hexagonal architecture. The one architecture topic with canonical C literature is FSMs (Samek, [_Practical UML Statecharts in C/C++_](https://www.routledge.com/Practical-UML-Statecharts-in-CC-Event-Driven-Programming-for-Embedded-Systems/Samek/p/book/9780750687065), Routledge 2008, 2nd ed.), so C appears there.

## How This Track Differs from OOP and FP

| Concern              | OOP track formulation                                              | FP track formulation                           | Procedural track formulation                                                                                                      |
| -------------------- | ------------------------------------------------------------------ | ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **Polymorphism**     | Inheritance hierarchies + virtual dispatch                         | Sum types + pattern matching, typeclasses      | Structural interfaces (Go), nominal traits without HKT (Rust), function-pointer dispatch (C)                                      |
| **Composition**      | Aggregation, embedding (composition over inheritance)              | Function composition, higher-order functions   | Struct embedding (Go), trait composition (Rust), function pointers in structs (C)                                                 |
| **Ports**            | Interface declarations with `implements`                           | Function-type aliases or records of functions  | Structural interfaces (Go: implicit satisfaction) / nominal traits (Rust: `impl Trait for T`) / struct of function pointers (C)   |
| **Error handling**   | Exceptions or `Optional` / `Either` types                          | `Result<'a, 'e>`, Railway-Oriented Programming | Multi-return values (Go: `(value, error)`), `Result<T, E>` + `?` operator (Rust), out-parameters + sentinel returns (C)           |
| **State management** | Encapsulated mutable fields, getters / setters                     | Immutable records + transition functions       | Mutable struct fields with explicit transition methods (Go), typestate consuming `self` (Rust), explicit state-machine tables (C) |
| **Resource cleanup** | `try`-`finally`, `using`, GC                                       | GC + `use` / scoped resources                  | `defer` (Go), `Drop` (Rust), explicit `free` (C)                                                                                  |
| **DI**               | Spring `@Configuration` + reflection (Java), constructor injection | Partial application, record-of-functions       | Manual constructor wiring in `main.go` / `main.rs`, function-pointer init in C                                                    |

## Authority Basis

- **Rob Pike — _Go at Google: Language Design in the Service of Software Engineering_** ([2012 SPLASH keynote](https://go.dev/talks/2012/splash.article)) — canonical statement of Go's rejection of inheritance hierarchies and embrace of composition + structural typing.
- **Matthew Boyle — _Domain-Driven Design with Golang_** ([Packt, 2022](https://www.oreilly.com/library/view/domain-driven-design-with/9781804613450/)) — dedicated book-length DDD treatment for Go.
- **Three Dots Labs — DDD + CQRS + Clean Architecture in Go** ([threedots.tech](https://threedots.tech/post/ddd-cqrs-clean-architecture-combined/)) — most-cited open-source Go DDD reference implementation.
- **Alistair Cockburn — Hexagonal Architecture** (2005, [alistair.cockburn.us](https://alistair.cockburn.us/hexagonal-architecture)) — explicitly language-agnostic; Go's structural typing fits the original definition more cleanly than Java's nominal `implements`.
- **Hoverbear — Pretty State Machine Patterns in Rust** ([hoverbear.org](https://hoverbear.org/blog/rust-state-machine-pattern/)) — canonical Rust typestate FSM walkthrough.
- **Will Crichton — Type-Driven API Design in Rust** ([willcrichton.net](https://willcrichton.net/rust-api-type-patterns/typestate.html)) — Stanford treatment of typestate as Rust API design discipline.
- **Miro Samek — _Practical UML Statecharts in C/C++_** ([Routledge, 2nd ed. 2008](https://www.routledge.com/Practical-UML-Statecharts-in-CC-Event-Driven-Programming-for-Embedded-Systems/Samek/p/book/9780750687065)) — authoritative C/C++ state-machine treatment.
- **Blandy, Orendorff & Tindall — _Programming Rust_** ([O'Reilly, 3rd ed. 2023](https://www.oreilly.com/library/view/programming-rust-3rd/9781098176228/)) — Ch. 10 (Enums and Patterns) and Ch. 11 (Traits) for paradigm framing.

## Sibling Tracks

- [in-oop-by-example](/en/learn/software-engineering/software-architecture/patterns-and-principles/in-oop-by-example/overview) — Java / Kotlin / C# / TypeScript, inheritance-bearing OOP idioms.
- [in-fp-by-example](/en/learn/software-engineering/software-architecture/patterns-and-principles/in-fp-by-example/overview) — F# / Clojure / TypeScript / Haskell, ADT + higher-order-function FP idioms (Rust also appears here for patterns that translate cleanly via `enum` + `Result`).

## Rollout Plan

Full beginner / intermediate / advanced example content authoring tracks under [`plans/in-progress/architecture-procedural-track/`](https://github.com/wahidyankf/ose-public/tree/main/plans/in-progress/architecture-procedural-track). The overview and paradigm framing on this page are stable and are the canonical reference until the example tiers land.

## Structure of Each Example (Planned)

Every example will follow the same five-part format used in the OOP and FP tracks:

1. **Brief Explanation** — what the pattern or principle addresses (2-3 sentences).
2. **Mermaid Diagram** — visual representation of component relationships, pipelines, or data flow (when appropriate).
3. **Heavily Annotated Code** — parallel tabs showing Go (canonical), Rust where the idiom changes, and C in the few cases where C is canonical (FSM topic only). Annotations use `// =>` notation at 1.0–2.25 comment lines per code line per tab.
4. **Key Takeaway** — the core insight to retain from the example (1-2 sentences).
5. **Why It Matters** — production relevance and real-world impact (50-100 words).
