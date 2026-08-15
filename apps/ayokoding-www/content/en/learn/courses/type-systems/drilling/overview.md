---
title: "Drilling Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

**What does exhaustive matching prove?**

<details><summary>Answer</summary>Every variant the declared type permits has a handling path.</details>

**Why use a newtype rather than an alias?**

<details><summary>Answer</summary>An alias is interchangeable with its representation; a newtype adds
a distinct compiler-recognized meaning.</details>

## Calculation practice

Map increment over Some 4, then bind a division that rejects zero. The final shape records success
or failure without null or exception.

## Scenario judgment

Use a product for a record's fields, a sum for alternate states, and a recursive ADT for nested
syntax. Let a compiler show missing states rather than writing a default that hides them.

## Design exercise

Model an email verification state so an unverified address cannot be passed to a send function.
Add a total match and Result pipeline.

## Automaticity checklist

- [ ] I can choose sum versus product.
- [ ] I can read an inferred polymorphic type.
- [ ] I can distinguish Option from Result.
- [ ] I can explain map versus bind.
- [ ] I can state one cost of a stronger type boundary.

## Why / why not prompts

- Why not encode state as an unconstrained string?
- Why not use a default pattern arm for every union?
- Why not call every generic a typeclass?
- Why does a phantom parameter help units?
- Why is a type assertion not a proof in TypeScript?
