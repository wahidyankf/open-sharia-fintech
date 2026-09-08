---
description: The required frontmatter, introduction, Principles Implemented/Respected, Purpose, Scope, and Standards sections every convention document must include.
when_to_use: Use when drafting a new convention document and assembling its mandatory sections.
---

# Convention Document Structure — Required Sections

All convention documents SHOULD follow this structure. This page defines the required sections; see [Recommended and Optional Sections](./document-structure-recommended-and-optional-sections.md) for the rest.

## 1. Frontmatter (YAML)

```yaml
---
description: Brief description of what this convention covers
when_to_use: Use when <the specific situation this convention governs>.
---
```

**Requirements:**

- Exactly these two keys. Every file under `repo-governance/` carries `description` and
  `when_to_use` and nothing else; a third key is a validation failure
- Description is 1-2 sentences explaining the convention's purpose
- `when_to_use` states the situation that should send a reader here, starting with "Use when"
- The document's title is its H1, and its identifier is its filename stem — neither is restated
  in frontmatter
- No `created:` or `updated:` field — git history is the authoritative change record, per
  [No Manual Date Metadata Convention](../../structure/no-date-metadata.md)

## 2. Introduction (H1 + opening paragraph)

```markdown
# Convention Name

Brief overview explaining what this convention covers and why it exists.
1-3 paragraphs maximum.
```

**Purpose:** Orient readers to the convention's scope and value.

## 3. Principles Implemented/Respected Section (H2)

Keep this section as H2 when it remains in the convention's parent file. When progressive
disclosure moves the whole section to an indexed child document, that child's document title is
the equivalent H1; do not repeat an empty H2 in the parent merely to satisfy a mechanical check.

```markdown
## Principles Implemented/Respected

This convention implements/respects the following core principles:

- **[Principle Name](../../principles/[category]/[name].md)**: Brief explanation of HOW this convention implements or respects this principle. What specific aspect of the principle does this convention embody?
- **[Another Principle](../../principles/[category]/[name].md)**: Another explanation.
```

**Purpose:** Traceability from documentation standards back to foundational values, made verifiable.

**Requirements:**

- List ALL principles this convention implements or respects
- Link each one with a relative path: `../principles/[category]/[name].md`
- Explain HOW the convention embodies each principle, not just its name

**Note:** This section is MANDATORY for all convention documents. It enables traceability validation and ensures conventions trace back to foundational values.

**Once a document is split**, the heading belongs to the **parent** `<name>.md`, not to the `NN-<slug>.md` children. `repo-governance traceability validate` skips numbered children that sit beside a `README.md`, so the requirement binds once per document. Same for `## Vision Supported` and `## Conventions Implemented/Respected`.

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

**Note:** Exclusions prevent scope creep and point readers at related conventions.

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
