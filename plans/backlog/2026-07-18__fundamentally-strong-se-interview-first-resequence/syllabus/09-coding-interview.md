# 09 · Coding Interview (By Example, Python — patterns language-agnostic)

**Mapping row** (frozen [tech-docs §Canonical Mapping Table](../tech-docs.md#canonical-mapping-table)):
N=9 · Phase 1 · Interview Preparation · By Example · Python (patterns language-agnostic) · folder
weight 190 / learn 109 / drill 209. **NEW (interview module)**.

**Scope note**: the coding-interview _as a format_ — the recurring problem-solving **patterns**, the
narration and time-management **strategy**, and the pass/fail signals interviewers actually score. It
is a **refresh** for an experienced engineer re-grounding fast, not a first teaching of data
structures (that is [N=7 `data-structures-and-algorithms-essentials`](./README.md)) or algorithms (that
is [N=8 `advanced-algorithms`](./README.md)) — it references those forward and drills the _interview
skin_ over them. Examples are Python; every pattern is language-agnostic.

## Why this exists · the big idea

- **The problem before the solution**: a strong engineer can still fail a coding round — not for lack
  of ability, but for freezing on an unfamiliar framing, silent problem-solving that gives the
  interviewer nothing to score, or burning the clock on the wrong approach. The round tests a
  _performance_ skill distinct from the underlying CS.
- **Keep-this-if-you-forget-everything**: recognise the **pattern**, state your plan and its complexity
  _out loud before coding_, then code the plan — the interview scores your visible reasoning at least as
  much as the final code.
- **Big ideas touched**: `correctness-vs-pragmatism` (a correct brute force stated clearly beats a
  half-built optimal solution), `abstraction-and-its-cost` (pattern recognition is reusable abstraction
  over a family of problems).

## Prerequisites

- **Prior topics**: [N=7 Data Structures & Algorithms Essentials](./README.md) and
  [N=8 Advanced Algorithms](./README.md) (arrays, hash maps, trees, graphs, sorting, recursion, DP,
  Big-O); [N=4 Just Enough Python](./README.md) for the example language.
- **Tools & environment**: a macOS/Linux terminal; Python 3.x; `pytest` for the drill harness; a
  whiteboard-or-plain-editor discipline (no autocomplete/LSP during a mock, to mirror interview
  conditions); Neovim/VSCode for authoring.
- **Assumed knowledge**: reading and writing Python comfortably; Big-O analysis; the core data
  structures and their operations' costs.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (DD-28 convention). Items below are stable-concept or
> flagged `[Needs Verification]`.

- 2026-07-18 — the pattern taxonomy (two-pointer, sliding window, binary search, BFS/DFS, backtracking,
  dynamic programming, greedy, heap/top-k, union-find, trie, monotonic stack) is a **stable, vendor-
  independent** body of practice; not pinned to any platform.
- 2026-07-18 — `[Needs Verification]`: any named practice platform, its problem counts, or its UI —
  keep shipped text platform-agnostic; re-verify before naming a specific site.
- 2026-07-18 — `[Needs Verification]`: current company-round _formats_ (durations, number of problems,
  remote tooling) change; state them as typical ranges, not fixed facts, and re-verify at authoring.

## Concepts

1. **co-01 · what-the-round-scores** — a coding round scores problem-solving process, communication,
   correctness, and coding fluency — not just a passing submission.
2. **co-02 · clarify-before-coding** — restating the problem and asking about constraints, input
   ranges, and edge cases before writing code prevents solving the wrong problem.
3. **co-03 · work-a-concrete-example** — hand-tracing one small input surfaces the pattern and the edge
   cases before any code exists.
4. **co-04 · state-the-approach-and-complexity-first** — announcing the plan and its time/space Big-O
   before coding lets the interviewer redirect early and scores visible reasoning.
5. **co-05 · brute-force-then-optimize** — a correct brute force stated first anchors correctness; the
   optimization is a deliberate second step, not the opening move.
6. **co-06 · pattern-recognition** — most interview problems map to a small set of recurring patterns;
   naming the pattern collapses the search space.
7. **co-07 · two-pointer-pattern** — coordinated indices over a sequence solve pair/partition/reverse
   problems in one pass.
8. **co-08 · sliding-window-pattern** — a moving window over a sequence solves contiguous-subarray/
   substring problems in linear time.
9. **co-09 · binary-search-pattern** — searching a sorted or monotonic answer space halves the work
   each step, including "binary search on the answer."
10. **co-10 · hashing-for-lookup** — a hash map trades space for O(1) membership/counting, turning many
    quadratic scans into linear ones.
11. **co-11 · bfs-dfs-traversal** — breadth-first and depth-first traversal solve reachability,
    shortest-unweighted-path, and connectivity on trees and graphs.
12. **co-12 · backtracking-pattern** — systematic choose/explore/un-choose enumerates combinations,
    permutations, and constraint-satisfaction solutions.
13. **co-13 · dynamic-programming-pattern** — overlapping subproblems + optimal substructure yield a
    memoized or tabulated recurrence.
14. **co-14 · greedy-pattern** — a locally optimal choice yields a global optimum only when an exchange
    argument justifies it — and knowing when it does not is the skill.
15. **co-15 · heap-and-top-k** — a heap maintains the k largest/smallest or a running median in
    O(log n) per element.
16. **co-16 · monotonic-stack** — a stack kept sorted solves next-greater-element and span problems in
    linear time.
17. **co-17 · union-find** — disjoint-set union tracks connectivity and cycle detection near-constant
    time per operation.
18. **co-18 · edge-case-enumeration** — empty input, single element, duplicates, overflow, and negative
    values are the failures interviewers probe.
19. **co-19 · dry-run-verification** — walking the finished code over the concrete example, line by
    line, catches bugs before the interviewer runs it.
20. **co-20 · complexity-tradeoff-articulation** — stating the final time/space complexity and the
    trade-off taken demonstrates the senior-level judgment the round rewards.
21. **co-21 · thinking-aloud-discipline** — narrating reasoning continuously turns silent work into a
    scoreable signal and invites course-correcting hints.
22. **co-22 · time-boxing-the-problem** — allocating clarify/plan/code/verify time and cutting a
    stuck approach prevents a zero-signal round.
23. **co-23 · recovering-from-a-stuck-point** — asking for a hint, simplifying the problem, or falling
    back to brute force is a recoverable, scoreable move, not a failure.
24. **co-24 · handling-follow-ups** — interviewers extend a solved problem (scale it, change a
    constraint); anticipating the follow-up shows depth.

## Tensions & trade-offs — when NOT to reach for this

- **Optimal vs finished**: reaching for the clever O(n) solution and running out of time scores worse
  than a clean, tested O(n²) that runs. Optimize only after a correct solution exists — unless the
  interviewer explicitly asks for optimal up front.
- **Speed vs communication**: racing to code in silence forfeits the round's largest signal. The cost
  of narrating is a few seconds; the cost of silence is an unscoreable performance.
- **When NOT to pattern-match**: forcing a familiar pattern onto a problem it does not fit wastes the
  clock — a novel problem sometimes needs first-principles reasoning, and recognising _that_ is itself
  the skill.

## Lineage — why it beat the alternative

- The structured "clarify → example → plan+complexity → code → verify" loop displaced the older "just
  start coding" instinct because interviewers score _process_, and a legible process both prevents
  wrong-problem failures and gives the interviewer hooks to help. Pattern taxonomies emerged because the
  problem space, though large, clusters tightly — so recognition beats rederivation under time
  pressure. This module hands the interview skin forward to [N=10 Take-Home & Live
  Coding](./10-take-home-and-live-coding.md) (async and pairing formats) and up to the [Phase 1 mock
  loop capstone](./16c-capstone-interview-loop.md).

## Worked examples

Colocated under `coding-interview/learning/code/`. Each example is a recorded solve: a problem
statement, a spoken-reasoning transcript (as comments), the coded solution with inline complexity
notes, and a `pytest` drill. Contiguous `ex-01..ex-56`. Every example cites the `co-NN` it exercises;
every concept is exercised by ≥ 1 example.

> **Volume-target floor**: this syllabus lists **56** of the required **≥75** (the 75–85 By-Example/
> Primer band, floor not cap — see
> [prd.md §Volume-target bands](../prd.md#volume-target-bands-inherited-from-sibling-dd-34-floor-not-cap-dd-8)).
> The maker adds **≥19** more `ex-NN` entries at authoring time, continuing the numbering and pattern
> taxonomy below, before this topic passes its by-example quality gate.

### Beginner (ex 01–18)

1. **ex-01 · clarify-the-ambiguous-prompt** — given a deliberately under-specified prompt, write the
   clarifying questions before any code — verify the transcript lists input ranges + edge cases. (co-02)
2. **ex-02 · trace-a-concrete-example** — hand-trace a small input to reveal the pattern — verify the
   trace table matches the expected intermediate states. (co-03)
3. **ex-03 · state-plan-and-bigo-first** — announce approach + time/space before coding a sum problem —
   verify the stated Big-O matches the implemented one. (co-04)
4. **ex-04 · brute-force-two-sum** — solve two-sum in O(n²) first — verify correctness on all cases.
   (co-05)
5. **ex-05 · optimize-two-sum-with-hash** — reduce two-sum to O(n) with a hash map — verify same output,
   lower complexity. (co-05, co-10)
6. **ex-06 · two-pointer-reverse** — reverse an array in place with two pointers — verify against the
   slice reverse. (co-07)
7. **ex-07 · two-pointer-pair-sum-sorted** — find a pair summing to a target in a sorted array — verify
   O(n) single pass. (co-07)
8. **ex-08 · sliding-window-max-sum** — maximum sum of a fixed-size window — verify against the naive
   recompute. (co-08)
9. **ex-09 · sliding-window-longest-unique** — longest substring without repeats — verify on strings
   with duplicates. (co-08, co-10)
10. **ex-10 · binary-search-classic** — find a target index in a sorted array — verify boundaries and
    the not-found case. (co-09)
11. **ex-11 · binary-search-first-last** — leftmost/rightmost occurrence of a duplicate — verify both
    bounds. (co-09, co-18)
12. **ex-12 · hash-frequency-count** — count element frequencies — verify the map against a manual
    tally. (co-10)
13. **ex-13 · hash-anagram-check** — group anagrams by a canonical key — verify grouping. (co-10)
14. **ex-14 · enumerate-edge-cases** — for a max-subarray prompt, list empty/single/all-negative cases
    before coding — verify each is handled. (co-18)
15. **ex-15 · dry-run-a-solution** — line-trace a finished function over the concrete example — verify
    the trace predicts the actual output. (co-19)
16. **ex-16 · articulate-final-complexity** — write the closing complexity statement + trade-off for a
    solved problem — verify it names both time and space. (co-20)
17. **ex-17 · think-aloud-transcript** — annotate a solve with a continuous reasoning transcript —
    verify no coding step is silent. (co-21)
18. **ex-18 · time-box-a-solve** — split a 30-minute budget across clarify/plan/code/verify and record
    the actual split — verify the plan+verify phases were not skipped. (co-22)

### Intermediate (ex 19–40)

1. **ex-19 · bfs-shortest-unweighted** — shortest path in an unweighted grid via BFS — verify distance
   against a hand count. (co-11)
2. **ex-20 · dfs-connected-components** — count islands in a grid via DFS — verify component count.
   (co-11, co-17)
3. **ex-21 · tree-level-order** — BFS a binary tree into levels — verify the level lists. (co-11)
4. **ex-22 · tree-dfs-paths** — enumerate root-to-leaf paths via DFS — verify all paths. (co-11, co-12)
5. **ex-23 · backtracking-subsets** — generate all subsets via choose/explore/un-choose — verify count
   is 2ⁿ. (co-12)
6. **ex-24 · backtracking-permutations** — all permutations of a list — verify count is n!. (co-12)
7. **ex-25 · backtracking-combination-sum** — combinations summing to a target — verify no duplicates.
   (co-12, co-18)
8. **ex-26 · dp-fibonacci-memo** — memoized Fibonacci — verify against the naive recursion's values.
   (co-13)
9. **ex-27 · dp-climbing-stairs** — count ways with tabulation — verify the recurrence. (co-13)
10. **ex-28 · dp-coin-change** — minimum coins for an amount — verify the unreachable case returns the
    sentinel. (co-13, co-18)
11. **ex-29 · dp-longest-common-subsequence** — LCS length with a 2-D table — verify against a known
    pair. (co-13)
12. **ex-30 · greedy-interval-scheduling** — maximum non-overlapping intervals — verify optimality on a
    known case. (co-14)
13. **ex-31 · greedy-vs-dp-contrast** — a problem where greedy fails and DP succeeds — verify greedy's
    wrong answer, then DP's correct one. (co-14, co-13)
14. **ex-32 · heap-top-k-elements** — the k largest via a min-heap of size k — verify O(n log k). (co-15)
15. **ex-33 · heap-merge-k-lists** — merge k sorted lists with a heap — verify sorted output. (co-15)
16. **ex-34 · heap-running-median** — median of a stream with two heaps — verify after each insert.
    (co-15)
17. **ex-35 · monotonic-stack-next-greater** — next greater element per position — verify linear time.
    (co-16)
18. **ex-36 · monotonic-stack-daily-temps** — days-until-warmer via a monotonic stack — verify against
    brute force. (co-16)
19. **ex-37 · union-find-cycle-detection** — detect a cycle in an undirected graph — verify on cyclic
    and acyclic inputs. (co-17)
20. **ex-38 · recover-from-stuck** — a recorded solve that stalls, asks for a hint, and recovers —
    verify the transcript shows the recovery move. (co-23)
21. **ex-39 · handle-a-follow-up** — solve a problem, then answer "now make it streaming" — verify the
    follow-up solution reuses the first. (co-24)
22. **ex-40 · binary-search-on-answer** — minimum capacity to ship in D days via binary search on the
    answer — verify the feasibility predicate. (co-09, co-13)

### Advanced (ex 41–56)

1. **ex-41 · graph-dijkstra-topk** — shortest weighted path with a heap-backed Dijkstra — verify
   distances. (co-11, co-15)
2. **ex-42 · dp-edit-distance** — Levenshtein distance with a table — verify against a known pair.
   (co-13)
3. **ex-43 · dp-knapsack-0-1** — 0/1 knapsack — verify optimal value and the reconstruction. (co-13,
   co-20)
4. **ex-44 · backtracking-n-queens** — place n queens with pruning — verify solution count. (co-12)
5. **ex-45 · sliding-window-min-covering** — minimum window substring covering a target set — verify
   the window. (co-08, co-10)
6. **ex-46 · trie-prefix-search** — build a trie and query prefixes — verify membership + prefix
   counts. (co-06, co-10)
7. **ex-47 · union-find-account-merge** — merge accounts by shared email via union-find — verify
   groups. (co-17)
8. **ex-48 · monotonic-deque-sliding-max** — sliding-window maximum with a monotonic deque — verify
   O(n). (co-16, co-08)
9. **ex-49 · full-solve-transcript** — one problem end to end: clarify → example → plan+Big-O → code →
   dry-run → complexity → follow-up — verify every phase is present. (co-01..co-04, co-19, co-20, co-24)
10. **ex-50 · optimize-under-time-pressure** — ship a correct brute force, then optimize only if time
    remains, recording the decision — verify the brute force passed before the optimization began.
    (co-05, co-22)
11. **ex-51 · pattern-misfit-recovery** — a problem that resists the first pattern guessed; record the
    pivot to the correct one — verify the wrong pattern was abandoned, not forced. (co-06, co-23)
12. **ex-52 · communicate-a-tradeoff** — present two valid solutions and justify the chosen trade-off —
    verify both complexities are stated. (co-20, co-21)
13. **ex-53 · edge-case-hardening** — take a passing solution and add empty/overflow/duplicate tests
    that break it, then fix — verify red→green. (co-18, co-19)
14. **ex-54 · mock-round-self-scoring** — solve under a timer and score the transcript against a rubric
    (correctness, communication, complexity, edge cases) — verify each rubric row is rated. (co-01, co-22)
15. **ex-55 · language-agnostic-restate** — re-express one solved pattern's plan in pseudocode
    portable to any language — verify the plan omits Python-specific idioms. (co-06)
16. **ex-56 · capstone-mixed-set** — a mixed five-problem timed set spanning ≥ 4 patterns with self-
    scoring — verify all five pass and the score sheet is complete. (co-01, co-06, co-22)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: run a self-administered, timed coding round of five problems spanning at least four distinct
  patterns, each solved under the clarify → plan+Big-O → code → verify discipline with a recorded
  reasoning transcript, then self-scored against an interview rubric.
- **Concepts exercised**: [ ] clarify + concrete example (co-02, co-03) [ ] plan + complexity first
  (co-04) [ ] ≥ 4 distinct patterns (co-06–co-17) [ ] edge-case enumeration + dry run (co-18, co-19)
  [ ] think-aloud + time-boxing (co-21, co-22) [ ] complexity articulation (co-20).
- **Ordered steps**:
  1. `coding-interview/learning/capstone/problems.md` — five problems + a rubric. Verify each names its
     target pattern and the timer budget.
  2. `coding-interview/learning/capstone/code/` — one solution file per problem with a transcript and a
     `pytest`. Verify all five test suites pass.
  3. `coding-interview/learning/capstone/scoresheet.md` — self-score each solve on correctness,
     communication, complexity, and edge cases. Verify every row is rated with a justification.
- **Acceptance criteria**: all five problems pass their tests within their budgets; each solve records a
  visible plan-and-complexity step; the score sheet justifies every rating.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

- **Cracking the Coding Interview** — Gayle Laakmann McDowell. The standard practitioner reference for
  round structure and pattern practice (treat specific problems as illustrative, not canonical).
- **Introduction to Algorithms** — Cormen, Leiserson, Rivest, Stein (CLRS). The authoritative reference
  for the algorithms the patterns draw on.

---

← Previous: N=8 `advanced-algorithms` ([index](./README.md)) · Next:
[N=10 · Take-Home & Live Coding](./10-take-home-and-live-coding.md) →
