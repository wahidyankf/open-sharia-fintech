---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Goal

Build the smallest useful multi-file C program: a two-item inventory summary. It is a **light
consolidation**, not a new project. It combines only the Primer surface—a portable include guard, a
shared `struct`, arrays, pointers, `stdio`, and a warning-clean Makefile—so it proves readiness
for the OS and systems courses without introducing networking, processes, or an application framework.

## Concepts exercised

- [x] `Makefile` build and clean targets (`co-03`)
- [x] pointer plus array traversal (`co-10`, `co-12`)
- [x] a shared `struct Item` (`co-15`, `co-23`)
- [x] formatted output with `stdio` (`co-17`)
- [x] header declaration and portable include guard (`co-20`, `co-22`)
- [x] warning-clean compiler flags (`co-26`)

## Run

From `learning/capstone/code`, run:

```text
make
./inventory
make clean
```

Expected output:

```text
items=2 total=7
```

The program keeps data ownership simple: `main` owns its fixed array, passes its address and count
to `inventory_total`, and nothing allocates heap memory. That is intentional: this capstone
consolidates the language boundary before later systems material introduces resource lifetimes at OS
scale.
