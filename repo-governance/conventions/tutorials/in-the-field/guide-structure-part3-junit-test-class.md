---
title: "Guide Structure Part 3: JUnit 5 Test Class Example"
description: The worked production JUnit 5 test class example with lifecycle annotations and assertions.
when_to_use: Use when writing a JUnit 5 production test class example.
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - in-the-field
  - education
  - production-ready
created: 2026-02-04
---

# Guide Structure Part 3: JUnit 5 Test Class Example

```java
import org.junit.jupiter.api.*;
// => JUnit 5 API (org.junit.jupiter.api package)
// => Includes @Test, @BeforeEach, @AfterEach annotations
import static org.junit.jupiter.api.Assertions.*;
// => Static import for assertion methods
// => assertEquals, assertThrows, assertTrue, etc.
// => JUnit 5 testing framework
// => Provides test lifecycle and assertions
// => Industry standard (89% of Java projects)

class CalculatorTest {
    // => Test class naming: [ClassName]Test
    // => Must be in test source directory (src/test/java)
    // => Package-private visibility (no modifier needed)
    // => JUnit doesn't require public modifier
    // => Same package as Calculator class

    private Calculator calculator;
    // => Instance field shared across tests
    // => Reset before each test (test isolation)
    // => Not static (new instance per test)

    @BeforeEach
    void setUp() {
        // => Runs before each test method
        // => Creates fresh Calculator instance
        // => Annotation from org.junit.jupiter.api
        // => Test isolation pattern (clean state)

        calculator = new Calculator();
        // => Ensures test isolation
        // => Each test gets clean state
        // => No shared state between tests
    }

    @Test
    void add_shouldReturnSum() {
        // => Test method naming: [method]_should[Behaviour]
        // => @Test annotation marks test method
        // => JUnit discovers and runs this method
        // => Must be void, no parameters
        // => Package-private or public visibility

        int result = calculator.add(2, 3);
        // => result is 5
        // => Invokes method under test
        // => Arrange-Act-Assert pattern (Act phase)

        assertEquals(5, result, "2 + 3 should equal 5");
        // => Assertion: expected value first, actual second
        // => Third parameter: failure message (shown on failure)
        // => Throws AssertionFailedError if values differ
        // => Test passes if no exception thrown
        // => Better error messages than assert keyword
    }

    @Test
    void divide_shouldThrowOnZeroDivisor() {
        // => Test exception handling
        // => Verifies correct error behaviour
        // => Negative test case (error path)

        assertThrows(ArithmeticException.class, () -> {
            calculator.divide(10, 0);
        });
        // => Passes if lambda throws ArithmeticException
        // => Fails if different exception or no exception
        // => Lambda syntax for deferred execution
        // => Captures exception for inspection
    }

    @AfterEach
    void tearDown() {
        // => Runs after each test method
        // => Cleanup resources if needed
        // => Always executes (even if test fails)

        calculator = null;
        // => Release reference (GC eligible)
        // => Optional for simple objects
    }
    // => JUnit manages test lifecycle
    // => Test runner discovers @Test methods
    // => Reports: passed, failed, skipped
}
```
