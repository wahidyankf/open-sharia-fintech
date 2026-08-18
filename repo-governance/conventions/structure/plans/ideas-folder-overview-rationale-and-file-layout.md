---
title: "Ideas Folder (Two-Pagers)"
description: Defines the two-pager idea-brief format, why it exists between a one-liner and a full plan, its file layout, and the rule to fold new ideas into existing briefs rather than duplicating them.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when capturing a new idea in plans/ideas/ or deciding whether it duplicates an existing two-pager.
---

# Ideas Folder (Two-Pagers)

**Location**: `plans/ideas/` (folder at the root of `plans/`)

**Purpose**: Capture pre-plan ideas as **two-pagers** — shortened, promotable idea briefs that are
richer than a one-line todo but deliberately **NOT** the full five-document plan. Each idea is its own
file; the folder carries a `README.md` index. `ideas/` is the first stage of the plan lifecycle:

```text
ideas/ (two-pagers) → backlog/ (full 5-doc plans) → in-progress/ → done/
```

## Why a Two-Pager (Not a One-Liner, Not a Full Plan)

A two-pager sits between a throwaway one-line todo and a full backlog plan: short enough to write in
one sitting and triage at a glance, yet structured enough that a reader can decide whether to promote
it. The format is a synthesis of the common denominator across established short-proposal formats —
Amazon's PR/FAQ, Basecamp's Shape Up "pitch", Architecture Decision Records (ADR), Google's "mini
design doc", and the Rust RFC — all of which name the problem, sketch a solution at a level that
invites debate rather than forecloses it, state what is explicitly out of scope, name the open
questions, and define what success looks like, inside a one-to-two-page ceiling (ADR: _"the whole
document should be one or two pages long"_; Google's mini design doc: _"1-3 pages"_). The full
five-document plan is the deliberately-longer sibling the two-pager is promoted into.

## File Layout

- **`plans/ideas/README.md`** — index of current two-pagers (one bulleted link + one-line hook each),
  a short statement of this convention, and the promotion criteria. Mirrors the shape of
  `backlog/README.md`.
- **`plans/ideas/<slug>.md`** — one two-pager per idea. Kebab-case slug, **no date prefix** (like
  `backlog/` and `in-progress/`; only `done/` carries a date prefix).

## Integrate Before You Add (No Duplicate Two-Pagers)

Before creating a new two-pager, **scan `plans/ideas/` first** (start with its `README.md` index) for
an existing brief that already covers the same problem or area — and **fold the new thought into that
brief** rather than adding a near-duplicate file. Two two-pagers about the same underlying problem
should be one. Consolidate related briefs when they converge on the same idea; split a brief only when
it is genuinely two separable ideas.

This applies equally when the [Knowledge Capture phase](./the-knowledge-capture-phase.md#the-knowledge-capture-phase-final-phase-before-archival)
routes a learning here: check for an existing home before opening a new file. The goal is a folder of
distinct, non-overlapping ideas — not a pile that repeats itself.
