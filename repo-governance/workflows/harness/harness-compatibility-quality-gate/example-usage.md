---
description: Three invocation examples — standard strict-mode run, single-harness scope, and explicit iteration bounds.
when_to_use: Use when looking for a concrete command to invoke this workflow with a specific scope or iteration setting.
---

# Example Usage

## Standard Invocation (Strict Mode — Default)

```
User: "Run repo harness compatibility quality gate workflow"
```

The orchestrator invokes specialized agents:

- `harness-compatibility-checker` consumes lifecycle evidence, runs unowned Phase 0 parity,
  then Phase 1
  (fetches current upstream conventions for all supported harnesses and diffs against the
  catalog and committed binding files)
- `harness-compatibility-fixer` applies in-scope parity fixes (CRITICAL/HIGH/MEDIUM)
  and catalog updates
- Iterates until zero findings achieved on two consecutive checks
- Reports LOW-severity drift without fixing it

## Single Harness Scope

```
User: "Run repo harness compatibility quality gate workflow with scope=codex-cli"
```

Scopes Phase 1 to a single harness. Unowned Phase 0 semantics still run; delegated predicates
remain filtered regardless of scope.

## With Iteration Bounds

```
User: "Run repo harness compatibility quality gate workflow in strict mode with min-iterations=2 and max-iterations=5"
```

Requires at least 2 check-fix cycles and caps at 5 iterations.
