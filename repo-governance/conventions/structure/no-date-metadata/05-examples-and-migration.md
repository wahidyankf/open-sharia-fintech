---
title: "No Manual Date Metadata: Examples and Migration"
description: Before/after examples for agent and convention files, plus the three-step migration checklist for removing existing date-metadata violations.
when_to_use: Read this when cleaning up an existing file's date metadata or when you need a worked before/after comparison to model a fix on.
category: explanation
subcategory: conventions
tags:
  - conventions
  - frontmatter
  - maintenance
  - git
created: 2026-04-25
---

# No Manual Date Metadata: Examples and Migration

Worked examples and the migration checklist for the
[No Manual Date Metadata Convention](../no-date-metadata.md).

## Examples

### Agent File — Before and After

FAIL — agent body with inline date annotations:

```markdown
## Agent Metadata

- **Role**: Maker (blue)
- **Created**: 2025-12-01
- **Last Updated**: 2026-03-15

**Model Selection Justification**: ...
```

PASS — agent body without date annotations:

```markdown
## Agent Metadata

- **Role**: Maker (blue)

**Model Selection Justification**: ...
```

### Convention File — Before and After

FAIL — convention with `updated:` frontmatter:

```yaml
---
title: "Example Convention"
description: An example.
category: explanation
subcategory: conventions
created: 2025-11-22
---
```

PASS — convention without `updated:` frontmatter:

```yaml
---
title: "Example Convention"
description: An example.
category: explanation
subcategory: conventions
created: 2025-11-22
---
```

## Migration

All existing violations in non-website files should be removed:

1. Remove `updated:` from YAML frontmatter
2. Remove `**Last Updated**` footer blocks (including the preceding `---` separator if it was added solely for the footer)
3. Remove standalone inline body date annotation lines (`- **Created**: date`, `- **Last Updated**: date`, etc.)

No replacement content is needed for any of these removals. The information they contained is already in git history.

When removing a `---` footer separator, confirm it is the final `---` in the file and not the YAML frontmatter closing delimiter or a section horizontal rule inside the document body. The safe pattern is: `\n---\n\n**Last Updated**:` appearing at or near the end of the file.
