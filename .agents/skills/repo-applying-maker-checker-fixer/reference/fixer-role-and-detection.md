# Maker-Checker-Fixer — Stage 3 Fixer Role, Priority, and Report Discovery

## Stage 3: Fixer (Remediation) — Role and Characteristics

**Role**: Applies validated fixes from checker audit reports

**Characteristics**:

- Validation-driven (works from audit reports, not user requests)
- Re-validation before fixing (confirms issues still exist)
- Confidence-based (only applies HIGH confidence fixes automatically)
- Safe application (skips MEDIUM and FALSE_POSITIVE)
- Audit trail (generates fix reports for transparency)

**Tool Pattern**: `Read`, `Edit`, `Glob`, `Grep`, `Write`, `Bash`

- `Edit` for applying fixes (NOT `Write`)
- `Write` for fix report generation
- `Bash` for timestamps

**Color**: Yellow (fixer agents)

**When to Use Fixer**:

- ✅ Checker has generated an audit report
- ✅ Issues are convention violations (not content gaps)
- ✅ Fixes are mechanical (field values, formatting)
- ✅ Validation-driven workflow

**When to SKIP Fixer (Manual Preferred)**:

- ❌ Issues require human judgment (narrative quality)
- ❌ Fixes are context-dependent
- ❌ Checker reports unclear/ambiguous
- ❌ User prefers manual control

**Priority-Based Execution**:

Fixers combine criticality (importance) × confidence (certainty) → priority:

| Priority         | Combination                      | Action                               |
| ---------------- | -------------------------------- | ------------------------------------ |
| **P0** (Blocker) | CRITICAL + HIGH                  | Auto-fix immediately, block if fails |
| **P1** (Urgent)  | HIGH + HIGH OR CRITICAL + MEDIUM | Auto-fix or urgent review            |
| **P2** (Normal)  | MEDIUM + HIGH OR HIGH + MEDIUM   | Auto-fix (if approved) or review     |
| **P3-P4** (Low)  | LOW combinations                 | Suggestions only                     |

**Execution Order**: P0 → P1 → P2 → P3-P4

## Fixer Workflow Step 1: Report Discovery

**Auto-detect with manual override (default pattern)**:

```bash
# Auto-detect latest audit report for agent family
ls -t local-tmp/{agent-family}/{agent-family}-*-audit.md | head -1
```

**Implementation Steps**:

1. **Auto-detect latest**: Find most recent audit report in `local-tmp/<agent-family>/`
2. **Allow manual override**: Accept explicit report path from user
3. **Verify report exists**: Check file exists before proceeding
4. **Parse report format**: Extract UUID chain and timestamp for fix report

**Report Naming**: Uses 4-part format per Temporary Files Convention:

- Pattern: `{agent-family}__{uuid-chain}__{timestamp}__audit.md`
- Example: `docs__a1b2c3__2025-12-14--20-45__audit.md`

## Fixer Workflow Step 2: Validation Strategy

**CRITICAL PRINCIPLE**: NEVER trust checker findings blindly. ALWAYS re-validate before applying fixes.

**For EACH finding in audit report**:

```
Read finding → Re-execute validation check → Assess confidence level

HIGH_CONFIDENCE:
  - Re-validation confirms issue exists
  - Issue is objective and verifiable
  - Apply fix automatically

MEDIUM_CONFIDENCE:
  - Re-validation unclear or ambiguous
  - Issue is subjective or context-dependent
  - Skip fix, flag as "needs manual review"

FALSE_POSITIVE:
  - Re-validation disproves issue
  - Skip fix, report to user
  - Suggest checker improvement
```

**Confidence Assessment Criteria**:

**HIGH Confidence** (Apply automatically):

- Objective, verifiable errors
- Clear violation of documented standards
- Pattern-based errors with known fixes
- File-based errors (paths, syntax, format)

**MEDIUM Confidence** (Manual review):

- Subjective quality judgments
- Context-dependent issues
- Ambiguous requirements
- Risky refactoring changes

**FALSE_POSITIVE** (Skip and report):

- Re-validation disproves the issue
- Checker misunderstood context
- Checker used wrong verification source
- Finding no longer applicable
