---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## 1. Recall Q&A

**Q. What does ownership prove?**

<details><summary>Answer</summary>Every value has one owner; when that owner ends, Rust drops the value. A move transfers that responsibility instead of copying it implicitly.</details>

**Q. Why does `Arc<Mutex<T>>` avoid a data race?**

<details><summary>Answer</summary>`Arc` gives shared ownership across threads and `Mutex` makes every mutation require exclusive locked access. The type system also refuses non-`Send` values at the thread boundary.</details>

## 2. Scenario judgment

A worker needs the first byte from a borrowed packet and then reports its length to another thread.

<details><summary>Reasoned answer</summary>Read the byte through a normal slice borrow, send an owned length or owned message through a channel, and do not send a borrowed reference unless scoped-thread lifetime rules prove it remains valid.</details>

## 3. Safety-boundary trace

For a C ABI call, name: the pointer validity and lifetime preconditions; the allocator responsible for freeing any allocation; the smallest `unsafe` block; and the safe wrapper that prevents callers from violating those facts.

## 4. Hands-on practice

Change `capstone/code/concurrent` to process three job values. Keep the channel as the ownership hand-off, join every worker, and write a test that proves the resulting total rather than relying on print output.

## 5. Automaticity checklist

- [ ] I can tell a move from a borrow and choose the least-owning interface.
- [ ] I can identify where `Send` and `Sync` constrain a design.
- [ ] I can choose channels for ownership transfer and a mutex for shared mutation.
- [ ] I can explain why iterator/generic abstractions need not add a runtime dispatch cost.
- [ ] I can write down an FFI safety contract before entering `unsafe`.
