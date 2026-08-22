---
title: "What Every PR Body Must Carry"
description: The four things every PR description states — why the change is needed, what is and is not in scope, where a reader starts, and what the reader may skip.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - pr-review
  - organization
created: 2026-08-22
when_to_use: Use when writing or reviewing a PR description.
---

# What Every PR Body Must Carry

Every PR here is read by a human, whatever else reviews it. Four things make that possible, and
`.github/pull_request_template.md` prompts for all four.

1. **Why the change is needed, not only what changed.** State the problem it solves in enough
   detail that a reader can judge whether the change answers it. A list of edits is not a reason.
2. **What is in scope, and what is deliberately not** — both stated, each with its reason. A
   non-goal without a reason reads as an oversight; with one it is a decision. This is the
   boundary the review loop is held to, so leaving it implicit means there is nothing to hold it
   to.
3. **Where to start reading** — the one file that makes the rest legible.
4. **Which paths to skip** — generated mirrors and mechanical churn, named explicitly.

**Why this binds prose PRs too.** [Code as
Liability](../../../development/practice/code-as-liability/the-obligation.md) makes a PR adding
code state its cost and benefit, but
[what counts as code](../../../development/practice/code-as-liability/what-counts-as-code.md)
excludes Markdown. Without this rule a rules-and-docs PR — most of this repo's traffic — would
carry no why-obligation at all, and its body would degrade to a changelog. That obligation and
this one are separate: a code PR carries both.

**Reviewers may ask.** A missing, vague, or self-contradicting scope statement is a legitimate
finding, not pedantry — it is the one thing the
[Scope Guard](../../../workflows/pr/pr-review-quality-gate/scope-guard-no-scope-creep.md) measures
against. Raise it as `clarify` and answer it by editing the body.

**Review scope.** The PR description is in scope every cycle.
[`pr-review-docs-maker`](../../../../.claude/agents/pr-review/pr-review-docs-maker.md) owns whether
the body accurately describes the diff it ships — a body contradicted by the diff is doc drift.
[`pr-review-governance-maker`](../../../../.claude/agents/pr-review/pr-review-governance-maker.md)
owns whether the required sections are present at all. The body is never frozen by the
correction-record freeze.

**Enforcement**: none automated. The template prompts; the two reviewers check.
