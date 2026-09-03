---
title: .NET 6 and C# 10 Release
description: OSE Platform compatibility note for the retired .NET 6 and C# 10 baseline
category: explanation
subcategory: prog-lang
tags:
  - c-sharp
  - dotnet
  - release
principles:
  - explicit-over-implicit
  - reproducibility
version: ".NET 6 / C# 10"
lts_until: 2024-11-12
status: retired
created: 2026-09-03
---

# .NET 6 and C# 10 Release

.NET 6 is retained only as historical migration context. Microsoft support ended on 2024-11-12;
new or maintained OSE Platform projects must not select it as a supported target.

Legacy compatibility work must isolate the exception and include an upgrade path to a supported,
repository-approved target framework.

**Upstream references**: [.NET lifecycle](https://learn.microsoft.com/en-us/lifecycle/products/microsoft-net-and-net-core) and [.NET 6 changes](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-6)
