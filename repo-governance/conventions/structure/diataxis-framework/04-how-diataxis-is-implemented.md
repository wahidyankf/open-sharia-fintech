---
title: "How Diátaxis is Implemented"
description: The docs/ directory structure, directory-naming rationale, filename integration, and required frontmatter that implement Diátaxis in this repository.
when_to_use: Use when you need the concrete docs/ directory layout or frontmatter shape that implements Diátaxis.
category: explanation
subcategory: conventions
tags:
  - diataxis
  - documentation-framework
  - organization
  - conventions
created: 2025-11-22
---

# How Diátaxis is Implemented

## Directory Structure

```
docs/
├── tutorials/                                # Learning-oriented
│   ├── README.md                            # Category index
│   └── ...
├── how-to/                                   # Problem-oriented
│   ├── README.md                            # Category index
│   └── ...
├── reference/                                # Information-oriented
│   ├── README.md                            # Category index
│   └── ...
└── explanation/                              # Understanding-oriented
    ├── README.md                             # Category index
    └── conventions/
        ├── README.md                         # Subcategory index
        ├── file-naming-convention.md
        ├── linking-convention.md
        └── diataxis-framework.md (this file)
```

**Note on Directory Naming:**

The directory names follow semantic conventions:

- `tutorials/` is **plural** because tutorials are discrete, countable documents
- `how-to/` is the **category name** (singular) matching "How-to Guides" from Diátaxis
- `reference/` is a **mass noun** (like "reference library") representing reference material as a whole
- `explanation/` is a **mass noun** representing explanatory content as a collective

This is intentional and follows standard documentation naming conventions. See the [File Naming Convention](../file-naming.md) for more details.

## File Naming Integration

Category is conveyed by directory location (`docs/tutorials/`, `docs/how-to/`, etc.). Filenames use kebab-case and describe the content directly without prefix codes. See [File Naming Convention](../file-naming.md) for details, and [Ordinal Filename Prefixes](../ordinal-filename-prefixes.md) for the one case where a leading `NN-` ordinal is permitted (a real step in an ordered sequence).

## Frontmatter Standard

All documentation files include the category in frontmatter:

```yaml
---
title: "Document Title"
description: Brief description
category: tutorial # or how-to, reference, explanation
tags:
  - relevant-tags
created: YYYY-MM-DD
---
```
