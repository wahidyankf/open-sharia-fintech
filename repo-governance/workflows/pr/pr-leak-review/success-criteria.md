---
title: "Success Criteria"
description: "Defines clean, finding, and stale scenarios."
when_to_use: "Use when validating the workflow's observable behavior."
---

# Success Criteria

```gherkin
Scenario: Current head contains no leak
  Given an open pull request at a pinned head
  When exact leak-only review finds no real leak
  Then it posts one sanitized COMMENT review
  And authenticated current-head ose-pr-leak-review:v1 evidence reports pass

Scenario: Current head contains a protected value
  Given a tracked PR hunk contains a real production credential
  When exact leak-only review reports it
  Then the finding names only category, location, and remediation
  And no output repeats or transforms the credential

Scenario: Head moves during review
  Given review began from a pinned head
  When the PR head changes before or after posting
  Then final-status is stale
  And no evidence authorizes the new head
```
