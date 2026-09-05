---
title: "Scope"
description: "What this convention applies to and its boundaries."
category: explanation
subcategory: development
tags:
  - verification
  - testing
  - playwright
  - api
  - quality
  - manual-testing
created: 2026-04-04
when_to_use: "Use when checking whether this convention applies to a change."
---

# Scope

This convention applies to:

- All AI agents implementing UI or API changes
- All human developers implementing UI or API changes
- All apps in `apps/` that have a UI or API surface

It does not apply to:

- Library-only changes (`libs/`) with no UI or API surface
- Documentation changes (`docs/`, `repo-governance/`, `plans/`)
- Configuration changes that do not affect runtime behaviour
- Internal refactors with no observable behavioural change
