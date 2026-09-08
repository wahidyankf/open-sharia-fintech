---
description: Covers unrelated actions hidden in one scenario and vague acceptance criteria.
when_to_use: Use when reviewing whether a scenario expresses one coherent journey.
---

# Anti-Patterns in Gherkin Journey Coherence and Acceptance Criteria

## Anti-Pattern 7: Unrelated Actions in One Scenario

**Problem**: Combining independently meaningful actions and outcomes that can pass or fail
separately. Repeated primary keywords are not themselves a violation when they express one
continuous journey.

**Bad Example:**

```gherkin
# NON-CONFORMING EXAMPLE — deliberate illustration of the violation
Scenario: User logs in and later deletes the account
  Given a registered user
  When the user submits valid credentials
  Then the dashboard is shown
  When the user deletes the account
  Then the account no longer exists
```

**Solution:**

```gherkin
Scenario: User login flow
  Given a registered user
  When the user submits valid credentials
  Then the dashboard is shown
  And a session token is set
```

Create a separate account-deletion scenario. Use repeated `When`/`Then` only when later steps cannot
stand alone from the same journey, such as requesting and then submitting a recovery code.

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
