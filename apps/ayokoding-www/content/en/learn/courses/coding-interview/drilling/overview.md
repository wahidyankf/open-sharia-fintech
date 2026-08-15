---
title: "Drilling overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

1. What must be clarified before coding? Input shape, constraints, output contract, edge cases, and whether mutation is allowed.
2. When is BFS preferable to DFS? When the required answer is minimum hops in an unweighted graph.
3. What makes binary search legitimate? A predicate or ordering whose truth changes monotonically.
4. What is the dry-run question? “What is every important state variable after this line on the concrete example?”

## Calculation practice

1. State the time and extra space for map-based two-sum, sort-and-two-pointer two-sum, fixed-window sum, and top-k with a heap of size `k`.
2. For a length-`n` sequence, calculate the maximum number of pushes and pops in a monotonic-stack pass.
3. Given a 30-minute slot, allocate minute budgets that leave at least four minutes for verification and explain the trade-off.

## Scenario judgment

1. The interviewer says the input is sorted after you propose a map. Decide whether two pointers improves space enough to switch.
2. Your greedy rule sounds plausible but you cannot give an exchange argument. Decide whether to retain it, test counterexamples, or present DP.
3. The expected result for empty input is unclear. Pause and ask rather than choosing a sentinel silently.
4. A follow-up changes batch input to a stream. Identify the invariant that can survive.

## Design exercise

Design a personal round template containing: clarification questions, a trace grid, a one-sentence pattern/invariant, time/space fields, an edge-case checklist, and a final follow-up prompt. Use it on a graph problem and a string problem; note which fields need different wording but keep the same decision sequence.

## Automaticity checklist

- [ ] I restate the contract before reaching for a pattern.
- [ ] I trace a representative input before implementation.
- [ ] I state the approach, invariant, and time/space cost aloud.
- [ ] I can produce a correct baseline when the optimal approach is uncertain.
- [ ] I enumerate boundaries and dry-run the final loop.
- [ ] I narrate a recovery move rather than becoming silent when stuck.
- [ ] I close with complexity, trade-off, tests, and a follow-up.
