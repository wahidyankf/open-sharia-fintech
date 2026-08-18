---
title: "How It Applies"
description: Five worked contrasts (structure, agents, frontmatter, docs, conventions) of simple versus complex choices.
category: explanation
subcategory: principles
tags:
  - principles
  - simplicity
  - over-engineering
created: 2025-12-15
when_to_use: Use when you need a concrete before/after example for a specific decision.
---

# How It Applies

## Flat Library Structure

**Context**: Organizing libraries in `libs/` directory.

PASS: **Simple (Correct)**:

```
libs/
├── ts-validation/
├── ts-auth/
├── ts-database/
└── ts-api-client/
```

**Why this works**: Flat structure. Easy to find libraries. No mental model of hierarchy needed.

FAIL: **Complex (Avoid)**:

```
libs/
├── shared/
│   ├── core/
│   │   ├── validation/
│   │   └── auth/
│   └── utils/
│       ├── database/
│       └── api/
└── features/
    └── user/
        └── data-access/
```

**Why this fails**: Deep nesting. Requires understanding the categorization scheme. Hard to find things. Premature organization.

## Single-Purpose AI Agents

**Context**: Agent responsibilities.

PASS: **Simple (Correct)**:

```
docs-maker.md - Creates documentation
docs-checker.md - Validates documentation
```

**Why this works**: One agent, one job. Clear responsibility. Easy to invoke.

FAIL: **Complex (Avoid)**:

```
docs-manager.md - Creates, validates, fixes, organizes, and links documentation
```

**Why this fails**: Multi-purpose agent. Hard to predict behavior. Unclear when to use.

## Minimal Frontmatter

**Context**: Document metadata.

PASS: **Simple (Correct)**:

```yaml
---
title: Document Title
description: Brief description
category: explanation
tags:
  - tag1
  - tag2
created: 2025-12-15
---
```

**Why this works**: Only essential fields. No unnecessary metadata. Self-explanatory.

FAIL: **Complex (Avoid)**:

```yaml
---
title: Document Title
subtitle: Additional subtitle
description: Brief description
long_description: Very long description
category: explanation
subcategory: principles
sub_subcategory: philosophy
tags:
  - tag1
  - tag2
keywords: [word1, word2, word3]
author: Name
contributors: [Name1, Name2]
version: 1.0.0
status: published
priority: high
visibility: public
license: MIT
created: 2025-12-15
reviewed: 2025-12-15
approved: 2025-12-15
next_review: 2026-01-15
---
```

**Why this fails**: Too many fields. Most are unused. Maintenance burden. Analysis paralysis deciding which fields to fill.

## Direct Markdown Over Templating

**Context**: Documentation format.

PASS: **Simple (Correct)**:

```markdown
# Document Title

## Section

Content here...
```

**Why this works**: Standard markdown. Works everywhere. Easy to write and read.

FAIL: **Complex (Avoid)**:

```
{{< section title="Section" >}}
  {{< content type="text" >}}
    Content here...
  {{< /content >}}
{{< /section >}}
```

**Why this fails**: Custom templating syntax. Requires learning. Not portable. Over-engineered.

## Convention Documents Over Frameworks

**Context**: Establishing standards.

PASS: **Simple (Correct)**:

```
repo-governance/conventions/
  file-naming-convention.md
  linking-convention.md
```

**Why this works**: Markdown documents. Searchable. Easy to update. Human-readable.

FAIL: **Complex (Avoid)**:

```
.conventions/
  schema.json
  rules.yaml
  validators/
    file-naming.ts
    linking.ts
  generators/
    scaffold.ts
```

**Why this fails**: Over-engineered framework. Requires tooling. Harder to understand and modify. Building a system before validating need.
