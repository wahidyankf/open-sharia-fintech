---
title: "Structure Decision"
description: States the no-secrets rule for plan content and the decision rule for choosing single-file versus the default five-document multi-file plan layout.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when deciding whether a new plan should use the single-file or multi-file structure.
---

# Structure Decision

> **No secrets (HARD RULE)**: Plan documents are committed to git. NEVER place system secrets
> — SSH keys, passwords, sensitive usernames, API keys, tokens, or connection strings with real
> credentials — in any plan file. Reference secrets by variable name and location only (e.g.
> "set `DEPLOY_TOKEN` in `.env`"); real values belong in uncommitted files. See the
> [No Secrets in Git convention](../../security/no-secrets-in-committed-files.md).

Plans can use either **single-file** or **multi-file** structure depending on size and complexity.

**Multi-File Structure** (DEFAULT — five documents):

Every new plan MUST use the five-document multi-file layout unless ALL of the exception criteria listed under Single-File Structure are met. When in doubt, use five documents.

- Five separate files: `README.md`, `brd.md`, `prd.md`, `tech-docs.md`, `delivery.md`
- Each file owns one concern (see Content-Placement Rules below), so diffs stay narrow per PR and cross-reviewers can find the section relevant to their concern without skimming an omnibus file

**Single-File Structure** (exception — only when ALL criteria below are met):

A plan MAY collapse to a single `README.md` only when **all** of the following hold simultaneously:

1. Combined business rationale + product scope + tech-docs + delivery fits within 1000 lines total
2. The condensed BRD and condensed PRD sections both fit comfortably in the README without crowding out the technical sections
3. The plan touches at most one subrepo or one narrow concern (single-phase, no new agents/workflows/conventions introduced)
4. The author does not foresee the plan growing mid-execution

If any criterion is unmet, use the five-document layout. If the plan grows past 1000 lines or any criterion is violated mid-execution, promote to the multi-file layout before continuing execution.

**Decision Rule**: The five-document multi-file layout is the required default. Single-file is a bounded exception that requires all four criteria above to be satisfied, not merely a choice based on line-count alone.
