---
title: "Principles and Command Mapping"
description: Core principles and the Acceptance Criteria convention this mapping builds on, plus the mandatory Clap-subcommand-to-Gherkin-tag rule and the domain-prefixed subcommand pattern.
category: explanation
subcategory: development
tags:
  - bdd
  - gherkin
  - specs:coverage
created: 2026-03-06
when_to_use: Use when confirming which principles and conventions this mapping convention builds on, or checking the core command-to-tag mapping rule before adding a new CLI command.
---

# Principles and Command Mapping

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Every command's behavior is explicitly specified in Gherkin before implementation. No undocumented commands.

- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**: `rhino-cli specs coverage` automatically enforces the mapping at file, scenario, and step levels.

- **[Documentation First](../../../principles/content/documentation-first.md)**: Specs are written alongside or before the command implementation, serving as living documentation.

## Conventions Implemented/Respected

- **[Acceptance Criteria Convention](../acceptance-criteria.md)**: Feature files follow Gherkin standards defined there, including the **step-keyword cardinality HARD rule** — every `Scenario` uses exactly one primary `Given`, one `When`, and one `Then`; additional steps chain with `And`/`But`. `Background` blocks and `Scenario Outline` `Examples` tables are exempt.

## CLI Apps: Command-to-Spec Mapping

### Core Rule

**Every Clap subcommand file must have a corresponding `@tag` in a Gherkin feature file under `specs/`.**

Infrastructure files (`main.rs`, `helpers.rs`) and parent command files (e.g., `agents.rs`, `docs.rs`) that do not implement logic are exempt.

## Domain-Prefixed Subcommands

All CLI apps in this monorepo use **Clap subcommands** grouped by domain. The domain is the prefix in every artifact:

```
rhino-cli {domain} {action}
crane-cli {domain} {action}
```
