---
title: "Overview"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

## Prerequisites

- **Required course**: [Just Enough C#](../just-enough-csharp/learning/overview.md) supplies the C#
  syntax, LINQ, tasks, and async/await used here. This course uses those tools to build a Windows
  application; it does not reteach the language.
- **Tools**: a Windows machine, the .NET SDK, and Visual Studio with a Windows desktop workload for
  WPF/WinForms or the Windows App SDK tooling for WinUI 3. The headless probes run with .NET 10.

## Why this exists

A desktop app must keep its UI responsive while it loads data, remembers state, and handles failure.
The durable pattern is MVVM plus async work: keep view state and commands testable outside the window,
then use bindings and the dispatcher to let a Windows host present them safely.

> **Scope boundary — Windows application development vs. Just Enough C#.** Just Enough C# owns
> language syntax, LINQ, asynchronous primitives, and the .NET runtime model. This course owns their
> application: XAML hosts, binding, MVVM, dispatcher affinity, Windows persistence, packaging, and
> desktop-test strategy. It deliberately assumes the primer instead of duplicating it.

## Course register

- **Learning** contains 78 source-matched, runnable examples: 26 Beginner, 28 Intermediate, and
  24 Advanced examples, followed by a WPF MVVM capstone with cancellation, progress, SQLite, settings,
  and xUnit tests.
- **Drilling** uses five fixed sections: recall, applied scenarios, hands-on katas, self-check, and
  elaborative interrogation.

## Accuracy boundary

Windows desktop stacks and package versions evolve independently. The examples name WinUI 3, WPF,
WinForms, the Windows App SDK, Microsoft.Data.Sqlite, and MSIX without pinning a moving framework or
package version; use the current Windows SDK and the current compatible package version when restoring
the capstone on Windows.

Next: [Learning Overview](./learning/overview.md) →
