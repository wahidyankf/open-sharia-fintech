---
description: The three preconditions that must hold before the API quality gate can run — reachable service, identified contract, non-destructive scope.
when_to_use: Use when confirming a service is ready to be exercised by the API quality gate.
---

# Preconditions

- **The service is running and reachable** at the supplied base URL. This gate tests a deployment,
  not a codebase — an unreachable service is a `fail`, never a `pass`.
- **The contract is identified**: an OpenAPI 3.x document or a GraphQL SDL. Without ground truth,
  the tester can only find crashes, not contract violations.
- **Destructive operations are out of scope.** The tester is non-destructive by construction; it
  never issues requests intended to delete or corrupt persistent state.
