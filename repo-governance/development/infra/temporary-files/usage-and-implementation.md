---
title: "Usage and Implementation for AI Agents"
description: When these directories apply and don't, plus implementation steps for both agent types.
category: explanation
subcategory: development
tags: [temporary-files, ai-agents, file-organization, best-practices]
created: 2025-12-01
when_to_use: Use when deciding if a file belongs here.
---

# Usage and Implementation for AI Agents

## PASS: When This Applies

Use these directories when:

- Creating validation or audit reports
- Generating temporary checklists or todo lists
- Writing intermediate analysis files
- Creating scratch files for processing
- Any file that is **not meant to be committed** to version control
- Files intended for immediate review/use only

## FAIL: When NOT to Use These Directories

Do NOT use these directories for:

- **Permanent documentation** - Use `docs/` directory with proper naming convention
- **Operational metadata** - Use `docs/metadata/` directory (e.g., `external-links-status.yaml` for link verification cache)
- **Project planning** - Use `plans/` directory with proper structure
- **Source code** - Use `apps/` or `libs/` directories
- **Configuration files** - Place in repository root or appropriate subdirectories
- **Files explicitly required by other conventions** - Follow the specific convention's guidelines

## Implementation for AI Agents

### For Report-Generating Agents

Agents that create validation/audit reports (docs-checker, plan-checker, rules-checker, etc.) should:

1. Use `local-tmp/<agent-family>/`, creating it first with `mkdir -p`
2. Follow naming pattern: `{agent-family}__{uuid-chain}__{YYYY-MM-DD--HH-MM}__{type}.md`
3. Include timestamp in filename for traceability
4. Use descriptive report type in filename
5. **MUST have both Write and Bash tools** in their frontmatter

**Tool Requirements**:

Any agent writing a report MUST have:

- **Write tool**: Required for creating report files
- **Bash tool**: Required for generating UTC+7 timestamps using `TZ='Asia/Jakarta' date +"%Y-%m-%d--%H-%M"`

**Example frontmatter**:

```yaml
---
name: rules-checker
description: Validates consistency between agents, AGENTS.md, conventions, and documentation.
tools: Read, Glob, Grep, Write, Bash
model: sonnet
color: green
---
```

**Rationale**: Write tool creates the file, Bash tool generates accurate timestamps. Both are mandatory for report-generating agents.

**Example implementation**:

```markdown
When generating a validation report:

- Path: `local-tmp/docs/docs__a1b2c3__2025-12-01--14-30__validation.md`
- Include: Timestamp, agent name, summary, detailed findings
```

### For General-Purpose Agents

Agents creating miscellaneous temporary files should:

1. Use `local-tmp/` directory
2. Use descriptive filenames
3. Clean up files after use (when appropriate)
4. Document the purpose of temporary files if they're long-lived
