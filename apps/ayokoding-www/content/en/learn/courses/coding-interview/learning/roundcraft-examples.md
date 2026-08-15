---
title: "Roundcraft examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 30
---

Examples 51–75 complete the continuous `ex-01` through `ex-75` sequence. They extend the syllabus’s fifty-six examples with nineteen compact rehearsals for variants, diagnostics, and mock-round judgement.

### Example 51 · pattern-misfit recovery

_ex-51 · co-06, co-23_
**Context.** A first two-pointer idea fails because input is unsorted and indices matter. **Key takeaway.** Abandon a misfit explicitly and choose a map. **Why it matters.** Course correction is evidence of reasoning, not a penalty.

### Example 52 · communicate a trade-off

_ex-52 · co-20, co-21_
**Context.** Present sort-plus-pointers and hash lookup for the same pair problem. **Key takeaway.** Say which resource and guarantee each option trades. **Why it matters.** A justified choice demonstrates engineering judgement.

### Example 53 · edge-case hardening

_ex-53 · co-18, co-19_
**Context.** Add empty, duplicate, and negative tests to a passing implementation. **Key takeaway.** Red-to-green repairs should name the broken contract. **Why it matters.** It proves the solution beyond its happy path.

### Example 54 · mock-round self-scoring

_ex-54 · co-01, co-22_
**Context.** Score a timed solve for correctness, communication, complexity, and edge cases. **Key takeaway.** Record evidence, not a vague confidence score. **Why it matters.** Deliberate feedback improves the next round.

### Example 55 · language-agnostic restatement

_ex-55 · co-06_
**Context.** Restate sliding window as pseudocode without Python containers. **Key takeaway.** The invariant is portable; syntax is incidental. **Why it matters.** It prepares the same reasoning for unfamiliar languages.

### Example 56 · capstone mixed set

_ex-56 · co-01, co-06, co-22_
**Context.** Complete five timed prompts across four pattern families. **Key takeaway.** A round needs breadth plus a consistent process. **Why it matters.** It is the bridge into the course capstone.

### Example 57 · choose BFS versus DFS

_ex-57 · co-11_
**Context.** Compare a minimum-hop route question with an existence-only reachability question. **Key takeaway.** Required output determines traversal choice. **Why it matters.** Naming the reason prevents pattern-by-habit.

### Example 58 · state a binary-search predicate

_ex-58 · co-09_
**Context.** Turn “minimum feasible rate” into `can_finish(rate)`. **Key takeaway.** Write the predicate before bounds. **Why it matters.** It makes monotonicity inspectable.

### Example 59 · explain map collision irrelevance

_ex-59 · co-10_
**Context.** An interviewer asks whether hash collisions invalidate expected O(1). **Key takeaway.** Distinguish expected cost from a language runtime’s worst case. **Why it matters.** Accurate caveats build trust without derailing the solve.

### Example 60 · bound a recursion depth

_ex-60 · co-12, co-18_
**Context.** A DFS may exceed Python’s recursion limit on a long chain. **Key takeaway.** State whether iterative traversal is safer for the input bound. **Why it matters.** Runtime limits are real constraints, not trivia.

### Example 61 · preserve a heap invariant

_ex-61 · co-15_
**Context.** Maintain a size-three min-heap while values arrive. **Key takeaway.** Discard only after the invariant has a replacement candidate. **Why it matters.** It avoids losing a top-k value through premature eviction.

### Example 62 · justify monotonic-stack pops

_ex-62 · co-16_
**Context.** Explain why a smaller next-greater candidate can never be useful after a larger arrival. **Key takeaway.** Every pop needs a dominance argument. **Why it matters.** The argument proves linear total work.

### Example 63 · union by size follow-up

_ex-63 · co-17, co-24_
**Context.** Extend basic union-find with size tracking. **Key takeaway.** Keep metadata at representatives. **Why it matters.** It turns a connectivity primitive into component queries.

### Example 64 · distinguish memo from cache

_ex-64 · co-13_
**Context.** Explain why a DP memo key represents a mathematical subproblem, not incidental program state. **Key takeaway.** Cache correctness depends on state completeness. **Why it matters.** It exposes hidden dependencies that cause wrong answers.

### Example 65 · test a greedy claim

_ex-65 · co-14, co-18_
**Context.** Try small counterexamples against a proposed local rule. **Key takeaway.** A failed counterexample search is not proof, but a found one is decisive. **Why it matters.** It keeps intuition proportional to evidence.

### Example 66 · narrate an invariant

_ex-66 · co-04, co-21_
**Context.** Before a loop, say what is true before and after every iteration. **Key takeaway.** An invariant links plan, code, and proof. **Why it matters.** It makes debugging and interviewer communication quicker.

### Example 67 · simplify a follow-up

_ex-67 · co-23, co-24_
**Context.** A follow-up adds a memory limit; first restate which stored state is essential. **Key takeaway.** Reduce the new requirement to a resource constraint. **Why it matters.** It avoids restarting from zero.

### Example 68 · request a focused hint

_ex-68 · co-23_
**Context.** Ask whether the graph is guaranteed acyclic after explaining the blocked choice. **Key takeaway.** A good hint request exposes the precise uncertainty. **Why it matters.** It preserves agency and lets the interviewer assess reasoning.

### Example 69 · preserve output ordering

_ex-69 · co-18, co-20_
**Context.** A grouping solution is correct but output order is unspecified. **Key takeaway.** Ask whether deterministic order is part of the contract. **Why it matters.** Sorting can be necessary correctness work or avoidable cost.

### Example 70 · separate validation from algorithm

_ex-70 · co-02, co-18_
**Context.** Inputs may include invalid edges or a null collection. **Key takeaway.** State whether validation belongs in scope before adding defensive branches. **Why it matters.** It prevents solving a different production problem than the prompt.

### Example 71 · explain space accounting

_ex-71 · co-20_
**Context.** A recursive solution says O(n) space without mentioning call frames. **Key takeaway.** Include auxiliary structures and recursion depth. **Why it matters.** Complete accounting is a credibility check.

### Example 72 · recover after a bug

_ex-72 · co-19, co-23_
**Context.** A dry run reveals an off-by-one boundary. **Key takeaway.** Name the violated invariant, patch narrowly, rerun the trace. **Why it matters.** Calm repair is a strong live signal.

### Example 73 · prioritise the test set

_ex-73 · co-18, co-22_
**Context.** Two minutes remain before handoff. **Key takeaway.** Test a representative success, smallest boundary, and likely invariant breaker. **Why it matters.** A focused set gives more confidence than random cases.

### Example 74 · close the round

_ex-74 · co-20, co-21_
**Context.** Summarise solution, complexity, tests, and one likely follow-up. **Key takeaway.** End with a concise decision record. **Why it matters.** It ensures the strongest signals are heard even if time expires.

### Example 75 · replay with a different pattern

_ex-75 · co-06, co-22, co-24_
**Context.** Re-solve a familiar prompt using a deliberately different valid approach. **Key takeaway.** Compare invariants and costs rather than memorising one answer. **Why it matters.** Flexible recall is what survives a novel interview framing.
