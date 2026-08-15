---
title: "Drilling Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

**Why use a discriminated union for an AST?**

<details><summary>Answer</summary>It enumerates the legal shapes and lets the compiler check a match
against those shapes.</details>

**What does Result model that Option does not?**

<details><summary>Answer</summary>A successful value or a meaningful failure payload.</details>

## Calculation practice

Evaluate Add(Number 2, Number 3) by recursively evaluating both children, then combine them to 5.

## Scenario judgment

Use a record for named product data, a union for alternative states, and a function when no new
domain shape is required.

## Design exercise

Create a record containing a recursive expression union. Parse a safe integer to Result, evaluate
it with match, and pipe the answer to a formatter.

## Automaticity checklist

- [ ] I can write a total match over a union.
- [ ] I can make absence or failure explicit.
- [ ] I can explain a pipeline without hidden mutation.
- [ ] I can distinguish record copy-update from mutation.
- [ ] I can run an F# project and test from dotnet.

## Why / why not prompts

- Why not encode every AST state as a string?
- Why not use null for expected absence?
- Why does FS0025 matter before a feature ships?
- Why is a pipeline clearer than nested application here?
- Why is a .NET interop call not a reason to abandon functional boundaries?
