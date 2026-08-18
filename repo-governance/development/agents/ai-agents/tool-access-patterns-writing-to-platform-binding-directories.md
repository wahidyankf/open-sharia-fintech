---
title: "Tool Access Patterns — Writing to Platform Binding Directories"
description: "Defines which tools an agent needs when it writes to a platform binding directory such as .claude/agents/."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when an agent's frontmatter tools list needs to support writing to a platform binding directory.
---

# Tool Access Patterns — Writing to Platform Binding Directories

Use the normal `Write` / `Edit` tools for files in `.claude/` and `.opencode/`. Both paths are pre-authorized in the platform settings (`Write(.claude/**)`, `Edit(.claude/**)`, `Write(.opencode/**)`, `Edit(.opencode/**)`), so no approval prompts fire. `Bash` heredoc and `sed` remain appropriate for bulk mechanical substitutions across many files, but there is no restriction on direct edits.

**Applies to**:

- Creating or updating agent files in `.claude/agents/` or `.opencode/agents/`
- Creating or updating skill files in `.claude/skills/*/SKILL.md` or `.claude/skills/*/SKILL.md`
- Updating the corresponding `README.md` index files

**Sync requirement**: After editing `.claude/` sources, run `npm run generate:bindings` to regenerate all secondary binding artifacts (`.opencode/agents/`, `.amazonq/`). The pre-commit hook validates both formats.
