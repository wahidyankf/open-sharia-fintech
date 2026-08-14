---
title: "Factual Validation Convention — Overview"
description: What factual validation is, why it matters (with and without it), and which content types across the repository it applies to.
when_to_use: Use when introducing someone to what factual validation means in this repository, or checking which content type's validation focus applies to a document you're reviewing.
category: explanation
subcategory: conventions
tags:
  - factual-validation
  - verification
  - web-research
  - accuracy
  - quality-assurance
created: 2025-12-16
---

# Overview

## What is Factual Validation?

Factual validation is the systematic process of verifying technical claims, commands, code examples, and references against authoritative sources using web-based research tools (WebSearch and WebFetch).

**Core Activities:**

- Verifying command syntax and options against official documentation
- Checking software versions are current or marked as historical
- Validating API usage matches current implementations
- Confirming external references are accessible and accurate
- Detecting contradictions within and across documents
- Identifying outdated information using web research

## Why This Matters

**Without factual validation:**

- FAIL: Readers follow incorrect commands that don't work
- FAIL: Tutorials reference deprecated APIs causing confusion
- FAIL: Documentation contradicts itself creating trust issues
- FAIL: Outdated version numbers mislead about compatibility
- FAIL: Broken links frustrate users seeking additional information

**With factual validation:**

- PASS: All technical claims verified against authoritative sources
- PASS: Commands and code examples guaranteed to work
- PASS: Version information current and accurate
- PASS: Contradictions detected and resolved
- PASS: External references validated for accessibility

## Scope

This convention applies to **all content types** across the repository:

| Content Type                | Validation Focus                                                    |
| --------------------------- | ------------------------------------------------------------------- |
| **Documentation** (`docs/`) | Technical accuracy, command syntax, code examples, version numbers  |
| **App Content** (`apps/`)   | Educational accuracy, tutorial code, bilingual consistency          |
| **Plans** (`plans/`)        | Technology choices, codebase assumptions, documentation URLs        |
| **README Files**            | Installation instructions, version requirements, feature claims     |
| **Convention Documents**    | Referenced standards, tool capabilities, specification URLs         |
| **Agent Definitions**       | Tool permissions, model capabilities, reference documentation links |
