---
title: "Directory Status, Exceptions, and Related Conventions"
description: Confirms both directories are gitignored and when another convention overrides this default.
category: explanation
subcategory: development
tags: [temporary-files, ai-agents, file-organization, best-practices]
created: 2025-12-01
when_to_use: Use when confirming gitignore status.
---

# Directory Status, Exceptions, and Related Conventions

## ️ Directory Status

Both directories are **gitignored** (not tracked by version control):

Under the "Temporary files" section (line 70):

- `local-tmp/`

Under the "Generated reports" section (line 73):

- `generated-reports/`

Under the "Execution tracking files" section:

- `generated-reports/.execution-chain-*`

Files in these directories will not be committed to the repository.

**Note**: The `.execution-chain-{scope}` files are hidden files within `generated-reports/` used for parent-child execution tracking. They are automatically gitignored via the `generated-reports/` pattern.

## Exception Handling

The rule includes "unless specified otherwise by other repo-governance/conventions":

- If a specific convention already defines where certain files should go, **follow that convention instead**
- This rule serves as the **default/fallback** for temporary files
- When in doubt, use these directories rather than creating files in the repository root

**Example exceptions**:

- **Operational metadata files** - Use `docs/metadata/` instead (e.g., `external-links-status.yaml` is committed to git, not temporary)
- **Manual-verification evidence** - Screenshots and exported reports proving a plan's manual checks are **committed**, not temporary, and belong in that plan's own `evidence/` subfolder — see [The Rule](../../quality/evidence-capture/02-the-rule.md). A root-anchored `/evidence/` entry in `.gitignore` catches the repo-root misplacement, so evidence written there silently never stages
- Agent-specific conventions may override this rule
- Task-specific requirements may specify different locations
- User instructions may explicitly request different locations

## Related Conventions

- [Build-Artifact Sweeper Convention](../build-artifact-sweeper.md) - The complementary boundary: an ambient sweeper removes gitignored **build output and caches** (`target/`, `dist/`, `.next/`, `.nx/cache`) at any time, but never the agent-owned `generated-reports/` and `local-tmp/` directories defined here. A report or scratch file missing is therefore never explained by a sweep
- [File Naming Convention](../../../conventions/structure/file-naming.md) - For permanent documentation files
- [Evidence Capture — The Rule](../../quality/evidence-capture/02-the-rule.md) - Where committed manual-verification artifacts live, and the `.gitignore` guard behind it
- [AI Agents Convention](../../agents/ai-agents.md) - For agent design and tool access
- [Diátaxis Framework](../../../conventions/structure/diataxis-framework.md) - For documentation organization

## Benefits

This convention provides:

1. **Clear Organization** - Temporary files are isolated from permanent content
2. **Prevent Clutter** - No temporary files scattered across the repository
3. **Easy Cleanup** - Both directories can be safely cleared when needed
4. **Traceability** - Generated reports include dates for tracking
5. **Consistent Behavior** - All agents follow the same pattern

## Important Notes

- Always use one of these directories for temporary files (never the repository root)
- Choose `generated-reports/` for structured reports, `local-tmp/` for everything else
- Include dates in report filenames for traceability
- Remember these files are gitignored and won't be committed
- Clean up old files periodically to prevent accumulation
