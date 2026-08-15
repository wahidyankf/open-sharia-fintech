---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Every worked example is a C17-portable, warning-clean source set under `learning/code/`. From an
example directory, run `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`;
the multi-file and Makefile examples state their `make` command instead. GCC 15 defaults to a
newer dialect and Clang’s C23 support continues to evolve, so the course intentionally uses
conservative C17 syntax that both compilers support.

The examples progress from the compile/run loop and core syntax (1–26), through addresses, arrays,
strings, structs, files, headers, and linking (27–54), to allocation, linked data, object files,
Makefiles, and a short integration program (55–78). This is not a C reference: each example serves
the OS and systems prerequisites stated in the course [overview](../overview).
