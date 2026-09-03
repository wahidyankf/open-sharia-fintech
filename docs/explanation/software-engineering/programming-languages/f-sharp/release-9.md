---
title: F# 9 and .NET 9 Release
description: OSE Platform compatibility note for F# 9 and .NET 9 STS
category: explanation
subcategory: prog-lang
tags:
  - f-sharp
  - dotnet
  - release
principles:
  - explicit-over-implicit
  - reproducibility
version: "F# 9 / .NET 9"
lts_until: not-applicable
status: strategy-target
created: 2026-09-03
---

# F# 9 and .NET 9 Release

F# 9 ships with .NET 9, a standard-term-support release, and is the README's documented feature
target. Projects selecting it must deliberately accept that support model and pin both the SDK and
target framework.

Relevant changes include nullable reference type integration, additional discriminated-union
properties, and standard-library and tooling improvements.

**Upstream references**: [F# 9 changes](https://learn.microsoft.com/en-us/dotnet/fsharp/whats-new/fsharp-9) and [.NET lifecycle](https://learn.microsoft.com/en-us/lifecycle/products/microsoft-net-and-net-core)
