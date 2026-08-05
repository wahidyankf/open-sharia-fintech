---
title: "Overview"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

Swift makes the safe choice feel ordinary: structs copy by default, optionals make absence visible,
and enums can carry the exact data each state needs. This primer teaches just enough Swift to be
productive in the later iOS App Development course: syntax, modeling, protocols, closures, error
handling, and one carefully bounded `async`/`await` preview.

It is a language primer, not an iOS course or a complete Swift reference. Xcode, SwiftUI, UIKit,
actors, isolation, package design, and production concurrency belong in the platform course or later
study. Here, every runnable example starts from `swift` or `swiftc`, so the language stays visible.

## Prerequisites

Complete [Object-Oriented Programming Essentials](../object-oriented-programming-essentials/learning/overview.md)
for classes and types, then [Just Enough Kotlin](../just-enough-kotlin/learning/overview.md) for the
transferable intuition that absence should be explicit. You need a macOS Swift toolchain or a current
Swift toolchain on Linux; Xcode is not required yet.

## What you will build

The learning track contains 78 small annotated programs. They progress from compiling a file and
unwrapping an optional to value-oriented models, protocols, generic constraints, errors, and an async
CLI capstone. Save a standard example as `Example.swift` and run `swift Example.swift`, or compile it
with `swiftc Example.swift -o example && ./example`.

Start with the [learning overview](./learning/overview.md), execute an example when its behavior is
not obvious, then use the [drilling track](./drilling/overview.md) to practise choosing constructs
without a prompt.

## Read more

- [The Swift Programming Language](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/)
  is the official, continuously maintained language book.
- [Swift.org documentation](https://www.swift.org/documentation/) is the official toolchain and language hub.
