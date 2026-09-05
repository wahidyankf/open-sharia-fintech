# Validation Reports — Progressive Writing, Templates, Scope, Tools

## Progressive Writing Methodology

**CRITICAL REQUIREMENT**: All checker agents MUST write findings progressively, not buffer and write once at end.

**Why?** Context compaction during long validation runs can lose buffered findings. Progressive writing ensures audit history survives.

**Implementation Pattern**:

```markdown
Step 0: Initialize Report File

- Generate UUID and chain
- Create report file immediately
- Write header with "In Progress" status

Steps 1-N: Validate Content

- For each validation check:
  1. Perform validation
  2. Immediately write finding to report file (append mode)
  3. Continue to next check
- DO NOT buffer findings in memory

Final Step: Finalize Report

- Update status from "In Progress" to "Complete"
- Add summary statistics
- File already contains all findings from progressive writing
```

## Report Template Structure

**Initial Header** (Step 0):

```markdown
# Validation Report: [Agent Name]

**Status**: In Progress
**Agent**: [agent-name]
**Scope**: [scope-description]
**Timestamp**: [YYYY-MM-DD--HH-MM UTC+7]
**UUID Chain**: [uuid-chain]

---

## Findings

[Findings will be written progressively during validation]
```

**Progressive Findings** (Steps 1-N):

```markdown
## Finding [N]: [Title]

**File**: path/to/file.md
**Line**: 123
**Criticality**: HIGH
**Category**: [category-name]

**Issue**: [Description of what's wrong]

**Recommendation**: [How to fix it]

---
```

**Final Summary** (Last Step):

```markdown
## Summary

**Total Findings**: [N]

- CRITICAL: [count]
- HIGH: [count]
- MEDIUM: [count]
- LOW: [count]

**Status**: Complete
**Completed**: [YYYY-MM-DD--HH-MM UTC+7]
```

## Scope Definitions

Common scopes for execution tracking:

| Agent Family          | Scope              | Tracking File                       |
| --------------------- | ------------------ | ----------------------------------- |
| rules-checker         | `repo-rules`       | `.execution-chain-repo-rules`       |
| docs-checker          | `docs`             | `.execution-chain-docs`             |
| docs-tutorial-checker | `docs-tutorial`    | `.execution-chain-docs-tutorial`    |
| readme-checker        | `readme`           | `.execution-chain-readme`           |
| plan-checker          | `plan`             | `.execution-chain-plan`             |
| ayokoding-web-\*      | `ayokoding-[lang]` | `.execution-chain-ayokoding-[lang]` |
| ose-web-\*            | `ose-platform`     | `.execution-chain-ose-platform`     |

## Tool Requirements

Agents using this Skill MUST have:

- **Write tool**: Required for creating report files
- **Bash tool**: Required for UUID generation and UTC+7 timestamps

**Example frontmatter**:

```yaml
---
name: example-checker
tools: [Read, Glob, Grep, Write, Bash]
skills: [repo-generating-validation-reports]
---
```
