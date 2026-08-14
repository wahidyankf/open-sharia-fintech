# Criticality-Confidence — Priority Matrix

## Decision Matrix

| Criticality     | HIGH Confidence                                  | MEDIUM Confidence               | FALSE_POSITIVE                                    |
| --------------- | ------------------------------------------------ | ------------------------------- | ------------------------------------------------- |
| 🔴 **CRITICAL** | **P0** - Auto-fix immediately (block deployment) | **P1** - URGENT manual review   | Report with CRITICAL context (fix urgently)       |
| 🟠 **HIGH**     | **P1** - Auto-fix after P0                       | **P2** - Standard manual review | Report with HIGH context (fix soon)               |
| 🟡 **MEDIUM**   | **P2** - Auto-fix after P1 (user approval)       | **P3** - Optional review        | Report with MEDIUM context (note for improvement) |
| 🟢 **LOW**      | **P3** - Batch fixes (user decides when)         | **P4** - Suggestions only       | Report with LOW context (informational)           |

## Priority Levels Explained

- **P0** (Blocker): MUST fix before any publication/deployment
- **P1** (Urgent): SHOULD fix before publication, can proceed with approval
- **P2** (Normal): Fix in current cycle when convenient
- **P3** (Low): Fix in future cycle or batch operation
- **P4** (Optional): Suggestion only, no action required

## Execution Order for Fixers

Fixer agents MUST process findings in strict priority order:

```
1. P0 fixes (CRITICAL + HIGH) → Auto-fix, block if fails
2. P1 fixes (HIGH + HIGH OR CRITICAL + MEDIUM) → Auto-fix HIGH+HIGH, flag CRITICAL+MEDIUM
3. P2 fixes (MEDIUM + HIGH OR HIGH + MEDIUM) → Auto-fix MEDIUM+HIGH if approved, flag HIGH+MEDIUM
4. P3-P4 fixes (LOW priority) → Include in summary only
```
