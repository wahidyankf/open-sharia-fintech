---
title: "Integration with Test Automation"
description: Mapping Gherkin scenarios to step definitions in Cucumber.js, Jest-Cucumber, and cucumber-rs.
category: explanation
subcategory: development
tags:
  - acceptance-criteria
  - gherkin
  - testing
  - requirements
created: 2025-12-07
when_to_use: Use when wiring a Gherkin scenario to a BDD test framework in TypeScript, Rust, or F#.
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

## Rust

**cucumber-rs** (the `harness = false` test-binary pattern `rhino-cli` uses):

```rust
// specs/.../login.feature (Gherkin)
// tests/login.rs
#[given(regex = r#"^a user with email "([^"]*)"$"#)]
fn a_user_with_email(w: &mut LoginWorld, email: String) {
    w.user = create_user(&email);
}

#[when("the user logs in with correct password")]
fn logs_in(w: &mut LoginWorld) {
    w.response = login(&w.user.email, &w.user.password);
}

#[then("the user should be authenticated")]
fn is_authenticated(w: &mut LoginWorld) {
    assert!(w.response.authenticated);
}
```

## F\#

F# suites auto-bind scenarios by name rather than declaring explicit step definitions, so there is
no step-definition file to write — name the test after the scenario and the binding follows.

## Adding a Language

Only wire a framework for a language this repository actually builds in. Adding a new one also
means teaching `rhino-cli`'s spec-coverage extractor to recognise its step-definition syntax —
otherwise the scenarios read as uncovered.
