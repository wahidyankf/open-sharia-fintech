---
description: "Defines the purpose of by-example tutorials and how their structure adapts and inherits from the general Tutorial Convention."
when_to_use: "Read first when you need to understand why by-example tutorials exist and how their structure maps onto the general tutorial structure."
---

# Purpose and Structure Integration with General Tutorial Standards

## Purpose

This convention **extends the [Tutorials Convention](../general.md) for the By Example tutorial type**, defining specialized standards for code-first learning through 75-85 heavily annotated, self-contained, runnable examples achieving 95% coverage.

**Base requirements**: By-example tutorials inherit general tutorial standards (learning-oriented approach, visual completeness, hands-on elements from [Tutorials Convention](../general.md)) and add code-specific specializations defined below.

**Target audience**: Experienced developers (seasonal programmers, software engineers) switching languages or frameworks who prefer learning through working code rather than narrative explanations.

## Structure Integration with General Tutorial Standards

By-example tutorials adapt the general [Tutorial Convention](../general.md) structure for code-first learning:

### Adaptation of General Structure

**Traditional Tutorial Structure** (from [Tutorials Convention](../general.md)):

- Introduction → Prerequisites → Objectives → Content Sections → Challenges → Summary → Next Steps

**By-Example Structure Adaptation**:

1. **overview.md** (serves as introduction):
   - Hook and motivation (why this language/framework matters)
   - Prerequisites (required programming experience level)
   - Learning approach explanation (code-first via 75-85 examples)
   - Comparison to by-concept path (narrative-driven alternative)
   - Links to by-concept tutorials for those preferring comprehensive explanations

2. **beginner.md / intermediate.md / advanced.md** (replace traditional content sections):
   - Contains 75-85 annotated examples across three complexity levels
   - Each example is self-contained and runnable (not sequential sections)
   - Examples progress from fundamental syntax (beginner) to expert mastery (advanced)
   - Coverage: beginner (0-40%), intermediate (40-75%), advanced (75-95%)

3. **Hands-on elements integrated into examples**:
   - No separate "Challenges" section - each example IS a hands-on exercise
   - Self-contained code means learners can copy, run, and modify immediately
   - Educational annotations guide experimentation

4. **Summary and next steps** (included in overview.md or advanced.md):
   - Links to by-concept path for deeper narrative explanations
   - Links to related frameworks/tools
   - Production application guidance
