---
title: "Special Considerations"
description: Abbreviation rules for long filenames, language/framework identifier mapping, version alignment policy, and the checklist for adding a new workflow.
category: explanation
subcategory: development
tags:
  - github-actions
  - ci-cd
  - naming
  - workflow
created: 2026-03-13
when_to_use: Use when a derived filename is too long, when aligning a language version across workflows, or when adding a new workflow to the canonical set.
---

# Special Considerations

## Permitted abbreviations for long names

When the fully derived filename would be excessively long (over 60 characters before `.yml`),
abbreviations are permitted provided they are applied consistently and the mapping remains obvious.
Established abbreviations in this codebase:

| Full word/phrase | Abbreviation |
| ---------------- | ------------ |
| `Backend`        | `be`         |
| `Staging`        | `stag`       |
| `Production`     | `prod`       |

When using an abbreviation, update this table so the mapping remains documented and reviewable.

## Language/framework identifiers in parentheses

The pattern `(Language/Framework)` in a name maps to `language-framework` in the filename:
parentheses are removed, the `/` is removed, a hyphen separates language from framework, and the
whole segment is lowercased. For example, `(Rust/Axum)` → `rust-axum`.

## Version Alignment Policy

`pr-quality-gate.yml` is the **source of truth** for language version choices. All scheduled
test and deploy workflows must use the same language versions as `pr-quality-gate.yml`.

**Rule**: When upgrading a language version in `pr-quality-gate.yml`, update all deploy
workflows that use that language in the same commit. Version drift creates inconsistencies where CI
passes on `main` but manually dispatched tests fail (or vice versa).

**Workflows that must stay aligned**:

| Language | `pr-quality-gate.yml` step | Scheduled workflows to update                                                       |
| -------- | -------------------------- | ----------------------------------------------------------------------------------- |
| Node.js  | `node-version`             | All workflows installing Node.js                                                    |
| .NET     | `dotnet-version`           | `organiclever-app-test-local-deploy-stag.yml`, `ose-app-test-local-deploy-stag.yml` |

## Adding new workflows

When creating a new workflow:

1. Identify the domain (app group or cross-cutting qualifier).
2. Compose the `{action-chain}` from the verb/qualifier vocabulary, left-to-right in execution
   order.
3. Prefix with `_reusable-` only if the workflow uses `on: workflow_call`.
4. Derive the `name:` field from the filename using the derivation rule above.
5. If the derived name would exceed 60 characters, apply a documented abbreviation.
6. Add the new filename to the target file set table in this document.
