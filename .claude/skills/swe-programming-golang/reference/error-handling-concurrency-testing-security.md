# Go Quick Standards — Error Handling, Concurrency, Testing, Security

## Error Handling

**Explicit Error Returns**: Always check errors

```go
result, err := doSomething()
if err != nil {
    return fmt.Errorf("operation failed: %w", err)
}
```

**Custom Error Types**: Define for specific cases

```go
type ValidationError struct {
    Field string
    Err   error
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed for %s: %v", e.Field, e.Err)
}
```

**Error Wrapping**: Preserve error chain

```go
return fmt.Errorf("processing user %s: %w", userID, err)
```

## Concurrency

**Goroutines**: Use for concurrent operations

```go
go func() {
    // Concurrent work
}()
```

**Channels**: Use for communication

```go
ch := make(chan Result, 10) // Buffered
ch <- result                // Send
result := <-ch              // Receive
```

**Context**: Use for cancellation and timeouts

```go
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()
```

## Testing Standards

**Table-Driven Tests**: Preferred testing pattern

```go
tests := []struct {
    name     string
    input    int
    expected int
}{
    {"positive", 5, 10},
    {"zero", 0, 0},
    {"negative", -5, -10},
}

for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        result := double(tt.input)
        if result != tt.expected {
            t.Errorf("got %d, want %d", result, tt.expected)
        }
    })
}
```

**Test Helpers**: Use `t.Helper()` for helper functions

```go
func assertEqual(t *testing.T, got, want any) {
    t.Helper()
    if got != want {
        t.Errorf("got %v, want %v", got, want)
    }
}
```

## Security Practices

**Input Validation**: Validate all external input

- Check bounds, formats, and types
- Reject invalid input early

**SQL Injection**: Use parameterized queries

```go
rows, err := db.Query("SELECT * FROM users WHERE id = ?", userID)
```

**Context Timeouts**: Always set timeouts

```go
ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
defer cancel()
```
