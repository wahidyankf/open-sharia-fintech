---
title: "What This Applies To"
description: "The kinds of changes this convention covers and does not cover."
category: explanation
subcategory: development
tags:
  - feature-completeness
  - specs
  - contracts
  - testing
  - documentation
  - quality
created: 2026-04-04
when_to_use: "Use when deciding whether a specific change falls under this convention."
---

# What This Applies To

This convention applies to ALL changes that alter observable behavior:

| Change Type                                | Requires Artifact Updates?    | Which Artifacts?                       |
| ------------------------------------------ | ----------------------------- | -------------------------------------- |
| New feature                                | Yes                           | All applicable                         |
| Feature modification                       | Yes                           | All affected artifacts                 |
| Feature deletion                           | Yes                           | Remove/archive related artifacts       |
| Refactor that changes behavior             | Yes                           | Specs, tests, possibly contracts       |
| Refactor that preserves behavior           | No (behavior unchanged)       | None (unless tests need restructuring) |
| Bug fix that matches existing spec         | No (spec was already correct) | Tests only (add regression test)       |
| Bug fix that changes spec                  | Yes                           | Spec + tests + possibly contracts      |
| Dependency upgrade with no behavior change | No                            | None                                   |
| Dependency upgrade with behavior change    | Yes                           | All affected artifacts                 |
