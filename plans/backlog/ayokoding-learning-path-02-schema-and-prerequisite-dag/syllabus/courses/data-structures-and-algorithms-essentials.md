# Data Structures and Algorithms Essentials (By Example, Python)

**Course ID**: `data-structures-and-algorithms-essentials` · **Format**: By Example · **Language**: Python.

**Short summary**: Core data structures and algorithms, complexity

**Scope note**: the **usable slice** — the structures and algorithms a working engineer reaches for
daily. Deep paradigms (amortized/Θ/Ω rigor, graph/DP/greedy families) are deferred to
[`25-advanced-algorithms`](./advanced-algorithms.md) (split-and-interleave, DD-11).

## Why this exists · the big idea

- **The problem before the solution**: the same task can run instantly or crawl depending on how you
  store the data — choosing the wrong structure is a bug you feel only at scale.
- **Keep-this-if-you-forget-everything**: pick the structure that makes the _common_ operation cheap; the
  data-structure choice is the real decision, and the algorithm often follows from it.
- **Big ideas touched**: `abstraction-and-its-cost` — every structure trades one operation's cost for
  another (a hash buys O(1) lookup and charges ordering; a list buys order and charges search).

## Prerequisites

- **Prior topics**: [topic 4 Just Enough Python](./just-enough-python.md) (all examples are Python).
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x** with `pytest` installed in a `venv`.
- **Assumed knowledge**: reading/writing basic Python — functions, lists, dicts, loops (from topic 04);
  no prior algorithms background required.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: `heapq`, `collections.deque`, and `bisect` stdlib APIs are current/unchanged in
  Python 3.14; list `.append()` is amortized O(1), dict lookup average-case O(1) (degrades only under
  pathological collisions). (docs.python.org / wiki.python.org TimeComplexity)
- 2026-07-14 — re-verified (independent `web-researcher` confirmation pass): 5 of 6 checked claims hold
  unchanged (`heapq`/`deque`/`bisect` APIs, `sorted()`/`list.sort()` = Timsort, the wiki TimeComplexity
  complexity table, dict insertion-order as a 3.7+ language-spec guarantee, `RecursionError` as a
  `RuntimeError` subclass). Only the Python version pin had drifted: **latest stable patch is now
  3.14.6 (2026-06-10)** — the 3.14 series itself is still current/latest and no cited API changed; 3.14.0
  (2025-10-07) is simply an older patch within the same still-current series. (python.org/downloads,
  docs.python.org)

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to a primary/authoritative source fetched and read in the retroactive
> grounding sweep (2026-07-12, `web-researcher`). Sources: `docs.python.org`, the CPython-endorsed
> [wiki.python.org TimeComplexity](https://wiki.python.org/moin/TimeComplexity) page, and CLRS 4th ed.
> All 22 concepts + sampled worked examples + Read-more citations verified; 2 precision fixes applied.

- **Complexity table (co-02/03/05/06/08/09/12/14)** — [wiki TimeComplexity](https://wiki.python.org/moin/TimeComplexity)
  verbatim: `list.append` amortized O(1), `list.insert(0)`/`pop(0)` O(n), `dict`/`set` get/set/delete +
  `x in s` average O(1), `deque` append/appendleft/pop/popleft all O(1). Python **3.14.x** current
  (series released 2025-10-07 as 3.14.0; latest patch **3.14.6**, 2026-06-10 — re-verified 2026-07-14);
  `heapq`/`deque`/`bisect` unchanged (3.14 only _adds_ `heapify_max` etc., unused here) per
  [What's New 3.14](https://docs.python.org/3/whatsnew/3.14.html).
- **Sorting (co-15/16)** — [sorting howto](https://docs.python.org/3/howto/sorting.html) names the stable
  algorithm "Timsort" (CPython 3.11+ uses a Powersort merge policy but the docs still say Timsort — claim
  tracks the primary source). co-16 corrected: **quicksort is O(n log n) average but O(n²) worst-case**
  (poor pivot), vs merge sort's guaranteed O(n log n) worst-case — per CLRS ch. 7.
- **dict ordering (co-08)** — corrected: Python **3.7+ guarantees insertion-order iteration** as a
  language-spec guarantee (not merely a CPython implementation detail); `dict` isn't key-sorted like a BST.
- **heapq / bisect / RecursionError (co-12/14/18)** — [heapq](https://docs.python.org/3/library/heapq.html)
  ("logarithmic" percolation), [bisect](https://docs.python.org/3/library/bisect.html) (search + insertion
  points; `insort` O(n) overall — not overclaimed), `RecursionError`
  ([exceptions](https://docs.python.org/3/library/exceptions.html), a `RuntimeError` subclass since 3.5).
- **Algorithms (ex-71/72/73/75/78)** — Dijkstra + min-heap (CLRS 24.3), **Kahn's** topological sort
  (Arthur B. Kahn, in-degree+queue), white/gray/black DFS cycle detection (CLRS 22.3), quickselect (Hoare
  1961), dict+doubly-linked-list LRU — all standard, no misattribution.
- **Read more** — CLRS 4th ed. 2022 ([MIT Press](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/));
  Skiena _Algorithm Design Manual_ 3rd ed. 2020 ([Springer](https://link.springer.com/book/10.1007/978-3-030-54256-6));
  Sedgewick & Wayne _Algorithms_ 4th ed. 2011 ([algs4.cs.princeton.edu](https://algs4.cs.princeton.edu/home/)) —
  author/edition/year/URL all confirmed.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (subject topic). Each example below cites the co-NN it exercises. -->

- **co-01 · big-o-notation** — describe an algorithm's growth as its input scales — O(1), O(log n),
  O(n), O(n log n), O(n²) — as the vocabulary for "does this scale?".
- **co-02 · amortized-analysis** — some operations are cheap on average even when an occasional step is
  costly: `list.append` is amortized O(1); `dict`/`set` operations average O(1).
- **co-03 · dynamic-array** — Python's `list` is a growable contiguous array with O(1) index and
  amortized-O(1) append but O(n) insert/delete at the front.
- **co-04 · stack** — a last-in-first-out (LIFO) structure implemented with `list.append`/`list.pop`.
- **co-05 · queue** — a first-in-first-out (FIFO) structure; use `collections.deque` for O(1)
  `popleft` instead of a list's O(n) `pop(0)`.
- **co-06 · deque** — a double-ended queue supporting O(1) push/pop at both ends.
- **co-07 · singly-linked-list** — a node-based sequence (`val` + `next`) supporting O(1) head
  insertion and O(n) traversal, contrasted with the array.
- **co-08 · hash-map** — `dict` gives average-O(1) keyed insert/lookup/delete; unlike a BST it isn't
  key-sorted, though Python 3.7+ guarantees insertion-order iteration (a language-spec guarantee, not
  just a CPython detail).
- **co-09 · hash-set** — `set` gives average-O(1) membership testing and deduplication.
- **co-10 · binary-tree** — a node with up to two children; traversals are preorder, inorder, postorder
  (depth-first) and level-order (breadth-first).
- **co-11 · binary-search-tree** — an ordered binary tree where an inorder traversal yields sorted
  values, giving average-O(log n) insert/search/delete.
- **co-12 · heap-priority-queue** — `heapq` maintains a binary min-heap over a list for O(log n) push
  and pop-min, the basis of a priority queue.
- **co-13 · linear-search** — scan a sequence element by element in O(n); the only option on unsorted
  data.
- **co-14 · binary-search** — halve a sorted range each step for O(log n) lookup; the `bisect` module
  provides it plus sorted-insertion points.
- **co-15 · builtin-sort** — `sorted()` / `list.sort()` are stable O(n log n) Timsort, tunable with
  `key` and `reverse`.
- **co-16 · comparison-sorts** — the classic algorithms — bubble, insertion, selection (O(n²)); merge
  (O(n log n) guaranteed worst-case); quick (O(n log n) average, but O(n²) worst-case with a poor pivot) —
  and how each orders elements.
- **co-17 · recursion** — a function that solves a problem in terms of smaller instances, needing a base
  case and a recursive case, and consuming call-stack frames.
- **co-18 · iterate-vs-recurse** — any recursion can be rewritten iteratively (often with an explicit
  stack) to bound stack depth and avoid `RecursionError`.
- **co-19 · memoization** — cache subproblem results (a `dict` or `functools.lru_cache`) to collapse
  exponential recomputation into linear work.
- **co-20 · two-pointer-and-sliding-window** — coordinate two indices (or a moving window) over a
  sequence to solve pair/subarray problems in O(n).
- **co-21 · graph-adjacency** — represent a graph as a dict-of-lists adjacency map and traverse it with
  BFS (a queue) or DFS (recursion/stack).
- **co-22 · static-type-hints** — annotate parameters and returns (`list[int]`, `dict[str, int]`,
  `Optional[Node]`) so every example reads as typed, self-documenting Python.

## Worked examples

All colocated under `data-structures-and-algorithms-essentials/learning/code/`; each is a runnable
Python module with static type hints, executed with `python3 <file>` and self-checked with `assert`
statements (DD-20/DD-30). Each cites the `co-NN` it exercises. Contiguous `ex-01..ex-82`.

### Beginner

- **ex-01 · list-append-index** — build a `list[int]`, append and index into it — verify the printed
  length and element match expected. (co-03, co-02)
- **ex-02 · list-slicing** — slice a `list[int]` — verify the sub-list equals the expected slice via
  `assert`. (co-03)
- **ex-03 · list-reverse-inplace** — reverse a `list[int]` with `.reverse()` — verify it equals the
  expected order via `assert`. (co-03)
- **ex-04 · list-reverse-slice** — reverse via `lst[::-1]` — verify a new reversed list is returned and
  the original is unchanged via `assert`. (co-03)
- **ex-05 · stack-push-pop** — use a `list` as a stack with `append`/`pop` — verify LIFO order via
  `assert`. (co-04)
- **ex-06 · balanced-parentheses** — check bracket balance with a stack — verify `"(())"` is True and
  `"(()"` is False via `assert`. (co-04)
- **ex-07 · queue-with-deque** — enqueue/dequeue with `deque.append`/`popleft` — verify FIFO order via
  `assert`. (co-05, co-06)
- **ex-08 · deque-both-ends** — `appendleft`/`append`/`pop`/`popleft` on a `deque[int]` — verify the
  resulting order via `assert`. (co-06)
- **ex-09 · list-front-pop-is-slow** — dequeue with `list.pop(0)` vs `deque.popleft`, same output —
  verify identical order and note the O(n) vs O(1) cost in a comment. (co-05, co-01)
- **ex-10 · dict-lookup** — build a `dict[str, int]`, look up a present and an absent key via `.get` —
  verify the value and the default via `assert`. (co-08)
- **ex-11 · dict-count-frequencies** — count characters into a `dict[str, int]` — verify the frequency
  map via `assert`. (co-08)
- **ex-12 · set-membership** — build a `set[int]`, test `in` — verify the True/False results via
  `assert`. (co-09)
- **ex-13 · set-dedup** — deduplicate a `list[int]` via `set()` — verify the unique count via `assert`.
  (co-09)
- **ex-14 · two-sum-with-dict** — find two indices summing to a target using a `dict` — verify the
  indices via `assert`. (co-08)
- **ex-15 · linear-search-found** — scan a `list[int]` for a value — verify it returns the correct index
  via `assert`. (co-13)
- **ex-16 · linear-search-not-found** — search for a missing value — verify it returns `-1` via
  `assert`. (co-13)
- **ex-17 · builtin-sorted** — call `sorted(list[int])` — verify ascending order via `assert`. (co-15)
- **ex-18 · sort-with-key** — sort a `list[str]` by length with `key=len` — verify the order via
  `assert`. (co-15)
- **ex-19 · sort-reverse** — `sorted(..., reverse=True)` — verify descending order via `assert`. (co-15)
- **ex-20 · sort-tuples-by-field** — sort a `list[tuple[int, str]]` by the second field — verify the
  order via `assert`. (co-15)
- **ex-21 · factorial-recursive** — recursive factorial with a base case — verify `factorial(5) == 120`
  via `assert`. (co-17)
- **ex-22 · sum-list-recursive** — recursively sum a `list[int]` — verify the total via `assert`. (co-17)
- **ex-23 · countdown-iterative-vs-recursive** — implement both, same output — verify identical results
  via `assert`. (co-18)
- **ex-24 · big-o-constant-vs-linear** — probe a `dict` lookup vs a `list` scan over growing n — verify
  the lookup stays 1 step while the scan grows (print the step counts). (co-01)
- **ex-25 · type-hints-on-function** — annotate `def add(a: int, b: int) -> int` — verify it runs and
  `add.__annotations__` prints the hints. (co-22)
- **ex-26 · type-hints-on-collections** — annotate `list[int]` and `dict[str, int]` parameters — verify
  the function runs correctly on typed inputs via `assert`. (co-22)
- **ex-27 · singly-linked-list-build** — build nodes with a `Node` class (`val: int`, `next:
Optional["Node"]`) — verify traversal prints the values in order. (co-07, co-22)
- **ex-28 · linked-list-length** — count nodes by traversal — verify the length via `assert`. (co-07)

### Intermediate

- **ex-29 · linked-list-reverse** — reverse a singly linked list iteratively — verify the new order via
  `assert`. (co-07)
- **ex-30 · linked-list-middle** — find the middle node with slow/fast pointers — verify the middle
  value via `assert`. (co-07, co-20)
- **ex-31 · binary-search-iterative** — binary-search a sorted `list[int]` — verify the index of the
  target via `assert`. (co-14)
- **ex-32 · binary-search-not-found** — search for a missing value in a sorted list — verify it returns
  `-1` via `assert`. (co-14)
- **ex-33 · binary-search-first-occurrence** — find the first index of a duplicated value — verify the
  leftmost index via `assert`. (co-14)
- **ex-34 · binary-search-last-occurrence** — find the last index of a duplicated value — verify the
  rightmost index via `assert`. (co-14)
- **ex-35 · bisect-insertion-point** — use `bisect.bisect_left` on a sorted list — verify the insertion
  point via `assert`. (co-14)
- **ex-36 · bisect-insort** — `bisect.insort` into a sorted list — verify the list stays sorted via
  `assert`. (co-14, co-03)
- **ex-37 · min-heap-push-pop** — push ints with `heapq.heappush`, pop with `heappop` — verify ascending
  pop order via `assert`. (co-12)
- **ex-38 · heapify-list** — `heapq.heapify` a `list[int]` — verify `heap[0]` is the minimum via
  `assert`. (co-12)
- **ex-39 · top-k-largest** — find the k largest with a min-heap — verify the result set via `assert`.
  (co-12)
- **ex-40 · priority-queue-tuples** — push `(priority, task)` tuples onto a heap — verify pop order by
  priority via `assert`. (co-12)
- **ex-41 · max-heap-via-negation** — negate values to simulate a max-heap — verify the largest pops
  first via `assert`. (co-12)
- **ex-42 · merge-sorted-with-heapq** — merge two sorted lists with `heapq.merge` — verify the merged
  order via `assert`. (co-12, co-15)
- **ex-43 · insertion-sort** — implement insertion sort — verify the output equals `sorted()` via
  `assert`. (co-16)
- **ex-44 · selection-sort** — implement selection sort — verify the sorted output via `assert`. (co-16)
- **ex-45 · bubble-sort** — implement bubble sort — verify the sorted output via `assert`. (co-16)
- **ex-46 · merge-sort** — implement recursive merge sort — verify the sorted output via `assert`.
  (co-16, co-17)
- **ex-47 · quicksort** — implement quicksort — verify the sorted output via `assert`. (co-16, co-17)
- **ex-48 · binary-tree-build** — build a binary tree with a `TreeNode` class — verify the structure via
  a level-order print. (co-10, co-22)
- **ex-49 · tree-inorder-traversal** — inorder-traverse recursively — verify the visited order via
  `assert`. (co-10, co-17)
- **ex-50 · tree-pre-and-post-order** — preorder and postorder traversals — verify both orders via
  `assert`. (co-10, co-17)
- **ex-51 · tree-level-order-bfs** — level-order (BFS) traversal with a `deque` — verify the per-level
  lists via `assert`. (co-10, co-06)
- **ex-52 · tree-height** — compute the tree height recursively — verify the height via `assert`.
  (co-10, co-17)
- **ex-53 · bst-insert** — insert values into a BST maintaining order — verify an inorder traversal
  yields sorted values via `assert`. (co-11)
- **ex-54 · bst-search** — search a BST for a value — verify found and not-found via `assert`. (co-11)
- **ex-55 · bst-min-max** — find the min (leftmost) and max (rightmost) nodes — verify both via
  `assert`. (co-11)
- **ex-56 · graph-adjacency-build** — build a dict-of-lists adjacency graph — verify each node's
  neighbors print correctly. (co-21, co-08)
- **ex-57 · graph-bfs** — BFS over the adjacency dict with a `deque` and a visited `set` — verify the
  visit order via `assert`. (co-21, co-05, co-09)
- **ex-58 · graph-dfs** — DFS recursively with a visited `set` — verify the visit order via `assert`.
  (co-21, co-17, co-09)
- **ex-59 · graph-bfs-shortest-path** — BFS shortest-path length in an unweighted graph — verify the
  distance via `assert`. (co-21, co-05)
- **ex-60 · sliding-window-max-sum** — max sum of a length-k window over a `list[int]` — verify the
  result via `assert`. (co-20)

### Advanced

- **ex-61 · fibonacci-naive-recursive** — naive recursive Fibonacci — verify `fib(10) == 55` and print
  the (exponential) call count. (co-17, co-01)
- **ex-62 · fibonacci-memoized-dict** — memoize Fibonacci with a `dict` cache — verify the same result
  with far fewer calls via `assert`/print. (co-19, co-08)
- **ex-63 · fibonacci-lru-cache** — memoize with `functools.lru_cache` — verify the result and print
  `cache_info()` hits. (co-19)
- **ex-64 · fibonacci-iterative** — bottom-up iterative Fibonacci — verify the result and its O(1) space
  via `assert`. (co-18)
- **ex-65 · coin-change-memoized** — minimum coins via memoized recursion — verify the answer via
  `assert`. (co-19, co-17)
- **ex-66 · grid-paths-memoized** — count unique grid paths with memoization — verify the count via
  `assert`. (co-19)
- **ex-67 · bst-delete** — delete a node from a BST (all three cases) — verify an inorder traversal
  stays sorted via `assert`. (co-11)
- **ex-68 · bst-inorder-iterative** — inorder traversal with an explicit stack — verify it equals the
  recursive order via `assert`. (co-11, co-04, co-18)
- **ex-69 · tree-is-balanced** — check whether a tree is height-balanced — verify True/False on fixtures
  via `assert`. (co-10, co-17)
- **ex-70 · bst-lowest-common-ancestor** — find the LCA of two nodes in a BST — verify the ancestor via
  `assert`. (co-11)
- **ex-71 · dijkstra-with-heap** — shortest paths on a weighted graph using a heap — verify the
  distances via `assert`. (co-12, co-21)
- **ex-72 · topological-sort-kahn** — topo-order a DAG with in-degrees and a queue — verify a valid
  order via `assert`. (co-21, co-05, co-08)
- **ex-73 · detect-cycle-directed** — detect a cycle in a directed graph via DFS coloring — verify True
  on a cyclic and False on an acyclic fixture via `assert`. (co-21, co-17)
- **ex-74 · merge-k-sorted-lists** — merge k sorted lists with a heap — verify the merged order via
  `assert`. (co-12, co-07)
- **ex-75 · quickselect-kth-smallest** — find the kth smallest via quickselect partitioning — verify the
  value via `assert`. (co-16)
- **ex-76 · two-pointer-pair-sum** — find a pair summing to a target in a sorted array with two pointers
  — verify the indices via `assert`. (co-20, co-14)
- **ex-77 · sliding-window-longest-unique** — longest substring without repeats via a window and a `set`
  — verify the length via `assert`. (co-20, co-09)
- **ex-78 · lru-cache-from-scratch** — implement an LRU cache with a `dict` plus a doubly linked list —
  verify the eviction order via `assert`. (co-08, co-07)
- **ex-79 · trie-insert-search** — build a prefix trie with dict-based children — verify insert, search,
  and prefix queries via `assert`. (co-08, co-10)
- **ex-80 · big-o-empirical-doubling** — measure the step counts of linear vs binary search as n doubles
  — verify binary grows ~log n while linear grows ~n (print the counts). (co-01, co-13, co-14)
- **ex-81 · stable-multi-key-sort** — sort records by a tuple key (primary, then secondary) — verify the
  stable multi-key order via `assert`. (co-15)
- **ex-82 · deep-recursion-to-iteration** — convert a deep recursion to iteration to avoid
  `RecursionError` — verify a large input succeeds iteratively via `assert`. (co-18, co-17)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a small "job scheduler" that ingests tasks with priorities and dependencies and emits a
  valid run order — exercising a heap (priority), a dict/set (lookup + seen-tracking), a queue/BFS
  (dependency traversal), and complexity reasoning, all in one runnable program with tests.
- **Concepts exercised**: [ ] `heapq` priority queue [ ] `dict`/`set` lookups [ ] BFS over an adjacency
  dict [ ] cycle detection [ ] Big-O reasoning documented per operation.
- **Ordered steps**:
  1. `.../learning/capstone/code/scheduler.py` — parse tasks `{id, priority, deps}`; build adjacency +
     in-degree. Verify `pytest` on a fixture graph.
  2. Topologically order by dependency, breaking ties by priority via `heapq`. Verify the emitted order
     respects all deps and prefers higher priority on ties.
  3. Detect a dependency cycle and raise a clear error. Verify a cyclic fixture raises.
  4. Document the Big-O of each phase in the module docstring.
- **Acceptance criteria**: `pytest` green on acyclic + cyclic fixtures; documented complexities correct;
  program runs from the CLI on a sample input.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Introduction to Algorithms (CLRS)** — Cormen, Leiserson, Rivest, Stein (4th ed., 2022). The standard rigorous algorithms/data-structures reference; the field's most-cited textbook.
- **The Algorithm Design Manual** — Steven Skiena (3rd ed., 2020). Practical companion to CLRS, prized for "war stories" and its algorithm catalog for working engineers.
- **Algorithms** — Sedgewick, Wayne (4th ed., 2011). Implementation-focused classic pairing runnable code with rigorous analysis. <https://algs4.cs.princeton.edu/home/>

## In which paths

- `interview-ready/software-engineer` — Phase 1 · Interview preparation (through senior).
- `immediately-effective/software-engineer` — Deepening band · CS fundamentals, DS&A & algorithms — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 2 · Data structures, algorithms & object-oriented design.

> _Content originated in the now-closed FS-SE plan (topic 7); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
