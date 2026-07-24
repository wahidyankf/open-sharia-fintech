# Functional Programming (By Example, Python)

**Course ID**: `functional-programming` · **Format**: By Example · **Language**: Python.

**Short summary**: Pure functions, immutability, composition, HOFs

**Scope note**: functional programming as an everyday discipline in Python — purity, immutability,
higher-order functions, composition, and the algebraic error-handling patterns (`Option`/`Result`), plus
a **gentle, practical** first exposure to functors/monoids/monads as code patterns. The deeper,
law-checking treatment lives in [`88-type-systems`](./type-systems.md); the functional-core /
imperative-shell idea recurs across the whole curriculum.

## Why this exists · the big idea

- **The problem before the solution**: shared mutable state is the root of the hardest bugs — action at a
  distance, failures you can't reproduce, and a codebase you're afraid to change because nothing is local.
- **Keep-this-if-you-forget-everything**: push side effects to the edges and keep a pure core — code that
  only maps inputs to outputs is code you can test, reason about, and parallelize without fear.
- **Big ideas touched**: `taming-state` (the central move — quarantine state and effects), `determinism-vs-emergence`
  (purity buys deterministic, replayable behavior), `abstraction-and-its-cost` (immutability costs allocations).

## Prerequisites

- **Prior topics**: [topic 4 Just Enough Python](./just-enough-python.md) (functions, closures,
  comprehensions, generators); [topic 7 Data Structures & Algorithms Essentials](./data-structures-and-algorithms-essentials.md)
  for the data being transformed; contrasts against [topic 8 OOP](./object-oriented-programming-essentials.md).
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x** (`functools`, `itertools` from the
  stdlib); `pytest` for the purity/refactor examples.
- **Assumed knowledge**: writing Python functions and comprehensions; the idea of a side effect; basic
  generators/iterators.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: `functools.reduce`/`partial`/`lru_cache`, `itertools`, and generator/`yield`
  semantics (PEP 342/380) are stable unchanged stdlib APIs, no recent breaking changes. The gentle
  functor/monad framing is a pedagogical choice, not a hard fact — safe as long as content stays practical
  and avoids overclaiming category-theory rigor (file already scopes it correctly). (docs.python.org)
- 2026-07-12 — verified: `match`/`case` structural pattern matching is Python 3.10+ (PEP 634) and has **no
  compile-time exhaustiveness checking** — an unmatched value simply falls through; the rigorous exhaustive
  treatment is deferred to [`88-type-systems`](./type-systems.md). CPython has **no tail-call
  optimization** by design (Guido's stance) — deep recursion raises `RecursionError`; the advanced examples
  use an explicit stack or a trampoline. Immutability tools: `@dataclass(frozen=True)`,
  `dataclasses.replace` (shallow copy), `types.MappingProxyType` (read-only dict view), and PEP 604
  `X | Y` union syntax (3.10+). `copy.replace` is 3.13+ — examples stay on `dataclasses.replace` for 3.10
  compatibility. The `Some`/`Nothing`/`Ok`/`Err` types are **hand-rolled** (mirroring Rust's `Option`/
  `Result`), stdlib-only — no third-party FP library required. Current stable is Python 3.14.
  (docs.python.org / PEP 634 / PEP 604)

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · pure-functions** — functions whose output depends only on their inputs, with no observable side effect.
- **co-02 · side-effects-and-purity** — naming what a side effect is and drawing the purity boundary around it.
- **co-03 · referential-transparency** — a call can be replaced by its value without changing the program.
- **co-04 · immutability** — data that cannot be mutated after construction (`tuple`, `frozen` dataclass, `frozenset`).
- **co-05 · persistent-data-and-structural-sharing** — updated versions share unchanged structure with the old.
- **co-06 · first-class-functions** — functions are ordinary values: assigned, stored, passed, returned.
- **co-07 · higher-order-functions** — functions that take and/or return other functions.
- **co-08 · closures-for-configuration** — a returned function captures enclosing variables to bake in config.
- **co-09 · currying** — turning an n-ary function into a chain of one-argument functions.
- **co-10 · partial-application** — fixing some arguments now (`functools.partial`) to get a smaller function.
- **co-11 · function-composition** — building `f ∘ g` so data flows through a sequence of small functions.
- **co-12 · pipe-utilities** — a left-to-right `pipe(x, f, g)` reading in application order, not inside-out.
- **co-13 · map-filter-reduce** — the three core transforms over sequences, replacing accumulation loops.
- **co-14 · recursion-and-pythons-missing-tco** — recursion as a functional idiom; CPython has no tail-call optimization.
- **co-15 · lazy-evaluation-and-generators** — compute values on demand with generators/`yield`, not all up front.
- **co-16 · itertools-toolkit** — the composable lazy building blocks (`islice`, `chain`, `accumulate`, `groupby`, `tee`).
- **co-17 · memoization** — cache pure-function results by argument (`functools.lru_cache` or a hand dict).
- **co-18 · decorators-as-higher-order-functions** — decorators are HOFs that wrap behavior around a function.
- **co-19 · point-free-style** — expressing a transform by composing functions without naming the argument.
- **co-20 · algebraic-data-types-in-python** — sum types as unions of frozen dataclasses (`X | Y`, PEP 604).
- **co-21 · structural-pattern-matching** — `match`/`case` destructuring an ADT (PEP 634; no compile-time exhaustiveness).
- **co-22 · option-maybe-type** — a hand-rolled `Some`/`Nothing` making "absence" a value, not a `None` landmine.
- **co-23 · result-either-type** — a hand-rolled `Ok`/`Err` carrying success-or-error as a value, not an exception.
- **co-24 · railway-oriented-error-handling** — threading `Result` through a pipeline that short-circuits on the first error.
- **co-25 · functor-intuition** — a "mappable" container: `map` applies a function inside without unwrapping.
- **co-26 · applicative-intuition** — combining several wrapped values with a multi-argument function.
- **co-27 · monad-intuition** — chaining functions that each return a wrapped value (`bind`/`and_then`/`flat_map`).
- **co-28 · functional-core-imperative-shell** — a pure core surrounded by a thin I/O shell that holds all effects.

## Tensions & trade-offs — when NOT to reach for this

- **Purity vs the machine**: immutability allocates, and a tight numeric loop or a huge in-place buffer is a
  place an imperative core is honestly faster — insisting on purity there is dogma, not engineering.
- **Monad-all-the-things**: the algebraic patterns (`Result`/`Option`, functors, monads) buy composability
  and charge indirection plus a learning tax; a `Result` chain three layers deep can read _worse_ than an
  early `raise`. Reach for them where error-as-value genuinely simplifies, not everywhere.
- **When NOT to use it**: a fundamentally stateful, mutation-heavy domain (a game loop, a physics sim, a
  device driver) fights the paradigm head-on. The move is functional-core / imperative-shell to _quarantine_
  the state, not a crusade to abolish it.

## Lineage — why it beat the alternative

- FP traces to Church's lambda calculus (1930s) — a model of computation as pure function application that
  predates stored-program machines. It stayed academic (Lisp 1958, ML, Haskell 1990) until multicore and
  distributed systems made _shared mutable state_ the industry's dominant pain: the property FP had all
  along — referential transparency — became the practical answer to concurrency and testability. That is why
  "reduce shared mutable state" now surfaces inside mainstream OO languages (immutable records, `map`/`filter`,
  `Optional`). The lesson is not purity-as-religion but that _controlling where state and effects live_ is the
  leverage — the same functional-core / imperative-shell split this repo is built on, and the ground
  [`88-type-systems`](./type-systems.md) later makes rigorous.

## Worked examples

Colocated under `functional-programming/learning/code/`; each a runnable pure/impure contrast (DD-20/DD-30).
Contiguous `ex-01..ex-80`. Every example cites the `co-NN` it exercises; every concept above is exercised
by ≥1 example.

### Beginner

- **ex-01 · pure-vs-impure-pair** — a pure `add(a, b)` beside an impure version mutating a global — verify the pure one gives the same result on repeat calls. (co-01, co-02)
- **ex-02 · referential-transparency-substitution** — replace a call with its literal value in an expression — verify the program's output is unchanged. (co-03)
- **ex-03 · detect-side-effect** — three functions (one prints, one mutates an arg, one is pure); classify each — verify only the pure one is flagged pure. (co-02)
- **ex-04 · immutable-tuple-vs-list** — attempt to mutate a `tuple`, catch `TypeError` — verify immutability is enforced. (co-04)
- **ex-05 · frozen-dataclass** — a `@dataclass(frozen=True)` rejects an attribute set — verify `FrozenInstanceError` is raised. (co-04)
- **ex-06 · dataclasses-replace-copy** — `dataclasses.replace` produces a new record — verify the original is unchanged and the copy differs. (co-04, co-05)
- **ex-07 · structural-sharing-cons** — a persistent cons-list prepend sharing the tail — verify the old version is still intact after the update. (co-05)
- **ex-08 · function-as-value** — assign a function to a variable and call through it — verify the same result. (co-06)
- **ex-09 · functions-in-a-list** — store functions in a list and call each — verify all are invoked with the right output. (co-06)
- **ex-10 · higher-order-apply** — an `apply(fn, x)` returning `fn(x)` — verify it works for two different functions. (co-07)
- **ex-11 · return-a-function** — a `multiplier(n)` returning a closure — verify `multiplier(3)(4) == 12`. (co-07, co-08)
- **ex-12 · closure-captures-config** — a closure capturing a threshold — verify behavior varies with the captured config. (co-08)
- **ex-13 · map-basic** — `map(str.upper, words)` — verify every word is uppercased. (co-13)
- **ex-14 · filter-basic** — `filter(is_even, nums)` — verify only evens remain. (co-13)
- **ex-15 · reduce-sum** — `reduce(add, nums, 0)` — verify the total. (co-13)
- **ex-16 · comprehension-vs-map** — a comprehension matching a `map`+`filter` — verify an identical list. (co-13)
- **ex-17 · curry-manual** — hand-curry a 2-arg function into `f(a)(b)` — verify the result matches the uncurried call. (co-09)
- **ex-18 · partial-application** — `functools.partial(pow, 2)` — verify it computes `2**n`. (co-10)
- **ex-19 · compose-two** — a `compose(f, g)` helper — verify it computes `f(g(x))`. (co-11)
- **ex-20 · pipe-left-to-right** — a `pipe(x, f, g)` reading left→right — verify it equals the nested calls. (co-12, co-11)
- **ex-21 · generator-lazy-count** — a generator yielding on demand — verify only pulled values are computed. (co-15)
- **ex-22 · generator-vs-list-memory** — a generator expression vs a list of the same data — verify the generator doesn't materialize eagerly. (co-15)
- **ex-23 · itertools-islice-infinite** — `islice` over an infinite `count()` — verify the first N values are taken. (co-16, co-15)
- **ex-24 · itertools-chain-groupby** — `chain` + `groupby` over data — verify the grouped output. (co-16)
- **ex-25 · memoize-lru-cache** — `@lru_cache` on a recursive `fib` — verify `cache_info()` shows hits. (co-17)
- **ex-26 · decorator-log-wrap** — a HOF decorator wrapping a function with a log — verify the wrapped result is unchanged. (co-18)
- **ex-27 · recursion-factorial** — a recursive factorial — verify the value; comment that CPython has no TCO. (co-14)
- **ex-28 · optional-none-guard** — a function returning `None` on a miss, caller guards — verify the miss is handled. (co-22)

### Intermediate

- **ex-29 · pure-core-extract** — extract a pure core from a mutating routine — verify the core is tested with no I/O. (co-01, co-28)
- **ex-30 · persistent-list-prepend** — a persistent linked list `prepend` sharing structure — verify O(1) sharing and the old list intact. (co-05)
- **ex-31 · mappingproxy-readonly** — expose a `dict` via `types.MappingProxyType` — verify writes through the view raise. (co-04)
- **ex-32 · closure-counter-vs-pure-fold** — a stateful closure counter vs a pure fold count — verify both count, contrast where state lives. (co-08, co-01)
- **ex-33 · currying-with-partial** — build a pipeline of `partial`s — verify the composed transform. (co-10, co-09)
- **ex-34 · compose-n-functions** — `compose(*fns)` folding a list of functions — verify the application order. (co-11)
- **ex-35 · point-free-transform** — rewrite a lambda pipeline point-free — verify identical output. (co-19)
- **ex-36 · reduce-histogram** — `reduce` building a `dict` histogram — verify the counts. (co-13)
- **ex-37 · map-filter-reduce-pipeline** — chain all three for a data summary — verify the result. (co-13, co-11)
- **ex-38 · lazy-pipeline-generators** — a `map`/`filter` generator pipeline pulled by `next` — verify laziness end to end. (co-15, co-13)
- **ex-39 · itertools-accumulate** — running totals via `accumulate` — verify the prefix sums. (co-16)
- **ex-40 · itertools-pairwise-tee** — `pairwise`/`tee` over a stream — verify the adjacent pairs. (co-16)
- **ex-41 · memoize-manual-dict** — a hand-rolled memo dict for an expensive function — verify the second call is cached. (co-17)
- **ex-42 · decorator-with-args** — a parameterized decorator (`@retry(3)`) — verify the retries are counted. (co-18)
- **ex-43 · decorator-preserves-metadata** — `functools.wraps` keeps `__name__` — verify the wrapped name is preserved. (co-18)
- **ex-44 · recursion-to-iteration** — convert deep recursion to an explicit stack — verify the same result on an input that would `RecursionError`. (co-14)
- **ex-45 · adt-sum-type-dataclasses** — model a shape as a union of frozen dataclasses (`Circle | Square`) — verify each variant. (co-20)
- **ex-46 · match-case-over-adt** — `match`/`case` over the ADT — verify each branch fires; comment on the lack of exhaustiveness checking. (co-21, co-20)
- **ex-47 · match-guards** — `case` with `if` guards — verify the guard selects the right branch. (co-21)
- **ex-48 · option-some-nothing** — a hand-rolled `Some`/`Nothing` with `map` — verify `map` is skipped on `Nothing`. (co-22, co-25)
- **ex-49 · option-chaining** — chain `Option`-returning lookups — verify short-circuit on the first miss. (co-22)
- **ex-50 · result-ok-err** — a hand-rolled `Ok`/`Err` mirroring Rust — verify the error is carried as a value. (co-23)
- **ex-51 · result-map-and-then** — `map`/`and_then` on a `Result` — verify the pipeline stops at the first `Err`. (co-23, co-27)
- **ex-52 · railway-parse-pipeline** — a validation pipeline threading `Result` — verify one bad field short-circuits the rest. (co-24, co-23)
- **ex-53 · functor-law-identity** — show `container.map(identity) == container` — verify the identity law holds by example. (co-25)
- **ex-54 · functor-over-list-and-option** — one `fmap` working on both a list and an `Option` — verify both are mapped. (co-25)
- **ex-55 · applicative-combine-options** — apply a 2-arg function across two `Option`s (`map2`) — verify both-present combines and any-absent short-circuits. (co-26)
- **ex-56 · monad-bind-chain** — `bind`/`flat_map` chaining `Result`-returning steps — verify monadic sequencing. (co-27)

### Advanced

- **ex-57 · functional-core-imperative-shell-tool** — a CSV analyzer split into a pure core + I/O shell — verify the core is pure-tested and the shell holds all I/O. (co-28, co-01)
- **ex-58 · property-test-purity** — a Hypothesis test asserting a function is pure/idempotent — verify the property holds across generated inputs. (co-01, co-03)
- **ex-59 · persistent-tree-update** — a persistent binary tree with a structural-sharing update — verify the old root is intact. (co-05)
- **ex-60 · immutable-state-reducer** — a Redux-style pure `(state, action) -> state` reducer — verify replaying the actions reproduces the state. (co-01, co-04)
- **ex-61 · compose-with-result** — compose `Result`-returning functions (Kleisli) — verify error propagation through the composition. (co-11, co-27, co-23)
- **ex-62 · curry-decorator** — a `@curry` decorator auto-currying by arity — verify partial calls accumulate arguments. (co-09, co-18)
- **ex-63 · lazy-infinite-sieve** — a lazy prime sieve over an infinite generator — verify the first N primes. (co-15, co-16)
- **ex-64 · generator-coroutine-pipeline** — a pull pipeline of `yield` stages — verify the streaming result. (co-15)
- **ex-65 · memoize-bounded-lru** — a memo decorator with a bounded `maxsize` — verify eviction of the oldest entry. (co-17, co-18)
- **ex-66 · tail-recursion-trampoline** — a trampoline simulating TCO — verify a deep recursion completes without `RecursionError`. (co-14)
- **ex-67 · adt-expression-evaluator** — an AST as an ADT with a `match` evaluator — verify an arithmetic result. (co-20, co-21)
- **ex-68 · option-do-style-sequence** — sequence `Option` computations readably — verify short-circuit on absence. (co-22, co-27)
- **ex-69 · result-form-validation** — validate a form, short-circuiting on the first error — verify the failing rule is reported. (co-24, co-23)
- **ex-70 · functor-laws-property-checked** — property-test the functor identity + composition laws — verify both hold. (co-25)
- **ex-71 · applicative-validation-accumulate** — an applicative that accumulates _all_ errors instead of short-circuiting — verify every error is collected. (co-26, co-24)
- **ex-72 · monad-laws-intuition** — show left-identity, right-identity, associativity by example for `Result` — verify the laws hold. (co-27)
- **ex-73 · point-free-combinator-lib** — a small point-free combinator library — verify a composed transform. (co-19, co-12)
- **ex-74 · pipe-vs-nested-readability** — a deep `pipe` vs nested calls on real data — verify identical output, note the readability difference. (co-12, co-11)
- **ex-75 · immutability-perf-cost** — measure persistent-update cost vs in-place mutation — verify both correct, note the allocation cost numerically. (co-04, co-05)
- **ex-76 · reduce-shared-state-refactor** — refactor shared-mutable code to pass state explicitly — verify no globals remain and the output is unchanged. (co-28, co-04)
- **ex-77 · decorator-stack-composition** — stack multiple decorators and reason about order — verify the order-dependent behavior. (co-18, co-11)
- **ex-78 · lazy-vs-eager-tradeoff** — a case where laziness saves work and one where it hides cost — verify both behaviors. (co-15)
- **ex-79 · monad-option-vs-result** — the same pipeline in `Option` vs `Result` — verify each carries its own error model. (co-22, co-23, co-27)
- **ex-80 · capstone-preview-log-analyzer** — a functional-core log analyzer with `Result` errors + an applicative combine — verify the end-to-end report. (co-28, co-23, co-26)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a small data-processing tool (e.g. a log/CSV analyzer) as a **functional core +
  imperative shell**: pure transformation pipeline (`map`/`filter`/`reduce` + composition), `Result`-based
  error handling instead of exceptions, immutable data, and a thin I/O shell — with property tests
  asserting purity/invariants.
- **Concepts exercised**: [ ] pure functions + referential transparency (co-01, co-03) [ ] composition pipeline (co-11, co-13)
  [ ] `Result`/`Option` error handling (co-22, co-23, co-24) [ ] immutability (co-04, co-05) [ ] functional core / imperative shell split (co-28)
  [ ] a functor/applicative/monad pattern used in earnest (co-25, co-26, co-27).
- **Ordered steps**:
  1. `.../learning/capstone/code/core.py` — pure parse→transform→aggregate functions, no I/O. Verify a
     `pytest` suite (incl. a Hypothesis invariant) passes with no mocking needed.
  2. `shell.py` — the imperative shell reading a file and calling the core. Verify it produces the report
     end to end from the CLI.
  3. Replace exception control flow with a `Result`/`Either` chain. Verify malformed rows yield a
     collected error result, not a crash.
  4. Show one functor/monoid pattern (e.g. combining partial aggregates monoidally). Verify the combined
     result equals the whole-in-one-pass result.
- **Acceptance criteria**: the core is pure and tested without mocks; errors are values not exceptions; the
  shell is the only place with I/O; the tool runs end to end.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Structure and Interpretation of Computer Programs** — Harold Abelson & Gerald Jay Sussman (1985; 2nd ed. 1996). Teaches functional-programming fundamentals — closures, higher-order functions, recursion — as its core method. <https://mitp-content-server.mit.edu/books/content/sectbyfn/books_pres_0/6515/sicp.zip/full-text/book/book.html>
- **Learn You a Haskell for Great Good!** — Miran Lipovača (2011). The most widely used friendly introduction to pure functional programming and Haskell's type system. <https://learnyouahaskell.com/>
- **Programming in Haskell** — Graham Hutton (2007; 2nd ed. 2016). Rigorous, widely adopted undergraduate functional programming textbook.
- **Functional Programming in Scala** — Paul Chiusano & Rúnar Bjarnason (2014). Canonical text teaching algebraic data types and pure-function design in a hybrid OO/FP language.

**Papers & articles**

- **Why Functional Programming Matters** — John Hughes (1989). Classic paper arguing that higher-order functions and lazy evaluation are what make functional programming modular. <https://www.cs.kent.ac.uk/people/staff/dat/miranda/whyfp90.pdf>
- **Out of the Tar Pit** — Ben Moseley & Peter Marks (2006). Influential essay diagnosing software complexity and proposing a functional-relational remedy. <https://curtclifton.net/papers/MoseleyMarks06a.pdf>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Theory & low-level systems — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · CS fundamentals, DS&A & algorithms — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 1 · CS theory & foundations (the university core, taught first).

> _Content originated in the now-closed FS-SE plan (topic 23); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
