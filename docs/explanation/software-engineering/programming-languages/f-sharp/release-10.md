---
title: F# 10 and .NET 10 Release
description: OSE Platform compatibility note for the current F# 10 and .NET 10 LTS target
category: explanation
subcategory: prog-lang
tags:
  - f-sharp
  - dotnet
  - release
principles:
  - explicit-over-implicit
  - reproducibility
version: "F# 10 / .NET 10"
lts_until: 2028-11-14
status: current
created: 2026-09-03
---

# F# 10 and .NET 10 Release

F# 10 ships with .NET 10 and is the current OSE Platform target for new F# projects. .NET 10 is an
LTS release supported through 2028-11-14. Projects must pin the SDK and declare `net10.0` explicitly.

Relevant changes include scoped warning control, per-accessor property visibility, improved
computation expressions, clearer diagnostics, trimming improvements, and compiler performance work.

**Upstream references**: [F# 10 changes](https://learn.microsoft.com/en-us/dotnet/fsharp/whats-new/fsharp-10) and [.NET support policy](https://dotnet.microsoft.com/en-us/platform/support/policy)
