---
title: "Per-Repository Delivery Mode Restrictions — Enforcement and File Naming"
description: States that main-to-pr is unused despite being technically available, the plan-checker enforcement for invalid delivery-mode fields, and the file-naming rule for files inside a plan folder.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when checking why main-to-pr is never selected, or when naming a file inside a plan folder.
---

# Per-Repository Delivery Mode Restrictions — Enforcement and File Naming

Continues [Per-Repository Delivery Mode Restrictions (HARD RULE)](./per-repository-delivery-mode-restrictions.md).

`main-to-pr` is not blocked by protection in `ose-public` — it still opens a PR — but
is not used either: every plan here uses **`worktree-to-pr`**, with no exception. The
[Plan-Docs-Only Carve-Out](../../../workflows/plan/plan-planning/plan-docs-only-carve-out.md#the-plan-docs-only-carve-out-superseded--retired-in-ose-public)
and the `.md`-only condition of the content restriction above are **retired** here — direct push is
disallowed by this rule regardless of file content.

**Why this is a hard rule**: a direct push bypasses the branch-protected PR route and its exact-head
`Quality gate`. Narrowing that bypass across both repositories to the one case with a genuine
technical reason (secrets and state that cannot leave the primary checkout) closes the gap between
"convenient" and "actually necessary" that the old `.md`-only carve-out left open everywhere.

**Enforcement**: `plan-checker` flags a `## Delivery Mode` field naming `worktree-to-origin-main` or
`main-to-origin-main` in `ose-public` as **HIGH** — those modes have no executable
path there. It flags the same fields in `ose-private` as **HIGH** unless the plan
is genuinely an infrastructure-as-code plan.

## Important Note on File Naming

Files inside plan folders use descriptive kebab-case names or short industry-standard acronyms (e.g., `brd.md`, `prd.md`, `tech-docs.md`, `delivery.md`). The folder structure provides sufficient context, so the filename only needs to describe its purpose.
