---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

This active-recall companion asks you to answer first, then write the smallest program that proves
the answer.

## Recall Q&A

**Q1. What is RAII?**

<details><summary>Answer</summary>A type acquires a resource during construction and releases it in its destructor, so scope determines lifetime even during exception unwinding.</details>

**Q2. When should a function take `const T&`?**

<details><summary>Answer</summary>When it needs to borrow a potentially expensive object without copying or mutating it. Use a value when the function must own or intentionally copy the argument.</details>

**Q3. What is the normal modern-C++ default for heap ownership?**

<details><summary>Answer</summary>`std::unique_ptr`, created with `std::make_unique`; use `shared_ptr` only for genuine shared ownership and use `weak_ptr` for non-owning back-links.</details>

**Q4. Why do templates commonly live in headers?**

<details><summary>Answer</summary>The compiler needs the complete template definition at each instantiation point, unlike a non-template function that can be separately compiled and linked.</details>

## Applied problems

**AP1. A lookup may not find a configuration key. Choose `optional`, an exception, or a sentinel.**

<details><summary>Answer</summary>Use `std::optional` for expected, locally handled absence; use an exception for exceptional invalid state; avoid magic sentinels.</details>

**AP2. A `vector<unique_ptr<Base>>` owns plugin objects. How should a caller inspect them?**

<details><summary>Answer</summary>Borrow a `const Base&` or `const Base*`; do not copy or release the `unique_ptr` merely to call a virtual method.</details>

## Code katas

1. Replace a raw `new`/`delete` pair with `std::unique_ptr` and `std::make_unique`.
2. Add a `const` accessor to a class whose representation must remain private.
3. Convert a hand-written loop over a vector into `std::find` or `std::transform`.
4. Return `std::optional<int>` instead of `-1` from a parser where `-1` can be valid.
5. Add a CTest executable to a two-target CMake project.

## Self-check checklist

- [ ] I can compile a C++17 source with warnings enabled and read every warning.
- [ ] I can explain reference borrowing, value ownership, and `unique_ptr` transfer.
- [ ] I can describe deterministic destruction during normal and exceptional scope exit.
- [ ] I can use a vector, map, iterator range, algorithm, lambda, and template deliberately.
- [ ] I can build and test a small CMake target and add address/UB sanitizer flags when supported.

## Elaborative interrogation and self-explanation

**Why is RAII safer than a cleanup comment?**

<details><summary>Answer</summary>A destructor is language-enforced at scope exit; a comment relies on every control-flow path and every future maintainer remembering the same manual cleanup step.</details>

**Why not default to `shared_ptr`?**

<details><summary>Answer</summary>Shared ownership hides who controls lifetime, adds reference-counting cost, and can leak through cycles. Prefer the simplest single owner and borrow non-owning views.</details>
