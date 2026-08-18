---
title: "GitHub Actions Workflow Naming Convention"
description: Domain-first filename grammar and name-mirrors-filename rule for all workflow files
category: explanation
subcategory: development
tags:
  - github-actions
  - ci-cd
  - naming
  - workflow
created: 2026-03-13
when_to_use: Use when naming a new GitHub Actions workflow file or its `name:` field, or when auditing an existing workflow filename/name pair for alignment.
---

# GitHub Actions Workflow Naming Convention

GitHub Actions workflow files live in `.github/workflows/`. Two rules govern every file in that
directory: the **domain-first filename grammar** (what the file is called) and the
**`name:`-mirrors-filename rule** (what the `name:` field inside the file must say). The sections
below are split across the following documents.

## Sections

- [Purpose and Scope](./github-actions-workflow-naming/purpose-and-scope.md) — Why the GitHub Actions workflow naming convention exists, the principles/conventions it implements, and what it does and does not cover. Use when orienting to why the workflow naming convention exists, or checking whether a topic is in scope for it.
- [Filename Grammar and Vocabulary](./github-actions-workflow-naming/filename-grammar-and-vocabulary.md) — The domain-first filename grammar for GitHub Actions workflow files and the fixed verb/qualifier vocabulary used to compose the action-chain segment. Use when composing a workflow filename — choosing its domain and stringing together verbs/qualifiers in execution order.
- [Name Derivation](./github-actions-workflow-naming/name-derivation.md) — The mechanical derivation rule from filename to `name:` field, and the character transformation table it applies. Use when deriving or checking a workflow's `name:` field against its filename, character by character.
- [Deploy Model and Examples](./github-actions-workflow-naming/deploy-model-and-examples.md) — How "deploy" maps to branch force-pushes for web and backend tiers, and worked PASS/FAIL examples of the filename/name derivation rule. Use when tracing what a workflow's "deploy" step actually does, or when checking a candidate filename/name pair against PASS/FAIL examples.
- [Target File Set](./github-actions-workflow-naming/target-file-set.md) — The canonical 17-workflow-file set established by the standardize-github-actions-pipeline-naming plan, organized by tier. Use when checking whether a workflow filename already exists in the canonical set, or when adding a new filename to it.
- [Special Considerations](./github-actions-workflow-naming/special-considerations.md) — Abbreviation rules for long filenames, language/framework identifier mapping, version alignment policy, and the checklist for adding a new workflow. Use when a derived filename is too long, when aligning a language version across workflows, or when adding a new workflow to the canonical set.
- [Tools and References](./github-actions-workflow-naming/tools-and-references.md) — The validating tooling and agents that enforce this convention, and related development standards and naming conventions. Use when locating the tooling/agents that enforce this convention or finding related naming conventions.
