# In-the-Field — Core Concepts

## Core Concepts

## What is In-the-Field?

**In-the-field tutorials** are production implementation guides that achieve production readiness through 20-40 guides covering real-world scenarios with standard library→framework progression.

**NOT a replacement for**:

- By-example (which provides 95% language coverage through code-first examples)
- By-concept (which provides narrative explanations of fundamentals)
- Quick Start (which is 5-30% coverage touchpoints)

**Target Audience**:

- **Developers with foundation**: Completed by-example and/or by-concept
- **Ready for production**: Need to apply concepts in real systems
- **Framework selection**: Want informed decisions about tools
- **Enterprise patterns**: Need industry-standard practices

## Standard Library First Principle

**CRITICAL**: In-the-field tutorials MUST teach standard library/built-in approaches first, THEN introduce production frameworks with clear rationale.

**Progression pattern**:

1. **Show standard library approach** - Demonstrate built-in capabilities with full code
2. **Identify limitations** - Explain why standard approach insufficient for production
3. **Introduce framework** - Show how framework addresses limitations
4. **Compare trade-offs** - Discuss complexity, learning curve, maintenance

**Example progression** (Testing):

```markdown
## Testing in Production

## Standard Library: assert Keyword

Java provides `assert` keyword for runtime assertions...

[Code example with annotations]

**Limitations for production**:

- No test organization (all tests in main method)
- No reporting (just exceptions or silence)
- Manual execution (no test runner)

## Production Framework: JUnit 5

JUnit 5 provides test organization, reporting, automation...

[Code example with annotations]

**Trade-offs**:

- External dependency (2MB) vs organized tests
- Learning curve vs powerful features
- Justification: Worth it for production systems

## When to Use Each:

- assert: Simple scripts, internal tools
- JUnit: Production code, CI/CD, team projects
```
