---
description: "The CRITICAL level definition and examples."
when_to_use: "Use when classifying a finding as CRITICAL."
---

# Four Universal Criticality Levels

## CRITICAL

**Definition**: Issues that break functionality, block users, or violate mandatory requirements.

**Impact**: System failures, build breaks, broken user experiences, security vulnerabilities.

**When to Use**:

- Missing required fields that prevent compilation/build
- Broken links that cause 404 errors
- Security vulnerabilities
- Data loss risks
- Syntax errors that prevent execution
- Violations of MUST requirements in conventions

**Action Required**: Must fix before publication/deployment/merge.

**Auto-Fix**: Yes (if confidence is HIGH).

**Examples Across Domains**:

**Repository Governance**:

- Missing `description` or `when_to_use`, or any other key present, in a `repo-governance/` document's frontmatter (see [Governance Frontmatter](../../../conventions/structure/governance-frontmatter.md))
- Agent `name` field doesn't match filename (breaks agent discovery)
- Broken internal link to non-existent file in documentation

**Next.js Content (ayokoding-www/ose-www)**:

- Missing required `title` field (content validation fails)
- Invalid frontmatter syntax (YAML parsing error)
- Broken internal links (404 on site)
- Missing language prefix in internal links (Next.js specific)

**Documentation (docs/)**:

- Command syntax errors that would fail when executed
- Broken links to critical reference material
- Security vulnerabilities in code examples
- Missing alt text on images (WCAG violation)

**Plans**:

- Missing required sections in plan template
- Contradictory requirements (implementation impossible)
- Broken links to critical dependencies

**README**:

- Broken quick start instructions (users cannot get started)
- Incorrect installation commands (fails on execution)

**Factual Validation**:

- Code examples that won't compile/run
- Incorrect command syntax (verified via web search)
- Outdated major version references (breaking changes exist)

**Links**:

- 404 errors on internal links
- 404 errors on external links to critical resources
- Redirect chains >3 hops
