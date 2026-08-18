---
title: "Enforcement"
description: How the retired `validate:*` naming scheme is caught by the plan delivery gate via a grep across project.json, hook, workflow, and package.json files.
category: explanation
subcategory: development
tags:
  - nx
  - targets
  - naming
  - conventions
created: 2026-06-13
when_to_use: Use when checking how the old `validate:*` naming scheme is enforced, or writing a similar grep-based delivery gate.
---

# Enforcement

The `validate:*` naming scheme is not validated at the Rust level (no clippy rule), but any
usage of the old form in `project.json` targets, `.husky/` hook files, `.github/workflows/`,
or `package.json` scripts is caught by the plan delivery gate:

```bash
grep -r "validate:" apps/*/project.json libs/*/project.json nx.json .husky/ .github/ package.json
```

A clean output (no matches) is the P10 / P11 gate criterion.

**See also**: [Nx Target Standards](../nx-targets.md) for the full required target set per
project type and caching rules, and [CI/CD Conventions](../ci-conventions.md) for the
Invariant E description.
