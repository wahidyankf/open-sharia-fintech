---
description: Part 2 requirements plus the worked standard-library testing example (Java assert keyword) and its limitations.
when_to_use: Use when writing the standard-library testing example for a Part 2 section.
---

# Guide Structure Part 2: Standard Library First — Testing Example

**Purpose**: Teach fundamentals before introducing frameworks

**Must include**:

- Standard library/built-in approach with code example
- Annotation density: 1.0-2.25 per code line (same as by-example)
- Explanation of how standard approach works
- Limitations that motivate framework adoption
- Multiple comprehensive examples showing progression

**Example 1: Basic Testing with Standard Library**

````markdown
## Built-in Testing with Standard Library

Java provides the `assert` keyword for runtime assertions that verify program correctness.

**Pattern**:

```java
public class Calculator {
    // => Simple calculator for demonstration
    // => No external dependencies

    public int add(int a, int b) {
        return a + b;
        // => Returns sum of two integers
    }

    public static void main(String[] args) {
        // => main() serves as test runner
        // => Must enable assertions with -ea flag

        Calculator calc = new Calculator();
        // => Creates calculator instance

        int result = calc.add(2, 3);
        // => result is 5
        // => Invokes add method

        assert result == 5 : "Expected 2 + 3 = 5, got " + result;
        // => Assertion passes (no exception)
        // => If false, throws AssertionError with message
        // => Assertions disabled by default (no-op)

        System.out.println("All assertions passed!");
        // => Output: All assertions passed!
        // => Only printed if assertion didn't throw
    }
}
```
````

**Enabling assertions**: Assertions disabled by default. Enable with `-ea` flag.

```bash
java -ea Calculator  # => Assertions enabled
java Calculator      # => Assertions disabled (default, no checks)
```

**Limitations for production testing**:

- No test organization (all tests in main method)
- No reporting (just exceptions or silence)
- Manual execution (no test runner, no automation)
- No assertions library (limited built-in assertions)
- No test isolation (shared state between assertions)
- No parameterized tests (must copy-paste for variants)
