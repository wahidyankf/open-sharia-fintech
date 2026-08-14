---
title: "Purpose and Scope"
description: Why structured grilling replaces open-ended prose questions, and what this convention covers versus what it explicitly leaves to other conventions.
category: explanation
subcategory: development
tags:
  - planning
  - grill-me
  - user-interaction
  - plan-maker
  - design-decisions
  - interaction
  - agents
created: 2026-05-26
when_to_use: Use when deciding whether a given design-decision interaction falls under this convention or one of its companions.
---

# Purpose and Scope

## Purpose

Open-ended questions ("What approach do you want?") produce vague answers, require follow-up
clarification, and shift cognitive burden from the agent to the user. Structured
multiple-choice grilling resolves this by:

1. Requiring the agent to explore the repo and enumerate concrete options before asking.
2. Giving the user a small, well-defined decision surface rather than a blank canvas.
3. Making trade-offs explicit so decisions are reversible and auditable in the plan.
4. Using the harness's native interactive tool when available, so options are rendered as
   selectable choices rather than prose the user must parse.

## Scope

### What This Convention Covers

- All grilling interactions during plan creation (pre-write and post-write grill sessions).
- All grilling steps in the plan establishment workflow (Steps 1 and 3).
- Pre-execution grilling of unresolved design decisions before plan execution begins.
- Any "grill me" design-review or stress-testing session invoked explicitly by the user.
- The interaction format, option structure, Recommended marking, and mechanism (native tool
  vs. markdown fallback).

### What This Convention Does Not Cover

- The content of individual grilling questions (domain-specific; defined by the agent or
  workflow that invokes the grill).
- Plan document structure (see
  [Plans Organization Convention](../../../conventions/structure/plans.md)).
- Agent file structure and frontmatter (see
  [AI Agents Convention](../../agents/ai-agents.md)).
- Commit message format for decisions captured in plans (see
  [Commit Message Convention](../commit-messages.md)).
