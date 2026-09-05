---
title: "Example Usage"
description: "Worked example invocations covering standard, lax, strict, ocd modes, scoped validation, and iteration bounds."
when_to_use: "Use when looking for a concrete invocation pattern to copy for a specific scenario."
---

# Example Usage

## Standard Invocation (Normal Strictness)

```
User: "Run documentation quality gate workflow in normal mode"
```

The AI will invoke specialized agents via the Agent tool:

- Validate all docs/ content in parallel (`docs-checker`, `docs-tutorial-checker`, `docs-link-checker` delegated agents)
- Fix CRITICAL/HIGH findings (`docs-fixer`, `docs-tutorial-fixer` delegated agents)
- Iterate until zero CRITICAL/HIGH findings achieved
- Report MEDIUM/LOW findings without fixing them

## Quick Critical-Only Check (Lax Mode)

```
User: "Run documentation quality gate workflow in lax mode"
```

The AI will invoke agents with minimal criteria:

- Fix CRITICAL findings only
- Report HIGH/MEDIUM/LOW findings without fixing them
- Success when zero CRITICAL findings remain

## Pre-Release Validation (Strict Mode)

```
User: "Run documentation quality gate workflow in strict mode"
```

The AI will invoke agents with stricter criteria:

- Fix CRITICAL/HIGH/MEDIUM findings
- Report LOW findings without fixing them
- Iterate until zero CRITICAL/HIGH/MEDIUM findings achieved

## Comprehensive Audit (OCD Mode)

```
User: "Run documentation quality gate workflow in ocd mode"
```

The AI will invoke agents with zero-tolerance criteria:

- Fix ALL findings (CRITICAL, HIGH, MEDIUM, LOW)
- Iterate until zero findings at all levels
- Equivalent to pre-mode parameter behaviour

## Validate Specific Scope

```
User: "Run documentation quality gate workflow for docs/tutorials/"
```

The AI will invoke agents with scoped validation:

- Validate only tutorial files
- Fix issues in that scope only

```
User: "Run documentation quality gate workflow for repo-governance/conventions/structure/file-naming.md"
```

The AI will invoke agents with single-file scope:

- Validate specific file only
- Fix issues in that file

## With Iteration Bounds

```
User: "Run documentation quality gate workflow in normal mode with min-iterations=2 and max-iterations=10"
```

The AI will invoke agents with iteration controls:

- Require at least 2 check-fix cycles
- Cap at maximum 10 iterations
- Report final status after completion
