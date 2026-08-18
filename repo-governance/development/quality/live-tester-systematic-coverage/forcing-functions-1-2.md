---
title: "The Six Forcing-Functions (1-2)"
description: "Forcing-functions 1-2: shared-control matrix, per-control round-trip."
category: explanation
subcategory: development
tags:
  - testing
  - live-testing
  - usability
  - ux
  - quality
  - systematic
created: 2026-06-22
when_to_use: "Use when applying the shared-control or round-trip forcing-function."
---

# The Six Forcing-Functions (1-2)

## 1. Shared-Control x Surface Matrix

**Obligation**: Identify every control that appears on more than one tab, view, or surface.
For each such control, exercise it on every surface it appears on and assert that the behavior
is identical across surfaces. A control that triggers a change on one surface but no-ops on
another is a consistency defect (Nielsen Heuristic 4: Consistency and Standards; WCAG 2.2 SC
3.2.4 Consistent Identification, technique G197).

**How to apply**: Build a matrix before testing begins:

| Control        | Tab A | Tab B | Tab C | Consistent? |
| -------------- | ----- | ----- | ----- | ----------- |
| City filter    | check | check | check | YES / NO    |
| Currency input | check | check | --    | YES / NO    |

Fill in the matrix by exercising each cell. A blank or "NO" cell is a finding.

**Ground**: Nielsen Heuristic 4 (Consistency and Standards); WCAG 2.2 SC 3.2.4 Consistent
Identification (technique G197).

## 2. Per-Control URL / State Round-Trip

**Obligation**: For every interactive control (filter, input, toggle, selector, tab),
execute the full round-trip: change the control value, verify the URL updates, reload the
page (or open a new tab with the same URL), and verify the control restores to its changed
state. A control whose value does not survive a reload is a statelessness defect
(MDN History API state contract; Nielsen Heuristics 1: Visibility of System Status and
3: User Control and Freedom).

**How to apply**: For each control:

1. Record the URL before the change.
2. Change the control.
3. Assert the URL has updated to reflect the new value.
4. Reload.
5. Assert the control shows the value it held before reload.

If any step fails, record a finding with the control name, the expected URL parameter, and
the observed behavior.

**Ground**: MDN History API state contract; Nielsen Heuristics 1 and 3.
