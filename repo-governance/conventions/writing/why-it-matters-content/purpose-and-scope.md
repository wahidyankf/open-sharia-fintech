---
title: "Why It Matters: Purpose and Scope"
description: Why fabricated corporate anecdotes are prohibited in Why It Matters sections and which tutorial files this convention governs
category: explanation
subcategory: conventions
tags:
  - ayokoding-www
  - tutorial-content
  - factual-accuracy
  - why-it-matters
  - hallucination-prevention
created: 2026-05-09
when_to_use: Read this before writing or reviewing a Why It Matters section in an ayokoding-www tutorial.
---

# Why It Matters: Purpose and Scope

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md)**:
  AI-generated corporate anecdotes invite readers to accept unverifiable claims as fact.
  Deliberate content creation requires surfacing uncertainty rather than papering over it
  with invented evidence. Theoretical explanations make their epistemic status transparent.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**:
  The boundary between verifiable fact and theoretical reasoning must be explicit in every
  tutorial section. This convention makes that boundary a hard structural rule rather than
  a judgment call left to individual authors or AI agents.

- **[Root Cause Orientation](../../../principles/general/root-cause-orientation.md)**:
  Fabricated corporate case studies are the root cause of accuracy debt in educational
  content. Patching individual hallucinated claims after the fact is the wrong fix;
  prohibiting the pattern at authoring time eliminates the root cause.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**:
  Theoretical explanations convey the same pedagogical value as corporate case studies
  without the verification complexity. Simpler content with lower accuracy risk is
  preferable to elaborate anecdotes that require ongoing fact-checking.

## Purpose

`**Why It Matters**:` sections exist to help readers understand the practical importance
of each concept before they invest time learning it. This pedagogical value is fully
achievable through theoretical reasoning about system properties, trade-offs, and
consequences — no corporate anecdote is required.

The problem this convention solves: AI agents writing tutorial content frequently invent
specific corporate case studies (e.g., "When LinkedIn migrated from Oracle to MySQL...",
"Netflix adopted this pattern because...", "A ride-sharing platform integrated with...")
that appear credible but are hallucinated. These claims:

- Cannot be verified without a citable primary source
- Create accuracy debt that is expensive to audit and fix
- Erode reader trust when discovered to be fabricated
- Require ongoing re-verification as content is updated

This convention eliminates the problem at the source by prohibiting the pattern entirely.

## Scope

### What This Convention Covers

- All `**Why It Matters**:` sections in ayokoding-www tutorial files
- Applies to both by-example tutorials (`apps/ayokoding-www/content/en/learn/**/by-example/`)
- Applies to in-the-field guides (`apps/ayokoding-www/content/en/learn/**/in-the-field/`)
- Applies to all future tutorial formats that include a Why It Matters section
- Applies equally to English and Indonesian content

### What This Convention Does NOT Cover

- The overall structure of tutorial files — see the relevant tutorial format conventions
- Factual validation of technical code examples — see [Factual Validation Convention](../factual-validation.md)
- Other tutorial sections (Introduction, Code Example, Explanation, etc.)
- Content in `docs/`, `plans/`, or convention documents themselves
