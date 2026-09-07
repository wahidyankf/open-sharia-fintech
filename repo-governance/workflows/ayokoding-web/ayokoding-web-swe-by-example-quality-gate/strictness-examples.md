---
description: Three worked examples showing which findings the fixer skips under normal, strict, and ocd strictness modes.
when_to_use: Use as worked references for how each strictness mode determines which findings get auto-fixed.
---

# Strictness Examples 4-6: Normal, Strict, and OCD Modes

## Example 4: Normal Strictness (Default)

**Scenario**: Standard by-example validation for Go tutorial

**Invocation**:

```
User: "Run ayokoding-web by-example quality gate workflow for golang/tutorials/by-example/ in normal mode"
```

**Checker results**:

- 3 CRITICAL findings (missing imports)
- 5 HIGH findings (color violations, missing frontmatter)
- 8 MEDIUM findings (missing annotations)
- 12 LOW findings (style improvements)

**Fixer behaviour**:

- Fixes: 3 CRITICAL + 5 HIGH = 8 fixes applied
- Skips: 8 MEDIUM + 12 LOW = 20 findings reported but not fixed
- Status: `excellent` (zero threshold-level findings, below-threshold findings acceptable)

**Final audit**:

- Zero CRITICAL/HIGH findings
- 8 MEDIUM findings reported (acceptable)
- 12 LOW findings reported (acceptable)

## Example 5: Strict Mode (Pre-Deployment)

**Scenario**: Pre-deployment validation for Elixir tutorial

**Invocation**:

```
User: "Run ayokoding-web by-example quality gate workflow for elixir/tutorials/by-example/ in strict mode"
```

**Checker results**:

- 2 CRITICAL findings
- 4 HIGH findings
- 10 MEDIUM findings
- 15 LOW findings

**Fixer behaviour**:

- Fixes: 2 CRITICAL + 4 HIGH + 10 MEDIUM = 16 fixes applied
- Skips: 15 LOW findings reported but not fixed
- Status: `excellent` (zero CRITICAL/HIGH/MEDIUM, LOW findings acceptable)

**Final audit**:

- Zero CRITICAL/HIGH/MEDIUM findings
- 15 LOW findings reported (acceptable)

## Example 6: Very Strict Mode (Comprehensive)

**Scenario**: Comprehensive audit for Java tutorial

**Invocation**:

```
User: "Run ayokoding-web by-example quality gate workflow for java/tutorials/by-example/ in ocd mode with max-iterations=10"
```

**Checker results**:

- 1 CRITICAL finding
- 3 HIGH findings
- 6 MEDIUM findings
- 20 LOW findings

**Fixer behaviour**:

- Fixes: 1 CRITICAL + 3 HIGH + 6 MEDIUM + 20 LOW = 30 fixes applied
- Skips: None
- Status: `excellent` (zero findings at all levels)

**Final audit**:

- Zero findings at all levels
- Equivalent to pre-mode parameter behaviour
