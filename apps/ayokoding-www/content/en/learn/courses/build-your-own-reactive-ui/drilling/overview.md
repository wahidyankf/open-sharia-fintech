---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

This active-recall companion uses the fixed progression: recall Q&A, scenario judgment, hands-on
implementation, and an automaticity checklist. Attempt each prompt before opening its answer.

## Recall Q&A

**Q1 (co-01).** What two parts make a UI reactive?

<details><summary>Answer</summary>A function from state to view, plus a mechanism that re-runs the affected work when state changes.</details>

**Q2 (co-06/co-07).** What is the difference between diffing and patching?

<details><summary>Answer</summary>Diffing decides what changed between descriptions; patching performs those chosen host mutations.</details>

**Q3 (co-11).** Why is a stable key not an array index?

<details><summary>Answer</summary>A key represents the item's identity across reorder and insertion; an index represents a position that can change.</details>

**Q4 (co-16).** When does a signal become a dependency of an effect?

<details><summary>Answer</summary>When the effect reads that signal while it is the active tracked computation.</details>

**Q5 (co-22).** Why must hooks be unconditional?

<details><summary>Answer</summary>A minimal hook runtime addresses state by call order, so conditional calls shift later slots.</details>

**Q6 (co-31).** What prevents a diamond graph from publishing a stale intermediate value?

<details><summary>Answer</summary>Batching or a topological scheduler waits until upstream inputs are stable before recomputing shared downstream work.</details>

## Scenario judgment

1. A filtered list reorders while inputs retain the wrong text. Diagnose positional keys and use a durable item id.
2. A counter update re-renders an unrelated chart. Diagnose coarse invalidation; make the chart read only its own signal.
3. A cleanup never runs after navigation. Keep a disposal handle and call it when the component unmounts.
4. A component's second state value changes type after an `if`. Move every hook call above the branch.

## Hands-on implementation

1. Implement `h(type, props, children)` with a discriminated text-or-element `VNode` union.
2. Write a keyed reconciliation function that reuses an unchanged task node after reordering.
3. Implement `signal` and `effect`; prove an unrelated effect does not re-run.
4. Add batch scheduling and write an assertion that a diamond's leaf observes no intermediate value.

## Automaticity checklist

- [ ] I can explain virtual-DOM reconciliation separately from DOM patching.
- [ ] I can choose a stable key and explain why an index is unsafe after reordering.
- [ ] I can trace a signal read into an effect subscription and dispose it safely.
- [ ] I can explain when fine-grained updates avoid whole-tree work.
- [ ] I can identify hook-order and diamond-graph failures from their symptoms.
