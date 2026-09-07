---
description: Six best practices for writing concrete, testable Gherkin scenarios, each with a PASS/FAIL example.
when_to_use: Use when drafting a Gherkin scenario and wanting to check it against the specific-values, single-behaviour, present-tense, behaviour-focused, testable, and data-table best practices.
---

# Best Practices

## 1. Be Specific with Concrete Values

PASS: **Good**:

```gherkin
Given a cart with 3 items totaling $150.00
When the user applies discount code "SAVE20"
Then the total should be reduced to $120.00
```

FAIL: **Bad**:

```gherkin
Given a cart with items
When the user applies a discount
Then the total should be less
```

## 2. One Scenario Per Behaviour

PASS: **Good**:

```text
Scenario: User login succeeds with valid credentials
Scenario: User login fails with invalid password
Scenario: User login fails with non-existent email
```

FAIL: **Bad**:

```text
Scenario: User login (covers success, wrong password, wrong email, etc.)
```

## 3. Use Present Tense

PASS: **Good**: `When the user clicks the button`
FAIL: **Bad**: `When the user clicked the button` or `When the user will click`

## 4. Focus on Behaviour, Not Implementation

PASS: **Good**:

```gherkin
When the user submits the registration form
Then an account should be created
```

FAIL: **Bad**:

```gherkin
When the user clicks submit button triggering handleSubmit() function
Then a POST request to /api/users endpoint should create a database record
```

## 5. Make It Testable

PASS: **Good**:

```text
Then the success message "Account created!" should be displayed
And the user should receive a confirmation email within 5 minutes
```

FAIL: **Bad**:

```text
Then the user should feel confident their account was created
```

## 6. Use Data Tables for Multiple Inputs

```gherkin
Scenario Outline: Password validation
 Given a user enters password "<password>"
 When the password is validated
 Then validation should return "<result>"
 And show message "<message>"

 Examples:
  | password   | result | message                          |
  | abc        | fail   | Password must be at least 8 chars |
  | abcd1234   | fail   | Password must include uppercase   |
  | Abcd1234   | pass   | Password meets requirements       |
```
