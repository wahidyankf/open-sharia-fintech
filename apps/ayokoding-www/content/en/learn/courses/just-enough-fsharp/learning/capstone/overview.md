---
title: "Capstone: Expression Evaluator"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Run the small evaluator with dotnet run from code. It combines immutable bindings, a recursive
discriminated union, exhaustive pattern matching, a Result error path, and a pipeline.

The source includes a built-in assertion function so its expected behaviors are executable without
a third-party dependency. Add a separate dotnet test project when the evaluator grows beyond this
primer boundary.
