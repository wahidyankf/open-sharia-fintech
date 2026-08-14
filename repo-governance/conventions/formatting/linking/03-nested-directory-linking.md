---
title: "Nested Directory Linking"
description: How to calculate the correct number of ../ segments for a relative link based on file nesting depth, with a depth reference table and worked patterns.
when_to_use: Use when writing a relative link between files at different nesting depths and you need to count the correct number of ../ segments.
category: explanation
subcategory: conventions
tags:
  - linking
  - markdown
  - conventions
  - github-compatibility
created: 2025-11-22
---

# Nested Directory Linking

Understanding relative paths is crucial when linking from files at different nesting depths. The number of `../` you need depends on how deep your current file is nested.

## How to Calculate Relative Paths

1. **Count how many directories deep your current file is** from the `docs/` root
2. **Use that many `../` to reach the `docs/` root**
3. **Then navigate down** to your target file

## Nesting Depth Reference

| File Location                                          | Depth from `docs/` | To reach `docs/` root |
| ------------------------------------------------------ | ------------------ | --------------------- |
| `docs/README.md`                                       | 0 (at root)        | `.` (current dir)     |
| `docs/tutorials/README.md`                             | 1 level deep       | `../`                 |
| `repo-governance/conventions/README.md`                | 2 levels deep      | `../../`              |
| `repo-governance/conventions/formatting/linking.md`    | 3 levels deep      | `../../../`           |
| `repo-governance/principles/software-engineering/*.md` | 3 levels deep      | `../../../`           |

## Common Linking Patterns

### From 1-Level Deep Files (`docs/explanation/README.md`)

```markdown
<!-- To sibling directories (same level) -->

[Conventions](./README.md)
[Development](./README.md)

<!-- To parent (docs/ root) -->

[Documentation Home](./README.md)

<!-- To other categories (up 1, down 1) -->

[Tutorials](./README.md)
[How-To](./README.md)
```

### From 3-Level Deep Files (`repo-governance/conventions/formatting/linking.md`)

```markdown
<!-- To docs/ root (up 3 levels) -->

[Documentation Home](./README.md)

<!-- To other categories (up 3, down 1) -->

[Tutorials](./README.md)
[How-To](./README.md)

<!-- To sibling files (same directory) -->

[File Naming Convention](../structure/file-naming.md)
```

### From 3-Level Deep Files (`repo-governance/principles/software-engineering/explicit-over-implicit.md`)

```markdown
<!-- To docs/ root (up 3 levels) -->

[Documentation Home](./README.md)

<!-- To other categories (up 3, down 1 or 2) -->

[Tutorials](./README.md)
[Conventions](./README.md)

<!-- To parent categories (up 1, 2, or 3) -->

[Software Engineering Principles](./README.md) <!-- Parent directory -->
[All Principles](./README.md) <!-- Grandparent directory -->
[Explanation Index](../../docs/explanation/README.md) <!-- Great-grandparent -->
```

## Verification Tip

To verify your relative path is correct:

1. **Start at your current file's location**
2. **Count each `../` as going up one directory level**
3. **Count each `/dirname/` as going down one level**
4. **Verify you end at the target file**

Example from `repo-governance/conventions/structure/file-naming.md` to `docs/tutorials/README.md`:

```
Start:  repo-governance/conventions/structure/file-naming.md
  ../   repo-governance/conventions/structure/ → repo-governance/conventions/   (up 1)
  ../   repo-governance/conventions/ → repo-governance/                         (up 2)
  ../   repo-governance/ → / (repo root)                                   (up 3)
  docs/tutorials/README.md                                            (down into target)

Final path: ../../../docs/tutorials/README.md
```
