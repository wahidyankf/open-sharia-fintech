---
title: "Overview"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

This code-first route prepares an experienced developer to read and change the Dart that appears
in Flutter applications. Every Dart block is self-contained unless it explicitly demonstrates a
CLI command, compiler rejection, or runtime trap. Save a normal block as `example.dart` and run
`dart run example.dart`. Use a current stable SDK; the examples intentionally avoid a brittle SDK
number and third-party runtime packages.

## Prerequisites

This track requires [Object-Oriented Programming Essentials](../../object-oriented-programming-essentials/learning/overview.md)
and [Just Enough TypeScript](../../just-enough-typescript/learning/overview.md). You need the Dart
SDK, a terminal, and confidence running a CLI program. Flutter, Android Studio, and a device
simulator are deliberately deferred to Hybrid App Development.

## Concept map

- **co-01 · Dart CLI** — `dart create`, `run`, `test`, and `compile` scaffold and execute code.
- **co-02 · pub** — `pubspec.yaml` declares package metadata; `dart pub get` resolves it.
- **co-03 · variables** — `var` infers, `final` sets once, `const` is compile-time, and `dynamic` opts out.
- **co-04 · built-in types** — numbers, text, booleans, and typed collections have distinct contracts.
- **co-05 · interpolation** — `$name` and `${expression}` compose readable text.
- **co-06 · sound null safety** — non-null is normal; `T?` records possible absence.
- **co-07 · `late`** — delayed initialization moves the check to runtime.
- **co-08 · null-aware operators** — `?.`, `??`, `??=`, and `!` make absence handling visible.
- **co-09 · functions** — declarations and arrow bodies name reusable behavior.
- **co-10 · named parameters** — callers name optional or required roles.
- **co-11 · optional positional parameters** — brackets provide defaulted positional inputs.
- **co-12 · first-class functions** — functions can be stored, passed, returned, and capture scope.
- **co-13 · collections** — `List`, `Set`, and `Map` hold typed values.
- **co-14 · collection control flow** — `if`, `for`, and spread build literals declaratively.
- **co-15 · generics** — type parameters retain static guarantees in containers and functions.
- **co-16 · classes** — fields, constructors, methods, and `this` model stateful values.
- **co-17 · named constructors** — a name states a distinct construction path.
- **co-18 · factory constructors** — construction may return a cached or alternate instance.
- **co-19 · initializer lists** — final fields initialize before a constructor body.
- **co-20 · getters and setters** — computed or validated properties keep a simple client surface.
- **co-21 · mixins** — reusable behavior joins a class with `with`.
- **co-22 · records** — immutable positional and named aggregates return multiple values.
- **co-23 · patterns** — matching and destructuring expose a value's useful shape.
- **co-24 · `Future`, `async`, `await`** — later values can read in sequential order.
- **co-25 · streams** — sequences of async values can be produced and consumed in order.
- **co-26 · error handling** — `throw`, `try`, `catch`, and `finally` make failure explicit.

## Learning route

- [Beginner examples](./beginner.md) establish the CLI, types, null safety, functions, and literals (1–26).
- [Intermediate examples](./intermediate.md) add declarative collections, modelling, mixins, and errors (27–54).
- [Advanced examples](./advanced.md) apply records, patterns, `Future`, and `Stream` (55–78).
- [Capstone](./capstone/overview.md) consolidates the bounded language surface without becoming a Flutter app.

## Scope boundary

This course stops before Flutter widgets, state-management packages, isolates, FFI, platform
channels, code generation, and package publishing. Completing it means you can follow the Dart
inside Hybrid App Development and make small safe changes; it does not claim complete Dart mastery.
