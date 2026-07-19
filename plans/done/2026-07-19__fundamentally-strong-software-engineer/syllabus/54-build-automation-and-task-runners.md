# 54 · Build Automation & Task Runners (By Example, multi-tool †)

**prd row**: Pass 3 · Build for the Real World · By Example · multi-tool † · Learn 154 / Drill 254 ·
Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: automating the repeatable work of a project — from simple command runners to
dependency-graph build systems. The spectrum: command runners that just name shell recipes
([`just`](https://just.systems), npm scripts), timestamp-driven incremental builders
([GNU Make](https://www.gnu.org/software/make/) + POSIX make), and content-hash, hermetic, cached
build systems ([Bazel](https://bazel.build), [Gradle](https://gradle.org)). `†`: the "language" is the
tool config itself — a `Makefile`, a `justfile`, `package.json` `"scripts"`, a `BUILD` file, a
`build.gradle(.kts)` — plus the `make`/`just`/`npm`/`bazel`/`gradle` CLIs against a real project (the
[`13-just-enough-typescript`](./13-just-enough-typescript.md) project + a compiled artifact). Wiring a
build tool into a pipeline is [`55-cicd-and-release-engineering`](./55-cicd-and-release-engineering.md);
here the build tool is the unit, not the pipeline.

## Why this exists · the big idea

- **The problem before the solution**: retyping the same `tsc && eslint && node build.js` by hand is
  slow, undocumented, and non-reproducible — and rebuilding _everything_ every time wastes minutes when
  one file changed. Ad-hoc shell scripts drift, hide the dependency order, and rebuild blindly.
- **Keep-this-if-you-forget-everything**: declare the artifacts, their inputs, and how to produce them —
  then let the tool rebuild _only what changed_ by comparing inputs to outputs. You describe the
  dependency graph, not the imperative steps.
- **Big ideas touched**: `mechanism-vs-policy` (you declare targets and prerequisites — the _policy_; the
  build tool is the reconciling _mechanism_ that decides what to run), `determinism-vs-emergence`
  (hermetic, content-hashed builds buy byte-reproducibility and cross-machine cache reuse; incremental
  correctness emerges from an accurate dependency graph).

## Prerequisites

- **Prior topics**: [topic 5 Just Enough Bash](./05-just-enough-bash.md) (recipes are shell commands),
  [topic 6 Version Control & Git](./06-version-control-and-git.md) (tracked source files are the build
  inputs), and [topic 13 Just Enough TypeScript](./13-just-enough-typescript.md) (a `package.json`
  project with an npm-scripts + `tsc` compile step to automate).
- **Tools & environment**: a macOS/Linux terminal; **GNU Make** (`make`); **just** (`just`); **Node.js +
  npm** for npm scripts; optionally **Bazel** (`bazel`/`bazelisk`) and **Gradle** (`gradle`/`gradlew`)
  for the hermetic/cached tier. Tool versions pinned where practical.
- **Assumed knowledge**: running shell commands and reading exit codes (topic 05); a project with source
  files that produce an artifact (topic 13); the idea of a file's modification time.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (DD-28) and a DD-35 primary-source pass, both
> 2026-07-12.

- 2026-07-12 — verified: **GNU Make 4.4.1** (released 2023-02-26; no newer release exists) — license
  GPL-3.0-or-later (source), manual under GFDL 1.3-or-later. **Timestamp-driven**: rebuild is decided by
  file modification times.
- 2026-07-12 — verified: **POSIX make** is IEEE Std 1003.1-2017 (Open Group Base Specifications Issue 7);
  `.POSIX` is the opt-in portability marker. Also mtime-driven.
- 2026-07-12 — verified: **just 1.56.0** (released 2026-07-10 — very fresh; fast-moving, **version-
  sensitive**) — license CC0-1.0. A **command runner, not a build system**: every recipe is treated as
  phony (always runs); no file-freshness model at all.
- 2026-07-12 — verified: **npm 12.0.1** is the current latest (npm v12 shipped recently with breaking
  security defaults; **version-sensitive**). The `scripts`/`run` behavior quoted below is from the
  official `/cli/v11/` docs; whether a distinct `/v12/` docs path supersedes it is `[Needs Verification]`,
  and the npm-CLI license (Artistic-2.0) was not re-verified against a primary source this pass —
  `[Needs Verification]`.
- 2026-07-12 — verified: **Bazel 9.1.1** is the current active LTS (9.2.0rc2 is a release candidate, not
  stable) — license Apache-2.0 (some bundled components differ). **Content-hash, hermetic, cached.**
- 2026-07-12 — verified: **Gradle 9.6.1** is current — license Apache-2.0. **Content-fingerprint
  incremental + build cache**; Groovy DSL (`.gradle`) and Kotlin DSL (`.gradle.kts`).

> DD-35 primary-source pass (2026-07-12). Rule semantics, freshness models, and CLI/target syntax traced
> to primary sources (gnu.org Make manual, pubs.opengroup.org POSIX, just.systems, docs.npmjs.com,
> bazel.build, docs.gradle.org) and fetched/read. Version numbers flagged version-sensitive above.

- **Make — rule model** — "A _target_ is usually the name of a file that is generated by a program";
  "A _prerequisite_ is a file that is used as input to create the target"; "A _recipe_ is an action that
  `make` carries out"; "A _rule_, then, explains how and when to remake certain files … `make` carries
  out the recipe on the prerequisites to create or update the target." Source:
  [Make — Rule Introduction](https://www.gnu.org/software/make/manual/html_node/Rule-Introduction.html) (fetched, verbatim).
- **Make — freshness** — "The recompilation must be done if the source file, or any of the header files
  named as prerequisites, is more recent than the object file, or if the object file does not exist."
  Source: [Make — How Make Works](https://www.gnu.org/software/make/manual/html_node/How-Make-Works.html) (fetched, verbatim).
- **Make — `.PHONY`** — "A phony target is one that is not really the name of a file; rather it is just a
  name for a recipe to be executed when you make an explicit request"; "The implicit rule search is
  skipped for `.PHONY` targets." Source:
  [Make — Phony Targets](https://www.gnu.org/software/make/manual/html_node/Phony-Targets.html) (fetched, verbatim).
- **Make — automatic variables** — "'$@' … The file name of the target of the rule"; "'$<' … The name of
  the first prerequisite"; "'$^' … The names of all the prerequisites, with spaces between them." Source:
  [Make — Automatic Variables](https://www.gnu.org/software/make/manual/html_node/Automatic-Variables.html) (fetched, verbatim).
- **Make — pattern rules** — "A pattern rule looks like an ordinary rule, except that its target contains
  the character '%' (exactly one of them)"; "the '%' can match any nonempty substring, while other
  characters match only themselves." Source:
  [Make — Pattern Rules](https://www.gnu.org/software/make/manual/html_node/Pattern-Rules.html) (fetched, verbatim).
- **Make — variable assignment** — recursive `=`: "The value you specify is installed verbatim; if it
  contains references to other variables, these references are expanded whenever this variable is
  substituted"; simply-expanded `:=`: "The value of a simply expanded variable is scanned once, expanding
  any references to other variables and functions, when the variable is defined." Sources:
  [Recursive Assignment](https://www.gnu.org/software/make/manual/html_node/Recursive-Assignment.html),
  [Simple Assignment](https://www.gnu.org/software/make/manual/html_node/Simple-Assignment.html) (fetched, verbatim).
- **Make — parallel** — "Specifies the number of recipes (jobs) to run simultaneously. With no argument,
  `make` runs as many recipes simultaneously as possible" (`-j`/`--jobs`). Source:
  [Make — Options Summary](https://www.gnu.org/software/make/manual/html_node/Options-Summary.html) (fetched, verbatim).
- **POSIX make** — ".POSIX: The application shall ensure that this special target is specified without
  prerequisites or commands"; "If it appears as the first non-comment line in the makefile, make shall
  process the makefile as specified by this section"; "The make utility shall use the modification times
  of files to determine whether the corresponding targets are out-of-date." Source:
  [POSIX make](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/make.html) (fetched, verbatim).
- **just** — "`just` is a command runner, not a build system, so it avoids much of make's complexity and
  idiosyncrasies"; "Commands, called recipes, are stored in a file called `justfile`"; "In `just`, all
  recipes are treated as if they were phony"; "Recipes may have parameters … Parameters may have default
  values … The last parameter of a recipe may be variadic." Sources:
  [just manual](https://just.systems/man/en/),
  [recipe parameters](https://just.systems/man/en/recipe-parameters.html) (fetched, verbatim).
- **npm scripts** — "The `\"scripts\"` property of your `package.json` file supports a number of built-in
  scripts and their preset life cycle events as well as arbitrary scripts"; "To create 'pre' or 'post'
  scripts for any scripts … simply create another script _with a matching name_ and add 'pre' or 'post'
  to the beginning of them"; "This runs an arbitrary command from a package's `\"scripts\"` object." Sources:
  [npm scripts](https://docs.npmjs.com/cli/v11/using-npm/scripts),
  [npm run](https://docs.npmjs.com/cli/v11/commands/npm-run/) (fetched, verbatim; v12-path `[Needs Verification]`).
- **Bazel — hermeticity & hashing** — "When given the same input source code and product configuration, a
  hermetic build system always returns the same output by isolating the build from changes to the host
  system"; "Bazel and some other build systems address this problem by requiring a workspacewide manifest
  file that lists a _cryptographic hash_ for every external dependency." Sources:
  [Bazel — Hermeticity](https://bazel.build/basics/hermeticity),
  [artifact-based builds](https://bazel.build/basics/artifact-based-builds) (fetched, verbatim).
- **Bazel — BUILD & targets & cache** — "By definition, every package contains a `BUILD` file, which is a
  short program"; `//...` = "All rule targets in packages in the main repository"; "A remote cache is used
  by a team of developers and/or a continuous integration (CI) system to share build outputs." Sources:
  [BUILD files](https://bazel.build/concepts/build-files),
  [build targets](https://bazel.build/run/build#specifying-build-targets),
  [remote caching](https://bazel.build/remote/caching) (fetched, verbatim).
- **Gradle — task graph & incremental & cache** — "Across all projects in the build, tasks form a Directed
  Acyclic Graph (DAG)"; "Gradle builds the task graph **before** executing any task(s)"; "Before a task is
  executed for the first time, Gradle takes a fingerprint of the inputs. This fingerprint contains the
  paths of input files and a hash of the contents of each file"; "The Gradle build cache is a cache
  mechanism that aims to save time by reusing outputs produced by other builds"; "Groovy DSL script files
  use the `.gradle` file name extension" / "Kotlin DSL script files use the `.gradle.kts` file name
  extension." Sources:
  [build lifecycle](https://docs.gradle.org/current/userguide/build_lifecycle.html),
  [incremental build](https://docs.gradle.org/current/userguide/incremental_build.html),
  [build cache](https://docs.gradle.org/current/userguide/build_cache.html),
  [Kotlin DSL](https://docs.gradle.org/current/userguide/kotlin_dsl.html) (fetched, verbatim).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. Concepts come before examples. -->

- **co-01 · why-build-automation** — automating repeatable project work makes it fast, documented, and
  reproducible, versus retyping ad-hoc shell.
- **co-02 · task-runner-vs-build-system** — a command runner just names recipes; a build system models a
  dependency graph and rebuilds only what changed.
- **co-03 · make-rules** — a Make rule is a target, its prerequisites, and a recipe that produces the
  target from the prerequisites.
- **co-04 · dependency-graph-dag** — targets and prerequisites form a directed acyclic graph the tool
  walks to order work.
- **co-05 · incremental-rebuild-timestamps** — Make rebuilds a target when a prerequisite is newer (by
  modification time) or the target is missing.
- **co-06 · phony-targets** — `.PHONY` marks a recipe-name that is not a file (`clean`, `all`), so it
  always runs and skips implicit-rule search.
- **co-07 · automatic-variables** — `$@` (target), `$<` (first prerequisite), `$^` (all prerequisites)
  keep recipes DRY.
- **co-08 · pattern-rules** — a `%`-pattern rule (`%.o: %.c`) generates a rule per matching stem.
- **co-09 · variable-assignment** — recursive `=` expands at use; simply-expanded `:=` expands once at
  definition.
- **co-10 · builtin-implicit-rules** — Make ships built-in rules and variables (`$(CC)`, `.c`→executable)
  that fire without an explicit rule.
- **co-11 · make-functions** — text functions like `$(wildcard …)` and `$(patsubst …)` compute variable
  values.
- **co-12 · parallel-make** — `make -j` runs independent recipes concurrently; a correct graph makes this
  safe.
- **co-13 · posix-make-portability** — `.POSIX` as the first line selects the portable, standardized
  make behavior across vendors.
- **co-14 · command-runner-just** — `just` runs named recipes from a `justfile`; every recipe is phony
  (always runs), with no freshness model.
- **co-15 · just-recipes-parameters** — just recipes take positional parameters, default values, and a
  trailing variadic parameter.
- **co-16 · just-vs-make** — pick a command runner for task aliases; pick a build system when you need
  incremental artifact rebuilds.
- **co-17 · npm-scripts** — `package.json` `"scripts"` name commands run via `npm run <name>`.
- **co-18 · npm-pre-post-hooks** — a `pre<name>`/`post<name>` script auto-runs before/after `<name>`.
- **co-19 · npm-lifecycle-scripts** — built-in lifecycle names (`test`, `start`, `install`) have
  shortcut commands and hook points.
- **co-20 · task-composition** — recipes/scripts call other recipes/scripts to build larger workflows
  from small ones.
- **co-21 · hermetic-builds** — a hermetic build isolates from the host so identical inputs always
  produce identical output.
- **co-22 · content-hash-caching** — Bazel/Gradle key cache entries on a hash of the inputs, reusing
  outputs on a hit.
- **co-23 · bazel-build-files** — a `BUILD` file declares targets in a package; `bazel build //pkg:tgt`
  builds one.
- **co-24 · bazel-target-patterns** — label syntax `//package:target` and patterns like `//...` select
  what to build.
- **co-25 · bazel-remote-cache** — a shared remote cache lets a team/CI reuse each other's build outputs.
- **co-26 · gradle-task-graph** — Gradle builds a DAG of tasks during configuration, before executing
  any task.
- **co-27 · gradle-incremental-build** — Gradle fingerprints inputs/outputs and marks a task `UP-TO-DATE`
  when nothing changed.
- **co-28 · gradle-build-cache** — the Gradle build cache reuses outputs across builds and machines when
  inputs match.
- **co-29 · gradle-kotlin-groovy-dsl** — build logic is written in the Groovy DSL (`.gradle`) or the
  Kotlin DSL (`.gradle.kts`).
- **co-30 · timestamp-vs-hash-freshness** — Make/POSIX decide freshness by modification time; Bazel/Gradle
  by content hash; just has no freshness model.
- **co-31 · reproducible-builds** — pinned, hermetic inputs yield byte-identical outputs — distinct from
  merely incremental.
- **co-32 · ci-integration** — CI invokes the build tool (`make ci`, `bazel test //...`, `gradle build`)
  and restores its cache.

## Worked examples

Colocated under `build-automation-and-task-runners/learning/`; each is a real `Makefile`, `justfile`,
`package.json`, `BUILD`, or `build.gradle(.kts)` run from the `make`/`just`/`npm`/`bazel`/`gradle` CLI
**or** an annotated decision artifact (DD-20/DD-30). Contiguous `ex-01..ex-80`. Every example cites the
`co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · why-build-automation** — a decision table ad-hoc shell vs an automated build (repeatable,
  documented, incremental) — verify each column's trade-off. (co-01)
- **ex-02 · runner-vs-build-system** — a decision table command runner (names recipes) vs build system
  (models a graph) — verify the distinction. (co-02)
- **ex-03 · first-makefile-rule** — a `Makefile` with one target, one prerequisite, one recipe — verify
  `make` builds the target. (co-03)
- **ex-04 · make-run-target** — `make <target>` runs the recipe — verify the target file appears. (co-03)
- **ex-05 · target-prereq-recipe** — annotate the three parts of a rule — verify each part's role. (co-03)
- **ex-06 · dependency-graph** — annotate a small DAG (`app` ← `main.o` ← `main.c`) — verify the build
  order the graph implies. (co-04)
- **ex-07 · make-default-goal** — the first target is the default goal — verify bare `make` builds it.
  (co-03)
- **ex-08 · incremental-rebuild** — touch one prerequisite, rerun `make` — verify only the dependent
  target rebuilds. (co-05)
- **ex-09 · up-to-date-skip** — rerun `make` with nothing changed — verify "Nothing to be done". (co-05)
- **ex-10 · timestamp-comparison** — annotate mtime(prereq) > mtime(target) ⇒ rebuild — verify the
  freshness rule. (co-05)
- **ex-11 · phony-clean** — a `.PHONY: clean` target removing artifacts — verify `make clean` always runs.
  (co-06)
- **ex-12 · phony-file-collision** — annotate a stray file named `test` shadowing a `test` target — verify
  `.PHONY` fixes the "up to date" bug. (co-06)
- **ex-13 · phony-aggregate** — a phony `all` depending on several targets — verify it builds each. (co-06)
- **ex-14 · autovar-target** — `$@` in a recipe — verify it expands to the target name. (co-07)
- **ex-15 · autovar-first-prereq** — `$<` in a recipe — verify it expands to the first prerequisite.
  (co-07)
- **ex-16 · autovar-all-prereqs** — `$^` in a recipe — verify it expands to all prerequisites. (co-07)
- **ex-17 · pattern-rule** — a `%.o: %.c` pattern rule — verify one rule compiles many files. (co-08)
- **ex-18 · pattern-stem-match** — annotate `%` matching a nonempty stem — verify `foo.c`→`foo.o`. (co-08)
- **ex-19 · recursive-assignment** — a recursive `=` variable referencing another — verify it expands at
  use. (co-09)
- **ex-20 · simple-assignment** — a simply-expanded `:=` variable — verify it expands once at definition.
  (co-09)
- **ex-21 · assignment-difference** — a decision table `=` vs `:=` expansion timing — verify when each
  differs. (co-09)
- **ex-22 · implicit-rule** — compile a `.c` with no explicit rule — verify Make's built-in rule fires.
  (co-10)
- **ex-23 · builtin-variables** — use `$(CC)`/`$(CFLAGS)` in a recipe — verify the built-in variables
  resolve. (co-10)
- **ex-24 · make-wildcard** — `SRCS := $(wildcard *.c)` — verify it lists the source files. (co-11)
- **ex-25 · make-patsubst** — `OBJS := $(patsubst %.c,%.o,$(SRCS))` — verify the name transform. (co-11)
- **ex-26 · first-justfile** — a `justfile` with one recipe — verify `just <recipe>` runs it. (co-14)
- **ex-27 · just-run** — `just` with no args runs the default (first) recipe — verify it executes. (co-14)

### Intermediate

- **ex-28 · just-list** — `just --list` — verify it prints the available recipes. (co-14)
- **ex-29 · just-recipe-dependency** — a recipe with a `recipe: dep` prerequisite recipe — verify the dep
  runs first. (co-14)
- **ex-30 · just-always-runs** — annotate that just recipes are all phony (always run) — verify no
  freshness skip. (co-14)
- **ex-31 · just-parameter** — a recipe with a positional parameter — verify the argument is passed.
  (co-15)
- **ex-32 · just-default-param** — a parameter with a default value — verify the default when omitted.
  (co-15)
- **ex-33 · just-variadic** — a trailing `+args` variadic parameter — verify multiple args collect.
  (co-15)
- **ex-34 · just-vs-make** — a decision table just (command runner) vs make (build system) — verify when
  to reach for each. (co-16)
- **ex-35 · npm-script** — a `"scripts": { "build": … }` + `npm run build` — verify the command runs.
  (co-17)
- **ex-36 · npm-run-list** — `npm run` with no name — verify it lists the scripts. (co-17)
- **ex-37 · npm-test-shortcut** — `npm test` runs the `test` script — verify the shortcut. (co-19)
- **ex-38 · npm-start** — `npm start` runs the `start` script — verify the lifecycle shortcut. (co-19)
- **ex-39 · npm-pre-hook** — a `prebuild` script — verify it runs before `build`. (co-18)
- **ex-40 · npm-post-hook** — a `postbuild` script — verify it runs after `build`. (co-18)
- **ex-41 · npm-pre-post-order** — annotate `pre` → main → `post` ordering — verify the sequence. (co-18)
- **ex-42 · npm-compose-scripts** — a script chaining `npm run lint && npm run test` — verify both run.
  (co-20)
- **ex-43 · make-calls-npm** — a `Makefile` target invoking `npm run build` — verify cross-tool
  composition. (co-20)
- **ex-44 · composition-graph** — annotate composed tasks forming a graph — verify the composed order.
  (co-20)
- **ex-45 · parallel-make** — `make -j4` on independent targets — verify concurrent execution. (co-12)
- **ex-46 · parallel-correctness** — annotate why accurate prerequisites make `-j` safe — verify a
  missing-dep race. (co-12)
- **ex-47 · posix-make** — a `.POSIX` first-line makefile — verify the portable-subset behavior. (co-13)
- **ex-48 · posix-portability** — annotate why `.POSIX` exists (vendor make divergence) — verify the
  opt-in marker. (co-13)
- **ex-49 · clean-rebuild** — `make clean && make` — verify a full from-scratch rebuild. (co-06)
- **ex-50 · hermetic-build** — annotate hermeticity (same inputs ⇒ same output, host-isolated) — verify
  the definition. (co-21)
- **ex-51 · non-hermetic-pitfall** — annotate a host-installed library leaking into a build — verify the
  reproducibility break. (co-21)
- **ex-52 · content-hash-cache** — annotate a hash-of-inputs cache key — verify why it beats mtime. (co-22)
- **ex-53 · cache-hit-reuse** — annotate a cache hit reusing prior outputs — verify no recompute. (co-22)
- **ex-54 · timestamp-vs-hash** — a decision table mtime vs content-hash freshness — verify each's failure
  mode. (co-30)
- **ex-55 · freshness-three-way** — annotate Make (mtime) / Bazel+Gradle (hash) / just (always) — verify
  the three models. (co-30)

### Advanced

- **ex-56 · bazel-build-file** — a `BUILD` file declaring a target — verify the target is defined. (co-23)
- **ex-57 · bazel-build-cmd** — `bazel build //path:target` — verify the single target builds. (co-23)
- **ex-58 · bazel-all-targets** — `bazel build //...` — verify all main-repo targets build. (co-24)
- **ex-59 · bazel-label-syntax** — annotate `//package:target` label syntax — verify the addressing.
  (co-24)
- **ex-60 · bazel-incremental** — rebuild after one change — verify unchanged actions are reused. (co-22)
- **ex-61 · bazel-remote-cache** — annotate a team/CI remote cache — verify shared-output reuse. (co-25)
- **ex-62 · bazel-hermetic-hash** — annotate the manifest cryptographic-hash pin of external deps — verify
  reproducibility. (co-21)
- **ex-63 · gradle-task** — a task in `build.gradle` — verify it is registered. (co-26)
- **ex-64 · gradle-task-graph** — annotate the DAG built during configuration, before execution — verify
  the pre-build graph. (co-26)
- **ex-65 · gradle-run-task** — `./gradlew build` — verify the task executes. (co-26)
- **ex-66 · gradle-up-to-date** — rerun with nothing changed — verify the `UP-TO-DATE` skip via input
  fingerprint. (co-27)
- **ex-67 · gradle-incremental-change** — change one input — verify only the affected task reruns. (co-27)
- **ex-68 · gradle-build-cache** — annotate the reuse-across-builds cache — verify a cache-restored output.
  (co-28)
- **ex-69 · gradle-groovy-dsl** — a `.gradle` Groovy DSL snippet — verify it configures the build. (co-29)
- **ex-70 · gradle-kotlin-dsl** — a `.gradle.kts` Kotlin DSL snippet — verify the typed equivalent. (co-29)
- **ex-71 · dsl-comparison** — a decision table Groovy vs Kotlin DSL — verify each's trade-off. (co-29)
- **ex-72 · reproducible-build** — annotate pinned/hermetic inputs ⇒ byte-identical output — verify
  reproducibility. (co-31)
- **ex-73 · reproducible-vs-incremental** — annotate reproducibility (same output) vs incrementality (skip
  work) — verify they are distinct. (co-31)
- **ex-74 · tool-selection** — a decision table runner vs make vs bazel/gradle by scale + language —
  verify the selection heuristic. (co-02)
- **ex-75 · monorepo-scaling** — annotate why large polyglot repos adopt Bazel/Gradle — verify the caching
  motivation. (co-24)
- **ex-76 · ci-invokes-build** — annotate CI calling `make ci` / `bazel test //...` / `gradle build` —
  verify the build tool as the CI unit. (co-32)
- **ex-77 · cache-in-ci** — annotate CI restoring the build cache between runs — verify the CI cache
  reuse. (co-28)
- **ex-78 · npm-lifecycle-install** — annotate the `install`/`prepare` lifecycle scripts — verify they
  fire on `npm install`. (co-19)
- **ex-79 · build-graph-end-to-end** — the full source → object → binary incremental loop with Make —
  verify one changed source rebuilds only its chain. (co-05)
- **ex-80 · build-automation-capstone** — a top-level `Makefile` orchestrating an `npm run build`, a
  compiled artifact, and a `just` alias, with an incremental rebuild, a phony `all`/`clean`, and `-j`
  parallelism — verify a one-file change rebuilds only the affected chain. (co-03, co-05, co-06, co-12,
  co-17, co-20)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: automate a small polyglot project end-to-end — a top-level `Makefile` that (a) delegates the
  JS/TS build to `npm run build`, (b) compiles a second artifact with a pattern rule + incremental
  timestamp rebuild, (c) aggregates both under a phony `all` and cleans with a phony `clean`, and (d)
  exposes a developer-friendly `just` alias over the same targets — proving that a one-file change
  rebuilds only the affected chain and that `-j` parallelizes independent targets.
- **Concepts exercised**: [ ] Make rules + default goal (co-03) [ ] incremental timestamp rebuild (co-05)
  [ ] phony `all`/`clean` (co-06) [ ] automatic variables + a pattern rule (co-07, co-08) [ ] `make -j`
  parallelism (co-12) [ ] a `package.json` `npm run build` target (co-17) [ ] cross-tool composition
  Make → npm + a `just` alias (co-20, co-14).
- **Ordered steps**:
  1. `.../learning/capstone/Makefile` — a default `all` phony aggregating a `js` target (`npm run build`)
     and a compiled artifact via a `%`-pattern rule using `$@`/`$<`. Verify `make` builds both and a
     rerun reports up-to-date.
  2. Touch one source file, rerun `make`. Verify only that file's chain rebuilds (the other target stays
     up-to-date).
  3. `make -j` the two independent targets. Verify they build concurrently and the result is identical.
  4. `.../learning/capstone/justfile` — a `just build`/`just clean` alias delegating to the Makefile
     targets. Verify `just build` produces the same artifacts and `make clean` removes them.
- **Acceptance criteria**: `make` builds all artifacts; a no-change rerun does no work; a single-file edit
  rebuilds only the affected chain; `-j` parallelizes independent targets; the `just` alias and `npm run
build` produce identical outputs to the Make path.
- **Done bar**: runnable end-to-end from the CLI + web-verified.

## Read more

**Books**

- **Managing Projects with GNU Make** — Robert Mecklenburg (3rd ed., 2004, O'Reilly). The standard,
  thorough treatment of GNU Make's model, rules, and idioms; released under the GNU Free Documentation
  License.
- **The GNU Make Book** — John Graham-Cumming (2015, No Starch Press). A modern, practical deep dive into
  Make's trickier corners (functions, parallelism, debugging).
- **Software Engineering at Google** — Titus Winters, Tom Manshreck, Hyrum Wright (eds.) (2020, O'Reilly).
  Its build-systems chapters articulate the artifact-based / hermetic / cached model that motivated Bazel.

**Papers & articles**

- **Build Systems à la Carte** — Andrey Mokhov, Neil Mitchell, Simon Peyton Jones (2018, ICFP). A rigorous
  taxonomy of build systems along the dependency/rebuild/scheduling axes — Make, Bazel, and others as
  points in one design space. <https://www.microsoft.com/en-us/research/publication/build-systems-la-carte/>
- **GNU Make Manual** — Free Software Foundation (ongoing). The canonical reference for rules, variables,
  functions, and parallelism. <https://www.gnu.org/software/make/manual/>
- **Bazel — Build Basics (hermeticity & artifact-based builds)** — Google / Bazel authors (ongoing). The
  official articulation of hermetic, content-hashed, cached builds. <https://bazel.build/basics>

---

← Previous: [53 · Self-Managed Kubernetes & On-Prem GitOps](./53-self-managed-kubernetes-and-gitops.md) · Next: [55 · CI/CD & Release Engineering](./55-cicd-and-release-engineering.md) →
