---
title: "Proactive Preexisting Error Resolution — The Three Anti-Patterns"
description: Acting ignorant, monkey-patching, and passive mentioning - the three failure patterns for handling preexisting errors, each with worked examples and the correct alternative
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
when_to_use: Use when reviewing your own response to a discovered preexisting error for one of these three failure patterns.
---

# The Three Anti-Patterns

## Anti-Pattern 1: Acting Ignorant

Seeing broken state and proceeding as if it does not exist.

**Example**: A CI test has been failing intermittently for two weeks. You re-run the pipeline three times hoping the flake clears. It clears. You move on without investigating why the test fails.

**What happened**: The root cause — a race condition in the test setup — remains. The next CI run will fail again. The next developer will re-run it three times too.

**What to do instead**: Read the test output. Understand the actual failure mode. Fix the test or the code it tests. Verify locally. Commit the fix.

---

**Example**: You open a file to add a feature and notice a broken import reference from a previous refactor. The import is unused in the code path you are touching. You add your feature and ignore the broken import.

**What to do instead**: Fix the broken import. It takes thirty seconds and it removes a latent error before it causes a runtime failure.

## Anti-Pattern 2: Monkey-Patching

Working around the problem instead of solving it.

**Example**: An upstream API contract changed and now a call throws an exception on certain inputs. You wrap the call in a `try/catch` that swallows the exception and returns a default value. The contract mismatch remains; the error is now hidden.

**What to do instead**: Update the contract, fix the call site, and regenerate types if applicable. The swallowed exception will resurface as a data integrity problem downstream.

---

**Example**: A configuration file has an incorrect base URL that causes integration tests to fail. You hardcode the correct URL in the test setup to make the tests pass.

**What to do instead**: Fix the configuration file. The incorrect base URL will break other consumers of that configuration in production.

## Anti-Pattern 3: Passive Mentioning

Noting the problem without taking action.

**Example**: A PR description contains: "Note: I noticed the validation function in `user-service.ts` has a bug where empty strings pass validation. This is pre-existing and unrelated to this PR."

**What happened**: The bug is now documented and still present. The reviewer reads the note, acknowledges it, and merges. The bug is added to a backlog where it waits indefinitely.

**What to do instead**: Fix the validation function. Add a test that covers the empty string case. Include it in the same PR or a separate commit within the same session with a clear commit message explaining the preexisting bug that was found.
