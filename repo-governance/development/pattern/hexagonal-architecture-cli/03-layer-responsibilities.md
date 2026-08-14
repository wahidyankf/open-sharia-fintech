---
title: "Layer Responsibilities"
description: "What each CLI layer is responsible for - commands/ as inbound adapter, domain/, application/, and infrastructure/."
category: explanation
subcategory: development
tags:
  - architecture
  - hexagonal
  - cli
  - rust
  - fsharp
created: 2026-05-26
when_to_use: "Use when deciding which CLI layer a piece of code belongs in."
---

# Layer Responsibilities

## commands/ — Inbound Adapter

- Parse CLI arguments using Clap (`#[derive(Parser)]`) or Cobra
- Validate argument types and required/optional constraints
- Map parsed arguments to application-layer input types
- Translate application errors to human-readable messages and non-zero exit codes
- Print progress or results to stdout/stderr

## domain/ — Domain Layer

- Business entities and value objects relevant to the CLI's domain
- Pure validation and transformation functions
- Domain error types (no exit codes, no `fmt.Println`)

## application/ — Application Layer

- Use-case functions that orchestrate domain objects and call outbound ports
- Outbound port definitions (repository traits in Rust, interfaces in Go)
- Application-level error types

## infrastructure/ — Outbound Adapters

- File system access (reading input files, writing output files)
- HTTP client calls to external services
- Concrete port implementations
