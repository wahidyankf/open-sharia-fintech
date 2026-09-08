---
description: "The HIGH level definition and examples."
when_to_use: "Use when classifying a finding as HIGH."
---

# HIGH

**Definition**: Issues causing significant quality degradation or violating documented conventions.

**Impact**: Poor user experience, accessibility violations, convention non-compliance, maintainability problems.

**When to Use**:

- Wrong format but system still functions
- Accessibility violations (WCAG AA failures)
- Convention violations (documented SHOULD requirements)
- Incorrect link format (works but violates convention)
- Missing optional but important fields
- Structural inconsistencies affecting navigation

**Action Required**: Should fix before publication (current cycle).

**Auto-Fix**: Yes (if confidence is HIGH).

**Examples Across Domains**:

**Repository Governance**:

- Missing "Principles Respected" section in convention doc
- YAML comments in agent frontmatter (convention violation)
- Filename not following kebab-case convention

**Next.js Content**:

- Missing `weight` field (navigation order undefined)
- Wrong heading hierarchy (H3 before H2)
- Missing overview links in navigation
- Incorrect internal link format (relative path instead of absolute)

**Documentation**:

- Missing alt text on non-critical images
- Passive voice in instructional content
- Incorrect heading nesting (H1 → H3 skip)
- Missing code block language tags

**Plans**:

- Missing acceptance criteria
- Incomplete deliverables checklist
- Ambiguous requirements needing clarification

**README**:

- Jargon without explanation
- Paragraphs >5 lines (scannability issue)
- Missing problem-solution hook
- Acronyms without context

**Factual Validation**:

- Outdated minor version (still functional but newer exists)
- Unverified external claims (need web verification)
- Incomplete code examples (missing imports)

**Links**:

- External link redirects (1-2 hops, working but suboptimal)
- Missing HTTPS upgrade
- Slow-loading external resources
