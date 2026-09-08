---
description: "Five worked edge cases: tutorial-only findings, broken-links blocking success, below-threshold-only findings, non-converging fixes, and tutorial-checker on non-tutorial content."
when_to_use: "Use when diagnosing an unexpected workflow outcome against a known edge-case pattern."
---

# Edge Cases

## Case 1: Only Tutorial-Checker Finds Issues

**Scenario**: Factual and link validators pass, tutorial validator reports findings

**Handling**:

- Step 3 skipped (no factual findings)
- Step 4 runs (tutorial fixer applies fixes)
- Re-validate confirms success across all dimensions

## Case 2: Broken Links Block Success

**Scenario**: Factual and tutorial issues fixed, but link-checker reports broken links

**Handling**:

- No fixer available for links (link-checker reports only)
- Threshold-level findings > 0 (broken links count)
- Max-iterations reached → Status `partial`
- User must manually fix broken links
- Re-run workflow after manual fixes

**Mitigation**:

- Document broken link locations clearly in audit report
- Provide file paths and line numbers for manual fixes
- Recommend running link-checker separately before workflow

## Case 3: Below-Threshold Findings Only

**Scenario**: Mode=normal, but only MEDIUM/LOW findings exist

**Handling**:

- Only CRITICAL/HIGH counted toward threshold
- MEDIUM/LOW reported but don't block
- Fixers skip MEDIUM/LOW (not in scope)
- Success achieved with documented below-threshold issues
- User can re-run with stricter mode if desired

## Case 4: Non-Converging Fixes

**Scenario**: Fixes introduce new issues, findings never reach zero

**Handling**:

- Each iteration tracks finding trends
- Max-iterations reached → Status `partial`
- Report lists remaining issues for investigation
- May indicate fundamental content problems requiring maker intervention

## Case 5: Tutorial-Checker on Non-Tutorial Content

**Scenario**: Tutorial-checker validates reference or how-to documents

**Handling**:

- Tutorial-checker gracefully handles non-tutorial files
- Skips tutorial-specific checks (story arc, scaffold progression)
- Applies universal checks (writing quality, diagram colors, time estimates)
- No false positives from tutorial structure expectations
