---
title: "Factual Validation Convention — Web Verification Workflow"
description: When to use WebSearch vs. WebFetch, search query patterns, handling 403 errors, and the preference order for authoritative sources.
when_to_use: Use when choosing between WebSearch and WebFetch for a verification task, crafting a search query, or a fetch is blocked with a 403.
category: explanation
subcategory: conventions
tags:
  - factual-validation
  - verification
  - web-research
  - accuracy
  - quality-assurance
created: 2025-12-16
---

# Web Verification Workflow

## WebSearch Usage Patterns

**When to use WebSearch:**

1. **Finding current version information**
   - "Next.js latest version 2025"
   - "Prisma npm latest"

2. **Verifying tool existence and status**
   - "gobuster GitHub repository"
   - "volta Node.js version manager"

3. **Checking best practices and standards**
   - "WCAG AA contrast ratio standard"
   - "Conventional Commits specification"

4. **Fallback when WebFetch is blocked (403 errors)**
   - "wikipedia TypeScript article"
   - Verify article exists via search results

**Search Query Patterns:**

- Include current year for recency: `"[tool] documentation 2025"`
- Use official source names: `"[library] npm"`, `"[tool] GitHub"`
- Be specific: `"Next.js 15 release notes"` not just `"Next.js"`

## WebFetch Usage Patterns

**When to use WebFetch:**

1. **Accessing official documentation URLs**
   - Official GitHub repositories
   - Package registries (npm, PyPI)
   - Standards bodies (NIST, OWASP, W3C)

2. **Verifying external reference accessibility**
   - Check links return 200 (not 404, 403)
   - Validate redirect chains are reasonable

3. **Reading API documentation for verification**
   - Method signatures
   - Parameter types
   - Return values

**Handling 403 Errors:**

Some sites block automated tools (Wikipedia, GitHub, etc.):

1. **Use WebSearch as fallback**
   - Search: "wikipedia [article name]"
   - Verify article exists via search results

2. **Try alternative sources**
   - Official mirrors or documentation
   - Internet Archive (Wayback Machine)

3. **Document the limitation**
   - Note: "Unable to WebFetch due to 403, verified via WebSearch"

## Authoritative Sources (Preference Order)

**Prefer in this order:**

1. **Official documentation** - Primary source of truth
2. **Official GitHub repository** - README, docs/, releases
3. **Package registries** - npm, PyPI, RubyGems (for versions)
4. **Standards bodies** - NIST, OWASP, W3C, IETF RFCs
5. **Reputable tech sites** - MDN, Stack Overflow Docs (with caution)

**Avoid:**

- Blog posts (unless from official source)
- Outdated Stack Overflow answers
- Unofficial wikis or third-party docs
- Forums or discussion threads
