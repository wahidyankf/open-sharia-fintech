---
description: Standard markdown indentation for all files in the repository
when_to_use: Use when indenting bullets, YAML frontmatter, or code blocks in any markdown file.
---

# Indentation Convention

This convention establishes standard markdown indentation for all files in the repository to ensure compatibility with standard markdown tools.

## In This Convention

- [Purpose, Scope, and Bullet Indentation Rules](./indentation/purpose-scope-and-bullet-indentation-rules.md) — Principles, scope, the core space-indentation principle, and standard bullet indentation
- [YAML and Code Block Indentation](./indentation/yaml-and-code-block-indentation.md) — 2-space YAML frontmatter indentation and language-specific code block indentation

## Related Conventions

**Universal Application**:

- [Content Quality Principles](../writing/quality.md) — Quality standards for all markdown

**Context-Specific**:

- [File Naming Convention](../structure/file-naming.md) — File naming standards

## External Resources

- [YAML Specification](https://yaml.org/spec/) - YAML format specification
- [CommonMark Specification](https://spec.commonmark.org/) - Standard markdown specification

## Complete Example and Checklist

### Complete Example

Here's a complete example showing proper indentation in a `docs/` file:

````markdown
---
title: "Authentication Guide"
description: How to implement authentication
category: how-to
tags:
  - auth # 2 spaces (frontmatter uses spaces)
  - oauth # 2 spaces (frontmatter uses spaces)
created: 2025-12-12
---

# Authentication Guide

- Overview of authentication #auth
  - OAuth 2.0 is the recommended approach
    - Authorization code flow for web apps
    - Client credentials flow for service-to-service
  - Key security considerations
    - Token storage strategy
    - Refresh token rotation

- Implementation steps
  - Install dependencies:

```bash
npm install oauth2-provider
```

- Configure the provider:

```javascript
const oauth = new OAuth2Provider({
  clientId: process.env.CLIENT_ID, // 2 spaces (JS standard)
  clientSecret: process.env.CLIENT_SECRET,
  redirectUri: "https://example.com/callback",
});
```

- Test the integration
  - Use Postman for manual testing
  - Write automated tests for token flow

#authentication #oauth #implementation
````

### Indentation Checklist

Before committing files in `docs/`:

- [ ] **Markdown bullets** use standard format: `- Text` (dash-space-text)
- [ ] **Nested bullets** use 2 spaces per indentation level
- [ ] **YAML frontmatter** uses 2 spaces per indentation level
- [ ] **Code blocks** use language-specific idiomatic indentation:
  - [ ] JavaScript/TypeScript: 2 spaces
  - [ ] Python: 4 spaces
  - [ ] YAML: 2 spaces
  - [ ] JSON: 2 spaces
  - [ ] CSS: 2 spaces
  - [ ] Bash/Shell: 2 spaces
  - [ ] Go: Tabs (Go language standard)
- [ ] **No mixed indentation** - consistent throughout file
- [ ] **No tabs in bullets** - use spaces only (standard markdown)
