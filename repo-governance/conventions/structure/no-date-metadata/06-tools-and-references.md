---
title: "No Manual Date Metadata: Tools and References"
description: The agents that enforce this convention, and links to the related conventions and development practices that cross-reference it.
when_to_use: Read this when you need the enforcing agent names or the related-convention links for this rule.
category: explanation
subcategory: conventions
tags:
  - conventions
  - frontmatter
  - maintenance
  - git
created: 2026-04-25
---

# No Manual Date Metadata: Tools and References

Enforcement agents and related documents for the
[No Manual Date Metadata Convention](../no-date-metadata.md).

## Tools and Automation

- **`repo-rules-checker`** — validates that non-website markdown files do not contain `updated:` frontmatter, `**Last Updated**` footer blocks, or inline body date annotations
- **`repo-rules-fixer`** — removes these fields from non-website files when found

## References

**Related Conventions:**

- [Convention Writing Convention](../../writing/conventions.md) — meta-convention for how to structure convention documents; its frontmatter example must not include `updated:`
- [File Naming Convention](../file-naming.md) — kebab-case naming rules for all files

**Related Development Practices:**

- [AI Agents Convention](../../../development/agents/ai-agents.md) — frontmatter field requirements for agent files; body annotation cleanup applies to agent files

**Agents:**

- `repo-rules-checker` — enforces this convention during governance audits
- `repo-rules-fixer` — removes disallowed fields from non-website files
