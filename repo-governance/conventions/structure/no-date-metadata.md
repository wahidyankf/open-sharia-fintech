---
title: "No Manual Date Metadata Convention"
description: Non-website markdown files must not contain manual date metadata of any kind. Git history is the single source of truth for when files changed and why.
when_to_use: Read this before adding, reviewing, or removing any date field (updated, Last Updated, inline Created/Updated annotations) in a non-website markdown file.
category: explanation
subcategory: conventions
tags:
  - conventions
  - frontmatter
  - maintenance
  - git
created: 2026-04-25
---

# No Manual Date Metadata Convention

Non-website markdown files in this repository must not contain manual date metadata of any kind: no `updated:` frontmatter fields, no `**Last Updated**` footer blocks, and no inline body date annotations such as `- **Created**: YYYY-MM-DD` or `- **Last Updated**: YYYY-MM-DD`. Git history is the authoritative, drift-free record of when files changed and why. Manual date fields create maintenance overhead, drift the moment any file is touched, and add zero information value over what `git log` already provides.

## Contents

- [Principles and Purpose](./no-date-metadata/principles-and-purpose.md) — why manual date
  metadata was banned in favor of git history
- [Scope](./no-date-metadata/scope.md) — which files this applies to, which website content is
  exempt, and what stays unaffected
- [Standards 1-3](./no-date-metadata/standards-1-to-3.md) — no `updated:` frontmatter, no
  `**Last Updated**` footer blocks, no misplaced mid-body `**Last Updated**` lines
- [Standards 4-5](./no-date-metadata/standards-4-to-5.md) — no inline date annotation lines, and
  how to find the authoritative change date via git
- [Examples and Migration](./no-date-metadata/examples-and-migration.md) — worked before/after
  comparisons and the cleanup checklist
  related conventions

## No Manual Date Metadata: Tools and References

Enforcement agents and related documents for the
[No Manual Date Metadata Convention](./no-date-metadata.md).

### Tools and Automation

- **`rules-checker`** — validates that non-website markdown files do not contain `updated:` frontmatter, `**Last Updated**` footer blocks, or inline body date annotations
- **`rules-propagation`** — removes these fields from non-website files when found

### References

**Related Conventions:**

- [Convention Writing Convention](../writing/conventions.md) — meta-convention for how to structure convention documents; its frontmatter example must not include `updated:`
- [File Naming Convention](./file-naming.md) — kebab-case naming rules for all files

**Related Development Practices:**

- [AI Agents Convention](../../development/agents/ai-agents.md) — frontmatter field requirements for agent files; body annotation cleanup applies to agent files

**Agents:**

- `rules-checker` — enforces this convention during governance audits
- `rules-propagation` — removes disallowed fields from non-website files
