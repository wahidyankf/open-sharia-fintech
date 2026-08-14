# Gherkin Acceptance Criteria — Domain Patterns: Auth and CRUD

## Authentication & Authorization

```gherkin
Feature: User Authentication

Scenario: Successful login with valid credentials
  Given a user with email "user@example.com" and password "secure123"
  When the user submits login credentials
  Then the user should be authenticated
  And session token should be created
  And user should be redirected to dashboard

Scenario: Rejected login with invalid credentials
  Given a user with email "user@example.com"
  When the user submits incorrect password
  Then authentication should fail
  And error message "Invalid credentials" should display
  And no session token should be created

Scenario: Access protected resource without authentication
  Given the user is not logged in
  When the user attempts to access "/dashboard"
  Then the user should be redirected to "/login"
  And error message "Please log in to continue" should display
```

## CRUD Operations

```gherkin
Feature: Article Management

Scenario: Create new article
  Given I am authenticated as editor
  When I create article with title "Test" and content "Content"
  Then article should be saved to database
  And article should have status "draft"
  And I should see success message "Article created"

Scenario: Update existing article
  Given I am authenticated as editor
  And article "Test" exists with id 123
  When I update article 123 title to "Updated Test"
  Then article 123 title should be "Updated Test"
  And article 123 updated_at timestamp should be current time
  And I should see success message "Article updated"

Scenario: Delete article
  Given I am authenticated as editor
  And article "Test" exists with id 123
  When I delete article 123
  Then article 123 should not exist in database
  And I should see success message "Article deleted"
  And I should be redirected to articles list
```
