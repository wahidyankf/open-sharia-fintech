---
title: Frontend Development
description: UI development conventions for the open-sharia-enterprise monorepo's frontend applications
category: explanation
subcategory: development/frontend
tags:
  - index
  - frontend
  - ui
  - conventions
  - accessibility
  - styling
created: 2026-03-28
when_to_use: Use when building, styling, or testing a UI component in any frontend app in this monorepo.
---

# Frontend Development

UI development conventions for the open-sharia-enterprise monorepo's frontend applications. These documents define how to build, style, and test user interface components across all frontend apps in the repository.

**Governance**: All frontend conventions in this directory serve the [Vision](../../vision/open-sharia-enterprise.md) (Layer 0), implement the [Core Principles](../../principles/README.md) (Layer 1), and complement [Documentation Conventions](../../conventions/README.md) (Layer 2) as part of the six-layer architecture. Each convention MUST include TWO mandatory sections: "Principles Implemented/Respected" and "Conventions Implemented/Respected". See [Repository Governance Architecture](../../repository-governance-architecture.md) for the complete governance model.

## 🎯 Scope

**This directory contains conventions for UI DEVELOPMENT:**

**✅ Belongs Here:**

- UI component patterns and composition strategies
- Design token categories, naming rules, and per-app override patterns
- Styling approach (Tailwind v4, utility-first, class ordering)
- Accessibility requirements specific to UI components (focus management, ARIA, reduced-motion)
- Dark mode implementation requirements
- Form control patterns and validation UI

**❌ Does NOT Belong Here:**

- How to write and format documentation (use [Conventions](../../conventions/README.md))
- Color accessibility for diagrams and documentation (use [Color Accessibility Convention](../../conventions/formatting/color-accessibility.md))
- Backend API patterns or server-side logic
- Build infrastructure and Nx targets (use [Nx Target Standards](../infra/nx-targets.md))

## 📋 Contents

- [Design Tokens Convention](./design-tokens.md) — Conventions for CSS design tokens across frontend apps, covering structural shared tokens, per-app brand overrides, dark mode requirements, and Tailwind v4 integration. Use when adding, naming, or overriding a CSS design token.
- [Component Patterns Convention](./component-patterns.md) — Standards for building UI components with CVA variants, Radix primitives, and React patterns. Use when creating or reviewing any UI component in ayokoding-www or organiclever-app-web.
- [Accessibility Convention](./accessibility.md) — WCAG AA requirements for UI components — focus management, ARIA attributes, reduced motion, form controls, and keyboard navigation. Use when building or reviewing any frontend UI component.
- [Styling Convention](./styling.md) — CSS and Tailwind v4 styling patterns for frontend applications. Use when writing or reviewing CSS/Tailwind styling in any frontend app.

## 🔗 Related Documentation

- [Color Accessibility Convention](../../conventions/formatting/color-accessibility.md) — WCAG AA color palette, contrast ratios, and color-blind friendly design (authoritative source for all color decisions)
- [Accessibility First Principle](../../principles/content/accessibility-first.md) — Foundational principle governing all accessibility requirements
- [Implementation Workflow](../workflow/implementation.md) — Three-stage development workflow applied when building UI features
- [Behaviour-Driven Development](../behaviour-driven-development.md) — Unit, integration, and E2E testing requirements for frontend apps

## ✅ Principles Implemented/Respected

- [Accessibility First](../../principles/content/accessibility-first.md) — Every UI convention in this directory enforces WCAG AA compliance as a baseline requirement, not an afterthought
- [Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md) — Component patterns favor composition over inheritance and utility-first styling over custom CSS abstractions
- [Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md) — Design tokens, variant definitions, and class ordering rules make UI decisions visible and auditable

## 📐 Conventions Implemented/Respected

- [Color Accessibility Convention](../../conventions/formatting/color-accessibility.md) — UI color usage must meet the WCAG AA contrast ratios defined in this convention
- [Indentation Convention](../../conventions/formatting/indentation.md) — All code examples in this directory use language-appropriate indentation (2 spaces for TypeScript/JSX/JSON)
