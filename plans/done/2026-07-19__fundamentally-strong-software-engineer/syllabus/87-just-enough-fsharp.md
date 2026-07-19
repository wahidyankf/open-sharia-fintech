# 87 · Just Enough F# (Primer, F# †)

**prd row**: Pass 4 · Concurrency & Systems · Primer · F# † · Learn 187 / Drill 287 ·
Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: **just enough F#** to be productive in
[`89-compilers-parsers-and-transpilers`](./89-compilers-parsers-and-transpilers.md). The `dotnet` F#
toolchain, let-bindings and immutability by default, discriminated unions + records, exhaustive pattern
matching, the pipeline (`|>`) style, and the type system. F# is the ML-family language on .NET — its
algebraic data types and pattern matching are exactly what make an AST and an evaluator natural, which is
why it precedes the compilers topic.

## Why this exists · the big idea

- **The problem before the solution**: modelling a compiler's AST — or any domain with many shapes and
  states — in a language without sum types means classes, visitors, and runtime checks for the cases you
  forgot. F# is here to give you algebraic data types and exhaustive matching, so the shapes are exact and
  a missing case is a compile-time warning.
- **Keep-this-if-you-forget-everything**: with immutability by default and discriminated unions matched
  exhaustively, illegal states become hard to build and forgotten cases impossible to ignore — the
  compiler carries the load.
- **Big ideas touched**: `taming-state` — immutability by default and let-bindings drop mutable shared
  state as the default, so data flows through `|>` pipelines instead of being mutated in place;
  `abstraction-and-its-cost` — discriminated unions and records model a domain precisely (the AST the
  compilers topic needs), at the cost of learning to think in types and pattern matches.

## Prerequisites

- **Prior topics**: [topic 23 Functional Programming](./23-functional-programming.md) (immutability, pure
  functions, higher-order functions, recursion) and
  [topic 8 Object-Oriented Programming Essentials](./08-object-oriented-programming-essentials.md) (F# is
  functional-first but interoperates with .NET's object model).
- **Tools & environment**: a macOS/Linux/Windows machine; the **.NET SDK** (`dotnet`), pinned to a current
  LTS, which ships the F# compiler and FSI (the F# Interactive REPL); Neovim/VSCode with the F# LSP
  (Ionide/FSAutoComplete, DD-17). Keep the SDK version unpinned in prose — re-pull at authoring time.
- **Assumed knowledge**: functional fundamentals — immutability, first-class functions, recursion (topic 23);
  types and interfaces from any prior typed language (topic 08); running a CLI build/run tool (topic 05).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: keep ".NET SDK current LTS" unpinned in shipped text. The F# language surface used
  here — let-bindings, immutability by default, discriminated unions, records, active patterns, exhaustive
  match, the `|>` pipeline, and `Option`/`Result` — is stable and evergreen. `dotnet` subcommands
  (`new`/`run`/`build`/`test`/`fsi`) are current/unchanged. (learn.microsoft.com/dotnet/fsharp)
- 2026-07-12 — verified: the F# toolchain (dotnet SDK, and FParsec for the compilers topic that follows) is
  correctly left version-unpinned here; note the exact SDK and FParsec versions as "to verify" at authoring
  time.

### DD-35 primary-source citations (fetched-and-read)

Every version, subcommand, and language claim below traces to a primary source fetched and read during
grounding. Unverifiable specifics are marked `[Needs Verification]` and never shipped as fact.

- **F# 10** is the current language version, shipping with **.NET 10** (an LTS release, GA November 2025).
  Keep the SDK version **unpinned in prose** ("a current .NET LTS") — the language surface taught here is
  evergreen. (learn.microsoft.com/dotnet/fsharp/whats-new, dotnet.microsoft.com/download/dotnet/10.0)
- **`dotnet` CLI subcommands** used — `dotnet new`, `dotnet run`, `dotnet build`, `dotnet test`,
  `dotnet fsi` — are current and unchanged. `dotnet fsi` is the F# Interactive (FSI) REPL.
  (learn.microsoft.com/dotnet/core/tools, learn.microsoft.com/dotnet/fsharp/tools/fsharp-interactive)
- **Language features** — let-bindings, `mutable` + `<-`, records, discriminated unions, exhaustive
  `match ... with`, incomplete-match compiler **warning FS0025**, active patterns `(|Name|_|)`,
  `Option`/`Result`, pipeline `|>`, composition `>>`, `List.map`/`filter`/`fold`, `let rec` and
  `let rec ... and` — all verified against the F# language reference. (learn.microsoft.com/dotnet/fsharp/language-reference)
- **Type inference** is Hindley–Milner-style (whole-program inference); explicit annotations are optional.
  (learn.microsoft.com/dotnet/fsharp/language-reference/type-inference)
- **Expecto 11.1.0** is a current F# test framework used for the `dotnet test` examples; the built-in
  `dotnet test` runner (via `Microsoft.NET.Test.Sdk`) also works with no third-party dependency.
  Pin the exact Expecto version **at authoring time** — treat 11.1.0 as `[Needs Verification]` when code
  is written. (github.com/haf/expecto/releases, nuget.org/packages/Expecto)
- **Ionide / FSAutoComplete** provides the F# LSP for Neovim/VSCode (DD-17); versions float, left
  unpinned. (ionide.io)

## Concepts

<!-- co-01 · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (Primer, subject band). Each example below cites the co-NN it exercises. -->

- **co-01 · dotnet-new** — `dotnet new console -lang F#` scaffolds a runnable F# project with an `.fsproj`.
- **co-02 · dotnet-run** — `dotnet run` compiles and executes the project's entry point.
- **co-03 · dotnet-build** — `dotnet build` compiles without running; surfaces warnings and errors.
- **co-04 · dotnet-test** — `dotnet test` runs a test project (Expecto or the built-in runner).
- **co-05 · dotnet-fsi** — `dotnet fsi` is the F# Interactive REPL for evaluating expressions and scripts.
- **co-06 · let-binding** — `let` binds an immutable value; rebinding a name is shadowing, not mutation.
- **co-07 · mutable-binding** — `let mutable` plus the `<-` assignment operator opts into in-place mutation.
- **co-08 · function-definition** — `let f x = ...` defines a curried function; application is juxtaposition.
- **co-09 · significant-whitespace** — indentation delimits blocks; there are no braces or semicolons.
- **co-10 · type-inference** — Hindley–Milner inference derives types; annotations are optional.
- **co-11 · tuples** — `(a, b)` groups heterogeneous values; `let (x, y) = ...` destructures them.
- **co-12 · lists** — immutable singly-linked lists: `[1; 2; 3]`, cons `x :: xs`, ranges `[1..5]`.
- **co-13 · records** — named-field product types with structural copy-and-update `{ r with F = v }`.
- **co-14 · discriminated-unions** — sum types: `type Shape = Circle of float | Rect of float * float`.
- **co-15 · pattern-matching** — `match ... with` deconstructs unions, records, tuples, and literals.
- **co-16 · exhaustiveness-warning** — a match missing a union case raises compiler warning FS0025.
- **co-17 · active-patterns** — `(|Name|_|)` defines reusable, composable custom match patterns.
- **co-18 · option-type** — `Option<'a>` (`Some`/`None`) models absence without null.
- **co-19 · result-type** — `Result<'a,'e>` (`Ok`/`Error`) models success-or-failure for total functions.
- **co-20 · pipeline-operator** — `|>` feeds a value into the next function, left-to-right data flow.
- **co-21 · function-composition** — `>>` composes two functions into one without naming the argument.
- **co-22 · higher-order-functions** — `List.map`/`filter`/`fold` take functions as arguments.
- **co-23 · recursion** — `let rec` enables self-reference; `let rec ... and` for mutual recursion.
- **co-24 · recursive-du** — a self-referential DU (an expression tree) is the AST the compilers topic needs.
- **co-25 · dotnet-interop** — `open System` and dotted method calls give access to the .NET library.
- **co-26 · modules-namespaces** — `module` and `namespace` group and qualify definitions.

## Worked examples

Colocated under `just-enough-fsharp/learning/code/`; each runnable via `dotnet` (DD-20/DD-30). Contiguous
`ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · hello-console** — `dotnet new console -lang F#` then `dotnet run` printing `Hello` — verify the greeting prints. (co-01, co-02)
- **ex-02 · fsi-eval** — evaluate `1 + 1` in `dotnet fsi` — verify FSI echoes `val it : int = 2`. (co-05)
- **ex-03 · let-immutable** — `let x = 5` then print — verify `5` prints and reassigning `x` is rejected. (co-06)
- **ex-04 · let-shadowing** — rebind `let x = x + 1` in an inner scope — verify shadowing changes the visible value, not the original. (co-06)
- **ex-05 · mutable-counter** — `let mutable n = 0` then `n <- n + 1` — verify `n` is `1` after assignment. (co-07)
- **ex-06 · function-add** — `let add a b = a + b` — verify `add 2 3` returns `5`. (co-08)
- **ex-07 · function-typed** — annotate `let add (a: int) (b: int) : int` — verify it compiles and behaves identically. (co-08, co-10)
- **ex-08 · type-inference-infer** — `let square x = x * x` with no annotation — verify inference fixes `x : int`. (co-10)
- **ex-09 · indentation-block** — a nested `let` inside a function body via indentation — verify de-indenting breaks compilation. (co-09)
- **ex-10 · tuple-pair** — `let p = (1, "a")` — verify `fst p` is `1` and `snd p` is `"a"`. (co-11)
- **ex-11 · tuple-destructure** — `let (a, b) = (10, 20)` — verify `a` and `b` bind to `10` and `20`. (co-11)
- **ex-12 · list-literal** — `[1; 2; 3]` — verify `List.length` returns `3`. (co-12)
- **ex-13 · list-cons** — `0 :: [1; 2]` — verify the result is `[0; 1; 2]`. (co-12)
- **ex-14 · list-range** — `[1..5]` — verify it produces `[1; 2; 3; 4; 5]`. (co-12)
- **ex-15 · record-define** — `type Person = { Name: string; Age: int }` — verify a value constructs and compiles. (co-13)
- **ex-16 · record-construct** — `{ Name = "Ada"; Age = 30 }` — verify field access `p.Name` returns `"Ada"`. (co-13)
- **ex-17 · record-copy** — `{ p with Age = 31 }` — verify the copy has `Age = 31` and the original is unchanged. (co-13, co-06)
- **ex-18 · du-define** — `type Shape = Circle of float | Rect of float * float` — verify both cases compile. (co-14)
- **ex-19 · du-construct** — `Circle 1.0` and `Rect (2.0, 3.0)` — verify each has type `Shape`. (co-14)
- **ex-20 · match-literal** — `match n with 0 -> "zero" | _ -> "other"` — verify `0` maps to `"zero"`. (co-15)
- **ex-21 · match-wildcard** — a `_` catch-all arm — verify unmatched inputs fall through to it. (co-15)
- **ex-22 · option-some** — `Some 5` — verify pattern `Some v` binds `v = 5`. (co-18)
- **ex-23 · option-none** — `None` for a missing lookup — verify the `None` arm runs. (co-18)
- **ex-24 · pipeline-simple** — `5 |> square` — verify it equals `square 5`. (co-20)
- **ex-25 · hof-map** — `List.map square [1; 2; 3]` — verify the result is `[1; 4; 9]`. (co-22)
- **ex-26 · rec-factorial** — `let rec fact n = if n <= 1 then 1 else n * fact (n - 1)` — verify `fact 5` is `120`. (co-23)

### Intermediate

- **ex-27 · pipeline-chain** — `[1..10] |> List.filter even |> List.sum` — verify the chain sums the evens. (co-20, co-22)
- **ex-28 · compose-operator** — `let f = square >> string` — verify `f 3` returns `"9"`. (co-21)
- **ex-29 · filter-list** — `List.filter (fun x -> x > 2) [1; 2; 3; 4]` — verify the result is `[3; 4]`. (co-22)
- **ex-30 · fold-sum** — `List.fold (+) 0 [1; 2; 3]` — verify it returns `6`. (co-22)
- **ex-31 · map-filter-pipe** — a `|>` pipeline of `map` then `filter` — verify the ordered transform is correct. (co-20, co-22)
- **ex-32 · record-pattern** — `match p with { Age = 0 } -> ...` — verify field patterns bind and match. (co-15, co-13)
- **ex-33 · du-match-exhaustive** — `match shape with Circle r -> ... | Rect (w, h) -> ...` — verify both cases handled, no warning. (co-15, co-16)
- **ex-34 · du-missing-case-warning** — omit the `Rect` arm — verify the compiler emits warning FS0025. (co-16)
- **ex-35 · option-match** — `match opt with Some v -> v | None -> 0` — verify both arms behave. (co-18, co-15)
- **ex-36 · option-map** — `Option.map square (Some 4)` — verify it returns `Some 16`. (co-18, co-22)
- **ex-37 · option-default-value** — `Option.defaultValue 0 None` — verify it returns `0`. (co-18)
- **ex-38 · result-ok** — `Ok 42` — verify pattern `Ok v` binds `v = 42`. (co-19)
- **ex-39 · result-error** — `Error "bad input"` — verify the `Error` arm carries the message. (co-19)
- **ex-40 · result-match** — `match r with Ok v -> ... | Error e -> ...` — verify both paths run. (co-19, co-15)
- **ex-41 · result-bind** — chain `Result.bind` over two fallible steps — verify a mid-chain `Error` short-circuits. (co-19)
- **ex-42 · active-pattern-parse** — `let (|Int|_|) s = ...` parsing a string to int — verify it returns `Some`/`None`. (co-17)
- **ex-43 · active-pattern-match** — use `(|Int|_|)` inside a `match` — verify numeric strings take the `Int` arm. (co-17, co-15)
- **ex-44 · tuple-return** — a function returning `(quotient, remainder)` — verify both components are correct. (co-11)
- **ex-45 · list-map-record** — `List.map (fun p -> p.Name) people` — verify it extracts the names. (co-12, co-13, co-22)
- **ex-46 · nested-du** — a DU case carrying a record payload — verify construction and matching both work. (co-14, co-13)
- **ex-47 · guard-clause** — `match n with x when x > 0 -> ...` — verify the `when` guard gates the arm. (co-15)
- **ex-48 · list-pattern** — `match xs with [] -> ... | x :: rest -> ...` — verify head/tail decomposition. (co-15, co-12)
- **ex-49 · rec-list-sum** — a recursive `sum` over a list via head/tail — verify `sum [1;2;3]` is `6`. (co-23, co-12)
- **ex-50 · mutual-recursion** — `let rec isEven ... and isOdd ...` — verify the mutually-recursive pair terminates correctly. (co-23)
- **ex-51 · module-define** — `module Math = let pi = 3.14159` — verify `Math.pi` resolves. (co-26)
- **ex-52 · namespace-open** — `open System` then `Console.WriteLine` — verify the .NET call runs. (co-26, co-25)

### Advanced

- **ex-53 · expr-tree-define** — `type Expr = Num of int | Add of Expr * Expr | Mul of Expr * Expr` — verify the recursive DU compiles. (co-24, co-14)
- **ex-54 · expr-tree-construct** — build `Add (Num 1, Mul (Num 2, Num 3))` — verify it has type `Expr`. (co-24)
- **ex-55 · expr-eval-recursive** — `let rec eval e = match e with ...` — verify `eval` of the tree returns `7`. (co-24, co-23, co-15)
- **ex-56 · expr-eval-nested** — evaluate a deeply nested expression — verify the recursion yields the right total. (co-24)
- **ex-57 · expr-fold** — a generic `fold` collapsing the tree to a value — verify it counts nodes correctly. (co-24, co-22)
- **ex-58 · exhaustive-eval-warning** — add a `Sub` case to `Expr` but not to `eval` — verify FS0025 flags the gap. (co-16, co-24)
- **ex-59 · option-in-eval** — a variable lookup returning `Option` — verify an unbound variable yields `None`. (co-18, co-24)
- **ex-60 · result-in-eval** — division returning `Result` — verify divide-by-zero returns `Error`, not an exception. (co-19, co-24)
- **ex-61 · pipeline-eval** — `input |> parse |> eval` — verify the pipeline threads the expression to a result. (co-20, co-24)
- **ex-62 · active-pattern-token** — an active pattern classifying a character as digit/operator — verify tokens are tagged. (co-17)
- **ex-63 · record-with-du-field** — a record whose field is an `Expr` — verify construction and matching. (co-13, co-14)
- **ex-64 · generic-function** — `let swap (a, b) = (b, a)` inferred as `'a * 'b -> 'b * 'a` — verify it works on any pair. (co-10)
- **ex-65 · hof-compose-pipeline** — combine `>>` and `|>` in one transform — verify the composed pipeline is correct. (co-21, co-20)
- **ex-66 · fold-build-string** — fold an `Expr` into its infix string form — verify the rendered string matches. (co-22, co-24)
- **ex-67 · list-of-du** — process a `Shape list` — verify each shape is handled. (co-12, co-14, co-15)
- **ex-68 · area-dispatch** — `match shape with Circle r -> pi*r*r | Rect (w,h) -> w*h` — verify each area is correct. (co-15, co-14)
- **ex-69 · option-sequence** — traverse a `list<Option>` to an `Option<list>` — verify one `None` collapses the whole. (co-18)
- **ex-70 · result-collect** — collect a `list<Result>` into `Result<list,_>` — verify the first `Error` wins. (co-19)
- **ex-71 · interop-datetime** — `System.DateTime.Now.Year` — verify the .NET property returns the current year. (co-25)
- **ex-72 · interop-string-method** — `"abc".ToUpper()` — verify it returns `"ABC"`. (co-25)
- **ex-73 · module-organize** — group `Expr` + `eval` in a `module` — verify qualified access compiles. (co-26, co-24)
- **ex-74 · dotnet-test-expecto** — an Expecto test on `eval` — verify `dotnet test` reports it passing. (co-04)
- **ex-75 · dotnet-test-assert** — assert `eval (Add (Num 1, Num 2)) = 3` — verify the assertion passes. (co-04, co-24)
- **ex-76 · property-immutability** — copy-update a record — verify the source binding is untouched. (co-06, co-13)
- **ex-77 · railway-pipeline** — a full `Result.bind` chain (parse → validate → eval) — verify success and error paths. (co-19, co-20)
- **ex-78 · capstone-fsharp-evaluator** — the capstone: an `Expr` evaluator app with `dotnet test` — verify end-to-end run and passing test. (co-24, co-15, co-19, co-20)

## Capstone spec — intra-topic (primer → light consolidation)

- **Goal**: build a small F# console app that exercises the primer's surface — immutable let-bindings, a
  discriminated union + a record, exhaustive pattern matching, the `|>` pipeline, and an `Option`/`Result`
  return — runnable via `dotnet run` with a `dotnet test`, proving readiness for the compilers topic.
- **Concepts exercised**: [ ] immutable let-bindings (co-06) [ ] a discriminated union (co-14) [ ] a record
  (co-13) [ ] exhaustive pattern matching (co-15, co-16) [ ] the `|>` pipeline (co-20) [ ] `Option`/`Result`
  (co-18, co-19) [ ] a recursive DU + evaluator (co-24, co-23) [ ] a `dotnet test` (co-04).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — a console app defining a discriminated union + record and transforming
     data through a `|>` pipeline. Verify `dotnet run` produces the expected output.
  2. Add an exhaustive `match` over the union and a function returning `Result`. Verify the compiler reports
     no missing-case warning and the error path returns `Error`, not an exception.
  3. Add a small recursive DU (an expression tree) with a recursive evaluator + a `dotnet test`. Verify the
     evaluator returns correct results and the test passes.
- **Acceptance criteria**: immutability and the pipeline style work; the union/record and exhaustive match
  compile warning-free; `Option`/`Result` handles the error path; the recursive evaluator is correct;
  `dotnet test` passes.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Domain Modeling Made Functional** — Scott Wlaschin (2018). Canonical guide to applying F#'s type system
  and functional idioms to domain-driven design.
- **Get Programming with F#** — Isaac Abraham (2018). Widely recommended step-by-step primer for .NET
  developers learning F#.
- **Stylish F#** — Kit Eason (2018). Focused guide to idiomatic, elegant F# style for working engineers.

**Papers & articles**

- **F# for Fun and Profit** — Scott Wlaschin. The most widely cited free resource for practical,
  ML-family functional-first F# idioms. <https://fsharpforfunandprofit.com/>

---

← Previous: [86 · Lisp](./86-lisp.md) · Next: [88 · Type Systems](./88-type-systems.md) →
