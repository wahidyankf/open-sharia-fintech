---
description: The bidirectional idiomatic rule preventing either language from mimicking the other, and how to handle a concept that exists natively in only one language via closest equivalent plus annotation.
when_to_use: Use when a concept in one tab has no direct native counterpart in the other, to decide the correct closest-equivalent-plus-annotation treatment.
---

# Standards S4-S5: Bidirectional Rule and Cross-Paradigm Handling

## S4: Bidirectional Idiomatic Rule

Neither language MUST force non-idiomatic patterns from the other. This rule applies in both directions:

- **F# MUST NOT** adopt Clojure-style dynamic dispatch, untyped maps, or runtime-tag dispatch solely to mirror the Clojure tab's structure.
- **Clojure MUST NOT** adopt F#-style record simulations (defrecord used purely as a value-semantics clone) or rigid type-hierarchy patterns that conflict with Clojure's data-orientation philosophy.

The idiomatic divergence between tabs is intentional and educational. Authors MUST NOT normalise or suppress the difference. Where tabs diverge structurally (for example, F# uses a computation expression and Clojure uses a threading macro), both structures MUST be retained as written; the cross-paradigm annotation in S5 explains the divergence.

## S5: Cross-Paradigm Concept Handling

When a paradigm-specific concept exists natively in only one language, use the closest native equivalent in the other language and add an annotation explaining the trade-off. Do NOT mechanically translate the construct.

**Direction rules:**

- If the concept is F#-native (discriminated unions, computation expressions, units of measure), the Clojure tab uses the closest Clojure native equivalent (multimethods, tagged maps, malli spec, threading macros) with a comment annotation.
- If the concept is Clojure-native (multimethods, REPL session state, spec hierarchies), the F# tab uses the closest F# native equivalent (DUs + pattern matching, interfaces, discriminated union hierarchies) with a comment annotation.

**Annotation format for cross-paradigm divergence:**

In F# tabs, use `// [Clojure: <equivalent> — <one-sentence trade-off note>]`:

```fsharp
// [Clojure: tagged map {:tag :ok :value x} — data-first; no compile-time exhaustiveness check]
type Outcome<'T, 'E> = Ok of 'T | Err of 'E
```

In Clojure tabs, use `; [F#: <equivalent> — <one-sentence trade-off note>]`:

```clojure
; [F#: discriminated union — compiler-enforced exhaustiveness; Clojure uses open dispatch via multimethods]
(defmulti handle-outcome :status)
```

The annotation MUST appear on the line immediately preceding the construct it annotates, or as an inline comment on the same line when the construct is a single line.
