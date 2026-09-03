---
title: F# 8 and .NET 8 Release
description: OSE Platform compatibility note for F# 8 and .NET 8 LTS
category: explanation
subcategory: prog-lang
tags:
  - f-sharp
  - dotnet
  - release
principles:
  - explicit-over-implicit
  - reproducibility
version: "F# 8 / .NET 8"
lts_until: 2026-11-10
status: supported
created: 2026-09-03
---

# F# 8 and .NET 8 Release

F# 8 ships with the .NET 8 LTS toolchain, which is supported through 2026-11-10. Existing projects
may retain this target while supported, but checked-in SDK and target-framework declarations remain
authoritative.

The release includes shorthand lambda syntax, improved inference, and stronger tail-call validation.

**Upstream references**: [F# 8 changes](https://learn.microsoft.com/en-us/dotnet/fsharp/whats-new/fsharp-8) and [.NET lifecycle](https://learn.microsoft.com/en-us/lifecycle/products/microsoft-net-and-net-core)
