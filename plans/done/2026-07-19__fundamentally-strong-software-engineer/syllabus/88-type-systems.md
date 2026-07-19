# 88 · Type Systems (By Example, OCaml + Haskell + F# †)

**prd row**: Pass 4 · Concurrency & Systems · By Example · OCaml + Haskell + F# † · Learn 188 /
Drill 288 · Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: what a strong static type system buys you — algebraic data types, sum/product types,
exhaustive pattern matching, parametric polymorphism, Hindley-Milner inference, and typeclasses/modules —
taught in the **ML family from scratch** (OCaml as the workhorse, Haskell for purity/typeclasses), with an
**F# sidebar** connecting it back to the .NET topics. Closes with **applied category theory** (functor/
monad intuition per Bartosz Milewski, CC-licensed) — practical, not abstract.

- **License note (DD-15/DD-21)**: OCaml (LGPL-with-linking-exception), Haskell/GHC (BSD-3), F# (MIT). All
  OSS, runnable with no paid account (DD-20). Milewski's _Category Theory for Programmers_ is
  Creative-Commons.

## Why this exists · the big idea

- **The problem before the solution**: whole categories of bug — nulls, unhandled cases, wrong-shape data
  — are things a program can express and then fail on at runtime. A strong static type system exists to
  make those states unrepresentable, so the class of error is caught before the program ever runs.
- **Keep-this-if-you-forget-everything**: the compiler is a proof assistant — make illegal states
  unrepresentable and let exhaustive matching prove you've handled every case, and a large class of runtime
  bugs simply cannot occur.
- **Big ideas touched**: `correctness-vs-pragmatism` — types shift the dial toward provable-before-run,
  with the compiler proving totality and shape in exchange for some flexibility; `abstraction-and-its-cost`
  — parametric polymorphism, typeclasses/functors, and monads generalize code safely, but they leak the
  theory you must learn to wield them.

## Prerequisites

- **Prior topics**: [topic 23 Functional Programming](./23-functional-programming.md) (immutability, pure
  functions, HOFs), [topic 22 Programming Paradigms](./22-programming-paradigms.md) (typed-functional as one
  paradigm among several), and [topic 13 Just Enough TypeScript](./13-just-enough-typescript.md)
  (a first taste of static types — generics, unions — before the ML-family deep dive).
- **Tools & environment**: an **OCaml** toolchain (opam/dune), a **Haskell** toolchain (GHCup/`ghc`/`cabal`
  or `stack`), and a **.NET** SDK for the F# sidebar; Neovim/VSCode with the respective LSPs (DD-17).
- **Assumed knowledge**: FP fundamentals — recursion, HOFs, immutability (topic 23); paradigm fluency
  (topic 22); basic static-typing exposure — generics, unions (topic 13).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified (licenses, exact match): **OCaml = LGPL-with-linking-exception** (SPDX
  OCaml-LGPL-linking-exception), **GHC/Haskell = BSD-3**, **F# = MIT** (dotnet/fsharp). Milewski's
  _Category Theory for Programmers_ is **CC BY-SA 4.0** (more precise than "Creative-Commons").
- 2026-07-12 — verified: OCaml (opam/dune) and Haskell (GHCup / `ghc` + `cabal` or `stack`) toolchains are
  current; Hindley-Milner inference, typeclasses-vs-modules/functors, and functor/applicative/monad are
  evergreen PL theory, unchanged.

### DD-35 primary-source citations (fetched-and-read)

Every version, license, and theory claim below traces to a primary source fetched and read during
grounding. Unverifiable specifics are marked `[Needs Verification]` and never shipped as fact.

- **Licenses (SPDX-exact)** — **OCaml** is `LGPL-2.1-only WITH OCaml-LGPL-linking-exception`; **GHC/Haskell**
  is `BSD-3-Clause`; **F#** (dotnet/fsharp) is `MIT`; Milewski's _Category Theory for Programmers_ is
  **CC BY-SA 4.0**. (github.com/ocaml/ocaml/blob/trunk/LICENSE, gitlab.haskell.org/ghc/ghc, github.com/dotnet/fsharp, github.com/hmemcpy/milewski-ctfp-pdf)
- **Toolchains** — OCaml via **opam** + **dune**; Haskell via **GHCup** (`ghc`/`cabal`/`stack`); F# via the
  **.NET SDK** (`dotnet fsi`). Left version-unpinned in prose — the language surface taught is evergreen.
  (ocaml.org/install, haskell.org/ghcup, learn.microsoft.com/dotnet/fsharp)
- **Hindley–Milner** (Damas–Milner) inference gives whole-program principal-type inference for the ML core;
  annotations are optional. Verified against Pierce, _Types and Programming Languages_ (2002), ch. 22.
- **Soundness contrast (co-27)** — TypeScript's type system is **deliberately unsound** by design (bivariant
  parameter checks, `any`, type assertions), traded for JS interop; the TS handbook states type-checking is
  not a soundness guarantee. This is the concrete foil for ML soundness. (typescriptlang.org/docs/handbook/type-compatibility.html, "TypeScript Design Goals" non-goal #3)
- **TypeScript 7.0 native port** ("tsgo", Project Corsa) is a Go rewrite of the compiler announced March 2025;
  it changes the _implementation_, not the _type theory_. Treat its GA status as `[Needs Verification]` at
  authoring time — cite it only as an implementation note, never as changing the type system. (devblogs.microsoft.com/typescript/typescript-native-port)
- **Functor / applicative / monad laws** (identity, composition; left/right identity, associativity) are the
  standard laws verified against the Haskell `base` documentation. (hackage.haskell.org/package/base — Data.Functor, Control.Monad)

## Concepts

<!-- co-01 · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (subject). Each example below cites the co-NN it exercises. -->

- **co-01 · static-vs-dynamic** — static typing rejects whole classes of error before the program runs.
- **co-02 · sum-types** — a value is exactly one of several named variants (`Red | Green | Blue`).
- **co-03 · product-types** — a value bundles several fields at once (records, tuples).
- **co-04 · algebraic-data-types** — sums of products compose to model any domain shape precisely.
- **co-05 · illegal-states-unrepresentable** — choosing types so invalid states cannot be constructed.
- **co-06 · pattern-matching** — deconstructing an ADT by its variant, binding the payload.
- **co-07 · exhaustiveness-checking** — the compiler flags any match missing a variant.
- **co-08 · parametric-polymorphism** — generic code over any type (`'a list`, `a -> a`).
- **co-09 · hindley-milner-inference** — principal types inferred whole-program without annotations.
- **co-10 · type-annotations** — explicit type ascriptions where inference needs help or for clarity.
- **co-11 · unit-and-bottom** — the `unit` type (one value) and bottom/never (no value).
- **co-12 · option-type** — `Option`/`Maybe` models absence in the type, replacing null.
- **co-13 · result-type** — `Result`/`Either` models success-or-failure in the type.
- **co-14 · recursive-types** — self-referential ADTs (a tree, an expression) model nested structure.
- **co-15 · type-aliases** — naming a type without creating a distinct one.
- **co-16 · typeclasses** — Haskell's ad-hoc polymorphism: constrained generics over a class of types.
- **co-17 · typeclass-instances** — supplying a type's implementation of a class's methods.
- **co-18 · modules-functors** — OCaml modules and functors (modules parameterized by modules).
- **co-19 · signatures** — module type signatures specify a module's interface.
- **co-20 · higher-kinded-types** — abstracting over type constructors (`f a`, not just `a`).
- **co-21 · functor** — `map`/`fmap` lifts a function over a structure, preserving shape (functor laws).
- **co-22 · applicative** — applying a wrapped function to a wrapped value (`<*>`).
- **co-23 · monad** — sequencing dependent effects with `bind`/`>>=`.
- **co-24 · monad-laws** — left identity, right identity, associativity that a lawful monad obeys.
- **co-25 · map-bind-pipeline** — chaining `map`/`bind` over `Option`/`Result` for total pipelines.
- **co-26 · fsharp-adts** — the F# sidebar: the same ADTs + exhaustive match on .NET.
- **co-27 · soundness** — a sound type system never lets a well-typed program go wrong (TS is unsound by design).
- **co-28 · type-variance** — covariance/contravariance: when `T<A>` is a subtype of `T<B>`.
- **co-29 · phantom-types** — a type parameter carrying compile-time info with no runtime representation.
- **co-30 · newtype-wrapper** — a distinct type over an existing representation for extra safety.

## Worked examples

Colocated under `type-systems/learning/code/`; OCaml primary + Haskell + F# sidebar (DD-20/DD-30). Contiguous
`ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · ocaml-variant-define** — `type color = Red | Green | Blue` — verify each constructor type-checks. (co-02)
- **ex-02 · ocaml-record-define** — `type point = { x: int; y: int }` — verify field access works. (co-03)
- **ex-03 · ocaml-adt-combine** — a variant whose case carries a record — verify the ADT compiles. (co-04)
- **ex-04 · illegal-state-model** — model a connection state so "connected without a socket" cannot be built — verify the bad state won't compile. (co-05)
- **ex-05 · ocaml-match-variant** — `match c with Red -> ... | Green -> ...` — verify each arm runs. (co-06)
- **ex-06 · ocaml-exhaustive-warn** — omit the `Blue` arm — verify the compiler warns non-exhaustive. (co-07)
- **ex-07 · ocaml-poly-list** — `List.length : 'a list -> int` on two element types — verify both work. (co-08)
- **ex-08 · ocaml-inference** — `let id x = x` — verify inferred type is `'a -> 'a`. (co-09)
- **ex-09 · ocaml-annotation** — `let f (x: int) : int = x + 1` — verify the annotation is accepted. (co-10)
- **ex-10 · ocaml-unit** — `()` and a `unit`-returning `print` — verify the type is `unit`. (co-11)
- **ex-11 · ocaml-option-some** — `Some 5` — verify its type is `int option`. (co-12)
- **ex-12 · ocaml-option-none** — `None` for a missing lookup — verify the `None` branch. (co-12)
- **ex-13 · ocaml-option-match** — `match o with Some v -> v | None -> 0` — verify both arms. (co-12, co-06)
- **ex-14 · ocaml-result-ok** — `Ok x` / `Error e` — verify each constructor. (co-13)
- **ex-15 · ocaml-recursive-type** — `type tree = Leaf | Node of tree * int * tree` — verify it compiles. (co-14)
- **ex-16 · ocaml-type-alias** — `type name = string` — verify `name` is interchangeable with `string`. (co-15)
- **ex-17 · haskell-data-define** — `data Color = Red | Green | Blue` — verify it type-checks. (co-02)
- **ex-18 · haskell-record** — `data Point = Point { x :: Int, y :: Int }` — verify field accessors. (co-03)
- **ex-19 · haskell-maybe** — `Just 5` / `Nothing` — verify the `Maybe Int` type. (co-12)
- **ex-20 · haskell-either** — `Left e` / `Right v` — verify the `Either` type. (co-13)
- **ex-21 · haskell-pattern-match** — `case c of Red -> ...` — verify each branch. (co-06)
- **ex-22 · haskell-exhaustive-warn** — compile with `-Wincomplete-patterns` and omit a case — verify the warning. (co-07)
- **ex-23 · haskell-poly-id** — `id :: a -> a` — verify it works at two types. (co-08)
- **ex-24 · haskell-inference** — omit the signature — verify GHC infers the most general type. (co-09)
- **ex-25 · fsharp-du** — F# `type Color = Red | Green | Blue` sidebar — verify it compiles on .NET. (co-26, co-02)
- **ex-26 · fsharp-match** — F# exhaustive `match` over the DU — verify FS0025 on a missing case. (co-26, co-06)

### Intermediate

- **ex-27 · ocaml-map-function** — `List.map` over a list — verify the mapped result. (co-08)
- **ex-28 · ocaml-fold** — `List.fold_left (+) 0` — verify the sum. (co-08)
- **ex-29 · ocaml-option-map** — `Option.map` over `Some`/`None` — verify shape preserved. (co-12, co-21)
- **ex-30 · ocaml-option-bind** — `Option.bind` chaining two lookups — verify `None` short-circuits. (co-12, co-23)
- **ex-31 · ocaml-module-define** — `module Stack = struct ... end` — verify a member resolves. (co-18)
- **ex-32 · ocaml-signature** — `module type STACK` — verify it constrains the module. (co-19)
- **ex-33 · ocaml-functor** — `module Make (E: EQ) = struct ... end` — verify the functor compiles. (co-18)
- **ex-34 · ocaml-functor-apply** — apply the functor to a concrete module — verify the produced module works. (co-18)
- **ex-35 · haskell-typeclass-define** — `class MyEq a where eq :: a -> a -> Bool` — verify it compiles. (co-16)
- **ex-36 · haskell-typeclass-instance** — `instance MyEq Color where ...` — verify `eq Red Red`. (co-17)
- **ex-37 · haskell-show-instance** — `instance Show Color` — verify `show Red` renders. (co-17)
- **ex-38 · haskell-functor-instance** — `instance Functor Box` — verify `fmap` over it. (co-21)
- **ex-39 · haskell-fmap** — `fmap (+1) (Just 4)` — verify `Just 5`. (co-21)
- **ex-40 · haskell-applicative** — `Just (+1) <*> Just 4` — verify `Just 5`. (co-22)
- **ex-41 · haskell-monad-bind** — `Just 4 >>= \x -> Just (x+1)` — verify `Just 5`. (co-23)
- **ex-42 · haskell-do-notation** — a `do` block over `Maybe` — verify it desugars to `>>=`. (co-23)
- **ex-43 · option-pipeline** — chain `Option.map`/`bind` in OCaml — verify a total pipeline. (co-25)
- **ex-44 · result-pipeline** — chain `Either` in Haskell — verify the first `Left` wins. (co-25, co-13)
- **ex-45 · hkt-example** — a function generic over `f a` (higher-kinded) — verify it compiles. (co-20)
- **ex-46 · newtype-haskell** — `newtype UserId = UserId Int` — verify it is distinct from `Int`. (co-30)
- **ex-47 · phantom-type** — `data Tagged tag a = Tagged a` — verify the phantom `tag` carries no runtime data. (co-29)
- **ex-48 · type-alias-vs-newtype** — compare `type` alias vs `newtype` — verify only `newtype` blocks mixing. (co-15, co-30)
- **ex-49 · fsharp-record-copy** — F# `{ r with F = v }` sidebar — verify copy-update. (co-26, co-03)
- **ex-50 · fsharp-option-map** — F# `Option.map` sidebar — verify it maps `Some`. (co-26, co-12)
- **ex-51 · recursive-eval** — evaluate an OCaml expression tree via match — verify the result. (co-14, co-06)
- **ex-52 · variance-intuition** — an immutable list is covariant; a mutable ref is not — verify the intuition with a compiled example. (co-28)

### Advanced

- **ex-53 · functor-law-check** — verify `fmap id = id` on a custom functor — verify the law holds. (co-21)
- **ex-54 · monad-law-left-id** — verify `return a >>= f == f a` — verify equality. (co-24)
- **ex-55 · monad-law-right-id** — verify `m >>= return == m` — verify equality. (co-24)
- **ex-56 · monad-law-assoc** — verify `(m >>= f) >>= g == m >>= (\x -> f x >>= g)` — verify associativity. (co-24)
- **ex-57 · state-monad** — a minimal `State` monad in Haskell — verify threaded state. (co-23)
- **ex-58 · reader-monad** — a minimal `Reader` — verify injected environment. (co-23)
- **ex-59 · maybe-monad-chain** — safe-division pipeline over `Maybe` — verify divide-by-zero yields `Nothing`. (co-23, co-25)
- **ex-60 · either-error-chain** — railway error handling over `Either` — verify the error path carries a message. (co-25, co-13)
- **ex-61 · applicative-validation** — accumulate multiple errors with an applicative — verify all errors collected. (co-22)
- **ex-62 · ocaml-result-bind-chain** — `Result.bind` pipeline in OCaml — verify short-circuit on `Error`. (co-25, co-23)
- **ex-63 · functor-over-tree** — `fmap` over a custom tree — verify structure preserved. (co-21, co-14)
- **ex-64 · traversable** — turn a `list (Option a)` into `Option (list a)` — verify one `None` collapses it. (co-25)
- **ex-65 · gadt-taste** — a small OCaml GADT typed-expression evaluator — verify types rule out ill-typed terms. (co-04, co-14)
- **ex-66 · typeclass-constraint** — `(Eq a) => a -> a -> Bool` — verify the constraint is required. (co-16)
- **ex-67 · multiparam-intuition** — combine two constraints `(Eq a, Show a)` — verify both dispatch. (co-16)
- **ex-68 · module-functor-set** — `Set.Make (Ord)` in OCaml — verify the produced set works. (co-18)
- **ex-69 · phantom-units** — phantom-typed metres vs feet — verify mixing them won't compile. (co-29)
- **ex-70 · newtype-smart-constructor** — a validated `Email` newtype with a smart constructor — verify invalid input is rejected. (co-30)
- **ex-71 · illegal-state-refactor** — refactor a stringly-typed status to an ADT — verify bad statuses become uncompilable. (co-05, co-04)
- **ex-72 · exhaustive-refactor** — add a variant, let the compiler find every match to update — verify all sites flagged. (co-07)
- **ex-73 · soundness-demo** — show a TS assertion that lies at runtime vs OCaml rejecting the equivalent — verify the contrast. (co-27)
- **ex-74 · inference-limits** — a case needing an annotation (e.g. the monomorphism restriction) — verify why inference stops. (co-09, co-10)
- **ex-75 · fsharp-monad-ce** — an F# computation expression sidebar for `Option` — verify it sequences like `bind`. (co-26, co-23)
- **ex-76 · cross-lang-adt** — the same domain ADT in OCaml, Haskell, and F# — verify all three compile and agree. (co-04, co-26)
- **ex-77 · category-intuition-writeup** — `intuition.md` tying `map`/`bind` to functor/monad (Milewski, CC) — verify the write-up references the concrete code. (co-21, co-23)
- **ex-78 · capstone-type-safe-domain** — the capstone: a domain where illegal states are unrepresentable, with a `map`/`bind` pipeline, in all three languages — verify end-to-end compile + run. (co-05, co-07, co-25, co-26)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: model a small domain so that **illegal states are unrepresentable** — algebraic data types +
  exhaustive pattern matching in OCaml, a Haskell version using a typeclass for ad-hoc polymorphism, and an
  F# sidebar — then build a `map`/`bind` pipeline over an `Option`/`Result`-style type with the functor/
  monad intuition written up plainly, showing types as a correctness tool.
- **Concepts exercised**: [ ] ADTs (sum + product) making illegal states unrepresentable (co-04, co-05) [ ]
  exhaustive pattern matching (compiler-checked total coverage) (co-06, co-07) [ ] parametric polymorphism +
  HM inference (co-08, co-09) [ ] a typeclass (Haskell) vs a module/functor (OCaml) (co-16, co-18) [ ] a
  functor/monad `map`/`bind` pipeline with grounded category-theory intuition (co-21, co-23, co-25) [ ] the
  F# sidebar (co-26).
- **Ordered steps**:
  1. `.../learning/capstone/code/domain.ml` — model the domain with ADTs + exhaustive matching in OCaml.
     Verify the compiler rejects a non-exhaustive match and accepts the total one.
  2. `Domain.hs` — the Haskell version using a typeclass; `domain.fs` — the F# sidebar. Verify both compile
     and reproduce the OCaml behaviour.
  3. Add a `map`/`bind` pipeline over an `Option`/`Result`-style type + `intuition.md` explaining the
     functor/monad pattern (Milewski, CC). Verify the pipeline runs and the write-up ties the abstraction to
     the concrete code.
- **Acceptance criteria**: illegal states are unrepresentable; pattern matching is exhaustive (compiler-
  proven); the `map`/`bind` pipeline works; the category-theory intuition is concrete, not hand-wavy; all
  three versions (OCaml, Haskell, F#) compile.
- **Done bar**: runnable end-to-end (OCaml + Haskell + F#) + web-verified.

## Read more

**Books**

- **Types and Programming Languages** — Benjamin C. Pierce (2002). The definitive graduate-level textbook on type theory; the standard reference across the field.
- **Practical Foundations for Programming Languages**, 2nd ed. — Robert Harper (2016). Rigorous, comprehensive treatment of programming language semantics and type systems.
- **Real World OCaml**, 2nd ed. — Yaron Minsky, Anil Madhavapeddy, Jason Hickey (2022). The canonical practical guide to OCaml and ML-family typed functional programming; open access. <https://realworldocaml.org/>
- **Programming in Haskell**, 2nd ed. — Graham Hutton (2016). Widely adopted, rigorous introduction to Haskell and its type system.
- **Learn You a Haskell for Great Good!** — Miran Lipovača (2011). The most widely recommended accessible introduction to Haskell's type system; free online. <https://learnyouahaskell.github.io/>
- **Software Foundations** — Benjamin C. Pierce et al. Free, machine-checked introduction to programming language theory and type systems using a proof assistant. <https://softwarefoundations.cis.upenn.edu/>

---

← Previous: [87 · Just Enough F#](./87-just-enough-fsharp.md) · Next: [89 · Compilers, Parsers & Transpilers](./89-compilers-parsers-and-transpilers.md) →
