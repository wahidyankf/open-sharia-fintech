---
title: "Example Usage"
description: Four invocation examples — normal, strict, ocd modes, and explicit iteration bounds.
when_to_use: Use when looking for a concrete command to invoke this workflow at a specific mode or iteration setting.
---

# Example Usage

## Standard Invocation (Normal Strictness)

```
User: "Run repository rules quality gate workflow in normal mode"
```

The AI will invoke specialized agents via the Agent tool:

- Validate repository consistency (`rules-checker` delegated agent)
- Apply fixes for CRITICAL/HIGH findings (`rules-fixer` delegated agent)
- Iterate until zero CRITICAL/HIGH findings achieved
- Report MEDIUM/LOW findings without fixing them

## Pre-Release Validation (Strict Mode)

```
User: "Run repository rules quality gate workflow in strict mode"
```

The AI will invoke agents with stricter criteria:

- Fix CRITICAL/HIGH/MEDIUM findings
- Report LOW findings without fixing them
- Iterate until zero CRITICAL/HIGH/MEDIUM findings achieved

## Comprehensive Audit (OCD Mode)

```
User: "Run repository rules quality gate workflow in ocd mode"
```

The AI will invoke agents with zero-tolerance criteria:

- Fix ALL findings (CRITICAL, HIGH, MEDIUM, LOW)
- Iterate until zero findings at all levels
- Equivalent to pre-mode parameter behaviour

## With Iteration Bounds

```
User: "Run repository rules quality gate workflow in normal mode with min-iterations=2 and max-iterations=10"
```

The AI will invoke agents with iteration controls:

- Require at least 2 check-fix cycles
- Cap at maximum 10 iterations to prevent infinite loops
- Report final status (pass/partial) after completion
