---
title: "Examples: Repo-Governance through Documentation"
description: "Examples for repo-governance, ayokoding-www, ose-www, docs checkers."
category: explanation
subcategory: development
tags:
  - criticality
  - validation
  - checker-agents
  - fixer-agents
  - quality-assurance
created: 2025-12-27
when_to_use: "Use for a domain example in these checkers."
---

# Domain-Specific Examples: Repository Governance through Documentation

## Domain-Specific Examples

### Repository Governance (repo-rules-checker)

**CRITICAL**:

- Missing required `subcategory` field in convention document (breaks organization)
- Agent `name` field doesn't match filename (agent discovery fails)
- YAML comment in agent frontmatter (parsing error)

**HIGH**:

- Missing "Principles Respected" section in convention (traceability violation)
- Filename not in kebab-case (convention violation)
- Broken internal link to convention document

**MEDIUM**:

- Missing optional cross-reference
- Suboptimal section ordering
- Minor formatting inconsistency

**LOW**:

- Suggest adding related links
- Consider alternative organization
- Potential future sections

### Next.js Content - ayokoding-www (general-checker, facts-checker, link-checker)

**CRITICAL**:

- Missing required `title` field (content validation fails)
- Invalid YAML syntax in frontmatter (parsing error)
- Broken internal link without language prefix (404 on site)
- Code example won't compile (verified via web search)

**HIGH**:

- Missing `weight` field (navigation order undefined)
- Wrong internal link format (relative instead of absolute)
- Incorrect heading hierarchy (H3 before H2)
- Outdated tutorial sequence (verified via official docs)

**MEDIUM**:

- Missing optional `description` field
- Suboptimal weight spacing (still ordered correctly)
- Minor bilingual inconsistency (both versions functional)
- Unverified external claim (needs web verification)

**LOW**:

- Suggest adding optional tags
- Consider alternative content structure
- Potential cross-linking opportunity
- Suggest mentioning alternative approach

### Next.js Content - ose-www (content-checker)

**CRITICAL**:

- Missing required frontmatter for Next.js content validation
- Broken internal link (404 error)
- Invalid markdown syntax (rendering breaks)

**HIGH**:

- Missing recommended metadata for SEO
- Wrong heading hierarchy
- Accessibility violation (missing alt text)

**MEDIUM**:

- Suboptimal content organization
- Minor formatting inconsistency
- Missing optional PaperMod feature

**LOW**:

- Suggest adding cover image
- Consider adding tags
- Potential cross-reference

### Documentation (docs-checker, docs-tutorial-checker, docs-link-checker)

**CRITICAL**:

- [Error] Command syntax incorrect (verified via web search)
- [BROKEN] Internal link to non-existent file (404)
- Security vulnerability in code example
- Missing alt text on critical diagram (WCAG violation)

**HIGH**:

- [Outdated] Major version reference with breaking changes
- [BROKEN] External link to important resource (404)
- Passive voice in step-by-step instructions
- Wrong heading nesting (H1 → H3)

**MEDIUM**:

- [Unverified] External claim needs web verification
- [REDIRECT] External link redirects (1 hop, working)
- Minor formatting inconsistency
- Missing optional code fence language tag

**LOW**:

- Suggest additional examples
- Consider adding diagram
- Potential cross-linking opportunity
- Alternative phrasing suggestion
