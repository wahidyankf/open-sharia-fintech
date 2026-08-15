---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Lisp teaches the uncommon but powerful idea that code is data. This course starts with Scheme
s-expressions, recursion, and hygienic macros, then uses Clojure as a modern hosted-Lisp sidebar.

## Prerequisites

[Functional Programming](../functional-programming/learning/overview.md) supplies recursion and
higher-order functions. [Programming Paradigms](../programming-paradigms/learning/overview.md)
provides the broader context. Use Racket or a Scheme implementation for the primary examples and a
Clojure toolchain plus JDK for the sidebar.

## Scope boundary

This is Lisp thinking, macro hygiene, and code-as-data—not complete Racket, Common Lisp, Clojure,
or compiler implementation coverage. Hash tables are implementation-specific in Scheme; vectors are
the R7RS-small indexed collection. The course avoids version-pinned implementation claims.

## Sources

- [R7RS-small](https://small.r7rs.org/) defines the Scheme small language and proper tail recursion.
- [Racket license](https://download.racket-lang.org/license.html) documents its Apache-2.0/MIT terms.
- [Clojure license](https://clojure.org/community/license) documents EPL-1.0.
- [Clojure macros](https://clojure.org/reference/macros) documents macro expansion and syntax quote.

All examples are original instructional artifacts.
