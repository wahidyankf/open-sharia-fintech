# 68 · Just Enough Kotlin (Primer, Kotlin †)

**prd row**: Pass 4 · Concurrency & Systems · Primer · Kotlin † · Learn 168 / Drill 268 ·
Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: **just enough Kotlin** to be productive in
[`69-android-app-development`](./69-android-app-development.md). The toolchain, syntax, null-safety,
`val`/`var`, data classes, functions/lambdas, collections, classes/interfaces, and a coroutine _preview_.

## Why this exists · the big idea

- **The problem before the solution**: Android in topic 69 leans on null-safety and coroutines from the
  first line — this primer makes Kotlin's type system and concurrency preview familiar before the
  platform's complexity lands on top of them.
- **Keep-this-if-you-forget-everything**: Kotlin makes null a compile-time decision, not a runtime
  surprise — the type `T?` forces you to handle absence exactly where it can occur.
- **Big ideas touched**: `taming-state` — nullability is a state hazard the type system contains before it
  becomes an NPE; `abstraction-and-its-cost` — data classes and coroutines buy concise expression over
  machinery you stop seeing (and occasionally must see through).

## Prerequisites

- **Prior topics**: [topic 8 Object-Oriented Programming Essentials](./08-object-oriented-programming-essentials.md)
  (classes/interfaces) and general typed-language fluency —
  [topic 13 Just Enough TypeScript](./13-just-enough-typescript.md) helps for null-safety intuition.
- **Tools & environment**: a macOS/Linux terminal; **Kotlin** (`kotlinc`) + Gradle (`./gradlew`), pinned to
  a current stable release; a JDK; Neovim/VSCode (DD-17).
- **Assumed knowledge**: classes + interfaces (topic 08); nullable-vs-non-null thinking (topic 13);
  running a build tool (topic 05).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: keep the version unpinned in shipped text. Current stable is **Kotlin 2.4.0**
  (~June 2026; 2.4.20 planned Sept 2026, 2.5.0 Dec 2026). Null-safety (`?`, `?:`, `!!`), data classes,
  `val`/`var`, and coroutine-preview syntax are unchanged. Re-pull the exact version at authoring time.
  (kotlinlang.org/docs/releases.html)

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to an official kotlinlang.org / JetBrains GitHub page the pre-authoring
> `web-researcher` sweep fetched and read. `[Needs Verification]` marks phrasing not captured verbatim at
> source or currency risk.

- **Version** — github.com/JetBrains/kotlin/releases (API `published_at`): **Kotlin 2.4.0**, released
  **2026-06-03**. Kotlin ships ~6-monthly + patches, so re-check at authoring time. `[Verified]`
- **JVM target** — kotlinlang.org `gradle-configure-project.html`: with no explicit `jvmTarget` the compiler
  defaults it to `1.8`; docs recommend `jvmToolchain(17)` "to avoid JVM target incompatibility". The exact
  `plugins { kotlin("jvm") version "..." }` block was NOT captured verbatim: `[Needs Verification]` on that
  snippet. `[Verified]` on the toolchain guidance.
- **`val`/`var` + inference** — kotlinlang.org `basic-syntax.html`: `val` = "immutable, read-only local
  variables that can't be reassigned"; `var` = "mutable variables"; "Kotlin supports type inference and
  automatically identifies the data type". Entry point `fun main()`; `println` "prints its arguments and
  adds a line break". `[Verified]`
- **Null safety** — kotlinlang.org `null-safety.html`: nullable type `String?`; safe call `?.` "if the
  object is null, the `?.` operator simply returns null"; Elvis `?:` "if the expression to the left is not
  null, returns it. Otherwise, returns the expression to the right"; `!!` "converts any value to a
  non-nullable type" (throws NPE if actually null); `?.let { ... }` runs the block only on a non-null
  value. `[Verified]`
- **Functions** — kotlinlang.org `functions.html`: default args (`len: Int = b.size`), named args (any
  order), single-expression `fun double(x: Int) = x * 2`, `Unit` = "a type that has only one value ...
  You don't have to specify Unit as a return type". `[Verified]`
- **Classes / data classes / objects** — kotlinlang.org `classes.html` / `data-classes.html` /
  `object-declarations.html`: primary constructor in the header (`class Person(val name: String)`), `init`
  blocks run in order; `data class` auto-derives "`equals()`/`hashCode()` ... `toString()` ...
  `componentN()` ... `copy()`" and requires ≥1 `val`/`var` primary-constructor param; `object` = a
  thread-safe singleton initialised on first access; `companion object` members "called simply by using
  the class name as the qualifier" (default name `Companion`). `[Verified]`
- **`when` / `if` as expressions** — kotlinlang.org `control-flow.html`: `if` as expression "an else
  branch is required"; `when` "returns a value you can use later" and, as an expression, "you must cover
  all possible cases ... the compiler throws an error" if not. `[Verified]`
- **Collections & lambdas** — kotlinlang.org `collections-overview.html` / `lambdas.html`: read-only vs
  mutable interfaces (a `MutableList` in a `val` is still writable); lambda `{ x, y -> x + y }`;
  higher-order functions "take functions as parameters, or return a function"; trailing-lambda syntax (a
  final function arg goes outside the parens); implicit single param `it` (`ints.filter { it > 0 }`).
  The exact string "`listOf`" was verified by strong analogy to the confirmed `mutableListOf`/`mutableMapOf`
  factories: `[Needs Verification]` on a direct quote of `listOf`, `[Verified]` on the pattern. `[Verified]`
- **Extension functions** — kotlinlang.org `extensions.html`: "prefix its name with a receiver type
  followed by a `.`"; verbatim example `fun String.truncate(maxLength: Int): String { ... }` called as
  `s.truncate(15)`. `[Verified]`
- **Sealed classes** — kotlinlang.org `sealed-classes.html`: "All direct subclasses ... are known at
  compile time"; the payoff is exhaustive `when` — "the Kotlin compiler can check exhaustively that all
  possible cases are covered ... you don't need to add an else clause". `[Verified]`
- **Coroutines preview** — kotlinlang.org `coroutines-basics.html`: a `suspend` function "allows a running
  operation to pause and resume later"; "you can only call a suspending function from another suspending
  function" (or a `suspend fun main`); `CoroutineScope.launch()` "starts a new coroutine without blocking";
  `runBlocking()` "blocks the current thread until the coroutines ... finish" (a bridge/entry-point tool,
  "only when there is no other option"); structured concurrency = "coroutines form a tree hierarchy of
  parent and child tasks with linked lifecycles". Flow/channels are OUT of scope for this primer (depth in
  [`69-android-app-development`](./69-android-app-development.md)). `[Verified]`

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (Primer, subject band). Each example below cites the co-NN it exercises. -->

- **co-01 · kotlin-toolchain** — `kotlinc`/Gradle (`./gradlew`) compile and run; `fun main()` is the
  entry point and `println` the standard output — the daily loop.
- **co-02 · val-var** — `val` is a read-only binding (cannot be reassigned); `var` is mutable; prefer
  `val` and reach for `var` only when a value must change.
- **co-03 · type-inference** — Kotlin infers a declaration's type from its initialiser, so annotations are
  optional but available (`val x: Int = 5`).
- **co-04 · basic-types** — `Int`/`Long`/`Double`, `Boolean`, `Char`, `String`; numeric conversions are
  explicit, and there are no implicit widenings.
- **co-05 · string-templates** — `"$name has ${items.size}"` interpolates values and expressions into
  strings; triple-quoted strings span multiple lines.
- **co-06 · null-safety** — a type is non-nullable by default; `T?` opts into nullability, so the compiler
  forces you to handle absence exactly where it can occur.
- **co-07 · safe-call** — `a?.b` returns `null` instead of throwing when `a` is null, and chains
  (`a?.b?.c`) short-circuit on the first null.
- **co-08 · elvis** — `a ?: default` yields `a` when non-null, else the right-hand value; commonly used
  with an early `return`/`throw` to unwrap-or-bail.
- **co-09 · not-null-assertion** — `a!!` forces a nullable to non-null and throws an NPE if it was null —
  the deliberate "I know better" escape hatch, used sparingly.
- **co-10 · safe-let** — `a?.let { ... }` runs a block only when `a` is non-null, binding the unwrapped
  value as `it`.
- **co-11 · functions** — `fun name(params): Ret { ... }`; a function returning nothing useful returns
  `Unit` (which may be omitted).
- **co-12 · default-named-args** — parameters can have default values and be passed by name in any order,
  collapsing overloads into one signature.
- **co-13 · single-expression-fn** — `fun double(x: Int) = x * 2` drops the braces and `return` when the
  body is one expression, inferring the return type.
- **co-14 · lambdas** — `{ x -> ... }` is a function literal; a trailing lambda goes outside the parens
  and a single parameter is the implicit `it`.
- **co-15 · higher-order-functions** — functions take and return other functions, the basis of the
  collection operators and callback-style APIs.
- **co-16 · collections** — `List`/`Set`/`Map` (read-only) vs `MutableList`/… (writable) built with
  `listOf`/`mutableListOf`/`mapOf`; a `val` mutable collection is still writable.
- **co-17 · collection-ops** — `map`/`filter`/`reduce`/`fold`/`forEach` express iteration declaratively
  and chain into readable pipelines.
- **co-18 · extension-functions** — `fun Type.name(...)` adds a method to an existing type without
  subclassing it (`"hi".truncate(5)`), keeping call sites natural.
- **co-19 · classes-constructors** — a primary constructor in the class header (`class P(val n: String)`)
  declares properties; `init` blocks run at construction in order.
- **co-20 · data-classes** — `data class` auto-derives `equals`/`hashCode`/`toString`/`copy`/`componentN`,
  giving value-like records and destructuring for free.
- **co-21 · interfaces** — interfaces declare behaviour (with optional default method bodies); a class
  implements one with `: Iface`, enabling polymorphic dispatch.
- **co-22 · objects-companion** — `object` is a lazily-initialised, thread-safe singleton; a `companion
object` holds class-level members (constants, factory methods) reached via the class name.
- **co-23 · when-expression** — `when` matches a value against cases (or acts as a conditionless if-else
  chain) and returns a value; as an expression it must be exhaustive.
- **co-24 · if-expression** — `if` is an expression returning a value (`val m = if (a > b) a else b`), so
  the `else` is required when used for its value.
- **co-25 · sealed-classes** — a `sealed` hierarchy has a compile-time-known set of subclasses, so a `when`
  over it is exhaustive with no `else` — the idiom for typed state/result unions.
- **co-26 · coroutines-preview** — `suspend` functions pause and resume without blocking a thread;
  `launch`/`runBlocking` start them and structured concurrency links parent/child lifecycles (depth in
  [`69-android-app-development`](./69-android-app-development.md)).

## Worked examples

Colocated under `just-enough-kotlin/learning/code/`; each runnable via the Kotlin CLI/Gradle (DD-20/DD-30).
Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · hello-kotlinc** — a `fun main` compiled with `kotlinc hello.kt -include-runtime -d hello.jar`
  — verify `java -jar hello.jar` prints. (co-01)
- **ex-02 · main-println** — `println("...")` inside `main` — verify the output. (co-01)
- **ex-03 · gradle-run** — a Gradle project run with `./gradlew run` — verify it prints. (co-01)
- **ex-04 · val-immutable** — `val x = 1` then reassign — verify it fails to compile. (co-02)
- **ex-05 · var-mutable** — `var y = 1; y = 2` — verify the reassignment. (co-02)
- **ex-06 · type-inference** — `val n = 5` — verify the inferred `Int`. (co-03)
- **ex-07 · type-annotation** — `val s: String = "hi"` — verify the explicit type. (co-03)
- **ex-08 · int-double-num** — `Int` vs `Double` arithmetic + `toDouble()` — verify explicit conversion. (co-04)
- **ex-09 · boolean-char** — a `Boolean` and a `Char` literal — verify their values. (co-04)
- **ex-10 · string-template** — `"$name: ${1 + 2}"` — verify the interpolation. (co-05)
- **ex-11 · string-multiline** — a `"""triple-quoted"""` string — verify it spans lines. (co-05)
- **ex-12 · nullable-type** — `var s: String? = null` — verify it compiles and holds null. (co-06)
- **ex-13 · non-null-default** — assign `null` to a non-null `String` — verify a compile error. (co-06)
- **ex-14 · safe-call** — `s?.length` on a null — verify it returns null, not NPE. (co-07)
- **ex-15 · safe-call-chain** — `a?.b?.c` — verify it short-circuits on the first null. (co-07)
- **ex-16 · elvis-default** — `s?.length ?: 0` — verify the default on null. (co-08)
- **ex-17 · elvis-return** — `val v = m[k] ?: return` — verify the early return path. (co-08)
- **ex-18 · not-null-assertion** — `s!!.length` on a null — verify it throws NPE. (co-09)
- **ex-19 · safe-let** — `s?.let { println(it) }` — verify the block runs only when non-null. (co-10)
- **ex-20 · fun-basic** — `fun add(a: Int, b: Int): Int` — verify the returned sum. (co-11)
- **ex-21 · unit-return** — a `fun` with no useful return — verify its type is `Unit`. (co-11)
- **ex-22 · default-args** — `fun greet(name: String, hi: String = "Hi")` — verify both call forms. (co-12)
- **ex-23 · named-args** — call with `greet(hi = "Hey", name = "A")` — verify order-independence. (co-12)
- **ex-24 · single-expression-fn** — `fun double(x: Int) = x * 2` — verify the result + inferred type. (co-13)
- **ex-25 · fun-vararg** — a `vararg` parameter — verify it accepts multiple args. (co-11)
- **ex-26 · if-expression** — `val m = if (a > b) a else b` — verify the assigned value. (co-24)

### Intermediate

- **ex-27 · lambda-basic** — `val sq = { x: Int -> x * x }` — verify `sq(3)`. (co-14)
- **ex-28 · trailing-lambda** — `list.map { it * 2 }` with the lambda outside parens — verify the result. (co-14)
- **ex-29 · it-implicit** — a single-param lambda using `it` — verify it works without a named param. (co-14)
- **ex-30 · higher-order-fn** — a function taking a `(Int) -> Int` — verify it applies the passed fn. (co-15)
- **ex-31 · fn-as-param** — pass `::isEven` as a function reference — verify it filters. (co-15)
- **ex-32 · fn-return-fn** — a function returning a lambda — verify the returned closure. (co-15)
- **ex-33 · listof** — `listOf(1, 2, 3)` (read-only) — verify an add method is unavailable. (co-16)
- **ex-34 · mutable-list** — `mutableListOf<Int>()` + `add` — verify mutation, even held in a `val`. (co-16)
- **ex-35 · map-literal** — `mapOf("a" to 1)` — verify keyed access. (co-16)
- **ex-36 · set-literal** — `setOf(1, 1, 2)` — verify duplicates collapse. (co-16)
- **ex-37 · collection-map** — `list.map { it + 1 }` — verify the transformed list. (co-17)
- **ex-38 · collection-filter** — `list.filter { it > 0 }` — verify it drops non-positives. (co-17)
- **ex-39 · collection-reduce-fold** — `list.fold(0) { a, e -> a + e }` — verify the sum. (co-17)
- **ex-40 · collection-foreach** — `list.forEach { println(it) }` — verify each element prints. (co-17)
- **ex-41 · collection-chain** — `list.filter { ... }.map { ... }` — verify the chained result. (co-17)
- **ex-42 · extension-function** — `fun String.shout() = uppercase() + "!"` — verify `"hi".shout()`. (co-18)
- **ex-43 · extension-property** — an extension val (e.g. `String.firstChar`) — verify it reads. (co-18)
- **ex-44 · class-primary-constructor** — `class Point(val x: Int, val y: Int)` — verify field access. (co-19)
- **ex-45 · class-init-block** — an `init { }` — verify it runs at construction. (co-19)
- **ex-46 · class-method** — a method on a class — verify it uses the instance's properties. (co-19)
- **ex-47 · data-class** — `data class User(val name: String)` — verify the generated `toString`. (co-20)
- **ex-48 · data-class-copy** — `.copy(name = "B")` — verify a new instance with one field changed. (co-20)
- **ex-49 · data-class-destructure** — `val (n, a) = user` — verify componentN destructuring. (co-20)
- **ex-50 · data-class-equals** — two equal data objects — verify structural `==` equality. (co-20)
- **ex-51 · interface-impl** — a class implementing an interface — verify the overridden method. (co-21)
- **ex-52 · interface-default-method** — an interface with a default body — verify it is inherited. (co-21)
- **ex-53 · object-singleton** — an `object Counter` — verify a single shared instance. (co-22)
- **ex-54 · companion-object** — a `companion object` factory — verify `Type.create()` by class name. (co-22)

### Advanced

- **ex-55 · when-value** — `when (x) { 1 -> ...; else -> ... }` — verify the matched branch. (co-23)
- **ex-56 · when-condition** — a conditionless `when { a > 0 -> ... }` — verify the if-else-chain form. (co-23)
- **ex-57 · when-expression-return** — assign the result of a `when` — verify the returned value. (co-23)
- **ex-58 · when-multiple-cases** — `1, 2 -> ...` combined cases — verify both match the branch. (co-23)
- **ex-59 · if-else-expression** — a chained `if/else if/else` as an expression — verify the value. (co-24)
- **ex-60 · sealed-class** — a `sealed class Result` with subclasses — verify each constructs. (co-25)
- **ex-61 · sealed-when-exhaustive** — a `when` over the sealed type with no `else` — verify it compiles
  (all cases covered). (co-25)
- **ex-62 · sealed-when-missing-case** — remove a branch — verify the compiler flags non-exhaustiveness. (co-25)
- **ex-63 · suspend-function** — a `suspend fun` — verify it can only be called from a coroutine/suspend. (co-26)
- **ex-64 · launch-coroutine** — `launch { ... }` in a scope — verify it runs concurrently. (co-26)
- **ex-65 · runblocking** — `runBlocking { ... }` bridging to `main` — verify it blocks to completion. (co-26)
- **ex-66 · coroutine-delay** — a `delay(100)` inside a coroutine — verify it suspends without blocking a
  thread. (co-26)
- **ex-67 · coroutine-return-value** — a suspend computation returning a value — verify the awaited result. (co-26)
- **ex-68 · structured-concurrency-preview** — a parent coroutine awaiting children — verify it finishes
  after them. (co-26)
- **ex-69 · null-safe-collection** — `list.mapNotNull { ... }` over nullable elements — verify nulls are
  dropped. (co-06, co-17)
- **ex-70 · data-class-in-collection** — a `List<User>` — verify `contains` uses structural equality. (co-20, co-16)
- **ex-71 · lambda-over-data-class** — `users.map { it.name }` — verify the projected list. (co-14, co-20)
- **ex-72 · interface-polymorphism** — a `List<Shape>` of different impls — verify dynamic dispatch. (co-21)
- **ex-73 · extension-on-nullable** — an extension on `String?` handling null — verify it runs on null. (co-18, co-06)
- **ex-74 · when-with-sealed-result** — a `when` returning per sealed subtype — verify each maps
  correctly. (co-23, co-25)
- **ex-75 · higher-order-with-lambda** — pass a lambda to a higher-order fn — verify the callback. (co-15, co-14)
- **ex-76 · filter-map-chain** — `list.filter { ... }.map { ... }.sum()` — verify the final number. (co-17)
- **ex-77 · gradle-multi-file** — a Gradle build across two source files — verify it compiles and runs. (co-01, co-19)
- **ex-78 · capstone-preview-cli** — a CLI: null-safe access + a data class + a collection lambda + an
  interface + a coroutine — verify it builds and produces the expected output. (co-06, co-20, co-14,
  co-21, co-26)

## Capstone spec — intra-topic (primer → light consolidation)

- **Goal**: build a small Kotlin CLI that exercises the primer's surface — null-safety, data classes,
  lambdas over collections, an interface, and a single coroutine — with a Gradle/`kotlinc` build, proving
  readiness for Android development.
- **Concepts exercised**: [ ] null-safety (`?`/`?:`) (co-06, co-07, co-08) [ ] data classes (co-20)
  [ ] lambdas over collections (co-14, co-17) [ ] an interface (co-21) [ ] a coroutine (co-26).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — a program using data classes + collection lambdas + null-safe access.
     Verify it builds and produces the expected output.
  2. Add an interface + an implementation. Verify polymorphic dispatch works.
  3. Add a single coroutine (e.g. a suspended computation). Verify it runs to completion and returns its
     value.
- **Acceptance criteria**: null-safety, data classes, and collection lambdas work; the interface dispatches;
  the coroutine completes.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Kotlin in Action** — Dmitry Jemerov & Svetlana Isakova (2017, Manning). Written by JetBrains engineers; the classic Kotlin primer.

**Papers & articles**

- **Kotlin documentation** — JetBrains, official (kotlinlang.org). The authoritative, continuously updated language reference. <https://kotlinlang.org/docs/home.html>
- **Kotlin tour** — official (kotlinlang.org). The official guided primer to Kotlin fundamentals. <https://kotlinlang.org/docs/kotlin-tour-welcome.html>
- **Kotlin language specification** — official (kotlinlang.org). The formal specification of the language. <https://kotlinlang.org/spec/>

---

← Previous: [67 · Actor-Model Concurrency](./67-actor-model-concurrency.md) · Next: [69 · Android App Development](./69-android-app-development.md) →
