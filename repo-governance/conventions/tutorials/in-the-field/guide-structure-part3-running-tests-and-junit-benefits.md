---
description: How to run JUnit 5 tests via Maven and why JUnit 5 is the production-standard testing framework.
when_to_use: Use when documenting how to run tests or justifying JUnit 5 over the standard library.
---

# Guide Structure Part 3: Running Tests and JUnit 5 Benefits

**Running tests**:

```bash
mvn test
# => Compiles test code in src/test/java
# => Runs all @Test methods via Surefire plugin
# => Reports: passed, failed, skipped
# => Exit code 0 if all pass, non-zero if failures
# => Generates reports in target/surefire-reports/
```

**WHY JUNIT 5**:

- Organized test structure (no main method required)
- Rich assertion library (assertEquals, assertThrows, assertTimeout)
- Test lifecycle hooks (@BeforeEach, @AfterEach, @BeforeAll, @AfterAll)
- Parameterized tests (@ParameterizedTest)
- Build tool integration (Maven, Gradle)
- IDE support (IntelliJ, Eclipse, VS Code)
- Trade-off: External dependency (2MB) vs assertion simplicity
