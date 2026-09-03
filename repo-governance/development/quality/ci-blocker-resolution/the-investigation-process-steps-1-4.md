---
title: "The Investigation Process (Steps 1-4)"
description: "Steps 1-4: read the error, blast radius, reproduce, trace to root cause."
category: explanation
subcategory: development
tags:
  - ci
  - quality-gates
  - root-cause
  - debugging
  - anti-pattern
  - preexisting-issues
created: 2026-04-04
when_to_use: "Use when starting to investigate a CI blocker."
---

# The Investigation Process (Steps 1-4)

## Step 1: Read the Error

Read the full error output. Not just the summary line -- the full stack trace, the full lint output, the full test failure message. The root cause is in the details.

## Step 2: Identify the Blast Radius

Determine which projects are affected:

```bash
# See which projects are affected by your changes (test:quick internally chains
# typecheck -> lint -> test:unit -> test:coverage -> test:specs; see Nx Target Standards)
npx nx affected -t test:quick --dry-run
```

If a project you did not modify is failing, it is a preexisting issue. Your changes did not cause it, but you are responsible for fixing it because you discovered it.

## Step 3: Reproduce the Failure

Reproduce the failure in isolation to confirm it is preexisting:

```bash
# Run the specific failing target for the specific project
npx nx run <project>:typecheck
npx nx run <project>:lint
npx nx run <project>:test:quick
npx nx run <project>:specs:behavior:coverage
```

## Step 4: Trace to Root Cause

Common root causes of preexisting CI failures:

| Symptom                                      | Common Root Cause                                                                                                                                                                                                                                          |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Type errors in a project you did not touch   | A shared library changed its types without updating consumers                                                                                                                                                                                              |
| Lint errors in generated code                | The codegen target needs to run before lint                                                                                                                                                                                                                |
| Test failures with stale snapshots           | Snapshots need updating after a dependency upgrade                                                                                                                                                                                                         |
| Import resolution failures                   | A dependency was added to one project but not another                                                                                                                                                                                                      |
| Coverage threshold failure                   | A recent commit removed tests without replacing them                                                                                                                                                                                                       |
| Spec-coverage failure                        | A command was added without a corresponding Gherkin scenario                                                                                                                                                                                               |
| F# analyzer/lint passes locally, fails in CI | Local `obj/` predates a newly added `.fs` file (or a cached/skipped `typecheck`), so the design-time compile list silently excludes it -- `dotnet build` before trusting a local `lint` pass; CI is the sole authority for G-Research analyzer diagnostics |
