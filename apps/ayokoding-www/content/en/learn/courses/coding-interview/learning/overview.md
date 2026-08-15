---
title: "Learning overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

This is a technique refresher. It assumes the underlying data structures and algorithms are already familiar, then makes the choices and verification visible enough for an interviewer to follow and assess.

## Concepts

### co-01 · What the round scores

A round scores problem-solving process, communication, correctness, and coding fluency, not merely whether a final submission passes. **Verify**: a self-score contains a separate observation for each of those four signals.

### co-02 · Clarify before coding

Restate the task and ask about input range, mutability, duplicates, invalid input, and the desired output before implementation. **Verify**: the written plan names constraints rather than silently assuming them.

### co-03 · Work a concrete example

Trace one small representative input before code; it often reveals the state, invariant, and awkward edge case. **Verify**: each pointer, queue, or table change can be explained on the trace.

### co-04 · State approach and complexity first

Say the intended method and time/space cost before coding, allowing early correction. **Verify**: the complexity statement matches the loops and retained state.

### co-05 · Brute force, then optimize

Anchor correctness with a baseline, then replace repeated work deliberately. **Verify**: the optimisation preserves the baseline's result on the same inputs.

### co-06 · Pattern recognition

Problem families recur: sequence bounds, contiguous windows, monotonic predicates, traversals, enumeration, and state recurrences. **Verify**: the named pattern has an invariant that fits the prompt.

### co-07 · Two pointers

Coordinated indices solve pair, partition, and reverse problems with one traversal when their movement rule is justified. **Verify**: each pointer movement makes the discarded region impossible to need again.

### co-08 · Sliding window

Maintain a contiguous range and update only what enters or leaves it. **Verify**: the window invariant holds after every expand and shrink.

### co-09 · Binary search

Halve a sorted collection or monotonic answer space. **Verify**: the predicate changes only once and the boundary update always shrinks the interval.

### co-10 · Hashing for lookup

Use a map or set to exchange memory for expected constant-time membership, counting, or complement lookup. **Verify**: the lookup is made before state is updated when that ordering matters.

### co-11 · BFS and DFS

Traversal answers reachability, connectivity, and unweighted shortest-path questions; choose breadth for minimum hops and depth for systematic exploration. **Verify**: visited state prevents repeated work.

### co-12 · Backtracking

Choose, explore, and undo to enumerate valid candidates while pruning impossible partial states. **Verify**: every mutation has its matching undo.

### co-13 · Dynamic programming

Overlapping subproblems plus optimal substructure permit a memoized or tabulated recurrence. **Verify**: base cases and state meaning are stated before transitions.

### co-14 · Greedy choice

A local choice needs an exchange argument or a known theorem; a plausible-looking greedy rule is not proof. **Verify**: compare against a counterexample or state why the choice is safe.

### co-15 · Heap and top-k

A heap retains the best `k` items or exposes the current frontier with logarithmic updates. **Verify**: heap size and ordering convention are explicit.

### co-16 · Monotonic stack

Keep candidates ordered so an arriving value resolves exactly the candidates it dominates. **Verify**: each item is pushed and popped at most once.

### co-17 · Union-find

Disjoint-set union maintains dynamic components and detects cycle-forming edges. **Verify**: `find` establishes the representative before `union` compares components.

### co-18 · Edge-case enumeration

Empty input, one element, duplicates, negatives, boundaries, and large values deserve named treatment. **Verify**: each case maps to a test or an intentional contract decision.

### co-19 · Dry-run verification

Walk completed code over the earlier example line by line. **Verify**: the predicted state sequence equals the actual result.

### co-20 · Complexity trade-offs

State final time, space, and what resource the selected approach spends. **Verify**: the explanation includes an alternative and why it was not chosen.

### co-21 · Thinking aloud

Narrate observations, hypotheses, discarded routes, and checks continuously enough to be scoreable. **Verify**: an observer could reconstruct why each substantive line exists.

### co-22 · Time-boxing

Reserve time for clarification, planning, code, and verification; cut an unproductive direction early. **Verify**: the plan includes a recovery threshold.

### co-23 · Recovering when stuck

Simplify, state a baseline, ask a focused question, or request a hint. **Verify**: the recovery produces a next experiment instead of silence.

### co-24 · Handling follow-ups

Scale, streaming, mutation, memory, or new-constraint questions test whether the first solution's assumptions are understood. **Verify**: the response names which invariant or data structure changes.

## Reference sources

- Gayle Laakmann McDowell, _Cracking the Coding Interview_, for practitioner-oriented interview practice.
- Cormen, Leiserson, Rivest, and Stein, _Introduction to Algorithms_, for algorithmic proof and complexity foundations.

These references inform the durable technique. The examples below are original course material and do not reproduce platform or company prompts.
