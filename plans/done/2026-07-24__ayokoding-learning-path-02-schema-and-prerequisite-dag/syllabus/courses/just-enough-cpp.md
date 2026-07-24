# Just Enough C++ (Primer, C++)

**Course ID**: `just-enough-cpp` · **Format**: Primer · **Language**: C++. **NEW** — systems-language
principle on-ramp (manual memory / RAII / templates). **Prereq**: `just-enough-c`. Wazuh's C++ core is
one illustration, not the subject.

**Scope note**: **just enough C++** to read and contribute to a modern C++ codebase — the delta over C
that matters: **RAII** and destructors, references, `class`/access, constructors/`~`destructors,
operator overloading (lightly), **templates** and the **STL** (containers, iterators, algorithms),
**smart pointers** (`unique_ptr`/`shared_ptr`), namespaces, and the `cmake`/compiler toolchain. It
builds directly on `just-enough-c` (pointers, structs, the compile/link loop) and keeps that a pure C
ramp. Proof-of-transfer target: `wazuh/wazuh` (C++ manager/agent core), not a subject.

## Why this exists · the big idea

- **The problem before the solution**: enormous, important systems (databases, browsers, security tools
  like Wazuh) are C++, and C alone does not prepare you to read them — manual `malloc`/`free` and raw
  pointers give way to RAII, the STL, templates, and smart pointers, and without those you cannot follow
  modern C++ or reason about its memory safety.
- **Keep-this-if-you-forget-everything**: C++ ties a resource's lifetime to an object's scope (RAII) — a
  destructor runs deterministically when the object leaves scope, so memory and resources clean
  themselves up if you let the type system own them.
- **Big ideas touched**: `taming-state` (RAII makes lifetime a structural property, not a manual chore),
  `abstraction-and-its-cost` (templates + the STL buy powerful zero-overhead abstractions at the cost of
  compile-time complexity and error verbosity).

## Prerequisites

- **Prior topics**: `just-enough-c` (pointers, structs, `stdio`, the compile/link
  loop, `make`) — a hard prerequisite; `just-enough-python` for a high-level contrast.
- **Tools & environment**: a macOS/Linux terminal; a C++ compiler (`g++`/`clang++`) targeting a modern
  standard (C++17/C++20 — pin at authoring); `cmake` + `make`; Neovim/VSCode with a C++ LSP (`clangd`).
- **Assumed knowledge**: C pointers, arrays, structs, functions, headers, and the compile/link build
  loop (topic 75); comfort with a terminal build step.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (per this plan's Anti-Hallucination verification recipe).

- 2026-07-19 — `[Needs Verification]`: the current C++ standard baseline to teach against (C++20 is
  widely available; C++23 is landing in compilers) and the exact `g++`/`clang++`/`cmake` versions — pin
  at authoring; keep examples portable to a conservative baseline (C++17) unless a newer feature is the
  point.
- 2026-07-19 — RAII, references, the STL (containers/iterators/algorithms), templates, and smart pointers
  (`std::unique_ptr`/`std::shared_ptr`) are **stable, core** C++ language + library concepts.
- 2026-07-19 — `[Needs Verification]`: `cmake` command surface and minimum version conventions evolve —
  re-verify the `CMakeLists.txt` idiom at authoring.

## Concepts

1. **co-01 · cpp-compiler-toolchain** — `g++`/`clang++` compile C++ to a binary; the compile/link loop
   extends the C one.
2. **co-02 · cmake-build** — `cmake` generates a build from a `CMakeLists.txt`, the common C++ build
   driver.
3. **co-03 · iostream** — `std::cout`/`std::cin` with `<<`/`>>` replace C's `printf`/`scanf` for typed
   I/O.
4. **co-04 · namespaces** — `namespace` groups names; `::` qualifies them; `using` imports selectively.
5. **co-05 · references** — a reference is an alias for an existing object, passed without pointer
   syntax.
6. **co-06 · const-correctness** — `const` on parameters, methods, and references expresses and enforces
   immutability.
7. **co-07 · auto-type-deduction** — `auto` deduces a variable's type from its initializer.
8. **co-08 · classes-and-access** — a `class` groups data + methods with `public`/`private`/`protected`
   access.
9. **co-09 · constructors** — a constructor initializes an object; member initializer lists set fields.
10. **co-10 · destructors-and-raii** — a destructor runs deterministically at end of scope, the basis of
    RAII resource management.
11. **co-11 · the-rule-of-three-five** — a class managing a resource needs a coordinated destructor, copy,
    and move (rule of three/five).
12. **co-12 · copy-vs-move** — copy duplicates; move transfers ownership cheaply via move semantics
    (`std::move`, rvalue refs).
13. **co-13 · operator-overloading** — operators (`+`, `==`, `<<`) can be defined for user types (used
    sparingly).
14. **co-14 · inheritance-and-virtual** — `class` inheritance + `virtual` methods enable runtime
    polymorphism.
15. **co-15 · smart-pointers-unique** — `std::unique_ptr` owns a heap object with single ownership,
    freeing it automatically.
16. **co-16 · smart-pointers-shared** — `std::shared_ptr` shares ownership via reference counting.
17. **co-17 · templates-functions** — a function template writes one definition parameterized over
    types.
18. **co-18 · templates-classes** — a class template parameterizes a type over element types (the basis
    of the STL containers).
19. **co-19 · stl-containers** — `std::vector`, `std::string`, `std::map`, `std::unordered_map` are the
    workhorse containers.
20. **co-20 · stl-iterators** — iterators abstract traversal across containers uniformly.
21. **co-21 · stl-algorithms** — `<algorithm>` (`sort`, `find`, `transform`, `accumulate`) operate over
    iterator ranges.
22. **co-22 · range-based-for** — `for (auto& x : container)` iterates a container idiomatically.
23. **co-23 · lambdas** — anonymous function objects with captures, passed to algorithms and callbacks.
24. **co-24 · exceptions** — `throw`/`try`/`catch` handle errors; RAII makes them safe by unwinding
    cleanly.
25. **co-25 · header-and-source-split** — declarations in `.hpp`, definitions in `.cpp`, compiled +
    linked (templates often header-only).
26. **co-26 · std-optional-and-variant** — `std::optional`/`std::variant` express "maybe" and "one of"
    type-safely (C++17).
27. **co-27 · compiler-warnings-and-sanitizers** — `-Wall -Wextra` + address/UB sanitizers surface bugs;
    clean builds are the goal.

## Tensions & trade-offs — when NOT to reach for this

- **Power vs complexity**: C++ gives zero-overhead abstractions and total control, at the cost of one of
  the largest, most feature-dense languages in existence — template errors are notoriously verbose and
  the footguns (dangling references, undefined behavior) are sharp. Reach for C++ where you need the
  performance + control and the ecosystem demands it (systems, security tooling), not by default.
- **Manual memory vs RAII vs GC**: C++ chooses deterministic RAII over C's manual `malloc`/`free` and
  over a garbage collector — no pauses, but you must think in ownership and lifetimes. When a task
  tolerates a GC, a managed language is simpler.
- **When NOT to reach for raw features**: raw `new`/`delete`, manual resource management, and heavy
  operator overloading are usually the wrong move in modern C++ — prefer smart pointers, RAII types, and
  the STL. This primer teaches the modern idiom, not the 1990s one.

## Lineage — why it beat the alternative

- C++ began as "C with classes" and grew RAII, templates, the STL, and (later) move semantics and smart
  pointers to give C's performance and control _without_ C's manual-memory drudgery and unsafety. RAII —
  tying resource lifetime to object scope — is its defining idea, and modern C++ (smart pointers, the
  STL, `optional`/`variant`) is a deliberate move away from raw pointers and manual `new`/`delete`
  toward safety by construction. It kept mindshare in systems, databases, browsers, games, and security
  tooling (Wazuh's core) precisely where a GC pause or a higher-level language's overhead is
  unacceptable. This primer builds on `just-enough-c` and equips the reader for the
  low-level systems topics and C++ codebases.

## Worked examples

Colocated under `just-enough-cpp/learning/code/`; each built via `g++`/`clang++` + `cmake`,
compiled warning-clean. Contiguous `ex-01..ex-72`. Every example cites the `co-NN` it
exercises. Concepts come before examples.

> **Volume-target floor**: this syllabus lists **72** of the required **≥75** (the 75–85 Primer band,
> floor not cap — see
> [prd.md §Volume-target bands](../../prd.md#new-course--capstone-specifications)).
> The maker adds **≥3** more `ex-NN` entries at authoring time, continuing the numbering and pattern
> taxonomy below, before this topic passes its primer quality gate.

### Beginner (ex 01–24)

1. **ex-01 · g++-compile** — `g++ hello.cpp -o hello` — verify a binary. (co-01)
2. **ex-02 · iostream-hello** — `std::cout << "..."` — verify output. (co-03)
3. **ex-03 · cin-input** — read an int with `std::cin` — verify the value. (co-03)
4. **ex-04 · cmake-build** — a minimal `CMakeLists.txt` + build — verify `cmake` builds the binary.
   (co-02)
5. **ex-05 · namespace-basic** — define + use a `namespace` — verify qualified access. (co-04)
6. **ex-06 · using-declaration** — a selective `using` — verify unqualified access. (co-04)
7. **ex-07 · auto-deduction** — `auto` for a deduced local — verify the type. (co-07)
8. **ex-08 · reference-basic** — a reference alias — verify it tracks the original. (co-05)
9. **ex-09 · reference-parameter** — pass by reference to mutate — verify the caller sees the change.
   (co-05)
10. **ex-10 · const-reference-param** — pass a large object by `const&` — verify no copy + no mutation.
    (co-05, co-06)
11. **ex-11 · const-method** — a `const` member method — verify it cannot mutate the object. (co-06,
    co-08)
12. **ex-12 · class-basic** — a `class` with public data + a method — verify member access. (co-08)
13. **ex-13 · private-encapsulation** — private fields + a public accessor — verify encapsulation.
    (co-08)
14. **ex-14 · constructor** — a constructor with a member initializer list — verify initialization.
    (co-09)
15. **ex-15 · destructor-trace** — a destructor logging at scope end — verify deterministic cleanup.
    (co-10)
16. **ex-16 · raii-file-wrapper** — a class opening a file in its ctor, closing in its dtor — verify the
    file closes at scope end. (co-10)
17. **ex-17 · std-string** — `std::string` operations (concat, length) — verify results. (co-19)
18. **ex-18 · std-vector-basic** — a `std::vector<int>` push/index — verify elements. (co-19)
19. **ex-19 · range-based-for** — iterate a vector with `for (auto& x : v)` — verify traversal. (co-22)
20. **ex-20 · vector-of-strings** — a `std::vector<std::string>` — verify iteration. (co-19, co-22)
21. **ex-21 · std-map** — a `std::map` insert + lookup — verify ordering + values. (co-19)
22. **ex-22 · unordered-map** — a `std::unordered_map` count — verify O(1) lookup. (co-19)
23. **ex-23 · warnings-clean** — compile with `-Wall -Wextra` — verify no warnings. (co-27)
24. **ex-24 · header-source-split** — declare a class in `.hpp`, define in `.cpp` — verify it links.
    (co-25)

### Intermediate (ex 25–50)

1. **ex-25 · function-template** — a `template<typename T>` max function — verify it works for int +
   double. (co-17)
2. **ex-26 · template-multiple-types** — a two-type function template — verify instantiation. (co-17)
3. **ex-27 · class-template** — a simple `template` container class — verify it holds different types.
   (co-18)
4. **ex-28 · stl-sort** — `std::sort` a vector — verify ordering. (co-21)
5. **ex-29 · stl-find** — `std::find` in a range — verify hit/miss. (co-21, co-20)
6. **ex-30 · stl-transform** — `std::transform` a vector — verify the mapped result. (co-21)
7. **ex-31 · stl-accumulate** — `std::accumulate` a sum — verify the total. (co-21)
8. **ex-32 · iterator-explicit** — iterate with explicit `begin()`/`end()` iterators — verify traversal.
   (co-20)
9. **ex-33 · lambda-basic** — a lambda passed to `std::sort` for custom order — verify the ordering.
   (co-23, co-21)
10. **ex-34 · lambda-capture** — a lambda capturing a local by value + by reference — verify each
    semantics. (co-23)
11. **ex-35 · unique-ptr** — `std::unique_ptr` owning a heap object — verify auto-free at scope end.
    (co-15)
12. **ex-36 · unique-ptr-move** — move a `unique_ptr` (transfer ownership) — verify the source is null.
    (co-15, co-12)
13. **ex-37 · shared-ptr** — `std::shared_ptr` shared ownership — verify the refcount + auto-free.
    (co-16)
14. **ex-38 · shared-ptr-cycle-awareness** — a refcount cycle leak + the `weak_ptr` fix — verify the leak
    then the fix. (co-16)
15. **ex-39 · raii-vs-manual-new** — contrast raw `new`/`delete` with a `unique_ptr` — verify the smart
    pointer prevents the leak. (co-15, co-10)
16. **ex-40 · rule-of-three** — a resource-owning class with dtor + copy ctor + copy assign — verify
    correct copy. (co-11)
17. **ex-41 · move-semantics** — add a move ctor + move assign (rule of five) — verify a cheap move.
    (co-11, co-12)
18. **ex-42 · operator-overload-plus** — overload `+` for a small value type — verify addition. (co-13)
19. **ex-43 · operator-overload-stream** — overload `<<` for printing a type — verify `std::cout` output.
    (co-13, co-03)
20. **ex-44 · inheritance-virtual** — a base + derived with a `virtual` method — verify runtime dispatch.
    (co-14)
21. **ex-45 · abstract-base** — a pure-virtual interface + an implementation — verify polymorphism.
    (co-14)
22. **ex-46 · exception-throw-catch** — `throw`/`try`/`catch` an error — verify handling. (co-24)
23. **ex-47 · raii-exception-safety** — an exception unwinds through an RAII type — verify the resource
    still frees. (co-24, co-10)
24. **ex-48 · std-optional** — `std::optional` for a maybe-value — verify present/absent handling.
    (co-26)
25. **ex-49 · std-variant** — `std::variant` + `std::visit` — verify type-safe dispatch. (co-26)
26. **ex-50 · sanitizer-run** — compile with the address sanitizer + fix a caught bug — verify a clean
    run. (co-27)

### Advanced (ex 51–72)

1. **ex-51 · cmake-multi-target** — a `cmake` project with a library + an executable — verify linkage.
   (co-02, co-25)
2. **ex-52 · templated-container-full** — a small generic stack class template with push/pop — verify
   across types. (co-18, co-11)
3. **ex-53 · iterator-support-for-custom-type** — add `begin()`/`end()` to a custom container — verify
   range-based for works. (co-20, co-22)
4. **ex-54 · algorithm-on-custom-type** — run `std::sort` on a vector of a custom type via a comparator
   — verify ordering. (co-21, co-13)
5. **ex-55 · unique-ptr-factory** — a factory returning `unique_ptr` — verify ownership transfer to the
   caller. (co-15, co-12)
6. **ex-56 · polymorphic-container** — a `vector<unique_ptr<Base>>` of derived objects — verify virtual
   dispatch across it. (co-14, co-15)
7. **ex-57 · move-only-type** — a move-only resource type (deleted copy) — verify it cannot be copied.
   (co-11, co-12)
8. **ex-58 · raii-lock-guard** — an RAII scoped-lock wrapper — verify it releases at scope end. (co-10)
9. **ex-59 · exception-hierarchy** — a custom exception hierarchy caught by base — verify dispatch.
   (co-24, co-14)
10. **ex-60 · template-specialization** — specialize a template for one type — verify the specialized
    path. (co-17, co-18)
11. **ex-61 · lambda-in-algorithm-pipeline** — chain `transform` + `accumulate` with lambdas — verify the
    result. (co-23, co-21)
12. **ex-62 · const-correct-api** — design a small `const`-correct class API — verify const + non-const
    paths. (co-06, co-08)
13. **ex-63 · smart-pointer-tree** — a tree of nodes owned by `unique_ptr` — verify no leak on
    destruction. (co-15, co-10)
14. **ex-64 · optional-returning-parser** — a parser returning `std::optional` on failure — verify both
    outcomes. (co-26, co-24)
15. **ex-65 · variant-state-machine** — a small state machine over `std::variant` — verify transitions.
    (co-26)
16. **ex-66 · header-only-template-lib** — a header-only templated utility + a consumer — verify it
    compiles + links. (co-18, co-25)
17. **ex-67 · sanitizer-clean-suite** — build the examples under `-Wall -Wextra` + UB sanitizer — verify
    a clean run. (co-27)
18. **ex-68 · cmake-with-tests** — add a test target to the `cmake` project — verify `ctest`/the test runs.
    (co-02)
19. **ex-69 · c-interop** — call a C function from C++ with `extern "C"` — verify linkage across the
    boundary. (co-25, co-01)
20. **ex-70 · raii-resource-pool** — an RAII-managed small resource pool — verify acquire/release
    correctness. (co-10, co-15)
21. **ex-71 · integration-stl-raii-templates** — a program combining an STL container, a smart-pointer-
    owned resource, a template, and a lambda — verify end-to-end. (co-15, co-18, co-19, co-23)
22. **ex-72 · capstone-cpp-cli** — a `cmake`-built multi-file C++ CLI using classes + RAII + smart
    pointers + STL containers/algorithms + templates + exceptions, compiled warning + sanitizer clean —
    verify `cmake` builds, it runs correctly, and the sanitizer is clean. (co-02, co-08, co-10, co-15,
    co-17, co-19, co-21, co-24, co-27)

## Capstone spec — intra-topic (primer → light consolidation)

- **Goal**: build a small multi-file C++ CLI, driven by `cmake`, that exercises the primer's modern-C++
  surface — a class with RAII + a destructor, `unique_ptr` ownership, STL containers + algorithms + a
  lambda, a template, and exception handling — compiling warning-clean and sanitizer-clean, proving
  readiness to read a modern C++ codebase.
- **Concepts exercised**: [ ] `cmake` multi-file build (co-02, co-25) [ ] classes + RAII + destructors
  (co-08, co-10) [ ] smart pointers (co-15, co-16) [ ] templates (co-17, co-18) [ ] STL containers +
  algorithms + lambdas (co-19, co-21, co-23) [ ] exceptions + const-correctness (co-24, co-06).
- **Ordered steps**:
  1. `just-enough-cpp/learning/capstone/code/` — a class hierarchy with an RAII resource + `unique_ptr`
     ownership across a header/source split. Verify it compiles warning-clean.
  2. `CMakeLists.txt` — a `cmake` build with the library + executable (+ a test target). Verify `cmake`
     builds and the test runs.
  3. Use STL containers + an algorithm + a lambda + a template + exception handling in the program logic.
     Verify correct output.
  4. Build under `-Wall -Wextra` + the address/UB sanitizer. Verify a clean run.
- **Acceptance criteria**: the `cmake` multi-file build works; RAII + smart pointers manage all
  resources (no raw `new`/`delete` leak); STL, templates, and exceptions behave; the program compiles
  warning-clean and runs sanitizer-clean with correct output.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

- **A Tour of C++** — Bjarne Stroustrup (3rd ed.). The concise, authoritative modern-C++ primer from the
  language's creator.
- **Effective Modern C++** — Scott Meyers. The standard guide to smart pointers, move semantics, and
  modern idioms (C++11/14; still foundational).
- **cppreference.com** — the authoritative community reference for the language + the STL (pin the
  standard revision at authoring).

## In which paths

- `interview-ready/software-engineer` — Go deeper · Theory & low-level systems — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Concurrency & language breadth — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 4 · Systems programming & OS internals.

---

← Back to [README.md — course library catalog](./README.md)
