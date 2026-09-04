# Maker-Checker-Fixer — Checker Report Finalization and Progressive Writing

## Final Step: Finalize Report

**Final update to existing report file:**

```bash
# Update report status
cat >> "$REPORT_FILE" << 'SUMMARY'

## Summary

**Total Findings**: {N}

**By Criticality**:
- CRITICAL: {count}
- HIGH: {count}
- MEDIUM: {count}
- LOW: {count}

**Status**: Complete
**Completed**: {YYYY-MM-DD--HH-MM UTC+7}
SUMMARY
```

**Finalization Checklist**:

1. Update status: "In Progress" → "Complete"
2. Count findings by criticality level
3. Add completion timestamp
4. Ensure all findings written to file (progressive writing)
5. Report file path to user

## Progressive Writing Methodology

**CRITICAL REQUIREMENT**: All checker agents MUST write findings progressively.

**Why?** Context compaction during long validation runs can lose buffered findings. Progressive writing ensures audit history survives.

**Implementation Pattern**:

```markdown
Step 0: Initialize Report File
→ Create file immediately with header

Steps 1-N: Validate Content
→ For each validation check:

1. Perform validation
2. Immediately append finding to report file
3. Continue to next check
   → DO NOT buffer findings in memory

Final Step: Finalize Report
→ Update status and add summary
→ File already contains all findings
```

**Example Workflow**:

```markdown
User: "Check the new TypeScript tutorial"

Checker:

1. Reads tutorial file
2. Validates frontmatter (date format, required fields, weight)
3. Checks content structure (heading hierarchy, links)
4. Validates content conventions (links, structure)
5. Checks content quality (alt text, accessible colors)
6. Generates audit report: local-tmp/ayokoding-web/ayokoding-web**2025-12-14--20-45**audit.md
7. Reports findings summary in conversation
8. Does NOT modify the tutorial file
```
