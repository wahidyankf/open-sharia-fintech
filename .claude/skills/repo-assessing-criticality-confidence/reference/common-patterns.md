# Criticality-Confidence — Common Patterns

## Pattern 1: Checker categorizing finding

```markdown
### 1. Missing Required Frontmatter Field

**File**: `apps/ayokoding-www/content/en/programming/python/_index.md:3`
**Criticality**: CRITICAL - Breaks page rendering
**Category**: Missing Required Field

**Finding**: Required `draft` field missing from frontmatter
**Impact**: Page fails to render with missing required field
**Recommendation**: Add `draft: false` to frontmatter
```

## Pattern 2: Fixer assessing confidence

```python
# Read checker finding
finding = "Missing `draft` field"

# Re-validate
frontmatter = extract_frontmatter(file)
draft_exists = "draft" in frontmatter  # Result: False (confirmed)

# Assess confidence
issue_type = "objective"  # Field either exists or doesn't
re_validation = "confirmed"  # Field is indeed missing
fix_safety = "safe"  # Adding missing field is straightforward

confidence = "HIGH"  # Objective, confirmed, safe → HIGH
priority = determine_priority("CRITICAL", "HIGH")  # → P0

# Apply fix
apply_fix(finding)
```

## Pattern 3: Dual-label finding

```markdown
### 1. [Error] - Command Syntax Incorrect

**File**: `docs/tutorials/quick-start.md:42`
**Verification**: [Error] - Command syntax verified incorrect via WebSearch
**Criticality**: CRITICAL - Breaks user quick start experience
**Category**: Factual Error - Command Syntax

**Finding**: Installation command uses incorrect npm flag `--save-deps`
**Impact**: Users get command error, cannot complete setup
**Recommendation**: Change to `--save-dev`
**Verification Source**: https://docs.npmjs.com/cli/v9/commands/npm-install

**Confidence**: HIGH (verified via official docs)
```
