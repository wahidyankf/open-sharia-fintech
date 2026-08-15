---
title: "Capstone overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Goal

Run a self-administered timed round of five original problems spanning at least four patterns. For every problem, record clarification, a concrete example, plan plus Big-O, implementation, a dry run, and a score. This capstone integrates the course; it does not introduce a sixth topic.

## Concepts exercised

- [x] clarify and trace a concrete example (co-02, co-03)
- [x] state plan and complexity before code (co-04)
- [x] select at least four patterns (co-06 through co-17)
- [x] enumerate edge cases and dry run (co-18, co-19)
- [x] narrate and time-box the work (co-21, co-22)
- [x] articulate the final trade-off (co-20)

## Problems and timer budgets

| Problem           | Target pattern | Budget | Required visible evidence                           |
| ----------------- | -------------- | -----: | --------------------------------------------------- |
| Pair indices      | hash lookup    | 18 min | clarification, complement invariant, duplicate test |
| Compact window    | sliding window | 22 min | trace, validity invariant, shrink explanation       |
| Islands           | BFS or DFS     | 22 min | visited contract, component count, boundary test    |
| Meeting selection | greedy         | 18 min | sorting rule and exchange argument                  |
| Streaming top-k   | heap           | 20 min | heap-size invariant and memory trade-off            |

The original reference solutions live in `learning/capstone/code/round.py`; execute their assertions with `pytest -q learning/capstone/code` from this course directory.

## Procedure

1. Work each prompt under its timer without autocomplete.
2. Before implementation, write the contract, trace, chosen pattern, invariant, and Big-O.
3. Execute the supplied tests only after your own dry run; compare a disagreement against the invariant, not against a memorised answer.
4. Record a score for correctness, communication, complexity, and edge cases using the score sheet below.
5. Rework the weakest score with a different prompt, retaining the same six-step interview loop.

## Score sheet

| Problem           | Correctness | Communication | Complexity | Edge cases | Evidence and next action                   |
| ----------------- | ----------- | ------------- | ---------- | ---------- | ------------------------------------------ |
| Pair indices      | _rate 1–4_  | _rate 1–4_    | _rate 1–4_ | _rate 1–4_ | cite trace or failed test; name one repair |
| Compact window    | _rate 1–4_  | _rate 1–4_    | _rate 1–4_ | _rate 1–4_ | cite trace or failed test; name one repair |
| Islands           | _rate 1–4_  | _rate 1–4_    | _rate 1–4_ | _rate 1–4_ | cite trace or failed test; name one repair |
| Meeting selection | _rate 1–4_  | _rate 1–4_    | _rate 1–4_ | _rate 1–4_ | cite trace or failed test; name one repair |
| Streaming top-k   | _rate 1–4_  | _rate 1–4_    | _rate 1–4_ | _rate 1–4_ | cite trace or failed test; name one repair |

A rating is complete only with a justification. A four is not “it felt good”; it identifies the stated invariant, representative trace, and edge test that support it.
