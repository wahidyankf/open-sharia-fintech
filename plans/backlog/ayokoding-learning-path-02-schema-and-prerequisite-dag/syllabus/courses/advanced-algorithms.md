# Advanced Algorithms (By Example, Python)

**Course ID**: `advanced-algorithms` · **Format**: By Example · **Language**: Python.

**Short summary**: Graphs, dynamic programming, advanced techniques

**Scope note**: the deep algorithms pass — rigorous complexity, advanced trees and graphs, algorithmic
paradigms (D&C, greedy, DP, backtracking), and the problem-solving patterns for interviews and real work.
The everyday basics are the prerequisite
[`07-data-structures-and-algorithms-essentials`](./data-structures-and-algorithms-essentials.md); this
topic is where they become a toolkit.

## Why this exists · the big idea

- **The problem before the solution**: some problems look intractable until you know the paradigm that
  cracks them — brute force silently explodes from milliseconds to millennia as the input grows.
- **Keep-this-if-you-forget-everything**: most hard problems reduce to a known shape — divide, be greedy,
  memoize, or backtrack — and recognizing which shape you're holding is the actual skill.
- **Big ideas touched**: `abstraction-and-its-cost` — every paradigm is a resource trade (DP buys time
  with memory; greedy buys speed by giving up a guarantee; the analysis is deciding which trade is worth it).

## Prerequisites

- **Prior topics**: [topic 7 Data Structures & Algorithms Essentials](./data-structures-and-algorithms-essentials.md)
  (arrays, hashmaps, trees, Big-O, recursion) and [topic 4 Just Enough Python](./just-enough-python.md);
  [topic 19 Computer Science Foundations](./computer-science-foundations.md) sharpens the complexity
  reasoning.
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x** (`heapq`, `collections`, `functools`,
  `itertools` from the stdlib); `pytest` to check algorithm correctness on edge cases.
- **Assumed knowledge**: recursion, Big-O notation, and the basic data structures from topic 07; reading a
  simple recurrence.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: `heapq` and `functools.cache` (added 3.9, a simplified `lru_cache(maxsize=None)`)
  are current unchanged stdlib APIs. The Master-theorem statement (comparing `f(n)` against `n^(log_b a)`)
  is a stable unchanged mathematical result; complexity facts stable. (docs.python.org / CLRS canon)

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

This topic **extends** the essentials in [topic 07](./data-structures-and-algorithms-essentials.md) into
rigor and paradigm mastery — where topic 07 introduced BFS/DFS, a basic Dijkstra, tries, and two-pointer as
tools, here they gain complexity proofs, colors/timestamps, negative-cycle handling, and balanced/segment
structures. The concepts do not re-teach the basics; they deepen them.

- **co-01 · asymptotic-notation-theta-omega** — Θ is a tight bound, Ω a lower bound, O an upper bound; naming which one you are asserting.
- **co-02 · amortized-analysis** — the average cost per operation across a sequence (aggregate, accounting, and potential methods).
- **co-03 · recurrence-relations** — expressing a recursive algorithm's running time as a recurrence to be solved.
- **co-04 · master-theorem** — solving divide-and-conquer recurrences by comparing `f(n)` against `n^(log_b a)`.
- **co-05 · space-time-tradeoff** — spending memory to buy time (and the reverse) as a deliberate engineering choice.
- **co-06 · divide-and-conquer** — split a problem, solve the subproblems, and combine their results.
- **co-07 · merge-sort-invariants** — a stable O(n log n) sort whose merge step maintains an explicit ordering invariant.
- **co-08 · quicksort-partitioning** — in-place partitioning around a pivot; pivot choice separates average from worst case.
- **co-09 · heapsort-and-binary-heaps** — the heap property, sift-up/sift-down, and an in-place O(n log n) heapsort.
- **co-10 · non-comparison-sorts** — counting, radix, and bucket sort beating the comparison-sort `n log n` lower bound.
- **co-11 · sort-stability** — preserving the input order of equal-key records through a sort.
- **co-12 · balanced-bst** — AVL and red-black trees keeping height O(log n) via rotations and invariants.
- **co-13 · tries** — prefix trees giving O(key-length) lookup and prefix queries over string keys.
- **co-14 · fenwick-tree** — a binary indexed tree for prefix-sum plus point-update in O(log n).
- **co-15 · segment-tree** — a tree for range queries and (lazy) range updates in O(log n).
- **co-16 · union-find** — a disjoint-set structure with union-by-rank and path compression for near-constant queries.
- **co-17 · graph-traversal-deep** — BFS/DFS with discovery/finish timestamps and vertex colors, not just a visited set.
- **co-18 · topological-sort** — a linear order of a DAG (Kahn's algorithm or DFS) with cycle detection.
- **co-19 · dijkstra-shortest-path** — single-source shortest paths on non-negative weights using a heap.
- **co-20 · bellman-ford** — shortest paths that tolerate negative edges and detect negative cycles.
- **co-21 · minimum-spanning-tree** — Kruskal (union-find) and Prim (heap) building a minimum-weight spanning tree.
- **co-22 · greedy-paradigm** — making locally optimal choices, valid only when the greedy-choice property holds.
- **co-23 · dynamic-programming-1d** — memoization or tabulation over a single dimension of overlapping subproblems.
- **co-24 · dynamic-programming-2d** — two-dimensional DP tables (edit distance, LCS, knapsack, grid paths).
- **co-25 · backtracking** — systematic search with pruning (N-queens, subsets, Sudoku).
- **co-26 · two-pointers-and-sliding-window** — linear-scan array/string patterns replacing nested loops.
- **co-27 · binary-search-on-answer** — binary-searching a monotonic predicate over a value space, not just an array.
- **co-28 · np-hardness-intuition** — recognizing intractable problems, reductions, and settling for approximation.

## Worked examples

Colocated under `advanced-algorithms/learning/code/`; each runnable with edge-case tests (DD-20/DD-30).
Contiguous `ex-01..ex-80`. Every example cites the `co-NN` it exercises; every concept above is exercised
by ≥1 example.

### Beginner

- **ex-01 · big-o-empirical-timing** — time a linear vs quadratic routine over growing `n` — verify the ratio tracks the predicted growth curve. (co-01)
- **ex-02 · theta-vs-o-classification** — classify a handful of functions into Θ/O/Ω buckets — verify each assertion against a doubling test. (co-01)
- **ex-03 · recurrence-for-merge-sort** — write the `T(n) = 2T(n/2) + n` recurrence and unroll it — verify the closed form is `n log n`. (co-03)
- **ex-04 · master-theorem-cases** — apply the Master theorem to three recurrences (one per case) — verify each stated bound. (co-04, co-03)
- **ex-05 · merge-sort-implement** — implement top-down merge sort — verify it sorts and matches `sorted()` on random inputs. (co-06, co-07)
- **ex-06 · merge-invariant-check** — assert the merge step's "output stays sorted" invariant with an inline check — verify it holds every merge. (co-07)
- **ex-07 · quicksort-lomuto** — implement quicksort with Lomuto partition — verify correctness on random + sorted inputs. (co-08)
- **ex-08 · quicksort-worst-case** — feed sorted input to a naive first-pivot quicksort — verify the O(n²) comparison blow-up empirically. (co-08, co-01)
- **ex-09 · heap-push-pop** — build a min-heap with `heapq`, push/pop — verify smallest always emerges first. (co-09)
- **ex-10 · heapsort-in-place** — implement in-place heapsort via sift-down — verify sorted output and O(1) extra space. (co-09)
- **ex-11 · counting-sort** — sort small-range integers with counting sort — verify O(n+k) and correct order. (co-10)
- **ex-12 · radix-sort** — LSD radix-sort fixed-width integers — verify against `sorted()`. (co-10)
- **ex-13 · stable-vs-unstable** — sort `(key, seq)` pairs stably vs unstably — verify stability preserves input order of equal keys. (co-11)
- **ex-14 · bst-insert-search** — implement an unbalanced BST insert/search — verify in-order traversal is sorted. (co-12)
- **ex-15 · bst-degenerates** — insert sorted keys into the plain BST — verify it degenerates to a O(n) chain. (co-12, co-01)
- **ex-16 · trie-insert-lookup** — build a trie, insert/lookup words — verify hit/miss and O(key-length) cost. (co-13)
- **ex-17 · trie-prefix-count** — count words sharing a prefix via the trie — verify counts on a small dictionary. (co-13)
- **ex-18 · adjacency-list-build** — build an adjacency-list graph from an edge list — verify neighbor sets. (co-17)
- **ex-19 · bfs-shortest-unweighted** — BFS for shortest hop-count on an unweighted graph — verify distances on a hand example. (co-17)
- **ex-20 · dfs-recursive** — recursive DFS collecting visit order — verify it reaches every reachable node. (co-17)
- **ex-21 · dfs-discovery-finish-times** — DFS stamping discovery/finish times with colors — verify parenthesis nesting of intervals. (co-17)
- **ex-22 · union-find-basic** — implement union/find without optimizations — verify connectivity queries. (co-16)
- **ex-23 · two-pointer-pair-sum** — find a pair summing to target in a sorted array with two pointers — verify O(n). (co-26)
- **ex-24 · sliding-window-max-sum** — max sum of a fixed-size window — verify against brute force. (co-26)

### Intermediate

- **ex-25 · amortized-dynamic-array** — grow a dynamic array by doubling, count total copies — verify amortized O(1) append. (co-02)
- **ex-26 · amortized-accounting-method** — assign credits to array appends (accounting method) — verify credits never go negative. (co-02)
- **ex-27 · quicksort-random-pivot** — randomized-pivot quicksort — verify worst-case sorted input no longer degrades. (co-08)
- **ex-28 · quickselect-kth** — quickselect for the k-th smallest — verify against `sorted()[k]` on random inputs. (co-08)
- **ex-29 · closest-pair-divide-conquer** — closest pair of points by divide-and-conquer — verify against brute force. (co-06)
- **ex-30 · fenwick-prefix-sum** — Fenwick tree for prefix sums + point update — verify against a running array. (co-14)
- **ex-31 · segment-tree-range-min** — segment tree for range-min queries — verify against brute-force slices. (co-15)
- **ex-32 · segment-tree-range-update** — segment tree with lazy range-add — verify point reads after range updates. (co-15)
- **ex-33 · union-find-optimized** — union-by-rank + path compression — verify near-constant amortized queries at scale. (co-16, co-02)
- **ex-34 · connected-components** — count components via union-find — verify on a graph with known components. (co-16)
- **ex-35 · topological-sort-kahn** — Kahn's in-degree topological sort — verify a valid order on a DAG. (co-18)
- **ex-36 · topological-sort-dfs** — DFS finish-time topological sort — verify it equals a valid order. (co-18, co-17)
- **ex-37 · cycle-detection-directed** — detect a cycle via DFS colors — verify a cyclic graph is rejected. (co-18, co-17)
- **ex-38 · dijkstra-heap** — Dijkstra with a `heapq` priority queue — verify shortest paths on a weighted graph. (co-19)
- **ex-39 · dijkstra-unreachable** — Dijkstra with an unreachable node — verify it reports infinity, not a crash. (co-19)
- **ex-40 · bellman-ford-negative-edges** — Bellman-Ford on a graph with negative edges — verify correct distances Dijkstra would miss. (co-20)
- **ex-41 · bellman-ford-negative-cycle** — detect a negative cycle on the Nth relaxation — verify it flags the cycle. (co-20)
- **ex-42 · mst-kruskal** — Kruskal's MST via union-find — verify total weight matches the known minimum. (co-21, co-16)
- **ex-43 · mst-prim** — Prim's MST via a heap — verify same total weight as Kruskal. (co-21, co-19)
- **ex-44 · greedy-interval-scheduling** — max non-overlapping intervals by earliest-finish greedy — verify optimality on a hand example. (co-22)
- **ex-45 · greedy-coin-change-fails** — greedy coin change on a non-canonical coin set — verify it produces a suboptimal answer. (co-22, co-23)
- **ex-46 · dp-fib-memo-vs-tab** — Fibonacci by memoization and by tabulation — verify equal results and both O(n). (co-23)
- **ex-47 · dp-climbing-stairs** — count stair-climbing ways (1/2 steps) with DP — verify against a recurrence. (co-23)
- **ex-48 · dp-coin-change-min** — minimum coins via DP where greedy failed — verify it beats ex-45's answer. (co-23)
- **ex-49 · dp-edit-distance** — Levenshtein edit distance, 2D table — verify against known string pairs. (co-24)
- **ex-50 · dp-lcs** — longest common subsequence, 2D table — verify length + reconstruction. (co-24)
- **ex-51 · dp-knapsack-01** — 0/1 knapsack, 2D table — verify optimal value on a small instance. (co-24)
- **ex-52 · binary-search-boundary** — binary search for leftmost/rightmost match — verify boundaries incl. absent target. (co-27)

### Advanced

- **ex-53 · backtracking-n-queens** — place N queens by backtracking — verify solution counts for N=4..8. (co-25)
- **ex-54 · backtracking-subsets** — enumerate all subsets by backtracking — verify count is 2ⁿ and no dups. (co-25)
- **ex-55 · backtracking-permutations** — enumerate permutations by backtracking — verify count is n! and all distinct. (co-25)
- **ex-56 · backtracking-word-search** — grid word-search with backtracking — verify found/not-found cases. (co-25)
- **ex-57 · backtracking-sudoku** — solve Sudoku by constraint backtracking — verify a solved board is valid. (co-25)
- **ex-58 · greedy-vs-dp-contrast** — same problem solved greedily and with DP — verify where greedy diverges from optimal. (co-22, co-23)
- **ex-59 · dp-2d-grid-paths** — count/least-cost paths through a grid, 2D DP — verify against enumeration on small grids. (co-24)
- **ex-60 · dp-longest-increasing-subsequence** — LIS via O(n²) DP and O(n log n) patience — verify equal lengths. (co-23, co-27)
- **ex-61 · dp-matrix-chain** — matrix-chain multiplication order, 2D DP — verify minimal cost on a known chain. (co-24)
- **ex-62 · dp-space-optimized** — roll a 2D DP down to O(width) rows — verify same result as the full table. (co-24, co-05)
- **ex-63 · dijkstra-vs-bellman-tradeoff** — benchmark Dijkstra vs Bellman-Ford on the same graph — verify the speed/generality trade. (co-19, co-20)
- **ex-64 · a-star-heuristic** — A\* with an admissible heuristic on a grid — verify it matches Dijkstra's cost but expands fewer nodes. (co-19)
- **ex-65 · topo-sort-critical-path** — longest path (critical path) over a DAG via DP on topo order — verify on a hand-computed schedule. (co-18, co-24)
- **ex-66 · strongly-connected-components** — Tarjan/Kosaraju SCCs — verify components on a known digraph. (co-17, co-18)
- **ex-67 · segment-tree-vs-fenwick** — same prefix-sum workload on both structures — verify equal answers, contrast code + cost. (co-14, co-15)
- **ex-68 · avl-rotations** — AVL insert with rotations — verify height stays O(log n) on sorted inserts. (co-12)
- **ex-69 · red-black-invariants** — assert red-black invariants after inserts — verify no red-red and equal black-heights. (co-12)
- **ex-70 · two-pointer-three-sum** — 3-sum via sort + two pointers — verify unique triplets against brute force. (co-26)
- **ex-71 · sliding-window-longest-substring** — longest substring without repeats, variable window — verify against brute force. (co-26)
- **ex-72 · sliding-window-min-window** — minimum window substring covering a target set — verify on known cases. (co-26)
- **ex-73 · binary-search-on-answer** — binary-search a monotonic feasibility predicate (e.g. min capacity to ship in D days) — verify the boundary. (co-27)
- **ex-74 · quickselect-median-of-medians** — deterministic O(n) selection — verify worst-case linearity vs random pivot. (co-08, co-01)
- **ex-75 · np-hard-tsp-brute-vs-heuristic** — brute-force TSP vs a nearest-neighbor heuristic — verify the heuristic is fast but not optimal. (co-28)
- **ex-76 · np-reduction-sketch** — reduce subset-sum to a known NP-hard problem in code comments + a checker — verify the mapping preserves yes-instances. (co-28)
- **ex-77 · amortized-potential-method** — analyze a multi-pop stack with the potential method — verify amortized O(1). (co-02)
- **ex-78 · complexity-stated-and-tested** — annotate three routines with their complexity and back each with a doubling test — verify claims hold. (co-01, co-05)
- **ex-79 · benchmark-paradigm-shootout** — same problem by brute force / greedy / DP, timed — verify the paradigm crossover as `n` grows. (co-22, co-23, co-05)
- **ex-80 · capstone-preview-scheduler** — thread topo-sort + critical-path DP + Dijkstra into a mini task scheduler — verify end-to-end on a sample DAG. (co-18, co-24, co-19)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a small "algorithm workbench" that solves one substantial problem end to end — e.g. a
  task scheduler over a dependency DAG that computes a topological order, a critical path via DP, and a
  shortest-cost path via Dijkstra — with complexity stated and verified against edge-case tests.
- **Concepts exercised**: [ ] graph representation + BFS/DFS (co-17) [ ] topological sort with cycle
  detection (co-18) [ ] a DP formulation — critical path / longest path (co-24) [ ] Dijkstra with a heap
  (co-19) [ ] stated + justified complexity (co-01) [ ] edge-case tests (empty, cyclic, disconnected).
- **Ordered steps**:
  1. `.../learning/capstone/code/graph.py` — the DAG model + topological sort with cycle detection. Verify
     a cyclic input is rejected and a valid DAG yields a correct order.
  2. `critical_path.py` — DP longest-path/critical-path over the DAG. Verify it matches a hand-computed
     small example.
  3. `shortest.py` — Dijkstra over a weighted variant with `heapq`. Verify it matches a known shortest path
     and handles an unreachable node.
  4. State each routine's time/space complexity; add a `pytest` suite of edge cases. Verify all pass.
- **Acceptance criteria**: every algorithm is correct on the edge-case suite; complexities are stated and
  defended; the workbench runs end to end on a sample project graph.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Introduction to Algorithms** — Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein (2022, 4th ed.). The standard reference ("CLRS") for algorithms, data structures, and complexity analysis.
- **Algorithm Design** — Jon Kleinberg & Éva Tardos (2005). Widely adopted text teaching algorithmic design paradigms — greedy, divide-and-conquer, DP, network flow — through motivating problems.
- **The Algorithm Design Manual** — Steven S. Skiena (1997; 3rd ed. 2020). Practitioner-oriented reference pairing "war stories" with a catalog of algorithmic techniques and data structures.
- **Approximation Algorithms** — Vijay V. Vazirani (2001). The standard graduate reference on approximation algorithms and hardness of approximation for NP-hard problems.

**Papers & articles**

- **A Note on Two Problems in Connexion with Graphs** — Edsger W. Dijkstra (1959). Original paper introducing Dijkstra's shortest-path algorithm, still taught in every graph algorithms course.

## In which paths

- `interview-ready/software-engineer` — Phase 1 · Interview preparation (through senior).
- `immediately-effective/software-engineer` — Deepening band · CS fundamentals, DS&A & algorithms — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 2 · Data structures, algorithms & object-oriented design.

> _Content originated in the now-closed FS-SE plan (topic 25); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
