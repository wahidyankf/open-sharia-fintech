---
title: "Real-World Examples, Anti-Patterns, and When to Use"
description: Full worked Gherkin examples, common anti-patterns to avoid, and the four categories of documentation where acceptance criteria belong.
category: explanation
subcategory: development
tags:
  - acceptance-criteria
  - gherkin
  - testing
  - requirements
created: 2025-12-07
when_to_use: Use when you need a full worked scenario to copy from, want to check a draft scenario against known anti-patterns, or are deciding whether a document needs acceptance criteria at all.
---

# Real-World Examples, Anti-Patterns, and When to Use

## Real-World Examples

### Example 1: User Authentication (from 2025-11-24\_\_init-monorepo)

```gherkin
Scenario: User successfully creates account with valid information
 Given the registration page is loaded
 When the user enters email "newuser@example.com"
 And enters password "SecurePass123!"
 And enters password confirmation "SecurePass123!"
 And accepts terms of service
 And clicks "Create Account"
 Then account should be created in database
 And confirmation email should be sent to "newuser@example.com"
 And user should be redirected to dashboard
 And session should be authenticated
```

### Example 2: Content Validation (from 2025-12-03\_\_golang-full-set-tutorials)

```gherkin
Scenario: Tutorial content passes quality validation
 Given a tutorial file "01-hello-world.md"
 When the validator checks the tutorial
 Then frontmatter should include required fields (title, description, level, topics)
 And code examples should be syntax-highlighted
 And all internal links should be valid
 And no broken external links should exist
 And Mermaid diagrams should use accessible color palette
```

## Anti-Patterns

### FAIL: Vague or Ambiguous Language

```text
Then the system should work correctly
Then performance should be acceptable
Then users should be happy
```

**Better**: Define specific, measurable criteria

### FAIL: Testing Implementation Details

```text
Then the Redux store should be updated
Then the database transaction should commit
Then the cache should be invalidated
```

**Better**: Focus on observable behaviour from user perspective

### FAIL: Multiple Behaviours in One Scenario

```text
Scenario: Complete user workflow
 [50 lines covering registration, login, profile update, logout]
```

**Better**: Split into separate scenarios (one behaviour each)

### FAIL: Missing Context

```text
When the button is clicked
Then something happens
```

**Better**: Specify which button, what context, what exact outcome

## When to Use Acceptance Criteria

### PASS: Project Plans

- **Product requirements files** (`plans/*/prd.md`): Define Gherkin acceptance criteria for each user story
- **Delivery checklists**: Validate implementation against Gherkin scenarios
- See [Plans Organization Convention](../../../conventions/structure/plans.md)

### PASS: Feature Specifications

- **Feature docs**: Describe expected behaviour for new features
- **RFC documents**: Define acceptance criteria for proposed changes
- **ADRs**: Specify outcomes of architectural decisions

### PASS: API Documentation

- **Endpoint specifications**: Describe request/response scenarios
- **Error handling**: Define error conditions and responses
- **Integration scenarios**: Describe cross-service behaviour

### PASS: Test Documentation

- **Test plans**: Structure test cases as Gherkin scenarios
- **QA checklists**: Verify manual testing scenarios
- **Regression test suites**: Document scenarios to prevent regressions
