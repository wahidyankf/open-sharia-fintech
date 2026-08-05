---
title: "Catalog Report CLI"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

Build a compact catalog report, not a Windows project. The program proves nullable-aware lookup,
records, a LINQ query, an interface seam, and one awaited operation.

## Run and verify

```bash
dotnet run --project code/CatalogReport/CatalogReport.csproj
dotnet test code/CatalogReport.Tests/CatalogReport.Tests.csproj
```

The program prints a sorted report and reports a missing requested ID as `unavailable`. The test
project uses `Microsoft.NET.Test.Sdk`, `xunit`, and `xunit.runner.visualstudio` package references to
verify both behaviors through `dotnet test`.

## Why this capstone stays small

A desktop UI would add platform APIs before the core language choices are visible. This console
program keeps those choices inspectable: nullable types represent absence, a record models data,
LINQ creates a report, an interface makes the source replaceable, and `await` keeps the asynchronous
boundary honest.
