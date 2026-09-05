---
title: "App README vs Specs — Examples: README Trim and PM-Readable Header"
description: Worked before/after examples of trimming Category B content out of an app README, and adding the PM-readability header block to a spec file.
when_to_use: Use when you need a concrete before/after example of applying the content-split rule or the PM-readability header block.
category: explanation
subcategory: conventions
status: "Pilot — initial issue"
tags:
  - conventions
  - readme
  - specs
  - spec-tree-shape
  - pm-readability
  - c4
created: 2026-05-09
---

# Examples: README Trim and PM-Readable Header

## Before/After — App README Trim

**Before** (Category B content in README — 300+ lines):

```markdown
## Routes and Screens

| Route       | Screen       | Description         |
| ----------- | ------------ | ------------------- |
| `/`         | Dashboard    | Main activity feed  |
| `/workouts` | Workout list | All workout history |

...

## Bounded Context Map

The app is split into five bounded contexts: journal, stats, workout-session...
[40 lines of architecture narrative]
```

**After** (Category A only — link pointer for Category B):

```markdown
## Behaviour and Architecture

OrganicLever Web is a productivity tracker. See [specs/apps/organiclever/](../../specs/apps/organiclever/README.md) for routes, screens, bounded-context map, architecture decisions, and design system.
```

## Before/After — PM-Readable Spec File Header

**Before** (no audience block, opens with mechanism):

```markdown
# Architecture

The journal context owns the `JournalEvent` aggregate and exposes `appendEvent`, `bumpEvent`, and `listEvents` use-cases via PGlite store.
```

**After** (Rule 1 header block, Rule 2 intent-before-mechanism):

```markdown
# Architecture

> **Audience**: Engineers, Technical Product/Project Managers
>
> **Plain-language summary**: OrganicLever Web stores and displays productivity data in the browser using a local database. The app divides its logic into five areas — journal (what happened), stats (summaries), workout-session (active workout), routines (templates), and diagnostics. Each area owns its data and exposes a narrow API to the others.

## Journal

The journal records every life-event the user logs — workouts, meals, reading, focus sessions. It is the system of record; every other area either writes events here or reads from here.

Under the hood the journal area uses PGlite (Postgres-WASM — Postgres compiled to WebAssembly running directly in the browser, persisted via IndexedDB) and models its core record as a `JournalEvent` aggregate (a cluster of domain objects treated as one consistent unit by writes).
```
