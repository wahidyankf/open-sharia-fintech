---
title: "Nx Target Naming Rules"
description: "Canonical lifecycle and testing target vocabulary"
category: explanation
subcategory: development
tags: [nx, targets, project-json]
created: 2026-02-23
when_to_use: "Use when naming or reviewing an Nx target."
---

# Nx Target Naming Rules

- Use `dev` for development and `start` for production serving; never use `serve` aliases.
- Use `test:unit`, `test:integration`, and `test:e2e` only for runtime execution at the named
  boundary.
- Use `test:coverage:unit`, `test:coverage:integration`, `test:coverage:e2e`, and
  `test:coverage:behaviour` only for deterministic static coverage validation.
- Use `test:coverage` only as an aggregate of applicable static coverage targets.
- Use `test:quick` for the closed fast composition; never include Integration/E2E runtime.
- Separate variants with a colon and use lowercase kebab-case within each segment.
- Omit an inapplicable target; never provide an echo, no-op, sentinel, duplicate, or alias.
