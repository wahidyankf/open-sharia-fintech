---
description: "Domain-first filename grammar and name-mirrors-filename rule for all workflow files"
when_to_use: "Read this index to find the right GitHub Actions Workflow Naming Convention child document."
---

# GitHub Actions Workflow Naming Convention

- [Purpose and Scope](./purpose-and-scope.md) — Why the GitHub Actions workflow naming convention exists, the principles/conventions it implements, and what it does and does not cover. Use when orienting to why the workflow naming convention exists, or checking whether a topic is in scope for it.
- [Filename Grammar and Vocabulary](./filename-grammar-and-vocabulary.md) — The domain-first filename grammar for GitHub Actions workflow files and the fixed verb/qualifier vocabulary used to compose the action-chain segment. Use when composing a workflow filename — choosing its domain and stringing together verbs/qualifiers in execution order.
- [Name Derivation](./name-derivation.md) — The mechanical derivation rule from filename to `name:` field, and the character transformation table it applies. Use when deriving or checking a workflow's `name:` field against its filename, character by character.
- [Deploy Model and Examples](./deploy-model-and-examples.md) — How "deploy" maps to branch force-pushes for web and backend tiers, and worked PASS/FAIL examples of the filename/name derivation rule. Use when tracing what a workflow's "deploy" step actually does, or when checking a candidate filename/name pair against PASS/FAIL examples.
- [Target File Set](./target-file-set.md) — The canonical 17-workflow-file set established by the standardize-github-actions-pipeline-naming plan, organized by tier. Use when checking whether a workflow filename already exists in the canonical set, or when adding a new filename to it.
- [Special Considerations](./special-considerations.md) — Abbreviation rules for long filenames, language/framework identifier mapping, version alignment policy, and the checklist for adding a new workflow. Use when a derived filename is too long, when aligning a language version across workflows, or when adding a new workflow to the canonical set.
- [Tools and References](./tools-and-references.md) — The validating tooling and agents that enforce this convention, and related development standards and naming conventions. Use when locating the tooling/agents that enforce this convention or finding related naming conventions.
