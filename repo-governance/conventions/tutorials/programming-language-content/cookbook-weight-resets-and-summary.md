---
description: "Shows how sibling category folders independently reset their child weights, and summarizes the full level-based weight system."
when_to_use: "Use when you need to confirm that two sibling files can safely share the same weight number, or want a one-glance summary of the weight system."
---

# Cookbook Weight Resets and Summary

**Understanding Weight Resets Across Sibling Folders:**

```
# PASS: GOOD: Category folders at level 6, content inside at level 7 with resets
tutorials/
├── _index.md           (100002) ← Level 6 (represents tutorials folder, 3rd sibling)
├── overview.md         (1000000) ← Level 7 base (content inside tutorials/)

how-to/
├── _index.md           (100003) ← Level 6 (represents how-to folder, 4th sibling)
├── overview.md         (1000000) ← Level 7 base RESET (different parent, content inside how-to/)

explanation/
├── _index.md           (100004) ← Level 6 (represents explanation folder, 5th sibling)
├── overview.md         (1000000) ← Level 7 base RESET (different parent, content inside explanation/)

reference/
├── _index.md           (100005) ← Level 6 (represents reference folder, 6th sibling)
├── overview.md         (1000000) ← Level 7 base RESET (different parent, content inside reference/)
```

**RESET Explanation:** Different parent folders independently use the same base weight (1000000) for their children. Navigation only compares siblings (files with the same parent), so `tutorials/overview.md` (1000000) and `how-to/overview.md` (1000000) never conflict - they have different parents and appear in different navigation contexts.

**Weight System Summary:**

- **Level 5** (language folder): Language folder's `_index.md` at 10002
- **Level 6** (content inside language folder): `overview.md` at 100000, category folders' `_index.md` at 100002, 100003, 100004...
- **Level 7** (content inside category folders): 1000000, 1000001, 1000002... (resets per category parent)
- Follows ayokoding-www's level-based system: folder at level N has `_index.md` at level N, content inside at level N+1
