# Gherkin Acceptance Criteria — Basic Scenario Patterns

## Pattern 1: Simple Success Path

**Use case**: Straightforward happy path with clear steps

```gherkin
Scenario: Create new blog post
  Given I am logged in as a content editor
  When I navigate to "Create New Post" page
  And I fill in the title with "My First Post"
  And I fill in the content with "This is my content"
  And I click "Publish" button
  Then I should see success message "Post published successfully"
  And the post should appear in my posts list
  And the post should have status "Published"
```

## Pattern 2: Error Handling

**Use case**: Invalid input or error conditions

```gherkin
Scenario: Reject login with invalid password
  Given a registered user with email "alice@example.com"
  When the user submits login form with incorrect password
  Then the user should remain on login page
  And error message should display "Invalid email or password"
  And login attempt should be logged
  And no session token should be created
```

## Pattern 3: Boundary Conditions

**Use case**: Testing edge cases and limits

```gherkin
Scenario: Prevent posts with titles exceeding maximum length
  Given I am logged in as a content editor
  And maximum title length is 200 characters
  When I attempt to create post with title of 201 characters
  Then I should see validation error "Title must be 200 characters or less"
  And the post should not be created
  And I should remain on post creation page
```
