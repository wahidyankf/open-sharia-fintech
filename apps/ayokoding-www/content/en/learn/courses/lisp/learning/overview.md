---
title: "Learning Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Concepts

1. **co-01 · s-expressions** — code and data use the same parenthesized form.
2. **co-02 · homoiconicity** — programs can be manipulated as ordinary data.
3. **co-03 · reader** — the reader turns text into forms before evaluation.
4. **co-04 · quote** — quote suppresses evaluation.
5. **co-05 · eval** — eval evaluates a constructed form.
6. **co-06 · atoms-lists** — atoms and lists are the core data distinction.
7. **co-07 · cons** — cons constructs a pair.
8. **co-08 · car-cdr** — car and cdr decompose a list.
9. **co-09 · define** — define binds values and procedures.
10. **co-10 · lambda** — lambda creates an anonymous procedure.
11. **co-11 · closures** — procedures capture lexical environment.
12. **co-12 · recursion** — recursion supplies repeated computation.
13. **co-13 · tail-calls** — Scheme requires proper tail calls.
14. **co-14 · higher-order-functions** — functions can consume and return functions.
15. **co-15 · conditionals** — if and cond express alternatives.
16. **co-16 · let-binding** — let and let-star give local scope.
17. **co-17 · repl** — the REPL supports incremental development.
18. **co-18 · quasiquote** — templates become forms with unquote holes.
19. **co-19 · syntax-rules** — pattern macros are hygienic.
20. **co-20 · macro-hygiene** — introduced names avoid accidental capture.
21. **co-21 · macro-new-form** — macros introduce language-level forms.
22. **co-22 · macroexpand** — expansion makes a macro inspectable.
23. **co-23 · continuations** — call/cc reifies an escape continuation.
24. **co-24 · vectors** — vectors are Scheme's standard indexed collection.
25. **co-25 · clojure-data-structures** — Clojure uses persistent collections.
26. **co-26 · clojure-homoiconicity** — Clojure code is Clojure data.
27. **co-27 · clojure-defmacro** — Clojure macros require deliberate gensym hygiene.
28. **co-28 · clojure-jvm-interop** — Clojure calls Java directly.
29. **co-29 · clojure-seq** — seq unifies lazy collection traversal.
30. **co-30 · lisp-lineage** — Scheme, Clojure, and Common Lisp make distinct trade-offs.

The 78 contiguous examples below have colocated artifacts in [learning/code](./code/README.md).
