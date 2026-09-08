---
description: The three-step Red/Green/Refactor loop every code change follows under TDD.
when_to_use: Use as the canonical definition of the Red-Green-Refactor loop before implementing any code change.
---

# The Red-Green-Refactor Cycle

Every code change follows this loop:

1. **Red** — Write a failing test that captures the desired behaviour. Run it and confirm it fails
   for the right reason (not due to a syntax error, missing import, or wrong test setup). A test
   that fails for the wrong reason is not a useful test.
2. **Green** — Write the minimum production code that makes the failing test pass without a
   hardcoded outcome, literal-success sentinel, or production bypass. Do not add behaviour beyond
   what the scenario requires.
3. **Refactor** — With all tests green, improve the implementation: remove duplication, improve
   names, extract functions, apply clean-code principles. Tests must remain green after every
   refactor step. If they go red during refactoring, that is a bug introduced by the refactor, not
   a deliberate failure.

Repeat the cycle for the next behaviour and applicable adapter.

## A new harness needs its own red

Step 1 covers the test case. It does not cover the **harness** the case runs inside — a new E2E
driver, a fixture that starts a real process, a runner wired up after the code already worked.
There the loop has to be run deliberately in reverse: mutate the production code so the assertion
must fail, watch the suite go red, then revert. A harness that has never been observed red is an
untested claim, and the ways it can be permanently green are not exotic — asserting against a
process it did not start, resolving a stale build, or binding zero scenarios all produce a
confident pass. Capture the red run as the evidence, not the green one; the green run is what a
broken harness also produces.

**Enforcement**: **unenforced by decision.** Nothing distinguishes a harness that was driven red
from one that never was — the artefact of a demonstrated red is a deleted mutation. The nearest
mechanical support is the behaviour-coverage validator, which fails a suite binding zero scenarios;
the rest stays with the author and reviewer.
