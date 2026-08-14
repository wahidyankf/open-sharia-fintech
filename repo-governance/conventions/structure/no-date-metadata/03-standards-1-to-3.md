---
title: "No Manual Date Metadata: Standards 1-3"
description: Standards 1 through 3 — no updated frontmatter field, no Last Updated footer blocks, and no misplaced Last Updated lines mid-document.
when_to_use: Read this when checking a file's frontmatter block or its ending/mid-body content for a forbidden updated or Last Updated pattern.
category: explanation
subcategory: conventions
tags:
  - conventions
  - frontmatter
  - maintenance
  - git
created: 2026-04-25
---

# No Manual Date Metadata: Standards 1-3

The first three standards enforced by the
[No Manual Date Metadata Convention](../no-date-metadata.md).

## Standard 1: No `updated:` in YAML Frontmatter

Non-website markdown files MUST NOT contain an `updated:` field in their YAML frontmatter block.

FAIL — forbidden:

```yaml
---
title: "Example Convention"
created: 2025-11-22
updated: 2026-04-19
---
```

PASS — correct:

```yaml
---
title: "Example Convention"
created: 2025-11-22
---
```

## Standard 2: No `**Last Updated**` Footer Blocks

Non-website markdown files MUST NOT contain a `**Last Updated**` footer block. The typical pattern is a `---` horizontal rule separator followed by a `**Last Updated**: YYYY-MM-DD` line at the end of the file — both the separator and the line must be absent.

FAIL — forbidden (at end of file):

```markdown
...last paragraph of content...

---

**Last Updated**: 2026-04-19
```

PASS — correct (file ends after last content paragraph):

```markdown
...last paragraph of content...
```

## Standard 3: Misplaced `**Last Updated**` Lines Must Also Be Removed

Some files have `**Last Updated**` embedded in the middle of the document body rather than at the end. These must also be removed regardless of position.
