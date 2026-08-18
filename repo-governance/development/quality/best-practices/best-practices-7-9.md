---
title: "Best Practices 7-9"
description: "Combine criticality and confidence, enable lint-staged, document validation rules."
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: "Use when applying these three quality best practices."
---

# Best Practices 7-9

## Practice 7: Combine Criticality and Confidence for Priority

**Principle**: Use priority matrix (P0-P4) for fix execution order.

**Good Example:**

```bash
# P0 (Blocker): CRITICAL + HIGH confidence
# Fix immediately, block if fails

# P1 (Urgent): HIGH + HIGH OR CRITICAL + MEDIUM
# Fix with high priority

# P2 (Normal): MEDIUM + HIGH OR HIGH + MEDIUM
# Fix when approved

# P3-P4 (Low): All LOW combinations
# Suggestions only
```

**Bad Example:**

```bash
# Random fix order (DO NOT DO THIS)
for finding in $FINDINGS; do
  apply_fix "$finding"  # No priority!
done
```

**Rationale:**

- Blockers fixed first
- Efficient resource use
- Clear escalation path
- Business impact aligned

## Practice 8: Enable Lint-Staged for Incremental Quality

**Principle**: Format and lint only staged files in pre-commit. For languages that require project
context (e.g. Rust, .NET), use dedicated hook steps rather than lint-staged.

**Good Example:**

```json
// package.json — lint-staged for JS/TS/JSON/YAML/CSS/MD
{
  "lint-staged": {
    "*.md": ["prettier --write", "markdownlint-cli2 --fix"]
  }
}
```

```sh
# .husky/pre-commit — dedicated step for language-native formatters

# gofmt: no project context required, safe in lint-staged or hook
gofmt -w staged_go_files

# rustfmt: safe in lint-staged (no project context required)
rustfmt staged_rs_files
```

**Bad Example:**

```bash
# Format entire repo on every commit (DO NOT DO THIS)
prettier --write .  # SLOW!

# Running cargo fmt from repo root without --manifest-path (DO NOT DO THIS)
# Formats entire workspace, not just staged files
cargo fmt
```

**Rationale:**

- Fast pre-commit hooks — only affects changed files
- Language-native formatters (gofmt, rustfmt) enforce language-specific style
- Gradual quality improvement; developer-friendly

## Practice 9: Document Validation Rules and Rationale

**Principle**: Explain WHY each validation exists, not just WHAT it checks.

**Good Example:**

```markdown
## Validation: Alt Text Required

**Rule**: All images must have descriptive alt text.

**Rationale**:

- Screen readers need text descriptions
- WCAG AA compliance requirement
- Improves SEO
- Benefits users on slow connections

**Example**: `<img src="photo.jpg" alt="Team photo at conference" />`
```

**Bad Example:**

```markdown
## Validation: Alt text

Check alt text.
```

**Rationale:**

- Clear purpose and context
- Easier to maintain rules
- Enables informed decisions
- Educational for team
