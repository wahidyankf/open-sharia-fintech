---
description: "A worked example of a second issue entry."
when_to_use: "Use for a second-issue-entry report example."
---

# 2. [Next CRITICAL Issue]

[Same format as above]

---

[Continue for all CRITICAL findings]

````

**Repeat section template for each criticality level**:

- `## HIGH Issues (Should Fix)`
- `## MEDIUM Issues (Improve When Possible)`
- `## LOW Issues (Optional Enhancements)`

### Report Footer

```markdown
---

## Recommendations

### Critical Path (Before Publication)
1. Fix all CRITICAL issues immediately (blocking)
2. Address HIGH issues before deployment (recommended)

### Next Iteration
- Review and fix MEDIUM issues for polish
- Consider LOW suggestions if relevant to current work

### For Fixer Agent
Run `{agent-family}-fixer` on this audit report:
- Fixer will auto-apply HIGH confidence fixes for CRITICAL and HIGH issues
- MEDIUM confidence issues flagged for manual review
- FALSE_POSITIVE findings will be reported to improve checker

---

## Audit Completion

**Report File**: `local-tmp/{agent-family}/{agent-family}__{uuid-chain}__{timestamp}__audit.md`
**Next Steps**:
1. Review findings by priority (CRITICAL → HIGH → MEDIUM → LOW)
2. Run fixer agent if auto-fixes desired
3. Manually address flagged items

---

**Audit Report ID**: {uuid-chain}
**Checker Version**: {agent-name} v{version}
**Generated**: {timestamp} UTC+7
````
