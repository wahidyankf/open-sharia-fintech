---
title: "File Naming and Organization: Directory Structure and Naming"
description: "Defines the directory structure, file naming pattern, and the start of the mandatory Examples-by-Level section including per-level subheadings and bullet pattern."
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - by-example
  - education
  - code-first
created: 2025-12-25
when_to_use: "Read when scaffolding a new by-example tutorial's directory/files, or when writing the Examples by Level bullet list on overview.md."
---

# File Naming and Organization: Directory Structure and Naming

## Directory Structure

```
content/
└── en/
    └── learn/
        └── software-engineering/
            └── programming-language/
                └── {language}/
                    └── tutorials/
                        └── by-example/
                            ├── _index.md          # Landing page
                            ├── overview.md        # What is by-example, how to use
                            ├── beginner.md        # Examples 1-25/30
                            ├── intermediate.md    # Examples 26-50/60
                            └── advanced.md        # Examples 51-75/90
```

## File Naming Pattern

- `overview.md`: Always named "Overview" (weight: 10000000)
- `beginner.md`: Always named "Beginner" (weight: 10000001)
- `intermediate.md`: Always named "Intermediate" (weight: 10000002)
- `advanced.md`: Always named "Advanced" (weight: 10000003)

## Examples-by-Level Section (MANDATORY)

Every `overview.md` MUST contain a top-level section with the exact heading:

```markdown
## Examples by Level
```

### Per-level subheadings

Inside that section, each level gets a subheading in the form:

```markdown
### {Level} (Examples N–M)
```

where `{Level}` is exactly one of `Beginner`, `Intermediate`, `Advanced`, or `Production` (if the
tutorial uses a Production level), and `N–M` is the inclusive example range for that level using
an en-dash (`–`, U+2013).

### Bullet pattern

Every example that exists on a level page MUST appear as a bullet of this exact form:

```markdown
- [Example N: Title](/en/learn/.../<tutorial-base>/<level>#<github-slugger-slug>)
```

Rules:

- The link text (`Example N: Title`) MUST be copied verbatim from the `### Example N: Title`
  heading on the level page.
- The anchor (`#<github-slugger-slug>`) MUST be the slug produced by the `github-slugger` library
  against that exact heading text. This is the same algorithm the static site's `rehype-slug`
  plugin uses, so the anchor will work without modification.
- The path segment before the anchor MUST match the URL of the level page
  (e.g., `.../by-example/beginner`).
- No bullet may point to an anchor that does not exist on the target level page.
