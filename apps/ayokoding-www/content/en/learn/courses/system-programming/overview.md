---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Prerequisites

This course has exactly two prerequisites: [Just Enough C](../just-enough-c/learning/overview.md)
(functions, pointers, structs, compilation) and [Linux OS](../linux-os/learning/overview.md)
(processes, descriptors, syscalls, and signals). Bring a POSIX terminal, `cc`/`clang`/`gcc`, and,
on Linux, Valgrind. The examples use C11 plus POSIX APIs where named.

## Why this exists

C exposes memory, files, byte layouts, and kernel handles directly. That makes compact, fast programs
possible, but it also means an allocation, file descriptor, or socket remains the program's
responsibility until it is released. The durable habit is simple: name the owner, make transfer
explicit, and release every acquired resource on every exit path.

## Boundary: this course vs Modern System Programming

This is the **C manual-resource-management** course: pointer lifetime, checked size arithmetic,
portable cleanup with `goto cleanup`, ABI-facing layouts, byte-order-explicit serialization, and the
small POSIX file/signal/socket surface needed to practise them. It deliberately does **not** teach
concurrency, lock-free algorithms, threads, async I/O, epoll/kqueue reactors, advanced IPC, kernel
internals, performance engineering, or production protocol design. Those topics and their stronger
invariants belong in Modern System Programming. `__attribute__((cleanup))` appears only as an optional
GCC/Clang extension; it is not ISO C and is never the portable answer.

## Learning route

Work through the [78 runnable examples](./learning/overview.md), then complete the
[five-section drilling pack](./drilling/overview.md), then build the
[capstone](./learning/capstone/explanation.md). Compile ordinary examples with:

```sh
cc -std=c11 -Wall -Wextra -Werror path/to/example.c -o example && ./example
```

On Linux, add `-fsanitize=address,undefined -g` for ASan/UBSan and run the resulting binary under
`valgrind --leak-check=full --error-exitcode=1 ./example`. AddressSanitizer is normally not
combined with Valgrind: make a clean run with each tool separately.
