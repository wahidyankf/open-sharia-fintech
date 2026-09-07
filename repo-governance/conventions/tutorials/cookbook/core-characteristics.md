---
description: "Defines the problem-focused approach, coverage domains, recipe independence, and cross-level applicability that characterize Cookbook tutorials."
when_to_use: "Read when scoping what problem domains a cookbook should cover and confirming a recipe is independent and cross-level."
---

# Core Characteristics

## 1. Problem-Focused Approach

**Philosophy**: Organize by "what problem does this solve" not "what topic does this teach".

Recipes prioritize:

- Specific problem statements over broad topics
- Working solutions over educational explanations
- Practical utility over theoretical completeness
- Copy-paste readiness over step-by-step guidance

## 2. Coverage Target: Practical Problem Domains

**What "30+ recipes" means**: Breadth across common problem categories developers encounter in production.

**Problem categories to cover**:

- **Setup and Configuration** - Environment setup, tool configuration, dependency management
- **Data Manipulation** - Parsing, transforming, validating, serializing data
- **File Operations** - Reading, writing, processing files (CSV, JSON, XML, etc.)
- **Network and HTTP** - API calls, request handling, error handling, authentication
- **Concurrency and Parallelism** - Async operations, threading, race conditions
- **Testing and Debugging** - Test setup, mocking, debugging techniques
- **Performance Optimization** - Profiling, caching, optimization patterns
- **Error Handling** - Exception patterns, error recovery, logging
- **Security** - Input validation, authentication, authorization patterns
- **Database Operations** - CRUD operations, transactions, query optimization

**Not included** (covered elsewhere):

- Comprehensive language features (that's by-concept)
- Sequential learning examples (that's by-example)
- Project-specific implementations (that's how-to guides)

## 3. Recipe Independence

**What independence means**: Each recipe can be understood and used without reading other recipes.

**Self-containment rules**:

- Recipe includes all necessary imports/dependencies
- Problem context is stated clearly upfront
- No assumptions about prior recipe reading
- Cross-references are optional, not required

**Different from by-example**:

- By-example: Sequential examples building on each other (1→85)
- Cookbook: Independent recipes in any order

## 4. Cross-Level Applicability

**What cross-level means**: Same recipe useful regardless of developer skill level.

A beginner might use a recipe to solve an immediate problem.
An intermediate developer might study the recipe to understand the pattern.
An advanced developer might reference the recipe for syntax or edge cases.

**Different from by-concept**:

- By-concept: Separate beginner/intermediate/advanced files
- Cookbook: Single recipe serves all levels (problem is the organizing principle)
