---
description: "Standard 1: cap discovery (GIT_CEILING_DIRECTORIES)."
when_to_use: "Use when implementing capped git-discovery in a fixture."
---

# The Rule: Six Mandatory Layers (Standard 1)

Every test or fixture in scope (see [Scope](./scope.md) above) MUST implement **all six** of the
following layers. None of the six is optional, and none substitutes for another -- each closes a
distinct escape mechanism (see [Why Defense-in-Depth](./why-defense-in-depth-not-a-single-assertion.md)
below for the mapping).

## Standard 1: Cap Discovery (`GIT_CEILING_DIRECTORIES`)

Set `GIT_CEILING_DIRECTORIES` to the fixture's temp root so `git` never searches for a `.git`
directory above it, no matter what else goes wrong.

```rust
cmd.env("GIT_CEILING_DIRECTORIES", tempdir.path());
```

**Why**: `git`'s default repository discovery walks upward from the working directory until it
finds a `.git`. If a fixture's temp directory itself lacks a `.git` at the moment a command runs
(a race during setup, an `init` that has not completed, a `TMPDIR` misconfiguration placing the
temp root under the real repository), discovery keeps walking upward -- potentially all the way to
the real repository. Capping the ceiling makes that upward walk terminate at the fixture's own
root, with no repository found beyond it, rather than continuing until it finds one.
