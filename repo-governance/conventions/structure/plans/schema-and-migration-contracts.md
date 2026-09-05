---
title: "Schema and Migration Contracts"
description: Defines the data-model, compatibility, migration, recovery, and proof required for schema-changing plans.
category: explanation
subcategory: conventions
tags: [conventions, plans, schema, migrations]
created: 2026-08-30
when_to_use: Use when a formal plan adds, removes, renames, retypes, or reinterprets persisted data.
---

# Schema and Migration Contracts

## Purpose

Schema names and DDL types do not explain data ownership, meaning, transition behaviour, or recovery.
A schema-changing plan must make the resulting contract and safe migration executable.

## Standards

- Include a relational ERD or storage-appropriate data-model diagram showing affected entities,
  keys, and relationships.
- State the exact old and new contracts. Add a field-by-field guide covering purpose, owner,
  type/constraints, default and nullability, sensitivity, readers/writers, lifecycle and retention,
  clearing behaviour, and recovery implications where applicable.
- Define compatibility boundaries for mixed-version readers, writers, APIs, jobs, and deployments.
- Use `expand → migrate → verify → contract`, or explain why a step is inapplicable without
  weakening compatibility or data safety.
- Specify rollback triggers and procedure, migration observability, reconciliation checks, and
  evidence that proves no loss, duplication, or unintended reinterpretation.

## Examples

A column rename identifies the dual-read/dual-write interval, backfill batching and retry behaviour,
old/new API fields, row-count and value reconciliation, rollback trigger, and the evidence required
before dropping the old column.

## Validation

Semantic plan review fails a schema-changing plan when implementation must infer field meaning,
transition order, compatibility, verification, or recovery.
