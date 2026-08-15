---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Run the 78 examples from `learning/code/` with `cargo run --bin ex-NN`; the examples are
independent binaries in one workspace, so a later lesson never silently depends on an earlier
file. Examples 71, 72, and 77 also carry tests; run `cargo test --bin ex-71`, for example.

The progression is intentional: examples 1–26 establish Rust’s typed value and data-model surface;
27–52 make ownership, borrowing, errors, traits, and generic contracts concrete; 53–78 combine
those ideas without introducing systems-programming depth that Modern System Programming owns.

## Concepts

- **co-01 · cargo-new** — scaffold a conventional Cargo project.
- **co-02 · cargo-run** — compile and execute a selected binary.
- **co-03 · cargo-build** — compile without executing a binary.
- **co-04 · cargo-test** — run focused `#[test]` functions.
- **co-05 · cargo-dependencies** — declare a needed crate in `Cargo.toml`.
- **co-06 · bindings-and-mutation** — use immutable bindings, `mut`, and local shadowing.
- **co-07 · basic-types-and-functions** — use scalar values, tuples, and typed functions.
- **co-08 · ownership** — one value has one responsible owner.
- **co-09 · moves** — transfer ownership by assignment or by-value calls.
- **co-10 · shared-borrows** — read through `&T` without moving its owner.
- **co-11 · mutable-borrows** — mutate through exclusive `&mut T` access.
- **co-12 · borrow-rules** — permit one mutable or many shared borrows at once.
- **co-13 · lifetimes** — keep every reference within its referent’s lifetime.
- **co-14 · structs** — name related fields and attach methods with `impl`.
- **co-15 · enums** — model a choice among typed variants.
- **co-16 · exhaustive-match** — handle every enum state through patterns.
- **co-17 · focused-patterns** — use `if let` and `while let` for one pattern.
- **co-18 · option** — represent optional data with `Some` and `None`.
- **co-19 · result** — represent success or recoverable failure with `Ok` and `Err`.
- **co-20 · question-mark** — propagate `Result` or `Option` failure early with `?`.
- **co-21 · traits** — state behavior as a capability contract.
- **co-22 · trait-bounds** — constrain generic code by required capabilities.
- **co-23 · generics** — write one type-safe algorithm for many concrete types.
- **co-24 · owned-collections** — use `Vec`, `String`, and `HashMap` deliberately.
- **co-25 · iterators** — compose map, filter, collect, and fold pipelines.
- **co-26 · closures** — carry a typed operation and captured context.
