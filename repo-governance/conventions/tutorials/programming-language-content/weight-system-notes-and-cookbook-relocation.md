---
description: "Wraps up the weight-system explanation and documents the cookbook's move from how-to/cookbook.md into the tutorials/cookbook/ folder."
when_to_use: "Use when you need the closing notes on the weight system, or when migrating a language's cookbook from the deprecated how-to/cookbook.md location."
---

# Weight System Notes and Cookbook Relocation

## Weight System Key Insight and Notes

**Key Insight: "Level" Has Two Meanings**

1. **Directory depth** (counting from /en/): golang/ is 5 steps from root
2. **Weight range** (powers of 10): level 5 uses 10000-99999, level 6 uses 100000-999999

The rule connects them: folder at directory depth N uses weight range N, content inside uses weight range N+1.

The level-based weight system above is the complete reference for ayokoding-www content navigation.

**Notes:**

- File names are FIXED (do not rename `beginner.md` to `basics.md`)
- Reference directory is placeholder for future API documentation
- All directories require `_index.md` and `overview.md`
- Weights follow powers of 10 progression: 10, 100, 1000, 10000, 100000, 1000000...

## Cookbook Location Change

**CRITICAL UPDATE (2026-01-30):** Cookbook has **MOVED** from `how-to/cookbook.md` to `tutorials/cookbook/` folder as **Component 5** of the Full Set Tutorial Package.

**Old Location (DEPRECATED):** `how-to/cookbook.md` at position 3 (weight: 1000001)
**New Location:** `tutorials/cookbook/` folder (weight: 1000002)

**Rationale for Move:**

1. **Part of Complete Educational Package**: Cookbook complements both learning tracks (by-concept and by-example)
2. **Used Alongside Tutorials**: Learners reference cookbook while studying tutorials, not as separate how-to guide
3. **Practical Learning Component**: Bridges theory (tutorials) with real-world problem-solving
4. **Consistent Organization**: All tutorial-related content in one location

**Migration Impact**: Languages currently with `how-to/cookbook.md` need migration to `tutorials/cookbook/` folder.

**New Cookbook Structure:**

```
# PASS: GOOD: Cookbook in tutorials/ folder as Component 5
tutorials/
├── _index.md           (100002) ← Level 6 (represents tutorials folder)
├── by-example/         (1000000) ← Level 7 (Component 3 - PRIORITY)
├── by-concept/         (1000001) ← Level 7 (Component 4)
├── cookbook/           (1000002) ← Level 7 (Component 5, NEW LOCATION)
│   ├── _index.md       (1000002) ← Represents cookbook folder
│   └── (recipes)       (10000000+) ← Level 8 content
├── initial-setup.md    (1000003) ← Level 7 (Component 1)
└── quick-start.md      (1000004) ← Level 7 (Component 2)
```

**Weight Calculation:**

Path: `/en/` (1) → `/learn/` (2) → `/swe/` (3) → `/programming-languages/` (4) → `/[language]/` (5) → `/tutorials/` (6) → `/cookbook/` (7)

- `cookbook/` is a **level 7 folder** (child of tutorials/)
- `cookbook/_index.md` represents the folder at level 7 → **weight: 1000002** (3rd child in tutorials/)
- Recipe files inside cookbook/ → **weight: 10000000+** (level 8 content)
