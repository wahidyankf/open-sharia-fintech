---
description: Explains why the plans/ convention exists, what it covers and excludes, and the high-level lifecycle and no-secrets rule for plan documents.
when_to_use: Use when orienting to why plans/ is organized the way it is, or checking whether a topic is in scope for this convention.
---

# Purpose, Scope, and Overview

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: Flat structure with three clear states (backlog, in-progress, done). No complex nested hierarchies or status tracking systems.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: The stage-aware naming convention makes lifecycle state explicit. `backlog/` and `in-progress/` use no date prefix; `done/` uses a completion-date prefix (added only at archival). File location (backlog/, in-progress/, done/) indicates status — no hidden metadata or databases required.

## Purpose

This convention establishes the organization and quality contract for project planning documents in
the `plans/` directory. A formal plan is a comprehensive, traceable decision-to-delivery record for
an engineer new to the repository and stack, not merely a delivery checklist.

## Scope

### What This Convention Covers

- **Plans directory structure** - ideas/, backlog/, in-progress/, done/ organization
- **Folder naming pattern** - stage-aware: no date prefix in `backlog/` or `in-progress/`; completion-date prefix in `done/` only
- **File organization** - What files belong in each folder
- **Lifecycle stages** - How plans move from ideas → backlog → in-progress → done
- **Project identifiers** - How to name projects consistently

### What This Convention Does NOT Cover

- **Plan content quality** - Audience, reasoning, structure, delivery packets, and validation
- **Project management methodology** - This is file organization, not PM process
- **Task tracking** - Covered by the [plan-execution workflow](../../../workflows/plan/plan-execution.md) (orchestrated directly by the calling context)
- **Deployment scheduling** - Covered in deployment conventions

## Overview

The `plans/` folder serves as the workspace for project planning activities:

- **Purpose**: Temporary project planning and tracking
- **Location**: Root-level `plans/` folder (not inside `docs/`)
- **Lifecycle**: Plans move between subfolders as work progresses
- **Format**: Structured markdown documents following specific naming and organization conventions

**Key Distinction**: Plans are temporary working documents that eventually move to `done/` and may be archived, while `docs/` contains permanent documentation that evolves over time.

Creating a durable plan requires literal user authorization. Use the harness task list for internal
planning and `local-tmp/` for temporary findings; neither authorizes a new `plans/` artifact.

**No secrets in plans**: Plan documents are committed to git — including `done/` history, which is permanent. Never put a secret value (credentials, SSH keys, tokens, API keys, sensitive usernames, or connection strings with real credentials) in any plan. Name the variable and state where the value lives, never the value itself. This is a hard iron rule — see [No Secrets in Git](../../security/no-secrets-in-committed-files.md).
