---
title: "Learning Overview"
date: 2026-07-31T00:00:00+07:00
draft: false
weight: 1
---

These 80 examples move from a single Make rule to a reproducible, cached build graph. Every code-bearing
example owns a runnable artifact under `learning/code/`, except the deliberately integrated final
capstone under `learning/capstone/`; run the command shown from that artifact directory. The early Make
examples use POSIX shell and local files, npm examples have no dependencies, and optional Bazel or Gradle
examples provide a local wrapper-compatible build definition.

## Concepts

- **co-01–co-13**: automation purpose, Make rules and graphs, timestamp freshness, phony targets,
  automatic variables, patterns, variables, functions, parallelism, and POSIX portability.
- **co-14–co-20**: just recipes and parameters, npm scripts and hooks, and task composition.
- **co-21–co-32**: hermeticity, content hashes, Bazel and Gradle graphs, caches, reproducibility, and
  CI invocation.

## Examples by Level

### Beginner (Examples 1–27)

- [Example 1: Choose Automation Over Repetition](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-1-choose-automation-over-repetition)
- [Example 2: Distinguish a Runner from a Build System](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-2-distinguish-a-runner-from-a-build-system)
- [Example 3: Write the First Make Rule](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-3-write-the-first-make-rule)
- [Example 4: Request a Specific Target](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-4-request-a-specific-target)
- [Example 5: Read Target, Prerequisite, and Recipe](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-5-read-target-prerequisite-and-recipe)
- [Example 6: Follow a Small Dependency Graph](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-6-follow-a-small-dependency-graph)
- [Example 7: Use the Default Goal](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-7-use-the-default-goal)
- [Example 8: Rebuild When an Input Changes](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-8-rebuild-when-an-input-changes)
- [Example 9: Observe an Up-to-Date Target](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-9-observe-an-up-to-date-target)
- [Example 10: State the Timestamp Rule](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-10-state-the-timestamp-rule)
- [Example 11: Mark a Clean Command Phony](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-11-mark-a-clean-command-phony)
- [Example 12: Avoid a File Collision](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-12-avoid-a-file-collision)
- [Example 13: Aggregate Several Artifacts](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-13-aggregate-several-artifacts)
- [Example 14: Expand the Target Name with `$@`](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-14-expand-the-target-name-with-)
- [Example 15: Expand the First Prerequisite with `$<`](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-15-expand-the-first-prerequisite-with-)
- [Example 16: Expand All Prerequisites with `$^`](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-16-expand-all-prerequisites-with-)
- [Example 17: Compile with a Pattern Rule](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-17-compile-with-a-pattern-rule)
- [Example 18: Match a Pattern Stem](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-18-match-a-pattern-stem)
- [Example 19: Defer Expansion with `=`](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-19-defer-expansion-with-)
- [Example 20: Expand Once with `:=`](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-20-expand-once-with-)
- [Example 21: Choose Assignment Timing](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-21-choose-assignment-timing)
- [Example 22: Use Make's Built-In C Rule](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-22-use-makes-built-in-c-rule)
- [Example 23: Use `CC` and `CFLAGS`](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-23-use-cc-and-cflags)
- [Example 24: Discover Source Files with `wildcard`](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-24-discover-source-files-with-wildcard)
- [Example 25: Transform Names with `patsubst`](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-25-transform-names-with-patsubst)
- [Example 26: Write a First `justfile`](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-26-write-a-first-justfile)
- [Example 27: Run the Default `just` Recipe](/en/learn/courses/build-automation-and-task-runners/learning/beginner#example-27-run-the-default-just-recipe)

### Intermediate (Examples 28–55)

- [Example 28: List Available just Recipes](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-28-list-available-just-recipes)
- [Example 29: Depend on Another just Recipe](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-29-depend-on-another-just-recipe)
- [Example 30: Recognize That just Always Runs](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-30-recognize-that-just-always-runs)
- [Example 31: Pass a Positional just Parameter](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-31-pass-a-positional-just-parameter)
- [Example 32: Supply a Default just Parameter](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-32-supply-a-default-just-parameter)
- [Example 33: Collect a Variadic just Parameter](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-33-collect-a-variadic-just-parameter)
- [Example 34: Choose just or Make](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-34-choose-just-or-make)
- [Example 35: Run an npm Script](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-35-run-an-npm-script)
- [Example 36: List npm Scripts](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-36-list-npm-scripts)
- [Example 37: Use the npm test Shortcut](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-37-use-the-npm-test-shortcut)
- [Example 38: Use the npm start Shortcut](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-38-use-the-npm-start-shortcut)
- [Example 39: Run an npm prebuild Hook](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-39-run-an-npm-prebuild-hook)
- [Example 40: Run an npm postbuild Hook](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-40-run-an-npm-postbuild-hook)
- [Example 41: State the Full npm Hook Order](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-41-state-the-full-npm-hook-order)
- [Example 42: Compose npm Scripts](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-42-compose-npm-scripts)
- [Example 43: Let Make Delegate to npm](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-43-let-make-delegate-to-npm)
- [Example 44: Inspect a Composed Task Graph](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-44-inspect-a-composed-task-graph)
- [Example 45: Run Independent Make Targets in Parallel](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-45-run-independent-make-targets-in-parallel)
- [Example 46: Recognize a Parallel Race](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-46-recognize-a-parallel-race)
- [Example 47: Select POSIX Make Behavior](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-47-select-posix-make-behavior)
- [Example 48: Explain POSIX Portability](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-48-explain-posix-portability)
- [Example 49: Clean and Rebuild](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-49-clean-and-rebuild)
- [Example 50: Define a Hermetic Build](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-50-define-a-hermetic-build)
- [Example 51: Find a Non-Hermetic Pitfall](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-51-find-a-non-hermetic-pitfall)
- [Example 52: Model a Content-Hash Cache](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-52-model-a-content-hash-cache)
- [Example 53: Reuse a Cache Hit](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-53-reuse-a-cache-hit)
- [Example 54: Compare Timestamp and Hash Freshness](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-54-compare-timestamp-and-hash-freshness)
- [Example 55: Compare Three Freshness Policies](/en/learn/courses/build-automation-and-task-runners/learning/intermediate#example-55-compare-three-freshness-policies)

### Advanced (Examples 56–80)

- [Example 56: Declare a Bazel Build Target](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-56-declare-a-bazel-build-target)
- [Example 57: Build One Bazel Target](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-57-build-one-bazel-target)
- [Example 58: Select All Main-Repository Bazel Targets](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-58-select-all-main-repository-bazel-targets)
- [Example 59: Read Bazel Label Syntax](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-59-read-bazel-label-syntax)
- [Example 60: Understand Bazel Incrementality](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-60-understand-bazel-incrementality)
- [Example 61: Describe a Bazel Remote Cache](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-61-describe-a-bazel-remote-cache)
- [Example 62: Pin a Bazel External Dependency](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-62-pin-a-bazel-external-dependency)
- [Example 63: Register a Gradle Task](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-63-register-a-gradle-task)
- [Example 64: Observe Gradle's Task Graph Phase](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-64-observe-gradles-task-graph-phase)
- [Example 65: Run a Gradle Build Task](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-65-run-a-gradle-build-task)
- [Example 66: Observe a Gradle Up-to-Date Task](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-66-observe-a-gradle-up-to-date-task)
- [Example 67: Rerun an Affected Gradle Task](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-67-rerun-an-affected-gradle-task)
- [Example 68: Enable a Gradle Build Cache](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-68-enable-a-gradle-build-cache)
- [Example 69: Use the Gradle Groovy DSL](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-69-use-the-gradle-groovy-dsl)
- [Example 70: Use the Gradle Kotlin DSL](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-70-use-the-gradle-kotlin-dsl)
- [Example 71: Compare the Gradle DSLs](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-71-compare-the-gradle-dsls)
- [Example 72: Define a Reproducible Build](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-72-define-a-reproducible-build)
- [Example 73: Separate Reproducibility from Incrementality](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-73-separate-reproducibility-from-incrementality)
- [Example 74: Choose a Build Tool by Need](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-74-choose-a-build-tool-by-need)
- [Example 75: Explain Monorepo Build Scaling](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-75-explain-monorepo-build-scaling)
- [Example 76: Invoke a Build Tool from CI](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-76-invoke-a-build-tool-from-ci)
- [Example 77: Restore a Cache in CI](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-77-restore-a-cache-in-ci)
- [Example 78: Recognize the npm Install Lifecycle](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-78-recognize-the-npm-install-lifecycle)
- [Example 79: Build a Complete Incremental Make Graph](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-79-build-a-complete-incremental-make-graph)
- [Example 80: Assemble the Build-Automation Capstone](/en/learn/courses/build-automation-and-task-runners/learning/advanced#example-80-assemble-the-build-automation-capstone)

### Capstone

- [Build automation capstone](/en/learn/courses/build-automation-and-task-runners/learning/capstone)
