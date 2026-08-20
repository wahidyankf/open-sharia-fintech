---
title: "Tutorial Conventions"
description: Standards for creating learning-oriented tutorial content
when_to_use: Use when authoring, reviewing, or scoping any tutorial content and need to find the convention for its type (by-concept, by-example, cookbook, in-the-field, etc.).
category: explanation
tags:
  - index
  - conventions
  - tutorials
  - education
created: 2026-01-30
---

# Tutorial Conventions

Use these conventions when you are helping someone learn, rather than merely listing facts. They answer: **"How can a reader make steady progress without needing hidden context?"**

## Purpose

This directory contains standards for tutorial creation, structure, naming, and content that apply to **all tutorial content** across the repository (docs/, ayokoding-www, ose-www, anywhere). These conventions **build upon and extend** the universal [writing conventions](../writing/README.md).

## Documents

### Core Tutorial Standards

- [Tutorial Convention](./general.md) — Standards for creating learning-oriented tutorials in open-sharia-enterprise. Use when authoring, reviewing, or scoping any tutorial, or when a type-specific tutorial convention needs the base standards it extends.
- [Tutorial Naming Convention](./naming.md) — Standardized tutorial naming and depth levels for consistent learning experiences. Use when naming, scoping, or choosing the type of a new tutorial anywhere in the repository.

### Tutorial Types

- [By-Concept Tutorial Convention](./by-concept.md) — Standards for creating concept-driven tutorials with 95% coverage, heavily annotated code, and rich diagrams. Use when authoring, reviewing, or scoping a By-Concept (narrative-driven) tutorial for any language or framework.
- [By-Example Tutorial Convention](./swe-by-example.md) — Standards for creating code-first by-example tutorials with 95% coverage, self-contained examples, and educational annotations. Read before creating or reviewing SWE by-example tutorial content (code-first, 75-85 annotated examples) for any programming language or framework.
- [Security By-Example Tutorial Convention](./security-by-example.md) — Standards for security-domain by-example tutorials using tool output, lab scenarios, and annotated security artifacts — extends the SWE By-Example Convention. Use when authoring, reviewing, or scoping a security-domain by-example tutorial (Foundations, Red Team, or Blue Team) and need the security-specific adaptations of the SWE By-Example convention.
- [Scenario By-Example Tutorial Convention](./scenario-by-example.md) — Standards for scenario-domain by-example tutorials using annotated documents, decisions, and governance artifacts — extends the SWE By-Example Convention for any non-code domain. Use when writing or reviewing a non-code, scenario-driven by-example tutorial (security governance, ADRs, legal/compliance, risk) and you need the standard this content must follow.
- [Cookbook Tutorial Convention](./cookbook.md) — Standards for creating problem-focused cookbook tutorials with practical, copy-paste ready recipes organized by problem type. Use when authoring, reviewing, or scoping a Cookbook (problem-focused recipe) tutorial for any language or framework.
- [In-the-Field Tutorial Convention](./in-the-field.md) — Standards for creating production-ready implementation guides building on by-example/by-concept foundations with frameworks, libraries, and enterprise patterns. Use when writing, reviewing, or validating an In-the-Field production implementation guide.

### Programming Language Tutorials

- [Programming Language Content Standard](./programming-language-content.md) — Universal content architecture for programming language education on ayokoding-www with mandatory structure, coverage model, and quality benchmarks. Use before creating or reviewing any programming language tutorial content on ayokoding-www, to confirm the mandatory Full Set Tutorial Package structure, coverage levels, and quality benchmarks it must follow.
- [Programming Language Tutorial Structure Convention](./programming-language-structure.md) — Dual-path tutorial organization pattern for programming language education with by-concept and by-example learning tracks. Use when creating, auditing, or restructuring a programming language's Full Set Tutorial Package directory structure on ayokoding-www.

## Full Set Tutorial Package

The Full Set Tutorial Package consists of 5 mandatory components:

1. **Foundational Tutorials** (Initial Setup, Quick Start) - Getting started content
2. **By Example Track** (Component 3 - PRIORITY) - Code-first, 75-85 examples, "move fast"
3. **By Concept Track** (Component 4) - Narrative-driven, "learn deep"
4. **Cookbook** (Component 5) - Practical recipes, problem-focused
5. **In-the-Field Track** - Production-ready implementations with frameworks and enterprise patterns

## Related Documentation

- [Writing Conventions](../writing/README.md) — Universal content quality standards (foundation)
- [Structure Conventions](../structure/README.md) — File organization and Diataxis framework
- [How to Add a Programming Language](../../../docs/how-to/add-programming-language.md) — Step-by-step guide

## Principles Implemented/Respected

This set of conventions implements/respects the following core principles:

- **[Documentation First](../../principles/content/documentation-first.md)**: Tutorial conventions mandate structured learning content as a primary deliverable. The Full Set Tutorial Package architecture ensures systematic documentation of all facets of a programming language or topic rather than ad-hoc, incomplete coverage.

- **[Progressive Disclosure](../../principles/content/progressive-disclosure.md)**: The five-component Full Set Tutorial Package follows a deliberate progression from foundational (Initial Setup, Quick Start) through increasing depth (By Example, By Concept, Cookbook). Learners access complexity at their own pace following a structured path.

- **[Accessibility First](../../principles/content/accessibility-first.md)**: By Example tutorials require self-contained, runnable examples that work without additional setup, lowering barriers to entry. Hands-on learning elements (required in all tutorial types) ensure content is accessible to different learning styles, not only theoretical readers.

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: By Example track is prioritized (Component 3 - PRIORITY) because code-first, annotated examples deliver maximum learning value with minimum cognitive overhead. The five-component package structure provides a complete, non-overlapping taxonomy of tutorial types.
