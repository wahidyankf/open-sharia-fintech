---
title: "Governance Surfaces"
description: Definitions for surface, instruction file, binding, mirror, harness, and autoloaded — the vocabulary the word-budget and vendor-independence conventions run on.
when_to_use: Use when reading a word-budget report, editing a binding, or reasoning about which guidance an agent actually receives.
category: explanation
subcategory: governance
tags:
  - governance
  - glossary
  - platform-bindings
  - agents
created: 2026-08-16
---

# Governance Surfaces

| Term                 | What it means                                                           |
| -------------------- | ----------------------------------------------------------------------- |
| **Surface**          | A file class a gate measures, declared as a glob with thresholds        |
| **Instruction file** | A file a coding agent reads on its own, without being asked             |
| **Harness**          | A coding agent that reads this repository                               |
| **Binding**          | Harness-specific configuration translating shared rules into its format |
| **Mirror**           | A generated binding, derived from the primary one                       |

## Surface

A surface is whatever a gate's glob selects, paired with target, warn, and fail thresholds. When a
path matches more than one glob, the last-declared surface wins. Word count is a raw whole-file
count with no exclusions — front matter, code blocks, and link URLs all count.

The single sanctioned remedy for an over-budget file is progressive disclosure: split it, leaving
an index that links annotated children. Compression, silent truncation, and raising a threshold to
fit a bloated file are all excluded.

## Binding and Mirror

One binding is hand-authored and primary; the rest are generated from it and must land in the same
commit as their source. A mirror is never hand-edited — an edit there is overwritten on the next
generation and, worse, passes review as if it were a real change.

Governance prose stays vendor-neutral: it says "the primary binding" rather than naming a harness.
Concrete directory names belong in binding examples and the platform catalog.

The `class: vendored` exception to "never hand-edited" is not uniform — it covers two structurally
different subclasses, and confusing one for the other misfires in opposite directions. See [The
`class: vendored` Exception Has Two Subclasses](./vendored-exception-subclasses.md) before
hand-editing a vendored path or writing a sentence that states this rule.

## Autoloaded

**Autoloaded** means a harness reads the file into context unprompted. It is narrower than it
sounds, and the distinction matters:

- The canonical instruction file is autoloaded — for the main conversation only.
- **Delegated agents do not inherit it.** They receive only their own definition and the agent
  skills their definition declares.
- A link inside an autoloaded file is not autoloaded. It is an invitation to read, taken or not.

Guidance that every delegated agent must share therefore has to reach them through their declared
agent skills, not through the canonical instruction file alone.

## Related Documents

- [Glossary](../glossary.md) — the other term clusters.
- [Governance Word-Budget](../conventions/structure/governance-word-budget.md) — thresholds and
  enforcement.
- [Governance Vendor-Independence](../conventions/structure/governance-vendor-independence.md) —
  neutral vocabulary and the allowlist mechanism.
