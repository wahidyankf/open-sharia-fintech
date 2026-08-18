---
title: "Multi-Harness Binding: Canonical Surface, Binding Tiers, and No-Shadowing (Rules 1-3)"
description: Rules 1 through 3 — AGENTS.md as the single instruction source, the Tier-1/Tier-2 binding model, and the hard no-shadowing rule for higher-precedence harness files.
when_to_use: Read this when deciding whether a harness needs a committed binding file, or when auditing whether a harness-specific file improperly shadows AGENTS.md.
category: explanation
subcategory: conventions
tags:
  - conventions
  - governance
  - platform-bindings
  - agents
  - compatibility
created: 2026-05-24
---

# Multi-Harness Binding: Canonical Surface, Binding Tiers, and No-Shadowing (Rules 1-3)

The first three standards of the [Multi-Harness Binding Convention](../multi-harness-binding.md):
what the canonical surface is, how harnesses are tiered, and the hard rule against shadowing it.

## Rule 1 — Canonical Surface (AD1)

`AGENTS.md` at the repository root is the **single source of instruction content**. No harness-
specific binding file may contain instruction prose that does not also appear in `AGENTS.md`. Binding
files exist only to wire a harness to the canonical file — as a native read, a pointer, or a
mechanically derived artifact.

**Rationale**: Most harnesses read `AGENTS.md` natively. Keeping content in one place eliminates the
entire class of cross-tool drift.

## Rule 2 — Two Binding Tiers (AD2)

Every harness falls into exactly one of two tiers.

### Tier 1 — Native canonical-file readers

A harness that reads the canonical root instruction file natively requires no additional committed
file. The native read is sufficient; the catalog entry documents that status.

A Tier-1 binding file is permitted only when it materially improves instruction discovery for that
harness (for example, a tool that reads a supplementary file in addition to the canonical file). Even
then, the file must be a **non-duplicating pointer** — it must reference `AGENTS.md` rather than
copy or paraphrase it. The default position is: **add nothing**.

### Tier 2 — Non-native readers

A harness that does not read the canonical root instruction file natively requires an **explicit
committed bridge file**. The bridge must point to (or be mechanically derived from) the canonical
file. It must not contain independent instruction prose.

## Rule 3 — No-Shadowing Rule (AD3, HARD)

Some harnesses rank a tool-specific instruction file **above** the canonical root instruction file.
If such a higher-precedence file exists in the repository, it silently overrides `AGENTS.md` for
that tool only, producing divergent behavior that is invisible to contributors using any other
harness.

**The repository must not commit any higher-precedence file whose content diverges from `AGENTS.md`.**

The default is to **not create such files at all**. If a future operational need forces one to exist,
it must be implemented as a pure pointer or import of `AGENTS.md` — no independent prose. This
decision must be recorded in the platform-bindings catalog with an explicit justification.

Examples of file categories that trigger this rule (the concrete file names belong under the
Platform Binding Examples heading in the
[Platform Binding Examples](./platform-binding-examples.md) child, not in this rule prose):

- Any tool-specific file that a harness explicitly ranks above `AGENTS.md` when both are present.
