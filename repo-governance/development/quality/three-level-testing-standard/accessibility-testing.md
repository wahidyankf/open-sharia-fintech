---
title: "Accessibility Testing"
description: "Accessibility testing within this standard."
category: explanation
subcategory: development
tags:
  - testing
  - unit-tests
  - integration-tests
  - e2e-tests
  - bdd
  - gherkin
created: 2026-03-13
when_to_use: "Use when scoping an accessibility test."
---

# Accessibility Testing

Accessibility testing is compulsory for all UI-related projects and operates at two levels that
complement the three-level testing standard.

## Static A11y Linting (via `lint` target)

All UI projects must include static accessibility checks in their `lint` target. These checks catch
common accessibility violations at compile time and are enforced at all three gates: pre-push hook,
PR quality gate, and scheduled Test CI workflows.

- **TypeScript UI projects** (`organiclever-app-web`, `ayokoding-www`, `ose-www`, `libs/web-ui`):
  `oxlint --jsx-a11y-plugin`

## Runtime Accessibility E2E Tests (via `test:e2e`)

All UI projects must have runtime accessibility E2E tests using `@axe-core/playwright` (axe-core)
covering WCAG AA compliance:

- Color contrast ratios (WCAG AA: 4.5:1 for normal text, 3:1 for large text)
- Keyboard navigation (all interactive elements reachable via Tab/Shift+Tab)
- ARIA labels and roles on interactive elements
- Focus management (focus moves logically, focus traps work correctly)
- Heading hierarchy (no skipped levels, single H1)

## Gherkin Accessibility Specs

UI projects must have an `accessibility.feature` file under a domain subdirectory in
`specs/apps/<domain>/fe/gherkin/` (e.g., `accessibility/accessibility.feature` or
`layout/accessibility.feature`). UI component library specs in
`specs/libs/web-ui/behaviors/<component>/` must include "Has no accessibility violations" scenarios for
each component.

See [Nx Target Standards](../infra/nx-targets.md) for the full list of projects with static a11y
linting and the enforcement gates.
