---
title: "Overview"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 1
---

This page is the spaced-repetition companion to the Computer Science Foundations topic: recall
first, then applied judgment, then hands-on katas, then a checklist to confirm real automaticity.
Every answer is hidden in a `<details>` block; try each item yourself before opening it.

Every kata below is self-contained and deterministic -- mocked/hand-constructed inputs only, no live
network, no external service, and no dependency on this topic's own worked-example code. Where a
kata touches timing (cache-locality, the memory hierarchy), it checks a **relative** comparison
(row-major faster than column-major) rather than asserting a specific number, since wall-clock
numbers vary run to run and machine to machine.

## Recall Q&A

Twenty-eight short-answer questions, one per concept (`co-01` through `co-28`). Answer from memory,
then check.

**Q1 (co-01 -- positional number systems).** Why does converting a decimal integer to binary via
repeated division by 2 work, and what do the remainders represent?

<details>
<summary>Answer</summary>

A positional system's digit value depends on its place-value power of the base. Repeatedly dividing
by 2 peels off the least-significant bit as each step's remainder; reading the remainders from last
to first reconstructs the number's binary digits from most- to least-significant.

</details>

**Q2 (co-02 -- two's complement).** What single identity defines two's complement, and why does it
let one adder circuit handle both addition and subtraction?

<details>
<summary>Answer</summary>

`complement(n) + |n| == 2**bits`. Because a negative number's two's-complement encoding is designed
so that adding it to a positive number's encoding, with any overflow past the word width discarded,
produces the mathematically correct result -- subtraction becomes "add the negation," with no
separate subtract circuit needed.

</details>

**Q3 (co-03 -- IEEE-754 floats).** Why does `0.1 + 0.2 != 0.3` in almost every programming language,
and is it a bug?

<details>
<summary>Answer</summary>

Not a bug -- it's structural. Neither `0.1` nor `0.2` (nor `0.3`) has an exact binary64
representation, so each literal is already rounded to the nearest representable value the moment
it's parsed, before any arithmetic runs; the sum of the two roundings doesn't land exactly on the
rounding of `0.3`.

</details>

**Q4 (co-04 -- endianness).** What's the difference between little-endian and big-endian byte order,
and why does it matter when reading a binary file format?

<details>
<summary>Answer</summary>

Little-endian stores the least-significant byte first; big-endian stores the most-significant byte
first. Reading a multi-byte value with the wrong assumed order produces a different, still
plausible-looking number instead of an error -- so the format's specified byte order must be known,
not assumed.

</details>

**Q5 (co-05 -- Unicode and UTF-8).** Why can `len(s)` and `len(s.encode('utf-8'))` disagree for the
same string?

<details>
<summary>Answer</summary>

`len(s)` counts Unicode code points; `len(s.encode('utf-8'))` counts the actual UTF-8 storage bytes.
UTF-8 is variable-width -- ASCII code points cost 1 byte, but many non-ASCII characters cost 2, 3, or
4 bytes -- so the two counts diverge for any string containing non-ASCII characters.

</details>

**Q6 (co-06 -- boolean algebra).** State De Morgan's law for `not (a and b)`, and explain why NAND
alone is functionally complete.

<details>
<summary>Answer</summary>

`not (a and b) == (not a) or (not b)`. NAND is functionally complete because AND, OR, and NOT can
each be constructed purely from repeated NAND applications (`NOT(a) = NAND(a, a)`, and the rest
follow from De Morgan's law applied through NAND) -- so a chip fabricator only needs to perfect one
gate.

</details>

**Q7 (co-07 -- truth tables and gates).** What are a half-adder's two outputs, and which boolean
gates compute each one?

<details>
<summary>Answer</summary>

The sum bit, computed by XOR, and the carry-out bit, computed by AND. `1 + 1` produces sum=0,
carry=1 -- exactly binary `10`.

</details>

**Q8 (co-08 -- combinational vs. sequential).** What's the defining difference between a
combinational circuit and a sequential one?

<details>
<summary>Answer</summary>

A combinational circuit's output depends only on its current inputs. A sequential circuit's output
also depends on stored state from previous inputs -- it has memory a combinational circuit lacks.

</details>

**Q9 (co-09 -- sets and relations).** What three properties classify a relation, and give an example
of a relation that has exactly two of the three?

<details>
<summary>Answer</summary>

Reflexive, symmetric, transitive. "Divides" on a set of positive integers is reflexive (n divides n)
and transitive (a|b and b|c implies a|c) but not symmetric (1 divides 2, but 2 does not divide 1).

</details>

**Q10 (co-10 -- propositional logic).** When is the material implication `p -> q` false, and only
then?

<details>
<summary>Answer</summary>

Only when `p` is true and `q` is false. All three other combinations (including `p` false, `q`
false -- "vacuously true") make the implication true.

</details>

**Q11 (co-11 -- predicate logic).** What do the universal (forall) and existential (exists)
quantifiers correspond to in Python, and which one short-circuits on the first counterexample?

<details>
<summary>Answer</summary>

`all()` implements forall (short-circuits on the first `False`); `any()` implements exists
(short-circuits on the first `True`). Both quantify a predicate over a domain rather than a single
fixed statement.

</details>

**Q12 (co-12 -- combinatorics).** What formula counts `nPr` (ordered selections), and roughly how
many people does it take before a shared-birthday probability exceeds 50%?

<details>
<summary>Answer</summary>

`n! / (n-r)!`. 23 people -- the classic birthday-paradox threshold, because the number of _pairs_ to
compare grows quadratically with group size even though the group itself grows linearly.

</details>

**Q13 (co-13 -- graph theory).** What's a vertex's degree in an adjacency-list representation, and
what DFS-coloring rule detects a cycle in a directed graph?

<details>
<summary>Answer</summary>

The length of its neighbor list. A cycle exists iff DFS finds a "back-edge" -- an edge to a vertex
that is currently gray (on the active recursion path), not yet fully black (finished).

</details>

**Q14 (co-14 -- induction).** What are the two required parts of a proof by induction?

<details>
<summary>Answer</summary>

A base case (the smallest instance holds directly) and an inductive step (assuming it holds for `k`,
prove it must also hold for `k+1`). Together they cover every natural number without checking each
one individually.

</details>

**Q15 (co-15 -- CPU registers and the ALU).** What three phases repeat for every CPU instruction,
and what two status flags does a real ALU add operation typically expose?

<details>
<summary>Answer</summary>

Fetch, decode, execute. Zero flag (result is exactly zero) and carry flag (the unwrapped sum
overflowed the register's fixed width) -- both readable by conditional-branch instructions.

</details>

**Q16 (co-16 -- the memory hierarchy).** Roughly how does register latency compare to RAM latency,
and to disk latency, and why does row-major traversal of a 2-D array typically beat column-major?

<details>
<summary>Answer</summary>

RAM is roughly ~100x slower than a register/L1-cache access; disk is roughly ~10,000,000x slower
than a register access. Row-major traversal walks memory in the same order it's physically stored
(stride 1), keeping the CPU's cache-line prefetcher useful; column-major traversal jumps a full row's
width between consecutive accesses (stride N), landing in a different cache line almost every step.

</details>

**Q17 (co-17 -- the stack and heap).** Why can a heap-allocated object (like a list a function
builds and returns) outlive the stack frame that created it, while a plain local variable cannot?

<details>
<summary>Answer</summary>

A stack frame's own automatic storage (its local names) is reclaimed the instant the frame pops. A
heap object's _storage_ is independent of any one frame's lifetime -- as long as some live reference
to it exists (e.g. returned to the caller), the object persists after the frame that created it is
gone.

</details>

**Q18 (co-18 -- finite automata).** What five components formally define a DFA, and what's the
single difference that makes an NFA "nondeterministic"?

<details>
<summary>Answer</summary>

States, alphabet, transition function, start state, accepting states -- `(Q, Sigma, delta, q0, F)`.
An NFA can be in multiple live states simultaneously (and may have epsilon-moves consuming no input),
whereas a DFA always has exactly one current state.

</details>

**Q19 (co-19 -- regex-FA equivalence).** What does Kleene's theorem guarantee about a regular
expression and a finite automaton for the same language?

<details>
<summary>Answer</summary>

Every regular expression has an equivalent finite automaton that accepts exactly the same language,
and vice versa -- so a regex and a hand-built DFA for the same language must classify every possible
input string identically.

</details>

**Q20 (co-20 -- CFGs and pushdown automata).** What single extra piece of memory does a pushdown
automaton add over a finite automaton, and why does `a^n b^n` need it?

<details>
<summary>Answer</summary>

One stack. `a^n b^n` requires counting an unbounded number of `a`s before checking the same count of
`b`s follow -- a fixed-state machine has no way to remember an unbounded count, but a stack can push
one marker per `a` and pop one per `b`, accepting iff the stack empties exactly when the input ends.

</details>

**Q21 (co-21 -- the Chomsky hierarchy).** Name the four Chomsky-hierarchy levels from most to least
restrictive, and how do they nest?

<details>
<summary>Answer</summary>

Regular, context-free, context-sensitive, recursively-enumerable. Each level strictly contains the
one before it -- every regular language is context-free, every context-free language is
context-sensitive, and so on, but not the reverse.

</details>

**Q22 (co-22 -- Turing machines).** What three actions does a Turing machine take on every step, and
what makes its tape different from a DFA's input?

<details>
<summary>Answer</summary>

Read the current cell, write a symbol, move the head left or right, then transition state. Unlike a
DFA's read-only, left-to-right-only input, a Turing machine's tape is unbounded and can be written to
and revisited, which is exactly what gives it more computational power than a finite automaton.

</details>

**Q23 (co-23 -- the halting problem).** Sketch the diagonalization argument that proves no algorithm
can decide, for every program and input, whether that program halts.

<details>
<summary>Answer</summary>

Suppose a halting oracle `H(P, I)` exists. Define `D(P)`: "if `H(P, P)` says P halts, loop forever;
otherwise halt." Applying `D` to itself (`P := D`) means whichever answer `H(D, D)` gives, `D`'s own
definition guarantees the opposite actually happens -- a contradiction, so no such `H` can exist.

</details>

**Q24 (co-24 -- P vs. NP).** What is P, what is NP, and what's the key difference in what each class
promises is fast?

<details>
<summary>Answer</summary>

P is problems _solvable_ in polynomial time. NP is problems whose proposed solution can be _verified_
in polynomial time, even if finding one is believed to require far more (possibly exponential) time
in the worst case.

</details>

**Q25 (co-25 -- NP-completeness and reductions).** What does a polynomial-time reduction from problem
A to problem B prove, and why does that make every NP-complete problem "connected"?

<details>
<summary>Answer</summary>

That B is at least as hard as A -- if you could solve B quickly, you could solve A quickly too, by
reducing first. Every NP-complete problem reduces to every other one this way, so a fast algorithm
for any single NP-complete problem would yield a fast algorithm for all of them.

</details>

**Q26 (co-26 -- Shannon entropy).** What's the entropy of a fair coin, in bits, and why is a heavily
biased coin's entropy lower?

<details>
<summary>Answer</summary>

Exactly 1 bit -- the maximum possible for a two-outcome distribution. A biased coin is more
predictable (less "surprising" on average), and Shannon entropy directly measures average surprise,
so a more-predictable distribution has strictly lower entropy.

</details>

**Q27 (co-27 -- lossless and lossy compression).** What's the difference between lossless and lossy
compression, and which one is Huffman coding?

<details>
<summary>Answer</summary>

Lossless compression discards no information -- decompression exactly reconstructs the original.
Lossy compression permanently discards some information for a smaller size. Huffman coding is
lossless: it assigns shorter bit-codes to more frequent symbols, but decoding recovers the exact
original.

</details>

**Q28 (co-28 -- checksums and hashing).** What's the "avalanche effect" a cryptographic hash like
SHA-256 should exhibit, and why is CRC32 unsuitable for security purposes despite catching
corruption well?

<details>
<summary>Answer</summary>

Changing even a single input bit should flip roughly half of the output digest's bits, with no
discernible pattern. CRC32 reliably flags accidental corruption but is trivial to deliberately
construct a different message with a matching checksum, so it provides no security guarantee against
an adversary.

</details>

## Applied problems

Fourteen scenarios spanning representation through complexity and information theory. Each describes
a realistic situation without naming the specific concept -- decide what applies and why, then check
your reasoning against the worked solution. Every scenario below is invented for this drill and does
not reuse any function, fixture, or domain from the 55 worked examples.

**AP1.** A billing service stores a running total in a plain Python `float` and, after summing
thousands of small transaction amounts, notices the total is off by a fraction of a cent from an
independently computed sum. The developer suspects a bug in the summation loop. What's actually
going on, and what's the general-purpose fix?

<details>
<summary>Worked solution</summary>

This is IEEE-754 rounding error (co-03), not a summation-loop bug -- most decimal fractions (including
ordinary currency amounts like `0.10`) have no exact binary64 representation, and rounding error
accumulates across many additions. The fix is to represent money as integer cents (or use `Decimal`
for exact decimal arithmetic) rather than accumulating fractional dollar amounts in a binary float.

</details>

**AP2.** A network protocol parser reads a 4-byte integer field from an incoming packet using
`struct.unpack("<i", data)` and gets a wildly wrong value, even though the bytes themselves look
correct in a hex dump. The protocol's specification says fields are big-endian. What's wrong?

<details>
<summary>Worked solution</summary>

An endianness mismatch (co-04) -- `"<i"` unpacks assuming little-endian byte order, but the protocol
specifies big-endian. The same 4 bytes interpreted in the wrong order produce a different, still
plausible-looking integer instead of an error. The fix is `struct.unpack(">i", data)`, matching the
protocol's specified order.

</details>

**AP3.** A support system enforces a 280-character limit on ticket titles by checking
`len(title) <= 280` before saving, then later truncates the stored UTF-8 bytes to a 280-byte database
column. A user whose title is entirely emoji and CJK characters reports their title arrives corrupted
(cut off mid-character) even though it passed the length check. What happened?

<details>
<summary>Worked solution</summary>

`len(title)` counts Unicode code points, but the database column truncates by UTF-8 _bytes_ (co-05).
Many CJK characters and emoji cost 3-4 bytes each in UTF-8, so a 280-code-point title can easily
exceed 280 bytes, and byte-level truncation can cut a multi-byte character in half, producing invalid
UTF-8. The fix is to size the check and the storage limit consistently -- both in bytes, or truncate
on a code-point boundary, never mixing the two units.

</details>

**AP4.** A junior engineer proposes adding a dedicated "subtract" instruction to a toy CPU design,
arguing "otherwise how would it do subtraction?" A senior engineer says it's unnecessary. What's the
senior engineer's reasoning?

<details>
<summary>Worked solution</summary>

Two's complement (co-02) makes subtraction "add the negation" -- negating an operand (invert its bits,
add 1) and feeding it into the same adder circuit used for ordinary addition produces the correct
subtraction result, with any overflow past the word width simply discarded. No separate subtract
circuit is needed.

</details>

**AP5.** A logic-simplification tool flags `not (is_premium and has_valid_card)` as "hard to read"
and suggests `(not is_premium) or (not has_valid_card)` instead. A reviewer asks whether the rewrite
is actually equivalent. How would you settle it, and is it equivalent?

<details>
<summary>Worked solution</summary>

Yes -- this is De Morgan's law (co-06), and because both sides are boolean functions over a finite
(2-variable) domain, checking all 4 input combinations exhaustively is a complete proof of
equivalence, not a sample. `not (a and b) == (not a) or (not b)` holds unconditionally.

</details>

**AP6.** A hardware description for a small ALU is reviewed, and a colleague points out the "add"
module has no memory elements at all -- its Verilog is a pure combinational block. Another colleague
worries this means the ALU "can't remember its last result." Is that a real concern?

<details>
<summary>Worked solution</summary>

No -- and the confusion is exactly the combinational-vs-sequential distinction (co-08). A pure
combinational adder's output depends only on its CURRENT inputs; it's not supposed to remember
anything. If the system needs to remember a previous result, that's the job of a separate register
(sequential element) that latches the adder's output on a clock edge -- not something the adder
itself should do.

</details>

**AP7.** A permissions system models "user X can access resource Y" as a relation. A security
reviewer wants to know whether it's safe to assume "if X can access Y and Y can access Z, then X can
access Z" without checking the actual data. What should the reviewer check first?

<details>
<summary>Worked solution</summary>

Whether the relation is actually transitive (co-09) -- that assumption is exactly the definition of
transitivity, and it does not hold for every relation just because it sounds intuitive (e.g.
"reports to" is often NOT transitive -- your manager's manager doesn't necessarily manage you the same
way). The reviewer must verify transitivity against the actual access-control semantics, not assume
it.

</details>

**AP8.** A dependency-resolution tool needs to detect circular package dependencies (A depends on B,
B depends on C, C depends on A) before installing anything. What general algorithmic approach solves
this, and what's the exact condition that flags a cycle?

<details>
<summary>Worked solution</summary>

Model packages and their dependencies as a directed graph (co-13) and run DFS with white/gray/black
coloring. A cycle exists iff DFS ever finds an edge to a gray vertex -- one that is currently on the
active recursion path, not yet fully finished (black). That back-edge is both necessary and
sufficient evidence of a cycle.

</details>

**AP9.** A performance-sensitive image-processing routine iterates over a large 2-D pixel buffer
column by column because "that's how the output needs to be written." A profiler shows this loop is
the single slowest part of the pipeline, despite doing the same number of arithmetic operations as a
row-by-row version would. What's the likely cause, and what's a possible fix?

<details>
<summary>Worked solution</summary>

Cache-unfriendly access pattern (co-16) -- if the buffer is stored row-major (the common default),
column-by-column traversal has stride N between consecutive accesses, landing in a different cache
line almost every step, while row-by-row traversal has stride 1, matching the CPU's cache-line
prefetcher. A fix is to either restructure the loop to traverse in storage order and transpose only
once at the boundary, or store the buffer in the traversal-friendly layout to begin with.

</details>

**AP10.** A recursive function that walks a deeply nested JSON structure crashes in production on a
particular customer's data with `RecursionError: maximum recursion depth exceeded`, even though the
same code handles every other customer's data fine. Is this a bug, and what are two general fixes?

<details>
<summary>Worked solution</summary>

It's an expected consequence of a finite call stack (co-17), triggered by unusually deep nesting in
that one customer's data, not necessarily a logic bug. Two general fixes: convert the recursive walk
to an explicit iterative one using your own stack data structure (removing the call-stack depth
limit entirely), or, if recursion must be kept, raise `sys.setrecursionlimit()` cautiously while
being aware that doing so trades safety margin for depth.

</details>

**AP11.** A code reviewer asks whether a proposed regex `^(foo|bar)+$` for validating a config
field could instead be implemented as a hand-written state machine, for a slight performance gain in
a hot path. Is that guaranteed to be possible in principle?

<details>
<summary>Worked solution</summary>

Yes, in principle, by Kleene's theorem (co-19) -- any regular expression has an equivalent finite
automaton accepting the exact same language, so a hand-built DFA for `(foo|bar)+` is guaranteed to
exist and can be constructed to classify every input identically to the regex.

</details>

**AP12.** A parser-generator's documentation claims their tool "can parse any language you can
describe with a regular expression, but not necessarily one requiring matched, arbitrarily-nested
delimiters." A new team member is confused why nested delimiters would be a special case. What's the
underlying reason?

<details>
<summary>Worked solution</summary>

Matched, arbitrarily-deep nested delimiters (like balanced parentheses) require counting an unbounded
depth, which needs a stack -- exactly the co-20 pushdown-automaton / context-free distinction from
regular languages (co-18/co-19). A regex-based (finite-automaton) matcher has no stack and provably
cannot track unbounded nesting depth, which is why the tool needs a separate, more powerful
context-free grammar mechanism for that case.

</details>

**AP13.** A startup claims their new scheduling algorithm "solves the general job-shop scheduling
problem exactly, in all cases, in well under a second, no matter the input size" and is seeking
funding. A technical advisor is skeptical. What complexity-theory fact motivates that skepticism, and
what would change the advisor's mind?

<details>
<summary>Worked solution</summary>

Job-shop scheduling is a well-known NP-complete problem (co-24, co-25); no polynomial-time exact
algorithm is known for any NP-complete problem, and finding one would resolve the famous open P vs. NP
question. The advisor should ask for the actual algorithm and a worst-case complexity analysis (or a
large adversarial benchmark) rather than accepting the speed claim on faith -- either the claim doesn't
generalize to true worst-case instances, or it's a landmark result that needs far more scrutiny than a
funding pitch.

</details>

**AP14.** A team debates whether to use CRC32 or SHA-256 to verify that a downloaded software update
package hasn't been tampered with by an attacker in transit (as opposed to just corrupted by a flaky
network). Which is the right choice, and why does it matter here specifically?

<details>
<summary>Worked solution</summary>

SHA-256 (co-28) -- CRC32 is fast and excellent at catching _accidental_ corruption, but it is
computationally trivial for an adversary to deliberately construct a different (malicious) file with
the same CRC32 checksum. SHA-256's avalanche property and cryptographic design make it computationally
infeasible to forge a matching digest for a different, adversary-chosen payload, which is exactly the
threat model tampering detection needs to defend against.

</details>

## Code katas

Nine self-contained exercises. Every kata runs on hand-constructed, in-memory data using only the
Python 3.13.12 standard library -- no live network, no external service, and no dependency on this
topic's own worked-example files, so every kata is runnable anywhere Python 3.13 is installed, with
nothing else to set up.

### Kata 1 -- Binary and two's-complement round-trip on five self-chosen values

Write `to_binary(n: int) -> str` (repeated division by 2) and `to_twos_complement(n: int, bits: int =
8) -> str`. Pick five values of your own choosing -- at least one 0, one positive value near 255, and
one negative value -- and confirm `to_binary` matches Python's own `bin()` for the non-negative ones,
and that `(to_twos_complement's unsigned value) + abs(n) == 2**bits` holds for the negative ones
(co-01, co-02).

### Kata 2 -- IEEE-754 bit inspector for three self-chosen floats

Using `struct.pack(">d", x)`, write a function that decodes any float into its sign/exponent/mantissa
fields. Run it against `1.0`, `-1.0`, and `2.0`, and confirm by hand that `2.0`'s unbiased exponent is
exactly one more than `1.0`'s (since `2.0 == 1.0 * 2**1`), and that `-1.0` differs from `1.0` only in
its sign bit (co-03).

### Kata 3 -- Endianness round-trip through both byte orders

Pick a 4-byte integer of your own choosing (something with at least 3 distinct nonzero bytes, e.g.
`0x01020304`). Pack it with `struct.pack("<i", ...)` and `struct.pack(">i", ...)`, confirm the two
byte sequences are reverses of each other, and confirm each one correctly decodes back to your
original integer using the SAME format string it was packed with (co-04).

### Kata 4 -- UTF-8 byte-length divergence on a string you construct

Build a string containing at least one ASCII character, one 2-byte UTF-8 character (e.g. an accented
Latin letter), and one 3-byte UTF-8 character (e.g. a CJK character) of your own choosing. Confirm
`len(s)` and `len(s.encode('utf-8'))` diverge, and identify by hand which specific character(s) account
for the difference (co-05).

### Kata 5 -- Build AND/OR/NOT from NAND alone, then verify against Python's builtins

Write `nand(a, b)`, then `not_from_nand`, `and_from_nand`, `or_from_nand`, using only `nand()` calls
(no `and`/`or`/`not` inside them). Exhaustively check all 4 input combinations against Python's own
`and`/`or`/`not` operators and confirm every one matches (co-06).

### Kata 6 -- A DFA for a language of your own choosing, cross-checked against a regex

Design a DFA for any regular language over `{0, 1}` you choose that is NOT one of this topic's worked
examples (e.g. "contains at least two 1s," or "length is a multiple of 3"). Implement it as a
transition-table-driven simulator, write an equivalent Python regex for the same language, and
confirm both agree on at least 10 test strings you construct yourself, including edge cases like the
empty string (co-18, co-19).

### Kata 7 -- A Turing machine that reverses a short binary string

Design (states, transitions) and implement a Turing machine that reverses a binary string of your
choosing (e.g. `"1101"` -> `"1011"`), using a tape-based read/write/move simulator in the same style
as this topic's increment and unary-addition machines. Confirm it correctly reverses at least three
strings of different lengths that you construct yourself (co-22).

### Kata 8 -- Cache-locality direction check without asserting a specific number

Build an `array.array('d', ...)` matrix of a size you choose (large enough that the effect is
measurable, e.g. 1000x1000 or larger), time a row-major full-sum traversal and a column-major
full-sum traversal with `time.perf_counter()`, and confirm ONLY that `row_major_time < col_major_time`
-- do not assert or hardcode any specific ratio or duration, since wall-clock numbers vary by machine
and by run (co-16).

### Kata 9 -- Huffman-encode a string of your own choosing and confirm exact round-trip

Pick any short string with a genuinely skewed letter frequency (at least one character appearing
noticeably more often than another). Build a Huffman tree, encode, and decode it, confirming the
decoded string exactly matches your original and that the encoded bit-length is strictly less than
`8 * len(your_string)` (co-27).

## Self-check checklist

Confirm each item without checking the learning track first. If you hesitate, that concept needs
another pass.

- [ ] I can explain why repeated division by the target base is the mechanical basis for converting
      between binary, octal, decimal, and hex. (co-01)
- [ ] I can explain the identity that defines two's complement and why it lets one adder circuit do
      both addition and subtraction. (co-02)
- [ ] I can explain why `0.1 + 0.2 != 0.3` is structural, not a bug, and name a fix for
      currency-sensitive arithmetic. (co-03)
- [ ] I can explain the difference between little-endian and big-endian byte order and why reading
      the wrong one produces a wrong-but-plausible value instead of an error. (co-04)
- [ ] I can explain why `len(s)` and `len(s.encode('utf-8'))` can diverge for the same string. (co-05)
- [ ] I can state De Morgan's law and explain why NAND alone is functionally complete. (co-06)
- [ ] I can name a half-adder's two outputs and which gate computes each one. (co-07)
- [ ] I can explain the defining difference between a combinational circuit and a sequential one.
      (co-08)
- [ ] I can name the three properties that classify a relation and give an example that has exactly
      two of the three. (co-09)
- [ ] I can state exactly when `p -> q` is false, and only then. (co-10)
- [ ] I can explain how `all()`/`any()` correspond to the forall/exists quantifiers, and which
      short-circuits on what. (co-11)
- [ ] I can state the `nPr` formula and explain why the birthday-paradox threshold (23 people) is
      lower than most people's intuition expects. (co-12)
- [ ] I can explain what a vertex's degree means in an adjacency list and the DFS-coloring rule that
      detects a cycle. (co-13)
- [ ] I can name the two required parts of a proof by induction. (co-14)
- [ ] I can name the three repeating phases of a CPU instruction cycle and two status flags a real
      ALU add operation exposes. (co-15)
- [ ] I can order register/L1/L2/RAM/SSD/disk from fastest to slowest and explain why row-major
      traversal usually beats column-major. (co-16)
- [ ] I can explain why a heap-allocated object can outlive the stack frame that created it, while a
      plain local variable cannot. (co-17)
- [ ] I can name the five components of a formal DFA definition and the one property that makes an
      NFA nondeterministic. (co-18)
- [ ] I can state what Kleene's theorem guarantees about a regex and a finite automaton for the same
      language. (co-19)
- [ ] I can explain what a pushdown automaton adds over a finite automaton and why `a^n b^n` needs
      it. (co-20)
- [ ] I can name the four Chomsky-hierarchy levels in nesting order, from most to least restrictive.
      (co-21)
- [ ] I can name the three actions a Turing machine takes on every step and what makes its tape more
      powerful than a DFA's input. (co-22)
- [ ] I can sketch the diagonalization argument that proves the halting problem is undecidable.
      (co-23)
- [ ] I can state the difference between P and NP in terms of solving versus verifying. (co-24)
- [ ] I can explain what a polynomial-time reduction from problem A to problem B proves about their
      relative difficulty. (co-25)
- [ ] I can state the entropy of a fair coin in bits and explain why a biased coin's entropy is
      lower. (co-26)
- [ ] I can explain the difference between lossless and lossy compression and which one Huffman
      coding is. (co-27)
- [ ] I can explain the avalanche effect a cryptographic hash should exhibit and why CRC32 is
      unsuitable for security purposes despite catching corruption well. (co-28)

---

← Previous: [Capstone](../learning/capstone/overview.md)
