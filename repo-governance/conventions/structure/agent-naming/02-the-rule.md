---
title: "Agent Naming Convention — The Rule"
description: The scope-qualifier-role filename structure every agent filename must match, and how it inherits from the File Naming Convention.
when_to_use: Use when you need the exact filename structure required for a new or renamed agent.
category: explanation
subcategory: conventions
tags:
  - agents
  - naming
  - conventions
created: 2026-04-17
---

# The Rule

Every agent filename (basename without the `.md` extension) MUST match the structure:

```text
<scope>(-<qualifier>)*-<role>
```

Token definitions:

- **`<scope>`** — Exactly one token from the [Scope Vocabulary](./03-scope-vocabulary.md#scope-vocabulary) below. Names the domain or subsystem the agent operates in. Appears first.
- **`<qualifier>`** — Zero or more lowercase kebab tokens narrowing the scope. Each qualifier is a single hyphen-separated word or a compound kebab phrase (e.g., `ayokoding-web`, `by-example`, `file`). Qualifiers stack in order from broadest to narrowest. Each qualifier token must be `[a-z0-9]+` and separated from its neighbours by single hyphens.
- **`<role>`** — Exactly one token from the [Role Vocabulary](./04-role-vocabulary.md#role-vocabulary) below. Names the functional responsibility. Appears last.

**No exceptions.** Every agent has exactly one scope (first) and exactly one role (last); everything between is qualifier. Filenames that cannot be parsed against this structure are governance violations regardless of history, context, or convenience.

Additional filename rules inherit from the [File Naming Convention](../file-naming.md): lowercase ASCII, digits and hyphens only, single `.md` extension, no leading or trailing hyphens, case-insensitively unique within the directory.
