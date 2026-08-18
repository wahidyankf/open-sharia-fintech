---
title: "Anti-Patterns in Gherkin Keyword Cardinality and Acceptance Criteria"
description: Covers the Gherkin multiple-primary-keyword and vague-acceptance-criteria anti-patterns, with the cardinality rule and testable-criteria examples.
category: explanation
subcategory: development
tags: [anti-patterns, gherkin, acceptance-criteria, specs]
created: 2026-05-12
when_to_use: Use when writing or reviewing a Gherkin Scenario block or drafting acceptance criteria for a plan or spec.
---

# Anti-Patterns in Gherkin Keyword Cardinality and Acceptance Criteria

## Anti-Pattern 7: Multiple Primary `When`/`Then` Keywords in One Scenario

**Problem**: Using more than one primary `When` or `Then` keyword in the same `Scenario` block
instead of chaining with `And`/`But`. This violates the
[step-keyword cardinality HARD rule](../acceptance-criteria/gherkin-format-and-step-keyword-cardinality.md#step-keyword-cardinality-hard-rule)
and obscures the "one action / one behavior" boundary.

**Bad Example:**

```gherkin
# NON-CONFORMING EXAMPLE — deliberate illustration of the violation
Scenario: User login flow
  Given a registered user
  When the user navigates to the login page
  When the user submits valid credentials
  Then the dashboard is shown
  Then a session token is set
```

**Solution:**

```gherkin
Scenario: User login flow
  Given a registered user
  And the login page is open
  When the user submits valid credentials
  Then the dashboard is shown
  And a session token is set
```

**Rationale:**

- Multiple primary keywords blur where the scenario's single action starts and ends
- Deterministic linter (`rhino-cli specs gherkin-cardinality validate`) flags violations
- `plan-checker` and `repo-rules-checker` enforce the rule on Gherkin fences in plan markdown
- Note: `Background` blocks and `Scenario Outline` `Examples` tables are exempt

## Anti-Pattern 8: Vague Acceptance Criteria

**Problem**: Writing ambiguous, non-testable acceptance criteria.

**Bad Example:**

```markdown
The system should work well and be fast.
Users should have a good experience.
```

**Solution:**

```gherkin
Scenario: User views dashboard
  Given a logged-in user
  When the user navigates to dashboard
  Then the page loads in under 2 seconds
  And all widgets display current data
```

**Rationale:**

- Vague criteria can't be tested
- No clear definition of "done"
- Can't automate validation
- Gherkin provides executable specifications
