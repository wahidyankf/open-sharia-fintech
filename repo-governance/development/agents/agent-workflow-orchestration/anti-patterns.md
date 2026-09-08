---
description: "Lists orchestration anti-patterns: pushing through when lost, premature completion, context bloat, and vague lessons."
when_to_use: Use when reviewing an agent's workflow for common orchestration mistakes.
---

# Anti-Patterns

## Pushing Through When Lost

**Problem**: Continuing to implement when the approach is clearly not working, hoping it resolves itself.

**Why it fails**: Each step based on a flawed premise compounds the problem. Re-planning from a known-good state is always faster than accumulating a chain of adjustments to a broken foundation.

**Fix**: Stop. Re-plan. State explicitly what assumption failed and what the revised approach is.

## Premature Completion

**Problem**: Declaring a task done when tests pass, without verifying the actual behaviour.

**Why it fails**: Tests are necessary but not sufficient. Verification requires demonstrating that the correct behaviour is present, not just that no existing test fails.

**Fix**: After tests pass, demonstrate the behaviour directly. Read the output. Confirm it matches the requirement.

## Context Bloat

**Problem**: Conducting extensive research and exploration in the main context rather than using delegated agents.

**Why it fails**: The main context fills with details that were needed for the research but are not needed for the decision. This degrades the quality of subsequent reasoning.

**Fix**: Offload research to delegated agents. Return only the findings needed to make the decision.

## Vague Lessons

**Problem**: Writing lessons that describe the mistake in general terms without specifying a concrete preventive action.

**Why it fails**: A vague lesson is easy to write and easy to ignore. When the same situation arises, the lesson provides no actionable check.

**Fix**: Write rules that name the specific trigger and the specific check. Test the rule against the original failure: "Would this rule have prevented the mistake?"
