---
title: .NET 9 and C# 13 Release
description: OSE Platform compatibility note for .NET 9 STS and C# 13
category: explanation
subcategory: prog-lang
tags:
  - c-sharp
  - dotnet
  - release
principles:
  - explicit-over-implicit
  - reproducibility
version: ".NET 9 / C# 13"
lts_until: not-applicable
status: supported-sts
created: 2026-09-03
---

# .NET 9 and C# 13 Release

.NET 9 is a standard-term-support release, not an LTS baseline. Use it only where the owning
project deliberately accepts its shorter support window and pins the SDK and target framework.

Relevant changes include C# 13, `Task.WhenEach`, new LINQ aggregation methods, and SDK workload sets.

**Upstream references**: [.NET lifecycle](https://learn.microsoft.com/en-us/lifecycle/products/microsoft-net-and-net-core) and [.NET 9 changes](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-9/overview)
