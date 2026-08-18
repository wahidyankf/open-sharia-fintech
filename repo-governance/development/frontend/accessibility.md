---
title: Accessibility Convention
description: WCAG AA requirements for UI components — focus management, ARIA attributes, reduced motion, form controls, and keyboard navigation for frontend applications
category: explanation
subcategory: development/frontend
tags:
  - accessibility
  - wcag
  - a11y
  - aria
  - focus
created: 2026-03-28
when_to_use: Use when building or reviewing any frontend UI component — focus rings, ARIA attributes, form inputs, color usage, images, or keyboard interaction.
---

# Accessibility Convention

Frontend accessibility requirements for all UI applications in the open-sharia-enterprise monorepo. These requirements implement the [Accessibility First](../../principles/content/accessibility-first.md) principle at the component and interaction layer.

## Governing Principle

The [Accessibility First](../../principles/content/accessibility-first.md) principle establishes WCAG AA compliance as the **minimum standard** — built in from day one, not retrofitted. Every interactive element, every form, every motion effect, and every color decision must satisfy this baseline.

## Scope Clarification

The [Color Accessibility Convention](../../conventions/formatting/color-accessibility.md) defines a 5-color palette that applies exclusively to **documentation** (Mermaid diagrams, charts, visual aids in `docs/` and `repo-governance/`). UI applications are **not** restricted to that palette. Frontend apps may use any colors, design tokens, or brand colors provided they meet the WCAG AA contrast requirements in this document and avoid encoding information through color alone.

## Contents

- [Contrast and Focus](./accessibility/contrast-and-focus.md) — WCAG AA minimum contrast ratios, and focus-visible ring patterns.
- [Reduced Motion and ARIA Attributes](./accessibility/reduced-motion-and-aria-attributes.md) — honoring prefers-reduced-motion, and required ARIA by component type.
- [Form Inputs and Hit Targets](./accessibility/form-inputs-and-hit-targets.md) — labels, autoComplete, inputMode, and minimum touch target sizes.
- [Color and Images](./accessibility/color-and-images.md) — no color-only indicators, and alt-text requirements.
- [Screen Readers and Keyboard Navigation](./accessibility/screen-readers-and-keyboard-navigation.md) — DOM order, skip navigation, live regions, and the full keyboard interaction table.

## Principles Implemented/Respected

- [Accessibility First](../../principles/content/accessibility-first.md) — This entire convention exists to implement WCAG AA compliance, keyboard navigation, screen reader support, and inclusive design as mandatory requirements, not optional enhancements.
- [Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md) — ARIA attributes, `htmlFor`/`id` associations, `autoComplete`, and `inputMode` values must be stated explicitly in markup; no implicit browser inference is sufficient.
- [Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md) — Use native HTML elements (`<button>`, `<input>`, `<select>`) over custom implementations where possible. Native elements come with accessibility semantics built in.

## Conventions Implemented/Respected

- [Color Accessibility Convention](../../conventions/formatting/color-accessibility.md) — WCAG AA contrast ratios referenced in this document align with the ratios defined there. That convention is the authoritative source for color-blind friendly palette guidance (for docs); this convention extends the same contrast standards to UI application colors.
- [Indentation Convention](../../conventions/formatting/indentation.md) — All TypeScript/TSX code examples use 2-space indentation per the project standard.

## Related Documentation

- [Design Tokens Convention](../frontend/design-tokens.md) — Token naming and dark mode requirements that underpin accessible color choices
- [Component Patterns Convention](../frontend/component-patterns.md) — CVA variants and Radix composition patterns that expose accessibility props
- [Accessibility First Principle](../../principles/content/accessibility-first.md) — Governing principle with rationale and moral context
- [Color Accessibility Convention](../../conventions/formatting/color-accessibility.md) — Master reference for color palette and contrast (docs scope)
- [WCAG 2.2 Level AA](https://www.w3.org/WAI/WCAG22/quickref/) — International accessibility standard
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) — Verify contrast ratios
