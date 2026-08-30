---
title: "Examples"
description: Shows the retired single-file boundary, the current mature formal-plan layout, and a full two-pager idea brief example.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when you want a concrete mature-plan layout, transition example, or two-pager.
---

# Examples

## Example: Existing Small Plan (Retired Shape)

An existing all-in-one `README.md` plan may complete under its recorded contract when it predates
the current structure rule. Never use this example to create a new formal plan.

## Example: Mature Formal Plan

```
<plan-identifier>/
├── README.md                # ~100 lines (overview + navigation)
├── brd.md                   # ~150 lines (business goal, impact, affected roles, success metrics)
├── prd.md                   # ~250 lines (personas, user stories, Gherkin acceptance criteria, product scope)
├── tech-docs.md             # ~800 lines (architecture + API specs + file impact analysis)
├── delivery.md              # Phased outcomes with granular action checklists
└── learnings.md             # Transient Knowledge Capture log
```

## Example: Two-Pager Idea Brief

A single `plans/ideas/<slug>.md`, e.g. `plans/ideas/api-rate-limiting.md`:

```markdown
# API rate limiting

One-line summary: cap per-client request rates so a single caller cannot degrade the API for everyone.

> Surfaced 2026-03-14 during load-testing-hardening execution.

## Problem / context

During load testing one misconfigured client sent ~40 req/s and drove p99 latency for all other
callers above 2s. Nothing in the stack bounds a single client's request rate today.

## Why now

We are about to expose the API to third-party integrators, so an abusive or buggy caller stops being
hypothetical.

## Proposed direction (sketch)

- A token-bucket limiter keyed by API key, enforced at the edge.
- Return `429` with a `Retry-After` header when the bucket is empty.
- Per-key limits configurable; a sane default applies when unset.

## Rough scope & non-goals

In scope: per-key request-rate limiting and the `429` response.
Out of scope (for now): per-endpoint quotas, billing/usage metering, distributed limiter state.

## Risks & open questions

- Where does limiter state live so it survives multiple API instances? (open)
- What default rate is generous enough not to break normal integrators? (open — needs a baseline)

## What success looks like + promotion signal

Success: one abusive key can no longer raise other callers' p99. Ready to promote once the state-store
question is answered well enough to design against — the rest is full-plan work.
```
