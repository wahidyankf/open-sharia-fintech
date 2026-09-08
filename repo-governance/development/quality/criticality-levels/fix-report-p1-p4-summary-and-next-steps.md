---
description: "P1-P4 fix summary, false positives, next steps."
when_to_use: "Use for the P1-P4 fix-report summary."
---

# Fix Report: P1-P4 Summary and Next Steps

## P1 Fixes Applied (HIGH + HIGH Confidence)

[Same format as P0]

---

## P1 Flagged for Urgent Review (CRITICAL + MEDIUM Confidence)

### 1. Ambiguous Link Target

**File**: `repo-governance/conventions/formatting/linking.md:89`
**Original Issue**: CRITICAL - Broken link to convention doc
**Validation**: MEDIUM confidence - Multiple possible target files found
**Reason for Flag**: Cannot determine correct link target automatically
**Action Required**: Manually select correct target from:

- `repo-governance/conventions/structure/file-naming.md`
- `repo-governance/development/infra/file-organization.md`

---

## P2 Fixes Applied (MEDIUM + HIGH Confidence)

[Same format as P0]

---

## P2-P3-P4 Suggestions (No Action Taken)

**Total**: 15 findings

1. **File**: `repo-governance/conventions/formatting/diagrams.md`
   **Suggestion**: Consider adding example of complex multi-layer diagram
   **Priority**: P4 (LOW + MEDIUM)

[... list remaining suggestions ...]

---

## False Positives Detected

[Same format as before, with criticality context]

---

## Next Steps

1. **URGENT** - Review 2 P1 flagged items (CRITICAL issues needing manual decision)
2. **Standard** - Review 3 P2 flagged items (HIGH issues needing clarification)
3. **Optional** - Consider 15 suggestions if relevant to current work

````

### Backward Compatibility

**Fixer agents must handle reports without criticality sections**:

```python
def parse_findings(audit_report):
    """Parse findings from audit report, handling old formats."""

    findings = []

    # Try new format first (criticality sections)
    if has_criticality_sections(audit_report):
        findings += parse_section(audit_report, "CRITICAL")
        findings += parse_section(audit_report, "HIGH")
        findings += parse_section(audit_report, "MEDIUM")
        findings += parse_section(audit_report, "LOW")
    else:
        # Fall back to old format (Critical/Important/Minor or other)
        findings += parse_legacy_section(audit_report, "Critical")
        findings += parse_legacy_section(audit_report, "Important")
        findings += parse_legacy_section(audit_report, "Minor")

        # Map legacy severity to new criticality
        for finding in findings:
            if finding.legacy_severity == "Critical":
                finding.criticality = "CRITICAL"
            elif finding.legacy_severity == "Important":
                finding.criticality = "HIGH"
            elif finding.legacy_severity == "Minor":
                finding.criticality = "MEDIUM"

    return findings
````

---
