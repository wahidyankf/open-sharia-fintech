---
title: "Example Usage"
description: "Worked example invocations covering all-relationships validation, a single language, a single framework, and iteration bounds."
when_to_use: "Use when looking for a concrete invocation pattern to copy for a specific scenario."
---

# Example Usage

## Validate All Explicit Relationships

```
User: "Run docs software engineering separation quality gate workflow for all"
```

The AI will invoke specialized agents via the Agent tool:

- Validate all explicit relationships (Java, Golang, Elixir, Spring, Spring Boot) (`docs-software-engineering-separation-checker` delegated agent)
- Apply separation fixes (`docs-software-engineering-separation-fixer` delegated agent)
- Iterate until zero findings achieved

## Validate Specific Language

```
User: "Run docs software engineering separation quality gate workflow for programming-languages/java"
```

The AI will invoke agents with scoped validation:

- Validate only Java documentation separation
- Fix issues in Java docs only
- Iterate until zero findings in scope

## Validate Specific Framework

```
User: "Run docs software engineering separation quality gate workflow for platform-web/tools/jvm-spring-boot"
```

The AI will invoke agents with framework scope:

- Validate only Spring Boot documentation separation
- Fix issues in Spring Boot docs
- Iterate until clean

## With Iteration Bounds

```
User: "Run docs software engineering separation quality gate workflow with min-iterations=2 and max-iterations=10"
```

The AI will invoke agents with iteration controls:

- Require at least 2 check-fix cycles
- Cap at maximum 10 iterations
- Report final status after completion
