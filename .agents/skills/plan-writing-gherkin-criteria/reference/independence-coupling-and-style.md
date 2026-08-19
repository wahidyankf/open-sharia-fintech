# Gherkin Acceptance Criteria — Scenario Independence, UI Coupling, and Style

## Scenario Independence

**Each scenario should be runnable in isolation** (no dependencies on other scenarios).

```gherkin
# ❌ Bad - Scenario depends on previous scenario
Scenario: Create user
  When I create user "Alice"
  Then user "Alice" should exist

Scenario: Update user email (DEPENDS on previous scenario)
  When I update user "Alice" email to "newemail@example.com"
  Then user "Alice" email should be "newemail@example.com"

# ✅ Good - Each scenario independent
Scenario: Create user
  When I create user with name "Alice" and email "alice@example.com"
  Then user should exist in database

Scenario: Update user email
  Given user "Alice" exists with email "alice@example.com"
  When I update user email to "newemail@example.com"
  Then user email should be "newemail@example.com"
```

## Avoiding UI Coupling

**Focus on behavior, not UI elements**.

```gherkin
# ❌ Bad - Coupled to UI implementation
Scenario: Login
  Given I am on "https://example.com/login"
  When I type "user@example.com" into input field with id "email-input"
  And I type "password" into input field with id "password-input"
  And I click button with class "btn-submit"
  Then I should be redirected to "https://example.com/dashboard"

# ✅ Good - Focused on business behavior
Scenario: Login with valid credentials
  Given I am on login page
  When I log in with email "user@example.com" and password "password"
  Then I should see the dashboard
  And I should be authenticated
```

## Declarative vs Imperative Style

**Prefer declarative style** (what should happen) over imperative style (how to do it).

```gherkin
# ❌ Imperative - Describes HOW
Scenario: User registration
  When I click "Sign Up" link
  And I fill in "Name" with "Alice"
  And I fill in "Email" with "alice@example.com"
  And I fill in "Password" with "secure123"
  And I fill in "Confirm Password" with "secure123"
  And I click "Register" button
  Then I should see "Registration successful"

# ✅ Declarative - Describes WHAT
Scenario: User registration
  When I register with name "Alice", email "alice@example.com", and password "secure123"
  Then registration should succeed
  And I should receive welcome email
  And I should be logged in automatically
```
