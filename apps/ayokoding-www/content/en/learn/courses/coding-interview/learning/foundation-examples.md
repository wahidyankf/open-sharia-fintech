---
title: "Foundation examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 10
---

The first twenty-five examples rehearse the visible loop before relying on more involved algorithms. Run the linked original Python artefacts in [`code/`](./code/) after narrating your own solution.

### Example 1 · clarify the ambiguous prompt

_ex-01 · co-02_
**Context.** “Return a pair that sums to a target” leaves pair shape, duplicate use, and no-solution behaviour unspecified. **Key takeaway.** Ask those questions before choosing state. **Why it matters.** A perfect answer to an invented contract is still a miss.

### Example 2 · trace a concrete example

_ex-02 · co-03_
**Context.** Trace `[2, 7, 11, 15]`, target `9`, marking the information known after each value. **Key takeaway.** A tiny trace exposes the needed lookup. **Why it matters.** It turns pattern selection into evidence rather than recall.

### Example 3 · state plan and Big-O first

_ex-03 · co-04_
**Context.** Before coding two-sum, say “one pass plus complement map: expected O(n) time and O(n) space.” **Key takeaway.** State the contract before implementation details. **Why it matters.** It gives the interviewer a chance to redirect cheaply.

### Example 4 · brute-force two-sum

_ex-04 · co-05_
**Context.** Check every index pair and explain its O(n²) cost. **Key takeaway.** A correct baseline is a useful first deliverable. **Why it matters.** It gives an optimisation something testable to preserve.

### Example 5 · optimise two-sum with a hash map

_ex-05 · co-05, co-10_
**Context.** Lookup each complement before storing the current value. **Key takeaway.** A map removes repeated scans. **Why it matters.** The ordering avoids accidentally pairing an element with itself.

### Example 6 · two-pointer reverse

_ex-06 · co-07_
**Context.** Swap the ends of a mutable sequence and move inward. **Key takeaway.** The already-swapped exterior is the invariant. **Why it matters.** It models disciplined pointer movement.

### Example 7 · two-pointer pair sum, sorted

_ex-07 · co-07_
**Context.** On sorted values, move left when the sum is low and right when high. **Key takeaway.** Ordering proves the discarded pair region cannot help. **Why it matters.** That proof, not “two pointers,” justifies linear time.

### Example 8 · fixed-window maximum sum

_ex-08 · co-08_
**Context.** Compare recomputing every width-three sum with subtracting the leaving value and adding the entering value. **Key takeaway.** Preserve the window aggregate. **Why it matters.** It converts repeated O(k) work into O(1) updates.

### Example 9 · longest unique substring

_ex-09 · co-08, co-10_
**Context.** Expand a character window and shrink until duplicates disappear. **Key takeaway.** The window must remain duplicate-free after each iteration. **Why it matters.** A stated invariant prevents off-by-one repairs later.

### Example 10 · classic binary search

_ex-10 · co-09_
**Context.** Search a sorted sequence with inclusive bounds and a clear not-found result. **Key takeaway.** Every branch must strictly reduce the interval. **Why it matters.** Boundary progress is the difference between logarithmic search and an infinite loop.

### Example 11 · first and last duplicate

_ex-11 · co-09, co-18_
**Context.** Find both bounds of a repeated target. **Key takeaway.** Equality can continue the search toward a desired boundary. **Why it matters.** It exercises duplicates and termination together.

### Example 12 · frequency count

_ex-12 · co-10_
**Context.** Count values in one pass, then inspect the resulting map. **Key takeaway.** A hash map records sufficient history. **Why it matters.** Frequency state supports many “first unique” and grouping prompts.

### Example 13 · group anagrams

_ex-13 · co-10_
**Context.** Group words by a canonical character-count or sorted key. **Key takeaway.** Equivalent inputs need the same key. **Why it matters.** The key design matters more than the dictionary syntax.

### Example 14 · enumerate edge cases

_ex-14 · co-18_
**Context.** Before max-subarray code, list empty, single, all-negative, and mixed arrays. **Key takeaway.** Edge cases are part of requirements discovery. **Why it matters.** They determine whether a default value is valid or a bug.

### Example 15 · dry-run a solution

_ex-15 · co-19_
**Context.** Walk a completed sliding-window loop over `"abba"`. **Key takeaway.** Predict state before trusting output. **Why it matters.** It catches stale counts and wrong boundary moves without a debugger.

### Example 16 · articulate final complexity

_ex-16 · co-20_
**Context.** Close a map solution with O(n) time, O(n) memory, and contrast it with O(n²)/O(1). **Key takeaway.** Complexity includes the resource exchanged. **Why it matters.** Senior judgement is often visible in the trade-off, not the notation.

### Example 17 · think-aloud transcript

_ex-17 · co-21_
**Context.** Narrate an observation, candidate pattern, invariant, and test while coding. **Key takeaway.** Explain decisions, not every keystroke. **Why it matters.** The transcript gives the interviewer evidence and a useful intervention point.

### Example 18 · time-box a solve

_ex-18 · co-22_
**Context.** Allocate a thirty-minute round to clarify, plan, code, and verify. **Key takeaway.** Verification is a scheduled activity. **Why it matters.** Leaving it to “if time remains” creates avoidable failures.

### Example 19 · BFS shortest unweighted path

_ex-19 · co-11_
**Context.** Explore a grid level by level and record distance on discovery. **Key takeaway.** FIFO order gives first-arrival minimum hops. **Why it matters.** It distinguishes BFS from DFS by a concrete guarantee.

### Example 20 · DFS connected components

_ex-20 · co-11, co-17_
**Context.** Flood-fill each unvisited island. **Key takeaway.** One traversal claims exactly one component. **Why it matters.** It makes the component count and visited invariant observable.

### Example 21 · tree level order

_ex-21 · co-11_
**Context.** Process a queue one level-sized batch at a time. **Key takeaway.** Queue length at the level boundary is useful state. **Why it matters.** It turns a generic traversal into structured output.

### Example 22 · tree root-to-leaf paths

_ex-22 · co-11, co-12_
**Context.** Carry a path through recursive DFS and copy it at leaves. **Key takeaway.** Mutable path state requires deliberate backtracking. **Why it matters.** It avoids aliases that make every recorded path identical.

### Example 23 · subsets

_ex-23 · co-12_
**Context.** For each element, choose or skip it. **Key takeaway.** The expected count is 2ⁿ. **Why it matters.** A count is a cheap correctness oracle for enumeration.

### Example 24 · permutations

_ex-24 · co-12_
**Context.** Select one unused value at each depth. **Key takeaway.** The used-set or swap boundary is the state contract. **Why it matters.** It prevents duplicate reuse and supports an n! sanity check.

### Example 25 · combination sum

_ex-25 · co-12, co-18_
**Context.** Build sorted combinations toward a target and prune overshoots. **Key takeaway.** Ordering and start positions prevent duplicate outputs. **Why it matters.** It demonstrates that pruning must preserve completeness.
