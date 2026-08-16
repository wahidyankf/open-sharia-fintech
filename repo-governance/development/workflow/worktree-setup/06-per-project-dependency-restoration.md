---
title: "Per-Project Dependency Restoration for Some Language Ecosystems"
description: The doctor --fix gap for Elixir and F# polyglot-demo projects, which need an explicit mix deps.get / dotnet restore step the toolchain-level fix does not cover.
category: explanation
subcategory: development
tags:
  - development
  - git
  - worktree
  - npm
  - nx
  - dependencies
  - toolchain
  - doctor
created: 2026-03-28
when_to_use: Use when `nx affected -t test:quick` fails on an Elixir or F# polyglot-demo project with a missing-dependency error right after provisioning a worktree.
---

# Per-Project Dependency Restoration for Some Language Ecosystems

Two further gaps have surfaced in practice that the two-step init above does not cover. Both are
one-time, worktree-local, and require no source or config changes — but agents should account for
them explicitly rather than rediscover them mid-task.

`npm run doctor -- --fix` converges the _toolchain_ (the `mix`, `dotnet`, `cargo`, etc. CLIs
themselves) but does not run _per-project_ dependency restoration for every polyglot project in
the workspace. Most language ecosystems restore dependencies automatically as a side effect of
their own build/test/typecheck invocation (Rust's `cargo`, TypeScript's package-manager-driven Nx
executors, Go's module cache, Python's `uv`/`pip`), so this gap is invisible for them. Two
ecosystems do NOT auto-restore and need an explicit one-time step in a freshly provisioned
worktree — this surfaced concretely in a polyglot demo-app fan-out (`ose-public`
itself currently has no Elixir projects; its own F# apps, e.g. `ose-be`/`organiclever-be`, use
per-domain names rather than the `*-fsharp-*` demo-app naming below and are unaffected by this
specific glob):

```bash
# Elixir projects — run once per affected libs/apps/*-elixir-* project
mix deps.get

# F#/.NET polyglot-demo projects — run once per affected apps/*-fsharp-*/src and .../tests project
dotnet restore
```

Symptom without this step: `nx affected -t test:quick` fails on
Elixir projects with `Unchecked dependencies ... run "mix deps.get"`, or on F# projects with
`NETSDK1004: Assets file ... not found. Run a NuGet package restore`, even though the toolchain
itself (`mix`, `dotnet`) is correctly installed. Root-cause the failure to this gap before
assuming a real regression — it reproduces on every freshly provisioned worktree that touches an
Elixir or F# polyglot-demo project, not just once. In a repo with no such projects in scope
(`ose-public`, until it gains one), this section is a no-op to skip past, not a step to run
blindly.
