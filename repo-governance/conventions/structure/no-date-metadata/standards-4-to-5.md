---
description: Standard 4 (no inline date annotation lines in the document body) with worked FAIL/PASS examples, and Standard 5 (how to find the authoritative change date via git).
when_to_use: Read this when checking a document body for inline Created/Last Updated/Version-date annotation lines, or when you need the git command to find a file's real last-changed date.
---

# No Manual Date Metadata: Standards 4-5

Standards 4 and 5 enforced by the
[No Manual Date Metadata Convention](../no-date-metadata.md).

## Standard 4: No Inline Date Annotations in Document Body

Non-website markdown files MUST NOT contain standalone inline date annotation lines in the document body. These are lines that exist solely to record metadata dates for human readers, not actual document content.

The most common patterns to remove:

- `- **Created**: YYYY-MM-DD`
- `- **Last Updated**: YYYY-MM-DD`
- `**Created**: YYYY-MM-DD` (standalone line, not part of a content paragraph)
- `**Version**: x.y — YYYY-MM-DD` (version-date annotation lines)

FAIL — forbidden inline body annotations in agent files:

```markdown
## Agent Metadata

- **Role**: Maker (blue)
- **Created**: 2025-12-01
- **Last Updated**: 2026-04-19
```

PASS — correct (remove the date annotation lines, keep the role):

```markdown
## Agent Metadata

- **Role**: Maker (blue)
```

FAIL — forbidden in convention documents:

```markdown
## Document History

- **Created**: 2025-11-22
- **Last Updated**: 2026-04-19
```

PASS — correct (remove the section entirely or keep only non-date content):

The section adds nothing git does not provide. Remove it.

**Important distinction**: This rule targets standalone metadata annotation lines. A date mentioned inside an actual content paragraph — for example, "This pattern was introduced in the 2025-12-01 refactor" — is content, not a metadata annotation, and is unaffected.

## Standard 5: How to Find the Authoritative Change Date

Use git to find when a file was last changed:

```bash
git log --follow --oneline -1 -- path/to/file.md
git log --follow --format="%ad %s" --date=short -- path/to/file.md
```

This gives the date, commit message, and full context — far more informative than a bare date in frontmatter or an inline annotation.
