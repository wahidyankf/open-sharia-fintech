---
description: "How to compute Hugo navigation weights for programming language content, based on directory depth and per-parent weight ranges."
when_to_use: "Use when assigning or auditing the `weight` frontmatter value for a folder's `_index.md` or a content file in the programming-language content tree."
---

# Weight System Explanation

Programming language folders (e.g., `golang/`, `python/`, `java/`) are at **level 5** in the directory hierarchy:

```
/en/ (level 1) → /learn/ (level 2) → /swe/ (level 3) → /programming-languages/ (level 4) → /golang/ (level 5)
```

**Understanding Levels and Weights:**

The level-based weight system uses a two-part rule:

1. **Folder's `_index.md`** represents the folder itself at level N → uses level N weight
2. **Content INSIDE the folder** is one level deeper → uses level N+1 base weight

**Why This Design?**

- `_index.md` IS the folder (navigation hub) → uses the folder's own level
- Regular content files LIVE INSIDE the folder → one level deeper in hierarchy
- Navigation compares siblings only → weights reset independently per parent

**Detailed Weight Calculation:**

- **Level 5 folder** (`golang/`, `python/`, `java/`):
  - These folders exist at level 5 in the directory tree
  - Each folder's `_index.md` represents the folder at level 5 → **weight: 10002** (level 5 range: 10000-99999)
  - Why 10002? Because golang/ might be the 3rd language among siblings (first is 10000, second is 10001, third is 10002)

- **Level 6 content** (files INSIDE the level 5 language folder):
  - Content inside a level 5 folder is one level deeper → uses **level 6 base: 100000** (level 6 range: 100000-999999)
  - `overview.md`: **100000** (first content file, uses level 6 base)
  - `tutorials/_index.md`: **100002** (represents the tutorials folder at level 6, 3rd sibling among category folders)
  - `how-to/_index.md`: **100003** (represents the how-to folder at level 6, 4th sibling)
  - `explanation/_index.md`: **100004** (represents the explanation folder at level 6, 5th sibling)
  - `reference/_index.md`: **100005** (represents the reference folder at level 6, 6th sibling)

- **Level 7 content** (files INSIDE the level 6 category folders):
  - Content inside level 6 folders is one level deeper → uses **level 7 base: 1000000** (level 7 range: 1000000-9999999)
  - **CRITICAL: Weights RESET per parent** - Each category folder's children independently start at 1000000
  - `tutorials/by-example/`: **1000000** (first folder in tutorials/, Component 3 - PRIORITY)
  - `tutorials/by-concept/`: **1000001** (second folder in tutorials/, Component 4)
  - `tutorials/cookbook/`: **1000002** (third folder in tutorials/, Component 5)
  - `tutorials/initial-setup.md`: **1000003** (fourth item, Component 1)
  - `tutorials/quick-start.md`: **1000004** (fifth item, Component 2)
  - `how-to/overview.md`: **1000000** (RESET - different parent, content inside how-to/ folder)
  - `explanation/overview.md`: **1000000** (RESET - different parent, content inside explanation/ folder)
  - `reference/overview.md`: **1000000** (RESET - different parent, content inside reference/ folder)
