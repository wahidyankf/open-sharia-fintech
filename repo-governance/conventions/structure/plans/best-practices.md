---
title: "Best Practices"
description: Gives working habits for plans - apply minimal sufficiency, keep them focused and secret-free, update them as you go, maintain indices, and archive completed plans.
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

## Apply [Minimal Sufficiency](../../../principles/general/simplicity-over-complexity/minimal-sufficiency-test.md)

- Treat the requested outcome, explicit non-goals and out-of-scope items, acceptance criteria, and
  required quality gates as the plan's boundary and stop condition
- For each new lasting mechanism, record its concrete need and why existing mechanisms are
  insufficient in `tech-docs.md`, or in a single-file plan's `Technical Approach`
- Choose the smallest responsible design that meets the outcome and every applicable rule; do not
  generalize one-off work or silently expand delivery beyond the stated boundary
- Keep every mandatory safeguard in scope; it is part of sufficiency

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
