---
title: "Scope"
description: "What this convention applies to."
category: explanation
subcategory: development
tags:
  - ci
  - quality-gates
  - root-cause
  - debugging
  - anti-pattern
  - preexisting-issues
created: 2026-04-04
when_to_use: "Use when checking whether this convention applies to a CI failure."
---

# Scope

This convention applies to:

- All CI quality gates, including `test:quick` with Unit runtime and every applicable static
  `test:coverage:*` validator
- All projects in the Nx workspace
- All contributors: human developers and AI agents
- All branches: main, worktree branches, and PR branches

It does not apply to:

- Intentional test removals that are part of a documented refactoring plan (the plan itself must justify the removal)
- CI infrastructure failures unrelated to code (GitHub Actions outage, runner disk full, network timeout) -- these are operational issues, not code quality issues
