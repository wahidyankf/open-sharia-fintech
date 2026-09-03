---
title: F# 6 and .NET 6 Release
description: OSE Platform compatibility note for the retired F# 6 and .NET 6 baseline
category: explanation
subcategory: prog-lang
tags:
  - f-sharp
  - dotnet
  - release
principles:
  - explicit-over-implicit
  - reproducibility
version: "F# 6 / .NET 6"
lts_until: 2024-11-12
status: retired
created: 2026-09-03
---

# F# 6 and .NET 6 Release

F# 6 with .NET 6 is retained as historical migration context. .NET 6 support ended on 2024-11-12,
so maintained OSE Platform projects must use a supported target instead.

The release introduced native `task {}` expressions and language improvements that remain available
when code moves to newer F# and .NET versions.

**Upstream references**: [F# 6 changes](https://learn.microsoft.com/en-us/dotnet/fsharp/whats-new/fsharp-6) and [.NET lifecycle](https://learn.microsoft.com/en-us/lifecycle/products/microsoft-net-and-net-core)
