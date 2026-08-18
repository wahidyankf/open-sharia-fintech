---
title: "Best Practices"
description: Gives working habits for plans - never put secrets in them, keep them focused, update them as you go, use the ideas folder liberally, maintain indices, and archive rather than delete completed plans.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when looking for day-to-day working habits for maintaining plan documents over their lifecycle.
---

# Best Practices

## Never Put Secrets in Plans

Plans are committed to git, so the [No Secrets in Git](../../security/no-secrets-in-committed-files.md) hard iron
rule applies in full. Never paste system secrets (SSH/private keys, passwords, API tokens, privileged
usernames, certificates, connection strings, and similar) into any plan document. When a plan must
reference a secret, name the environment variable (e.g. `DATABASE_URL`) or use a placeholder
(`<API_TOKEN>`); the real value lives in an uncommitted `.env*` file (except `.env.example`) or
another gitignored file.

## Keep Plans Focused

- One plan per project or major feature
- Break large initiatives into multiple plans
- Each plan should have clear, achievable scope

## Update Plans as You Go

- Plans are living documents during execution
- Update technical docs when making design decisions
- Check off deliverables as completed
- Add notes about challenges or learnings

## Use the Ideas Folder Liberally

- Before adding a new two-pager, scan `plans/ideas/` for an existing brief on the same problem and fold it in — don't repeat yourself (see [Integrate Before You Add](./ideas-folder-overview-rationale-and-file-layout.md#integrate-before-you-add-no-duplicate-two-pagers))
- Capture an idea as a two-pager as soon as it is worth more than a passing thought — one file per _distinct_ idea
- Keep it a brief, not a plan: fill each section with a real answer, including honest open questions
- Review two-pagers periodically and promote ripe ones to full `backlog/` plans
- Delete two-pagers that are no longer relevant (they carry no history worth keeping — that is what `done/` is for)

## Maintain Indices

- Always update subfolder README.md when moving plans
- Keep descriptions current and accurate
- Remove completed plans from in-progress index promptly

## Archive Completed Plans

- Don't delete completed plans - move them to `done/`
- Completed plans serve as historical record
- Review past plans to learn from successes and challenges
- Use completed plans as templates for similar future work
