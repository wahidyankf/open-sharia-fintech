---
title: "Universal Directory Structure"
description: "The mandatory directory tree every programming language must follow on ayokoding-www."
category: explanation
subcategory: conventions
tags:
  - programming-languages
  - ayokoding
  - tutorials
  - education
  - content-standards
created: 2025-12-18
when_to_use: "Use when scaffolding or auditing a language's content folder/file layout."
---

# Universal Directory Structure

Every programming language MUST follow this structure:

```
[language]/                                    # Level 5 folder (e.g., /en/learn/swe/programming-languages/golang/)
├── _index.md                                  # Folder (weight: 10002, level 5 - represents the folder)
├── overview.md                                # Content (weight: 100000, level 6 - content inside level 5 folder)
├── tutorials/                                 # Folder (weight: 100002, level 6 - represents the folder)
│   ├── _index.md                             # Folder (weight: 100002, level 6 - represents the folder)
│   ├── by-example/                           # COMPONENT 3: Code-first path (Level 7 folder) - PRIORITY
│   │   ├── _index.md                         # Folder (weight: 1000000, level 7 - represents the folder)
│   │   ├── overview.md                       # Content (weight: 10000000, level 8 - content inside level 7 folder)
│   │   ├── beginner.md                       # Content (weight: 10000001, level 8 - Examples 1-25)
│   │   ├── intermediate.md                   # Content (weight: 10000002, level 8 - Examples 26-50)
│   │   └── advanced.md                       # Content (weight: 10000003, level 8 - Examples 51-75)
│   ├── by-concept/                           # COMPONENT 4: Narrative-driven path (Level 7 folder)
│   │   ├── _index.md                         # Folder (weight: 1000001, level 7 - represents the folder)
│   │   ├── overview.md                       # Content (weight: 10000000, level 8 - content inside level 7 folder)
│   │   ├── beginner.md                       # Content (weight: 10000001, level 8 - 0-40% coverage)
│   │   ├── intermediate.md                   # Content (weight: 10000002, level 8 - 40-75% coverage)
│   │   └── advanced.md                       # Content (weight: 10000003, level 8 - 75-95% coverage)
│   ├── cookbook/                             # COMPONENT 5: Practical recipes (Level 7 folder)
│   │   └── _index.md                         # Folder (weight: 1000002, level 7 - represents the folder)
│   ├── initial-setup.md                      # COMPONENT 1: Foundational (0-5%, weight: 1000003, level 7)
│   └── quick-start.md                        # COMPONENT 2: Foundational (5-30%, weight: 1000004, level 7)
├── how-to/                                    # Folder (weight: 100003, level 6 - represents the folder)
│   ├── _index.md                             # Folder (weight: 100003, level 6 - represents the folder)
│   ├── overview.md                           # Content (weight: 1000000, level 7 - content inside level 6 folder)
│   ├── best-practices.md                     # Content (weight: 1000001, level 7 - MOVED UP from position 3)
│   └── [12-18 problem-solving guides]        # Content (weight: 1000002+, level 7)
├── explanation/                               # Folder (weight: 100004, level 6 - represents the folder)
│   ├── _index.md                             # Folder (weight: 100004, level 6 - represents the folder)
│   ├── overview.md                           # Content (weight: 1000000, level 7 - content inside level 6 folder)
│   ├── best-practices.md                     # Content (weight: 1000001, level 7)
│   └── anti-patterns.md                      # Content (weight: 1000002, level 7)
└── reference/                                 # Folder (weight: 100005, level 6 - represents the folder)
    ├── _index.md                             # Folder (weight: 100005, level 6 - represents the folder)
    └── overview.md                           # Content (weight: 1000000, level 7 - content inside level 6 folder)
```
