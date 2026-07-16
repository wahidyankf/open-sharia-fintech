# 19 · Computer Science Foundations (Annotated-concept, Python \*)

**prd row**: Pass 2 · Depth, Design & Craft · Annotated-concept · Python \* · Learn 119 / Drill 219 ·
Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: the CS bedrock a self-taught-style engineer usually skips — data representation, logic,
machine organization, automata, computability/complexity, and information theory — at intuition depth,
grounded in small runnable Python demonstrations (`*`: Python where code appears, else prose + diagrams).
Depth in specific areas is spread across [`25-advanced-algorithms`](./25-advanced-algorithms.md) and
[`88-type-systems`](./88-type-systems.md); this topic builds the mental model they hang on.

## Why this exists · the big idea

- **The problem before the solution**: skip the bedrock and you hit a ceiling you can't explain — why
  `0.1 + 0.2 != 0.3`, why one loop is 10× faster, why some problems have no fast solution at all.
- **Keep-this-if-you-forget-everything**: everything you write runs on a finite machine built in layers
  from gates upward — knowing the layers below lets you _explain_ the anomaly instead of fearing it.
- **Big ideas touched**: `layering-and-leaks` — the whole computing stack is abstraction over gates, and
  its leaks (float rounding, cache effects) are exactly this topic; `abstraction-and-its-cost`.

## Prerequisites

- **Prior topics**: [topic 4 Just Enough Python](./04-just-enough-python.md) (the small demonstrations
  are Python); [topic 7 Data Structures & Algorithms Essentials](./07-data-structures-and-algorithms-essentials.md)
  gives the stack/heap and Big-O vocabulary this topic deepens.
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x**; a REPL for number/representation demos.
- **Assumed knowledge**: reading/writing basic Python; comfort with arithmetic and simple algebra (no
  formal CS or discrete-math background assumed — the topic builds it).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: IEEE-754 (754-2019 current revision, no successor), two's-complement, and UTF-8
  (RFC 3629, unchanged since 2003) are stable specs; P-vs-NP remains open in 2026 (Clay Millennium Prize
  unclaimed) — the syllabus's "intuition" framing claims no resolution, so it is safe; Chomsky-hierarchy
  terminology unchanged. Python `struct`/`bin`/`hex` behavior long-stable — spot-check `docs.python.org` at
  authoring. (ieee.org / ietf.org / claymath.org)

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (Annotated-concept). Each example below cites the co-NN it exercises. -->

- **co-01 · positional-number-systems** — binary/hex/decimal are positional systems; convert between bases
  by repeated division/multiplication.
- **co-02 · twos-complement** — negative integers invert bits and add 1, letting one adder circuit handle
  both addition and subtraction.
- **co-03 · ieee-754-floats** — a float is a sign/exponent/mantissa bit layout (IEEE 754-2019); rounding
  error (`0.1 + 0.2 != 0.3`) is structural, not a bug.
- **co-04 · endianness** — byte order (big-endian vs little-endian) in which a multi-byte value is stored
  or transmitted.
- **co-05 · unicode-utf8** — Unicode assigns each character a code point; UTF-8 (RFC 3629) is the
  ASCII-compatible, variable-length encoding dominant on the wire.
- **co-06 · boolean-algebra** — AND/OR/NOT (and derived XOR/NAND/NOR) form a complete algebra; De Morgan's
  laws let any expression be rewritten.
- **co-07 · truth-tables-and-gates** — a truth table enumerates every input combination's output; logic
  gates are the physical/simulated realization.
- **co-08 · combinational-vs-sequential** — combinational circuits are pure functions of current inputs;
  sequential circuits add memory (state) via feedback/clocking.
- **co-09 · sets-and-relations** — sets, subsets, and relations (reflexive/symmetric/transitive) formalize
  "belongs to" and "is related to".
- **co-10 · propositional-logic** — propositions combine via ∧/∨/¬/→/↔; truth tables decide validity.
- **co-11 · predicate-logic** — quantifiers ∀/∃ extend propositional logic to statements over a domain's
  members.
- **co-12 · combinatorics-and-counting** — permutations, combinations, and counting principles that size a
  search space or a collision risk.
- **co-13 · graph-theory-basics** — vertices/edges, directed/undirected, degree/path/cycle vocabulary
  underlying data structures and automata.
- **co-14 · proof-by-induction** — a base case plus an inductive step proves a property for all naturals;
  the reasoning template recursion mirrors.
- **co-15 · cpu-registers-alu** — the fetch-decode-execute cycle; registers as fast local storage; the ALU
  as the arithmetic/logic execution unit.
- **co-16 · memory-hierarchy-intuition** — registers → cache → RAM → disk trade capacity for latency
  (survey depth here; full treatment in [`20-computer-architecture`](./20-computer-architecture.md)).
- **co-17 · stack-and-heap** — the call stack holds frames with automatic lifetime; the heap holds
  dynamically allocated data with manual/GC lifetime.
- **co-18 · finite-automata** — a DFA/NFA (states, alphabet, transition function, start, accept states)
  recognizes a regular language.
- **co-19 · regex-to-fa-equivalence** — Kleene's theorem: a language is regular iff a regex describes it
  iff a finite automaton accepts it.
- **co-20 · context-free-grammars-and-pushdown-automata** — a CFG's productions generate a context-free
  language; a pushdown automaton (FA + stack) accepts exactly the CFLs.
- **co-21 · chomsky-hierarchy** — four nested classes (regular ⊂ context-free ⊂ context-sensitive ⊂
  recursively enumerable), each tied to a grammar restriction and a matching automaton.
- **co-22 · turing-machines** — an infinite-tape read/write/move state machine is the formal model of
  "what is computable" (Church-Turing thesis).
- **co-23 · halting-problem** — no algorithm can decide, for every program/input pair, whether that program
  halts; proved by diagonalization (Turing, 1936).
- **co-24 · p-vs-np** — P is poly-time-solvable problems; NP is poly-time-verifiable problems; whether
  P = NP is open.
- **co-25 · np-completeness-and-reductions** — an NP-complete problem is in NP and every NP problem reduces
  to it in poly time (Cook-Levin, SAT); a poly-time solution to one collapses P = NP.
- **co-26 · shannon-entropy** — entropy quantifies the average bits needed to describe an outcome given its
  probability distribution (Shannon, 1948).
- **co-27 · lossless-vs-lossy-compression** — lossless coding (e.g. Huffman) reconstructs the exact input;
  lossy coding discards information for a smaller representation.
- **co-28 · checksums-and-hashing** — a checksum (e.g. CRC32) detects accidental corruption; a cryptographic
  hash (e.g. SHA-256) is a fixed-size, effectively-irreversible digest for integrity/identity.

## Worked examples

Colocated under `computer-science-foundations/learning/code/`; runnable Python + WCAG-accessible Mermaid
where code does not fit (DD-20/DD-30). Every example cites the `co-NN` concept(s) it exercises.
Contiguous `ex-01..ex-55`.

### Beginner

- **ex-01 · dec-to-binary-by-division** — convert 156 to binary by repeated division by 2 — verify it
  prints `10011100`, matching `bin(156)`. (co-01)
- **ex-02 · base-roundtrip** — round-trip a value through `bin`/`hex`/`int(s, base)` — verify equality
  holds across all three bases. (co-01)
- **ex-03 · twos-complement-8bit** — represent -42 in 8-bit two's complement — verify the pattern is
  `11010110` and `(-42 & 0xFF) + 42 == 256`. (co-02)
- **ex-04 · subtraction-as-addition** — compute `5 - 3` by adding the two's-complement of 3 in 8 bits —
  verify the low byte equals 2. (co-02)
- **ex-05 · float-rounding-error** — show `0.1 + 0.2 != 0.3` and print the exact value — verify
  `0.30000000000000004`. (co-03)
- **ex-06 · float-bit-inspector** — dump IEEE-754 bits of `1.0` via `struct.pack('>d', x)` — verify the
  sign/exponent/mantissa fields decode back to 1.0. (co-03)
- **ex-07 · endianness-struct-pack** — pack `1` as `<i` vs `>i` — verify byte orders `01 00 00 00` vs
  `00 00 00 01`. (co-04)
- **ex-08 · byteorder-roundtrip** — read `sys.byteorder`, convert with `int.to_bytes`/`from_bytes` both
  orders — verify round-trip identity. (co-04)
- **ex-09 · utf8-encode-multibyte** — encode `"café"` and `"文"` to UTF-8 — verify é is 2 bytes, 文 is
  3 bytes. (co-05)
- **ex-10 · codepoint-vs-byte-len** — show `len(s)` vs `len(s.encode('utf-8'))` diverge for non-ASCII —
  verify the two counts differ. (co-05)
- **ex-11 · truth-tables-generate** — generate AND/OR/XOR truth tables programmatically — verify each
  row matches the operator. (co-06, co-07)
- **ex-12 · de-morgan-verify** — check `not (a and b) == (not a or not b)` over all inputs — verify all
  four rows True. (co-06)
- **ex-13 · nand-completeness** — build AND/OR/NOT from only NAND — verify equivalence to the builtins.
  (co-06)
- **ex-14 · half-adder** — implement a half-adder (`sum = XOR`, `carry = AND`) — verify its truth table.
  (co-07, co-08)
- **ex-15 · sequential-counter** — simulate a clocked counter holding state across calls — verify the
  state persists and increments. (co-08)
- **ex-16 · set-operations** — union/intersection/difference on Python sets — verify against hand-computed
  results. (co-09)
- **ex-17 · relation-properties** — classify a relation as reflexive/symmetric/transitive — verify each
  property flag. (co-09)
- **ex-18 · implication-truth-table** — evaluate `p -> q` for all inputs — verify only `(True, False)` is
  False. (co-10)

### Intermediate

- **ex-19 · quantifiers-all-any** — model ∀/∃ with `all()`/`any()` over a domain — verify both against a
  hand check. (co-11)
- **ex-20 · permutations-count** — compute nPr and enumerate with `itertools.permutations` — verify count
  `== n!/(n-r)!`. (co-12)
- **ex-21 · birthday-collision** — compute the birthday-paradox collision probability — verify it exceeds
  0.5 at 23 people. (co-12)
- **ex-22 · graph-adjacency-degrees** — build an adjacency list and compute vertex degrees — verify
  against the edge list. (co-13)
- **ex-23 · cycle-detection-dfs** — detect a cycle in a directed graph via DFS colors — verify it flags a
  known cyclic graph. (co-13)
- **ex-24 · induction-sum-check** — verify `sum(1..n) == n(n+1)/2` via base case + inductive step in code
  — verify for n up to 1000. (co-14)
- **ex-25 · register-machine-sim** — simulate a tiny LOAD/ADD/STORE machine — verify the accumulator holds
  the expected result. (co-15)
- **ex-26 · alu-op-model** — model a register file feeding an ALU operation — verify the flag/result pair.
  (co-15)
- **ex-27 · latency-hierarchy-table** — print approximate register/cache/RAM/disk latency ratios — verify
  the strictly increasing ordering. (co-16)
- **ex-28 · cache-friendly-traversal** — time row-major vs column-major traversal of a 2-D array — verify
  row-major is measurably faster. (co-16)
- **ex-29 · stack-frame-trace** — recursive factorial printing call depth — verify frames push then pop
  in order. (co-17)
- **ex-30 · stack-vs-heap-ids** — contrast a local int with a heap-allocated list via `id()` — verify the
  heap object outlives the frame. (co-17)
- **ex-31 · recursion-limit** — trigger and catch `RecursionError` — verify the exception is raised near
  `sys.getrecursionlimit()`. (co-17)
- **ex-32 · dfa-even-zeros** — DFA accepting strings with an even number of 0s — verify accept/reject on
  a test set. (co-18)
- **ex-33 · dfa-simulator** — generic DFA driven by a transition table — verify it runs any supplied
  machine. (co-18)
- **ex-34 · nfa-nondeterminism** — an NFA with ε-moves showing multiple live states — verify it accepts
  where a naive DFA would not. (co-18)
- **ex-35 · regex-to-dfa** — map regex `(ab)*` to an accepting DFA — verify strings classify identically.
  (co-19)
- **ex-36 · kleene-equivalence** — compare Python `re` match vs the hand DFA on the same language —
  verify agreement on all inputs. (co-19)
- **ex-37 · cfg-balanced-parens** — a CFG for balanced parens with a recursive checker — verify balanced
  vs unbalanced strings. (co-20)
- **ex-38 · pda-anbn** — a pushdown automaton with a stack accepting `aⁿbⁿ` — verify accept/reject.
  (co-20)
- **ex-39 · anbn-not-regular** — show `aⁿbⁿ` cannot be a DFA (pumping-lemma intuition) — verify the
  counterexample string breaks any fixed-state machine. (co-20, co-21)
- **ex-40 · chomsky-hierarchy-map** — classify sample languages into the four levels — verify each against
  its matching automaton. (co-21)

### Advanced

- **ex-41 · turing-machine-increment** — a TM simulator incrementing a binary number on tape — verify the
  final tape. (co-22)
- **ex-42 · tm-unary-add** — a TM adding two unary numbers — verify the tape result equals the sum.
  (co-22)
- **ex-43 · halting-diagonalization** — code the diagonalization contradiction sketch for the halting
  problem — verify the self-reference contradiction. (co-23)
- **ex-44 · busy-beaver-intuition** — a small TM whose halting is hard to predict — verify it halts (or
  not) only by running it. (co-23)
- **ex-45 · p-class-sorting** — poly-time sorting as a P problem — verify O(n log n) scaling on growing
  inputs. (co-24)
- **ex-46 · np-verify-subset-sum** — verify a subset-sum certificate in poly time — verify the checker
  accepts a valid witness and rejects an invalid one. (co-24)
- **ex-47 · sat-brute-force** — brute-force a 3-SAT instance, exponential blowup — verify runtime grows
  ~2ⁿ with variable count. (co-25)
- **ex-48 · reduction-3sat-to-clique** — reduce a 3-SAT instance to a clique instance — verify the mapping
  preserves satisfiability. (co-25)
- **ex-49 · tsp-factorial-demo** — brute-force TSP with factorial growth — verify the tour count `== (n-1)!`.
  (co-24, co-25)
- **ex-50 · shannon-entropy-coin** — compute the entropy of a biased coin — verify H(0.5)=1 bit,
  H(0.9)<0.5 bit. (co-26)
- **ex-51 · entropy-english-text** — estimate per-character entropy of sample text — verify it lands near
  4 bits/char. (co-26)
- **ex-52 · huffman-lossless** — build Huffman codes, compress then decompress — verify exact
  reconstruction and a size reduction. (co-27)
- **ex-53 · lossy-vs-lossless** — contrast quantization (lossy) with `zlib` (lossless) — verify only the
  lossless path reconstructs the input exactly. (co-27)
- **ex-54 · crc32-corruption-detect** — compute CRC32, flip one bit, recompute — verify the checksum
  mismatch flags the corruption. (co-28)
- **ex-55 · sha256-avalanche** — hash two near-identical inputs — verify ~50% of digest bits differ.
  (co-28)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a small "CS foundations toolkit" in Python — a base/representation converter (incl. an
  IEEE-754 float inspector), a finite-automaton simulator that accepts/rejects strings for a given
  language, and a stack-frame + cache-traversal timing demo — each output explained against the theory.
- **Concepts exercised**: [ ] two's-complement + IEEE-754 representation (co-02, co-03) [ ] a regex→FA
  mapping run by a simulator (co-18, co-19) [ ] call-stack tracing (co-17) [ ] cache-friendly vs hostile
  access timing (co-16).
- **Ordered steps**:
  1. `.../learning/capstone/code/represent.py` — int/float ↔ binary/hex converter + float-bit inspector.
     Verify it prints the exact bit pattern for a known value and demonstrates `0.1+0.2 != 0.3`.
  2. `automaton.py` — an FA simulator; feed it accept/reject strings for one regular language. Verify each
     string is classified correctly against a hand-traced expectation.
  3. `memory.py` — time row-major vs column-major traversal of a 2-D array. Verify the cache-friendly order
     is measurably faster and explain why.
- **Acceptance criteria**: each tool runs from the CLI with the documented output; the FA matches the
  hand trace; the timing demo shows the expected ordering; every result is tied back to the theory.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Structure and Interpretation of Computer Programs** — Abelson, Sussman, Sussman (2nd ed., 1996). MIT's "Wizard Book": abstraction, recursion, the nature of computation via Scheme. <https://web.mit.edu/6.001/6.037/sicp.pdf>
- **Introduction to the Theory of Computation** — Michael Sipser (3rd ed., 2012). Standard text on automata, computability, complexity (incl. P vs NP).
- **Introduction to Algorithms (CLRS)** — Cormen, Leiserson, Rivest, Stein (4th ed., 2022). Definitive algorithms textbook and reference.
- **The Art of Computer Programming (Vols. 1–4B)** — Donald E. Knuth (1968–2022, ongoing). Reference-grade treatment of algorithms and their analysis.

**Papers & articles**

- **"On Computable Numbers, with an Application to the Entscheidungsproblem"** — Alan Turing (1936). Defines the Turing machine, founding modern computation theory. <https://www.cs.ox.ac.uk/activities/ieg/e-library/sources/tp2-ie.pdf>

---

← Previous: [18 · Technical Communication](./18-technical-communication.md) · Next: [20 · Computer Architecture](./20-computer-architecture.md) →
