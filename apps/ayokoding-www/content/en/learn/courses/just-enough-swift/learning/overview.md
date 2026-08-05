---
title: "Overview"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

This is a code-first Swift on-ramp for a reader about to enter iOS work. Every fenced block is a
self-contained Swift program unless it explicitly demonstrates a command or a compiler rejection.
Save one as `Example.swift`, run `swift Example.swift`, or compile it with
`swiftc Example.swift -o example && ./example`. Use an unpinned current stable toolchain: version
numbers age; the language contracts in these examples do not depend on one release.

## Prerequisites

This learning track requires the earlier library courses [Object-Oriented Programming Essentials](../../object-oriented-programming-essentials/learning/overview.md)
and [Just Enough Kotlin](../../just-enough-kotlin/learning/overview.md). It assumes a terminal and a
Swift CLI toolchain, but no Xcode or iOS simulator. The iOS course owns those platform tools.

## Concept map

- **co-01 · REPL and `swiftc`** — `swift` evaluates files or expressions; `swiftc` produces an executable.
- **co-02 · `var` and `let`** — choose immutable bindings by default and mark intended reassignment.
- **co-03 · inference and annotations** — inferred types remain static; annotations document contracts.
- **co-04 · basic types** — `Int`, `Double`, `String`, and `Bool` have distinct, explicit operations.
- **co-05 · interpolation** — `\(expression)` makes dynamic text readable.
- **co-06 · optionals** — `T?` models value-or-absence; `nil` is not a hidden sentinel.
- **co-07 · optional binding** — `if let` and `guard let` make the present branch non-optional.
- **co-08 · optional chaining** — `?.` stops a member path safely at absence.
- **co-09 · nil coalescing** — `??` supplies a policy-owned fallback.
- **co-10 · force unwrap** — `!` moves an absence check to a possible runtime trap.
- **co-11 · functions** — `func` declares reusable behavior and `Void` expresses no result.
- **co-12 · argument labels** — calls can name their roles and omit defaulted options.
- **co-13 · closures** — behavior is a value, may trail a call, and may capture context.
- **co-14 · higher-order functions** — `map`, `filter`, and `reduce` transform collections declaratively.
- **co-15 · structs** — structs are copied value types with memberwise construction.
- **co-16 · classes** — classes are reference types with shared identity.
- **co-17 · value vs reference** — copies of a struct diverge; copies of a class reference alias.
- **co-18 · properties** — stored, computed, and lazy properties put state and derivation in clear homes.
- **co-19 · mutating methods** — a struct method changing `self` must say `mutating`.
- **co-20 · enums** — closed cases and raw values model finite choices.
- **co-21 · associated values** — each enum case may carry data appropriate to that state.
- **co-22 · pattern matching** — exhaustive `switch`, binding, and `where` make alternatives explicit.
- **co-23 · protocols** — requirements enable polymorphism without class inheritance.
- **co-24 · protocol extensions** — a protocol can provide shared default behavior.
- **co-25 · generics** — reusable functions and types retain static type guarantees through constraints.
- **co-26 · errors** — `throws`, `do`/`catch`, and `try?` make failure paths visible.
- **co-27 · collections** — arrays, dictionaries, and sets are typed generic containers.
- **co-28 · async/await preview** — `async`, `await`, `Task`, and `async let` express suspension and child work.

## Learning route

- [Beginner examples](./beginner.md) cover the CLI, syntax, optionals, functions, collections, and closures (1–26).
- [Intermediate examples](./intermediate.md) establish value modeling, enums, switching, transformations, and protocols (27–54).
- [Advanced examples](./advanced.md) apply generics, errors, and the intentionally light concurrency preview (55–78).
- [Capstone](./capstone/overview.md) combines the primer without becoming an iOS application.

## Scope boundary

This course stops before Xcode projects, SwiftUI/UIKit, actors, `Sendable`, task cancellation,
isolation, the iOS main actor, and app lifecycle. Its concurrency examples establish the language
spelling and the idea of suspension; iOS App Development turns that foundation into platform practice.
