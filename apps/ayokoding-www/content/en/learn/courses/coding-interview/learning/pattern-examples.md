---
title: "Pattern examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 20
---

Examples 26–50 cover the common algorithm families. The runnable reference implementations in [`code/`](./code/) prioritise a clear invariant and deterministic tests over clever syntax.

### Example 26 · memoized Fibonacci

_ex-26 · co-13_
**Context.** Compare recursive recomputation with a cache keyed by `n`. **Key takeaway.** Memoize a stable subproblem answer once. **Why it matters.** It makes overlapping subproblems visible before larger DP tables.

### Example 27 · climbing stairs table

_ex-27 · co-13_
**Context.** Define `ways[i]` before filling it from prior states. **Key takeaway.** State meaning precedes recurrence. **Why it matters.** Most DP bugs are ambiguous state, not bad arithmetic.

### Example 28 · minimum coin change

_ex-28 · co-13, co-18_
**Context.** Fill a table with an unreachable sentinel then relax each coin. **Key takeaway.** Unreachable is a legitimate output state. **Why it matters.** It prevents a fabricated answer for impossible amounts.

### Example 29 · longest common subsequence

_ex-29 · co-13_
**Context.** Use a two-dimensional prefix table. **Key takeaway.** Match and mismatch transitions express the subproblem relation. **Why it matters.** It trains explaining table coordinates aloud.

### Example 30 · interval scheduling

_ex-30 · co-14_
**Context.** Sort intervals by finish time and accept compatible candidates. **Key takeaway.** Earliest finish leaves maximal remaining room. **Why it matters.** It is a greedy choice with a defensible exchange argument.

### Example 31 · greedy-versus-DP contrast

_ex-31 · co-14, co-13_
**Context.** Use coin denominations where largest-first fails. **Key takeaway.** A familiar rule needs a problem-specific proof. **Why it matters.** Naming a counterexample is stronger than calling an approach “intuitive.”

### Example 32 · top-k elements

_ex-32 · co-15_
**Context.** Maintain a min-heap of the best `k` values. **Key takeaway.** The root is the current eviction threshold. **Why it matters.** It makes O(n log k) preferable when `k` is small.

### Example 33 · merge k sorted lists

_ex-33 · co-15_
**Context.** Heap one head from each list, then replenish from the selected list. **Key takeaway.** The heap holds the frontier, not every item. **Why it matters.** It separates input size from active competition.

### Example 34 · running median

_ex-34 · co-15_
**Context.** Balance a max-heap lower half against a min-heap upper half. **Key takeaway.** Heap sizes differ by at most one. **Why it matters.** A simple invariant explains a streaming statistic.

### Example 35 · next greater element

_ex-35 · co-16_
**Context.** Pop smaller unresolved values when a larger value arrives. **Key takeaway.** A pop resolves an answer permanently. **Why it matters.** Each value moves through the stack once, yielding linear time.

### Example 36 · daily temperatures

_ex-36 · co-16_
**Context.** Store unresolved indices rather than temperatures. **Key takeaway.** The distance is computed at resolution time. **Why it matters.** It highlights what information the stack must retain.

### Example 37 · union-find cycle detection

_ex-37 · co-17_
**Context.** Before adding an undirected edge, compare its two representatives. **Key takeaway.** Equal roots mean the edge closes a cycle. **Why it matters.** It replaces a repeated traversal with near-constant connectivity checks.

### Example 38 · recover from stuck

_ex-38 · co-23_
**Context.** A stalled graph solution first states a brute-force reachability check, then asks whether weights are non-negative. **Key takeaway.** A focused question changes the search space. **Why it matters.** Recovery keeps the round scoreable.

### Example 39 · handle a streaming follow-up

_ex-39 · co-24_
**Context.** Extend batch top-k to accept one item at a time. **Key takeaway.** The heap invariant survives the delivery-mode change. **Why it matters.** Follow-ups test assumptions, not just the first answer.

### Example 40 · binary search on answer

_ex-40 · co-09, co-13_
**Context.** Find minimum ship capacity using a monotonic feasibility predicate. **Key takeaway.** Search answers only after proving monotonicity. **Why it matters.** It prevents binary search from becoming a cargo-cult move.

### Example 41 · weighted shortest path

_ex-41 · co-11, co-15_
**Context.** Run heap-backed Dijkstra on non-negative edges. **Key takeaway.** Finalising the cheapest frontier distance is valid only under that weight assumption. **Why it matters.** It makes the algorithm’s limit explicit.

### Example 42 · edit distance

_ex-42 · co-13_
**Context.** Define edits for two prefixes and fill the table. **Key takeaway.** Insert, delete, and substitute are alternative transitions. **Why it matters.** It practises narrating a multidimensional state.

### Example 43 · 0/1 knapsack

_ex-43 · co-13, co-20_
**Context.** Compare excluding and including each item at a capacity. **Key takeaway.** Reverse iterate a one-dimensional table when an item may be used once. **Why it matters.** It ties implementation direction to the modelling constraint.

### Example 44 · n-queens

_ex-44 · co-12_
**Context.** Place one queen per row and prune attacked columns and diagonals. **Key takeaway.** Rejecting an invalid partial candidate is the value of backtracking. **Why it matters.** It distinguishes pruning from blindly generating all arrangements.

### Example 45 · minimum covering window

_ex-45 · co-08, co-10_
**Context.** Expand to satisfy target counts, then shrink while still valid. **Key takeaway.** Validity and optimality are separate conditions. **Why it matters.** It avoids shrinking past a required character.

### Example 46 · trie prefix search

_ex-46 · co-06, co-10_
**Context.** Store characters as edges and mark terminal words. **Key takeaway.** Prefix traversal cost depends on key length. **Why it matters.** It shows when a hash map alone cannot answer a prefix question.

### Example 47 · account merge

_ex-47 · co-17_
**Context.** Union records sharing an email, then group by representative. **Key takeaway.** Connectivity models shared identity transitively. **Why it matters.** It avoids pairwise group reconciliation.

### Example 48 · sliding maximum with deque

_ex-48 · co-16, co-08_
**Context.** Keep candidate indices decreasing by value and evict expired ones. **Key takeaway.** The front is the current maximum. **Why it matters.** It demonstrates a monotonic structure beyond a stack.

### Example 49 · full solve transcript

_ex-49 · co-01, co-02, co-03, co-04, co-19, co-20, co-24_
**Context.** Record clarify, trace, plan, code, dry run, complexity, and a follow-up for one prompt. **Key takeaway.** The sequence is a reusable performance routine. **Why it matters.** It is the most direct rehearsal of what the round scores.

### Example 50 · optimise under time pressure

_ex-50 · co-05, co-22_
**Context.** Ship a tested baseline, then decide whether remaining time justifies optimisation. **Key takeaway.** Correctness earns the right to improve. **Why it matters.** It prevents an unfinished optimal attempt from replacing a working answer.
