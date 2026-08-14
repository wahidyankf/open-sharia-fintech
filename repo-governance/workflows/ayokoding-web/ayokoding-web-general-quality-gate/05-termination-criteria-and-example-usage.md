---
title: "Termination Criteria and Example Usage"
description: Defines the pass/partial/fail termination conditions for the general quality gate and shows four example invocations (full, language-scoped, section-scoped, iteration-bounded).
when_to_use: Use when determining whether a run has reached a terminal state, or when looking up example invocation syntax.
---

# Termination Criteria and Example Usage

## Termination Criteria

- PASS: **Success** (`pass`): Zero findings of ANY level (CRITICAL, HIGH, MEDIUM, LOW) across all validators on **two consecutive** validations (consecutive pass requirement)
- **Partial** (`partial`): Any findings remain after max-iterations OR final validation found issues
- FAIL: **Failure** (`fail`): Checkers, fixers, or finalization agents encountered technical errors

## Example Usage

### Full Content Check-Fix

```
User: "Run ayokoding-web general quality gate workflow"
```

The AI will invoke specialized agents via the Agent tool:

- Validate all ayokoding-web content in parallel (`apps-ayokoding-www-general-checker`, `apps-ayokoding-www-facts-checker`, `apps-ayokoding-www-link-checker` delegated agents)
- Fix all findings (`apps-ayokoding-www-general-fixer`, `apps-ayokoding-www-facts-fixer` delegated agents)
- Iterate until zero findings achieved

### Validate Specific Language

```
User: "Run ayokoding-web general quality gate workflow for ayokoding-web/content/en/"
```

The AI will invoke agents with language-scoped validation:

- Validate only English content
- Fix issues in English files only

### Validate Specific Section

```
User: "Run ayokoding-web general quality gate workflow for ayokoding-web/content/en/programming/"
```

The AI will invoke agents with section-scoped validation:

- Validate only programming section
- Fix issues in that section

### With Iteration Bounds

```
User: "Run ayokoding-web general quality gate workflow with min-iterations=2 and max-iterations=10"
```

The AI will invoke agents with iteration controls:

- Require at least 2 check-fix cycles
- Cap at maximum 10 iterations
- Report final status after completion
