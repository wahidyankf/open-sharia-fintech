---
title: "Multi-File Structure"
description: Shows the five-document plan folder layout and defines the purpose of README.md, brd.md, and prd.md.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when scaffolding a multi-file plan folder or clarifying what belongs in README.md, brd.md, or prd.md.
---

# Multi-File Structure

```
2025-12-01__feature-name/
├── README.md                # Plan overview and navigation
├── brd.md                   # Business Requirements Document
├── prd.md                   # Product Requirements Document
├── tech-docs.md             # Technical documentation and architecture
├── delivery.md              # Step-by-step delivery checklist
├── learnings.md             # (transient) running log of generalizable learnings
└── evidence/                # (optional) committed testing evidence — screenshots, curl responses
    ├── phase-1-homepage-en-1280px.png
    └── phase-2-api-health.txt
```

**File purposes**:

- **README.md**: High-level overview and navigation — Context, Scope (with affected subrepos / apps named explicitly), Approach Summary, and links to the other four files. First file a reader opens; first file checkers parse for scope.
- **brd.md** — **Business Requirements Document**: business goal and rationale ("why are we doing this"), business impact, affected roles, business-level success metrics, business-scope Non-Goals, business risks and mitigations. Content-placement container, not a sign-off artifact — code review is the only approval gate in this repo.
- **prd.md** — **Product Requirements Document**: product overview, personas, user stories (`As a … I want … So that …`), acceptance criteria in Gherkin, product scope (in-scope + out-of-scope features), product-level risks. **For UI-bearing plans** (those that add or change user-facing screens or components under `apps/` or `libs/`), `prd.md` additionally contains the complete **UI-design-funnel record**: the inline low-fidelity ASCII wireframes (Diverge stage, ≥ 2 named alternatives, at least mobile + desktop where they differ), the high-fidelity mockup embeds via `![]()` image links referencing the plan's `assets/` folder (Narrow stage finalists), the named selection (Select stage), and the rationale table (Justify stage). **For learning-bearing plans** (those whose delivery checklist authors or restructures course, tutorial, or curriculum content), `tech-docs.md` additionally requires a `## Corpus Disposition` declaration and the plan's `syllabus/` folder record, per the [Learning-Plan `syllabus/` Folder Convention](../learning-plan-syllabus.md). See [UI Mockups in Plan Docs — Placement](../../formatting/diagrams/ui-mockups-placement-hard-rule-requirements.md#placement--the-ui-lives-in-prdmd-hard-rule-requirements-and-enforcement) for the full placement rule.

See [Multi-File Structure — Additional File Purposes](./multi-file-structure-additional-file-purposes.md) for `tech-docs.md`, `delivery.md`, `learnings.md`, and `evidence/`.
