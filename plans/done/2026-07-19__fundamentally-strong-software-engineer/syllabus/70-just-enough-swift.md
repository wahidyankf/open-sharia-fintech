# 70 · Just Enough Swift (Primer, Swift †)

**prd row**: Pass 4 · Concurrency & Systems · Primer · Swift † · Learn 170 / Drill 270 ·
Nvim-ready Partial · VSCode-ready Partial. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: **just enough Swift** to be productive in
[`71-ios-app-development`](./71-ios-app-development.md), taught from the `swift` REPL / `swiftc` CLI
**before** the Xcode-bound topic. Syntax, optionals, structs vs classes, enums with associated values,
protocols, closures, and an `async`/`await` _preview_.

## Why this exists · the big idea

- **The problem before the solution**: iOS in topic 71 is Xcode-bound and dense — learning Swift's value
  semantics, optionals, and concurrency from the plain `swiftc` CLI first strips away the IDE so the
  language itself is what you actually learn.
- **Keep-this-if-you-forget-everything**: Swift defaults to value types (structs) — copies don't alias, so
  shared mutable state is opt-in (a class) rather than the default you fight.
- **Big ideas touched**: `taming-state` — value semantics and optionals make mutation and absence explicit
  instead of ambient; `abstraction-and-its-cost` — protocols and enums-with-associated-values buy
  expressive modeling you pay for in language surface.

## Prerequisites

- **Prior topics**: [topic 8 Object-Oriented Programming Essentials](./08-object-oriented-programming-essentials.md) (types,
  classes) and [topic 68 Just Enough Kotlin](./68-just-enough-kotlin.md) (null-safety/optionals intuition
  transfers).
- **Tools & environment**: a **macOS** machine (Swift toolchain; Xcode not yet required); the `swift` REPL
  - `swiftc` from the CLI; Neovim/VSCode (DD-17). (Linux Swift works for the CLI examples.)
- **Assumed knowledge**: classes/structs + types (topic 08); optional/nullable thinking (topic 68).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: keep the version unpinned in shipped text. Current stable is **Swift 6.3**
  (2026-03-24; 6.4 in beta — re-pull at authoring time). `swift` REPL / `swiftc`, optionals, structs-vs-
  classes, enums-with-associated-values, protocols, closures, and `async`/`await` are unchanged. Swift is
  open source and cross-platform (Swift 6.3 even shipped an official Android SDK), so the Linux-CLI framing
  holds. (swift.org/blog)

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to an official swift.org / docs.swift.org (The Swift Programming Language, TSPL)
> page the pre-authoring `web-researcher` sweep fetched and read. `[Needs Verification]` marks items not
> captured verbatim or with live currency risk. Re-pull the version line immediately before publish.

- **Version** — current stable is **Swift 6.3** (initial 2026-03-24), with patch **6.3.3** on the release
  track (~2026-06-30) and **6.4 in beta** at fetch time — `[Needs Verification]` on the exact patch/6.4-GA
  status; keep the version UNPINNED in shipped prose. Swift is open source + cross-platform (an official
  Android SDK shipped in the 6.3 line), so the Linux-`swiftc` framing holds. `[Verified]` on 6.3-stable +
  open-source/cross-platform. (swift.org/blog, swift.org/download)
- **Toolchain** — `swift` launches the REPL / runs a package; `swiftc file.swift` compiles a standalone
  executable. The exact `swiftc` man-page wording was not captured verbatim — `[Needs Verification]` on a
  verbatim `swiftc` quote, `[Verified]` on the REPL + compile behavior (swift.org/getting-started).
- **Optionals** — TSPL "Optionals": "You use optionals in situations where a value may be absent. An
  optional represents two possibilities: Either there is a value ... or there isn't a value at all." `nil`
  = "the absence of a value"; optional binding (`if let`/`guard let`) "find out whether an optional
  contains a value, and if so, to make that value available"; the nil-coalescing operator `??` "unwraps an
  optional ... if it contains a value, or returns a default value ... if the optional is nil"; forced
  unwrapping `!` "trigger[s] a runtime error if the optional's value is nil." `[Verified]`
- **Structs vs classes** — TSPL "Structures and Classes": "Structures and enumerations are value types. A
  value type is a type whose value is copied when it's assigned to a variable or constant, or when it's
  passed to a function." "Classes are reference types. Unlike value types, reference types are not copied
  when they're assigned to a variable or constant, or when they're passed to a function. Rather than a
  copy, a reference to the same existing instance is used." `mutating` "methods can modify the properties
  of the structure ... from within a particular method." `[Verified]`
- **Enums with associated values** — TSPL "Enumerations": "You can define Swift enumerations to store
  associated values of any given type, and the value types can be different for each case of the
  enumeration if needed." Raw values are "prepopulated values ... all of the same type." `[Verified]`
- **Pattern matching** — TSPL "Control Flow": a `switch` statement "must be exhaustive"; `case let` binds
  the matched value; a `where` clause "check[s] for additional conditions." `[Verified]`
- **Protocols** — TSPL "Protocols": "A protocol defines a blueprint of methods, properties, and other
  requirements that suit a particular task or piece of functionality. The protocol can then be adopted by a
  class, structure, or enumeration to provide an actual implementation of those requirements." Protocol
  extensions "provide method, initializer, subscript, and computed property implementations to conforming
  types" (default implementations). `[Verified]`
- **Closures** — TSPL "Closures": "Closures are self-contained blocks of functionality that can be passed
  around and used in your code." Trailing-closure syntax + capturing "constants and variables from the
  surrounding context." `map`/`filter`/`reduce` are standard-library higher-order methods. `[Verified]`
- **Generics** — TSPL "Generics": "Generic code enables you to write flexible, reusable functions and
  types that can work with any type, subject to requirements that you define." Type-parameter constraints
  and `where` clauses restrict the types. `[Verified]`
- **Error handling** — TSPL "Error Handling": a function marked `throws` can throw; you "use a do-catch
  statement to handle errors by running a block of code"; `try?` "convert[s] the error to an optional
  value"; error types "conform to the `Error` protocol." `[Verified]`
- **async/await (preview)** — TSPL "Concurrency": "Swift has built-in support for writing asynchronous
  ... code ... An asynchronous function or asynchronous method is a special kind of function or method that
  can be suspended while it's partway through execution." Mark with `async`; call with `await`; `Task { }`
  runs an async context; `async let` binds a concurrently-running child. Depth deferred to
  `ios-app-development`. `[Verified]`

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (Primer, subject band). Each example below cites the co-NN it exercises. -->

- **co-01 · repl-and-swiftc** — the `swift` REPL evaluates expressions interactively; `swiftc file.swift` compiles a standalone executable from the CLI (before Xcode).
- **co-02 · var-and-let** — `let` declares an immutable constant, `var` a mutable variable; prefer `let` by default.
- **co-03 · type-inference-and-annotations** — Swift infers a type from the initializer; an explicit `: Type` annotation overrides or documents it.
- **co-04 · basic-types** — `Int`, `Double`, `String`, and `Bool` are the core value types; Swift is strongly, statically typed.
- **co-05 · string-interpolation** — `"\(expr)"` embeds an expression's value inside a string literal.
- **co-06 · optionals** — `Type?` models a value that may be absent; `nil` is the absence of a value, made explicit by the type system.
- **co-07 · optional-binding** — `if let` / `guard let` safely unwrap an optional, binding the value only when present.
- **co-08 · optional-chaining** — `a?.b?.c` short-circuits to `nil` if any link is `nil`, avoiding a crash.
- **co-09 · nil-coalescing** — `optional ?? default` unwraps the optional or supplies a fallback value.
- **co-10 · force-unwrap** — `optional!` extracts the value but triggers a runtime crash on `nil` — a deliberate, sparingly-used escape hatch.
- **co-11 · functions** — `func name(params) -> ReturnType` defines a function; a function without `->` returns `Void`.
- **co-12 · argument-labels** — external argument labels name parameters at the call site; default parameter values make arguments optional.
- **co-13 · closures** — closures are self-contained blocks of functionality passed around as values; trailing-closure syntax and capture of surrounding state are idiomatic.
- **co-14 · higher-order-functions** — `map`, `filter`, and `reduce` transform collections functionally via closures.
- **co-15 · structs** — a `struct` is a value type: copied on assignment/passing, so instances never alias.
- **co-16 · classes** — a `class` is a reference type: assignment/passing shares one instance via a reference.
- **co-17 · value-vs-reference-semantics** — copying a struct is independent; copying a class reference aliases the same object — the central Swift modeling decision.
- **co-18 · properties** — types have stored properties, computed properties (a `get`/`set` pair), and `lazy` properties initialized on first access.
- **co-19 · mutating-methods** — a struct method that changes `self`'s properties must be marked `mutating`; class methods need no such mark.
- **co-20 · enums** — an `enum` defines a closed set of cases; raw values give each case an underlying literal.
- **co-21 · enums-with-associated-values** — each enum case can carry associated values of any type, modeling a tagged union.
- **co-22 · pattern-matching-switch** — an exhaustive `switch` matches cases; `case let` binds associated values and `where` adds conditions.
- **co-23 · protocols** — a `protocol` is a contract of requirements a type adopts; protocol-typed values enable polymorphism without inheritance.
- **co-24 · protocol-extensions** — extending a protocol supplies default implementations to every conforming type.
- **co-25 · generics** — generic functions and types work over any type subject to constraints (`<T: Protocol>` / `where`).
- **co-26 · error-handling** — a `throws` function signals failure; `do`/`try`/`catch` handles it, `try?` converts to an optional, and error types conform to `Error`.
- **co-27 · collections** — `Array`, `Dictionary`, and `Set` are the core generic collection types with literal syntax.
- **co-28 · async-await-preview** — an `async` function can suspend; `await` calls it, `Task { }` starts an async context, and `async let` runs children concurrently (depth deferred to iOS).

## Worked examples

Colocated under `just-enough-swift/learning/code/`; each runnable via `swift`/`swiftc` (DD-20/DD-30). Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · swiftc-compile** — compile `hello.swift` with `swiftc hello.swift && ./hello` — verify it prints. (co-01)
- **ex-02 · swift-repl** — evaluate `1 + 2` in the `swift` REPL — verify it echoes `3`. (co-01)
- **ex-03 · let-constant** — declare `let pi = 3.14` and attempt reassignment — verify the compiler rejects the mutation. (co-02)
- **ex-04 · var-mutable** — declare `var n = 0` and increment it — verify the new value prints. (co-02)
- **ex-05 · type-inference** — `let name = "Ada"` — verify its inferred type is `String` (via REPL `:type`). (co-03)
- **ex-06 · type-annotation** — `let count: Int = 0` — verify the explicit annotation compiles. (co-03)
- **ex-07 · int-double** — mix `Int` and `Double` arithmetic with an explicit conversion — verify the result type. (co-04)
- **ex-08 · bool-logic** — combine `Bool`s with `&&`/`||` — verify the truth table. (co-04)
- **ex-09 · string-interpolation** — print `"Hi \(name), you are \(age)"` — verify the interpolated output. (co-05)
- **ex-10 · optional-declare** — `var middle: String? = nil` — verify it holds `nil` without error. (co-06)
- **ex-11 · optional-assign** — assign then read an optional — verify the wrapped value. (co-06)
- **ex-12 · if-let-binding** — unwrap with `if let value = optional` — verify the present branch runs. (co-07)
- **ex-13 · guard-let** — early-return with `guard let value = optional else { return }` — verify the nil path exits. (co-07)
- **ex-14 · optional-chaining** — `user?.address?.city` — verify it yields `nil` when a link is `nil`. (co-08)
- **ex-15 · nil-coalescing** — `optional ?? "default"` — verify the fallback on `nil`. (co-09)
- **ex-16 · force-unwrap-danger** — force-unwrap a `nil` and observe the crash — verify the runtime trap message. (co-10)
- **ex-17 · func-basic** — `func greet(_ name: String)` — verify it prints the greeting. (co-11)
- **ex-18 · func-return** — `func square(_ n: Int) -> Int` — verify the returned value. (co-11)
- **ex-19 · argument-labels** — `func move(from: Int, to: Int)` called `move(from: 1, to: 2)` — verify labels are required. (co-12)
- **ex-20 · default-params** — `func log(_ msg: String, level: String = "info")` — verify the default applies. (co-12)
- **ex-21 · array-literal** — `let xs = [1, 2, 3]` — verify `xs.count == 3`. (co-27)
- **ex-22 · dictionary-literal** — `["a": 1, "b": 2]` — verify keyed lookup. (co-27)
- **ex-23 · set-literal** — `Set([1, 1, 2])` — verify dedup to two elements. (co-27)
- **ex-24 · array-iterate** — `for x in xs { }` — verify each element visits once. (co-27)
- **ex-25 · closure-basic** — assign `let add = { (a: Int, b: Int) in a + b }` — verify it computes. (co-13)
- **ex-26 · trailing-closure** — call a function with trailing-closure syntax — verify the block runs. (co-13)

### Intermediate

- **ex-27 · struct-define** — `struct Point { var x, y: Int }` — verify the memberwise initializer. (co-15)
- **ex-28 · struct-init** — construct `Point(x: 1, y: 2)` — verify field access. (co-15)
- **ex-29 · class-define** — `class Counter { var n = 0 }` — verify instantiation. (co-16)
- **ex-30 · class-reference** — pass a `Counter` to a function that mutates it — verify the caller sees the change. (co-16, co-17)
- **ex-31 · value-copy** — copy a struct, mutate the copy — verify the original is unchanged. (co-17)
- **ex-32 · reference-alias** — copy a class reference, mutate via one — verify both see the change. (co-17)
- **ex-33 · stored-property** — a stored `var` on a struct — verify read/write. (co-18)
- **ex-34 · computed-property** — a `var area: Int { width * height }` — verify it recomputes. (co-18)
- **ex-35 · lazy-property** — a `lazy var` initialized on first access — verify it defers computation. (co-18)
- **ex-36 · mutating-method** — a `mutating func` on a struct — verify it changes `self`. (co-19)
- **ex-37 · struct-method** — a non-mutating struct method returning a value — verify it computes without mutation. (co-19)
- **ex-38 · enum-basic** — `enum Direction { case north, south }` — verify a `switch` over it. (co-20)
- **ex-39 · enum-raw-value** — `enum Status: Int { case ok = 200 }` — verify `.ok.rawValue == 200`. (co-20)
- **ex-40 · enum-associated** — `enum Result { case success(String); case failure(Error) }` — verify each case carries its payload. (co-21)
- **ex-41 · enum-associated-multiple** — a case with two associated values `case point(Int, Int)` — verify extraction. (co-21)
- **ex-42 · switch-enum** — exhaustively `switch` an enum — verify the compiler requires all cases. (co-22)
- **ex-43 · switch-case-let** — `case let .success(msg)` — verify the associated value binds. (co-22, co-21)
- **ex-44 · switch-where** — `case let n where n > 0` — verify the guarded branch. (co-22)
- **ex-45 · map-transform** — `[1,2,3].map { $0 * 2 }` — verify `[2,4,6]`. (co-14)
- **ex-46 · filter** — `filter { $0.isEven }` — verify only evens remain. (co-14)
- **ex-47 · reduce** — `reduce(0, +)` — verify the sum. (co-14)
- **ex-48 · closure-capture** — a closure capturing a surrounding `var` — verify it reads the updated value. (co-13)
- **ex-49 · sorted-closure** — `sorted { $0 > $1 }` — verify descending order. (co-14)
- **ex-50 · protocol-declare** — `protocol Shape { var area: Double { get } }` — verify it compiles as a contract. (co-23)
- **ex-51 · protocol-conform** — a `struct Circle: Shape` implementing `area` — verify conformance. (co-23)
- **ex-52 · protocol-polymorphism** — an `[Shape]` array of mixed conformers — verify dynamic dispatch of `area`. (co-23)
- **ex-53 · protocol-extension-default** — a protocol extension providing a default `describe()` — verify conformers inherit it. (co-24)
- **ex-54 · protocol-as-type** — a function taking `some Shape` — verify it accepts any conformer. (co-23)

### Advanced

- **ex-55 · generic-function** — `func swap<T>(_ a: inout T, _ b: inout T)` — verify it works for `Int` and `String`. (co-25)
- **ex-56 · generic-type-stack** — `struct Stack<Element>` — verify push/pop over any element type. (co-25)
- **ex-57 · generic-constraint** — `func max<T: Comparable>(...)` — verify the constraint is enforced. (co-25)
- **ex-58 · generic-protocol-constraint** — a generic bound by a custom protocol — verify only conformers compile. (co-25, co-23)
- **ex-59 · throws-function** — `func parse() throws -> Int` — verify it can throw. (co-26)
- **ex-60 · do-catch** — handle the throw with `do { try parse() } catch { }` — verify the catch runs on error. (co-26)
- **ex-61 · try-optional** — `try?` a throwing call — verify it yields `nil` on error. (co-26, co-06)
- **ex-62 · custom-error-enum** — an `enum ParseError: Error` thrown and caught — verify the specific case matches. (co-26, co-21)
- **ex-63 · result-type** — return `Result<Int, Error>` and switch on it — verify success/failure branches. (co-26)
- **ex-64 · protocol-extension-shared** — shared behavior via a protocol extension across two types — verify both reuse it. (co-24)
- **ex-65 · protocol-composition** — a parameter typed `Named & Aged` — verify only types meeting both compile. (co-23)
- **ex-66 · equatable-conformance** — conform a struct to `Equatable` — verify `==` works. (co-23)
- **ex-67 · computed-getter-setter** — a computed property with both `get` and `set` — verify the setter updates backing state. (co-18)
- **ex-68 · enum-methods** — an enum with a method returning a per-case value — verify dispatch. (co-20, co-19)
- **ex-69 · optional-chaining-deep** — chain three optional links — verify the whole chain short-circuits. (co-08)
- **ex-70 · higher-order-pipeline** — chain `filter` → `map` → `reduce` — verify the composed result. (co-14)
- **ex-71 · closure-escaping** — store an `@escaping` closure and call it later — verify deferred execution. (co-13)
- **ex-72 · async-func** — `func fetch() async -> Int` — verify it compiles as async. (co-28)
- **ex-73 · await-call** — `await fetch()` inside a `Task` — verify it returns the value. (co-28)
- **ex-74 · task-run** — start work with `Task { }` — verify it runs to completion. (co-28)
- **ex-75 · async-let-concurrent** — `async let a = ...; async let b = ...` then `await (a, b)` — verify both run concurrently. (co-28)
- **ex-76 · async-error** — an `async throws` call handled with `try await` in `do/catch` — verify the error path. (co-28, co-26)
- **ex-77 · protocol-generic-combined** — a generic function over a protocol with an associated behavior — verify it dispatches correctly. (co-23, co-25)
- **ex-78 · capstone-cli** — a small CLI modeling a domain with an enum (associated values), optionals, a protocol + conformance, a closure transform, and one `async`/`await` call — verify `swiftc` builds it and it runs end-to-end. (co-06, co-21, co-23, co-13, co-28)

## Capstone spec — intra-topic (primer → light consolidation)

- **Goal**: build a small Swift CLI program that exercises the primer's surface — optionals, an enum with
  associated values, a protocol + conformance, closures, and a single `async`/`await` call — runnable via
  `swiftc`, proving readiness for iOS development.
- **Concepts exercised**: [ ] optionals (safe unwrapping) (co-06, co-07) [ ] an enum with associated
  values (co-21) [ ] a protocol + conformance (co-23) [ ] a closure (co-13) [ ] an `async`/`await` call
  (co-28).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — a program modeling a small domain with an enum (associated values) +
     optionals. Verify it compiles with `swiftc` and handles the nil case safely.
  2. Add a protocol + a conforming type + a closure-based transform. Verify polymorphic dispatch + the
     closure work.
  3. Add an `async` function + an `await` call. Verify it runs to completion and returns its value.
- **Acceptance criteria**: optionals, the enum, the protocol, and the closure work; the `async`/`await`
  call completes.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **The Swift Programming Language** — Apple Inc. / Swift core team, official book (CC BY 4.0). The canonical, continuously maintained, free-and-open Swift primer published alongside the language itself. <https://docs.swift.org/swift-book/documentation/the-swift-programming-language/>

**Papers & articles**

- **Swift.org Documentation** — Swift core team, official. The authoritative hub for language, toolchain, and evolution documentation. <https://www.swift.org/documentation/>

---

← Previous: [69 · Android App Development](./69-android-app-development.md) · Next: [71 · iOS App Development](./71-ios-app-development.md) →
