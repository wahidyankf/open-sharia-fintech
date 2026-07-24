# Just Enough Java (Primer, Java)

**Course ID**: `just-enough-java` · **Format**: Primer · **Language**: Java.

**Short summary**: Java syntax, the JVM, collections, idioms

**Scope note**: **just enough modern Java** to be productive on the JVM
([`85-enterprise-java-and-the-jvm`](./enterprise-java-and-the-jvm.md)). How to run Java both ways — a
one-off single source file (`java Hello.java`) and a full Maven/Gradle project; records, sealed types, and
pattern matching; generics; collections and streams; and the memory model at a glance. `†`: Java, run as a
single source file for one-offs and built with a standard JVM build tool for projects.

## Why this exists · the big idea

- **The problem before the solution**: Java carries decades of reputation for verbosity, and an engineer
  arriving from a modern typed language expects the boilerplate of 2005 — meanwhile the language has quietly
  modernized, and the enterprise JVM pass deserves that modern baseline rather than time spent on ceremony.
- **Keep-this-if-you-forget-everything**: modern Java is a statically typed, garbage-collected language whose
  recent additions — records, sealed types, pattern matching, and streams — remove most of the old
  boilerplate; know these and the collections/streams API and you can read and write idiomatic current Java.
- **Big ideas touched**: `taming-state` (the JVM's garbage collector and memory model handle the mutable
  shared state that systems languages made you manage by hand — records push you toward immutable data),
  `abstraction-and-its-cost` (the JVM abstracts away the machine for portability and safety — the cost is a
  runtime and a memory model you occasionally have to reason about explicitly).

## Prerequisites

- **Prior topics**: [topic 8 Object-Oriented Programming Essentials](./object-oriented-programming-essentials.md)
  (classes, interfaces, inheritance — Java is the canonical mainstream OO language these map onto).
- **Tools & environment**: a macOS/Linux/Windows machine; a **JDK** pinned to a current LTS and a standard
  build tool (**Maven** or **Gradle**); Neovim/VSCode with the Java LSP (DD-17).
- **Assumed knowledge**: classes/interfaces/inheritance (topic 08); static types and generics from an
  earlier typed language (topic 13); running a CLI build tool (topic 05).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: keep the JDK at "a current LTS" in shipped text rather than a pinned number —
  Java ships an LTS every few years (the JLS reference below is the SE 21 edition), and records, sealed
  types, pattern matching, generics, and the streams/collections API are stable, finalized language
  features. Re-pull the exact current LTS at authoring time.
- 2026-07-12 — verified: Maven and Gradle are both current, actively maintained build tools — reference
  them by role and keep any specific version unpinned; the primer stays on the standard library, so no
  third-party dependency version is claimed.

### DD-35 primary-source citations (fetched-and-read)

> Anti-hallucination (DD-35): every version/feature below traces to a primary source a
> `web-researcher` fetched and read on 2026-07-12. Unverifiable claims are marked `[Needs Verification]`.

- **JDK version** — the current LTS is **Java 25** (Java 26 is the latest non-LTS); shipped prose keeps "a
  current LTS", not a pinned number, and re-pulls at authoring time. Records, sealed types, pattern matching
  (`instanceof` + `switch`, incl. record deconstruction), generics, and the collections/streams API are all
  finalized, stable features. Verified against the Java Language Specification + OpenJDK.
- **Test library** — modern JUnit is **JUnit 6** (`org.junit.jupiter`), NOT JUnit 5 — cite JUnit 6 for
  `@Test`/`assertEquals`/parameterized tests. Verified against junit.org.
- **Build tools** — Maven and Gradle are both current, actively maintained; referenced by role, versions
  unpinned. The primer stays on the standard library, so no third-party dependency version is claimed
  beyond the test library.
- **One-off run (co-27/28, ex-79/80)** — added 2026-07-12 and DD-35-verified against openjdk.org the same
  day: single-file source-code launch (`java Hello.java`, compiled in memory, no `javac`, no `.class`)
  shipped in **Java 11** as **JEP 330** ([openjdk.org/jeps/330](https://openjdk.org/jeps/330) — "the source
  file is compiled into memory, and the first class found in the source file is executed"); compact source
  files + instance `void main()` (no explicit `class`, no `static`, no `String[]`) were **finalized in
  Java 25** as **JEP 512** ([openjdk.org/jeps/512](https://openjdk.org/jeps/512)), after the preview lineage
  **JEP 445** (JDK 21) → **463** (22) → **477** (23) → **495** (24). Titles evolved Unnamed Classes → Implicitly
  Declared Classes → Simple → Compact Source Files. Java 25 is the current LTS (GA 2025-09-16); Java 26 is the
  latest non-LTS (GA 2026-03-17).

## Concepts

<!-- co-01 · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (Primer, subject band). Each example below cites the co-NN it exercises. -->

- **co-01 · jdk-build-tool** — a Maven or Gradle project compiles, runs, and tests Java from the terminal.
- **co-02 · main-method** — `public static void main(String[])` is the program entry point.
- **co-03 · primitives** — `int`/`double`/`boolean`/`char`, their wrapper types, autoboxing, and `String`.
- **co-04 · classes-objects** — a class defines fields, a constructor, and methods; `new` instantiates it.
- **co-05 · interfaces** — an `interface` (with default methods) is implemented by classes for polymorphism.
- **co-06 · inheritance** — `extends` + `@Override` give subtype polymorphism.
- **co-07 · records** — a `record` is a concise, immutable data class with generated accessors/`equals`/`hashCode`.
- **co-08 · sealed-types** — `sealed` interfaces/classes with `permits` close a type hierarchy.
- **co-09 · enums** — an `enum` is a fixed set of typed constants, optionally with fields and methods.
- **co-10 · instanceof-pattern** — `instanceof` pattern matching binds the tested value to a typed variable.
- **co-11 · switch-pattern** — `switch` pattern matching (with record deconstruction and guards) dispatches over a sealed type.
- **co-12 · exhaustive-switch** — a `switch` over a sealed type is exhaustive with no `default` needed.
- **co-13 · generics** — generic classes and methods parameterize over types for compile-time safety.
- **co-14 · bounded-generics** — bounded type parameters (`extends`) and wildcards (`? extends`) express constraints/variance.
- **co-15 · collections-list** — `List`/`ArrayList` is the ordered, indexed collection.
- **co-16 · collections-map** — `Map`/`HashMap` is the key-value collection.
- **co-17 · collections-set** — `Set`/`HashSet` is the uniqueness collection.
- **co-18 · streams-map-filter** — `Stream` `map`/`filter` build lazy pipelines over collections.
- **co-19 · streams-collect** — `collect`/`Collectors` materialize a stream into a collection or grouping.
- **co-20 · streams-reduce** — `reduce`/`count`/`sum` aggregate a stream to a single value.
- **co-21 · lambdas** — lambda expressions implement functional interfaces inline.
- **co-22 · method-references** — method references are a terse form of a lambda that just calls a method.
- **co-23 · optional** — `Optional<T>` models a possibly-absent value without null.
- **co-24 · exceptions** — checked vs unchecked exceptions, `try`/`catch`, and custom exception types.
- **co-25 · jvm-memory** — heap vs stack, garbage collection, and object identity (`==`) vs equality (`equals`).
- **co-26 · junit-test** — a JUnit 6 `@Test` with assertions runs under the build tool.
- **co-27 · single-file-source-run** — `java Hello.java` runs a single `.java` source file directly, compiled
  in memory with no explicit `javac` step and no produced `.class` — the one-off/scripting entry point that
  complements the Maven/Gradle project of co-01 (JEP 330, launch single-file source-code programs, since Java 11).
- **co-28 · compact-source-and-instance-main** — a compact source file needs no explicit `class` declaration
  and uses an instance `void main()` (no `static`, no `String[]` required), so the smallest runnable Java
  program is a few lines — the modern on-ramp before the full `public static void main(String[])` of co-02
  (JEP 512, compact source files and instance main methods, finalized in Java 25).

## Worked examples

Colocated under `just-enough-java/learning/code/`; each runnable via the build tool (DD-20/DD-30), except the
one-off examples ex-79/ex-80 which run directly with `java <file>`. Contiguous `ex-01..ex-80`. Every example
cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · maven-project** — a Maven/Gradle project compiles — verify the build. (co-01)
- **ex-02 · hello-main** — a `main` method prints — verify the output. (co-02)
- **ex-03 · run-build-tool** — run via `mvn`/`gradle` — verify execution. (co-01)
- **ex-04 · primitives** — `int`/`double` arithmetic — verify the result. (co-03)
- **ex-05 · boolean-char** — a `boolean` and a `char` — verify the values. (co-03)
- **ex-06 · wrapper-boxing** — `Integer` autoboxing — verify the conversion. (co-03)
- **ex-07 · class-def** — a class with fields — verify instantiation. (co-04)
- **ex-08 · class-methods** — methods on a class — verify the call. (co-04)
- **ex-09 · constructor** — a constructor — verify initialization. (co-04)
- **ex-10 · interface** — an interface + `implements` — verify polymorphism. (co-05)
- **ex-11 · inheritance** — `extends` + `@Override` — verify dispatch. (co-06)
- **ex-12 · record-basic** — a `record` — verify the accessors. (co-07)
- **ex-13 · record-equals** — a record's generated `equals`/`hashCode` — verify equality. (co-07)
- **ex-14 · enum-basic** — an `enum` — verify a constant. (co-09)
- **ex-15 · enum-switch** — a `switch` over an enum — verify each case. (co-09, co-11)
- **ex-16 · list-basic** — a `List` add/get — verify the elements. (co-15)
- **ex-17 · list-iterate** — iterate a `List` — verify the traversal. (co-15)
- **ex-18 · map-basic** — a `Map` put/get — verify the lookup. (co-16)
- **ex-19 · set-basic** — a `Set`'s uniqueness — verify dedup. (co-17)
- **ex-20 · generic-list** — `List<String>` vs `List<Integer>` — verify type safety. (co-13, co-15)
- **ex-21 · for-each** — the enhanced `for` loop — verify iteration. (co-15)
- **ex-22 · string-methods** — `String` operations — verify the results. (co-03)
- **ex-23 · try-catch** — a `try`/`catch` — verify the exception is caught. (co-24)
- **ex-24 · checked-exception** — a declared checked exception — verify handling. (co-24)
- **ex-25 · null-handling** — a `NullPointerException` guard — verify the safe path. (co-24)
- **ex-26 · equals-vs-identity** — `==` vs `equals` for objects — verify the difference. (co-25)

### Intermediate

- **ex-27 · record-compact-ctor** — a compact constructor validating input — verify the validation. (co-07)
- **ex-28 · sealed-interface** — a `sealed` interface with `permits` — verify the closed hierarchy. (co-08)
- **ex-29 · sealed-record-hierarchy** — a sealed + records shape hierarchy — verify the variants. (co-08, co-07)
- **ex-30 · instanceof-pattern** — an `instanceof` pattern binding — verify the bound variable. (co-10)
- **ex-31 · switch-pattern** — a `switch` pattern over a sealed type — verify each arm. (co-11)
- **ex-32 · switch-exhaustive** — an exhaustive `switch` with no `default` — verify it compiles. (co-12)
- **ex-33 · switch-guard** — a `switch` pattern guard (`when`) — verify the conditional arm. (co-11)
- **ex-34 · switch-record-deconstruct** — record deconstruction in a `switch` — verify the destructure. (co-11, co-07)
- **ex-35 · generic-method** — a generic method — verify it works for two types. (co-13)
- **ex-36 · generic-class** — a generic class — verify it holds a type. (co-13)
- **ex-37 · bounded-type** — a bounded type parameter (`extends`) — verify the bound. (co-14)
- **ex-38 · wildcard** — a wildcard (`? extends`) — verify the variance. (co-14)
- **ex-39 · map-iterate** — iterate `Map` entries — verify the traversal. (co-16)
- **ex-40 · map-compute** — `computeIfAbsent` — verify insert-or-get. (co-16)
- **ex-41 · stream-map** — a stream `map` — verify the transform. (co-18)
- **ex-42 · stream-filter** — a stream `filter` — verify the selection. (co-18)
- **ex-43 · stream-collect-list** — `collect` to a `List` — verify materialization. (co-19)
- **ex-44 · stream-collect-map** — `collect` to a `Map` (`toMap`) — verify the mapping. (co-19)
- **ex-45 · stream-reduce** — `reduce`/`sum` — verify the accumulation. (co-20)
- **ex-46 · stream-count** — `count`/`anyMatch` — verify the aggregate. (co-20)
- **ex-47 · lambda-basic** — a lambda for a functional interface — verify the invocation. (co-21)
- **ex-48 · lambda-comparator** — a lambda `Comparator` sort — verify the order. (co-21)
- **ex-49 · method-reference** — a method reference — verify it equals the lambda form. (co-22)
- **ex-50 · optional-basic** — an `Optional` present/empty — verify both. (co-23)
- **ex-51 · optional-map** — `Optional.map`/`orElse` — verify the chaining. (co-23)
- **ex-52 · stream-of-records** — a stream over records — verify the pipeline. (co-18, co-07)

### Advanced

- **ex-53 · grouping-collector** — `Collectors.groupingBy` — verify the grouping. (co-19)
- **ex-54 · stream-flatmap** — `flatMap` — verify the flattening. (co-18)
- **ex-55 · stream-sorted** — `sorted` with a comparator — verify the order. (co-18)
- **ex-56 · stream-distinct** — `distinct` — verify the dedup. (co-18)
- **ex-57 · sealed-visitor** — a sealed type processed exhaustively — verify each variant. (co-08, co-11)
- **ex-58 · nested-record-pattern** — nested record patterns in a `switch` — verify the deep destructure. (co-11)
- **ex-59 · generic-bounded-method** — a generic method with a bound + stream — verify the constraint. (co-14, co-18)
- **ex-60 · optional-in-stream** — `Optional` in a stream (`flatMap`) — verify absence handling. (co-23, co-18)
- **ex-61 · exception-in-stream** — exception handling in a pipeline — verify clean failure. (co-24, co-18)
- **ex-62 · custom-exception** — a custom exception class — verify it propagates. (co-24)
- **ex-63 · immutable-record-collection** — an immutable collection of records — verify no mutation. (co-07, co-15)
- **ex-64 · record-as-map-key** — a record as a `Map` key — verify lookup by value. (co-07, co-16)
- **ex-65 · enum-with-fields** — an enum with fields/methods — verify the behavior. (co-09)
- **ex-66 · interface-default-method** — an interface default method — verify inherited behavior. (co-05)
- **ex-67 · gc-object-lifecycle** — object creation and GC eligibility — verify identity. (co-25)
- **ex-68 · heap-vs-stack** — stack locals vs heap objects — verify the distinction. (co-25)
- **ex-69 · junit-test-basic** — a JUnit 6 `@Test` — verify it passes. (co-26)
- **ex-70 · junit-assertions** — `assertEquals`/`assertThrows` — verify the assertions. (co-26)
- **ex-71 · junit-parameterized** — a parameterized test — verify multiple cases. (co-26)
- **ex-72 · build-run-test** — `mvn`/`gradle test` runs the suite — verify green. (co-01, co-26)
- **ex-73 · streams-pipeline-full** — a multi-stage streams pipeline — verify the result. (co-18, co-19, co-20)
- **ex-74 · sealed-plus-pattern-full** — a sealed hierarchy fully pattern-matched — verify exhaustiveness. (co-08, co-12)
- **ex-75 · generics-collections-streams** — generics + collections + streams together — verify a type-safe pipeline. (co-13, co-15, co-18)
- **ex-76 · full-primer-slice** — record + sealed + pattern + generic collection + streams in one program — verify the whole. (co-07, co-08, co-11, co-18)
- **ex-77 · integration-build-test** — the whole program built + tested under Maven/Gradle — verify green. (co-01, co-26)
- **ex-78 · capstone-java-primer** — a modern-Java program: a record, a sealed type consumed with pattern matching, a generic collection, a streams pipeline, a Maven/Gradle build + passing test — verify the record + generic collection work, the sealed type is matched exhaustively, the streams pipeline is correct, and the build + test pass. (co-07, co-08, co-11, co-18, co-01, co-26)

### One-off run (single-file)

- **ex-79 · single-file-source-run** — write `Hello.java` and run it directly with `java Hello.java`, no separate `javac` step — verify it prints and that no `.class` file is produced (source is compiled in memory). (co-27)
- **ex-80 · compact-source-instance-main** — the same program as a compact source file: no `class` declaration, an instance `void main()` (no `static`, no `String[]`) — verify it runs under `java <file>` and contrast its line count with ex-02's full `public static void main(String[])`. (co-28, co-02)

## Capstone spec — intra-topic (primer → light consolidation)

- **Goal**: build a small modern-Java program that exercises the primer's surface — a record, a sealed type
  consumed with pattern matching, a generic collection, and a streams pipeline — built and run with
  Maven/Gradle plus a passing test, proving readiness for the enterprise JVM pass.
- **Concepts exercised**: [ ] a record (co-07) [ ] a sealed type + pattern matching (co-08, co-11) [ ] a
  generic collection (co-13, co-15) [ ] a streams pipeline (co-18, co-19) [ ] a Maven/Gradle build (co-01)
  [ ] a unit test (co-26).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — a Maven/Gradle project with a record and a generic collection. Verify
     the build compiles and running it produces the expected output.
  2. Add a sealed type hierarchy consumed with `switch` pattern matching. Verify each variant is handled
     exhaustively and the match compiles without a default fall-through.
  3. Add a streams pipeline over the collection and a unit test. Verify the pipeline produces the expected
     result and the test passes under the build tool.
- **Acceptance criteria**: the record and generic collection work; the sealed type is matched exhaustively;
  the streams pipeline produces the expected result; the Maven/Gradle build and unit test pass.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Effective Java**, 3rd ed. — Joshua Bloch (2018). The essential idiomatic-Java reference by the former
  Java architect at Sun Microsystems and Google.
- **Head First Java**, 3rd ed. — Kathy Sierra, Bert Bates, Trisha Gee (2022). The most widely recommended
  beginner-friendly introduction to core Java language mechanics.
- **Core Java, Volume I — Fundamentals**, 12th ed. — Cay S. Horstmann (2021). Comprehensive, precise
  reference to Java language fundamentals; a longstanding classic.
- **Java: The Complete Reference**, 13th ed. — Herbert Schildt, Danny Coward (2024). Long-running,
  comprehensive single-volume Java language reference, updated for Java SE 21.

**Papers & articles**

- **The Java Language Specification, Java SE 21 Edition** — Oracle America, Inc. (2023). The official
  normative definition of Java syntax and semantics. <https://docs.oracle.com/javase/specs/jls/se21/jls21.pdf>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Concurrency, JVM & languages — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Concurrency & language breadth — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 3 · Concurrency & language breadth.

> _Content originated in the now-closed FS-SE plan (topic 84); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
