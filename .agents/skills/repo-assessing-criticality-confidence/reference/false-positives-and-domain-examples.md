# Criticality-Confidence — False Positives and Domain Examples

## False Positives Detected

### 1. [Issue Title]

**File**: `path/to/file.md`
**Checker Finding**: [What checker reported]
**Re-validation**: [What fixer found]
**Conclusion**: FALSE_POSITIVE
**Reason**: [Why checker was wrong]

**Recommendation for Checker**:
[How to improve checker logic]

---

## Domain-Specific Examples

### Repository Governance (rules-checker)

**CRITICAL**:

- Missing `subcategory` field in convention (breaks organization)
- Agent `name` doesn't match filename (discovery fails)
- YAML comment in agent frontmatter (parsing error)

**HIGH**:

- Missing "Principles Respected" section (traceability violation)
- Non-kebab-case filename in docs/ or repo-governance/ (convention violation)

**MEDIUM**:

- Missing optional cross-reference
- Suboptimal section ordering

**LOW**:

- Suggest adding related links
- Consider alternative organization

### ayokoding-web Content (Next.js)

**CRITICAL**:

- Missing required `title` field (page fails to render)
- Invalid content metadata (parsing error)
- Broken internal link without language prefix (404)

**HIGH**:

- Missing `weight` field (navigation undefined)
- Wrong internal link format (relative vs absolute)
- Incorrect heading hierarchy (H3 before H2)

**MEDIUM**:

- Missing optional `description` field
- Suboptimal weight spacing

**LOW**:

- Suggest adding optional tags
- Consider alternative structure

### Documentation (docs-checker)

**CRITICAL**:

- [Error] Command syntax incorrect (verified via WebSearch)
- [BROKEN] Internal link to non-existent file
- Security vulnerability in code example

**HIGH**:

- [Outdated] Major version with breaking changes
- Passive voice in step-by-step instructions
- Wrong heading nesting (H1 → H3)

**MEDIUM**:

- [Unverified] External claim needs verification
- Missing optional code fence language tag

**LOW**:

- Suggest additional examples
- Consider adding diagram
