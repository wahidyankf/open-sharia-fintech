---
description: Why two languages, why the bidirectional idiomatic constraint, and why closest-native-equivalent-plus-annotation rather than forced translation.
when_to_use: Use when you need to justify this convention's requirements to a reviewer or explain the reasoning behind the bidirectional rule.
---

# Rationale

**Why two languages?**

The FP-variant by-example tutorials teach architecture concepts — DDD, hexagonal architecture, FSM, and similar patterns — through a functional programming lens. F# and Clojure represent two distinct traditions within functional programming: typed-FP with rich compile-time guarantees (F#) and dynamic-FP with REPL-driven data orientation (Clojure). Showing the same architecture concept in both languages reveals how design decisions shift across these traditions, producing deeper understanding than a single-language presentation can achieve.

**Why the bidirectional idiomatic constraint?**

Mechanical translation produces code that no experienced practitioner in either community would write. A Clojure developer reading F#-flavoured Clojure code learns incorrect idioms. An F# developer reading Clojure-flavoured F# code learns patterns that fight the type system. In both cases the learner exits the tutorial with habits that the respective community would flag in code review. The bidirectional constraint protects the educational integrity of both language tracks.

**Why closest native equivalent plus annotation rather than forced translation?**

Some concepts are paradigm-specific, not merely language-specific. F# discriminated unions exist because the compiler can prove exhaustiveness at compile time — there is no meaningful Clojure equivalent that preserves that property. Pretending otherwise by constructing an elaborate simulation teaches the wrong lesson. The closest native equivalent plus an annotation teaches two true things simultaneously: how Clojure actually solves this class of problem, and what is lost or gained relative to the F# approach. That is richer and more honest than either forced symmetry or silent omission.
