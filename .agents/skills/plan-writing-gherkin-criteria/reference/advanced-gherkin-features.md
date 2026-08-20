# Gherkin Acceptance Criteria — Advanced Gherkin Features

## Background Block

**Purpose**: Share common setup across multiple scenarios

```gherkin
Feature: User Authentication

Background:
  Given the application is running
  And the database contains the following users:
    | email              | password   | role   |
    | admin@example.com  | admin123   | admin  |
    | user@example.com   | user123    | user   |

Scenario: Admin login
  When user "admin@example.com" logs in with password "admin123"
  Then the user should have admin privileges

Scenario: Regular user login
  When user "user@example.com" logs in with password "user123"
  Then the user should have user privileges
```

**Rules**:

- Background runs before EACH scenario in the feature
- Use for common setup that applies to all scenarios
- Don't put scenario-specific setup in Background

## Scenario Outline with Examples

**Purpose**: Test same scenario with multiple data sets

```gherkin
Scenario Outline: Validate email format
  Given I am on registration page
  When I enter email "<email>"
  And I submit the form
  Then I should see "<result>"

  Examples:
    | email                | result                          |
    | valid@example.com    | Registration successful         |
    | invalid              | Please enter a valid email      |
    | missing@             | Please enter a valid email      |
    | @missing.com         | Please enter a valid email      |
    | spaces @example.com  | Please enter a valid email      |
```

**Benefits**:

- DRY (Don't Repeat Yourself) - One scenario tests multiple cases
- Easy to add new test cases (just add row to table)
- Clear documentation of all tested variations

## Data Tables

**Purpose**: Pass structured data to steps

```gherkin
Scenario: Bulk import users
  Given I am logged in as admin
  When I import the following users:
    | name    | email              | role   |
    | Alice   | alice@example.com  | editor |
    | Bob     | bob@example.com    | viewer |
    | Charlie | charlie@example.com| editor |
  Then all 3 users should be created
  And I should see success message "3 users imported successfully"
  And each user should receive welcome email
```
