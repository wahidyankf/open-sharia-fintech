---
description: "Defines explicit invocation, clean-streak exit, and default-delivery non-applicability."
when_to_use: "Use when validating the optional cycle's observable behaviour."
---

# PR Review Cycle — Success Criteria

```gherkin
Scenario: Explicit cycle reaches its clean-streak exit
  Given a user explicitly requested pr-review-cycle for an open pull request
  When two consecutive pr-review passes are clean on the same live head under different probes
  And exact-head/base PR CI is green for each credited pass
  Then final-status is done
  And authenticated pass and cycle-credit records identify the reviewed head

Scenario: Ordinary delivery does not invoke the cycle
  Given a pull request is ready for its default integration gate
  And no user explicitly requested iterative semantic review
  When delivery evaluates merge readiness
  Then it does not invoke pr-review-cycle
  And absence of cycle evidence is not a merge blocker
```
