---
title: "Proactive Preexisting Error Resolution — Expected Behavior"
description: The five-step response to a discovered preexisting error - diagnose, fix, verify, scope, and communicate
category: explanation
subcategory: development
tags:
  - root-cause
  - quality
  - preexisting-errors
  - proactive
  - bug-fixing
  - ai-agents
created: 2026-03-28
when_to_use: Use when you've decided to fix a discovered preexisting error and need to know the steps to take.
---

# Expected Behavior

## 1. Diagnose

Before touching anything, understand the root cause of the preexisting error. Read the relevant code, test output, or configuration. Do not guess. Do not assume the fix is obvious without verification.

## 2. Fix

Apply a proper root cause fix. Not a workaround. Not a suppression. Not a TODO comment.

## 3. Verify

Confirm the fix works. Run the affected tests. Check that the configuration loads correctly. Verify the link resolves. Evidence of a working fix is required before proceeding.

## 4. Scope

If the fix is small enough to complete within a few minutes, fix it inline as part of your current work. If it requires its own commit for clarity, make a separate commit with a descriptive commit message explaining the preexisting bug that was resolved.

If the fix is too large to address within the current session — an architectural issue or a systemic problem — create a plan and begin executing it. Do not defer it to "someday." A plan that gets executed is categorically different from a noted issue that sits in a backlog.

## 5. Communicate

Explain what was found and what was fixed. Transparency is not optional. The communication belongs in the commit message, PR description, or conversation — wherever the context lives.
