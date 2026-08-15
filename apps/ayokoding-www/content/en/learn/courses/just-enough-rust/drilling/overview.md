---
title: "Drilling Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Use this five-section loop after running the examples. Answer from memory first, then run only the
small binary that resolves uncertainty.

## 1. Recall

**What owns a `String` after assignment?**

<details><summary>Answer</summary>The destination binding owns it; the source cannot be used unless the value was cloned or borrowed.</details>

**What does `Option<T>` replace?**

<details><summary>Answer</summary>A nullable-value convention: `Some(T)` is present and `None` is absent.</details>

## 2. Explain the Rules

Explain aloud: “many `&T` or one `&mut T`, never both at the same time.” Then explain why `?`
returns early rather than swallowing an error.

## 3. Predict Before Running

Predict `ex-27`, `ex-37`, `ex-57`, and `ex-67` before running them. For each, name the owner,
possible error path, or `match` arm responsible for the output.

## 4. Repair Katas

1. Replace an unnecessary `clone` with a shared borrow.
2. Change a nullable sentinel into `Option` and match both cases.
3. Return `Result` from a parser and propagate it with `?`.
4. Add the missing arm when an enum gains `Stopped`.
5. Constrain a generic function with only the trait it actually uses.

## 5. Self-Check and Transfer

- [ ] I can create, run, build, and test a Cargo binary.
- [ ] I can explain a move, shared borrow, mutable borrow, and an explicit lifetime relationship.
- [ ] I can model missing and invalid data with `Option`, `Result`, `?`, and exhaustive `match`.
- [ ] I can use a trait-bound generic and decide whether a collection owns or borrows its values.
- [ ] I know that concurrency, FFI, `unsafe`, and platform APIs begin in Modern System Programming.
