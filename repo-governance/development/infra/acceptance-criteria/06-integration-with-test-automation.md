---
title: "Integration with Test Automation"
description: Mapping Gherkin scenarios to step definitions in Cucumber.js, Jest-Cucumber, Behave, and Godog.
category: explanation
subcategory: development
tags:
  - acceptance-criteria
  - gherkin
  - testing
  - requirements
created: 2025-12-07
when_to_use: Use when wiring a Gherkin scenario to a BDD test framework in JavaScript/TypeScript, Python, or Go.
---

# Integration with Test Automation

Gherkin scenarios can be directly translated to automated tests using BDD frameworks:

## JavaScript/TypeScript

**Cucumber.js**:

```javascript
// features/login.feature
Scenario: User login with valid credentials
  Given a user with email "user@example.com"
  When the user logs in with correct password
  Then the user should be authenticated

// step-definitions/login.steps.js
Given('a user with email {string}', async (email) => {
  await createUser({ email });
});

When('the user logs in with correct password', async () => {
  await loginPage.login(user.email, user.password);
});

Then('the user should be authenticated', async () => {
  expect(await session.isAuthenticated()).toBe(true);
});
```

**Jest-Cucumber**:

```javascript
import { defineFeature, loadFeature } from "jest-cucumber";
const feature = loadFeature("./features/login.feature");

defineFeature(feature, (test) => {
  test("User login with valid credentials", ({ given, when, then }) => {
    given('a user with email "user@example.com"', () => {
      // Setup code
    });
    // ... when, then implementations
  });
});
```

## Python

**Behave**:

```python
# features/login.feature (Gherkin)
# features/steps/login.py
@given('a user with email "{email}"')
def step_impl(context, email):
  context.user = create_user(email=email)

@when('the user logs in with correct password')
def step_impl(context):
  context.response = login(context.user.email, context.user.password)

@then('the user should be authenticated')
def step_impl(context):
  assert context.response.authenticated == True
```

## Go

**Godog**:

```go
// features/login.feature (Gherkin)
// login_test.go
func (s *Suite) aUserWithEmail(email string) error {
 s.user = createUser(email)
 return nil
}

func (s *Suite) theUserLogsInWithCorrectPassword() error {
 s.response = login(s.user.Email, s.user.Password)
 return nil
}

func (s *Suite) theUserShouldBeAuthenticated() error {
 if !s.response.Authenticated {
  return fmt.Errorf("expected user to be authenticated")
 }
 return nil
}
```
