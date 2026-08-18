---
title: "Path Verification Checklist"
description: A pre-commit checklist for verifying AyoKoding relative-path links before committing documentation.
when_to_use: Use right before committing documentation that adds or edits an AyoKoding reference link.
category: explanation
subcategory: conventions
tags:
  - linking
  - cross-reference
  - relative-paths
  - portability
  - ayokoding-www
created: 2026-02-07
---

# Path Verification Checklist

Before committing documentation with AyoKoding references:

- [ ] All AyoKoding links use relative paths (no `https://ayokoding.com/...`)
- [ ] Path depth matches file location in docs/ hierarchy
- [ ] Paths use `/en/` language directory (not `/id/`)
- [ ] Paths point to existing directories in apps/ayokoding-www/content/
- [ ] Link text is descriptive and context-appropriate
- [ ] Links tested locally (navigate in file explorer or markdown preview)
