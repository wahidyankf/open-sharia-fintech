# Criticality-Confidence — Best Practices and Common Mistakes

## Best Practices

### For Checker Agents

**DO**:

- Use decision tree for consistent criticality assessment
- Document specific impact for each finding
- Provide clear, actionable recommendations
- Include examples showing broken vs fixed state
- Write findings progressively during execution

**DON'T**:

- Mix criticality levels in same report section
- Skip impact description
- Provide vague recommendations
- Forget to document verification source (for dual-label)

### For Fixer Agents

**DO**:

- ALWAYS re-validate before applying fixes
- Process findings in strict priority order (P0 → P1 → P2 → P3)
- Document confidence assessment reasoning
- Report false positives with improvement suggestions
- Group fixes by priority in report

**DON'T**:

- Trust checker findings without re-validation
- Apply fixes in discovery order (ignore priority)
- Skip MEDIUM confidence manual review flagging
- Apply P2 fixes without user approval

## Common Mistakes

### ❌ Mistake 1: Conflating verification with criticality

**Wrong**: [Error] is CRITICAL, [Verified] is LOW

**Right**: Verification describes WHAT (factual state), criticality describes HOW URGENT

### ❌ Mistake 2: File-level confidence instead of per-finding

**Wrong**: Overall file confidence HIGH

**Right**: Each finding assessed independently

### ❌ Mistake 3: Skipping re-validation

**Wrong**: Trust checker, apply fix directly

**Right**: Re-validate finding first, then assess confidence

### ❌ Mistake 4: Ignoring priority order

**Wrong**: Fix findings in discovery order

**Right**: Fix P0 first, then P1, then P2, then P3-P4
