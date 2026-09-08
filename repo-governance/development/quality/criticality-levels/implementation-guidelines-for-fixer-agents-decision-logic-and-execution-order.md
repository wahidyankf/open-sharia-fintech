---
description: "Criticality-aware decision logic and fix order."
when_to_use: "Use when implementing a fixer's fix-execution order."
---

# Implementation Guidelines for Fixer Agents: Decision Logic and Execution Order

## Implementation Guidelines for Fixer Agents

### Criticality-Aware Decision Logic

**Fixer agents must process findings considering BOTH criticality and confidence**.

**Priority Matrix** (already shown above):

| Criticality | HIGH Confidence      | MEDIUM Confidence     | FALSE_POSITIVE      |
| ----------- | -------------------- | --------------------- | ------------------- |
| CRITICAL    | P0 - Fix immediately | P1 - Urgent review    | Report with context |
| HIGH        | P1 - Fix after P0    | P2 - Standard review  | Report with context |
| MEDIUM      | P2 - Fix after P1    | P3 - Optional review  | Report with context |
| LOW         | P3 - Batch fixes     | P4 - Suggestions only | Report with context |

### Execution Order

```python
def apply_fixes(audit_report):
    """Apply fixes in priority order."""

    # Parse findings by section (CRITICAL → HIGH → MEDIUM → LOW)
    critical_findings = parse_section(audit_report, "CRITICAL")
    high_findings = parse_section(audit_report, "HIGH")
    medium_findings = parse_section(audit_report, "MEDIUM")
    low_findings = parse_section(audit_report, "LOW")

    # Re-validate and assess confidence for each finding
    validated_findings = []
    for finding in (critical_findings + high_findings + medium_findings + low_findings):
        confidence = revalidate_finding(finding)
        priority = determine_priority(finding.criticality, confidence)
        validated_findings.append((finding, confidence, priority))

    # Sort by priority (P0 first)
    validated_findings.sort(key=lambda x: x[2])  # Sort by priority

    # Apply fixes in priority order
    p0_fixes = []
    p1_fixes = []
    p2_fixes = []
    p3_fixes = []

    for finding, confidence, priority in validated_findings:
        if priority == "P0":
            if confidence == "HIGH":
                apply_fix(finding)
                p0_fixes.append(finding)
            else:
                # This shouldn't happen (P0 requires HIGH confidence)
                flag_for_urgent_review(finding)
        elif priority == "P1":
            if confidence == "HIGH":
                apply_fix(finding)
                p1_fixes.append(finding)
            else:  # MEDIUM confidence
                flag_for_urgent_review(finding)
        elif priority == "P2":
            if confidence == "HIGH" and user_approved_batch_mode:
                apply_fix(finding)
                p2_fixes.append(finding)
            else:
                flag_for_standard_review(finding)
        elif priority in ["P3", "P4"]:
            # Include in summary only, no automatic application
            p3_fixes.append(finding)

    # Report summary
    return {
        "p0_fixed": p0_fixes,
        "p1_fixed": p1_fixes,
        "p2_fixed": p2_fixes,
        "flagged_for_review": flagged_items,
        "suggestions_only": p3_fixes
    }
```
