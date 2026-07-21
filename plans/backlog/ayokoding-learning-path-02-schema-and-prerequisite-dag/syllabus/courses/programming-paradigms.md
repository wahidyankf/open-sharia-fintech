# Programming Paradigms (By Example, Python)

**Course ID**: `programming-paradigms` · **Format**: By Example · **Language**: Python.

**Short summary**: Imperative, functional, logic, declarative survey

**Scope note**: a **survey** of the major paradigms and how to choose among them, anchored in Python
(`**`) with other languages shown illustratively. Functional programming has its own deep topic
([`23-functional-programming`](./functional-programming.md)); the concurrency-oriented paradigms deepen
in Pass 4 (CSP → Go, actor → Elixir). This topic's job is fluency in _matching paradigm to problem_.

## Why this exists · the big idea

- **The problem before the solution**: most engineers default to one paradigm and bend every problem to
  it — the wrong paradigm makes easy problems hard and hides the shape the problem actually has.
- **Keep-this-if-you-forget-everything**: a paradigm is a set of _constraints that buy a property_ (purity
  buys reasoning, objects buy encapsulation, logic buys search) — match the problem's grain, don't fight it.
- **Big ideas touched**: `abstraction-and-its-cost` (each paradigm is a lens with a bill attached),
  `taming-state` (paradigms differ most in how they treat mutable state — this is the real fault line).

## Prerequisites

- **Prior topics**: [topic 4 Just Enough Python](./just-enough-python.md),
  [topic 8 Object-Oriented Programming Essentials](./object-oriented-programming-essentials.md) (the OO
  paradigm), and [topic 21 Object-Oriented Design & Patterns](./object-oriented-design-and-patterns.md);
  functional style is cross-referenced forward to [topic 23](./functional-programming.md).
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x** (all runnable examples); illustrative
  snippets in other languages are read-only (no extra toolchain required to follow).
- **Assumed knowledge**: comfortable writing Python in both procedural and OO styles; can read a small
  snippet in an unfamiliar language with explanation.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: the paradigm taxonomy (imperative/procedural, OO, functional, logic,
  event-driven/reactive, dataflow) is a stable decades-old classification with no material redefinition.
  Any illustrative non-Python snippet must be re-checked against current language versions once actually
  authored (none exist in this pre-authoring file yet). (general CS canon)
- 2026-07-12 — verified: `match`/`case` structural pattern matching is Python 3.10+ (PEP 634); it is the
  current idiomatic declarative-dispatch mechanism and is used in several examples below. State tags use a
  plain `enum.Enum` (not `StrEnum`, 3.11) so examples run on 3.10. All runnable examples are stdlib-only —
  the logic-programming and constraint examples are hand-rolled (no `kanren`/`python-constraint`) and the
  reactive/dataflow examples are hand-rolled (no `RxPY`) — so no third-party paradigm library is required.
  (docs.python.org / PEP 634)

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · imperative-programming** — computation as explicit statements that change state step by step.
- **co-02 · procedural-abstraction** — grouping steps into named, reusable procedures/functions.
- **co-03 · structured-programming** — sequence, selection, and iteration replacing arbitrary `goto` jumps.
- **co-04 · mutable-state-and-assignment** — variables as boxes that assignment rebinds; the imperative core.
- **co-05 · object-oriented-paradigm** — bundling state and the behavior that acts on it into objects.
- **co-06 · encapsulation-as-state-containment** — objects localize mutable state behind an interface.
- **co-07 · message-passing-vs-method-call** — OO's conceptual model of objects sending each other messages.
- **co-08 · declarative-vs-imperative** — describing _what_ result is wanted vs _how_ to compute it.
- **co-09 · functional-paradigm-overview** — pure functions and immutability as a paradigm (deep-dived in topic 23).
- **co-10 · expressions-vs-statements** — functional/declarative styles lean on value-producing expressions.
- **co-11 · pure-vs-impure** — the side-effect boundary that separates reasoning-friendly code from I/O.
- **co-12 · first-class-and-higher-order-functions** — functions as ordinary values passed and returned.
- **co-13 · logic-programming** — facts plus rules plus a query the engine resolves by search.
- **co-14 · unification-and-backtracking** — the matching-and-retry mechanics under a logic engine.
- **co-15 · constraint-programming** — declare constraints and let a solver search the feasible space.
- **co-16 · event-driven-paradigm** — handlers respond to events; the framework calls you (inversion of control).
- **co-17 · reactive-programming** — model data as streams and propagate change automatically to dependents.
- **co-18 · dataflow-programming** — computation as a graph of value dependencies recomputed on change.
- **co-19 · relational-set-based-thinking** — SQL/relational algebra as a declarative, set-oriented paradigm.
- **co-20 · multi-paradigm-languages** — languages (Python, Scala) that blend several paradigms deliberately.
- **co-21 · paradigm-as-constraint-buys-property** — each paradigm trades a constraint for a guarantee.
- **co-22 · state-as-the-fault-line** — paradigms differ most in how they treat mutable shared state.
- **co-23 · matching-paradigm-to-problem** — choosing the paradigm whose grain fits the problem's shape.
- **co-24 · paradigm-cost-and-tradeoff** — every lens has a bill: readability, testability, change-cost.
- **co-25 · mixing-paradigms-at-boundaries** — choose one paradigm per boundary, not freely per line.

## Tensions & trade-offs — when NOT to reach for this

- **No paradigm is universal**: functional purity shines for transformation and logic but fights hardware
  and I/O; OO models entities well but drowns a simple script in ceremony; logic/constraint programming is
  magic for search and dead weight everywhere else. Loyalty to one paradigm is the failure mode.
- **Multi-paradigm is not paradigm soup**: mixing freely _inside_ one boundary — mutable OO objects threaded
  through a nominally "functional" pipeline — collects the costs of both and the benefits of neither. Choose a
  paradigm per boundary, not per line.
- **When NOT to care**: for a 50-line script the paradigm question is noise; reach for whatever is fastest to
  write. Paradigm choice earns its weight only once a system is big enough to have a dominant axis of change.

## Lineage — why it beat the alternative

- Each paradigm is a historical reaction to a specific pain the prior one couldn't hold. Structured programming
  (Dijkstra, "Go To Considered Harmful", 1968) beat goto-spaghetti by constraining control flow; OO
  (Simula/Smalltalk) rose to tame large mutable-state systems by bundling state with behavior; functional
  (Lisp → ML → Haskell) answered the reasoning-and-concurrency crisis by removing shared mutable state;
  reactive/dataflow answered UIs and streams. So the durable skill is not allegiance to one paradigm but
  reading _which pain a problem has_ — a judgment that feeds straight into
  [`23-functional-programming`](./functional-programming.md) and the concurrency paradigms of Pass 4
  ([`65-csp-style-concurrency`](./csp-style-concurrency.md), [`67-actor-model-concurrency`](./actor-model-concurrency.md)).

## Worked examples

Colocated under `programming-paradigms/learning/code/`; the same problem is frequently solved multiple
ways for direct contrast (DD-20/DD-30). Contiguous `ex-01..ex-80`. Every example cites the `co-NN` it
exercises; every concept above is exercised by ≥1 example.

### Beginner

- **ex-01 · imperative-word-count** — count word frequencies with an explicit loop mutating a `dict` — verify counts match a known text. (co-01, co-04)
- **ex-02 · procedural-decompose** — refactor that loop into named procedures (`tokenize`, `tally`) — verify identical output, smaller `main`. (co-02)
- **ex-03 · structured-three-constructs** — rewrite a flag-and-jump routine using only sequence/selection/iteration — verify no boolean "goto flag" remains. (co-03)
- **ex-04 · mutable-variable-box** — reassign a variable then alias a list and mutate the alias — verify the original sees the change (shared box). (co-04)
- **ex-05 · goto-free-loop** — replace a `while True` + `break` state-hack with a clean `for` — verify equivalent output. (co-03)
- **ex-06 · oo-word-count** — a `WordCounter` class holding tally state, `add`/`result` methods — verify count via the method. (co-05, co-06)
- **ex-07 · encapsulation-private-state** — hide the counter behind `_tally` + a read method, assert callers can't corrupt the invariant — verify invariant held. (co-06)
- **ex-08 · method-call-as-message** — a `Duck`/`Dog` pair answering `speak()` polymorphically — verify dispatch picks the right message. (co-07)
- **ex-09 · declarative-comprehension** — express filter+map as a list comprehension vs an imperative loop — verify identical list. (co-08, co-10)
- **ex-10 · imperative-vs-declarative-sum** — sum of squares of evens both ways — verify same integer. (co-08)
- **ex-11 · functional-word-count** — word count via `collections.Counter` / `reduce`, no user-visible mutation — verify same counts. (co-09, co-11)
- **ex-12 · expression-vs-statement** — a value from a conditional expression vs from an `if`/assign block — verify both compute the same value. (co-10)
- **ex-13 · pure-vs-impure-pair** — a pure `normalize(text)` beside an impure `normalize_and_log` — verify the pure one is referentially transparent (call twice, same result, no output). (co-11)
- **ex-14 · higher-order-map** — pass a function into a `apply_all(fn, items)` helper — verify function-as-value transforms each item. (co-12)
- **ex-15 · sql-declarative-query** — "top-3 words" as a `sqlite3` `GROUP BY … ORDER BY … LIMIT` — verify rows match the functional version. (co-19, co-08)
- **ex-16 · event-driven-callback** — register a handler on a tiny dispatcher, then fire an event — verify the handler ran with the payload. (co-16)
- **ex-17 · reactive-counter** — a minimal observable value pushing updates to subscribers on `set` — verify a subscriber saw the new value. (co-17)
- **ex-18 · dataflow-two-cells** — cells `A` and `B=A+1` where writing `A` recomputes `B` — verify `B` updates. (co-18)
- **ex-19 · logic-family-facts** — encode `parent` facts + a `grandparent` rule, then query — verify the grandparent is inferred, not stored. (co-13)
- **ex-20 · multi-paradigm-one-file** — one script mixing a class, a comprehension, and a generator — verify all three run and agree. (co-20)
- **ex-21 · constraint-buys-property** — a frozen `tuple`/`frozenset` shared across two functions — verify neither can mutate it (immutability buys safe sharing). (co-21)
- **ex-22 · state-fault-line-demo** — the same running total as a mutable global vs an immutable fold — verify both count, contrast where state lives. (co-22)
- **ex-23 · match-case-dispatch** — `match`/`case` dispatching on a command tag string — verify each branch fires (Python 3.10+, PEP 634). (co-08)
- **ex-24 · imperative-fizzbuzz** — classic imperative FizzBuzz with an accumulator loop — verify the 1..20 output. (co-01)
- **ex-25 · declarative-fizzbuzz** — FizzBuzz as a rules table mapped over the range — verify identical output to ex-24. (co-08)
- **ex-26 · structured-guard-clauses** — flatten a nested-`if` pyramid into early-return guards — verify same behavior, lower nesting. (co-03)
- **ex-27 · oo-vs-procedural-area** — shape area via a class hierarchy vs a function + tag `dict` — verify equal areas. (co-05, co-02)
- **ex-28 · paradigm-is-noise-tiny-script** — a 15-line one-off where paradigm choice doesn't matter, written the fastest way, with a comment saying why — verify it runs. (co-23, co-24)

### Intermediate

- **ex-29 · four-ways-imperative** — word-frequency, imperative version (loop + `dict`) — verify counts. (co-01)
- **ex-30 · four-ways-oo** — word-frequency, OO version (`Counter` class) — verify same counts. (co-05)
- **ex-31 · four-ways-functional** — word-frequency, functional version (`reduce`/`Counter`, no mutation) — verify same counts. (co-09)
- **ex-32 · four-ways-declarative** — word-frequency, declarative version (`sqlite3` or comprehension aggregation) — verify same counts across all four. (co-08, co-19)
- **ex-33 · state-machine-imperative** — a turnstile as an explicit `state` variable + transition `if`s — verify locked→unlocked→locked sequence. (co-01, co-04)
- **ex-34 · state-machine-oo** — the same turnstile via `State` objects (State pattern) — verify same sequence. (co-05)
- **ex-35 · state-machine-functional** — the turnstile as a pure `(state, event) -> state` fold — verify same sequence, no mutation. (co-09, co-11)
- **ex-36 · prolog-in-python** — a tiny unification + backtracking solver over `parent` facts — verify a `grandparent` query resolves via search. (co-13, co-14)
- **ex-37 · backtracking-n-queens** — solve N-queens (N=8) by backtracking — verify the board has no two queens attacking. (co-14)
- **ex-38 · constraint-map-coloring** — declare adjacency constraints, brute-force/backtrack a 3-coloring — verify no adjacent regions share a color. (co-15)
- **ex-39 · constraint-mini-sudoku** — a 4×4 sudoku solver from declared constraints — verify rows/cols/boxes valid. (co-15)
- **ex-40 · event-driven-loop** — a small event loop draining a queue to handlers — verify events processed in order. (co-16)
- **ex-41 · reactive-derived-value** — a computed signal `c = a + b` recomputing when either source changes — verify `c` after two updates. (co-17)
- **ex-42 · reactive-vs-manual-recompute** — contrast manual "remember to update" vs automatic reactive propagation — verify both consistent, one forgets on a new path. (co-17, co-08)
- **ex-43 · dataflow-topo-execute** — a DAG of transforms executed in topological order — verify order respects deps and the result. (co-18)
- **ex-44 · generator-pull-pipeline** — a pull-based generator pipeline (`map`→`filter`→`take`) — verify laziness (only pulled items computed). (co-18, co-10)
- **ex-45 · inversion-of-control** — you-call-library vs framework-calls-you, same task both ways — verify the handler is invoked by the framework. (co-16)
- **ex-46 · declarative-config-vs-setup** — build an object from a declared data spec vs imperative step-by-step setup — verify equal objects. (co-08)
- **ex-47 · relational-vs-nested-loop-join** — join two datasets via SQL vs a hand-written nested loop — verify identical rows. (co-19)
- **ex-48 · pure-core-imperative-shell** — split a task into a pure core + an imperative I/O shell — verify the core is tested with no I/O. (co-11, co-25)
- **ex-49 · multi-paradigm-boundary** — a functional pipeline feeding an OO service across a clean boundary — verify the boundary passes only immutable data. (co-20, co-25)
- **ex-50 · paradigm-soup-antipattern** — mutable objects threaded through a nominally "functional" pipeline, collecting both costs — verify the aliasing bug reproduces. (co-25)
- **ex-51 · logic-vs-imperative-reachability** — graph reachability via inference rules vs a BFS loop — verify identical reachable set. (co-13, co-01)
- **ex-52 · match-case-adt-dispatch** — `match`/`case` over a union of dataclasses (a sum type) — verify each variant handled. (co-08, co-09)
- **ex-53 · enum-state-tags** — model states with a plain `enum.Enum` and dispatch transitions on it — verify a full transition cycle. (co-04)
- **ex-54 · declarative-validation-rules** — a list of rule objects evaluated declaratively over an input — verify a bad input is flagged with the failing rule. (co-08)
- **ex-55 · event-bus-pubsub** — a typed publish/subscribe bus with multiple subscribers — verify all subscribers notified once each. (co-16, co-17)
- **ex-56 · reactive-debounce** — a stream operator collapsing a burst to the last value — verify only the final value is delivered. (co-17)
- **ex-57 · dataflow-memoized-nodes** — cache node outputs in a dataflow graph, dirty-tracking on change — verify an unchanged subtree isn't recomputed. (co-18)
- **ex-58 · paradigm-cost-table** — measure lines/branch-count/testability of the same task across paradigms — verify a comparison table with concrete numbers. (co-24, co-23)

### Advanced

- **ex-59 · four-paradigms-shared-test** — one problem solved imperative + OO + functional + declarative against a single shared test — verify all four pass it. (co-23, co-01, co-05, co-09, co-08)
- **ex-60 · mini-logic-engine** — a backtracking Prolog-ish engine with rules + queries — verify a transitive-closure query resolves. (co-13, co-14)
- **ex-61 · generic-csp-solver** — a generic constraint-satisfaction solver with propagation — verify it solves both map-coloring and mini-sudoku. (co-15)
- **ex-62 · reactive-graph-diamond** — a signals graph with automatic dependency tracking on a diamond (`d←b,c←a`) — verify `d` recomputes exactly once per `a` update. (co-17, co-18)
- **ex-63 · dataflow-scheduler** — a topological scheduler exposing parallel-ready batches — verify correct order under a dependency chain. (co-18)
- **ex-64 · event-sourcing-fold** — rebuild state by folding an append-only event log (functional + event-driven) — verify replay reproduces the live state. (co-09, co-16, co-22)
- **ex-65 · actor-mailbox** — a message-passing object with a mailbox queue processed one at a time — verify messages handled in arrival order. (co-07, co-16)
- **ex-66 · paradigm-decision-record** — a decision table mapping problem shapes to paradigms with reasoning — verify each row cites a concrete selection criterion. (co-23, co-24)
- **ex-67 · imperative-to-functional-refactor** — refactor a mutation-heavy routine into a pure fold — verify identical output and no mutation of inputs. (co-11, co-22)
- **ex-68 · oo-behind-functional-facade** — wrap an OO subsystem behind a pure functional interface — verify the facade exposes no mutable state. (co-20, co-25)
- **ex-69 · declarative-mini-dsl** — a tiny internal rule-builder DSL evaluated declaratively — verify a composed rule runs. (co-08)
- **ex-70 · logic-type-inference-toy** — express simple type rules as logic clauses and infer a term's type — verify the inferred type. (co-13)
- **ex-71 · constraint-scheduling** — schedule tasks under precedence + resource constraints — verify a returned schedule is feasible. (co-15)
- **ex-72 · reactive-spreadsheet** — a working mini-spreadsheet: formula cells + cascading recompute — verify a multi-level cascade updates. (co-17, co-18)
- **ex-73 · multi-paradigm-request-handler** — an event-driven handler with a functional core over an OO domain model — verify a request is handled end to end. (co-16, co-25, co-20)
- **ex-74 · state-fault-line-case-study** — the same feature designed shared-mutable vs immutable, run under two threads — verify a race in one design and none in the other. (co-22, co-21)
- **ex-75 · paradigm-mismatch-cost** — a search problem solved painfully imperative, then cleanly with constraints — verify both correct, contrast effort/lines. (co-24, co-15)
- **ex-76 · dataflow-vs-callback** — a pipeline expressed as generators (dataflow) vs nested callbacks (event) — verify identical output, contrast readability. (co-18, co-16)
- **ex-77 · relational-algebra-engine** — a tiny in-memory relational engine (select/project/join) over dicts — verify a composed query's result. (co-19)
- **ex-78 · paradigm-portfolio-readme** — assemble every paradigm solution with a comparison matrix — verify the matrix covers all solutions with a criterion each. (co-23, co-20)
- **ex-79 · immutable-vs-mutable-perf** — measure persistent immutable updates vs in-place mutation on the same workload — verify both correct, note the trade-off numerically. (co-21, co-24)
- **ex-80 · choose-and-defend** — pick the best-fit paradigm for a stated real problem and defend it in prose grounded in the code you wrote — verify the defense references concrete functions. (co-23, co-25)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: pick one non-trivial small problem and implement it in **four paradigms** (imperative, OO,
  functional, declarative/reactive) producing identical output, then write a decision record arguing which
  paradigm best fits the problem and why — a runnable, side-by-side paradigm comparison.
- **Concepts exercised**: [ ] imperative/procedural solution (co-01, co-02) [ ] OO solution (co-05, co-06)
  [ ] functional solution (co-09, co-11) [ ] declarative or reactive solution (co-08, co-17)
  [ ] a reasoned paradigm-selection decision grounded in trade-offs (co-23, co-24, co-25).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — define the problem + a shared test asserting the expected output.
     Verify the test exists and fails against empty implementations.
  2. Implement the imperative and OO versions. Verify both pass the shared test.
  3. Implement the functional and declarative/reactive versions. Verify both pass the shared test.
  4. `decision.md` — argue the best-fit paradigm with trade-offs (readability, testability, change-cost).
     Verify each claim references the concrete code.
- **Acceptance criteria**: all four implementations pass the identical test; the decision record is
  grounded in the code, not generic prose; trade-offs are concrete.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Structure and Interpretation of Computer Programs** — Harold Abelson & Gerald Jay Sussman (1985; 2nd ed. 1996). Canonical MIT text teaching procedural, functional, object-oriented, and logic paradigms through a single Lisp substrate. <https://mitp-content-server.mit.edu/books/content/sectbyfn/books_pres_0/6515/sicp.zip/full-text/book/book.html>
- **Concepts, Techniques, and Models of Computer Programming** — Peter Van Roy & Seif Haridi (2004). Comprehensive graduate text organizing all major paradigms by their underlying computational models. <https://webperso.info.ucl.ac.be/~pvr/VanRoyHaridi2003-book.pdf>
- **Seven Languages in Seven Weeks** — Bruce Tate (2010). Practical survey spanning imperative, object-oriented, functional, and logic paradigms across seven languages.

**Papers & articles**

- **Programming Paradigms for Dummies: What Every Programmer Should Know** — Peter Van Roy (2009). Widely cited taxonomy of roughly thirty paradigms and how they relate. <https://webperso.info.ucl.ac.be/~pvr/VanRoyChapter.pdf>
- **Can Programming Be Liberated from the von Neumann Style? A Functional Style and Its Algebra of Programs** — John Backus (1978). Backus's ACM Turing Award lecture critiquing imperative programming and motivating the functional paradigm. <https://dl.acm.org/doi/10.1145/359576.359579>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Theory & low-level systems — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · CS fundamentals, DS&A & algorithms — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 1 · CS theory & foundations (the university core, taught first).

> _Content originated in the now-closed FS-SE plan (topic 22); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
