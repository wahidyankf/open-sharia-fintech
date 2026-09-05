---
title: "Best Practices: Execution Tracking, Acceptance Criteria, and Tooling"
description: Covers best practices for scope-based execution tracking in concurrent workflows, writing Gherkin acceptance criteria, and required tools for report-generating checker agents.
category: explanation
subcategory: development
tags: [infrastructure, best-practices, acceptance-criteria, agents]
created: 2026-05-12
when_to_use: Use when tracking concurrent workflow executions, writing Given-When-Then acceptance criteria, or configuring tools for a checker agent that generates reports.
---

# Best Practices: Execution Tracking, Acceptance Criteria, and Tooling

## Practice 5: Use Scope-Based Execution Tracking

**Principle**: Track execution chains within scopes to handle concurrent workflows.

**Good Example:**

```bash
# Determine scope
SCOPE="${EXECUTION_SCOPE:-docs}"

# Read parent chain from scope-specific file
CHAIN_FILE="local-tmp/.execution-chain-${SCOPE}"
if [ -f "$CHAIN_FILE" ]; then
  read PARENT_TIME PARENT_CHAIN < "$CHAIN_FILE"
  TIME_DIFF=$(($(date +%s) - PARENT_TIME))

  if [ $TIME_DIFF -lt 30 ]; then
    UUID_CHAIN="${PARENT_CHAIN}_${MY_UUID}"
  else
    UUID_CHAIN="${MY_UUID}"
  fi
else
  UUID_CHAIN="${MY_UUID}"
fi
```

**Bad Example:**

```bash
# Global tracking file (causes race conditions)
CHAIN_FILE="local-tmp/.execution-chain"
# All workflows share same file - parent tracking breaks!
```

**Rationale:**

- Isolates concurrent workflow executions
- Prevents cross-contamination between scopes
- Enables accurate parent-child hierarchy
- Handles parallel execution correctly

## Practice 6: Write Gherkin Acceptance Criteria

**Principle**: Use Given-When-Then format for testable requirements. Every scenario needs an
explicit `When` and `Then`. Prefer `And`/`But` for continuation, but allow repeated primary
keywords for one continuous journey.

**Good Example:**

```gherkin
Scenario: User logs in with valid credentials
  Given a registered user with email "user@example.com"
  When the user submits login form with correct password
  Then the user is redirected to dashboard
  And a session token is created
```

**Continuous-journey example:**

```gherkin
Scenario: User logs in with valid credentials
  Given a registered user with email "user@example.com"
  When the user navigates to the login page
  When the user submits login form with correct password
  Then the user is redirected to dashboard
```

**Bad Example (vague):**

```markdown
The system should allow users to log in.
```

**Rationale:**

- Testable and executable specifications
- Clear setup, action, and expected outcome
- Enables automated testing
- Reduces ambiguity in requirements
- Journey coherence keeps related actions together without hiding unrelated outcomes

## Practice 7: Require Write and Bash Tools for Report Generators

**Principle**: Checker agents MUST have both Write and Bash tools in frontmatter.

**Good Example:**

```yaml
---
name: docs-checker
description: Validates documentation quality
tools: [Read, Glob, Grep, Write, Bash]
model: sonnet
---
```

**Bad Example:**

```yaml
---
name: docs-checker
description: Validates documentation quality
tools: [Read, Glob, Grep] # MISSING Write and Bash!
---
```

**Rationale:**

- Write tool creates report files
- Bash tool generates UTC+7 timestamps
- Mandatory for audit report generation
- Consistency across all checker agents
