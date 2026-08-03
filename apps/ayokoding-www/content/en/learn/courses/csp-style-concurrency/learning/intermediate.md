---
title: "Intermediate Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 20
---

### Example 27: Once Init

_ex-27 · exercises co-14, co-16_

This CSP example is rendered verbatim from `learning/code/ex-27-once-init/main.go`.

```go
package main

import (
  // once init: this operation makes initialization, cancellation, or shared access explicit.
  "fmt"
  // once init: this operation makes initialization, cancellation, or shared access explicit.
  "sync"
)

// once init: this operation makes initialization, cancellation, or shared access explicit.
func main() {
  // once init: this operation makes initialization, cancellation, or shared access explicit.
  var once sync.Once
  // once init: this operation makes initialization, cancellation, or shared access explicit.
  value := 0
  // once init: this operation makes initialization, cancellation, or shared access explicit.
  for range 4 {
    // once init: this operation makes initialization, cancellation, or shared access explicit.
    go once.Do(func() { value = 42 })
  }
  // once init: this operation makes initialization, cancellation, or shared access explicit.
  once.Do(func() { value = 99 })
  // once init: this operation makes initialization, cancellation, or shared access explicit.
  fmt.Println("initialized", value)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 28: Sync Map

_ex-28 · exercises co-14, co-16_

This CSP example is rendered verbatim from `learning/code/ex-28-sync-map/main.go`.

```go
package main

import (
  // sync map: this operation makes initialization, cancellation, or shared access explicit.
  "fmt"
  // sync map: this operation makes initialization, cancellation, or shared access explicit.
  "sync"
)

// sync map: this operation makes initialization, cancellation, or shared access explicit.
func main() {
  // sync map: this operation makes initialization, cancellation, or shared access explicit.
  var values sync.Map
  // sync map: this operation makes initialization, cancellation, or shared access explicit.
  values.Store("region", "eu")
  // sync map: this operation makes initialization, cancellation, or shared access explicit.
  value, ok := values.Load("region")
  // sync map: this operation makes initialization, cancellation, or shared access explicit.
  fmt.Println(value, ok)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 29: Atomic Counter

_ex-29 · exercises co-14, co-16_

This CSP example is rendered verbatim from `learning/code/ex-29-atomic-counter/main.go`.

```go
package main

import (
  // atomic counter: this operation makes initialization, cancellation, or shared access explicit.
  "fmt"
  // atomic counter: this operation makes initialization, cancellation, or shared access explicit.
  "sync"
  // atomic counter: this operation makes initialization, cancellation, or shared access explicit.
  "sync/atomic"
)

// atomic counter: this operation makes initialization, cancellation, or shared access explicit.
func main() {
  // atomic counter: this operation makes initialization, cancellation, or shared access explicit.
  var n int64
  // atomic counter: this operation makes initialization, cancellation, or shared access explicit.
  var wg sync.WaitGroup
  // atomic counter: this operation makes initialization, cancellation, or shared access explicit.
  for range 10 {
    // atomic counter: this operation makes initialization, cancellation, or shared access explicit.
    wg.Add(1)
    // atomic counter: this operation makes initialization, cancellation, or shared access explicit.
    go func() { defer wg.Done(); atomic.AddInt64(&n, 1) }()
  }
  // atomic counter: this operation makes initialization, cancellation, or shared access explicit.
  wg.Wait()
  // atomic counter: this operation makes initialization, cancellation, or shared access explicit.
  fmt.Println(n)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 30: Context Withcancel

_ex-30 · exercises co-14, co-16_

This CSP example is rendered verbatim from `learning/code/ex-30-context-withcancel/main.go`.

```go
package main

import (
  // context withcancel: this operation makes initialization, cancellation, or shared access explicit.
  "context"
  // context withcancel: this operation makes initialization, cancellation, or shared access explicit.
  "fmt"
)

// context withcancel: this operation makes initialization, cancellation, or shared access explicit.
func main() {
  // context withcancel: this operation makes initialization, cancellation, or shared access explicit.
  ctx, cancel := context.WithCancel(context.Background())
  // context withcancel: this operation makes initialization, cancellation, or shared access explicit.
  cancel()
  // context withcancel: this operation makes initialization, cancellation, or shared access explicit.
  <-ctx.Done()
  // context withcancel: this operation makes initialization, cancellation, or shared access explicit.
  fmt.Println(ctx.Err())
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 31: Context Cancel Propagation

_ex-31 · exercises co-14, co-16_

This CSP example is rendered verbatim from `learning/code/ex-31-context-cancel-propagation/main.go`.

```go
package main

import (
  // context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
  "context"
  // context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
  "fmt"
)

// context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
func main() { // A parent cancellation reaches every child context.
  // context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
  parent, cancel := context.WithCancel(context.Background())
  // context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
  a, _ := context.WithCancel(parent)
  // context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
  b, _ := context.WithCancel(parent)
  // context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
  cancel()
  // context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
  <-a.Done()
  // context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
  <-b.Done()
  // context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
  if a.Err() != context.Canceled || b.Err() != context.Canceled {
    // context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
    panic("cancel did not cascade")
  }
  // context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
  fmt.Println("both children canceled")
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 32: Context Withtimeout

_ex-32 · exercises co-14, co-16_

This CSP example is rendered verbatim from `learning/code/ex-32-context-withtimeout/main.go`.

```go
package main

import (
  // context withtimeout: this operation makes initialization, cancellation, or shared access explicit.
  "context"
  // context withtimeout: this operation makes initialization, cancellation, or shared access explicit.
  "fmt"
  // context withtimeout: this operation makes initialization, cancellation, or shared access explicit.
  "time"
)

// context withtimeout: this operation makes initialization, cancellation, or shared access explicit.
func main() { // A timeout reports DeadlineExceeded rather than Canceled.
  // context withtimeout: this operation makes initialization, cancellation, or shared access explicit.
  ctx, cancel := context.WithTimeout(context.Background(), time.Millisecond)
  // context withtimeout: this operation makes initialization, cancellation, or shared access explicit.
  defer cancel()
  // context withtimeout: this operation makes initialization, cancellation, or shared access explicit.
  <-ctx.Done()
  // context withtimeout: this operation makes initialization, cancellation, or shared access explicit.
  if ctx.Err() != context.DeadlineExceeded {
    // context withtimeout: this operation makes initialization, cancellation, or shared access explicit.
    panic(ctx.Err())
  }
  // context withtimeout: this operation makes initialization, cancellation, or shared access explicit.
  fmt.Println("deadline exceeded")
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 33: Context Withdeadline

_ex-33 · exercises co-14, co-16_

This CSP example is rendered verbatim from `learning/code/ex-33-context-withdeadline/main.go`.

```go
package main

import (
  // context withdeadline: this operation makes initialization, cancellation, or shared access explicit.
  "context"
  // context withdeadline: this operation makes initialization, cancellation, or shared access explicit.
  "fmt"
  // context withdeadline: this operation makes initialization, cancellation, or shared access explicit.
  "time"
)

// context withdeadline: this operation makes initialization, cancellation, or shared access explicit.
func main() { // Deadlines let callers share one absolute cutoff.
  // context withdeadline: this operation makes initialization, cancellation, or shared access explicit.
  deadline := time.Now().Add(time.Millisecond)
  // context withdeadline: this operation makes initialization, cancellation, or shared access explicit.
  ctx, cancel := context.WithDeadline(context.Background(), deadline)
  // context withdeadline: this operation makes initialization, cancellation, or shared access explicit.
  defer cancel()
  // context withdeadline: this operation makes initialization, cancellation, or shared access explicit.
  <-ctx.Done()
  // context withdeadline: this operation makes initialization, cancellation, or shared access explicit.
  if ctx.Err() != context.DeadlineExceeded || time.Now().Before(deadline) {
    // context withdeadline: this operation makes initialization, cancellation, or shared access explicit.
    panic("deadline did not fire")
  }
  // context withdeadline: this operation makes initialization, cancellation, or shared access explicit.
  fmt.Println("deadline fired")
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 34: Context Err Canceled

_ex-34 · exercises co-14, co-16_

This CSP example is rendered verbatim from `learning/code/ex-34-context-err-canceled/main.go`.

```go
package main

import (
  // context err canceled: this operation makes initialization, cancellation, or shared access explicit.
  "context"
  // context err canceled: this operation makes initialization, cancellation, or shared access explicit.
  "fmt"
)

// context err canceled: this operation makes initialization, cancellation, or shared access explicit.
func main() { // Explicit cancellation is distinct from a deadline expiry.
  // context err canceled: this operation makes initialization, cancellation, or shared access explicit.
  ctx, cancel := context.WithCancel(context.Background())
  // context err canceled: this operation makes initialization, cancellation, or shared access explicit.
  cancel()
  // context err canceled: this operation makes initialization, cancellation, or shared access explicit.
  <-ctx.Done()
  // context err canceled: this operation makes initialization, cancellation, or shared access explicit.
  if ctx.Err() != context.Canceled {
    // context err canceled: this operation makes initialization, cancellation, or shared access explicit.
    panic(ctx.Err())
  }
  // context err canceled: this operation makes initialization, cancellation, or shared access explicit.
  fmt.Println("explicitly canceled")
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 35: Context Done In Select

_ex-35 · exercises co-14, co-16_

This CSP example is rendered verbatim from `learning/code/ex-35-context-done-in-select/main.go`.

```go
package main

import (
  // context done in select: this operation makes initialization, cancellation, or shared access explicit.
  "context"
  // context done in select: this operation makes initialization, cancellation, or shared access explicit.
  "fmt"
  // context done in select: this operation makes initialization, cancellation, or shared access explicit.
  "time"
)

// context done in select: this operation makes initialization, cancellation, or shared access explicit.
func main() { // Done wins over a slow input channel in select.
  // context done in select: this operation makes initialization, cancellation, or shared access explicit.
  ctx, cancel := context.WithCancel(context.Background())
  // context done in select: this operation makes initialization, cancellation, or shared access explicit.
  in := make(chan int)
  // context done in select: this operation makes initialization, cancellation, or shared access explicit.
  cancel()
  // context done in select: this operation makes initialization, cancellation, or shared access explicit.
  select {
  // context done in select: this operation makes initialization, cancellation, or shared access explicit.
  case <-ctx.Done():
    // context done in select: this operation makes initialization, cancellation, or shared access explicit.
    fmt.Println("canceled before input")
  // context done in select: this operation makes initialization, cancellation, or shared access explicit.
  case <-in:
    // context done in select: this operation makes initialization, cancellation, or shared access explicit.
    panic("slow input won")
  // context done in select: this operation makes initialization, cancellation, or shared access explicit.
  case <-time.After(time.Second):
    // context done in select: this operation makes initialization, cancellation, or shared access explicit.
    panic("blocked")
  }
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 36: Pipeline Two Stage

_ex-36 · exercises co-17, co-20, co-21_

This CSP example is rendered verbatim from `learning/code/ex-36-pipeline-two-stage/main.go`.

```go
package main

// pipeline two stage: this step makes data flow and termination explicit.
import "fmt"

// pipeline two stage: this step makes data flow and termination explicit.
func square(in <-chan int) <-chan int {
  // pipeline two stage: this step makes data flow and termination explicit.
  out := make(chan int)
  // pipeline two stage: this step makes data flow and termination explicit.
  go func() {
    // pipeline two stage: this step makes data flow and termination explicit.
    defer close(out)
    // pipeline two stage: this step makes data flow and termination explicit.
    for value := range in {
      // pipeline two stage: this step makes data flow and termination explicit.
      out <- value * value
    }
    // pipeline two stage: this step makes data flow and termination explicit.
  }()
  // pipeline two stage: this step makes data flow and termination explicit.
  return out
}

// pipeline two stage: this step makes data flow and termination explicit.
func label(in <-chan int) <-chan string {
  // pipeline two stage: this step makes data flow and termination explicit.
  out := make(chan string)
  // pipeline two stage: this step makes data flow and termination explicit.
  go func() {
    // pipeline two stage: this step makes data flow and termination explicit.
    defer close(out)
    // pipeline two stage: this step makes data flow and termination explicit.
    for value := range in {
      // pipeline two stage: this step makes data flow and termination explicit.
      out <- fmt.Sprintf("square=%d", value)
    }
    // pipeline two stage: this step makes data flow and termination explicit.
  }()
  // pipeline two stage: this step makes data flow and termination explicit.
  return out
}

// pipeline two stage: this step makes data flow and termination explicit.
func main() {
  // pipeline two stage: this step makes data flow and termination explicit.
  input := make(chan int, 3)
  // pipeline two stage: this step makes data flow and termination explicit.
  for _, value := range []int{2, 3, 4} {
    // pipeline two stage: this step makes data flow and termination explicit.
    input <- value
  }
  // pipeline two stage: this step makes data flow and termination explicit.
  close(input)
  // pipeline two stage: this step makes data flow and termination explicit.
  for value := range label(square(input)) {
    // pipeline two stage: this step makes data flow and termination explicit.
    fmt.Println(value)
  }
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 37: Pipeline Three Stage

_ex-37 · exercises co-17, co-20, co-21_

This CSP example is rendered verbatim from `learning/code/ex-37-pipeline-three-stage/main.go`.

```go
package main

// pipeline three stage: this step makes data flow and termination explicit.
import "fmt"

// pipeline three stage: this step makes data flow and termination explicit.
func values(items ...int) <-chan int {
  // pipeline three stage: this step makes data flow and termination explicit.
  out := make(chan int)
  // pipeline three stage: this step makes data flow and termination explicit.
  go func() {
    // pipeline three stage: this step makes data flow and termination explicit.
    defer close(out)
    // pipeline three stage: this step makes data flow and termination explicit.
    for _, item := range items {
      // pipeline three stage: this step makes data flow and termination explicit.
      out <- item
    }
    // pipeline three stage: this step makes data flow and termination explicit.
  }()
  // pipeline three stage: this step makes data flow and termination explicit.
  return out
}

// pipeline three stage: this step makes data flow and termination explicit.
func double(in <-chan int) <-chan int {
  // pipeline three stage: this step makes data flow and termination explicit.
  out := make(chan int)
  // pipeline three stage: this step makes data flow and termination explicit.
  go func() {
    // pipeline three stage: this step makes data flow and termination explicit.
    defer close(out)
    // pipeline three stage: this step makes data flow and termination explicit.
    for item := range in {
      // pipeline three stage: this step makes data flow and termination explicit.
      out <- item * 2
    }
    // pipeline three stage: this step makes data flow and termination explicit.
  }()
  // pipeline three stage: this step makes data flow and termination explicit.
  return out
}

// pipeline three stage: this step makes data flow and termination explicit.
func keepMultipleOfFour(in <-chan int) <-chan int {
  // pipeline three stage: this step makes data flow and termination explicit.
  out := make(chan int)
  // pipeline three stage: this step makes data flow and termination explicit.
  go func() {
    // pipeline three stage: this step makes data flow and termination explicit.
    defer close(out)
    // pipeline three stage: this step makes data flow and termination explicit.
    for item := range in {
      // pipeline three stage: this step makes data flow and termination explicit.
      if item%4 == 0 {
        // pipeline three stage: this step makes data flow and termination explicit.
        out <- item
      }
    }
    // pipeline three stage: this step makes data flow and termination explicit.
  }()
  // pipeline three stage: this step makes data flow and termination explicit.
  return out
}

// pipeline three stage: this step makes data flow and termination explicit.
func main() {
  // pipeline three stage: this step makes data flow and termination explicit.
  for item := range keepMultipleOfFour(double(values(1, 2, 3, 4))) {
    // pipeline three stage: this step makes data flow and termination explicit.
    fmt.Println("kept", item)
  }
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 38: Pipeline Generator

_ex-38 · exercises co-17, co-20, co-21_

This CSP example is rendered verbatim from `learning/code/ex-38-pipeline-generator/main.go`.

```go
package main

// pipeline generator: this step makes data flow and termination explicit.
import "fmt"

// pipeline generator: this step makes data flow and termination explicit.
func generator(values ...int) <-chan int {
  // pipeline generator: this step makes data flow and termination explicit.
  out := make(chan int)
  // pipeline generator: this step makes data flow and termination explicit.
  go func() {
    // pipeline generator: this step makes data flow and termination explicit.
    defer close(out)
    // pipeline generator: this step makes data flow and termination explicit.
    for _, value := range values {
      // pipeline generator: this step makes data flow and termination explicit.
      out <- value
    }
    // pipeline generator: this step makes data flow and termination explicit.
  }()
  // pipeline generator: this step makes data flow and termination explicit.
  return out
}

// pipeline generator: this step makes data flow and termination explicit.
func collect(in <-chan int) []int {
  // pipeline generator: this step makes data flow and termination explicit.
  var items []int
  // pipeline generator: this step makes data flow and termination explicit.
  for item := range in {
    // pipeline generator: this step makes data flow and termination explicit.
    items = append(items, item)
  }
  // pipeline generator: this step makes data flow and termination explicit.
  return items
}

// pipeline generator: this step makes data flow and termination explicit.
func main() {
  // pipeline generator: this step makes data flow and termination explicit.
  fmt.Println("first", collect(generator(1, 2, 3)))
  // pipeline generator: this step makes data flow and termination explicit.
  fmt.Println("second", collect(generator(8, 13)))
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 39: Fan Out Workers

_ex-39 · exercises co-17, co-20, co-21_

This CSP example is rendered verbatim from `learning/code/ex-39-fan-out-workers/main.go`.

```go
package main

import (
  // fan out workers: this step makes data flow and termination explicit.
  "fmt"
  // fan out workers: this step makes data flow and termination explicit.
  "sync"
)

// fan out workers: this step makes data flow and termination explicit.
func worker(id int, jobs <-chan int, results chan<- string, group *sync.WaitGroup) {
  // fan out workers: this step makes data flow and termination explicit.
  defer group.Done()
  // fan out workers: this step makes data flow and termination explicit.
  for job := range jobs {
    // fan out workers: this step makes data flow and termination explicit.
    results <- fmt.Sprintf("worker-%d processed %d", id, job)
  }
}

// fan out workers: this step makes data flow and termination explicit.
func main() {
  // fan out workers: this step makes data flow and termination explicit.
  jobs := make(chan int)
  // fan out workers: this step makes data flow and termination explicit.
  results := make(chan string, 4)
  // fan out workers: this step makes data flow and termination explicit.
  var group sync.WaitGroup
  // fan out workers: this step makes data flow and termination explicit.
  for id := 1; id <= 2; id++ {
    // fan out workers: this step makes data flow and termination explicit.
    group.Add(1)
    // fan out workers: this step makes data flow and termination explicit.
    go worker(id, jobs, results, &group)
  }
  // fan out workers: this step makes data flow and termination explicit.
  go func() {
    // fan out workers: this step makes data flow and termination explicit.
    for _, job := range []int{10, 20, 30, 40} {
      // fan out workers: this step makes data flow and termination explicit.
      jobs <- job
    }
    // fan out workers: this step makes data flow and termination explicit.
    close(jobs)
    // fan out workers: this step makes data flow and termination explicit.
    group.Wait()
    // fan out workers: this step makes data flow and termination explicit.
    close(results)
    // fan out workers: this step makes data flow and termination explicit.
  }()
  // fan out workers: this step makes data flow and termination explicit.
  for result := range results {
    // fan out workers: this step makes data flow and termination explicit.
    fmt.Println(result)
  }
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 40: Fan Out Parallel Speedup

_ex-40 · exercises co-17, co-20, co-21_

This CSP example is rendered verbatim from `learning/code/ex-40-fan-out-parallel-speedup/main.go`.

```go
package main

import (
  // fan out parallel speedup: this step makes data flow and termination explicit.
  "fmt"
  // fan out parallel speedup: this step makes data flow and termination explicit.
  "sync"
  // fan out parallel speedup: this step makes data flow and termination explicit.
  "time"
)

// fan out parallel speedup: this step makes data flow and termination explicit.
func runSequential(jobs []int) time.Duration {
  // fan out parallel speedup: this step makes data flow and termination explicit.
  started := time.Now()
  // fan out parallel speedup: this step makes data flow and termination explicit.
  for range jobs {
    // fan out parallel speedup: this step makes data flow and termination explicit.
    time.Sleep(10 * time.Millisecond)
  }
  // fan out parallel speedup: this step makes data flow and termination explicit.
  return time.Since(started)
}

// fan out parallel speedup: this step makes data flow and termination explicit.
func runParallel(jobs []int, workers int) time.Duration {
  // fan out parallel speedup: this step makes data flow and termination explicit.
  started := time.Now()
  // fan out parallel speedup: this step makes data flow and termination explicit.
  queue := make(chan int)
  // fan out parallel speedup: this step makes data flow and termination explicit.
  var group sync.WaitGroup
  // fan out parallel speedup: this step makes data flow and termination explicit.
  for range workers {
    // fan out parallel speedup: this step makes data flow and termination explicit.
    group.Add(1)
    // fan out parallel speedup: this step makes data flow and termination explicit.
    go func() {
      // fan out parallel speedup: this step makes data flow and termination explicit.
      defer group.Done()
      // fan out parallel speedup: this step makes data flow and termination explicit.
      for range queue {
        // fan out parallel speedup: this step makes data flow and termination explicit.
        time.Sleep(10 * time.Millisecond)
      }
      // fan out parallel speedup: this step makes data flow and termination explicit.
    }()
  }
  // fan out parallel speedup: this step makes data flow and termination explicit.
  for _, job := range jobs {
    // fan out parallel speedup: this step makes data flow and termination explicit.
    queue <- job
  }
  // fan out parallel speedup: this step makes data flow and termination explicit.
  close(queue)
  // fan out parallel speedup: this step makes data flow and termination explicit.
  group.Wait()
  // fan out parallel speedup: this step makes data flow and termination explicit.
  return time.Since(started)
}

// fan out parallel speedup: this step makes data flow and termination explicit.
func main() {
  // fan out parallel speedup: this step makes data flow and termination explicit.
  jobs := []int{1, 2, 3, 4}
  // fan out parallel speedup: this step makes data flow and termination explicit.
  sequential := runSequential(jobs)
  // fan out parallel speedup: this step makes data flow and termination explicit.
  parallel := runParallel(jobs, 2)
  // fan out parallel speedup: this step makes data flow and termination explicit.
  fmt.Println("parallel-faster", parallel < sequential)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 41: Fan In Merge

_ex-41 · exercises co-17, co-20, co-21_

This CSP example is rendered verbatim from `learning/code/ex-41-fan-in-merge/main.go`.

```go
package main

import (
  // fan in merge: this step makes data flow and termination explicit.
  "fmt"
  // fan in merge: this step makes data flow and termination explicit.
  "sync"
)

// fan in merge: this step makes data flow and termination explicit.
func merge(inputs ...<-chan int) <-chan int {
  // fan in merge: this step makes data flow and termination explicit.
  out := make(chan int)
  // fan in merge: this step makes data flow and termination explicit.
  var group sync.WaitGroup
  // fan in merge: this step makes data flow and termination explicit.
  for _, input := range inputs {
    // fan in merge: this step makes data flow and termination explicit.
    group.Add(1)
    // fan in merge: this step makes data flow and termination explicit.
    go func(source <-chan int) {
      // fan in merge: this step makes data flow and termination explicit.
      defer group.Done()
      // fan in merge: this step makes data flow and termination explicit.
      for value := range source {
        // fan in merge: this step makes data flow and termination explicit.
        out <- value
      }
      // fan in merge: this step makes data flow and termination explicit.
    }(input)
  }
  // fan in merge: this step makes data flow and termination explicit.
  go func() {
    // fan in merge: this step makes data flow and termination explicit.
    group.Wait()
    // fan in merge: this step makes data flow and termination explicit.
    close(out)
    // fan in merge: this step makes data flow and termination explicit.
  }()
  // fan in merge: this step makes data flow and termination explicit.
  return out
}

// fan in merge: this step makes data flow and termination explicit.
func main() {
  // fan in merge: this step makes data flow and termination explicit.
  left := make(chan int, 2)
  // fan in merge: this step makes data flow and termination explicit.
  right := make(chan int, 2)
  // fan in merge: this step makes data flow and termination explicit.
  left <- 1
  // fan in merge: this step makes data flow and termination explicit.
  left <- 2
  // fan in merge: this step makes data flow and termination explicit.
  right <- 3
  // fan in merge: this step makes data flow and termination explicit.
  right <- 4
  // fan in merge: this step makes data flow and termination explicit.
  close(left)
  // fan in merge: this step makes data flow and termination explicit.
  close(right)
  // fan in merge: this step makes data flow and termination explicit.
  total := 0
  // fan in merge: this step makes data flow and termination explicit.
  for value := range merge(left, right) {
    // fan in merge: this step makes data flow and termination explicit.
    total += value
  }
  // fan in merge: this step makes data flow and termination explicit.
  fmt.Println("merged-total", total)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 42: Fan In Waitgroup Close

_ex-42 · exercises co-17, co-20, co-21_

This CSP example is rendered verbatim from `learning/code/ex-42-fan-in-waitgroup-close/main.go`.

```go
package main

import (
  // fan in waitgroup close: this step makes data flow and termination explicit.
  "fmt"
  // fan in waitgroup close: this step makes data flow and termination explicit.
  "sync"
)

// fan in waitgroup close: this step makes data flow and termination explicit.
func mergeAndCloseWhenForwardersFinish(left, right <-chan string) <-chan string {
  // fan in waitgroup close: this step makes data flow and termination explicit.
  out := make(chan string)
  // fan in waitgroup close: this step makes data flow and termination explicit.
  var forwarders sync.WaitGroup
  // fan in waitgroup close: this step makes data flow and termination explicit.
  forward := func(input <-chan string) {
    // fan in waitgroup close: this step makes data flow and termination explicit.
    defer forwarders.Done()
    // fan in waitgroup close: this step makes data flow and termination explicit.
    for value := range input {
      // fan in waitgroup close: this step makes data flow and termination explicit.
      out <- value
    }
  }
  // fan in waitgroup close: this step makes data flow and termination explicit.
  forwarders.Add(2)
  // fan in waitgroup close: this step makes data flow and termination explicit.
  go forward(left)
  // fan in waitgroup close: this step makes data flow and termination explicit.
  go forward(right)
  // fan in waitgroup close: this step makes data flow and termination explicit.
  go func() {
    // fan in waitgroup close: this step makes data flow and termination explicit.
    forwarders.Wait()
    // fan in waitgroup close: this step makes data flow and termination explicit.
    close(out)
    // fan in waitgroup close: this step makes data flow and termination explicit.
  }()
  // fan in waitgroup close: this step makes data flow and termination explicit.
  return out
}

// fan in waitgroup close: this step makes data flow and termination explicit.
func main() {
  // fan in waitgroup close: this step makes data flow and termination explicit.
  left := make(chan string, 1)
  // fan in waitgroup close: this step makes data flow and termination explicit.
  right := make(chan string, 1)
  // fan in waitgroup close: this step makes data flow and termination explicit.
  left <- "left"
  // fan in waitgroup close: this step makes data flow and termination explicit.
  right <- "right"
  // fan in waitgroup close: this step makes data flow and termination explicit.
  close(left)
  // fan in waitgroup close: this step makes data flow and termination explicit.
  close(right)
  // fan in waitgroup close: this step makes data flow and termination explicit.
  count := 0
  // fan in waitgroup close: this step makes data flow and termination explicit.
  for range mergeAndCloseWhenForwardersFinish(left, right) {
    // fan in waitgroup close: this step makes data flow and termination explicit.
    count++
  }
  // fan in waitgroup close: this step makes data flow and termination explicit.
  fmt.Println("closed-after-forwarders", count)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 43: Worker Pool Bounded

_ex-43 · exercises co-17, co-20, co-21_

This CSP example is rendered verbatim from `learning/code/ex-43-worker-pool-bounded/main.go`.

```go
package main

import (
  // worker pool bounded: this step makes data flow and termination explicit.
  "fmt"
  // worker pool bounded: this step makes data flow and termination explicit.
  "sync"
  // worker pool bounded: this step makes data flow and termination explicit.
  "time"
)

// worker pool bounded: this step makes data flow and termination explicit.
func main() {
  // worker pool bounded: this step makes data flow and termination explicit.
  const workers = 3
  // worker pool bounded: this step makes data flow and termination explicit.
  jobs := make(chan int)
  // worker pool bounded: this step makes data flow and termination explicit.
  var group sync.WaitGroup
  // worker pool bounded: this step makes data flow and termination explicit.
  var lock sync.Mutex
  // worker pool bounded: this step makes data flow and termination explicit.
  active, peak := 0, 0
  // worker pool bounded: this step makes data flow and termination explicit.
  for range workers {
    // worker pool bounded: this step makes data flow and termination explicit.
    group.Add(1)
    // worker pool bounded: this step makes data flow and termination explicit.
    go func() {
      // worker pool bounded: this step makes data flow and termination explicit.
      defer group.Done()
      // worker pool bounded: this step makes data flow and termination explicit.
      for range jobs {
        // worker pool bounded: this step makes data flow and termination explicit.
        lock.Lock()
        // worker pool bounded: this step makes data flow and termination explicit.
        active++
        // worker pool bounded: this step makes data flow and termination explicit.
        if active > peak {
          // worker pool bounded: this step makes data flow and termination explicit.
          peak = active
        }
        // worker pool bounded: this step makes data flow and termination explicit.
        lock.Unlock()
        // worker pool bounded: this step makes data flow and termination explicit.
        time.Sleep(time.Millisecond)
        // worker pool bounded: this step makes data flow and termination explicit.
        lock.Lock()
        // worker pool bounded: this step makes data flow and termination explicit.
        active--
        // worker pool bounded: this step makes data flow and termination explicit.
        lock.Unlock()
      }
      // worker pool bounded: this step makes data flow and termination explicit.
    }()
  }
  // worker pool bounded: this step makes data flow and termination explicit.
  for job := 0; job < 8; job++ {
    // worker pool bounded: this step makes data flow and termination explicit.
    jobs <- job
  }
  // worker pool bounded: this step makes data flow and termination explicit.
  close(jobs)
  // worker pool bounded: this step makes data flow and termination explicit.
  group.Wait()
  // worker pool bounded: this step makes data flow and termination explicit.
  fmt.Println("bounded-peak", peak)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 44: Worker Pool Results

_ex-44 · exercises co-17, co-20, co-21_

This CSP example is rendered verbatim from `learning/code/ex-44-worker-pool-results/main.go`.

```go
package main

import (
  // worker pool results: this step makes data flow and termination explicit.
  "fmt"
  // worker pool results: this step makes data flow and termination explicit.
  "sort"
  // worker pool results: this step makes data flow and termination explicit.
  "sync"
)

// worker pool results: this step makes data flow and termination explicit.
type result struct {
  // worker pool results: this step makes data flow and termination explicit.
  job int
  // worker pool results: this step makes data flow and termination explicit.
  value int
}

// worker pool results: this step makes data flow and termination explicit.
func main() {
  // worker pool results: this step makes data flow and termination explicit.
  jobs := make(chan int)
  // worker pool results: this step makes data flow and termination explicit.
  results := make(chan result)
  // worker pool results: this step makes data flow and termination explicit.
  var group sync.WaitGroup
  // worker pool results: this step makes data flow and termination explicit.
  for range 2 {
    // worker pool results: this step makes data flow and termination explicit.
    group.Add(1)
    // worker pool results: this step makes data flow and termination explicit.
    go func() {
      // worker pool results: this step makes data flow and termination explicit.
      defer group.Done()
      // worker pool results: this step makes data flow and termination explicit.
      for job := range jobs {
        // worker pool results: this step makes data flow and termination explicit.
        results <- result{job: job, value: job * job}
      }
      // worker pool results: this step makes data flow and termination explicit.
    }()
  }
  // worker pool results: this step makes data flow and termination explicit.
  go func() {
    // worker pool results: this step makes data flow and termination explicit.
    for _, job := range []int{2, 3, 4} {
      // worker pool results: this step makes data flow and termination explicit.
      jobs <- job
    }
    // worker pool results: this step makes data flow and termination explicit.
    close(jobs)
    // worker pool results: this step makes data flow and termination explicit.
    group.Wait()
    // worker pool results: this step makes data flow and termination explicit.
    close(results)
    // worker pool results: this step makes data flow and termination explicit.
  }()
  // worker pool results: this step makes data flow and termination explicit.
  var collected []result
  // worker pool results: this step makes data flow and termination explicit.
  for item := range results {
    // worker pool results: this step makes data flow and termination explicit.
    collected = append(collected, item)
  }
  // worker pool results: this step makes data flow and termination explicit.
  sort.Slice(collected, func(i, j int) bool { return collected[i].job < collected[j].job })
  // worker pool results: this step makes data flow and termination explicit.
  fmt.Println("results", collected)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 45: Worker Pool Jobs Channel

_ex-45 · exercises co-17, co-20, co-21_

This CSP example is rendered verbatim from `learning/code/ex-45-worker-pool-jobs-channel/main.go`.

```go
package main

import (
  // worker pool jobs channel: this step makes data flow and termination explicit.
  "fmt"
  // worker pool jobs channel: this step makes data flow and termination explicit.
  "sync"
)

// worker pool jobs channel: this step makes data flow and termination explicit.
func main() {
  // worker pool jobs channel: this step makes data flow and termination explicit.
  const workers = 2
  // worker pool jobs channel: this step makes data flow and termination explicit.
  jobs := make(chan int)
  // worker pool jobs channel: this step makes data flow and termination explicit.
  exited := make(chan int, workers)
  // worker pool jobs channel: this step makes data flow and termination explicit.
  var group sync.WaitGroup
  // worker pool jobs channel: this step makes data flow and termination explicit.
  for id := 1; id <= workers; id++ {
    // worker pool jobs channel: this step makes data flow and termination explicit.
    group.Add(1)
    // worker pool jobs channel: this step makes data flow and termination explicit.
    go func(workerID int) {
      // worker pool jobs channel: this step makes data flow and termination explicit.
      defer group.Done()
      // worker pool jobs channel: this step makes data flow and termination explicit.
      for job := range jobs {
        // worker pool jobs channel: this step makes data flow and termination explicit.
        fmt.Println("processed", workerID, job)
      }
      // worker pool jobs channel: this step makes data flow and termination explicit.
      exited <- workerID
      // worker pool jobs channel: this step makes data flow and termination explicit.
    }(id)
  }
  // worker pool jobs channel: this step makes data flow and termination explicit.
  jobs <- 7
  // worker pool jobs channel: this step makes data flow and termination explicit.
  jobs <- 9
  // worker pool jobs channel: this step makes data flow and termination explicit.
  close(jobs)
  // worker pool jobs channel: this step makes data flow and termination explicit.
  group.Wait()
  // worker pool jobs channel: this step makes data flow and termination explicit.
  close(exited)
  // worker pool jobs channel: this step makes data flow and termination explicit.
  count := 0
  // worker pool jobs channel: this step makes data flow and termination explicit.
  for range exited {
    // worker pool jobs channel: this step makes data flow and termination explicit.
    count++
  }
  // worker pool jobs channel: this step makes data flow and termination explicit.
  fmt.Println("workers-exited-after-jobs-close", count)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 46: Done Channel Cancel

_ex-46 · exercises co-17, co-20, co-21_

This CSP example is rendered verbatim from `learning/code/ex-46-done-channel-cancel/main.go`.

```go
package main

// done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
import "fmt"

// done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
func producer(done <-chan struct{}, values ...int) <-chan int {
  // done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
  out := make(chan int)
  // done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
  go func() {
    // done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
    defer close(out)
    // done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
    for _, value := range values {
      // done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
      select {
      // done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
      case out <- value:
      // done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
      case <-done:
        // done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
        fmt.Println("producer-canceled")
        // done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
        return
      }
    }
    // done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
  }()
  // done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
  return out
}

// done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
func main() {
  // done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
  done := make(chan struct{})
  // done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
  values := producer(done, 1, 2, 3)
  // done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
  fmt.Println("received", <-values)
  // done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
  close(done)
  // done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
  for range values {
  }
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 47: Done Channel Defer Close

_ex-47 · exercises co-17, co-20, co-21_

This CSP example is rendered verbatim from `learning/code/ex-47-done-channel-defer-close/main.go`.

```go
package main

import (
  // done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
  "fmt"
  // done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
  "sync"
)

// done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
func run(done chan struct{}, group *sync.WaitGroup) {
  // done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
  defer close(done)
  // done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
  defer group.Done()
  // done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
  fmt.Println("owner-finished-work")
}

// done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
func main() {
  // done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
  done := make(chan struct{})
  // done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
  var group sync.WaitGroup
  // done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
  group.Add(1)
  // done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
  go run(done, &group)
  // done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
  <-done
  // done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
  group.Wait()
  // done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
  fmt.Println("done-closed-by-defer")
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 48: Pipeline Cancel Early

_ex-48 · exercises co-17, co-20, co-21_

This CSP example is rendered verbatim from `learning/code/ex-48-pipeline-cancel-early/main.go`.

```go
package main

// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
import "fmt"

// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
func generate(done <-chan struct{}, values ...int) <-chan int {
  // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
  out := make(chan int)
  // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
  go func() {
    // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
    defer close(out)
    // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
    for _, value := range values {
      // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
      select {
      // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
      case out <- value:
      // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
      case <-done:
        // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
        return
      }
    }
    // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
  }()
  // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
  return out
}

// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
func square(done <-chan struct{}, in <-chan int) <-chan int {
  // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
  out := make(chan int)
  // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
  go func() {
    // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
    defer close(out)
    // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
    for value := range in {
      // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
      select {
      // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
      case out <- value * value:
      // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
      case <-done:
        // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
        return
      }
    }
    // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
  }()
  // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
  return out
}

// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
func main() {
  // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
  done := make(chan struct{})
  // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
  out := square(done, generate(done, 2, 3, 4))
  // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
  fmt.Println("first-result", <-out)
  // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
  close(done)
  // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
  for range out {
  }
  // pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
  fmt.Println("pipeline-canceled-early")
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 49: Select Send Or Done

_ex-49 · exercises co-17, co-20, co-21_

This CSP example is rendered verbatim from `learning/code/ex-49-select-send-or-done/main.go`.

```go
package main

// select send or done: this step makes cancellation, ownership, or bounded work explicit.
import "fmt"

// select send or done: this step makes cancellation, ownership, or bounded work explicit.
func sendOrDone(done <-chan struct{}, out chan<- int, value int) bool {
  // select send or done: this step makes cancellation, ownership, or bounded work explicit.
  select {
  // select send or done: this step makes cancellation, ownership, or bounded work explicit.
  case out <- value:
    // select send or done: this step makes cancellation, ownership, or bounded work explicit.
    return true
  // select send or done: this step makes cancellation, ownership, or bounded work explicit.
  case <-done:
    // select send or done: this step makes cancellation, ownership, or bounded work explicit.
    return false
  }
}

// select send or done: this step makes cancellation, ownership, or bounded work explicit.
func main() {
  // select send or done: this step makes cancellation, ownership, or bounded work explicit.
  done := make(chan struct{})
  // select send or done: this step makes cancellation, ownership, or bounded work explicit.
  out := make(chan int)
  // select send or done: this step makes cancellation, ownership, or bounded work explicit.
  close(done)
  // select send or done: this step makes cancellation, ownership, or bounded work explicit.
  fmt.Println("sent-after-cancel", sendOrDone(done, out, 42))
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 50: Context Vs Done

_ex-50 · exercises co-17, co-20, co-21_

This CSP example is rendered verbatim from `learning/code/ex-50-context-vs-done/main.go`.

```go
package main

import (
  // context vs done: this step makes cancellation, ownership, or bounded work explicit.
  "context"
  // context vs done: this step makes cancellation, ownership, or bounded work explicit.
  "fmt"
  // context vs done: this step makes cancellation, ownership, or bounded work explicit.
  "sync"
)

// context vs done: this step makes cancellation, ownership, or bounded work explicit.
func waitForDone(done <-chan struct{}, group *sync.WaitGroup) {
  // context vs done: this step makes cancellation, ownership, or bounded work explicit.
  defer group.Done()
  // context vs done: this step makes cancellation, ownership, or bounded work explicit.
  <-done
  // context vs done: this step makes cancellation, ownership, or bounded work explicit.
  fmt.Println("done-channel-stopped")
}

// context vs done: this step makes cancellation, ownership, or bounded work explicit.
func waitForContext(ctx context.Context, group *sync.WaitGroup) {
  // context vs done: this step makes cancellation, ownership, or bounded work explicit.
  defer group.Done()
  // context vs done: this step makes cancellation, ownership, or bounded work explicit.
  <-ctx.Done()
  // context vs done: this step makes cancellation, ownership, or bounded work explicit.
  fmt.Println("context-stopped")
}

// context vs done: this step makes cancellation, ownership, or bounded work explicit.
func main() {
  // context vs done: this step makes cancellation, ownership, or bounded work explicit.
  done := make(chan struct{})
  // context vs done: this step makes cancellation, ownership, or bounded work explicit.
  ctx, cancel := context.WithCancel(context.Background())
  // context vs done: this step makes cancellation, ownership, or bounded work explicit.
  var group sync.WaitGroup
  // context vs done: this step makes cancellation, ownership, or bounded work explicit.
  group.Add(2)
  // context vs done: this step makes cancellation, ownership, or bounded work explicit.
  go waitForDone(done, &group)
  // context vs done: this step makes cancellation, ownership, or bounded work explicit.
  go waitForContext(ctx, &group)
  // context vs done: this step makes cancellation, ownership, or bounded work explicit.
  close(done)
  // context vs done: this step makes cancellation, ownership, or bounded work explicit.
  cancel()
  // context vs done: this step makes cancellation, ownership, or bounded work explicit.
  group.Wait()
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 51: Timeout Per Job

_ex-51 · exercises co-17, co-20, co-21_

This CSP example is rendered verbatim from `learning/code/ex-51-timeout-per-job/main.go`.

```go
package main

import (
  // timeout per job: this step makes cancellation, ownership, or bounded work explicit.
  "context"
  // timeout per job: this step makes cancellation, ownership, or bounded work explicit.
  "fmt"
  // timeout per job: this step makes cancellation, ownership, or bounded work explicit.
  "time"
)

// timeout per job: this step makes cancellation, ownership, or bounded work explicit.
func process(ctx context.Context, job int, duration time.Duration) string {
  // timeout per job: this step makes cancellation, ownership, or bounded work explicit.
  select {
  // timeout per job: this step makes cancellation, ownership, or bounded work explicit.
  case <-time.After(duration):
    // timeout per job: this step makes cancellation, ownership, or bounded work explicit.
    return fmt.Sprintf("job-%d-complete", job)
  // timeout per job: this step makes cancellation, ownership, or bounded work explicit.
  case <-ctx.Done():
    // timeout per job: this step makes cancellation, ownership, or bounded work explicit.
    return fmt.Sprintf("job-%d-%v", job, ctx.Err())
  }
}

// timeout per job: this step makes cancellation, ownership, or bounded work explicit.
func main() {
  // timeout per job: this step makes cancellation, ownership, or bounded work explicit.
  for _, job := range []struct {
    // timeout per job: this step makes cancellation, ownership, or bounded work explicit.
    id int
    // timeout per job: this step makes cancellation, ownership, or bounded work explicit.
    duration time.Duration
    // timeout per job: this step makes cancellation, ownership, or bounded work explicit.
  }{{1, time.Millisecond}, {2, 10 * time.Millisecond}} {
    // timeout per job: this step makes cancellation, ownership, or bounded work explicit.
    ctx, cancel := context.WithTimeout(context.Background(), 3*time.Millisecond)
    // timeout per job: this step makes cancellation, ownership, or bounded work explicit.
    fmt.Println(process(ctx, job.id, job.duration))
    // timeout per job: this step makes cancellation, ownership, or bounded work explicit.
    cancel()
  }
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 52: Graceful Shutdown

_ex-52 · exercises co-17, co-20, co-21_

This CSP example is rendered verbatim from `learning/code/ex-52-graceful-shutdown/main.go`.

```go
package main

import (
  // graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
  "fmt"
  // graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
  "sync"
  // graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
  "time"
)

// graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
func main() {
  // graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
  jobs := make(chan int, 3)
  // graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
  var group sync.WaitGroup
  // graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
  processed := 0
  // graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
  var lock sync.Mutex
  // graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
  group.Add(1)
  // graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
  go func() {
    // graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
    defer group.Done()
    // graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
    for job := range jobs {
      // graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
      time.Sleep(time.Millisecond)
      // graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
      lock.Lock()
      // graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
      processed += job
      // graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
      lock.Unlock()
    }
    // graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
  }()
  // graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
  for _, job := range []int{1, 2, 3} {
    // graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
    jobs <- job
  }
  // graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
  close(jobs)
  // graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
  group.Wait()
  // graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
  fmt.Println("gracefully-drained-total", processed)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 53: Rate Limit Ticker

_ex-53 · exercises co-17, co-20, co-21_

This CSP example is rendered verbatim from `learning/code/ex-53-rate-limit-ticker/main.go`.

```go
package main

import (
  // rate limit ticker: this step makes cancellation, ownership, or bounded work explicit.
  "fmt"
  // rate limit ticker: this step makes cancellation, ownership, or bounded work explicit.
  "time"
)

// rate limit ticker: this step makes cancellation, ownership, or bounded work explicit.
func main() {
  // rate limit ticker: this step makes cancellation, ownership, or bounded work explicit.
  limit := time.NewTicker(time.Millisecond)
  // rate limit ticker: this step makes cancellation, ownership, or bounded work explicit.
  defer limit.Stop()
  // rate limit ticker: this step makes cancellation, ownership, or bounded work explicit.
  for request := 1; request <= 3; request++ {
    // rate limit ticker: this step makes cancellation, ownership, or bounded work explicit.
    <-limit.C
    // rate limit ticker: this step makes cancellation, ownership, or bounded work explicit.
    fmt.Println("allowed-request", request)
  }
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 54: Semaphore Buffered Channel

_ex-54 · exercises co-17, co-20, co-21_

This CSP example is rendered verbatim from `learning/code/ex-54-semaphore-buffered-channel/main.go`.

```go
package main

import (
  // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
  "fmt"
  // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
  "sync"
  // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
  "time"
)

// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
func main() {
  // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
  sem := make(chan struct{}, 2)
  // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
  var group sync.WaitGroup
  // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
  var lock sync.Mutex
  // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
  active, peak := 0, 0
  // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
  for task := 1; task <= 5; task++ {
    // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
    group.Add(1)
    // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
    go func() {
      // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
      defer group.Done()
      // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
      sem <- struct{}{}
      // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
      lock.Lock()
      // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
      active++
      // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
      if active > peak {
        // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
        peak = active
      }
      // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
      lock.Unlock()
      // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
      time.Sleep(time.Millisecond)
      // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
      lock.Lock()
      // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
      active--
      // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
      lock.Unlock()
      // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
      <-sem
      // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
    }()
  }
  // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
  group.Wait()
  // semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
  fmt.Println("semaphore-peak", peak)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.
