---
title: .NET 10 and C# 14 Release
description: OSE Platform compatibility note for the current .NET 10 LTS and C# 14 target
category: explanation
subcategory: prog-lang
tags:
  - c-sharp
  - dotnet
  - release
principles:
  - explicit-over-implicit
  - reproducibility
version: ".NET 10 / C# 14"
lts_until: 2028-11-14
status: current
created: 2026-09-03
---

# .NET 10 and C# 14 Release

.NET 10 is the current LTS target for OSE Platform .NET projects and is supported through
2028-11-14. Projects must pin the SDK and declare `net10.0` (or the approved platform-specific
variant) explicitly.

Relevant changes include C# 14, runtime and Native AOT improvements, and expanded SDK tooling.

**Upstream references**: [.NET lifecycle](https://learn.microsoft.com/en-us/lifecycle/products/microsoft-net-and-net-core) and [.NET 10 changes](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-10/overview)
