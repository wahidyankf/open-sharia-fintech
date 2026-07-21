# Just Enough Dart (Primer, Dart)

**Course ID**: `just-enough-dart` · **Format**: Primer · **Language**: Dart.

**Short summary**: Dart syntax, async, idioms for Flutter

**Scope note**: **just enough Dart** to be productive in
[`73-hybrid-app-development`](./hybrid-app-development.md). The `dart` / `pub` CLI, sound null safety,
syntax and types, `async`/`await` with `Future`s and `Stream`s, and classes/mixins. `†`: Dart, run and
built with the `dart` toolchain.

## Why this exists · the big idea

- **The problem before the solution**: you cannot learn Flutter and Dart at the same time without drowning
  — the widget model deserves full attention, so the language it is written in has to already be muscle
  memory.
- **Keep-this-if-you-forget-everything**: Dart is a familiar C-family, null-safe, statically typed language
  with first-class async — if you know a typed OO language, most of it transfers; the parts worth deliberate
  practice are sound null safety and `Future`/`Stream` async.
- **Big ideas touched**: `taming-state` (async/await, `Future`s, and `Stream`s are Dart's structured way to
  handle state that arrives over time without callback tangles), `abstraction-and-its-cost` (sound null
  safety is a compile-time abstraction that eliminates a whole class of null errors — at the cost of forcing
  you to be explicit about what can be absent).

## Prerequisites

- **Prior topics**: [topic 8 Object-Oriented Programming Essentials](./object-oriented-programming-essentials.md)
  (classes, interfaces, inheritance) and [topic 13 Just Enough TypeScript](./just-enough-typescript.md)
  (static types and null-vs-non-null thinking transfer directly).
- **Tools & environment**: a macOS/Linux/Windows machine; the **Dart SDK** (`dart`, `pub`) pinned to a
  current stable (it ships with Flutter, so a Flutter install also provides it); Neovim/VSCode with the Dart
  LSP (DD-17).
- **Assumed knowledge**: classes/interfaces/inheritance (topic 08); static types and nullability (topic
  13); running a CLI build/run tool (topic 05).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: keep the Dart SDK at "a current stable" in shipped text — sound null safety, the
  `dart` CLI (`create`/`run`/`test`), `pub` package management, `async`/`await` with `Future`/`Stream`, and
  classes/mixins are stable, settled language surface. Dart releases on a moving cadence, so a pinned number
  would go stale fast.
- 2026-07-12 — verified: no third-party package version is claimed in the body — the primer stays on the
  standard library and language core, so there is no version to re-pull beyond the SDK itself.

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to an official dart.dev / api.dart.dev page the pre-authoring `web-researcher`
> sweep fetched and read. `[Verified]` = a directly-read primary quote; `[Needs Verification]` = currency
> or capture caveat. Keep the SDK version UNPINNED in shipped prose (Dart ships ~quarterly).

- **Version** — dart.dev/tools/sdk documents the current SDK as **3.12.2** ("this site's documentation and
  examples assume version `3.12.2` of the Dart SDK"); dart.dev/resources/whats-new dates Dart 3.12 to
  2026-05. Keep it unpinned. `[Verified]` (a 2-day release-date discrepancy between whats-new and the blog
  is `[Needs Verification]` but immaterial — the body cites no date).
- **Variables** — dart.dev/language/variables: "A final variable can be set only once; a const variable is
  a compile-time constant." `var` infers the type from the initializer; a bare `[]`/no annotation infers
  `dynamic`. `[Verified]`
- **Sound null safety** — dart.dev/null-safety: "Unless you explicitly tell Dart that a variable can be
  null, it's considered non-nullable"; unsafe uses are caught "at edit time, turning what would be runtime
  errors in other languages into analysis errors." `late` "enforce[s] this variable's constraints at
  runtime instead of at compile time" (lazy init); `!` "casts an expression to its underlying non-nullable
  type," a checked cast that can throw. `[Verified]`
- **Null-aware operators** — dart.dev/language/operators + null-safety/understanding-null-safety: `??`
  "returns [expr1] if non-null; otherwise evaluates and returns [expr2]"; `??=` "assign value to b if b is
  null"; `?.` "if the receiver is null then the property access ... is skipped and the expression evaluates
  to null." `[Verified]`
- **Built-in types** — dart.dev/language/built-in-types: `int` "no larger than 64 bits, depending on the
  platform"; `double` "64-bit (double-precision) floating-point, IEEE 754"; `num` supertype of both;
  `String` "holds a sequence of UTF-16 code units" with `${}` interpolation; `bool` only `true`/`false`
  (no truthy/falsy); `List`/`Set`/`Map` collection literals. `[Verified]`
- **Functions** — dart.dev/language/functions: named parameters "are optional unless explicitly marked as
  `required`" (`{}` syntax); optional positional parameters use `[]`; `=> expr` "is shorthand for
  `{ return expr; }`"; functions are first-class ("assigned to variables, passed as arguments, and returned
  from other functions"). `[Verified]`
- **Classes & constructors** — dart.dev/language/constructors: generative constructors ("`Point(this.x,
this.y);`" initializing formals); named constructors ("`Point.origin() : x = xOrigin, y = yOrigin;`");
  factory constructors (used when "the constructor doesn't always create a new instance" or needs
  "non-trivial work prior to constructing"); initializer lists (comma-separated `: x = json['x']!`);
  getters/setters via `get`/`set` (dart.dev/language/methods). `[Verified]`
- **Mixins** — dart.dev/language/mixins: "a way of defining code that can be reused in multiple class
  hierarchies"; `with` "to use a mixin"; the `on` clause "define[s] the type that `super` calls are
  resolved against." `[Verified]`
- **Collections & control flow** — dart.dev/language/collections: `List`/`Set`/`Map` literals with type
  inference; spread `...` and null-aware spread `...?` (the latter avoids a "compile-time error" on a null
  collection); collection-`if` and collection-`for` inside literals. `[Verified]`
- **Records & patterns (Dart 3)** — dart.dev/language/records: "Records require a language version of at
  least 3.0"; "an anonymous, immutable, aggregate type"; positional `(int, int)` / named `({int a})`;
  destructure `var (a, b) = record;`; positional fields `record.$1`. dart.dev/language/patterns: "a pattern
  can **match** a value, **destructure** a value, or both"; used in variable declarations, `switch`/`if-case`,
  and for-in. `[Verified]`
- **Async — Future/async/await** — dart.dev/language/async: "`async` and `await` ... let you write
  asynchronous code that looks similar to synchronous code"; an `async` function "executes only until it
  encounters its first `await` expression." `await for` is an asynchronous for-loop over a stream.
  `[Verified]`
- **Streams — async\*/yield** — dart.dev/libraries/async/creating-streams: `async*` generator functions
  create a `Stream`; `yield` appends a value ("similar to return, but it does not terminate the function").
  `[Needs Verification]` — confirmed via a search synthesis of that dart.dev URL rather than a fully verbatim
  fetch; the syntax is long-stable Dart surface.
- **CLI & pub** — dart.dev/tools/dart-tool: `dart create` "Creates a new project", `dart run` "Runs a Dart
  program", `dart test` "Runs tests in this package", `dart compile` "Compiles Dart to various formats".
  dart.dev/tools/pub/cmd/pub-get: `dart pub get` "retrieve[s] the dependencies" from `pubspec.yaml` and
  "writes a lockfile [`pubspec.lock`]". `[Verified]`

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (Primer, subject band). Each example below cites the co-NN it exercises. -->

- **co-01 · dart-cli** — `dart create`/`run`/`test`/`compile` scaffold, run, test, and compile a Dart program from the terminal.
- **co-02 · pub** — `pubspec.yaml` declares dependencies; `dart pub get` resolves them and writes `pubspec.lock` for reproducible versions.
- **co-03 · variables** — `var` infers a type, `final` sets once, `const` is a compile-time constant, `dynamic` opts out of static checking.
- **co-04 · built-in-types** — `int`, `double`, and their supertype `num`, plus `String` (UTF-16), `bool`, and the `List`/`Set`/`Map` collection types.
- **co-05 · string-interpolation** — `"${expr}"` (or `"$name"`) embeds a value inside a string.
- **co-06 · sound-null-safety** — every type is non-nullable by default; `Type?` opts into nullability, and unsafe uses are caught at compile time.
- **co-07 · late** — `late` defers a non-nullable field's initialization (checked at runtime) and can make the initializer lazy.
- **co-08 · null-aware-operators** — `?.` short-circuits on null, `??` supplies a default, `??=` assigns only if null, `!` asserts non-null (throwing on null).
- **co-09 · functions** — `ReturnType name(params) { }` or the `=> expr` arrow shorthand; every function returns a value (`void` if none).
- **co-10 · named-parameters** — `{...}` parameters are optional unless marked `required`, and are passed by name at the call site.
- **co-11 · optional-positional-parameters** — `[...]` parameters are optional positional, with optional default values.
- **co-12 · first-class-functions** — functions are values: assigned to variables, passed as arguments, and returned (closures capture their scope).
- **co-13 · collections** — `List`, `Set`, and `Map` literals with inferred element types.
- **co-14 · collection-control-flow** — collection-`if`, collection-`for`, spread `...`, and null-aware spread `...?` build collections declaratively.
- **co-15 · generics** — `List<T>`, generic functions, and generic classes parameterize over types, with optional constraints.
- **co-16 · classes** — fields, constructors (incl. `this.x` initializing formals), and methods; `this` refers to the instance.
- **co-17 · named-constructors** — `ClassName.identifier(...)` provides multiple, clearly-named ways to construct an instance.
- **co-18 · factory-constructors** — a `factory` constructor may return a cached or subtype instance instead of always creating a new one.
- **co-19 · initializer-lists** — a `: field = value, ...` list initializes final fields before the constructor body runs.
- **co-20 · getters-setters** — `get`/`set` expose computed properties; client code reads/writes them like fields.
- **co-21 · mixins** — a `mixin` bundles reusable behavior applied with `with`; an `on` clause constrains which classes may use it.
- **co-22 · records** — records (Dart 3+) are anonymous, immutable, aggregate values — positional `(a, b)` or named `({a, b})` — enabling multiple returns and destructuring.
- **co-23 · patterns** — patterns (Dart 3+) match and destructure values in variable declarations, `switch`, and `if-case`.
- **co-24 · future-async-await** — a `Future` is a value that arrives later; `async`/`await` writes asynchronous code that reads sequentially.
- **co-25 · streams** — a `Stream` is a sequence of async values; `await for` consumes it and `async*`/`yield` produces it.
- **co-26 · error-handling** — `throw` raises an error; `try`/`catch`/`finally` handles it; errors are `Exception`/`Error` objects.

## Worked examples

Colocated under `just-enough-dart/learning/code/`; each runnable via `dart` (DD-20/DD-30). Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · dart-create** — `dart create hello` scaffolds a project — verify the generated `bin/hello.dart` runs. (co-01)
- **ex-02 · dart-run** — `dart run` a console program — verify it prints. (co-01)
- **ex-03 · dart-test-cmd** — `dart test` a package — verify a passing test reports green. (co-01)
- **ex-04 · pubspec-add-package** — add a dependency to `pubspec.yaml` + `dart pub get` — verify `pubspec.lock` pins it. (co-02)
- **ex-05 · var-infer** — `var n = 42` — verify the inferred `int` type. (co-03)
- **ex-06 · final-const** — `final` vs `const` — verify `const` is a compile-time constant and `final` set-once. (co-03)
- **ex-07 · dynamic-type** — a `dynamic` variable reassigned across types — verify no static error. (co-03)
- **ex-08 · int-double-num** — mix `int`/`double` under `num` — verify arithmetic. (co-04)
- **ex-09 · string-bool** — a `String` and a `bool` in a condition — verify explicit boolean check (no truthy). (co-04)
- **ex-10 · string-interpolation** — `"Hi $name, ${age + 1}"` — verify the interpolated output. (co-05)
- **ex-11 · non-nullable-default** — assign `null` to a non-nullable `int` — verify the compiler rejects it. (co-06)
- **ex-12 · nullable-type** — `int? x = null` — verify it holds null legally. (co-06)
- **ex-13 · late-init** — a `late` field initialized before first use — verify runtime enforcement. (co-07)
- **ex-14 · null-aware-access** — `user?.name` — verify it yields null when `user` is null. (co-08)
- **ex-15 · null-coalescing** — `name ?? 'Guest'` — verify the fallback. (co-08)
- **ex-16 · null-coalescing-assign** — `b ??= compute()` — verify it assigns only when null. (co-08)
- **ex-17 · bang-operator** — `value!` on a null — verify the runtime throw. (co-08)
- **ex-18 · function-basic** — `int add(int a, int b) { return a + b; }` — verify the sum. (co-09)
- **ex-19 · arrow-function** — `int square(int n) => n * n;` — verify the shorthand. (co-09)
- **ex-20 · named-params** — `void greet({String? name})` called `greet(name: 'Ada')` — verify by-name passing. (co-10)
- **ex-21 · required-named** — `void f({required int id})` — verify omitting `id` is a compile error. (co-10)
- **ex-22 · optional-positional** — `String say(String s, [String end = '!'])` — verify the default. (co-11)
- **ex-23 · closure** — a closure capturing a local `var` — verify it reads the updated value. (co-12)
- **ex-24 · list-literal** — `var xs = [1, 2, 3]` — verify `xs.length == 3`. (co-13)
- **ex-25 · map-literal** — `{'a': 1}` — verify keyed lookup. (co-13)
- **ex-26 · set-literal** — `{1, 1, 2}` — verify dedup to two. (co-13)

### Intermediate

- **ex-27 · collection-if** — `[if (loggedIn) 'Logout']` — verify the conditional element. (co-14)
- **ex-28 · collection-for** — `[for (var n in xs) n * 2]` — verify the generated list. (co-14)
- **ex-29 · spread-operator** — `[0, ...a, 5]` — verify inlined elements. (co-14)
- **ex-30 · null-aware-spread** — `[...?maybeList]` — verify no error on null. (co-14)
- **ex-31 · generic-list** — `List<String>` — verify a type-mismatched add is rejected. (co-15)
- **ex-32 · generic-function** — `T first<T>(List<T> xs) => xs.first;` — verify it works for two types. (co-15)
- **ex-33 · generic-class** — `class Box<T> { T value; }` — verify parameterized construction. (co-15)
- **ex-34 · class-fields** — a class with two fields — verify default access. (co-16)
- **ex-35 · class-constructor** — a positional constructor — verify instantiation. (co-16)
- **ex-36 · this-in-constructor** — `Point(this.x, this.y)` initializing formals — verify field assignment. (co-16)
- **ex-37 · initializing-formals** — a constructor setting a final field via `this.` — verify it compiles. (co-16)
- **ex-38 · named-constructor** — `Point.origin() : x = 0, y = 0;` — verify the named path. (co-17)
- **ex-39 · factory-constructor** — a `factory` returning a cached instance — verify identical instances. (co-18)
- **ex-40 · initializer-list** — `Foo(int v) : _v = v * 2 { }` — verify pre-body init. (co-19)
- **ex-41 · getter** — `double get area => w * h;` — verify it recomputes. (co-20)
- **ex-42 · setter** — a `set` that validates — verify it rejects bad input. (co-20)
- **ex-43 · computed-getter** — a getter derived from two fields — verify the derived value. (co-20)
- **ex-44 · mixin-define** — `mixin Logger { void log(...) {} }` — verify it compiles. (co-21)
- **ex-45 · mixin-with** — `class Service with Logger` — verify the mixed-in method is callable. (co-21)
- **ex-46 · mixin-on** — a `mixin ... on Base` — verify only `Base` subtypes may use it. (co-21)
- **ex-47 · first-class-function-arg** — pass a function to another function — verify it's invoked. (co-12)
- **ex-48 · higher-order-map** — `xs.map((n) => n * 2)` — verify the transformed iterable. (co-12, co-13)
- **ex-49 · list-iterate** — `for (var x in xs)` — verify each element visits once. (co-13)
- **ex-50 · map-iterate** — iterate `map.entries` — verify key/value access. (co-13)
- **ex-51 · try-catch** — wrap risky code in `try/catch` — verify the catch runs on error. (co-26)
- **ex-52 · throw-exception** — `throw FormatException(...)` — verify it propagates. (co-26)
- **ex-53 · custom-exception** — a class implementing `Exception` thrown + caught — verify the type matches. (co-26)
- **ex-54 · finally** — a `finally` block — verify it runs on both success and error. (co-26)

### Advanced

- **ex-55 · record-positional** — `(int, int) p = (1, 2)` — verify `p.$1`/`p.$2`. (co-22)
- **ex-56 · record-named** — `({int x, int y}) p = (x: 1, y: 2)` — verify `p.x`. (co-22)
- **ex-57 · record-destructure** — `var (a, b) = p;` — verify both bind. (co-22)
- **ex-58 · record-return-multiple** — a function returning a record — verify multiple values return. (co-22)
- **ex-59 · pattern-variable-declaration** — `var [a, b] = list;` — verify list destructuring. (co-23)
- **ex-60 · pattern-switch** — a `switch` with object/constant patterns — verify the matched branch. (co-23)
- **ex-61 · pattern-if-case** — `if (x case int n)` — verify the guarded bind. (co-23)
- **ex-62 · pattern-map-destructure** — `if (json case {'user': String u})` — verify the map pattern binds. (co-23)
- **ex-63 · future-basic** — a function returning `Future<int>` — verify it completes. (co-24)
- **ex-64 · async-await** — `await fetch()` in an `async` function — verify the awaited value. (co-24)
- **ex-65 · future-then** — `.then((v) => ...)` — verify the callback fires on completion. (co-24)
- **ex-66 · future-error** — an async error caught with `try/await/catch` — verify the error path. (co-24, co-26)
- **ex-67 · multiple-await** — sequentially `await` two futures — verify order. (co-24)
- **ex-68 · stream-listen** — `stream.listen((v) => ...)` — verify each event delivers. (co-25)
- **ex-69 · await-for** — `await for (var v in stream)` — verify in-order consumption. (co-25)
- **ex-70 · async-generator** — `Stream<int> count() async* { yield i; }` — verify emitted values. (co-25)
- **ex-71 · stream-transform** — `stream.map(...)` — verify the transformed stream. (co-25)
- **ex-72 · generic-constraint** — `T max<T extends Comparable>(...)` — verify the bound is enforced. (co-15)
- **ex-73 · mixin-multiple** — `with A, B` two mixins — verify both behaviors compose. (co-21)
- **ex-74 · factory-cache** — a factory maintaining a registry — verify repeated names return the same object. (co-18)
- **ex-75 · null-safe-chain** — chain `a?.b?.c ?? d` — verify the whole chain short-circuits to the default. (co-08)
- **ex-76 · async-stream-combined** — an `async*` producer awaiting a `Future` per element — verify combined async. (co-24, co-25)
- **ex-77 · class-mixin-generic** — a generic class using a mixin — verify all three compose. (co-16, co-21, co-15)
- **ex-78 · capstone-cli** — a console program with null-safe types, a class + mixin, a generic collection, an `async`/`await` `Future`, and a `Stream` consumer — verify `dart run` output and `dart test` pass. (co-06, co-21, co-15, co-24, co-25)

## Capstone spec — intra-topic (primer → light consolidation)

- **Goal**: build a small Dart console program that exercises the primer's surface — null-safe types, a
  class with a mixin, a generic collection, and an `async`/`await` call over a `Future` (plus a `Stream`),
  runnable via `dart run` and a `dart test`, proving readiness for Flutter.
- **Concepts exercised**: [ ] sound null safety (co-06, co-08) [ ] a class + a mixin (co-16, co-21) [ ] a
  generic collection (co-15) [ ] an `async`/`await` + `Future` (co-24) [ ] consuming a `Stream` (co-25)
  [ ] a `dart test` (co-01).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — a console program using null-safe types, a class with a mixin, and a
     generic collection. Verify `dart run` produces the expected output.
  2. Add an `async` function returning a `Future` and `await` it. Verify the async path completes with the
     awaited value.
  3. Add a `Stream` consumer and a `dart test`. Verify the stream is consumed in order and the test passes.
- **Acceptance criteria**: null-safe code compiles and runs; the mixin and generic collection work; the
  `Future` completes and the `Stream` is consumed in order; `dart test` passes.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Papers & articles**

- **A tour of the Dart language** — official (dart.dev). The canonical language primer maintained by the
  Dart team. <https://dart.dev/language>
- **Dart documentation** — official (dart.dev). The authoritative documentation hub, including core
  libraries. <https://dart.dev/docs>
- **Dart language specification** — official (dart.dev). The formal specification of the language.
  <https://dart.dev/resources/language/spec>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Mobile & CLI platforms — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Mobile & desktop platforms — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 11 · Mobile & desktop platforms.

> _Content originated in the now-closed FS-SE plan (topic 72); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
