---
title: "Navigation Pattern: Weight Values"
description: The level-based weight-value system for tutorials/, by-example/, by-concept/, and cookbook/ folders and their content files.
when_to_use: Use when assigning or auditing weight values for a language's tutorial folders and files.
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

# Navigation Pattern: Weight Values

Uses ayokoding-www's level-based weight system with powers of 10 ranges:

**Path Calculation:**

```
/en/ (1) → /learn/ (2) → /software-engineering/ (3) → /programming-language/ (4) → /[language]/ (5) → /tutorials/ (6)
```

**tutorials/ is level 6 folder**:

- `tutorials/_index.md`: `weight: 100002` (level 6 - represents the folder)
- Content INSIDE tutorials/ uses level 7 (1000000, 1000001, 1000002...)

**by-example/ is level 7 folder** (child of tutorials/) - **PRIORITY**:

- `by-example/_index.md`: `weight: 1000000` (level 7 - first child, represents folder)
- Content INSIDE by-example/ uses level 8 (10000000, 10000001...)

**by-concept/ is level 7 folder** (child of tutorials/):

- `by-concept/_index.md`: `weight: 1000001` (level 7 - second child, represents folder)
- Content INSIDE by-concept/ uses level 8 (10000000, 10000001...)

**cookbook/ is level 7 folder** (child of tutorials/):

- `cookbook/_index.md`: `weight: 1000002` (level 7 - third child, represents folder)
- Content INSIDE cookbook/ uses level 8 (10000000, 10000001...)

**Foundational files are level 7 content** (children of tutorials/):

- `initial-setup.md`: `weight: 1000003` (level 7 - fourth child)
- `quick-start.md`: `weight: 1000004` (level 7 - fifth child)

**Complete Weight Example (Full Set Tutorial Package):**

```
tutorials/
├── _index.md                # weight: 100002 (level 6 - represents folder)
├── by-example/              # Component 3 - PRIORITY (move fast)
│   ├── _index.md            # weight: 1000000 (level 7 - first child, represents folder)
│   ├── overview.md          # weight: 10000000 (level 8 - content inside by-example/)
│   ├── beginner.md          # weight: 10000001 (level 8)
│   ├── intermediate.md      # weight: 10000002 (level 8)
│   └── advanced.md          # weight: 10000003 (level 8)
├── by-concept/              # Component 4 - learn deep
│   ├── _index.md            # weight: 1000001 (level 7 - second child, represents folder)
│   ├── overview.md          # weight: 10000000 (level 8 - RESET, different parent)
│   ├── beginner.md          # weight: 10000001 (level 8)
│   ├── intermediate.md      # weight: 10000002 (level 8)
│   └── advanced.md          # weight: 10000003 (level 8)
├── cookbook/                # Component 5 - practical recipes
│   └── _index.md            # weight: 1000002 (level 7 - third child)
├── initial-setup.md         # Component 1 - weight: 1000003 (level 7 - fourth child)
└── quick-start.md           # Component 2 - weight: 1000004 (level 7 - fifth child)
```

**Key Rules:**

1. **Folder's `_index.md`** represents the folder itself at level N → uses level N weight
2. **Content INSIDE folder** is one level deeper → uses level N+1 base weight
3. **Weights RESET per parent**: by-concept/ and by-example/ both start at 10000000 for overview.md (different parents, independent sequences)

See the ayokoding-www developing content skill for complete level-based weight system details.
