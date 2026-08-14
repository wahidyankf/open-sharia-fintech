---
title: "Workflow Naming: Meta Exception, Applies To, Enforcement, and Examples"
description: The meta/ reference-documentation exception to the naming rule, the files the rule applies to, the enforcement command, and worked filename examples for every type
when_to_use: Read this when checking whether a file under workflows/meta/ is exempt, running the naming-rule enforcement command, or reviewing example conforming filenames.
category: explanation
subcategory: conventions
tags:
  - workflows
  - naming
  - conventions
created: 2026-04-17
---

# Workflow Naming: Meta Exception, Applies To, Enforcement, and Examples

## Meta reference exception

Files under `repo-governance/workflows/meta/` are **reference documentation about the workflow system itself** (e.g., `execution-modes.md`, `workflow-identifier.md`). They describe how workflows are identified, how they are executed, and which patterns govern them. They are not workflows and therefore are exempt from the type-suffix rule.

This is the **only** exception. Every other file under `repo-governance/workflows/` that is not a `README.md` index MUST conform to the rule.

## Applies To

This convention applies to:

- **All `.md` files under `repo-governance/workflows/**/\*.md`\*\* except:
  - `repo-governance/workflows/README.md` and any per-scope `repo-governance/workflows/<scope>/README.md` index files.
  - Everything under `repo-governance/workflows/meta/` (reference material).

## Enforcement

`repo-rules-checker` MUST run the following audit command as part of every governance pass:

```bash
find repo-governance/workflows -name '*.md' -not -name 'README.md' -not -path '*/meta/*' \
  | sed 's|.*/||; s|\.md$||' \
  | grep -vE -- '-(quality-gate|execution|setup|planning|grooming)$'
```

Any non-empty output is a governance violation. Each line printed is a workflow filename whose suffix does not match the Type Vocabulary; each such file MUST be renamed to a compliant name before the checker can pass.

The `rhino-cli repo-governance workflows naming validate` subcommand wraps this check plus a frontmatter `name:` field consistency check and is wired into Husky pre-push and the CI quality gate.

## Examples

Current workflows, grouped by type, all conforming to the rule:

- **`quality-gate`** — `plan-quality-gate` (scope `plan`, type `quality-gate`), `repo-rules-quality-gate` (scope `repo`, qualifier `rules`, type `quality-gate`), `specs-quality-gate` (scope `specs`, type `quality-gate`), `docs-quality-gate` (scope `docs`, type `quality-gate`), `ci-quality-gate` (scope `ci`, type `quality-gate`), `ui-quality-gate` (scope `ui`, type `quality-gate`), `ayokoding-web-swe-by-example-quality-gate` (scope `ayokoding-web`, qualifier `by-example`, type `quality-gate`), `pdf-to-md-quality-gate` (scope `pdf-to-md`, type `quality-gate`, hosted in `content/` directory), `pr-review-quality-gate` (scope `pr`, qualifier `review`, type `quality-gate`)
- **`execution`** — `plan-execution` (scope `plan`, type `execution`)
- **`planning`** — `plan-planning` (scope `plan`, type `planning`), `plan-idea-promotion-planning` (scope `plan`, qualifier `idea-promotion`, type `planning`), `repo-dependency-bump-planning` (scope `repo`, qualifier `dependency-bump`, type `planning`), `web-ux-test-fixing-planning` (scope `web`, qualifier `ux`, descriptor `test-fixing`, type `planning`)
- **`setup`** — `infra-development-environment-setup` would be the fully qualified form; the file is stored as `development-environment-setup.md` in the `infra/` directory, making the scope implicit from directory location. The enforcement command (type-suffix check) passes. New `setup` workflows SHOULD include the scope prefix explicitly (e.g., `infra-something-setup.md`).
- **`grooming`** — `plan-ideas-grooming` (scope `plan`, type `grooming`)
