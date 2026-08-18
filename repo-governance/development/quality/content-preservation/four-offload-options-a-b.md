---
title: "Four Offload Options (A-B)"
description: "Option A (new convention doc) and Option B (merge into existing)."
category: explanation
subcategory: development
tags:
  - content-preservation
  - condensation
  - offload
  - zero-loss
  - documentation
created: 2025-12-14
when_to_use: "Use when creating a new convention doc or merging into an existing one."
---

# Four Offload Options (A-B)

## Option A: Create New Convention Document

**When to use:** Content represents a new convention or standard not yet documented.

**Process:**

1. Identify the convention topic (e.g., "acceptance criteria format")
2. Use `docs-maker` to create new convention doc in `repo-governance/conventions/` or `repo-governance/development/`
3. Move ALL relevant content to new convention (comprehensive detail)
4. Replace original content with 2-5 line summary + link
5. Update appropriate index (`repo-governance/conventions/README.md` or `repo-governance/development/README.md`)
6. Verify all cross-references work

**Example:**

- **Before:** Gherkin acceptance criteria details in `plan-maker.md` (500 lines)
- **After:**
  - New file: `repo-governance/development/infra/acceptance-criteria.md` (comprehensive)
  - `plan-maker.md`: "Use Gherkin format. See [Acceptance Criteria Convention](../../infra/acceptance-criteria.md)" (3 lines)
  - Savings: 497 lines

## Option B: Merge into Existing Convention

**When to use:** Content expands or clarifies an existing convention.

**Process:**

1. Identify the most relevant existing convention doc
2. Read convention doc to understand current content
3. Add new content to appropriate section (maintain structure)
4. Update frontmatter (`updated` date)
5. Replace original content with summary + link
6. Verify convention doc is indexed

**Example** (historical — `plan-executor.md` was later removed when plan execution moved into the plan-execution workflow orchestrated by the calling context):

- **Before:** TBD workflow details duplicated in `plan-maker.md` and `plan-executor.md`
- **After:**
  - Updated: `repo-governance/development/workflow/trunk-based-development.md` (comprehensive)
  - `plan-maker.md`: "Follow TBD workflow. See [TBD Convention](../../workflow/trunk-based-development.md)" (2 lines)
  - `plan-executor.md`: "Default to main branch per TBD. See [TBD Convention](../../workflow/trunk-based-development.md)" (2 lines)
  - Savings: Duplication eliminated
