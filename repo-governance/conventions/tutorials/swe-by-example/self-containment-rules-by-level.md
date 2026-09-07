---
description: "Defines the self-containment requirements for beginner, intermediate, and advanced examples, and the acceptable vs unacceptable forms of cross-referencing between examples."
when_to_use: "Read when deciding how much a given example may assume from earlier examples, or when checking whether a cross-reference is acceptable."
---

# Self-Containment Rules by Level

**Critical requirement**: Examples must be copy-paste-runnable within their chapter scope.

## Beginner Level Self-Containment

**Rule**: Each example is completely standalone

**Requirements**:

- Full package declaration and imports
- All helper functions defined in-place
- No references to previous examples
- Runnable with single command (go run, iex, java, etc.)

**Example structure**:

```go
package main

import (
    "fmt"
    "strings"
)

// Helper function defined inline
func helper(s string) string {
    return strings.ToUpper(s)
}

func main() {
    result := helper("go")  // => result is "GO"
    fmt.Println(result)     // => Output: GO
}
```

## Intermediate Level Self-Containment

**Rule**: Examples assume beginner concepts but include all necessary code

**Allowed assumptions**:

- Reader knows basic syntax (covered in beginner)
- Reader understands fundamental types and control flow
- Reader can run basic commands

**Requirements**:

- Full imports and necessary helper code
- Can reference beginner concepts conceptually ("as we saw with slices")
- Must be runnable without referring to previous examples
- Include type definitions and setup code needed

## Advanced Level Self-Containment

**Rule**: Examples assume beginner + intermediate knowledge but remain runnable

**Allowed assumptions**:

- Reader knows language fundamentals and production patterns
- Reader understands framework basics and architecture
- Reader can navigate documentation for context

**Requirements**:

- Full runnable code with imports and setup
- Can reference patterns by name ("using the middleware pattern")
- Include all interfaces, types, and configurations needed
- Provide complete example even if building on earlier concepts

## Cross-Reference Guidelines

**Acceptable cross-references**:

```markdown
This builds on the middleware pattern from Example 30, but here's the complete code including the middleware setup...
```

**Unacceptable cross-references**:

```markdown
Use the `handleRequest` function from Example 12 (code not shown).
```

**Golden rule**: If you delete all other examples, this example should still compile and run.
