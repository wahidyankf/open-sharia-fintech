---
description: "Details what each of the three validators checks: factual accuracy, pedagogical quality, and link validity (including the no-auto-fix link limitation)."
when_to_use: "Use when you need to know exactly what a given validator dimension checks for."
---

# Validation Dimensions

**Factual Accuracy** (docs-checker):

- Technical correctness using web verification
- Command syntax and flags validation
- Version information accuracy
- Code example API correctness
- Contradiction detection within/across documents
- Outdated information identification
- Mathematical notation validation
- Diagram color accessibility (color-blind palette)

**Pedagogical Quality** (docs-tutorial-checker):

- Tutorial structure and type compliance
- Narrative flow and story arc
- Learning scaffold progression
- Visual completeness (diagrams at 30-50% frequency)
- Hands-on elements (examples, exercises, actionable steps)
- Writing style and engagement
- **Time estimate detection** (forbidden in educational content)
- Color-blind friendly diagrams
- LaTeX delimiter correctness

**Link Validity** (docs-link-checker):

- External URL accessibility (HTTP status codes)
- Internal file reference validity
- Markdown extension presence (.md required)
- Redirect chain tracking
- **Cache management** (docs/metadata/external-links-status.yaml)
- Per-link expiry (6 months individual)
- **NO AUTO-FIX AVAILABLE** - Broken links block success, require manual intervention
