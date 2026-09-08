---
description: "The MEDIUM level definition and examples."
when_to_use: "Use when classifying a finding as MEDIUM."
---

# MEDIUM

**Definition**: Minor quality issues, style inconsistencies, or cosmetic problems.

**Impact**: Slight quality degradation, minor style inconsistencies, suboptimal but functional.

**When to Use**:

- Missing optional fields with minimal impact
- Formatting inconsistencies (whitespace, indentation variations)
- Suboptimal structure that still works
- Outdated versions that remain functional
- Minor style guide deviations
- Cosmetic improvements

**Action Required**: Fix when convenient (next cycle or maintenance window).

**Auto-Fix**: Only if explicitly approved by user.

**Examples Across Domains**:

**Repository Governance**:

- Missing optional description fields
- Suboptimal section ordering (still readable)
- Minor formatting inconsistencies

**Next.js Content**:

- Missing optional `description` field in frontmatter
- Inconsistent emoji usage (semantic meaning clear)
- Suboptimal weight spacing (still ordered correctly)

**Documentation**:

- Inconsistent code fence language tags (markdown vs md)
- Minor formatting variations in lists
- Suboptimal diagram styling

**Plans**:

- Missing optional implementation notes
- Suboptimal section organization
- Minor formatting inconsistencies

**README**:

- Paragraphs at 4-5 lines (approaching but not exceeding limit)
- Slightly verbose explanations
- Minor structural improvements

**Factual Validation**:

- Outdated patch versions (no breaking changes)
- Alternative approaches not mentioned
- Documentation could be more comprehensive

**Links**:

- Slow external resources (>3s load time)
- Unverified optional references
- Missing title attributes on links
