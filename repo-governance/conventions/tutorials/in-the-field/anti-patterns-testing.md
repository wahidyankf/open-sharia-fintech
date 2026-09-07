---
description: Why the Anti-Patterns section exists, plus the consequences of introducing a testing framework without standard-library foundation.
when_to_use: Use when explaining the risk of teaching a testing framework before its standard-library basis.
---

# Anti-Patterns: Testing Framework Without Foundation

**CRITICAL**: These anti-patterns show the consequences of jumping to frameworks without understanding standard library foundations.

## Anti-Pattern 1: Framework Without Foundation (Testing)

**FAIL: Starting with JUnit without understanding assertions**

```java
// Developer jumps directly to JUnit 5
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

@Test
void testCalculator() {
    Calculator calc = new Calculator();
    // What does assertEquals actually do?
    // When does test fail vs throw exception?
    // Why @Test annotation required?
    assertEquals(5, calc.add(2, 3));
}
```

**Problems**:

- Doesn't understand test execution model (when/how tests run)
- Can't debug test failures (assertion vs exception vs error)
- Doesn't know what @Test annotation does under the hood
- When to optimize: Can't reduce framework overhead because doesn't know what's happening

**PASS: Learning assertions first, then JUnit**

```java
// Step 1: Understand basic assertions (standard library)
assert result == 5 : "Expected 5";
// Now understands: assertion checks boolean, throws if false

// Step 2: Adopt JUnit (framework)
assertEquals(5, result);
// Now understands: assertEquals is assertion with better error messages
// Knows when test fails: assertion throws AssertionFailedError
// Can debug: understands test lifecycle (@BeforeEach, @Test, @AfterEach)
```

**Why standard library first matters**: Understanding `assert` keyword teaches test fundamentals. When JUnit's `assertEquals` fails, developer knows it's throwing specialized exception (AssertionFailedError), not magic. Can optimize by choosing appropriate assertion granularity.
