---
title: "Gherkin Format and Step-Keyword Cardinality"
description: The Gherkin keyword syntax used to write scenarios, plus the HARD rule limiting every scenario to one primary Given/When/Then line.
category: explanation
subcategory: development
tags:
  - acceptance-criteria
  - gherkin
  - testing
  - requirements
created: 2025-12-07
when_to_use: Use when looking up the Gherkin Given-When-Then keyword syntax, or checking that a scenario follows the one-primary-keyword-per-Scenario rule.
---

# Gherkin Format and Step-Keyword Cardinality

## Gherkin Format

Gherkin uses natural language with specific keywords to structure acceptance criteria as scenarios.

### Core Keywords

**Scenario**: Describes a specific behavior or outcome

```gherkin
Scenario: User successfully logs in with valid credentials
```

**Given**: Sets up the initial context or preconditions

```gherkin
Given a user with email "user@example.com" and password "securepass123"
And the user is on the login page
```

**When**: Describes the action or event being tested

```gherkin
When the user enters their email and password
And clicks the "Login" button
```

**Then**: Specifies the expected outcome or result

```gherkin
Then the user should be redirected to the dashboard
And see a welcome message "Welcome back, User!"
And the session should be authenticated
```

**And/But**: Connects multiple conditions (same semantic level as previous keyword)

```gherkin
Given a user is logged in
And has admin privileges
But has not completed onboarding
```

### Complete Syntax

```gherkin
Scenario: [Concise description of behavior]
 Given [initial context]
 And [additional context]
 When [action occurs]
 And [additional action]
 Then [expected outcome]
 And [additional outcome]
 But [constraint or exception]
```

## Step-Keyword Cardinality (HARD Rule)

> **HARD rule — one primary keyword each**: Every `Scenario` MUST use exactly **one**
> primary `Given` line, exactly **one** primary `When` line, and exactly **one** primary
> `Then` line. Every additional precondition, action, or outcome MUST be chained with
> `And` or `But` — never a repeated `Given` / `When` / `Then` keyword. This reinforces
> the "one action / one behavior per scenario" norm.
>
> **Exemptions**: `Background` blocks and `Scenario Outline` `Examples` tables are
> exempt from the one-each constraint.

**Conforming example**:

```gherkin
Scenario: Login succeeds
  Given a registered user
  And the login page is open
  When the user submits valid credentials
  Then the dashboard is shown
  And a session token is set
```

**Non-conforming example** (violates — two primary `When` keyword lines):

```gherkin
# NON-CONFORMING EXAMPLE — deliberate illustration of the violation
Scenario: Login succeeds
  Given a registered user
  When the user opens the login page
  When the user submits valid credentials
  Then the dashboard is shown
```

(The fix replaces the second `When` with `And`.)

**Enforcement**: The deterministic `rhino-cli specs gherkin-cardinality validate`
audit flags every `.feature` file that violates this rule. `plan-checker` and
`repo-rules-checker` apply the same rule to Gherkin fences in plan markdown.
