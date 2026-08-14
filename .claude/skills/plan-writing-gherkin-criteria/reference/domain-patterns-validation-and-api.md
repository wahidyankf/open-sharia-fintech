# Gherkin Acceptance Criteria — Domain Patterns: Form Validation and API Responses

## Form Validation

```gherkin
Feature: User Registration Form Validation

Scenario Outline: Email validation
  Given I am on registration page
  When I enter email "<email>"
  And I submit the form
  Then I should see validation result "<result>"

  Examples:
    | email               | result                        |
    | valid@example.com   | Success                       |
    | invalid             | Invalid email format          |
    | missing@domain      | Invalid email format          |
    | user@              | Invalid email format          |

Scenario: Password strength validation
  Given I am on registration page
  When I enter password "weak"
  Then I should see error "Password must be at least 8 characters"
  And submit button should be disabled

Scenario: Matching password confirmation
  Given I am on registration page
  When I enter password "secure123"
  And I enter password confirmation "different"
  Then I should see error "Passwords do not match"
  And submit button should be disabled
```

## API Responses

```gherkin
Feature: REST API User Endpoints

Scenario: GET user by ID
  Given user with id 123 exists in database
  When client sends GET request to "/api/users/123"
  Then response status should be 200
  And response body should contain:
    """
    {
      "id": 123,
      "name": "Alice",
      "email": "alice@example.com"
    }
    """

Scenario: POST create new user
  Given client is authenticated as admin
  When client sends POST request to "/api/users" with body:
    """
    {
      "name": "Bob",
      "email": "bob@example.com",
      "password": "secure123"
    }
    """
  Then response status should be 201
  And response should contain user id
  And user should exist in database
  And welcome email should be sent to "bob@example.com"
```
