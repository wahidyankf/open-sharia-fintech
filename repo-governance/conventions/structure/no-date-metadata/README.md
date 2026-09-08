---
description: "Non-website markdown files must not contain manual date metadata of any kind. Git history is the single source of truth for when files changed and why."
when_to_use: "Read this index to find the right No Manual Date Metadata Convention child document."
---

# No Manual Date Metadata Convention

- [No Manual Date Metadata: Principles and Purpose](./principles-and-purpose.md) — The core principles this convention implements, and why manual updated fields, Last Updated footers, and inline date annotations were removed in favor of git history. Read this to understand why the repository bans manual date metadata before you go looking for where to record a file's last-changed date.
- [No Manual Date Metadata: Scope](./scope.md) — Which files this convention applies to, which website-content directories are exempt, and why the created field and in-content dates are unaffected. Read this when checking whether a specific file or directory (especially website content under apps/\*-www) is subject to this convention or exempt from it.
- [No Manual Date Metadata: Standards 1-3](./standards-1-to-3.md) — Standards 1 through 3 — no updated frontmatter field, no Last Updated footer blocks, and no misplaced Last Updated lines mid-document. Read this when checking a file's frontmatter block or its ending/mid-body content for a forbidden updated or Last Updated pattern.
- [No Manual Date Metadata: Standards 4-5](./standards-4-to-5.md) — Standard 4 (no inline date annotation lines in the document body) with worked FAIL/PASS examples, and Standard 5 (how to find the authoritative change date via git). Read this when checking a document body for inline Created/Last Updated/Version-date annotation lines, or when you need the git command to find a file's real last-changed date.
- [No Manual Date Metadata: Examples and Migration](./examples-and-migration.md) — Before/after examples for agent and convention files, plus the three-step migration checklist for removing existing date-metadata violations. Read this when cleaning up an existing file's date metadata or when you need a worked before/after comparison to model a fix on.
