---
description: "Defines the two parallel-track coverage levels: the recipe-based Cookbook and the code-first By Example track for experienced developers."
when_to_use: "Use when writing or reviewing a language's Cookbook or By Example content, or deciding whether new content belongs in one of these parallel tracks."
---

# Coverage Levels: Cookbook and By-Example Tracks

## Cookbook (Parallel Track)

**Goal:** Provide copy-paste-ready solutions for common problems.

**Structure:** 30-40 recipes organized by category

- Each recipe: Problem → Solution → How It Works → Use Cases
- Runnable code with minimal dependencies
- Cross-references to relevant tutorials

**Mandatory categories:**

- Data structures and algorithms
- Concurrency patterns
- Error handling recipes
- Design patterns implementations
- Web development patterns
- Database patterns
- Testing patterns
- Performance optimization

**Success criteria:** Learner can solve common problems quickly.

## By Example (Parallel Track)

**Goal:** Quick language pickup for experienced developers through annotated code examples.

**Structure:** 60+ examples organized into 3 level-based files

- **beginner.md**: Examples 1-15 (Basics) - fundamental syntax, variables, control flow, functions
- **intermediate.md**: Examples 16-35 (Intermediate) - data structures, OOP/functional patterns, error handling, modules
- **advanced.md**: Examples 36-60 (Advanced) - concurrency, metaprogramming, internals, optimization

**Format per example:**

1. **Concept Name and Brief Explanation** (2-3 sentences)
2. **Mermaid Diagram** (when helpful for concept relationships)
3. **Heavily Commented Code:**
   - What each line does
   - Expected output (as comments)
   - Intermediate values for variables/processes
4. **Key Takeaway** (1-2 sentences summarizing the concept)

**Mandatory coverage areas:**

- Core syntax (variables, types, operators)
- Control flow (conditionals, loops, pattern matching)
- Functions and methods
- Data structures (arrays, lists, maps, sets, structs/classes)
- Error handling patterns
- Modules and packages
- Testing basics
- Concurrency primitives
- Common standard library patterns
- Language-specific features (e.g., Go channels, Python comprehensions, Rust ownership)

**Success criteria:** Experienced developer can read language code fluently and write basic programs after studying all 60+ examples.

**Target audience:** Experienced developers (seasonal programmers or software engineers) who:

- Already know at least one programming language well
- Want to quickly pick up a new language without extensive narrative
- Prefer learning through working code examples
- Need 90% language coverage efficiently

**Relationship to other tutorials:**

- **NOT a replacement** for Beginner tutorial (which provides deep explanations for complete beginners)
- **NOT a replacement** for Quick Start (which is 5-30% coverage touchpoints)
- **NOT a replacement** for Cookbook (which is problem-solving oriented, not learning-oriented)
- **Complements** the Full Set by providing an alternative learning path for experienced developers
