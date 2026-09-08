---
title: "Java Testing Standards"
description: Authoritative OSE Platform Java testing standards — the Cucumber Unit adapter, MockMvc boundaries, and JaCoCo coverage enforcement
category: explanation
subcategory: prog-lang
tags:
  - java
  - testing-standards
  - cucumber
  - bdd
  - jacoco
  - coverage
  - mockmvc
principles:
  - automation-over-manual
  - explicit-over-implicit
  - pure-functions
  - reproducibility
created: 2026-09-08
---

# Java Testing Standards

## Prerequisite Knowledge

**REQUIRED**: You MUST understand Java fundamentals from the [AyoKoding Java Learning Path](../../../../../apps/ayokoding-www/content/en/learn/legacy/software-engineering/programming-languages/java/_index.md) before using these standards.

**This document is OSE Platform-specific**, not a JUnit or Cucumber tutorial. We define HOW this repository tests Java, not WHAT a test framework is.

**See**: [Programming Language Documentation Separation Convention](../../../../../repo-governance/conventions/structure/programming-language-docs-separation.md)

## The Contract Java Tests Satisfy

Java projects are bound by the repository-wide [BDD contract](../../../../../repo-governance/development/behaviour-driven-development.md) and [TDD workflow](../../../../../repo-governance/development/workflow/test-driven-development.md), unchanged. Nothing on this page relaxes them; it states how they are met in Java.

Three obligations carry over verbatim:

1. **Gherkin first.** The scenario is written in the owning `specs/` corpus before the binding exists.
2. **Unit always.** Every scenario is bound in the Unit adapter, whatever else binds it.
3. **A bug fix ships with a regression test** that fails before the fix.

## Cucumber-JVM Is the Unit Adapter

Java's Unit adapter is Cucumber-JVM on the JUnit Platform, with `cucumber-spring` supplying the application context.

- One suite class per project (`RunCucumberTest`) is the JUnit Platform entry point.
- One `@CucumberContextConfiguration` class configures the context, and only one — Cucumber fails at startup if a second appears.
- Step definitions live under `steps/`, one class per coherent group of scenarios.

Step definitions use Cucumber expressions in `@Given` / `@When` / `@Then` annotations, and Cucumber-JVM resolves a step only against its own keyword. A `@When` step and a `@Then` step may share identical text without colliding; this is a real difference from the TypeScript adapter, where keyword is not part of resolution.

The repository's static coverage validator reads `.java` step definitions directly, so an unbound scenario or an unused binding is a build failure in `test:quick`, not something a reader has to notice.

## Assert at the HTTP Boundary With MockMvc

HTTP behaviour is asserted through MockMvc — in-process, no bound port, no started server.

This is a deliberate boundary choice. MockMvc exercises the real routing, the real serialization, and the real status-code selection, which is where controller defects actually live. It does not exercise the network, the process launcher, or the port resolution, and it should not pretend to: those belong to the E2E adapter, which starts the built artifact as a real process.

Do not add a `@SpringBootTest(webEnvironment = RANDOM_PORT)` variant to "be closer to production." It is slower, it is flakier, and the thing it adds is already covered one layer up.

## What a Test Must Not Do

- **Never sleep.** A test that needs a sleep to pass is a test with a race in it. Fix the race.
- **Never retry.** Retrying converts a real defect into an intermittent one.
- **Never widen an assertion to make it pass.** `status().is2xxSuccessful()` where the scenario says 200 is a weakened test, not a robust one.
- **Never skip or quarantine.** A flaky test is a defect and is fixed at its [root cause](../../../../../repo-governance/development/workflow/test-driven-development/flaky-tests-are-defects.md).

## Coverage Is Enforced, Not Reported

JaCoCo runs `jacocoTestCoverageVerification` as part of the unit-test target, and the build fails below the declared line-coverage floor. The floor is high on purpose: this is a small service, and on a small service anything less than near-total coverage means whole endpoints are untested.

Two rules keep that floor honest:

- **Do not exclude a class to reach the floor.** An exclusion is a decision that the class will never be tested; it needs a written reason in `build.gradle.kts`, not a quiet entry in an exclusion list.
- **Do not write a test whose only purpose is to execute a line.** Coverage is a symptom of testing behaviour, not a target to satisfy directly. A test that calls a getter and asserts nothing raises the number and lowers the value.

## Test Naming

Test and step-definition method names describe the behaviour, not the mechanism:

```java
// Good — a reader learns what the system does
public void aHealthRequestReturnsOk() {}

// Bad — a reader learns which method was called
public void testHealthController1() {}
```

Cucumber step methods take their meaning from the annotation text; the method name still matters, because it is what appears in a stack trace.

## Related Documentation

- [Java Overview](./README.md)
- [Java Coding Standards](./coding-standards.md)
- [Behaviour-Driven Development](../../../../../repo-governance/development/behaviour-driven-development.md)
- [Test-Driven Development](../../../../../repo-governance/development/workflow/test-driven-development.md)
