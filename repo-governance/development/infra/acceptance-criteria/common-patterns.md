---
title: "Common Patterns"
description: Reusable Gherkin scenario patterns for CRUD operations, authentication and authorization, and error handling.
category: explanation
subcategory: development
tags:
  - acceptance-criteria
  - gherkin
  - testing
  - requirements
created: 2025-12-07
when_to_use: Use when writing acceptance criteria for a CRUD feature, an auth-gated route, or an error-handling path and want a starting scenario shape.
---

# Common Patterns

## CRUD Operations

**Create**:

```gherkin
Scenario: Create new project
 Given the user is logged in
 When the user creates a project with name "My Project"
 And sets visibility to "Private"
 Then the project should appear in the projects list
 And the user should be set as owner
```

**Read**:

```gherkin
Scenario: View project details
 Given a project "My Project" exists
 When the user navigates to the project page
 Then the project name should be displayed
 And the project metadata should be visible
```

**Update**:

```gherkin
Scenario: Update project settings
 Given a project "My Project" exists with visibility "Private"
 When the user changes visibility to "Public"
 And saves the changes
 Then the project visibility should be "Public"
 And other users should be able to find the project
```

**Delete**:

```gherkin
Scenario: Delete project
 Given a project "My Project" exists
 When the user deletes the project
 And confirms the deletion
 Then the project should be removed from the database
 And the user should be redirected to the projects list
```

## Authentication & Authorization

```gherkin
Scenario: Admin user accesses admin panel
 Given a user with role "Admin"
 And the user is logged in
 When the user navigates to "/admin"
 Then the admin panel should be accessible

Scenario: Regular user cannot access admin panel
 Given a user with role "Member"
 And the user is logged in
 When the user attempts to navigate to "/admin"
 Then access should be denied with 403 Forbidden
 And the user should see "Insufficient permissions" message
```

## Error Handling

```gherkin
Scenario: Handle network timeout gracefully
 Given the API server is unresponsive
 When the user submits a form
 And waits more than 30 seconds
 Then a timeout error should be displayed
 And the form data should be preserved
 And the user should be prompted to retry
```
