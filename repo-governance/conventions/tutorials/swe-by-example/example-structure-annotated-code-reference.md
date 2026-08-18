---
title: "Example Structure: Part 3 Annotated Code Reference Example"
description: "Provides a production-quality reference example of heavily annotated code with measured density, plus the required annotation and code-organization checklists."
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - by-example
  - education
  - code-first
created: 2025-12-25
when_to_use: "Read when you need a worked reference for measuring annotation density on a real code block, or the required-annotations and code-organization checklists."
---

# Example Structure: Part 3 Annotated Code Reference Example

## Production Example and Required Annotations

**Production example from ayokoding-www** (Golang Example 1):

```go
package main // => Declares this is the main executable package
             // => "main" is special - it tells the compiler to create an executable
             // => Other package names (like "utils") create libraries, not executables

import (
    "fmt" // => Import formatting package from standard library
          // => fmt provides I/O formatting functions (Printf, Println, Sprintf, etc.)
          // => Standard library packages are always available, no installation needed
)

func main() { // => Entry point - every executable needs main() in main package
              // => Go runtime calls main() when program starts
              // => No parameters, no return value (unlike C/Java's int main)
              // => Program exits when main() returns

    fmt.Println("Hello, World!") // => Println writes to stdout and adds newline
                                  // => Returns (n int, err error) but we ignore them here
                                  // => n is bytes written, err is write error (if any)
                                  // => Equivalent to: fmt.Fprintln(os.Stdout, "Hello, World!")
    // => Output: Hello, World!
}
```

**Annotation density**: 7 code lines, 15 comment lines = **2.14 density** (within 1-2.25 target)

**Required annotations**:

- **Annotation density**: 1-2.25 lines of comment per line of code
- **Pattern matching**: Document which branch matched and why
- **Execution flow**: Show control flow decisions (which if/case branch taken)

- **Variable states**: Show value and type after assignment
- **Intermediate values**: Document values at each transformation step
- **Function outputs**: Show return values inline
- **Side effects**: Document mutations, I/O operations, state changes
- **Expected outputs**: Show stdout/stderr content with `=> Output:` prefix
- **Timing (compile vs runtime)**: Distinguish compile-time checks from runtime execution
- **Best practices**: Use PASS: GOOD vs FAIL: BAD indicators for pattern comparisons
- **Error cases**: Document when errors occur and how they're handled

**Code organization**:

- Include full imports (no "assume this is imported")
- Define helper functions if needed for self-containment
- Use descriptive variable names (avoid single-letter unless idiomatic)
- Format code with language-standard tools (gofmt, mix format, etc.)
