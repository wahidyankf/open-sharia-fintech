---
title: "Purpose and Scope"
description: Why the GitHub Actions workflow naming convention exists, the principles/conventions it implements, and what it does and does not cover.
category: explanation
subcategory: development
tags:
  - github-actions
  - ci-cd
  - naming
  - workflow
created: 2026-03-13
when_to_use: Use when orienting to why the workflow naming convention exists, or checking whether a topic is in scope for it.
---

# Purpose and Scope

## Principles Implemented/Respected

This convention implements/respects the following core principles:

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: The
  mapping between what GitHub Actions displays and what lives on disk is made explicit and
  deterministic. No guessing which file corresponds to a failing workflow run.

- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**: A
  consistent mechanical grammar and derivation rule make it possible to validate filename/name
  alignment automatically, without relying on human review.

## Conventions Implemented/Respected

This practice respects the following conventions:

- **[File Naming Convention](../../../conventions/structure/file-naming.md)**: Workflow filenames use
  kebab-case, consistent with the broader file naming rules applied across the repository.

## Purpose

Two problems motivate this convention:

1. **Discoverability**: GitHub shows the `name:` field in the Actions tab, in PR status checks, and
   in email notifications. When a workflow fails, developers look at the name in the UI then need to
   find and edit the corresponding `.yml` file. Without a consistent mapping rule, locating the right
   file requires opening files until the matching name is found.

2. **Grouping**: Sorting `.github/workflows/` alphabetically should cluster files by the product/domain
   they serve. A domain-first filename prefix (`organiclever-app-*`, `commons-*`, etc.) ensures related
   workflows appear together regardless of what action they perform.

This convention eliminates both friction points with a two-part standard: a domain-first grammar for
the filename and a deterministic derivation rule for the `name:` field.

## Scope

### What This Convention Covers

- All workflow files under `.github/workflows/`
- The relationship between the `name:` field and the `.yml` filename
- The `_reusable-` prefix for `workflow_call` reusable workflows

### What This Convention Does NOT Cover

- Workflow content, structure, or job naming
- Composite actions (`.github/actions/setup-*`) — these follow their own naming rules
- Fast-gate test policy (no integration/e2e in PR gates) — see
  [CI Conventions](../ci-conventions.md)
