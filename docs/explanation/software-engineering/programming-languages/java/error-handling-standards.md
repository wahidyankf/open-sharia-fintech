---
title: "Java Error Handling Standards"
description: Authoritative OSE Platform Java error-handling standards — exception boundaries, fail-fast startup, response shape, and what is never returned to a client
category: explanation
subcategory: prog-lang
tags:
  - java
  - error-handling-standards
  - exceptions
  - fail-fast
  - spring-boot
  - security
principles:
  - explicit-over-implicit
  - pure-functions
  - reproducibility
created: 2026-09-08
---

# Java Error Handling Standards

## Prerequisite Knowledge

**REQUIRED**: You MUST understand Java exception fundamentals from the [AyoKoding Java Learning Path](../../../../../apps/ayokoding-www/content/en/learn/legacy/software-engineering/programming-languages/java/_index.md) before using these standards.

**This document is OSE Platform-specific**, not a Java exceptions tutorial. We define HOW errors are handled in THIS codebase, not WHAT an exception is.

**See**: [Programming Language Documentation Separation Convention](../../../../../repo-governance/conventions/structure/programming-language-docs-separation.md)

## Two Kinds of Failure

Java code here distinguishes failures that are part of the design from failures that are not:

- **Expected outcomes** — a request for something that does not exist, input that does not parse. These are modelled as return values or as a specific exception type the caller is expected to handle, and they map to a deliberate HTTP status.
- **Programming errors and broken invariants** — a null where the type said non-null, an unreachable branch reached. These are not caught. They propagate, and the failure is loud.

The mistake this rule exists to prevent is catching the second kind and turning it into the first. A `catch (Exception e)` that returns a default converts a defect into wrong data.

## Fail Fast at Startup

Misconfiguration is a startup failure, never a runtime fallback.

If `OSE_LMS_BE_PORT` is set to something that is not a valid port, the application must not start. A service that silently ignores a malformed override starts on a port nobody asked for, and the operator discovers the mistake by finding nothing listening where they expected it.

This is the same rule as [explicit over implicit](../../../../../repo-governance/principles/software-engineering/explicit-over-implicit.md) applied to configuration: a value that was provided and ignored is worse than a value that was rejected.

## Catch Narrowly, at a Boundary

Catch the specific exception type you can actually handle, and catch it where handling is possible:

```java
// Good — a specific failure, converted at the point where a decision exists
try {
  return Integer.parseInt(rawPort);
} catch (NumberFormatException cause) {
  throw new IllegalArgumentException(
      "OSE_LMS_BE_PORT must be an integer, got: " + rawPort, cause);
}
```

Rules that follow from it:

- **Never swallow.** An empty catch block, or one that only logs and continues, discards the only evidence of the failure.
- **Always chain the cause.** Passing `cause` preserves the original stack trace. Constructing a new exception without it destroys the diagnosis.
- **Never catch `Throwable`.** It captures `Error` — `OutOfMemoryError`, `StackOverflowError` — which no application handler can meaningfully recover from.

## Prefer Unchecked Exceptions

Use unchecked exceptions for programming errors and unrecoverable conditions. Checked exceptions propagate a `throws` clause through every intermediate caller, and in practice the clause is satisfied by a wrapping catch that adds nothing.

Where a failure is a genuine expected outcome that a caller must handle, prefer expressing it in the return type over a checked exception.

## Exception Messages Are for Diagnosis

A message states what was expected, what was received, and which input it came from:

```java
// Good
"OSE_LMS_BE_PORT must be an integer, got: eight-thousand"

// Bad
"Invalid port"
```

The bad message costs a reader a debugging session to recover information the throwing code already had.

## What a Client Never Sees

Error responses returned over HTTP MUST NOT contain:

- Stack traces or exception class names
- File-system paths, hostnames, or internal service names
- Configuration values, connection strings, or anything read from the environment
- Any value that would be a secret if logged

A generic message with a stable status code goes to the client; the detail goes to the log. Actuator's health endpoint is configured with `show-details: never` for the same reason, and that restriction is asserted by a test rather than trusted.

**See**: [Secrets and Env Standards](../../../../../repo-governance/conventions/security/secrets-and-env-standards.md)

## Error Behaviour Is Specified Behaviour

An error path is behaviour, so it follows the same route as any other behaviour: a Gherkin scenario in the owning `specs/` corpus, bound in the Unit adapter, before the code exists.

"Returns 404 for an unknown path" and "rejects a malformed port at startup" are scenarios, not implementation details. If an error path has no scenario, its behaviour is whatever the framework happened to do — which is a default nobody chose and nothing protects.

## Related Documentation

- [Java Overview](./README.md)
- [Java Coding Standards](./coding-standards.md)
- [Java Testing Standards](./testing-standards.md)
