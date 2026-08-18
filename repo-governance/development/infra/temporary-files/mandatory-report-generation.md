---
title: "Mandatory Report Generation for Checker Agents"
description: The requirement that *-checker agents write reports to generated-reports/ with required tools.
category: explanation
subcategory: development
tags: [temporary-files, ai-agents, file-organization, best-practices]
created: 2025-12-01
when_to_use: Use when building or reviewing a *-checker agent.
---

# Mandatory Report Generation for Checker Agents

**CRITICAL REQUIREMENT**: All \*-checker agents MUST write their validation/audit reports to the `generated-reports/` directory. This is a hard requirement for consistency and traceability across all checker agent families.

## Checker Agents That Must Generate Reports

All checker agents in the following families MUST write audit reports to `generated-reports/`:

1. **repo-rules-checker** - Repository consistency validation
2. **apps-ayokoding-www-general-checker** - General content validation (ayokoding-www)
3. **apps-ayokoding-www-by-example-checker** - By-example tutorial validation (ayokoding-www)
4. **apps-ayokoding-www-facts-checker** - Educational content factual accuracy validation
5. **apps-ayokoding-www-link-checker** - Link validation (ayokoding-www)
6. **apps-ose-www-content-checker** - Content validation (ose-www, Next.js)
7. **docs-checker** - Documentation factual accuracy validation
8. **docs-link-checker** - External and internal link validation
9. **docs-tutorial-checker** - Tutorial quality validation
10. **readme-checker** - README quality validation
11. **plan-checker** - Plan readiness validation
12. **plan-execution-checker** - Implementation validation
13. **apps-ayokoding-www-in-the-field-checker** - In-the-field content validation (ayokoding-www)
14. **docs-software-engineering-separation-checker** - Software engineering docs separation validation
15. **repo-workflow-checker** - Workflow documentation quality validation
16. **specs-checker** - Gherkin/BDD specs directory structural and content validation
17. **swe-code-checker** - Software code quality validation

**NO EXCEPTIONS**: Checker agents MUST NOT output results in conversation only. All validation findings MUST be written to audit report files.

## Required Tool Permissions

All checker agents MUST have both `Write` and `Bash` tools in their frontmatter:

- **Write tool** - Required for creating report files in `generated-reports/`
- **Bash tool** - Required for generating UTC+7 timestamps using `TZ='Asia/Jakarta' date +"%Y-%m-%d--%H-%M"`

**Example frontmatter**:

```yaml
---
name: example-checker
description: Validates example content against conventions
tools: Read, Glob, Grep, Write, Bash
model: inherit
color: green
---
```

## Report File Naming Pattern

All checker agents MUST follow the universal naming pattern:

```
{agent-family}__{uuid-chain}__{YYYY-MM-DD--HH-MM}__{type}.md
```

**Components** (4 parts separated by `__`):

- `{agent-family}`: Agent name WITHOUT the `-checker` suffix (e.g., `repo-rules`, `ayokoding-web`, `docs`, `plan`)
- `{uuid-chain}`: Execution hierarchy as underscore-separated 6-char UUIDs (e.g., `a1b2c3`, `a1b2c3_d4e5f6`)
- `{YYYY-MM-DD--HH-MM}`: Timestamp in UTC+7 (double dash between date and time)
- `{type}`: Report type suffix (`audit`, `validation`, `fix`)
