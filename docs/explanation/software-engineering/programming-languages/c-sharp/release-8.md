---
title: .NET 8 and C# 12 Release
description: OSE Platform compatibility note for .NET 8 LTS and C# 12
category: explanation
subcategory: prog-lang
tags:
  - c-sharp
  - dotnet
  - release
principles:
  - explicit-over-implicit
  - reproducibility
version: ".NET 8 / C# 12"
lts_until: 2026-11-10
status: supported
created: 2026-09-03
---

# .NET 8 and C# 12 Release

.NET 8 is an LTS release supported through 2026-11-10. It remains valid for existing projects that
pin it explicitly, but the repository's actual target-framework declarations are authoritative.

Relevant platform capabilities include C# 12, Native AOT improvements, keyed dependency injection,
and `TimeProvider` for deterministic time-dependent tests.

**Upstream references**: [.NET lifecycle](https://learn.microsoft.com/en-us/lifecycle/products/microsoft-net-and-net-core) and [.NET 8 changes](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-8/overview)
