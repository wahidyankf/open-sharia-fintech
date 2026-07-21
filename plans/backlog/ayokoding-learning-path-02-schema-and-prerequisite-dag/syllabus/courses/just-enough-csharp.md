# Just Enough C# (Primer, C#)

**Course ID**: `just-enough-csharp` · **Format**: Primer · **Language**: C#.

**Short summary**: C# syntax, LINQ, async, .NET idioms

**Scope note**: **just enough C#** to be productive in
[`75-windows-app-development`](./windows-app-development.md). The `dotnet` CLI, syntax/types, nullable
reference types, properties, records, a LINQ intro, classes/interfaces, and an `async`/`await` _preview_.

## Why this exists · the big idea

- **The problem before the solution**: Windows app development in topic 75 assumes fluency in .NET's type
  system and async model — this primer gets you productive in C# and the `dotnet` CLI so the platform topic
  isn't also a language lesson.
- **Keep-this-if-you-forget-everything**: nullable reference types turn "could this be null?" from a
  runtime crash into a compile-time conversation — enable them and let the compiler track absence for you.
- **Big ideas touched**: `taming-state` — nullable reference types and records (immutable by default)
  contain two classic state hazards; `abstraction-and-its-cost` — LINQ and `async`/`await` hide iteration
  and continuation machinery you occasionally must see through.

## Prerequisites

- **Prior topics**: [topic 8 Object-Oriented Programming Essentials](./object-oriented-programming-essentials.md)
  (classes/interfaces) and general typed-language fluency (any of Kotlin/Swift/TypeScript from earlier
  primers transfers).
- **Tools & environment**: a macOS/Linux/Windows machine; the **.NET SDK** (`dotnet`), pinned to a current
  LTS; Neovim/VSCode with the C# LSP (DD-17).
- **Assumed knowledge**: classes/interfaces (topic 08); nullable-vs-non-null thinking (topics 13/68/70);
  running a CLI build tool (topic 05).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: keep "current LTS" unpinned in shipped text. Current .NET LTS is **.NET 10**
  (Nov 2025, supported to Nov 2028); next is **.NET 11** (STS, ~Nov 2026) — after that "current LTS" is
  still .NET 10 but a newer STS coexists, so re-pull at authoring time. `dotnet` CLI (`new`/`run`/`build`/
  `test`), nullable reference types, properties, records, LINQ, `async`/`await` are current/unchanged.
  (dotnet.microsoft.com/platform/support/policy/dotnet-core)

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to an official learn.microsoft.com / dotnet.microsoft.com page the
> pre-authoring `web-researcher` sweep fetched and read. `[Verified]` = a directly-read primary quote.
> Keep the .NET version UNPINNED in shipped prose; re-pull at authoring time.

- **Versions & cadence** — dotnet.microsoft.com/platform/support/policy/dotnet-core: "A new major release
  of .NET is published every year in November ... Even numbered releases are LTS releases that get free
  support and patches for three years. Odd numbered releases are STS releases ... two years." **.NET 10** is
  the current LTS (GA 2025-11-11, supported to 2028-11-14); **.NET 11** is the next STS (in preview, GA
  ~2026-11 → STS by the even/odd rule). The current language version is **C# 14** (with .NET 10); **C# 15**
  ships with .NET 11 (both out of this primer's scope). `[Verified]`
- **`dotnet` CLI** — learn.microsoft.com/dotnet/core/tools: `dotnet new` "Creates a new project,
  configuration file, or solution based on the specified template"; `dotnet run` "Runs source code without
  any explicit compile or launch commands ... depends on the `dotnet build` command"; `dotnet build`
  "Builds a project, solution, or file-based app and all of its dependencies"; `dotnet test` "builds the
  solution and runs the tests." `[Verified]`
- **Value vs reference types** — learn.microsoft.com/dotnet/csharp/language-reference/builtin-types/value-types:
  "A variable of a value type contains an instance of the type. This behavior differs from a variable of a
  reference type, which contains a reference to an instance of the type." Built-in simple types (`int`,
  `bool`, `char`) are structs; `object`, `string`, `dynamic` are reference types. `[Verified]`
- **Top-level statements** — learn.microsoft.com/dotnet/csharp/fundamentals/program-structure/top-level-statements:
  "When you create a new console app by using `dotnet new console`, it uses top-level statements by
  default." Introduced in **C# 9** (2020). `[Verified]`
- **Nullable reference types** — learn.microsoft.com/dotnet/csharp/fundamentals/null-safety/nullable-reference-types:
  "Nullable reference types are a group of features that minimize the chance your code throws
  System.NullReferenceException ... entirely a compile-time feature"; "Every reference type variable is
  non-nullable by default. Append `?` to declare a nullable reference type"; the null-forgiving operator
  `!` "declares that an expression is not-null ... Use `!` sparingly"; recent templates set
  `<Nullable>enable</Nullable>`. Introduced in **C# 8** (2019). `[Verified]`
- **Properties** — learn.microsoft.com/dotnet/csharp/programming-guide/classes-and-structs/auto-implemented-properties:
  "the compiler creates a private, anonymous backing field that can only be accessed through the property's
  `get` and `set` accessors"; the `init` accessor "assigns a value ... only during object construction ...
  enforces immutability." Expression-bodied members (`=> expr`) since C# 6/7. `[Verified]`
- **Records** — learn.microsoft.com/dotnet/csharp/language-reference/builtin-types/record: "the `record`
  modifier ... encapsulat[es] data ... primarily intended for supporting immutable data models"; positional
  records generate public properties from primary-constructor parameters; "two objects are equal if they
  are of the same type and store the same values"; a `with` expression "creates a new record instance that's
  a copy of an existing record instance, but with specified properties ... modified" (a shallow copy).
  Introduced in **C# 9**. `[Verified]`
- **LINQ** — learn.microsoft.com/dotnet/csharp/linq/get-started/introduction-to-linq-queries: "A LINQ data
  source is any object that supports the generic IEnumerable<T> interface"; query vs method syntax — "The C#
  compiler translates query syntax into method calls ... There's no semantic or performance difference";
  deferred execution — "the operation is performed only when the query variable is enumerated"; `Where`/
  `Select` are deferred+streaming, `OrderBy` deferred+nonstreaming, `Count`/`First` immediate. LINQ dates to
  **C# 3.0** (2007). `[Verified]`
- **Classes & interfaces** — learn.microsoft.com/dotnet/csharp/fundamentals/types/interfaces: "An interface
  defines a contract ... that a `class` or `struct` must implement. Interfaces let a single type implement
  multiple contracts ... C# doesn't support multiple inheritance of classes." Default interface members
  ("let an interface provide a method body") are stable since **C# 8**. `[Verified]`
- **async/await** — learn.microsoft.com/dotnet/csharp/asynchronous-programming/task-asynchronous-programming-model:
  "An `await` expression in an async method doesn't block the current thread while the awaited task is
  running. Instead, the expression signs up the rest of the method as a continuation"; "The `async` and
  `await` keywords don't cause extra threads to be created." Return type is `Task<TResult>` / `Task` / `void`
  (event handlers only). Introduced in **C# 5.0** (2012). `[Verified]`
- **ECMA-334** — the C# language is standardized as **ECMA-334, 6th edition (June 2022)** — authoritative for
  language formalism but predates C# 12–15 features. `[Verified]`

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (Primer, subject band). Each example below cites the co-NN it exercises. -->

- **co-01 · dotnet-cli** — `dotnet new`/`run`/`build`/`test` scaffold, run, build, and test a .NET project from the terminal.
- **co-02 · top-level-statements** — a console app's entry point can be top-level statements in `Program.cs`, without an explicit `Main`.
- **co-03 · value-vs-reference-types** — a value-type variable holds an instance (copied on assignment); a reference-type variable holds a reference to a shared instance.
- **co-04 · var-and-types** — `var` infers a local's type; `int`/`string`/`bool` are the core built-in types.
- **co-05 · nullable-reference-types** — with `<Nullable>enable</Nullable>`, reference types are non-nullable by default and `?` opts into nullability, with null-state analysis at compile time.
- **co-06 · null-forgiving** — the `!` operator asserts a value is non-null, suppressing the compiler's warning (used sparingly).
- **co-07 · classes** — a `class` groups fields, methods, and constructors; `new` instantiates it.
- **co-08 · interfaces** — an `interface` is a contract a class/struct implements; a type may implement many, and default interface members can supply a body.
- **co-09 · inheritance** — a class derives from a base with `:`; `virtual`/`override` enable polymorphic dispatch.
- **co-10 · properties** — auto-implemented `{ get; set; }` properties have a compiler-generated backing field; `init` accessors allow set-only-at-construction immutability.
- **co-11 · expression-bodied-members** — `=> expr` gives a concise body for methods, properties, and other members.
- **co-12 · records** — a `record` provides value equality, a `with` expression for non-destructive copies, and positional (primary-constructor) syntax for immutable data.
- **co-13 · enums** — an `enum` names a set of integral constants.
- **co-14 · collections** — arrays, `List<T>`, and `Dictionary<K,V>` are the core collection types.
- **co-15 · generics** — generic methods and classes (`<T>`) parameterize over types, with optional constraints (`where T : ...`).
- **co-16 · linq-query-syntax** — LINQ query syntax (`from`/`where`/`select`) expresses queries over any `IEnumerable<T>`.
- **co-17 · linq-method-syntax** — LINQ method syntax (`Where`/`Select`/`OrderBy`) chains the same operators as method calls.
- **co-18 · deferred-execution** — a LINQ query runs only when enumerated; `Count`/`First`/`ToList` force immediate execution.
- **co-19 · lambdas-delegates** — lambda expressions (`x => ...`) create `Func<>`/`Action<>` delegates passed as values.
- **co-20 · pattern-matching** — `switch` expressions and `is` patterns (type/property/tuple) match and destructure values.
- **co-21 · exception-handling** — `try`/`catch`/`finally` handles thrown exceptions; `throw` raises them.
- **co-22 · async-await** — `async` methods return `Task`/`Task<T>`; `await` suspends without blocking the thread, signing up a continuation.
- **co-23 · string-handling** — string interpolation (`$"..."`) and the core `String` methods manipulate text.
- **co-24 · namespaces-using** — `namespace` organizes types; `using` imports them.
- **co-25 · nuget** — `dotnet add package` adds a NuGet dependency.
- **co-26 · struct-vs-class** — a `struct` is a value type (copied, stack-friendly); a `class` is a reference type (shared, heap-allocated).

## Worked examples

Colocated under `just-enough-csharp/learning/code/`; each runnable via `dotnet` (DD-20/DD-30). Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · dotnet-new-console** — `dotnet new console` scaffolds an app — verify a `Program.cs` is created. (co-01)
- **ex-02 · dotnet-run** — `dotnet run` — verify it prints. (co-01)
- **ex-03 · dotnet-test-cmd** — `dotnet test` a test project — verify a passing test reports green. (co-01)
- **ex-04 · top-level-statements** — a `Program.cs` with top-level statements — verify it runs without an explicit `Main`. (co-02)
- **ex-05 · var-inference** — `var n = 42;` — verify the inferred `int`. (co-04)
- **ex-06 · int-string-bool** — declare `int`/`string`/`bool` — verify usage. (co-04)
- **ex-07 · value-type-copy** — copy an `int`/struct, mutate the copy — verify the original is unchanged. (co-03)
- **ex-08 · reference-type-alias** — copy a class reference, mutate via one — verify both see the change. (co-03)
- **ex-09 · nullable-enable** — set `<Nullable>enable</Nullable>` — verify null-state warnings appear. (co-05)
- **ex-10 · nullable-annotation** — `string? name = null;` — verify it compiles. (co-05)
- **ex-11 · null-analysis-warning** — dereference a maybe-null — verify the compiler warns. (co-05)
- **ex-12 · null-forgiving** — `name!.Length` — verify the warning is suppressed. (co-06)
- **ex-13 · string-interpolation** — `$"Hi {name}"` — verify the interpolated output. (co-23)
- **ex-14 · string-methods** — `ToUpper()`/`Split()`/`Contains()` — verify the results. (co-23)
- **ex-15 · namespace-declare** — declare a `namespace` — verify the type is scoped. (co-24)
- **ex-16 · using-directive** — `using System.Linq;` — verify the imported members resolve. (co-24)
- **ex-17 · class-define** — a `class` with a field — verify instantiation. (co-07)
- **ex-18 · class-constructor** — a constructor setting fields — verify construction. (co-07)
- **ex-19 · class-method** — an instance method returning a value — verify the call. (co-07)
- **ex-20 · auto-property** — `public string Name { get; set; }` — verify get/set. (co-10)
- **ex-21 · init-property** — `{ get; init; }` — verify it's set only at construction. (co-10)
- **ex-22 · expression-bodied** — `public int Area => W * H;` — verify it recomputes. (co-11)
- **ex-23 · enum-define** — `enum Status { Ok, Error }` — verify a switch over it. (co-13)
- **ex-24 · array** — `int[] xs = {1, 2, 3};` — verify indexing. (co-14)
- **ex-25 · list-generic** — `List<string>` add/iterate — verify contents. (co-14)
- **ex-26 · dictionary** — `Dictionary<string, int>` — verify keyed lookup. (co-14)

### Intermediate

- **ex-27 · interface-define** — `interface IShape { double Area(); }` — verify it compiles as a contract. (co-08)
- **ex-28 · interface-implement** — a `Circle : IShape` — verify conformance. (co-08)
- **ex-29 · default-interface-member** — a default method body in an interface — verify implementers inherit it. (co-08)
- **ex-30 · inheritance-base** — `class Dog : Animal` — verify base access. (co-09)
- **ex-31 · override-virtual** — `override` a `virtual` method — verify polymorphic dispatch. (co-09)
- **ex-32 · record-define** — `record Point(int X, int Y);` — verify construction. (co-12)
- **ex-33 · record-value-equality** — compare two equal records with `==` — verify value equality. (co-12)
- **ex-34 · record-with** — `p with { X = 5 }` — verify a non-destructive copy. (co-12)
- **ex-35 · record-positional** — deconstruct a positional record — verify the members bind. (co-12)
- **ex-36 · struct-value** — a `struct Vec` — verify value-copy semantics. (co-26)
- **ex-37 · struct-vs-class** — the same shape as struct vs class — verify the aliasing difference. (co-26, co-03)
- **ex-38 · generic-method** — `T First<T>(IEnumerable<T> xs)` — verify it works for two types. (co-15)
- **ex-39 · generic-class** — `class Box<T>` — verify parameterized construction. (co-15)
- **ex-40 · generic-constraint** — `where T : IComparable<T>` — verify the constraint is enforced. (co-15)
- **ex-41 · linq-query-where** — `from x in xs where x > 0 select x` — verify filtering. (co-16)
- **ex-42 · linq-query-select** — a `select` projection — verify the shape. (co-16)
- **ex-43 · linq-method-where** — `xs.Where(x => x > 0)` — verify filtering. (co-17)
- **ex-44 · linq-method-orderby** — `.OrderBy(x => x)` — verify ordering. (co-17)
- **ex-45 · linq-chain** — `.Where().Select().OrderBy()` — verify the composed result. (co-17)
- **ex-46 · deferred-execution** — enumerate a query twice after mutating the source — verify it re-evaluates. (co-18)
- **ex-47 · immediate-execution** — `.ToList()`/`.Count()` — verify eager evaluation. (co-18)
- **ex-48 · lambda-expression** — `x => x * 2` — verify the computation. (co-19)
- **ex-49 · func-delegate** — `Func<int, int>` — verify invocation. (co-19)
- **ex-50 · action-delegate** — `Action<string>` — verify the side effect. (co-19)
- **ex-51 · lambda-in-linq** — a lambda inside `Select` — verify the transform. (co-19, co-17)
- **ex-52 · list-of-records** — a `List<Point>` queried with LINQ — verify results. (co-12, co-14)
- **ex-53 · interface-polymorphism** — an `IShape[]` of mixed types — verify dynamic dispatch. (co-08, co-09)
- **ex-54 · nuget-add-package** — `dotnet add package` a library — verify it resolves and imports. (co-25)

### Advanced

- **ex-55 · switch-expression** — a `switch` expression returning a value — verify the matched arm. (co-20)
- **ex-56 · is-pattern** — `if (o is int n)` — verify the type-pattern bind. (co-20)
- **ex-57 · property-pattern** — `p is { X: 0 }` — verify the property match. (co-20)
- **ex-58 · tuple-pattern** — a `switch` over `(a, b)` — verify the tuple arm. (co-20)
- **ex-59 · try-catch** — wrap risky code — verify the catch runs on error. (co-21)
- **ex-60 · catch-specific-exception** — `catch (FormatException e)` — verify the specific catch. (co-21)
- **ex-61 · finally-block** — a `finally` — verify it runs on both paths. (co-21)
- **ex-62 · throw-custom** — throw a custom `Exception` subclass — verify it propagates. (co-21)
- **ex-63 · throw-expression** — `?? throw new ArgumentNullException()` — verify the throw expression. (co-21, co-11)
- **ex-64 · async-method** — `async Task Foo()` — verify it compiles as async. (co-22)
- **ex-65 · await-task** — `await SomeTask()` — verify it resumes after completion. (co-22)
- **ex-66 · async-return-value** — `async Task<int>` — verify the awaited value. (co-22)
- **ex-67 · async-non-blocking** — show the thread isn't blocked during `await` — verify concurrency. (co-22)
- **ex-68 · multiple-await** — sequential `await`s — verify order. (co-22)
- **ex-69 · task-whenall** — `await Task.WhenAll(...)` — verify all complete. (co-22)
- **ex-70 · async-exception** — an exception thrown in an async method caught by the awaiter — verify the error path. (co-22, co-21)
- **ex-71 · linq-aggregate** — `.Aggregate(...)` / `.Sum()` — verify the reduction. (co-17)
- **ex-72 · generic-linq-combined** — a generic method returning a LINQ result — verify it works over types. (co-15, co-17)
- **ex-73 · record-pattern-match** — a `switch` on a record with property patterns — verify the arms. (co-12, co-20)
- **ex-74 · nullable-linq** — a LINQ query over nullable elements handling null safely — verify no NRE. (co-05, co-17)
- **ex-75 · interface-generic** — `IRepository<T>` — verify a typed implementation. (co-08, co-15)
- **ex-76 · async-linq-pipeline** — await a fetch then LINQ over the result — verify the pipeline. (co-22, co-17)
- **ex-77 · domain-model-slice** — a class + a record + an interface modeling a small domain — verify they compose. (co-07, co-12, co-08)
- **ex-78 · capstone-cli** — a console app with nullable-aware code, records, a LINQ query, an interface, and an `async`/`await` call — verify `dotnet run` output and `dotnet test` pass. (co-05, co-12, co-16, co-08, co-22, co-01)

## Capstone spec — intra-topic (primer → light consolidation)

- **Goal**: build a small C# console app that exercises the primer's surface — nullable reference types,
  records, a LINQ query over a collection, an interface, and a single `async`/`await` call — runnable via
  `dotnet run` + a `dotnet test`, proving readiness for Windows app development.
- **Concepts exercised**: [ ] nullable reference types (co-05) [ ] records (co-12) [ ] a LINQ query (co-16)
  [ ] an interface (co-08) [ ] an `async`/`await` call (co-22) [ ] a `dotnet test` (co-01).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — a console app using records + a LINQ query with nullable-aware code.
     Verify `dotnet run` produces the expected output.
  2. Add an interface + an implementation. Verify dispatch works.
  3. Add an `async` method + an `await` call + a `dotnet test`. Verify the async path completes and the test
     passes.
- **Acceptance criteria**: records, LINQ, and nullable handling work; the interface dispatches; the
  `async`/`await` call completes; `dotnet test` passes.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **C# 12 in a Nutshell: The Definitive Reference** — Joseph Albahari (2023, O'Reilly). The field's definitive desktop-reference C# book, continuously updated with each language version.

**Papers & articles**

- **C# documentation** — Microsoft, official (Microsoft Learn). The authoritative, free language and API reference. <https://learn.microsoft.com/en-us/dotnet/csharp/>
- **ECMA-334: C# Language Specification**, 6th ed. — Ecma International (2022). The formal, standards-body specification of the C# language. <https://ecma-international.org/publications-and-standards/standards/ecma-334/>

## In which paths

- `immediately-effective/software-engineer` — Deepening band · Mobile & desktop platforms — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 11 · Mobile & desktop platforms.

> _Content originated in the now-closed FS-SE plan (topic 74); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
