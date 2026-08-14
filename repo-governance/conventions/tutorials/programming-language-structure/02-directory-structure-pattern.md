---
title: "Directory Structure Pattern"
description: Directory tree layouts for dual-path languages (by-example plus by-concept) versus single-path languages (by-concept only).
when_to_use: Use when scaffolding or reviewing a language's tutorials/ directory tree.
category: explanation
subcategory: conventions
tags:
  - programming-languages
  - tutorials
  - ayokoding-www
  - education
  - structure
created: 2025-12-27
---

# Directory Structure Pattern

## Dual-Path Languages (Java, Elixir, Golang)

Languages with both learning paths:

```
[language]/tutorials/                          # Level 6 folder
├── _index.md                                  # Navigation hub (weight: 100002)
├── by-example/                                # COMPONENT 3: Code-first path (Level 7 folder) - PRIORITY
│   ├── _index.md                              # Navigation hub (weight: 1000000)
│   ├── overview.md                            # Path introduction (weight: 10000000)
│   ├── beginner.md                            # Examples 1-25 (weight: 10000001)
│   ├── intermediate.md                        # Examples 26-50 (weight: 10000002)
│   └── advanced.md                            # Examples 51-75 (weight: 10000003)
├── by-concept/                                # COMPONENT 4: Narrative-driven path (Level 7 folder)
│   ├── _index.md                              # Navigation hub (weight: 1000001)
│   ├── overview.md                            # Path introduction (weight: 10000000)
│   ├── beginner.md                            # 0-40% coverage (weight: 10000001)
│   ├── intermediate.md                        # 40-75% coverage (weight: 10000002)
│   └── advanced.md                            # 75-95% coverage (weight: 10000003)
├── cookbook/                                  # COMPONENT 5: Practical recipes (Level 7 folder)
│   ├── _index.md                              # Navigation hub (weight: 1000002)
│   └── (recipe files organized by category)
├── initial-setup.md                           # COMPONENT 1: Foundational (0-5%, weight: 1000003)
└── quick-start.md                             # COMPONENT 2: Foundational (5-30%, weight: 1000004)

Note: By-example prioritized (weight 1000000) before by-concept (weight 1000001) for faster learning
```

## Single-Path Languages (Kotlin, Python, Rust)

Languages with only by-concept path (by-example not yet created):

```
[language]/tutorials/                          # Level 6 folder
├── _index.md                                  # Navigation hub (weight: 100002)
├── by-concept/                                # Narrative-driven path (Level 7 folder)
│   ├── _index.md                              # Navigation hub (weight: 1000000)
│   ├── overview.md                            # Path introduction (weight: 10000000)
│   ├── beginner.md                            # 0-60% coverage (weight: 10000001)
│   ├── intermediate.md                        # 60-85% coverage (weight: 10000002)
│   └── advanced.md                            # 85-95% coverage (weight: 10000003)
├── initial-setup.md                           # Foundational (0-5%, weight: 1000002)
└── quick-start.md                             # Foundational (5-30%, weight: 1000003)
```
