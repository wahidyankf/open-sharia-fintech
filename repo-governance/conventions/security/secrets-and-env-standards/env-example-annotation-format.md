---
title: ".env.example Annotation Format"
description: The required comment-block format preceding every env var line in a .env.example template — REQUIRED/OPTIONAL, type, description, and placeholder rules.
when_to_use: Use when adding or editing a line in any apps/<app>/.env.example file.
category: explanation
subcategory: conventions
tags:
  - security
  - secrets
  - env-files
  - guard-env-file-access
  - naming
  - reproducibility
created: 2026-06-10
---

# .env.example Annotation Format

Every env var line is preceded by a comment block:

```
# REQUIRED | <type> | <description>
# Format: <format note>
KEY=obviously-dev-placeholder

# OPTIONAL | <type> | <description> (default: <value>)
# OPTIONAL_KEY=
```

Rules:

- `REQUIRED` or `OPTIONAL` (no other values).
- Type is the runtime type: `string`, `u16`, `boolean`, `url`.
- Description is one short phrase; format notes go on a second `# Format:` line.
- **Required vars**: active line with an obviously-dev placeholder value (never a real secret).
- **Optional vars**: commented-out line (`# KEY=`), so the template is parseable without forcing
  developers to set non-required vars.
- Placeholders must be obviously fake: `postgres://postgres:postgres@localhost:5432/appname` is
  obviously local; `your-api-key-here` is obviously a placeholder.
