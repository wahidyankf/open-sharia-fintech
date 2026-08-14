---
title: "Agent Naming Conventions"
description: "Defines file naming and scope-prefix guidelines for agent definition files."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when naming or renaming an agent definition file.
---

# Agent Naming Conventions

## File Naming

Agent files follow the authoritative pattern defined in the [Agent Naming Convention](../../../conventions/structure/agent-naming.md). That convention is the single source of truth for agent filenames; the summary below is informational only.

**Pattern**: `<scope>(-<qualifier>)*-<role>` (hyphens only — no underscores, no double-underscores)

Where:

- `scope`: one token from the scope vocabulary in `agent-naming.md` (e.g., `docs`, `repo`, `apps-ayokoding-web`, `plan`)
- `qualifier`: zero or more narrowing tokens (e.g., `by-example`, `software-engineering-separation`)
- `role`: one of `maker`, `checker`, `fixer`, `dev`, `deployer`, etc.

```
PASS: Good - General agents (no scope prefix):
- docs-maker.md
- repo-rules-checker.md
- plan-execution-checker.md
- readme-maker.md

PASS: Good - App-scoped agents:
- apps-ayokoding-www-general-maker.md
- apps-ayokoding-www-by-example-checker.md
- apps-ose-www-content-maker.md
- apps-ose-www-deployer.md

FAIL: Bad:
- DocWriter.md (PascalCase)
- doc_writer.md (snake_case)
- documentation-writer-agent.md (redundant suffix)
- ayokoding-general-maker.md (missing scope)
- apps_ayokoding-web_general-maker.md (underscores forbidden — use hyphens)
- libs__ts-auth__validator.md (double-underscores forbidden — violates file naming convention)
```

See [Agent Naming Convention](../../../conventions/structure/agent-naming.md) for the complete, authoritative naming rule including the full scope vocabulary.

## Scope Prefix Guidelines

**When to use scope prefixes:**

1. **`apps-[app-name]-`** - Agent works ONLY with a specific app
   - Content creation for Next.js sites (ayokoding-www, ose-www)
   - App-specific validation, deployment, structure management
   - Examples: `apps-ayokoding-www-general-maker`, `apps-ose-www-deployer`

2. **`libs-[lib-name]-`** - Agent works ONLY with a specific library
   - Future use when monorepo has libraries with specific agents
   - Library-specific validation, testing, documentation
   - Examples: `libs-ts-auth-validator`, `libs-ts-payment-checker`

**When NOT to use scope prefixes:**

- **General-purpose agents**: Work across entire repository (docs-maker, repo-rules-checker, plan-execution-checker)
- **Cross-cutting agents**: Apply to multiple apps/libs (readme-maker, agent-maker, repo-workflow-maker)
- **Meta-agents**: Manage repository structure (docs-file-manager, repo-rules-maker)

**Scope naming rules:**

- App/lib names must match directory names exactly (e.g., `ayokoding-www` matches `apps/ayokoding-www/`)
- Use kebab-case throughout (no camelCase, PascalCase, or snake_case)
- Hyphens `-` separate all parts of the agent name (consistent kebab-case throughout)
- Agent name after scope uses standard kebab-case patterns
