---
name: repo-generating-validation-reports
description: Guidelines for generating validation/audit reports with UUID chains, progressive writing, and UTC+7 timestamps
---

# Generating Validation Reports

Generate validation and audit reports following repository standards for naming, progressive writing, and UUID-based execution tracking.

## When This Skill Loads

This Skill auto-loads for checker and fixer agents that need to generate validation reports in `generated-reports/`.

## Core Knowledge

See [Naming and UUID Chains](./reference/naming-and-uuid.md) for the 4-part report naming pattern, 6-character UUID generation, and scope-based UUID chain logic (parent-child execution tracking) and UTC+7 timestamp generation.

See [Progressive Writing, Templates, Scope, Tools](./reference/progressive-writing-and-templates.md) for the progressive-writing methodology (why buffering is forbidden), the report template structure (header, findings, summary), the scope-definitions table, and required tools.

## Reference Documentation

Complete specifications in:

- [Temporary Files Convention](../../../repo-governance/development/infra/temporary-files.md)
- [Timestamp Format Convention](../../../repo-governance/conventions/formatting/timestamp.md)
- [File Naming Convention](../../../repo-governance/conventions/structure/file-naming.md)

## Usage Example

See [Usage Example](./reference/usage-example.md) for a complete checker-agent startup script (UUID generation, chain logic, timestamp, report initialization).

## Key Principles

1. **Generate UUID early**: First thing at agent startup
2. **Initialize report immediately**: Before any validation begins
3. **Write progressively**: Append findings as you discover them
4. **Use UTC+7 timestamps**: Consistent timezone across all reports
5. **Follow 4-part naming**: Agent-family, UUID chain, timestamp, type
6. **Track execution scope**: Enable parent-child hierarchy for workflows
7. **Require Write+Bash tools**: Essential for report generation

## Common Mistakes to Avoid

❌ **Buffering findings**: Don't collect all findings in memory and write at end (context compaction risk)
✅ **Progressive writing**: Write each finding immediately after discovery

❌ **Wrong timestamp format**: Don't use `YYYY-MM-DD HH:MM` (spaces in filenames)
✅ **Correct format**: Use `YYYY-MM-DD--HH-MM` (double dash separator)

❌ **Missing UUID chain**: Don't use timestamp alone for uniqueness
✅ **UUID chain**: Enables parallel execution without collisions

❌ **Generic scope**: Don't use same scope for all agents
✅ **Specific scope**: Use agent-family or language-specific scope

## Convergence Safeguards

Checker agents re-running across maker-checker-fixer iterations MUST apply the known-false-positive
skip list, scoped re-validation, cached-verification, escalation, and convergence-target rules in
[reference/01-convergence-safeguards.md](./reference/convergence-safeguards.md).

## Integration with Other Skills

Works alongside:

- `repo-assessing-criticality-confidence` - Categorize findings by severity
- `repo-applying-maker-checker-fixer` - Fixer agents read these reports
- Domain Skills (`apps-ayokoding-www-developing-content`, etc.) - Provide validation criteria

## Benefits

1. **Parallelization-safe**: UUID chains prevent file collisions
2. **Traceable**: Can track parent-child execution hierarchy
3. **Resilient**: Progressive writing survives context compaction
4. **Consistent**: Standard naming across all checker agents
5. **Debuggable**: Timestamp and UUID chain aid troubleshooting
