---
title: "FP-Variant Multi-Language Convention — Scope and Tabbed Format (S1)"
description: Which files this convention governs (and excludes), plus the S1 standard for the F#-first, Clojure-second tabbed code block format.
when_to_use: Use when determining whether a file falls under this convention, or when structuring the outer tabs shortcode for a new FP-variant example.
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

# Scope and Tabbed Format (S1)

## Scope

### What This Convention Covers

- All FP-variant by-example tutorial files in `apps/ayokoding-www/content/en/learn/legacy/software-engineering/software-architecture/*/in-fp-by-example/` — specifically `beginner.md`, `intermediate.md`, and `advanced.md` level pages.
- Overview pages (`overview.md`) under those paths, for any code snippets they contain.
- Both English and Indonesian variants of those files when they exist.

### What This Convention Does NOT Cover

- **OOP-variant by-example tutorials** (`in-oop-by-example/`) — those have separate language scope rules.
- **In-the-field guides** (`in-the-field/`) — real-world framework and library choices override theoretical multi-language presentation.
- **By-concept tutorials** (`by-concept/`) — narrative explanations follow their own structure convention.
- **Other languages** (Java, TypeScript, Go, Python, etc.) — governed by their respective tutorial conventions. This convention is specific to the FP variant's F# + Clojure requirement.
- **docs/explanation/ documents** — repository explanation docs follow the Diátaxis explanation standard, not this tutorial-content convention.
- **Clojure or F# language tutorials** themselves — the programming-language tutorial structure convention governs standalone language tutorials.

## S1: Tabbed Format — F# First, Clojure Second

Every code block in an FP-variant by-example page MUST use tabbed format with F# as the first tab and Clojure as the second tab.

The outer shortcode structure is:

```text
{{< tabs items="F#,Clojure" >}}

{{< tab >}}
[F# code block here]
{{< /tab >}}

{{< tab >}}
[Clojure code block here]
{{< /tab >}}

{{< /tabs >}}
```

Each `[language code block here]` placeholder is a fenced code block with the appropriate language identifier (`fsharp` or `clojure`).

The tab label strings are exactly `F#` and `Clojure` (case-sensitive, in that order). Do not reorder the tabs, do not use alternate labels such as `fsharp` or `clj`.

Standalone code blocks that appear outside example sections (for example, in an intro paragraph) are exempt from the tabs requirement when they are not demonstrating the example concept itself.
