# 89 · Compilers, Parsers & Transpilers (By Example, F# †)

**prd row**: Pass 4 · Concurrency & Systems · By Example · F# † · Learn 189 / Drill 289 ·
Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: how a language processor works front-to-back — lexing, parsing (to an AST), semantic
analysis, and either interpreting/evaluating or emitting code — by building a small language end-to-end in
**F#**. The ML family is the natural home for this work: discriminated unions model an AST directly,
exhaustive pattern matching walks it safely, and parser combinators (FParsec) express a grammar as
composable functions. **Motivation (DD-16)**: in the AI-assisted era, compilers/type-checkers/linters are
your **guardrails** — understanding how they parse and reason about code makes you a sharper reader and
reviewer of both hand-written and AI-generated code. As the **last subject topic of Pass 4**, this file also
anchors the two Pass-4 concurrency capstones (`capstone-concurrency-and-systems` and
`capstone-concurrency-showdown`), which integrate the pass's concurrency + systems-depth threads (the
whole-journey `capstone-lead-at-altitude` now anchors at the journey's true close,
[`94-site-reliability-engineering`](./94-site-reliability-engineering.md)).

## Why this exists · the big idea

- **The problem before the solution**: every language, type-checker, linter, and transpiler you use is a
  black box until you've built one — and in the AI-assisted era those tools are your guardrails, so not
  understanding how they parse and reason about code makes you a weaker reviewer of both human and machine
  output. This topic opens the box.
- **Keep-this-if-you-forget-everything**: a language processor is a pipeline — source → tokens → AST →
  analysis → interpret or emit — and once you've built the pipeline once, every compiler, linter, and
  transpiler stops being magic.
- **Big ideas touched**: `layering-and-leaks` — a compiler is layering made literal, each stage
  transforming one representation into the next, with errors leaking upward from the layer that first
  noticed them; `abstraction-and-its-cost` — the AST is the abstraction the whole back-end is built on, and
  modelling it as a discriminated union walked by exhaustive matching is where the language's shape is
  captured (and where a missing case would leak).

## Prerequisites

- **Prior topics**: [topic 87 Just Enough F#](./87-just-enough-fsharp.md) (the implementation language —
  discriminated unions, records, pattern matching, pipelines),
  [topic 19 Computer Science Foundations](./19-computer-science-foundations.md) (trees, recursion, grammars),
  and [topic 88 Type Systems](./88-type-systems.md) (ADTs + pattern matching make an AST + evaluator natural
  — the immediately-prior topic).
- **Tools & environment**: the **.NET SDK** (`dotnet`) on a current LTS, which ships the F# compiler and FSI;
  **FParsec** (the F# parser-combinator library) to contrast with a hand-written recursive-descent parser; a
  test project via `dotnet test` (xUnit/Expecto); Neovim/VSCode with the F# LSP (Ionide, DD-17).
- **Assumed knowledge**: F# discriminated unions + pattern matching and recursion (topic 87); trees + grammar
  intuition (topic 19); sum types / pattern matching as a way to shape an AST (topic 88).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: the pipeline (lexer → parser/AST → semantic analysis → interpret/emit),
  recursive-descent + Pratt parsing (precedence-climbing operator parsing), tree-walking interpreter +
  environments/scopes, and transpilation are evergreen/unchanged. Modelling the AST as a discriminated union
  and walking it with exhaustive pattern matching is idiomatic ML-family compiler practice.
- 2026-07-12 — verified (to verify at authoring time): the F# toolchain is correctly left version-unpinned —
  pin the exact **.NET SDK** and **FParsec** versions at authoring time (both were stable and current in the
  sweep, but treat the specific numbers as "to verify"). FParsec's combinator API and F#'s DU/active-pattern
  surface are stable across recent releases. (fsprojects.github.io/FParsec)

### DD-35 primary-source citations (fetched-and-read)

Every version, library, and technique claim below traces to a primary source fetched and read during
grounding. Unverifiable specifics are marked `[Needs Verification]` and never shipped as fact.

- **.NET 10** (LTS, GA November 2025) ships **F# 10**, the F# compiler, and FSI (`dotnet fsi`). Keep the SDK
  version **unpinned in prose** — the compiler-construction surface taught here is evergreen.
  (dotnet.microsoft.com/download/dotnet/10.0, learn.microsoft.com/dotnet/fsharp)
- **FParsec 1.1.1** is the current release of the F# parser-combinator library; its
  `OperatorPrecedenceParser` handles operator precedence/associativity declaratively. Pin the exact version
  **at authoring time** — treat 1.1.1 as `[Needs Verification]` when code is written. (fsprojects.github.io/FParsec, nuget.org/packages/FParsec)
- **FsLexYacc 11.4.0** is the lexer/parser-generator alternative (fslex/fsyacc) for contrast with the
  hand-written and combinator parsers; version `[Needs Verification]` at authoring. (fsprojects.github.io/FsLexYacc, nuget.org/packages/FsLexYacc)
- **Expecto 11.1.0** (or the built-in `dotnet test` runner) drives the per-stage tests; version
  `[Needs Verification]` at authoring. (github.com/haf/expecto)
- **Pratt parsing** is Vaughan Pratt's "top-down operator precedence" (1973); Robert Nystrom's
  _Crafting Interpreters_ ch. 17 ("Compiling Expressions") is the canonical modern walkthrough of
  precedence-climbing. (craftinginterpreters.com/compiling-expressions.html)
- **Tree-walking interpreter, environments/scopes, recursive descent, transpilation** are evergreen
  compiler-construction techniques verified against the Dragon Book and _Crafting Interpreters_.
- **Guardrail lens (DD-16, co-29)** — type-checkers and linters reuse the same lexer→parser→AST front-end;
  understanding it sharpens review of AI-generated code. Framing, not a version claim.

## Concepts

<!-- co-01 · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (subject). Each example below cites the co-NN it exercises. -->

- **co-01 · compiler-pipeline** — a language processor is a pipeline: source → tokens → AST → analysis → interpret/emit.
- **co-02 · lexer-tokenizer** — the lexer turns a character stream into a token stream.
- **co-03 · token-du** — tokens are modelled as a discriminated union.
- **co-04 · whitespace-comments** — the lexer skips or attaches trivia (whitespace, comments).
- **co-05 · lexer-errors** — an unrecognized character produces a reported lexer error.
- **co-06 · grammar** — a formal grammar (EBNF) defines the language's production rules.
- **co-07 · recursive-descent** — one parsing function per grammar rule, mutually recursive.
- **co-08 · ast-du** — the AST is a discriminated union; the whole back-end is built on it.
- **co-09 · operator-precedence** — precedence levels determine which operator binds tighter.
- **co-10 · pratt-parsing** — precedence-climbing (Pratt) parsing drives operator precedence with binding powers.
- **co-11 · associativity** — left/right associativity fixes how same-precedence operators group.
- **co-12 · parser-combinators** — FParsec expresses a grammar as composable parser functions.
- **co-13 · fparsec-primitives** — `pchar`/`pstring`/`pint`/`many`/`choice` build parsers up.
- **co-14 · fparsec-sepby** — combinators like `sepBy` parse delimited sequences.
- **co-15 · parser-equivalence** — the hand-written and combinator parsers must produce the same AST.
- **co-16 · parse-errors** — the parser reports and can recover from unexpected tokens.
- **co-17 · tree-walking-interpreter** — evaluation walks the AST recursively to produce a value.
- **co-18 · exhaustive-eval** — the evaluator matches every AST case; a missing one warns (FS0025).
- **co-19 · environments-scopes** — variable bindings live in an environment threaded through evaluation.
- **co-20 · lexical-scope** — nested scopes; an inner binding shadows an outer one.
- **co-21 · semantic-analysis** — checks performed on the AST after parsing, before execution.
- **co-22 · name-resolution** — resolving identifiers to their bindings; unbound names error.
- **co-23 · type-checking-pass** — a front-end pass that rejects ill-typed programs (the guardrail).
- **co-24 · transpilation** — emitting equivalent target-language source instead of interpreting.
- **co-25 · code-generation** — building the target source (or IR) as output.
- **co-26 · transpiler-vs-interpreter** — the same program run two ways must agree.
- **co-27 · active-patterns-parsing** — F# active patterns classify characters/tokens during lexing.
- **co-28 · error-messages** — good diagnostics point at the offending location with a clear message.
- **co-29 · guardrail-lens** — linters/type-checkers share this front-end (DD-16); knowing it sharpens review.
- **co-30 · testing-stages** — `dotnet test` covers each stage (lexer, parser, interpreter, transpiler).

## Tensions & trade-offs — when NOT to reach for this

- **Recursive-descent vs parser combinators**: a hand-written recursive-descent parser gives full control
  over error messages and performance but means hand-writing every grammar rule; FParsec's combinators
  compose a grammar in far less code at the cost of a layer of abstraction between you and the exact parse
  steps — this topic teaches both so you can judge the trade rather than default to one.
- **Interpreting vs transpiling**: a tree-walking interpreter is the simplest way to run a language and is
  enough for a DSL or config language, but it re-walks the AST on every run; transpiling to an existing
  runtime reuses that runtime's performance and ecosystem at the cost of a whole extra code-generation
  stage that must stay correct as the source language grows.
- **When NOT to use it**: building a hand-rolled lexer/parser for a format that already has a stable,
  well-tested library (JSON, YAML, a common config format). The pipeline built here earns its cost when
  you are building a real language or DSL, not when you are re-parsing a solved format.

## Lineage — why it beat the alternative

- Early parser generators (yacc/bison-style LALR tools, and their F# analogue FsLexYacc) won for decades
  because they produce fast, correct parsers from a compact grammar spec — but the generated tables are
  opaque, and a grammar conflict is often harder to debug than the parser itself. Hand-written
  recursive-descent parsing, together with Pratt/precedence-climbing operator parsing (Vaughan Pratt, 1973) and parser-combinator libraries like FParsec, won back ground because they read like ordinary
  code, are debuggable with ordinary tools, and — in an ML-family language — let the AST be a
  discriminated union walked by exhaustive pattern matching, so a missing case is a compiler warning
  instead of a silent bug. That same front-end (lexer → parser → AST) is what every linter and
  type-checker in [`88-type-systems`](./88-type-systems.md) reuses, which is the guardrail lens (DD-16)
  this topic is built around.

## Worked examples

Colocated under `compilers-parsers-and-transpilers/learning/code/`; F# + `dotnet test` (DD-20/DD-30). The
AST is a discriminated union; walks are exhaustive `match` expressions. Contiguous `ex-01..ex-78`. Every
example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · token-du-define** — `type Token = Num of int | Plus | Minus | ...` — verify the DU compiles. (co-03)
- **ex-02 · lex-single-number** — tokenize `"42"` — verify it yields `[Num 42]`. (co-02)
- **ex-03 · lex-operators** — tokenize `"+ - * /"` — verify each operator token. (co-02, co-03)
- **ex-04 · lex-whitespace** — tokenize `"1  +  2"` — verify spaces are skipped. (co-04)
- **ex-05 · lex-comments** — tokenize input with a `// comment` — verify the comment is dropped. (co-04)
- **ex-06 · lex-multi-token** — tokenize `"1 + 2"` — verify `[Num 1; Plus; Num 2]`. (co-02)
- **ex-07 · lex-error-badchar** — tokenize `"@"` — verify a lexer error is reported, not a crash. (co-05)
- **ex-08 · lex-identifier** — tokenize `"foo"` — verify an `Ident "foo"` token. (co-02)
- **ex-09 · lex-keyword** — distinguish `let` from an identifier — verify the keyword token. (co-02)
- **ex-10 · lex-paren** — tokenize `"( )"` — verify `LParen`/`RParen`. (co-03)
- **ex-11 · active-pattern-digit** — `let (|Digit|_|) c = ...` — verify digits match, others don't. (co-27)
- **ex-12 · active-pattern-token** — an active pattern classifying a char as operator/digit/space — verify the tag. (co-27)
- **ex-13 · lex-test-tokens** — a `dotnet test` asserting the token stream of `"1 + 2"` — verify it passes. (co-30)
- **ex-14 · lex-test-error** — a test asserting the lexer error on `"@"` — verify it passes. (co-30, co-05)
- **ex-15 · grammar-write** — write an EBNF grammar for the expression language — verify it covers the operators. (co-06)
- **ex-16 · ast-du-define** — `type Expr = Num of int | BinOp of Op * Expr * Expr` — verify the DU compiles. (co-08)
- **ex-17 · ast-construct** — build `BinOp (Add, Num 1, Num 2)` — verify its type is `Expr`. (co-08)
- **ex-18 · rd-parse-number** — recursive-descent parse of a literal — verify `"42"` → `Num 42`. (co-07)
- **ex-19 · rd-parse-addition** — parse `"1 + 2"` — verify `BinOp (Add, Num 1, Num 2)`. (co-07)
- **ex-20 · rd-parse-nested** — parse `"(1 + 2)"` — verify grouping is respected. (co-07)
- **ex-21 · precedence-mul-over-add** — parse `"1 + 2 * 3"` — verify `*` binds tighter than `+`. (co-09)
- **ex-22 · left-assoc-subtraction** — parse `"1 - 2 - 3"` — verify left-associative grouping `((1-2)-3)`. (co-11)
- **ex-23 · paren-grouping** — parse `"(1 + 2) * 3"` — verify parens override precedence. (co-09)
- **ex-24 · rd-parse-error** — parse `"1 +"` — verify an unexpected-EOF parse error. (co-16)
- **ex-25 · fparsec-pchar** — `pchar '+'` — verify it parses a `+`. (co-13, co-12)
- **ex-26 · fparsec-pint** — `pint32` — verify it parses `"42"` to `42`. (co-13)

### Intermediate

- **ex-27 · fparsec-many** — `many digit` — verify it parses a run of digits. (co-13)
- **ex-28 · fparsec-sepby** — `sepBy pint32 (pchar ',')` — verify a comma-separated list. (co-14)
- **ex-29 · fparsec-choice** — `choice [pAdd; pSub]` — verify either operator parses. (co-13)
- **ex-30 · fparsec-expr-parser** — an FParsec parser for the expression language — verify it builds the AST. (co-12)
- **ex-31 · fparsec-opp** — `OperatorPrecedenceParser` with `+`/`*` — verify precedence declaratively. (co-10, co-12)
- **ex-32 · pratt-parser-core** — a hand-written Pratt precedence-climbing loop — verify it parses operators. (co-10)
- **ex-33 · pratt-binding-power** — assign binding powers per operator — verify `*` outbinds `+`. (co-10, co-09)
- **ex-34 · pratt-right-assoc** — right-associative `^` — verify `"2 ^ 3 ^ 2"` groups right. (co-11, co-10)
- **ex-35 · parser-equivalence-test** — a test that RD and FParsec produce the same AST — verify they agree. (co-15, co-30)
- **ex-36 · parse-error-message** — a parser error citing the position/token — verify the message is specific. (co-28, co-16)
- **ex-37 · ast-print** — render an AST back to a string — verify round-trip readability. (co-08)
- **ex-38 · eval-number** — interpret `Num 42` — verify it returns `42`. (co-17)
- **ex-39 · eval-binop** — interpret `BinOp (Add, Num 1, Num 2)` — verify `3`. (co-17, co-18)
- **ex-40 · eval-precedence** — evaluate `"1 + 2 * 3"` — verify `7`. (co-17, co-09)
- **ex-41 · eval-exhaustive** — an evaluator matching every `Expr` case — verify no warning. (co-18)
- **ex-42 · eval-missing-case-warn** — omit a case in `eval` — verify FS0025. (co-18)
- **ex-43 · env-define** — an environment as `Map<string,value>` — verify a binding stores. (co-19)
- **ex-44 · env-lookup** — look up a bound variable — verify it resolves. (co-19)
- **ex-45 · eval-let-binding** — evaluate `let x = 1 in x + 2` — verify `3`. (co-19, co-20)
- **ex-46 · lexical-scope-nested** — an inner `let x` shadows an outer — verify the inner value wins in scope. (co-20)
- **ex-47 · name-resolution** — a resolution pass binding identifiers — verify each name resolves. (co-22)
- **ex-48 · undefined-var-error** — evaluate an unbound `y` — verify an unbound-variable error. (co-22, co-16)
- **ex-49 · semantic-check-arity** — check a call's argument count — verify a wrong arity is rejected. (co-21)
- **ex-50 · eval-test** — a `dotnet test` over the interpreter — verify it passes. (co-30, co-17)
- **ex-51 · eval-conditional** — evaluate `if a then b else c` — verify the chosen branch. (co-17)
- **ex-52 · eval-comparison** — evaluate `1 < 2` — verify `true`. (co-17)

### Advanced

- **ex-53 · tree-walk-full** — a full recursive tree-walk over a nested expression — verify the total. (co-17, co-18)
- **ex-54 · function-call-eval** — evaluate a call with arguments — verify the returned value. (co-17, co-19)
- **ex-55 · closure-eval** — a closure capturing its environment — verify the captured binding is used. (co-19, co-20)
- **ex-56 · recursion-eval** — evaluate a recursive function (factorial) — verify `fact 5 = 120`. (co-17)
- **ex-57 · transpile-number** — emit `Num 42` as target source `42` — verify the emitted text. (co-24)
- **ex-58 · transpile-binop** — emit `1 + 2` as Python `(1 + 2)` — verify the string. (co-24, co-25)
- **ex-59 · transpile-precedence** — emit `1 + 2 * 3` with correct parenthesization — verify precedence preserved. (co-24, co-09)
- **ex-60 · transpile-run-match** — run the transpiled output — verify it equals the interpreter's result. (co-26)
- **ex-61 · transpiler-vs-interpreter-contrast** — the same program interpreted and transpiled-then-run — verify they agree. (co-26)
- **ex-62 · codegen-emit-string** — build the full target source string for a program — verify it is valid target code. (co-25)
- **ex-63 · type-check-pass** — a simple type-checking pass over the AST — verify a well-typed program passes. (co-23)
- **ex-64 · type-error-report** — report a type mismatch (`1 + true`) — verify a clear diagnostic. (co-23, co-28)
- **ex-65 · linter-lint-rule** — a lint rule flagging, e.g., an unused binding — verify it fires. (co-29)
- **ex-66 · guardrail-writeup** — `guardrail.md` framing the front-end as a review guardrail (DD-16) — verify it ties to the code. (co-29)
- **ex-67 · error-recovery** — continue parsing after a syntax error — verify a second error is still found. (co-16)
- **ex-68 · multi-error-report** — collect and report multiple errors in one pass — verify all are listed. (co-16, co-28)
- **ex-69 · semantic-analysis-full** — a full analysis stage (resolution + arity + types) — verify it gates bad programs. (co-21)
- **ex-70 · scope-stack** — a nested scope stack for blocks — verify shadowing and pop restore. (co-20, co-19)
- **ex-71 · ast-visitor** — a generic AST traversal (fold) — verify it visits every node. (co-08, co-18)
- **ex-72 · constant-folding** — fold `1 + 2` to `3` at compile time — verify the optimized AST. (co-08)
- **ex-73 · parser-combinator-recursive** — a recursive grammar rule in FParsec (`createParserForwardedToRef`) — verify nested expressions parse. (co-12)
- **ex-74 · dotnet-test-parser** — a `dotnet test` over the parser stage — verify it passes. (co-30)
- **ex-75 · dotnet-test-transpiler** — a `dotnet test` over the transpiler stage — verify it passes. (co-30, co-24)
- **ex-76 · pipeline-end-to-end** — run `source |> lex |> parse |> eval` — verify the whole pipeline yields the value. (co-01)
- **ex-77 · two-parser-fuzz** — a property test feeding random expressions to both parsers — verify they always agree. (co-15)
- **ex-78 · capstone-language-processor** — the capstone: lexer → parser → AST → interpreter + transpiler with tests — verify end-to-end run + green tests. (co-01, co-08, co-17, co-24)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a small but complete language processor in F# — lexer → parser (a hand-written
  recursive-descent/Pratt parser, with an FParsec combinator variant for contrast) → an AST discriminated
  union → **both** a tree-walking interpreter that evaluates programs **and** a transpiler that emits
  equivalent target code — fully covered by `dotnet test`, demonstrating the front-end that every
  compiler/type-checker/linter shares.
- **Concepts exercised**: [ ] a lexer/tokenizer with error handling (co-02, co-03, co-05) [ ] a
  recursive-descent/Pratt parser with correct precedence (co-07, co-09, co-10, co-11) [ ] an FParsec
  combinator parser for contrast (co-12, co-15) [ ] an AST as a discriminated union (co-08) [ ] a
  tree-walking interpreter with scopes/environments via pattern matching (co-17, co-18, co-19) [ ] a
  transpiler emitting target code (co-24, co-26) [ ] `dotnet test` coverage of each stage (co-30).
- **Ordered steps**:
  1. `.../learning/capstone/code/Lexer.fs` — tokenize the source language into a token DU. Verify tests cover
     tokens, whitespace/comments, and a lexer error.
  2. `Parser.fs` — a recursive-descent/Pratt parser → AST discriminated union with correct operator
     precedence, plus an FParsec variant. Verify precedence-sensitive expressions parse to the right tree, and
     that both parsers agree (tests).
  3. `Interpreter.fs` — evaluate the AST with scopes via exhaustive pattern matching; `Transpiler.fs` — emit
     equivalent target code. Verify the interpreter produces correct results and the transpiled output, when
     run, matches the interpreter.
- **Acceptance criteria**: the full pipeline works; precedence is correct; the recursive-descent and FParsec
  parsers agree; interpreter results and transpiler output agree; `dotnet test` covers each stage; the
  guardrail framing is stated.
- **Done bar**: runnable end-to-end + tests green + web-verified.

<!-- Inter-topic capstone spec block: this file (last subject topic of Pass 4) anchors the Pass-4 boundary capstones -->

## Capstone spec — inter-topic: capstone-concurrency-and-systems (Pass-4 boundary)

> **Weight**: `capstone-concurrency-and-systems/_index.md` = **995** (section root, after Pass 4 / topic 89).
> Kind: **subject → full runnable**. Integrates the pass's concurrency + systems-depth topics.

- **Goal**: build a **concurrent, systems-aware, observable service** that ties Pass 4 together — a
  work-processing service using a real concurrency model (CSP-Go **or** actor-Elixir), backed by a
  systems-level component, containerized, and instrumented with SRE golden signals + an SLO — demonstrating
  that concurrency, systems depth, and reliability compose into one operable system.
- **Concepts integrated**: [ ] a concurrency model in anger (Go CSP: goroutines/channels/`context`
  [topic 65] **or** Elixir actors: GenServer/supervision [topic 67]) [ ] a systems-level component (a C
  primitive / memory-aware data path [topics 78/79/80] **or** a justified equivalent) [ ] containerized +
  orchestrated deployment [topic 50, Pass 3] [ ] SRE instrumentation: four golden signals + an SLI/SLO +
  error budget [topic 94] [ ] a symptom-based alert + dashboard.
- **Ordered steps**:
  1. `capstone-concurrency-and-systems/code/` — a concurrent work-processing service in Go (CSP) **or**
     Elixir (actors), with a bounded worker pool / supervised workers and graceful shutdown. Verify it
     processes a concurrent workload with no race (Go `-race`) / clean supervision (Elixir) and shuts down
     gracefully.
  2. Add a systems-level component (or a justified equivalent) and containerize the service. Verify the
     container builds and runs the full workload.
  3. Instrument the four golden signals + an SLI/SLO + error budget; add a symptom-based alert + dashboard.
     Verify the signals expose under load, the SLO alert fires on violation, and the dashboard reflects it.
- **Acceptance criteria**: the concurrency model is used correctly (race-free / properly supervised); the
  service is containerized; golden signals + SLO + alert + dashboard all work; graceful shutdown holds.
- **Done bar**: runnable end-to-end + observable + web-verified.

## Capstone spec — inter-topic: capstone-concurrency-showdown (cross-cutting)

> **Weight**: `capstone-concurrency-showdown/_index.md` = **996** (section root, after Pass 4 / topic 89).
> Kind: **subject → full runnable + comparison artifact**. A deliberate CSP-vs-actor head-to-head.

- **Goal**: solve the **same** concurrent problem twice — once with **CSP-style Go**
  (goroutines/channels/`select`/`context`) and once with the **actor-model Elixir/OTP**
  (GenServer/supervision/"let it crash") — then write a grounded comparison of the two paradigms on the same
  workload: how each handles coordination, backpressure, failure/supervision, and observability.
- **Concepts integrated**: [ ] the same problem in Go CSP [topic 65] and Elixir actors [topic 67] [ ] channel
  coordination + `select` + `context` cancellation (Go) [ ] GenServer + supervision trees + "let it crash"
  (Elixir) [ ] backpressure + failure handling contrasted [ ] a decision write-up: when each model fits.
- **Ordered steps**:
  1. `capstone-concurrency-showdown/go/` — solve the chosen concurrent problem (e.g. a fan-out/fan-in
     pipeline with cancellation + backpressure) in Go. Verify it runs `-race`-clean and handles cancellation
     - a failing worker.
  2. `.../elixir/` — solve the identical problem with GenServer + a supervision tree. Verify it runs and a
     crashing worker is supervised/restarted without taking down the system.
  3. `comparison.md` — contrast the two on coordination, backpressure, failure/supervision, testability, and
     observability, with a concrete "when to reach for which" recommendation grounded in the two
     implementations. Verify each claim points at real behaviour in the two codebases.
- **Acceptance criteria**: both implementations solve the same problem correctly (Go race-free; Elixir
  supervised); the comparison is concrete and evidence-backed, not generic; the recommendation is justified.
- **Done bar**: both runnable end-to-end + comparison artifact + web-verified.

## Read more

**Books**

- **Compilers: Principles, Techniques, and Tools** ("The Dragon Book") — Alfred V. Aho, Monica S. Lam, Ravi
  Sethi, Jeffrey D. Ullman (2nd ed., 2006). The most iconic, field-defining compiler-construction textbook.
- **Engineering a Compiler** — Keith D. Cooper, Linda Torczon (3rd ed., 2022). Rigorous, modern treatment of
  compiler construction, optimization, and code generation.
- **Modern Compiler Implementation in ML** — Andrew W. Appel (1998). Influential, implementation-focused
  compilers text using ML — the closest classic to this topic's F# approach.
- **Crafting Interpreters** — Robert Nystrom (2021). Widely adopted, hands-on guide building a tree-walking
  interpreter and a bytecode VM from scratch; free online. <https://craftinginterpreters.com/>

---

← Previous: [88 · Type Systems](./88-type-systems.md) · Next: [90 · Build Your Own Git](./90-build-your-own-git.md) →
