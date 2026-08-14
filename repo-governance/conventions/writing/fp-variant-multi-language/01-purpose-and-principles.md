---
title: "FP-Variant Multi-Language Convention — Purpose and Principles"
description: Why FP-variant by-example tutorials require both F# and Clojure tabs, and the core principles this bidirectional idiomatic-language rule implements.
when_to_use: Use when you need the rationale for why an FP-variant page requires two languages before diving into the standards themselves.
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

# Purpose and Principles

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: The two-language requirement and the tabbed format are stated explicitly — not left to author preference. The list of idiomatic patterns for each language, the annotation density requirement, and the cross-paradigm annotation rule are all stated as numbered standards rather than vague guidance.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: When a paradigm-specific concept has no direct counterpart in the other language, the rule requires the closest native equivalent plus a short annotation — not an elaborate simulation. The simplest truthful representation takes precedence over architectural symmetry for its own sake.

- **[Accessibility First](../../../principles/content/accessibility-first.md)**: Non-idiomatic code in either language forces learners to decode foreign patterns on top of the architecture concept being taught. Idiomatic code in each language lowers the cognitive barrier for readers coming from that community.

- **[Documentation First](../../../principles/content/documentation-first.md)**: Cross-paradigm annotations are mandatory, not optional. When a concept is F#-native or Clojure-native and is expressed via the closest equivalent in the other language, the annotation documenting the trade-off is a required part of the example — it is documentation embedded in the code, not an afterthought.

## Purpose

This convention exists to:

- Mandate two-language coverage (F# and Clojure) in every FP-variant by-example page so learners see both typed-FP and dynamic-FP perspectives on the same architecture concept.
- Prevent mechanical cross-language translation that produces non-idiomatic code and misleads learners about each language's natural design style.
- Establish a closed-form rule for handling concepts that exist natively in only one language (closest native equivalent plus annotation, not forced translation).
- Maintain the annotation density standard required by the by-example tutorial convention, applied per-language within each tab.
