---
name: swe-programming-java
description: Java coding standards from authoritative docs/explanation/software-engineering/programming-languages/java/ documentation
---

# Java Coding Standards

## Purpose

Progressive disclosure of Java coding standards for agents writing Java code.

**Authoritative Source**: [docs/explanation/software-engineering/programming-languages/java/README.md](../../../docs/explanation/software-engineering/programming-languages/java/README.md)

**Usage**: Auto-loaded for agents when writing Java code. Provides quick reference to the platform's conventions, testing contract, and error-handling rules.

## Scope

Java is active for exactly one project — `ose-lms-be`, the Learning Management System backend. It is **not** the default for new backends; that remains F#. Introducing Java elsewhere needs its own recorded decision.

## Prerequisite Knowledge

**IMPORTANT**: This skill provides **OSE Platform-specific style guides**, not educational tutorials.

**You MUST understand Java fundamentals before using these standards.** Complete the AyoKoding Java learning path first:

1. **[Java Learning Path](../../../apps/ayokoding-www/content/en/learn/legacy/software-engineering/programming-languages/java/_index.md)** - Initial setup, language overview, quick start
2. **[Java By Example](../../../apps/ayokoding-www/content/en/learn/legacy/software-engineering/programming-languages/java/by-example/)** - Annotated code examples, beginner to advanced

**What this skill covers**: OSE Platform naming conventions, framework choices, repository-specific patterns, how to apply Java knowledge in THIS codebase.

**What this skill does NOT cover**: Java syntax, language fundamentals, Spring tutorials, generic patterns (those are in ayokoding-web).

**See**: [Programming Language Documentation Separation](../../../repo-governance/conventions/structure/programming-language-docs-separation.md) for content separation rules.

## Quick Standards Reference

- **Formatting is not a judgement call.** Spotless with google-java-format runs on commit and is verified in CI. Never suppress it per file; never mix a reformat into a behavioural change.
- **Package by feature, not by layer.** Root `com.oseplatform.<product>`, then `health/`, `hello/`. `config/` is the one layer-named package allowed.
- **Prefer `record` and `final`.** A setter on a domain type invites a defect.
- **Constructor injection only.** Never field `@Autowired` — it defeats `final`, hides unsatisfiable dependencies until first use, and forces a framework boot to test.
- **Keep decisions out of the framework.** Anything worth testing goes in a class with no Spring imports, so its test starts no context. `PortResolver` is the reference example.
- **Declare configuration you depend on**, even where the default already matches — Spring Boot defaults move between majors. Actuator exposure is declared narrowly and asserted by a test.
- **Fail fast on misconfiguration.** A malformed port override stops startup; it never falls back to the default.
- **Catch narrowly, chain the cause, never catch `Throwable`.** Never swallow.
- **Nothing internal reaches a client.** No stack traces, class names, paths, hostnames, or configuration values in an error response.

## Testing Contract

Java satisfies the repository-wide BDD and TDD contracts unchanged: Gherkin first, Unit always, a regression test with every bug fix.

- **Cucumber-JVM on the JUnit Platform** is the Unit adapter, with `cucumber-spring` supplying the context. One suite class and exactly one `@CucumberContextConfiguration` per project.
- Cucumber-JVM resolves a step **only against its own keyword**, so a `@When` and a `@Then` may share identical text — unlike the TypeScript adapter.
- **MockMvc** is the HTTP assertion boundary: real routing and serialization, no bound port. Process-level behaviour belongs to E2E.
- **JaCoCo verification fails the build** below the declared line floor. Never exclude a class to reach it, and never write a test whose only effect is to execute a line.
- Never sleep, retry, widen an assertion, skip, or quarantine. A flaky test is a defect.

## Comprehensive Documentation

**Authoritative Index**: [docs/explanation/software-engineering/programming-languages/java/README.md](../../../docs/explanation/software-engineering/programming-languages/java/README.md)

1. **[Coding Standards](../../../docs/explanation/software-engineering/programming-languages/java/coding-standards.md)** - Naming, package layout, records, controllers, configuration
2. **[Testing Standards](../../../docs/explanation/software-engineering/programming-languages/java/testing-standards.md)** - Cucumber Unit adapter, MockMvc boundary, JaCoCo enforcement
3. **[Error Handling Standards](../../../docs/explanation/software-engineering/programming-languages/java/error-handling-standards.md)** - Exception boundaries, fail-fast startup, what a client never sees

## Related Skills

- docs-applying-content-quality
- repo-practicing-trunk-based-development

## References

- [Java README](../../../docs/explanation/software-engineering/programming-languages/java/README.md)
- [Behaviour-Driven Development](../../../repo-governance/development/behaviour-driven-development.md)
