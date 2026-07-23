---
title: "Overview"
date: 2026-05-18T00:00:00+07:00
draft: false
weight: 10000000
description: "Software architecture patterns and principles — SOLID, GRASP, GoF patterns, architectural styles, trade-offs, and real-world decisions taught through 93 annotated examples (85 canonical + 5 FP-native extras + 3 OOP-native extras) across three paradigm tracks (OOP, FP, and Procedural) with explicit paradigm-fit framing"
tags:
  ["software-architecture", "patterns", "principles", "solid", "design-patterns", "tutorial", "clojure", "typescript"]
---

**You can read every chapter of the Gang of Four and still not know when to reach for a Strategy versus a sealed hierarchy, when SOLID becomes over-engineering, or how an Observer differs from a Domain Event in a production codebase.** This section answers those questions through 93 heavily annotated examples — the canonical 85 implemented twice (once in OOP and once in FP), plus 5 FP-native extras (#86–90) and 3 OOP-native extras (#91–93) that exist primarily in one paradigm. Every example is paired across both tracks with explicit paradigm-fit framing, so you see exactly how each pattern and principle changes shape across paradigms.

## What's in this section

Three paradigm tracks covering the same 93-example progression (the OOP and FP tracks are complete; the Procedural track is scaffolded with content rollout in progress):

- [Patterns and Principles in OOP](/en/learn/software-engineering/software-architecture/patterns-and-principles/in-oop-by-example) — Java, Kotlin, C#, and TypeScript examples emphasising classes, interfaces, sealed hierarchies, and pattern-matching
- [Patterns and Principles in FP](/en/learn/software-engineering/software-architecture/patterns-and-principles/in-fp-by-example) — F#, Clojure, TypeScript, and Haskell examples emphasising records, discriminated unions, function composition, and pipeline-shaped data flow; Rust appears here for patterns that translate one-to-one (with explicit concept adjustments for ownership, no-HKT, and the `?` operator)
- [Patterns and Principles in Procedural](/en/learn/software-engineering/software-architecture/patterns-and-principles/in-procedural-by-example) — Go (canonical), Rust, and (rarely) C — composition + structural typing + explicit data flow, without inheritance hierarchies (Pike 2012, Boyle 2022; tier content rollout in progress)

Each example carries the same number and conceptual title across the OOP and FP tracks, enabling direct cross-paradigm comparison. For paradigm-foreign patterns, the "non-native" track shows a stub pointing to the native form rather than a contrived reproduction. The Procedural track teaches the patterns that fit neither OOP (no inheritance) nor FP (no HKT, no persistent shared structures) cleanly.

## Paradigm-fit framing

Many examples carry a **Paradigm Note** banner citing authoritative sources (Norvig 1996, Seemann, Wlaschin, Hickey, Evans, Fowler) explaining whether the pattern is FP-native, OOP-native, or paradigm-neutral. The classification uses four buckets:

- **NEUTRAL** — paradigm-agnostic concept (microservices, hexagonal architecture, distributed tracing). Both tracks teach legitimately.
- **OOP-NATIVE** — pattern emerged from OOP. Norvig classified 16 of 23 GoF patterns as absorbed by FP language features (first-class functions, ADTs, modules). The FP track shows the native FP idiom rather than reproducing the OOP shape.
- **OOP-NATIVE-BUT-TRANSFERABLE** — OOP roots, but the concept transfers cleanly (SOLID, DDD aggregates, Repository). The paradigm note explains the FP encoding.
- **FP-NATIVE** — pattern emerged from or expresses most naturally in FP (Railway-Oriented Programming, Free Monads, Reader/State monads, Event Sourcing fold, FRP, Kleisli composition).

Banners link to the sibling tutorial so you can compare a pattern's expression in both paradigms side-by-side.

## What you will learn

The 93 examples are split into three canonical progressive levels plus two paradigm-native addenda:

- **Beginner (Examples 1–28)**: Foundational principles — SOLID, DRY, KISS, YAGNI, coupling and cohesion, layered architecture, repository pattern, service layer, DTOs, dependency injection.
- **Intermediate (Examples 29–57)**: Composite patterns — Hexagonal Architecture, Clean Architecture, Onion Architecture, GoF behavioural and creational patterns (Strategy, Factory, Builder, Observer, Adapter, Decorator, Command), domain events, event-driven architecture.
- **Advanced (Examples 58–85)**: Distributed systems — CQRS, event sourcing, saga pattern, circuit breaker, bulkhead, microservices boundaries, distributed transactions, eventual consistency, and the production trade-offs that go with each.
- **FP-Native Extras (Examples 86–90)**: Railway-Oriented Programming, Free Monads / Tagless Final, Reader Monad DI, Kleisli composition, State Monad. Full treatment lives in the FP track; the OOP track carries stubs.
- **OOP-Native Extras (Examples 91–93)**: Active Record, GRASP responsibility assignment, Singleton with FP counterexample. Full treatment lives in the OOP track; the FP track carries stubs.

## Structure of each example

Every example follows the same five-part format:

1. **Brief Explanation** — what the pattern or principle addresses and why it matters (2-3 sentences)
2. **Mermaid Diagram** — visual representation of component relationships, layers, or data flow (when appropriate)
3. **Heavily Annotated Code** — implementation with `// =>` comments documenting each architectural decision and its trade-offs
4. **Key Takeaway** — the core insight to retain (1-2 sentences)
5. **Why It Matters** — production relevance and real-world impact (50-100 words)

## How to use this section

Start at the level that matches your current understanding. If you are new to architectural patterns, work through Beginner end-to-end before moving on. If you already ship layered services and want to deepen your pattern vocabulary, jump to Intermediate. If you are wrestling with distributed-systems trade-offs, start at Advanced.

Pick the paradigm track that matches the language you write daily — but consider reading the matching example in the other paradigm whenever a pattern feels awkward. Many "OOP patterns" disappear in FP (the Strategy pattern collapses to a function parameter), and many "FP patterns" become heavier in OOP (immutable updates require `with` expressions or builder copies). Seeing both forms makes the underlying principle visible.

## Why three parallel tracks

A Strategy pattern in Java is an interface plus implementations plus a constructor injection. The same Strategy in F# is a function value passed as a parameter; in Clojure it is a higher-order function; in Go it is a function value or one-method interface satisfied structurally; in Rust it is a `dyn Fn` or trait object. The intent — swap algorithms without touching call sites — is identical; the syntax difference is paradigm-shaped, not principle-shaped. Reading all three forms in parallel teaches the principle directly instead of memorising one syntactic costume of it. The Procedural track exists because Go and Rust reject both OOP inheritance (so the OOP track misrepresents them) and FP's higher-kinded effect abstraction (so the FP track misrepresents them too); they deserve their own honest formulation.

## What this section is not

- **Not a language tutorial.** You should already be comfortable writing classes in Java/Kotlin/C#/TypeScript (for the OOP track) or functions and records in F#/Clojure/TypeScript (for the FP track).
- **Not a complete reference of every pattern in existence.** It covers the 93 examples that matter most in modern enterprise codebases (85 canonical + 8 paradigm-native extras). Specialised patterns (parser combinators, GoF Flyweight, Memento) are mentioned only when they illustrate a broader principle.
- **Not framework-specific.** Examples lean on standard libraries and minimal framework usage so the architectural intent stays visible. Framework-specific wiring (Spring beans, ASP.NET DI containers, Giraffe pipelines) shows up only in the [Cases](/en/learn/software-engineering/software-architecture/by-example/cases) section.
