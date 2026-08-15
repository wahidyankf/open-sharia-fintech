---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Rust counterpart to system-programming

## Why this exists

Rust keeps low-level control while making ownership, borrowing, and thread-safety obligations
checkable before the program runs. This course moves from values and borrows to concurrency,
zero-cost abstractions, explicit errors, and a deliberately small audited C boundary.

## Prerequisites

- [Just Enough Rust](../just-enough-rust/learning/overview.md): ownership intuition, traits,
  pattern matching, and `Result`.
- A current stable Rust toolchain (`cargo` and `rustc`); a C compiler is needed for the final FFI step.

## Scope boundary

This is not a duplicate of the C systems course. It teaches the Rust safety model and its C ABI
boundary, rather than manual allocation, pointer arithmetic, or C-specific operating-system APIs.

Start with [learning](./learning/overview.md), then make the decisions retrievable in
[drilling](./drilling/overview.md).
