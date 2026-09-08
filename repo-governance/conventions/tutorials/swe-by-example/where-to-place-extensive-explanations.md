---
description: "Defines the split between what belongs inside code-block annotations (WHAT) versus markdown text sections (WHY), with anti-pattern and correct-pattern examples."
when_to_use: "Read when an annotation is getting too long or explanatory, to decide whether that content belongs in the code block or in a text section instead."
---

# Self-Containment Rules: Where to Place Extensive Explanations

**CRITICAL**: Code block annotations should focus on WHAT the code does and returns. Extensive WHY explanations go in designated markdown text sections.

**Code block purpose** (inside ` ```language ` fence):

- Show WHAT each line does: `x := 10 // => x is now 10 (type: int)`
- Show return values: `result := fn() // => result is "output" (string)`
- Show state changes: `counter++ // => counter is now 5`
- Show outputs: `fmt.Println(x) // => Output: 10`

**Text section purpose** (outside code blocks):

- **Brief Explanation**: WHY this concept matters, WHEN to use it (2-3 sentences)
- **Why It Matters**: Production relevance, comparisons, practical impact (50-100 words)
- **Key Takeaway**: Core insight and common pitfalls (1-2 sentences)

**Anti-pattern** (verbose tutorial-style comments in code):

```go
// Go's goroutines are lightweight threads managed by the Go runtime.
// Unlike OS threads which consume 1MB+ of stack space, goroutines
// start with only 2KB and grow dynamically. This allows Go servers
// to handle 10,000+ concurrent connections on a single machine.
go processRequest(req)  // => Goroutine spawned (runs concurrently)
```

**Correct pattern** (concise code annotations + text sections):

```go
go processRequest(req)  // => Goroutine spawned (runs concurrently with minimal overhead)
```

**Why It Matters**: Goroutines enable servers to handle 10,000+ concurrent connections on a single machine with minimal memory overhead (2KB stack per goroutine vs 1MB+ per thread in Java), making Go the language of choice for high-throughput network services like Kubernetes, Docker, and Prometheus.

**Density control**:

- If code annotations exceed 2.5 density, MOVE explanatory content to text sections
- Keep code annotations focused on state tracking (`// =>` notation)
- Reserve extensive explanations for "Brief Explanation" and "Why It Matters" sections

**Note**: This annotation density standard (1-2.25 per example) is the general ayokoding-www code annotation standard applied to all content. By-example tutorials follow the same standard as other tutorial types, with additional requirements for self-containment and five-part format.
