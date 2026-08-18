---
title: "Granular Checklist Items in delivery.md"
description: States the one-checkbox-one-action rule for delivery.md and shows a bad-versus-good example of checklist granularity.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when writing or reviewing delivery.md checkboxes to check whether an item is too coarse.
---

# Granular Checklist Items in delivery.md

Every checkbox in `delivery.md` must represent exactly one concrete, independently verifiable action. Multi-step work hidden behind a single checkbox defeats the purpose of a checklist: it makes progress invisible and creates ambiguity about what "done" means.

**Rule**: One checkbox = one concrete action. If completing the item requires multiple distinct steps, split it into multiple checkboxes.

**Bad** (too coarse — hides multiple steps):

```markdown
- [ ] Implement coverage merging with all formats and tests
```

**Good** (granular — each item is independently completable):

```markdown
- [ ] Create `internal/testcoverage/merge.go` with format-agnostic merge logic
- [ ] Implement `CoverageMap` type for normalized per-line data
- [ ] Add parsers to return `CoverageMap` from each format
- [ ] Write unit tests for merge logic (same format, cross-format, overlapping)
```

**Test for granularity**: Each checkbox must pass this test — can you verify it is done without completing anything else on the list? If the answer is no, the item is too coarse.
