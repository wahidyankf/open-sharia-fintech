---
title: "Examples"
description: Shows a complete worked single-file plan, a multi-file plan's folder layout, and a full two-pager idea brief example.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when you want a concrete worked example of a single-file plan, a multi-file plan layout, or a two-pager.
---

# Examples

## Example: Small Plan (Single-File)

```
2025-12-05__add-user-search/
└── README.md                # ~400 lines total
```

**README.md structure**:

```markdown
# Add User Search Feature

## Context

Brief description and background...

## Scope

In-scope features, out-of-scope items, affected apps...

## Business Rationale (condensed BRD)

Why this matters, affected roles, success metrics (observable facts preferred; judgment calls labeled)...

## Product Requirements (condensed PRD)

User stories (As a … I want … So that …), Gherkin acceptance criteria, product scope...

## Technical Approach

API design, database changes, implementation notes...

## Delivery Checklist

Phased `- [ ]` items, one action per checkbox...

## Quality Gates

`apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push` (includes `nx affected -t test:quick`), markdown lint, manual verification...

## Verification

How to confirm done...
```

## Example: Large Plan (Multi-File)

```
2025-12-05__migrate-to-microservices/
├── README.md                # ~100 lines (overview + navigation)
├── brd.md                   # ~150 lines (business goal, impact, affected roles, success metrics)
├── prd.md                   # ~250 lines (personas, user stories, Gherkin acceptance criteria, product scope)
├── tech-docs.md             # ~800 lines (architecture + API specs + file impact analysis)
└── delivery.md              # ~200 lines (phased rollout plan)
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
