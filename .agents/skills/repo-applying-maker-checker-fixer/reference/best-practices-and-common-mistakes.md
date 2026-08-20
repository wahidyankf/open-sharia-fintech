# Maker-Checker-Fixer — Best Practices and Common Mistakes

## Best Practices

### For All Roles

1. **Always run checker before publication** - Catches issues early
2. **Review audit reports before fixing** - Understand what will change
3. **Use maker for user-driven creation** - Not fixer
4. **Use fixer for validation-driven fixes** - Not maker
5. **Re-run checker after major fixes** - Verify fixes worked
6. **Report false positives** - Improves checker accuracy over time

### For Checkers

**DO**:

- Initialize report file before validation begins (Step 0)
- Write findings progressively during execution
- Use decision tree for consistent criticality assessment
- Document specific impact for each finding
- Provide clear, actionable recommendations
- Include examples showing broken vs fixed state

**DON'T**:

- Buffer findings in memory (context compaction risk)
- Mix criticality levels in same report section
- Skip impact description
- Provide vague recommendations
- Forget to document verification source (for dual-label agents)

### For Fixers

**DO**:

- ALWAYS re-validate before applying fixes
- Process findings in strict priority order (P0 → P1 → P2 → P3)
- Document confidence assessment reasoning
- Report false positives with improvement suggestions
- Group fixes by priority in report
- Trust checker's documented verification work
- Respect mode parameter thresholds

**DON'T**:

- Trust checker findings without re-validation
- Apply fixes in discovery order (ignore priority)
- Skip MEDIUM confidence manual review flagging
- Apply P2 fixes without user approval
- Try to independently verify web-based findings (trust checker)

## Common Mistakes

### All Roles

- ❌ **Using fixer for content creation** - Use maker instead (fixer is for fixing issues, not creating)
- ❌ **Skipping checker validation** - Always validate before publication
- ❌ **Manual fixes for mechanical issues** - Use fixer for efficiency
- ❌ **Auto-applying MEDIUM confidence fixes** - Needs manual review
- ❌ **Not re-validating before fixing** - Prevents false positive fixes

### Checker-Specific

- ❌ **Buffering findings**: Don't collect all findings in memory and write at end (context compaction risk)
- ❌ **Wrong timestamp format**: Don't use `YYYY-MM-DD HH:MM` (spaces in filenames)
- ❌ **Missing UUID chain**: Don't use timestamp alone for uniqueness
- ❌ **Generic scope**: Don't use same scope for all agents
- ❌ **Conflating verification with criticality**: [Error] is WHAT (factual state), criticality is HOW URGENT

### Fixer-Specific

- ❌ **Skipping re-validation**: Don't trust checker, apply fix directly
- ❌ **Ignoring priority order**: Don't fix findings in discovery order
- ❌ **File-level confidence instead of per-finding**: Each finding assessed independently
- ❌ **Trying to independently verify web findings**: Trust checker's documented verification
