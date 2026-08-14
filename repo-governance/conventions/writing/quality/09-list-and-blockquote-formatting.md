---
title: "List and Blockquote Formatting"
description: "When to use unordered, ordered, nested, and checklist list formats, and how to format blockquotes and callouts"
category: explanation
subcategory: conventions
tags:
  - content-quality
  - markdown
  - writing-standards
  - accessibility
  - documentation
created: 2025-12-07
when_to_use: "Read this when choosing a list type or writing a blockquote/callout in markdown content."
---

# List and Blockquote Formatting

## List Formatting

**Use appropriate list types** for content structure.

### Unordered Lists

Use for:

- Items without specific order
- Feature lists
- Option lists
- Related items of equal importance

```markdown
Key features:

- User authentication
- Role-based access control
- Session management
- Audit logging
```

### Ordered Lists

Use for:

- Sequential steps
- Ranked items
- Processes with specific order
- Prerequisites with dependencies

```markdown
Setup steps:

1. Install Node.js 18 or higher
2. Clone the repository
3. Run `npm install`
4. Configure environment variables
5. Start the development server
```

### Nested Lists

**Use proper nesting** with 2-space or 4-space indentation:

```markdown
Project structure:

- src/
  - components/
    - auth/
      - Login.tsx
      - Signup.tsx
  - utils/
    - validation.ts
- tests/
  - unit/
  - integration/
```

### Checklist Format

Use checkboxes for task lists:

```markdown
Setup checklist:

- [x] Install dependencies
- [x] Configure database
- [ ] Set up authentication
- [ ] Deploy to production
```

## Blockquotes and Callouts

**Use blockquotes for quotations and callouts**.

### Simple Blockquote

```markdown
> "Good documentation is like good code - it should be clear, concise, and
> maintainable." — Anonymous Developer
```

### Callout Boxes

Use blockquotes with emoji or labels for callouts:

```markdown
> **Note**: Configuration changes require server restart.

> **Warning**: Deleting this file will remove all user data permanently.

> PASS: **Success**: Your authentication is now properly configured.

> **Tip**: Use environment variables for sensitive configuration.
```

**Callout Types**:

- **Note** / : General information
- **Warning** / ️: Caution required
- **Success** / : Confirmation or best practice
- **Tip** / : Helpful suggestion
- **Important** / : Critical information
