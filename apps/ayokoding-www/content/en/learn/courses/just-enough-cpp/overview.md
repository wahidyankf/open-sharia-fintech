---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

This C++17 primer follows [Just Enough C](../just-enough-c/learning/overview.md). It teaches the
productive delta over C: objects that own resources through RAII, references and const contracts,
classes, the STL, templates, smart pointers, exceptions, and the CMake/compiler loop. The goal is
to read and safely change a modern C++ codebase, not to survey every C++ feature.

## Prerequisites

The hard prerequisite is [Just Enough C](../just-enough-c/learning/overview.md): pointers, structs,
headers, arrays, `stdio`, and the compile/link loop. Use a macOS or Linux terminal with `g++` or
`clang++`, CMake, and an editor with `clangd` support.

## Scope boundary

Prefer RAII types, STL containers and algorithms, and smart pointers. Raw `new`/`delete`, manual
resource cleanup, deep template metaprogramming, complex inheritance, concurrency design, ABI work,
and platform-specific tooling are outside this bounded surface. Every runnable artifact targets
portable C++17; C++20/23 features are intentionally not a baseline.

Start with [learning](./learning/overview.md), then use [drilling](./drilling/overview.md) to recall
and repair the concepts without copying examples.
