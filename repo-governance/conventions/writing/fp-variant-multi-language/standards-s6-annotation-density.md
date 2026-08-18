---
title: "FP-Variant Multi-Language Convention — Standards S6: Annotation Density"
description: The 1.0-2.25 comment-to-code ratio applied independently to each tab, and how cross-paradigm annotations count toward it.
when_to_use: Use when checking whether an F# or Clojure tab's code block meets the required annotation density.
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

# Standards S6: Annotation Density

Every code block in both tabs MUST meet the annotation density standard defined in the [By-Example Tutorial Convention](../../tutorials/swe-by-example.md): **1.0–2.25 comment lines per code line, measured per individual example** (not tutorial-wide). This ratio applies independently to the F# tab and the Clojure tab.

Lines that are blank, closing braces, or closing brackets do not count as code lines. Comment lines beginning with `//` (F#) or `;` (Clojure) count as comment lines. Inline comments on a code line count as 0.5 comment lines toward the ratio.

When a cross-paradigm annotation (S5) is added, it counts toward the comment lines of the tab it appears in.
