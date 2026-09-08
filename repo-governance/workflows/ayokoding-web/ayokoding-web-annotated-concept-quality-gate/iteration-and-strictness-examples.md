---
description: Two worked examples — a full clean-path iteration for a new tutorial below the worked-example floor, and a normal-strictness run showing which findings the fixer skips.
when_to_use: Use as worked references when you want to see how a typical iteration or a strictness-mode fixer run plays out end to end.
---

# Iteration and Strictness Examples

## Iteration Example: New Annotated-Concept Tutorial (Clean Path)

**Scenario**: Creating a standard-mode Annotated-concept tutorial from scratch

**Step 1: Maker** (manual creation)

- Author writes 40 worked examples in per-theme clusters
- Includes code, some annotations, few diagrams
- Saves to `computer-science-foundations/learning/`

**Step 2: Checker** (validation)

```bash
apps-ayokoding-www-annotated-concept-checker validates computer-science-foundations learning subtree
```

**Results**:

- Mode detected: standard
- 40 worked examples (floor: 45) ️
- Self-containment: 90%
- Annotations: 70% coverage ️
- Status: **NEEDS IMPROVEMENT**

**Step 3: User Review**

- Reviews audit report
- Approves HIGH confidence fixes
- Approves MEDIUM confidence annotation additions
- Defers additional worked examples (needs content planning)

**Step 4: Fixer** (apply fixes)

```bash
apps-ayokoding-www-annotated-concept-fixer applies fixes from audit
```

**Fixes applied**:

- Added annotations to meet 1.0-2.25 comment lines per code line density on existing examples
  (MEDIUM, re-validated)
- Fixed 2 color violations (HIGH)
- Added 3 missing key takeaways (MEDIUM)

**Step 5: Re-validation**

```bash
apps-ayokoding-www-annotated-concept-checker re-validates
```

**Results**:

- Self-containment: 100%
- Annotations: 95% coverage
- Worked-example count: 40 (below floor, deferred) ️
- Status: **NEEDS IMPROVEMENT** (count still below the 45 floor)

**Outcome**: Return to maker to add 5+ more worked examples before EXCELLENT can be declared

## Strictness Example: Normal Strictness (Default)

**Scenario**: Standard-mode validation for a system design Annotated-concept tutorial

**Invocation**:

```
User: "Run ayokoding-web annotated-concept quality gate workflow for system-design/learning/ in normal mode"
```

**Checker results**:

- 1 CRITICAL finding (code found in what should be a no-code sub-mode topic — mode mismatch)
- 4 HIGH findings (color violations, missing frontmatter)
- 6 MEDIUM findings (missing annotations)
- 9 LOW findings (style improvements)

**Fixer behaviour**:

- Fixes: 1 CRITICAL + 4 HIGH = 5 fixes applied
- Skips: 6 MEDIUM + 9 LOW = 15 findings reported but not fixed
- Status: `excellent` (zero threshold-level findings, below-threshold findings acceptable)
