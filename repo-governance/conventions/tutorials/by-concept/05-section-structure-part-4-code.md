---
title: "Section Structure: Heavily Annotated Code Examples (Part 4)"
description: "Specifies the heavily annotated code examples part of the six-part concept-section structure, including annotation density and required annotation types."
when_to_use: "Read when drafting or reviewing the annotated code example inside a By-Concept tutorial section."
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - by-concept
  - education
  - narrative-driven
created: 2026-01-30
---

# Section Structure: Heavily Annotated Code Examples (Part 4)

## Part 4: Heavily Annotated Code Examples (1-5 examples)

**Core requirement**: Every significant line must have an inline comment

**Annotation density**: 1.0-2.25 lines of comment for every line of code (same as by-example)

**Comment annotations use `// =>` or `# =>` notation**:

```go
ch := make(chan int)             // => ch is unbuffered channel (blocks on send until receive)
                                  // => Type: chan int (channel of integers)

go func() {                       // => Spawn goroutine (runs concurrently)
    ch <- 42                      // => Send 42 to channel (blocks until main receives)
}()                               // => Goroutine now running in background

value := <-ch                     // => Receive from channel (blocks until goroutine sends)
                                  // => value is 42
fmt.Println(value)                // => Output: 42
```

**Required annotations**:

- **Variable states**: Show value and type after assignment
- **Execution flow**: Show which branch executes and why
- **Side effects**: Document mutations, I/O operations, state changes
- **Expected outputs**: Show stdout/stderr content with `=> Output:` prefix
- **Timing (compile vs runtime)**: Distinguish compile-time checks from runtime execution
- **Best practices**: Use PASS: GOOD vs FAIL: BAD indicators for pattern comparisons

**Code organization**:

- Include full imports (no "assume this is imported")
- Define helper functions if needed for clarity
- Use descriptive variable names
- Format code with language-standard tools (gofmt, mix format, etc.)
