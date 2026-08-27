---
title: "Success Criteria"
description: "Defines clean-discovery, verified-fix, partial, and lifecycle scenarios."
when_to_use: "Use when validating the bounded API quality gate's observable behavior."
---

# Success Criteria

```gherkin
Scenario: Clean discovery passes immediately
  Given discovery completes with no in-threshold AET findings
  When the workflow evaluates the result
  Then final-status is pass
  And no fixer, rebuild, redeployment, or verification pass runs

Scenario: Fixed findings verify against the live service
  Given discovery reports in-threshold findings
  When one fix, rebuild, and deployment completes
  And scoped verification resolves every original finding without regression
  Then final-status is pass

Scenario: Verification leaves API defects
  Given an original finding remains or affected-API smoke exposes a regression
  When scoped verification finishes
  Then final-status is partial
  And no automatic rerun starts

Scenario: Lifecycle evidence remains independently blocking
  Given final-status is pass
  And lifecycle-status is pending
  When merge readiness is evaluated
  Then the owning lifecycle gate still blocks delivery
```
