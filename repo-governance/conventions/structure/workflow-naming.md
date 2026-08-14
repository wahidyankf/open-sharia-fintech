---
title: "Workflow Naming Convention"
description: Single rule for workflow filename structure under repo-governance/workflows
when_to_use: Read this when naming a new workflow file, or validating an existing workflow filename against the scope/type structure.
category: explanation
subcategory: conventions
tags:
  - workflows
  - naming
  - conventions
created: 2026-04-17
---

# Workflow Naming Convention

Workflows under `repo-governance/workflows/` follow a **single filename rule with no exceptions**, except for reference documentation under `repo-governance/workflows/meta/` (which describes the workflow system rather than being a workflow).

## In This Convention

- [Why This Rule Exists and The Rule](./workflow-naming/01-why-this-rule-exists-and-the-rule.md) — rationale plus the exact `<scope>(-<qualifier>)*-<type>` filename structure
- [Scope Vocabulary](./workflow-naming/02-scope-vocabulary.md) — valid first-segment scope tokens
- [Type Vocabulary](./workflow-naming/03-type-vocabulary.md) — valid last-segment type tokens and their semantics
- [Meta Exception, Applies To, Enforcement, and Examples](./workflow-naming/04-meta-exception-applies-to-enforcement-and-examples.md) — the `meta/` exemption, scope of applicability, the enforcement command, and worked examples
- [Related Documentation and Principles](./workflow-naming/05-related-and-principles.md) — sibling naming conventions and the principles this convention implements
