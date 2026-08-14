---
title: "Workflow Naming: Related Documentation and Principles"
description: Sibling naming conventions related to workflow naming and the software engineering principles this convention implements
when_to_use: Read this when looking up a sibling naming convention or the principles this convention is built on.
category: explanation
subcategory: conventions
tags:
  - workflows
  - naming
  - conventions
created: 2026-04-17
---

# Workflow Naming: Related Documentation and Principles

## Related

- [`repo-governance/workflows/README.md`](../../../workflows/README.md) — Operational catalog of workflows.
- [Agent Naming Convention](../agent-naming.md) — Sibling rule governing `.claude/agents/*.md` and `.opencode/agents/*.md` filenames. Uses aligned scope vocabulary (`repo`, not `repository`).
- [File Naming Convention](../file-naming.md) — Sibling filename rule for non-workflow files.

## Principles Implemented/Respected

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)** — The scope and type of every workflow are explicit in its filename; no convention-by-tribal-knowledge.
- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)** — One rule, one type list, one regex. One documented exception (meta).
- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)** — A single-line `find | grep` decides conformance, enabling mechanical enforcement by `repo-rules-checker` and `rhino-cli repo-governance workflows naming validate`.
