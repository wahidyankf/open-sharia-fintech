---
title: Hexagonal Architecture — CLI Apps
description: Hexagonal architecture specialization for CLI apps — commands as inbound adapters, layer responsibilities, and forbidden imports
category: explanation
subcategory: development
tags:
  - architecture
  - hexagonal
  - cli
  - rust
  - fsharp
created: 2026-05-26
when_to_use: "Use when structuring a CLI app's commands/, domain/, application/, or infrastructure/ layer."
---

# Hexagonal Architecture — CLI Apps

CLI apps apply hexagonal architecture with the `commands/` directory acting as the inbound adapter. CLI
argument parsing libraries (Clap, Cobra) belong exclusively in that adapter layer; the domain and
application layers know nothing about flags, subcommands, or exit codes.

## Contents

- [Principles and Conventions](./hexagonal-architecture-cli/principles-and-conventions.md) — The core principles and conventions this pattern implements - explicitness, pure functions, simplicity, and functional programming. Use when you need to trace a CLI hexagonal-architecture rule back to the principle or convention it implements.
- [Overview and Directory Layout](./hexagonal-architecture-cli/overview-and-directory-layout.md) — How CLI argument parsing maps to the inbound adapter, plus the canonical directory layout across all four CLI apps. Use when scaffolding a new CLI app or command and need the canonical directory layout.
- [Layer Responsibilities](./hexagonal-architecture-cli/layer-responsibilities.md) — What each CLI layer is responsible for - commands/ as inbound adapter, domain/, application/, and infrastructure/. Use when deciding which CLI layer a piece of code belongs in.
- [Forbidden Imports, Examples, and Related](./hexagonal-architecture-cli/forbidden-imports-examples-and-related.md) — The forbidden-imports table, a worked Rust example of a command delegating to the application layer, and related pattern documentation. Use when checking whether a CLI layer imports something forbidden, or want a worked example of the commands/ to application/ handoff.
