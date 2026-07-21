# Lisp (By Example, Scheme + Clojure)

**Course ID**: `lisp` · **Format**: By Example · **Language**: Scheme + Clojure.

**Short summary**: Lisp, macros, homoiconic programming

**Scope note**: the Lisp idea — code-as-data (homoiconicity), s-expressions, the read-eval loop, and macros
that let the language extend itself. Taught in **Scheme from scratch** (minimal, pedagogical), with a
**Clojure sidebar** showing the same ideas on a modern hosted JVM Lisp. Deliberately stretches the mental
model established by the FP thread ([`23-functional-programming`](./functional-programming.md)).

- **License note (DD-15/DD-21)**: **Racket** (a batteries-included Scheme) is Apache-2.0/MIT; **Clojure** is
  EPL-1.0. Both OSS and runnable with no paid account (DD-20).

## Why this exists · the big idea

- **The problem before the solution**: in most languages the syntax is fixed by the compiler writers and
  you build only within it — when the language lacks the construct you need, you write boilerplate around
  the gap. Lisp exists to erase that wall: the language is made of the same data you manipulate, so you
  extend it yourself.
- **Keep-this-if-you-forget-everything**: when code is just data (s-expressions), macros let you grow the
  language toward your problem instead of bending your problem to fit the language.
- **Big ideas touched**: `abstraction-and-its-cost` — homoiconicity and macros let you build abstractions
  no fixed-syntax language can express, paid for with a uniform, parens-heavy surface and the power to
  rewrite meaning; `mechanism-vs-policy` — the reader/evaluator is a small fixed mechanism, and macros let
  you set new syntactic policy (new control forms) on top of it without touching the core.

## Prerequisites

- **Prior topics**: [topic 23 Functional Programming](./functional-programming.md) (recursion, higher-
  order functions, immutability) and [topic 22 Programming Paradigms](./programming-paradigms.md)
  (the paradigm-survey context — Lisp as its own family blending functional style with metaprogramming).
- **Tools & environment**: **Racket** (or another Scheme, e.g. Guile) for the from-scratch track; a
  **Clojure** toolchain (`clojure`/`deps.edn`) + JDK for the sidebar; Neovim/VSCode with a Lisp/REPL
  integration (DD-17).
- **Assumed knowledge**: recursion + higher-order functions + immutability as a habit (topic 23); comfort
  moving between programming paradigms (topic 22).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified (licenses, exact match): **Racket = Apache-2.0/MIT at your option**
  (download.racket-lang.org/license.html); **Clojure = EPL-1.0** (clojure.org/community/license). Both are
  fully free/open, runnable with no paid account. `syntax-rules` (Scheme, hygienic) vs `defmacro` (Clojure,
  unhygienic) contrast is correct standard terminology; GNU Guile remains an actively-maintained Scheme.
- 2026-07-12 — verified (minor copyedit for the content maker): "Racket (a batteries-included Scheme)" is
  fine but Racket now positions itself as a Lisp-family language _descended from_ Scheme (R7RS via
  `#lang r7rs`, not the default) — consider "a batteries-included Scheme descendant" for precision.

### DD-35 primary-source citations (fetched-and-read)

> Anti-hallucination (DD-35): every version/standard/API below traces to a primary source a
> `web-researcher` fetched and read on 2026-07-12. Unverifiable claims are marked `[Needs Verification]`.

- **Language standards** — Scheme's small language is **R7RS-small (ratified 2013)**; Common Lisp is
  **ANSI X3.226-1994** (unrevised). R7RS-large is still incomplete — do not cite a finished "large" Scheme
  standard. Verified against r7rs.org and the CLHS.
- **Proper tail calls + hygiene** — R7RS §3.5 mandates proper tail recursion (an unbounded number of
  active tail calls); `syntax-rules` (R7RS §4.3) is **hygienic and referentially transparent**. Clojure's
  `defmacro` and CL's `defmacro` are **unhygienic** (require manual `gensym`/`#`-auto-gensym) — community
  terminology, not a word those languages' own specs use. Verified against the R7RS report.
- **Hash tables caveat** — hash tables are **NOT in R7RS-small core** (deferred to the incomplete
  R7RS-large; implementations like Racket ship their own). Scheme **vectors** ARE core — teach vectors as
  core and flag hash tables as implementation-specific.
- **Current implementations (verified live, re-pin at authoring)** — **Racket 9.2** (May 2026),
  **Clojure 1.12.5** (May 2026), **SBCL 2.6.6** (Jun 2026). `#lang r7rs` in Racket may require a package
  rather than shipping in the base distribution — `[Needs Verification]`; confirm before shipping that claim.
- **Licenses (DD-15/DD-21)** — Racket = Apache-2.0/MIT; Clojure = EPL-1.0 (both OSS, no paid account).

## Concepts

<!-- co-01 · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · s-expressions** — code and data share one parenthesized s-expression syntax.
- **co-02 · homoiconicity** — programs are the very list data structures the language manipulates.
- **co-03 · reader** — the reader turns character text into s-expressions before evaluation.
- **co-04 · quote** — `quote` (`'`) suppresses evaluation, yielding the form as data.
- **co-05 · eval** — `eval` evaluates an s-expression as code, closing the code-as-data loop.
- **co-06 · atoms-lists** — the two data kinds are atoms and lists.
- **co-07 · cons** — `cons` builds a pair; lists are chains of pairs.
- **co-08 · car-cdr** — `car`/`cdr` (Scheme `first`/`rest`) decompose a list.
- **co-09 · define** — `define` binds a name to a value or a function.
- **co-10 · lambda** — `lambda` creates an anonymous function.
- **co-11 · closures** — a `lambda` captures the environment in which it was created.
- **co-12 · recursion** — recursion is the primary iteration mechanism.
- **co-13 · tail-calls** — Scheme mandates proper tail calls, so tail recursion runs in constant space.
- **co-14 · higher-order-functions** — functions are values passed to `map`/`filter`/`fold`.
- **co-15 · conditionals** — `if` and `cond` express branching.
- **co-16 · let-binding** — `let`/`let*` introduce local bindings (parallel vs sequential).
- **co-17 · repl** — the read-eval-print loop is the primary, incremental workflow.
- **co-18 · quasiquote** — quasiquote/unquote/unquote-splicing build list templates with holes.
- **co-19 · syntax-rules** — `syntax-rules` defines hygienic macros by pattern-based rewrite rules.
- **co-20 · macro-hygiene** — hygiene auto-renames introduced bindings so macros can't capture variables.
- **co-21 · macro-new-form** — a macro adds a genuinely new control or binding form to the language.
- **co-22 · macroexpand** — expansion can be inspected (macro stepper / `macroexpand-1`).
- **co-23 · continuations** — `call/cc` reifies the current continuation as a first-class escape procedure.
- **co-24 · vectors** — Scheme vectors are the core indexed collection (hash tables are R7RS-large/impl-specific).
- **co-25 · clojure-data-structures** — Clojure's list/vector/map/set are immutable and persistent.
- **co-26 · clojure-homoiconicity** — Clojure programs are Clojure data structures, too.
- **co-27 · clojure-defmacro** — Clojure `defmacro` is unhygienic; capture is avoided with `gensym`/`#`.
- **co-28 · clojure-jvm-interop** — Clojure is hosted on the JVM with direct Java interop.
- **co-29 · clojure-seq** — the `seq` abstraction unifies iteration over collections (lazily).
- **co-30 · lisp-lineage** — the Lisp family: Scheme's minimalism, Clojure's hosted pragmatism, Common Lisp.

## Worked examples

Colocated under `lisp/learning/code/`; Scheme (Racket) primary + Clojure sidebar (DD-20/DD-30).
Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · s-expr-eval** — evaluate an s-expression in the REPL — verify the value. (co-01, co-17)
- **ex-02 · atom-vs-list** — an atom vs a list — verify the distinction. (co-06)
- **ex-03 · cons-pair** — `cons` two values — verify the pair. (co-07)
- **ex-04 · car-cdr** — `car`/`cdr` a list — verify first/rest. (co-08)
- **ex-05 · list-construct** — build a list with `list`/`cons` — verify the contents. (co-07, co-06)
- **ex-06 · quote-list** — `quote` a list — verify it isn't evaluated. (co-04)
- **ex-07 · define-var** — `define` a variable — verify the value. (co-09)
- **ex-08 · define-fn** — `define` a function — verify a call. (co-09)
- **ex-09 · lambda-basic** — a `lambda` applied inline — verify the result. (co-10)
- **ex-10 · closure-capture** — a `lambda` capturing a variable — verify the capture. (co-11)
- **ex-11 · if-cond** — an `if` and a `cond` — verify the branches. (co-15)
- **ex-12 · let-binding** — a `let` binding — verify the locals. (co-16)
- **ex-13 · let-star** — `let*` sequential binding — verify visibility. (co-16)
- **ex-14 · recursion-factorial** — a recursive factorial — verify the value. (co-12)
- **ex-15 · recursion-list-length** — recursive list length — verify the count. (co-12, co-08)
- **ex-16 · recursion-list-sum** — recursive list sum — verify the total. (co-12)
- **ex-17 · map-example** — `map` over a list — verify the transform. (co-14)
- **ex-18 · filter-example** — `filter` a list — verify the selection. (co-14)
- **ex-19 · fold-example** — `fold`/reduce a list — verify the accumulation. (co-14)
- **ex-20 · repl-workflow** — build up a function in the REPL — verify incremental development. (co-17)
- **ex-21 · vector-basic** — a Scheme vector ref/set — verify indexing. (co-24)
- **ex-22 · clojure-hello** — a Clojure program prints — verify the output (sidebar). (co-28)
- **ex-23 · clojure-list-vector** — a Clojure list/vector — verify the literals. (co-25)
- **ex-24 · clojure-map** — a Clojure map `get` — verify the lookup. (co-25)
- **ex-25 · clojure-first-rest** — Clojure `first`/`rest` on a seq — verify decomposition. (co-29, co-08)
- **ex-26 · clojure-recursion** — a Clojure recursive function — verify the value. (co-12)

### Intermediate

- **ex-27 · tail-recursion** — a tail-recursive loop in Scheme — verify unbounded iteration. (co-13)
- **ex-28 · non-tail-vs-tail** — a non-tail vs tail version — verify the stack difference. (co-13, co-12)
- **ex-29 · hof-compose** — compose two functions — verify the composition. (co-14)
- **ex-30 · hof-return-fn** — a function returning a function — verify currying. (co-14, co-11)
- **ex-31 · named-let** — a named `let` loop — verify iteration. (co-16, co-12)
- **ex-32 · assoc-list** — an association-list lookup — verify retrieval. (co-06, co-08)
- **ex-33 · quasiquote-template** — a quasiquote/unquote template — verify substitution. (co-18)
- **ex-34 · unquote-splicing** — unquote-splicing into a template — verify the splice. (co-18)
- **ex-35 · eval-data-as-code** — `eval` an s-expression built as data — verify code-as-data. (co-05, co-02)
- **ex-36 · build-expr-then-eval** — construct then `eval` an expression — verify the result. (co-05, co-01)
- **ex-37 · homoiconicity-inspect** — inspect a program as a list — verify it's data. (co-02)
- **ex-38 · repl-define-redefine** — redefine a function at the REPL — verify the hot update. (co-17, co-09)
- **ex-39 · syntax-rules-swap** — a `syntax-rules` `swap!` macro — verify it swaps. (co-19, co-21)
- **ex-40 · syntax-rules-unless** — a `syntax-rules` `unless` macro — verify the new form. (co-19, co-21)
- **ex-41 · macro-pattern-ellipsis** — a `syntax-rules` ellipsis pattern — verify variadic expansion. (co-19)
- **ex-42 · macro-hygiene-demo** — a would-be capturing macro kept hygienic — verify no capture. (co-20)
- **ex-43 · macroexpand-inspect** — expand a macro with the stepper — verify the expansion. (co-22)
- **ex-44 · clojure-hof** — Clojure `map`/`filter`/`reduce` — verify the pipeline. (co-14, co-29)
- **ex-45 · clojure-immutable** — Clojure `conj` returns a new collection — verify immutability. (co-25)
- **ex-46 · clojure-set** — a Clojure set's uniqueness — verify dedup. (co-25)
- **ex-47 · clojure-code-as-data** — a Clojure form quoted as data — verify homoiconicity. (co-26)
- **ex-48 · clojure-defmacro-basic** — a Clojure `defmacro` — verify the expansion. (co-27)
- **ex-49 · clojure-macroexpand** — Clojure `macroexpand-1` — verify the expansion. (co-27, co-22)
- **ex-50 · clojure-gensym** — a Clojure macro using `gensym`/`#` to avoid capture — verify safety. (co-27, co-20)
- **ex-51 · clojure-java-interop** — Clojure calling a Java method — verify interop. (co-28)
- **ex-52 · scheme-vs-clojure-macro** — the same new form in `syntax-rules` vs `defmacro` — verify parity. (co-19, co-27)

### Advanced

- **ex-53 · syntax-rules-binding-form** — a macro introducing a new binding form — verify scoping. (co-21, co-19)
- **ex-54 · macro-recursive-expansion** — a recursive macro — verify nested expansion. (co-19)
- **ex-55 · macro-with-guard** — a macro with a pattern literal/guard — verify matching. (co-19)
- **ex-56 · hygiene-vs-capture** — hygiene compared to Clojure's manual `gensym` — verify the contrast. (co-20, co-27)
- **ex-57 · continuation-callcc** — `call/cc` capturing a continuation — verify the escape. (co-23)
- **ex-58 · callcc-early-exit** — `call/cc` for early exit from a loop — verify the jump. (co-23)
- **ex-59 · callcc-generator** — a simple generator via `call/cc` — verify resumption. (co-23)
- **ex-60 · mini-interpreter** — a tiny expression interpreter (`eval` over data) — verify evaluation. (co-05, co-02)
- **ex-61 · mini-interpreter-env** — the interpreter with an environment — verify variable lookup. (co-05, co-11)
- **ex-62 · dsl-via-macros** — a small DSL built with macros — verify a new syntax. (co-21, co-19)
- **ex-63 · fold-based-eval** — a fold-based evaluator over an s-expr tree — verify traversal. (co-14, co-02)
- **ex-64 · recursion-tree-walk** — a recursive tree walk of nested lists — verify traversal. (co-12, co-08)
- **ex-65 · clojure-structural-sharing** — a Clojure update sharing structure — verify no copy. (co-25)
- **ex-66 · clojure-seq-lazy** — a lazy Clojure sequence — verify laziness. (co-29)
- **ex-67 · clojure-threading-macro** — Clojure's `->` threading macro — verify pipeline readability. (co-27)
- **ex-68 · clojure-dsl-macro** — a Clojure DSL via `defmacro` — verify the new form. (co-27, co-26)
- **ex-69 · scheme-clojure-parity** — a feature built in both Lisps — verify equivalent behaviour. (co-30)
- **ex-70 · lisp-family-contrast** — Scheme minimalism vs Clojure hosted vs Common Lisp — verify the contrast. (co-30)
- **ex-71 · repl-driven-macro-dev** — develop a macro interactively at the REPL — verify the iteration. (co-17, co-22)
- **ex-72 · quote-eval-roundtrip** — quote a program, transform it, `eval` it — verify metaprogramming. (co-04, co-05, co-02)
- **ex-73 · hygienic-macro-verified** — a hygienic macro verified free of capture — verify hygiene holds. (co-20)
- **ex-74 · macro-adds-control-form** — a macro adding a genuine control form (`while`) — verify it works. (co-21)
- **ex-75 · both-lisps-run** — the Scheme + Clojure versions both run — verify parity. (co-30)
- **ex-76 · full-lisp-slice** — recursion + HOF + a `syntax-rules` macro + code-as-data in one program — verify the whole. (co-12, co-14, co-19, co-02)
- **ex-77 · integration-scheme-clojure** — the macro in Scheme + its Clojure `defmacro` mirror — verify both. (co-19, co-27)
- **ex-78 · capstone-lisp-macro** — a Lisp program: a recursive list-processing program using HOF, a `syntax-rules` macro adding a new control/binding form (with a macro-stepper check), then the Clojure `defmacro` equivalent — verify recursion + HOF + list processing work, the macro adds a genuinely new form and expands hygienically, and the Clojure sidebar mirrors it, both running. (co-12, co-14, co-19, co-27, co-02)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: use Lisp's code-as-data nature to build something the language couldn't do out of the box — a
  `syntax-rules` macro (Scheme) that introduces a new control/binding form, exercised by a small
  recursive, list-processing program — then reproduce the core idea in the **Clojure sidebar** with
  `defmacro`, showing homoiconicity across two Lisps.
- **Concepts exercised**: [ ] s-expressions + `quote`/`eval` (code-as-data) (co-01, co-02, co-04, co-05)
  [ ] recursion + `cons`/`car`/`cdr` list processing (co-12, co-07, co-08) [ ] higher-order functions (co-14)
  [ ] a hygienic `syntax-rules` macro adding a new form (co-19, co-20, co-21) [ ] the Clojure `defmacro`
  equivalent (sidebar) (co-27).
- **Ordered steps**:
  1. `.../learning/capstone/code/main.rkt` — a recursive list-processing program using higher-order
     functions. Verify it runs in Racket and produces the expected output.
  2. Add a `syntax-rules` macro introducing a new control/binding form, used by the program. Verify the
     macro expands correctly (check with the macro stepper) and the program still runs.
  3. `sidebar.clj` — reproduce the core idea in Clojure with `defmacro`. Verify it runs on the Clojure
     toolchain and mirrors the Scheme behaviour.
- **Acceptance criteria**: recursion + list processing + higher-order functions work; the macro adds a
  genuinely new form and expands hygienically; the Clojure sidebar reproduces the idea; both run.
- **Done bar**: runnable end-to-end (Racket + Clojure) + web-verified.

## Read more

**Books**

- **Structure and Interpretation of Computer Programs**, 2nd ed. — Harold Abelson, Gerald Jay Sussman, with Julie Sussman (1996). The field-defining text on abstraction, recursion, and interpreters, taught for decades at MIT; freely hosted. <https://web.mit.edu/6.001/6.037/sicp.pdf>
- **The Little Schemer**, 4th ed. — Daniel P. Friedman, Matthias Felleisen (1995). Classic Socratic introduction to recursion and Scheme thinking.
- **On Lisp** — Paul Graham (1993). Canonical text on Lisp macros and bottom-up programming, freely released by the author. <https://www.paulgraham.com/onlisptext.html>
- **Practical Common Lisp** — Peter Seibel (2005). Widely cited hands-on introduction to Common Lisp, freely available online. <https://gigamonkeys.com/book/>
- **Let Over Lambda** — Doug Hoyte (2008). Advanced, opinionated treatment of Common Lisp macro programming.
- **Clojure for the Brave and True** — Daniel Higginbotham (2015). The most widely recommended modern introduction to Clojure and Lisp-family functional programming, free online. <https://www.braveclojure.com/>

## In which paths

- `fundamentally-strong/software-engineer` — Stage 3 · Concurrency & language breadth.

> _Content originated in the now-closed FS-SE plan (topic 86); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
