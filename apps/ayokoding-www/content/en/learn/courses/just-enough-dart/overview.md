---
title: "Overview"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

Dart gives Flutter a compact, statically typed language with sound null safety and first-class
asynchrony. This primer teaches just enough Dart to be productive in the later Hybrid App
Development course: the CLI, types, collections, classes and mixins, and the `Future` and `Stream`
spelling that Flutter code uses every day.

It is a language primer, not a complete Dart reference or a Flutter course. Isolates, FFI,
macros, package publishing, code generation, and framework widgets stay outside this boundary so
the language remains visible before the platform adds its own vocabulary.

## Prerequisites

Complete [Object-Oriented Programming Essentials](../object-oriented-programming-essentials/learning/overview.md)
for classes, interfaces, and inheritance, then [Just Enough TypeScript](../just-enough-typescript/learning/overview.md)
for static types and explicit nullability. Install a current stable Dart SDK (a Flutter installation
also provides it) and use a terminal plus an editor with Dart language support.

## What you will build

The learning track contains 78 small, annotated Dart examples. Save a normal block as
`example.dart` and run `dart run example.dart`; compiler-rejection and runtime-trap lines stay
commented until you deliberately enable them. The light capstone is a console availability report
that combines nullable lookup, a mixin, generic collection, `Future`, `Stream`, and `dart test`.

Start with the [learning overview](./learning/overview.md), then use the
[drilling track](./drilling/overview.md) to practise choosing constructs without a worked answer.

## Read more

- [Dart language tour](https://dart.dev/language) is the official language introduction.
- [Dart CLI documentation](https://dart.dev/tools/dart-tool) documents `create`, `run`, `test`, and `compile`.
- [Dart language specification](https://dart.dev/resources/language/spec) is the formal, in-progress
  reference; use the language tour for current feature guidance.
