---
title: "Convention Document Structure — Required Sections"
description: The required frontmatter, introduction, Principles Implemented/Respected, Purpose, Scope, and Standards sections every convention document must include.
when_to_use: Use when drafting a new convention document and assembling its mandatory sections.
category: explanation
subcategory: conventions
tags:
  - meta
  - conventions
  - standards
  - documentation
created: 2025-12-07
---

# Convention Document Structure — Required Sections

All convention documents SHOULD follow this structure. This page defines the required sections; see [Recommended and Optional Sections](./03-document-structure-recommended-and-optional-sections.md) for the rest.

## 1. Frontmatter (YAML)

```yaml
---
title: "Convention Name"
description: Brief description of what this convention covers
category: explanation
subcategory: conventions
tags:
  - relevant
  - tags
created: YYYY-MM-DD
---
```

**Requirements:**

- Title uses Title Case and includes "Convention" for clarity
- Description is 1-2 sentences explaining the convention's purpose
- Category is always `explanation`
- Subcategory is always `conventions`
- Tags help with discoverability (3-5 tags)
- `created` uses `YYYY-MM-DD` format (date-only, not full timestamp)
- `updated:` field MUST NOT be included — per [No Manual Date Metadata Convention](../../structure/no-date-metadata.md), git history is the authoritative change record

## 2. Introduction (H1 + opening paragraph)

```markdown
# Convention Name

Brief overview explaining what this convention covers and why it exists.
1-3 paragraphs maximum.
```

**Purpose:** Immediately orient readers to the convention's scope and value.

## 3. Principles Implemented/Respected Section (H2)

```markdown
## Principles Implemented/Respected

This convention implements/respects the following core principles:

- **[Principle Name](../../principles/[category]/[name].md)**: Brief explanation of HOW this convention implements or respects this principle. What specific aspect of the principle does this convention embody?
- **[Another Principle](../../principles/[category]/[name].md)**: Another explanation.
```

**Purpose:** Explicit traceability from documentation standards back to foundational values. Makes governance hierarchy visible and verifiable.

**Requirements:**

- List ALL principles this convention implements or respects
- Include working link to each principle document
- Explain HOW the convention embodies each principle (not just listing names)
- Use relative paths: `../principles/[category]/[name].md`

**Note:** This section is MANDATORY for all convention documents. It enables traceability validation and ensures conventions trace back to foundational values.

## 4. Purpose Section (H2)

```markdown
## Purpose

Clearly state WHY this convention exists and what problems it solves.
Include the intended audience and use cases.
```

## 5. Scope Section (H2)

```markdown
## Scope

### What This Convention Covers

- Bulleted list of included topics

### What This Convention Does NOT Cover

- Bulleted list of excluded topics (with references to appropriate conventions)
```

**Note:** Explicit exclusions prevent scope creep and guide readers to related conventions.

## 6. Standards/Rules Section (H2)

```markdown
## Standards

Detailed requirements, rules, or guidelines. Use subsections (H3) to organize.

### Subsection 1

Content with examples

### Subsection 2

More guidance with concrete examples.
```

**Tips:**

- Break complex topics into digestible subsections
- Use clear, imperative language ("Use X", "Never do Y")
- Provide rationale for non-obvious rules
