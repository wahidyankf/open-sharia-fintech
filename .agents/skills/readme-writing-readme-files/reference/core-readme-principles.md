# Core README Principles

### Problem-Solution Hook

**Start with WHY**: Begin with a clear problem-solution hook that immediately shows value.

✅ **Good opening**:

```markdown
# Project Name

**Problem**: Managing enterprise Shariah-compliant rules is complex and time-consuming.
**Solution**: Open Sharia Enterprise provides automated, validated rule management.
```

❌ **Weak opening**:

```markdown
# Project Name

This is a project that does things.
```

### Plain Language Requirement

**Avoid unexplained jargon**: Use plain language and explain technical terms on first use.

✅ **Good**:

```markdown
Uses **Nx** (a monorepo build system) to manage multiple applications.
```

❌ **Bad**:

```markdown
Uses Nx for the monorepo. ← What's Nx? What's a monorepo?
```

**Acronym Context**: Define acronyms on first use.

✅ **Good**: `WCAG (Web Content Accessibility Guidelines)`
❌ **Bad**: `WCAG compliance required`

### Paragraph Length Limit

**Maximum 5 lines per paragraph**: Keep paragraphs scannable.

✅ **Good**:

```markdown
This project uses Volta for Node.js version management. Volta automatically
switches to the correct Node.js and npm versions based on package.json
configuration. This ensures all developers have identical environments.

Benefits include simplified onboarding and zero version conflicts.
```

❌ **Bad** (8 lines in one paragraph):

```markdown
This project uses Volta for Node.js version management which automatically
switches to the correct Node.js and npm versions based on package.json
configuration ensuring all developers have identical environments and this
provides benefits including simplified onboarding and zero version conflicts
and removes the need for manual version switching and solves many common
environment-related issues that teams face when working with different
Node.js versions across development, staging, and production environments.
```

### Benefits-Focused Language

**Emphasize outcomes, not features**: Show WHAT users gain, not just WHAT the system does.

✅ **Benefits-focused**:

```markdown
## Key Benefits

- **Faster Development**: Automated code generation reduces boilerplate by 70%
- **Fewer Bugs**: Type-safe APIs catch errors at compile time
- **Easier Onboarding**: Standardized structure helps new developers start quickly
```

❌ **Feature-focused**:

```markdown
## Features

- Has code generation
- Uses TypeScript
- Has standardized folder structure
```

### Visual Hierarchy and Structure

**Use headings, lists, and formatting to create scannable structure:**

- **H2 for major sections**: ## Installation, ## Usage, ## Contributing
- **Lists for steps**: Use ordered lists for sequential steps
- **Bold for emphasis**: Highlight key terms
- **Code blocks for commands**: Always format code properly
- **Tables for comparisons**: Use tables for structured data

### Progressive Disclosure

**Layer information from essential to detailed:**

1. **Above the fold**: Problem, solution, key benefits
2. **Quick start**: Minimal steps to get started
3. **Common use cases**: Typical workflows
4. **Detailed documentation**: Link to full docs
5. **Advanced topics**: Link to in-depth guides
