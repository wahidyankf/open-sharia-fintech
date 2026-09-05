---
title: "Iteration and Strictness Examples"
description: Two worked examples — a full clean-path iteration for a new primer below the example floor, and a normal-strictness run showing which findings the fixer skips.
when_to_use: Use as worked references when you want to see how a typical iteration or a strictness-mode fixer run plays out end to end.
---

# Iteration and Strictness Examples

## Iteration Example: New Primer Tutorial (Clean Path)

**Scenario**: Creating a "Just Enough Go" primer from scratch

**Step 1: Maker** (manual creation)

- Author identifies dependent topics (CSP concurrency, backend services) and derives the "just
  enough" scope
- Writes 60 examples across the scoped surface
- Includes code, some annotations, few diagrams

**Step 2: Checker** (validation)

```bash
apps-ayokoding-www-primer-checker validates just-enough-go learning subtree
```

**Results**:

- 60 examples (target: 75-85) ️
- Self-containment: 90%
- Annotations: 70% coverage ️
- Scope discipline: clean (no drift toward comprehensive coverage)
- Status: **NEEDS IMPROVEMENT**

**Step 3: User Review**

- Reviews audit report
- Approves HIGH confidence fixes
- Approves MEDIUM confidence annotation additions
- Defers example count increase (needs content planning)

**Step 4: Fixer** (apply fixes)

```bash
apps-ayokoding-www-primer-fixer applies fixes from audit
```

**Fixes applied**:

- Added annotations to meet 1.0-2.25 comment lines per code line density (MEDIUM, re-validated)
- Fixed 2 color violations (HIGH)
- Added 2 missing key takeaways (MEDIUM)

**Step 5: Re-validation**

```bash
apps-ayokoding-www-primer-checker re-validates
```

**Results**:

- Self-containment: 100%
- Annotations: 95% coverage
- Example count: 60 (below floor, deferred) ️
- Status: **NEEDS IMPROVEMENT** (count still below the 75 floor)

**Outcome**: Return to maker to add 15+ more examples within scope before EXCELLENT can be
declared

## Strictness Example: Normal Strictness (Default)

**Scenario**: Standard validation for a "Just Enough Rust" primer

**Invocation**:

```
User: "Run ayokoding-web primer quality gate workflow for just-enough-rust/learning/ in normal mode"
```

**Checker results**:

- 2 CRITICAL findings (missing scope statement in `overview.md`)
- 3 HIGH findings (color violations, missing frontmatter)
- 5 MEDIUM findings (missing annotations, borderline scope-creep flags)
- 8 LOW findings (style improvements)

**Fixer behaviour**:

- Fixes: 2 CRITICAL + 3 HIGH = 5 fixes applied
- Skips: 5 MEDIUM + 8 LOW = 13 findings reported but not fixed
- Status: `excellent` (zero threshold-level findings, below-threshold findings acceptable)
