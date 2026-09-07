---
description: "Reference patterns for annotating output, state changes, collections, and concurrency using the `// =>` notation."
when_to_use: "Read when writing `// =>` style annotations for outputs, state, collections, or goroutine/channel concurrency and you need a worked pattern to follow."
---

# Annotation Patterns Reference

## Output Annotation Pattern

Use `// =>` or `# =>` to show outputs, states, and intermediate values:

```go
// Variable assignment
age := 25                        // => age is 25 (type: int)

// Transformation
doubled := age * 2               // => doubled is 50 (age still 25)

// Function call with return
greeting := fmt.Sprintf("Age: %d", doubled)
                                 // => greeting is "Age: 50" (string)

// Output to stdout
fmt.Println(greeting)            // => Output: Age: 50

// Multiple returns
result, err := parseValue("42")  // => result is 42, err is nil

// Error case
result, err := parseValue("bad") // => result is 0, err is "invalid input"
```

## State Documentation Pattern

Show how state changes through execution:

```go
// Initial state
counter := 0                     // => counter is 0

// First increment
counter++                        // => counter is now 1

// Conditional modification
if counter > 0 {
    counter *= 10                // => counter is now 10 (condition was true)
}

// Final state
fmt.Println(counter)             // => Output: 10
```

## Collection Annotation Pattern

Show collection contents at each step:

```go
// Initialize
nums := []int{1, 2, 3}           // => nums is [1, 2, 3] (len=3, cap=3)

// Append
nums = append(nums, 4)           // => nums is [1, 2, 3, 4] (len=4, cap=6)

// Slice
subset := nums[1:3]              // => subset is [2, 3] (len=2, cap=5)
                                 // => nums unchanged: [1, 2, 3, 4]

// Modify slice
subset[0] = 99                   // => subset is [99, 3]
                                 // => nums is [1, 99, 3, 4] (backing array shared!)
```

## Concurrency Annotation Pattern

Document goroutine execution and channel operations:

```go
// Channel creation
ch := make(chan int)             // => ch is unbuffered channel (blocks on send until receive)

// Goroutine spawn
go func() {
    ch <- 42                     // => Blocks until main goroutine receives
}()                              // => Goroutine now running concurrently

// Receive
value := <-ch                    // => Blocks until goroutine sends, then value is 42
fmt.Println(value)               // => Output: 42
```
