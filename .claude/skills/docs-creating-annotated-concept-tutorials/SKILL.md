---
name: docs-creating-annotated-concept-tutorials
description: Format standards for Annotated-concept tutorials (concept-centric worked examples, standard and no-code sub-mode) shared by the ayokoding-www maker/checker/fixer family
---

# Creating Annotated-Concept Tutorials

Annotated-concept is a concept-centric tutorial format for ayokoding-web: worked
examples/scenarios that teach a concept through annotated code, pseudocode, config, or diagrams,
rather than language-syntax progression (that's By Example's job).

## When This Skill Loads

Auto-loads for `apps-ayokoding-www-annotated-concept-maker`, `-checker`, and `-fixer`.

## Two Modes

**Standard mode** (code-bearing): concepts illustrated with runnable code/pseudocode/config.
**No-code sub-mode** (leadership/governance topics): zero code, worked scenarios use decision
artifacts (decision records, matrices, runbook excerpts) instead. Mode is detected from the
topic's format designation before any other check runs — every subsequent rule branches on it.

## Format Requirements

See [reference/format-requirements.md](./reference/format-requirements.md) for the complete
worked-example/scenario count floors, annotation density formula, five-part structure, mode
integrity rule, and grouping/diagram requirements — shared by maker, checker, and fixer.

## Reference Documentation

- [Tutorial Convention](../../../repo-governance/conventions/tutorials/general.md)
- [Color Accessibility Convention](../../../repo-governance/conventions/formatting/color-accessibility.md)
