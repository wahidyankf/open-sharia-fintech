---
title: "Best Practices 4-6"
description: "Preserve content during refactoring, run affected tests only, use standardized validation patterns."
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: "Use when applying these three quality best practices."
---

# Best Practices 4-6

## Practice 4: Preserve Content During Refactoring

**Principle**: When condensing or restructuring files, preserve all knowledge.

**Good Example:**

```markdown
## Process

1. Read all source files thoroughly
2. Identify unique knowledge in each
3. Create target structure
4. Migrate content systematically
5. Cross-reference and verify nothing lost
6. Archive originals for safety
```

**Bad Example:**

```bash
# Delete files without preserving content (DO NOT DO THIS)
rm old-doc-1.md old-doc-2.md old-doc-3.md
# Knowledge lost forever!
```

**Rationale:**

- No knowledge loss
- Maintains documentation value
- Enables future reference
- Respects Documentation First principle

## Practice 5: Run Affected Tests Only in Pre-Push Using Canonical Target Names

**Principle**: Use `test:quick` via Nx affected detection for fast, consistent feedback. Only `test:unit` results (and other fast checks) belong in `test:quick`. Integration and E2E tests run on a CI schedule, never in the pre-push gate — with one named carve-out: `rhino-cli`'s `tests/*.rs` cucumber binaries (which drive the real command pipeline against real or fixture filesystems) are enumerated directly in `test:unit` and therefore do run in the pre-push gate; see [Per-Backend and CLI App Implementation Patterns](../three-level-testing-standard/per-backend-and-cli-app-implementation-patterns.md).

**See**: [Three-Level Testing Standard](.././three-level-testing-standard.md) for what belongs at each test level.

**Good Example:**

```bash
# .husky/pre-push
nx affected -t test:quick
# Only affected projects, using the canonical fast quality gate target
```

**Bad Example:**

```bash
# .husky/pre-push
nx test  # Non-standard target name; runs ALL tests (slow!)
```

**Rationale:**

- Fast feedback (seconds to a few minutes)
- `test:quick` is the canonical pre-push gate — every project must expose it
- Using `nx affected -t` ensures consistent behaviour across all project types
- Reduces friction for developers
- Maintains quality gate

**See**: [Nx Target Standards](../infra/nx-targets.md) for `test:quick` composition rules per project type.

## Practice 6: Use Standardized Validation Patterns

**Principle**: Follow repository validation methodology for consistency.

**Good Example:**

```bash
# Standardized validation pattern
validate_frontmatter() {
  local file=$1
  # Check required fields
  # Validate date format
  # Verify allowed values
  # Report findings with line numbers
}
```

**Bad Example:**

```bash
# Ad-hoc validation (DO NOT DO THIS)
validate() {
  grep something $file  # Unclear what's checked
}
```

**Rationale:**

- Consistent validation across agents
- Clear, documented patterns
- Easier to maintain and extend
- Reduces duplication
