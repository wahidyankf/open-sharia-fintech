---
title: "Related Documentation"
description: "Links to related conventions and agent files."
category: explanation
subcategory: development
tags:
  - maker-checker-fixer
  - workflow
  - content-quality
  - agent-patterns
  - validation
  - automation
created: 2025-12-14
when_to_use: "Use to find the doc backing this pattern."
---

# Related Documentation

**Pattern Implementation**:

- [AI Agents Convention](../../agents/ai-agents.md) - Agent structure and tool permissions
- [Repository Validation Methodology](../../quality/repository-validation.md) - Validation patterns and techniques
- [Temporary Files Convention](../../infra/temporary-files.md) - Report storage and naming

**Workflow Orchestration**:

- [Workflow Pattern Convention](../../../workflows/meta/workflow-identifier.md) - How workflows orchestrate agents

**Domain-Specific Standards**:

- [Content Quality Principles](../../../conventions/writing/quality.md) - Universal content standards
- [Tutorial Convention](../../../conventions/tutorials/general.md) - Tutorial quality standards
- [README Quality Convention](../../../conventions/writing/readme-quality.md) - README standards

**Agent Examples**:

- `.claude/agents/repo/rules-maker.md` - Example maker agent
- `.claude/agents/repo/rules-checker.md` - Example checker agent
- `.claude/agents/repo/rules-fixer.md` - Example fixer agent
- `.claude/agents/apps-ayokoding-www/apps-ayokoding-www-general-maker.md` - General Next.js content maker
- `.claude/agents/apps-ayokoding-www/apps-ayokoding-www-by-example-maker.md` - By-example tutorial maker
- `.claude/agents/apps-ayokoding-www/apps-ayokoding-www-general-checker.md` - General Next.js content checker
- `.claude/agents/apps-ayokoding-www/apps-ayokoding-www-by-example-checker.md` - By-example tutorial checker
- `.claude/agents/apps-ayokoding-www/apps-ayokoding-www-general-fixer.md` - General Next.js content fixer
- `.claude/agents/apps-ayokoding-www/apps-ayokoding-www-by-example-fixer.md` - By-example tutorial fixer

---

This pattern provides a **systematic, scalable, and safe approach** to content quality management across multiple domains. By separating creation, validation, and remediation into distinct stages, we achieve high-quality content through iterative improvement and automated safeguards.
