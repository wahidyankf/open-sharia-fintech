---
title: "FP-Variant Multi-Language Convention"
description: Bidirectional idiomatic-language rule requiring F# AND Clojure tabs in FP-variant by-example tutorials in ayokoding-www, with each language kept idiomatically native rather than mechanically translated from the other
when_to_use: Use when writing or reviewing an FP-variant by-example tutorial page in ayokoding-www that presents F# and Clojure code side by side.
category: explanation
subcategory: conventions
tags:
  - fp
  - clojure
  - fsharp
  - by-example
  - ayokoding-www
  - tutorial
created: 2026-05-17
---

# FP-Variant Multi-Language Convention

FP-variant by-example tutorials in ayokoding-www teach functional programming concepts through architecture examples. Without a normative language rule, authors may present only one language, mechanically translate idioms across languages, or present non-idiomatic code that misleads learners. This convention establishes the bidirectional idiomatic-language rule: every FP-variant by-example page presents code in F# AND Clojure using tabbed format, and each language stays idiomatic to its own community and runtime rather than being forced into the shape of the other.

## Contents

- [Purpose and Principles](./fp-variant-multi-language/purpose-and-principles.md) — why two languages are required and which principles this convention implements.
- [Scope and Tabbed Format (S1)](./fp-variant-multi-language/scope-and-tabbed-format.md) — which files are covered, and the F#-first, Clojure-second tabs structure.
- [Standards S2: F# Idiomatic Patterns](./fp-variant-multi-language/standards-s2-fsharp-idiomatic-patterns.md) — required native F# constructs.
- [Standards S3: Clojure Idiomatic Patterns](./fp-variant-multi-language/standards-s3-clojure-idiomatic-patterns.md) — required native Clojure constructs.
- [Standards S4-S5: Bidirectional Rule and Cross-Paradigm Handling](./fp-variant-multi-language/standards-s4-s5-bidirectional-rule-and-cross-paradigm-handling.md) — neither language mimics the other, and how to handle language-specific concepts.
- [Examples: PASS Idiomatic F# and Clojure Side-by-Side](./fp-variant-multi-language/examples-pass-idiomatic-side-by-side.md) — a full compliant worked example.
- [Examples: FAIL Non-Idiomatic Patterns](./fp-variant-multi-language/examples-fail-non-idiomatic-patterns.md) — two non-compliant examples and why they fail.
- [Rationale](./fp-variant-multi-language/rationale.md) — why two languages, the bidirectional constraint, and closest-equivalent-plus-annotation.
- [Validation and Tools and Automation](./fp-variant-multi-language/validation-and-tools.md) — the six compliance checks and the maker/checker/fixer agents.
- [References](./fp-variant-multi-language/references.md) — related conventions, agents, overview pages, and architecture documents.

## Standards S6: Annotation Density

Every code block in both tabs MUST meet the annotation density standard defined in the [By-Example Tutorial Convention](../tutorials/swe-by-example.md): **1.0–2.25 comment lines per code line, measured per individual example** (not tutorial-wide). This ratio applies independently to the F# tab and the Clojure tab.

Lines that are blank, closing braces, or closing brackets do not count as code lines. Comment lines beginning with `//` (F#) or `;` (Clojure) count as comment lines. Inline comments on a code line count as 0.5 comment lines toward the ratio.

When a cross-paradigm annotation (S5) is added, it counts toward the comment lines of the tab it appears in.
