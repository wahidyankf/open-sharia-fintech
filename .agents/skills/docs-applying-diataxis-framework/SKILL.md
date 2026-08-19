---
name: docs-applying-diataxis-framework
description: Diátaxis documentation framework for organizing content into four categories - tutorials (learning-oriented), how-to guides (problem-solving), reference (technical specifications), and explanation (conceptual understanding). Essential for creating and organizing documentation in docs/ directory.
---

# Applying Diátaxis Framework

## Purpose

This Skill provides guidance for applying the **Diátaxis documentation framework** to organize and create documentation. Diátaxis categorizes documentation into four distinct types based on user needs and context.

**When to use this Skill:**

- Creating new documentation in docs/
- Organizing documentation structure
- Deciding which documentation type to write
- Reviewing documentation for proper categorization
- Understanding documentation organization principles

## The Four Documentation Types

### Tutorials (Learning-Oriented)

**Purpose**: Guide learners through a complete journey to achieve a specific learning outcome.

**Characteristics**:

- Learning-oriented (not task-oriented)
- Hands-on, practical examples
- Gradual progression from simple to complex
- Safety and encouragement for beginners
- Minimal assumptions about prior knowledge

**Directory**: `docs/tutorials/`

**Example**: "Data Tutorial - Beginner" teaching fundamentals step-by-step.

### How-To Guides (Problem-Solving)

**Purpose**: Provide step-by-step instructions to solve specific problems or complete specific tasks.

**Characteristics**:

- Goal-oriented and task-focused
- Assumes basic knowledge
- Practical, actionable steps
- Specific to one problem/task
- Flexible order (can jump to relevant guide)

**Directory**: `docs/how-to/`

**Example**: "How to Add a New Nx App" - concrete steps for a specific task.

### Reference (Technical Specifications)

**Purpose**: Provide factual, accurate technical information for lookup.

**Characteristics**:

- Information-oriented
- Accurate, comprehensive technical details
- Consistent structure
- Minimal narrative
- Lookup-friendly organization

**Directory**: `docs/reference/`

**Example**: "Monorepo Structure Reference" - technical specifications.

### Explanation (Conceptual Understanding)

**Purpose**: Explain concepts, design decisions, principles, and context.

**Characteristics**:

- Understanding-oriented
- Conceptual, not procedural
- Provides context and rationale
- Explores alternatives and trade-offs
- Discusses WHY, not just HOW

**Directory**: `docs/explanation/`

**Example**: "Repository Governance Architecture" - explains six-layer system concept.

## Quick Decision Matrix

| User Wants To...          | Documentation Type | Directory         |
| ------------------------- | ------------------ | ----------------- |
| Learn a skill             | Tutorial           | docs/tutorials/   |
| Solve a specific problem  | How-To             | docs/how-to/      |
| Look up technical details | Reference          | docs/reference/   |
| Understand concepts/WHY   | Explanation        | docs/explanation/ |

## Organizing docs/explanation/

The explanation directory has special subdirectories:

- **vision/** - Foundational purpose (WHY we exist, WHAT change we seek)
- **principles/** - Foundational values and core principles
- **conventions/** - Documentation standards and rules
- **development/** - Software development practices
- **workflows/** - Multi-step orchestrated processes

## Reference Modules

- [Common Mistakes and Content Type Guidelines](./reference/common-mistakes-and-content-guidelines.md) — 4 common categorization mistakes, plus tone/style guidelines per documentation type

## References

**Primary Convention**: [Diátaxis Framework Convention](../../../repo-governance/conventions/structure/diataxis-framework.md)

**Related Conventions**:

- [Content Quality Principles](../../../repo-governance/conventions/writing/quality.md) - Universal content standards
- [File Naming Convention](../../../repo-governance/conventions/structure/file-naming.md) - Naming documentation files

**Related Skills**:

- `docs-applying-content-quality` - Universal markdown quality standards

---

This Skill packages Diátaxis framework knowledge for organizing and creating properly categorized documentation. For comprehensive details, consult the primary convention document.
