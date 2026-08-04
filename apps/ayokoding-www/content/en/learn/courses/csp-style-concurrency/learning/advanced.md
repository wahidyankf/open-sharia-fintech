---
title: "Advanced Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 30
---

### Example 55: Happens Before Channel

_ex-55 · exercises co-22, co-23, co-24_

This CSP example is rendered verbatim from `learning/code/ex-55-happens-before-channel/main.go`.

```go
package main

// happens before channel: this diagnostic keeps synchronization and cleanup observable.
import "fmt"

// happens before channel: this diagnostic keeps synchronization and cleanup observable.
type configuration struct {
  // happens before channel: this diagnostic keeps synchronization and cleanup observable.
  port int
}

// happens before channel: this diagnostic keeps synchronization and cleanup observable.
func main() {
  // happens before channel: this diagnostic keeps synchronization and cleanup observable.
  ready := make(chan configuration)
  // happens before channel: this diagnostic keeps synchronization and cleanup observable.
  go func() {
    // happens before channel: this diagnostic keeps synchronization and cleanup observable.
    config := configuration{port: 8080}
    // happens before channel: this diagnostic keeps synchronization and cleanup observable.
    ready <- config
    // happens before channel: this diagnostic keeps synchronization and cleanup observable.
  }()
  // happens before channel: this diagnostic keeps synchronization and cleanup observable.
  config := <-ready
  // happens before channel: this diagnostic keeps synchronization and cleanup observable.
  fmt.Println("published-port", config.port)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 56: Memory Visibility Unsync

_ex-56 · exercises co-22, co-23, co-24_

This CSP example is rendered verbatim from `learning/code/ex-56-memory-visibility-unsync/main.go`.

```go
package main

import (
  // memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
  "fmt"
  // memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
  "os"
  // memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
  "sync"
)

// memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
func main() {
  // memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
  if os.Getenv("RACE_DEMO") != "1" {
    // memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
    fmt.Println("diagnostic: RACE_DEMO=1 go run -race main.go")
    // memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
    return
  }
  // memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
  var ready bool
  // memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
  var group sync.WaitGroup
  // memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
  group.Add(1)
  // memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
  go func() {
    // memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
    defer group.Done()
    // memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
    ready = true
    // memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
  }()
  // memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
  for !ready {
  }
  // memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
  group.Wait()
  // memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
  fmt.Println("unsynchronized-read-completed")
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 57: Race On Shared Var

_ex-57 · exercises co-22, co-23, co-24_

This CSP example is rendered verbatim from `learning/code/ex-57-race-on-shared-var/main.go`.

```go
package main

import (
  // race on shared var: this diagnostic keeps synchronization and cleanup observable.
  "fmt"
  // race on shared var: this diagnostic keeps synchronization and cleanup observable.
  "os"
  // race on shared var: this diagnostic keeps synchronization and cleanup observable.
  "sync"
)

// race on shared var: this diagnostic keeps synchronization and cleanup observable.
func main() {
  // race on shared var: this diagnostic keeps synchronization and cleanup observable.
  if os.Getenv("RACE_DEMO") != "1" {
    // race on shared var: this diagnostic keeps synchronization and cleanup observable.
    fmt.Println("diagnostic: RACE_DEMO=1 go run -race main.go")
    // race on shared var: this diagnostic keeps synchronization and cleanup observable.
    return
  }
  // race on shared var: this diagnostic keeps synchronization and cleanup observable.
  counter := 0
  // race on shared var: this diagnostic keeps synchronization and cleanup observable.
  var group sync.WaitGroup
  // race on shared var: this diagnostic keeps synchronization and cleanup observable.
  for range 2 {
    // race on shared var: this diagnostic keeps synchronization and cleanup observable.
    group.Add(1)
    // race on shared var: this diagnostic keeps synchronization and cleanup observable.
    go func() {
      // race on shared var: this diagnostic keeps synchronization and cleanup observable.
      defer group.Done()
      // race on shared var: this diagnostic keeps synchronization and cleanup observable.
      for range 1000 {
        // race on shared var: this diagnostic keeps synchronization and cleanup observable.
        counter++
      }
      // race on shared var: this diagnostic keeps synchronization and cleanup observable.
    }()
  }
  // race on shared var: this diagnostic keeps synchronization and cleanup observable.
  group.Wait()
  // race on shared var: this diagnostic keeps synchronization and cleanup observable.
  fmt.Println("racy-counter", counter)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 58: Race Detector Output

_ex-58 · exercises co-22, co-23, co-24_

This CSP example is rendered verbatim from `learning/code/ex-58-race-detector-output/main.go`.

```go
package main

import (
  // race detector output: this diagnostic keeps synchronization and cleanup observable.
  "fmt"
  // race detector output: this diagnostic keeps synchronization and cleanup observable.
  "os"
  // race detector output: this diagnostic keeps synchronization and cleanup observable.
  "sync"
)

// race detector output: this diagnostic keeps synchronization and cleanup observable.
func main() {
  // race detector output: this diagnostic keeps synchronization and cleanup observable.
  if os.Getenv("RACE_DEMO") != "1" {
    // race detector output: this diagnostic keeps synchronization and cleanup observable.
    fmt.Println("run: RACE_DEMO=1 go run -race main.go")
    // race detector output: this diagnostic keeps synchronization and cleanup observable.
    fmt.Println("expect: WARNING: DATA RACE")
    // race detector output: this diagnostic keeps synchronization and cleanup observable.
    return
  }
  // race detector output: this diagnostic keeps synchronization and cleanup observable.
  value := 0
  // race detector output: this diagnostic keeps synchronization and cleanup observable.
  var group sync.WaitGroup
  // race detector output: this diagnostic keeps synchronization and cleanup observable.
  group.Add(2)
  // race detector output: this diagnostic keeps synchronization and cleanup observable.
  go func() {
    // race detector output: this diagnostic keeps synchronization and cleanup observable.
    defer group.Done()
    // race detector output: this diagnostic keeps synchronization and cleanup observable.
    value = 1
    // race detector output: this diagnostic keeps synchronization and cleanup observable.
  }()
  // race detector output: this diagnostic keeps synchronization and cleanup observable.
  go func() {
    // race detector output: this diagnostic keeps synchronization and cleanup observable.
    defer group.Done()
    // race detector output: this diagnostic keeps synchronization and cleanup observable.
    fmt.Println("read", value)
    // race detector output: this diagnostic keeps synchronization and cleanup observable.
  }()
  // race detector output: this diagnostic keeps synchronization and cleanup observable.
  group.Wait()
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 59: Race Fixed Mutex

_ex-59 · exercises co-22, co-23, co-24_

This CSP example is rendered verbatim from `learning/code/ex-59-race-fixed-mutex/main.go`.

```go
package main

import (
  // race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
  "fmt"
  // race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
  "sync"
)

// race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
func main() {
  // race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
  counter := 0
  // race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
  var lock sync.Mutex
  // race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
  var group sync.WaitGroup
  // race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
  for range 2 {
    // race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
    group.Add(1)
    // race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
    go func() {
      // race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
      defer group.Done()
      // race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
      for range 1000 {
        // race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
        lock.Lock()
        // race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
        counter++
        // race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
        lock.Unlock()
      }
      // race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
    }()
  }
  // race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
  group.Wait()
  // race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
  fmt.Println("mutex-counter", counter)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 60: Race Fixed Channel

_ex-60 · exercises co-22, co-23, co-24_

This CSP example is rendered verbatim from `learning/code/ex-60-race-fixed-channel/main.go`.

```go
package main

import (
  // race fixed channel: this diagnostic keeps synchronization and cleanup observable.
  "fmt"
  // race fixed channel: this diagnostic keeps synchronization and cleanup observable.
  "sync"
)

// race fixed channel: this diagnostic keeps synchronization and cleanup observable.
func main() {
  // race fixed channel: this diagnostic keeps synchronization and cleanup observable.
  increments := make(chan int)
  // race fixed channel: this diagnostic keeps synchronization and cleanup observable.
  total := make(chan int)
  // race fixed channel: this diagnostic keeps synchronization and cleanup observable.
  go func() {
    // race fixed channel: this diagnostic keeps synchronization and cleanup observable.
    counter := 0
    // race fixed channel: this diagnostic keeps synchronization and cleanup observable.
    for increment := range increments {
      // race fixed channel: this diagnostic keeps synchronization and cleanup observable.
      counter += increment
    }
    // race fixed channel: this diagnostic keeps synchronization and cleanup observable.
    total <- counter
    // race fixed channel: this diagnostic keeps synchronization and cleanup observable.
  }()
  // race fixed channel: this diagnostic keeps synchronization and cleanup observable.
  var senders sync.WaitGroup
  // race fixed channel: this diagnostic keeps synchronization and cleanup observable.
  for range 2 {
    // race fixed channel: this diagnostic keeps synchronization and cleanup observable.
    senders.Add(1)
    // race fixed channel: this diagnostic keeps synchronization and cleanup observable.
    go func() {
      // race fixed channel: this diagnostic keeps synchronization and cleanup observable.
      defer senders.Done()
      // race fixed channel: this diagnostic keeps synchronization and cleanup observable.
      for range 1000 {
        // race fixed channel: this diagnostic keeps synchronization and cleanup observable.
        increments <- 1
      }
      // race fixed channel: this diagnostic keeps synchronization and cleanup observable.
    }()
  }
  // race fixed channel: this diagnostic keeps synchronization and cleanup observable.
  senders.Wait()
  // race fixed channel: this diagnostic keeps synchronization and cleanup observable.
  close(increments)
  // race fixed channel: this diagnostic keeps synchronization and cleanup observable.
  fmt.Println("channel-owner-counter", <-total)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 61: Race Cost Note

_ex-61 · exercises co-22, co-23, co-24_

This CSP example is rendered verbatim from `learning/code/ex-61-race-cost-note/main.go`.

```go
package main

// race cost note: this diagnostic keeps synchronization and cleanup observable.
import "fmt"

// race cost note: this diagnostic keeps synchronization and cleanup observable.
func main() {
  // race cost note: this diagnostic keeps synchronization and cleanup observable.
  fmt.Println("benchmark with: GO111MODULE=off go test -race -bench=BenchmarkMutexCounter -benchtime=1x")
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 62: Goroutine Leak Blocked Send

_ex-62 · exercises co-22, co-23, co-24_

This CSP example is rendered verbatim from `learning/code/ex-62-goroutine-leak-blocked-send/main.go`.

```go
package main

import (
  // goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
  "fmt"
  // goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
  "runtime"
)

// goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
func main() {
  // goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
  out := make(chan int)
  // goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
  started := make(chan struct{})
  // goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
  baseline := runtime.NumGoroutine()
  // goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
  go func() {
    // goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
    close(started)
    // goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
    out <- 1
    // goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
  }()
  // goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
  <-started
  // goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
  fmt.Println("blocked-send-pending", runtime.NumGoroutine() > baseline)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 63: Goroutine Leak Fix Done

_ex-63 · exercises co-22, co-23, co-24_

This CSP example is rendered verbatim from `learning/code/ex-63-goroutine-leak-fix-done/main.go`.

```go
package main

import (
  // goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
  "fmt"
  // goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
  "sync"
)

// goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
func sendOrCancel(done <-chan struct{}, out chan<- int, group *sync.WaitGroup) {
  // goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
  defer group.Done()
  // goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
  select {
  // goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
  case out <- 1:
  // goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
  case <-done:
  }
}

// goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
func main() {
  // goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
  done := make(chan struct{})
  // goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
  out := make(chan int)
  // goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
  var group sync.WaitGroup
  // goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
  group.Add(1)
  // goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
  go sendOrCancel(done, out, &group)
  // goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
  close(done)
  // goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
  group.Wait()
  // goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
  fmt.Println("blocked-send-released-by-done")
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 64: Goroutine Leak Detect

_ex-64 · exercises co-22, co-23, co-24_

This CSP example is rendered verbatim from `learning/code/ex-64-goroutine-leak-detect/main.go`.

```go
package main

import (
  // goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
  "fmt"
  // goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
  "runtime"
)

// goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
func main() {
  // goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
  before := runtime.NumGoroutine()
  // goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
  done := make(chan struct{})
  // goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
  started := make(chan struct{})
  // goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
  exited := make(chan struct{})
  // goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
  go func() {
    // goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
    close(started)
    // goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
    <-done
    // goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
    close(exited)
    // goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
  }()
  // goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
  <-started
  // goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
  during := runtime.NumGoroutine()
  // goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
  close(done)
  // goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
  <-exited
  // goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
  runtime.Gosched()
  // goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
  after := runtime.NumGoroutine()
  // goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
  fmt.Println("goroutines", before, during, after)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 65: Deadlock All Asleep

_ex-65 · exercises co-22, co-23, co-24_

This CSP example is rendered verbatim from `learning/code/ex-65-deadlock-all-asleep/main.go`.

```go
package main

import (
  // deadlock all asleep: this step makes progress, ownership, or termination explicit.
  "fmt"
  // deadlock all asleep: this step makes progress, ownership, or termination explicit.
  "os"
)

// deadlock all asleep: this step makes progress, ownership, or termination explicit.
func main() {
  // deadlock all asleep: this step makes progress, ownership, or termination explicit.
  if os.Getenv("DEADLOCK_DEMO") != "1" {
    // deadlock all asleep: this step makes progress, ownership, or termination explicit.
    fmt.Println("diagnostic: DEADLOCK_DEMO=1 go run main.go")
    // deadlock all asleep: this step makes progress, ownership, or termination explicit.
    return
  }
  // deadlock all asleep: this step makes progress, ownership, or termination explicit.
  never := make(chan struct{})
  // deadlock all asleep: this step makes progress, ownership, or termination explicit.
  <-never
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 66: Deadlock Unbuffered Selfsend

_ex-66 · exercises co-22, co-23, co-24_

This CSP example is rendered verbatim from `learning/code/ex-66-deadlock-unbuffered-selfsend/main.go`.

```go
package main

import (
  // deadlock unbuffered selfsend: this step makes progress, ownership, or termination explicit.
  "fmt"
  // deadlock unbuffered selfsend: this step makes progress, ownership, or termination explicit.
  "os"
)

// deadlock unbuffered selfsend: this step makes progress, ownership, or termination explicit.
func main() {
  // deadlock unbuffered selfsend: this step makes progress, ownership, or termination explicit.
  if os.Getenv("DEADLOCK_DEMO") != "1" {
    // deadlock unbuffered selfsend: this step makes progress, ownership, or termination explicit.
    fmt.Println("diagnostic: DEADLOCK_DEMO=1 go run main.go")
    // deadlock unbuffered selfsend: this step makes progress, ownership, or termination explicit.
    return
  }
  // deadlock unbuffered selfsend: this step makes progress, ownership, or termination explicit.
  handoff := make(chan int)
  // deadlock unbuffered selfsend: this step makes progress, ownership, or termination explicit.
  handoff <- 1
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 67: Deadlock Fix

_ex-67 · exercises co-22, co-23, co-24_

This CSP example is rendered verbatim from `learning/code/ex-67-deadlock-fix/main.go`.

```go
package main

// deadlock fix: this step makes progress, ownership, or termination explicit.
import "fmt"

// deadlock fix: this step makes progress, ownership, or termination explicit.
func main() {
  // deadlock fix: this step makes progress, ownership, or termination explicit.
  handoff := make(chan int)
  // deadlock fix: this step makes progress, ownership, or termination explicit.
  go func() {
    // deadlock fix: this step makes progress, ownership, or termination explicit.
    handoff <- 1
    // deadlock fix: this step makes progress, ownership, or termination explicit.
  }()
  // deadlock fix: this step makes progress, ownership, or termination explicit.
  fmt.Println("received", <-handoff)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 68: Deadlock Circular Wait

_ex-68 · exercises co-22, co-23, co-24_

This CSP example is rendered verbatim from `learning/code/ex-68-deadlock-circular-wait/main.go`.

```go
package main

import (
  // deadlock circular wait: this step makes progress, ownership, or termination explicit.
  "fmt"
  // deadlock circular wait: this step makes progress, ownership, or termination explicit.
  "os"
)

// deadlock circular wait: this step makes progress, ownership, or termination explicit.
func main() {
  // deadlock circular wait: this step makes progress, ownership, or termination explicit.
  if os.Getenv("DEADLOCK_DEMO") != "1" {
    // deadlock circular wait: this step makes progress, ownership, or termination explicit.
    fmt.Println("diagnostic: DEADLOCK_DEMO=1 go run main.go")
    // deadlock circular wait: this step makes progress, ownership, or termination explicit.
    return
  }
  // deadlock circular wait: this step makes progress, ownership, or termination explicit.
  left := make(chan struct{})
  // deadlock circular wait: this step makes progress, ownership, or termination explicit.
  right := make(chan struct{})
  // deadlock circular wait: this step makes progress, ownership, or termination explicit.
  go func() {
    // deadlock circular wait: this step makes progress, ownership, or termination explicit.
    left <- struct{}{}
    // deadlock circular wait: this step makes progress, ownership, or termination explicit.
    <-right
    // deadlock circular wait: this step makes progress, ownership, or termination explicit.
  }()
  // deadlock circular wait: this step makes progress, ownership, or termination explicit.
  go func() {
    // deadlock circular wait: this step makes progress, ownership, or termination explicit.
    right <- struct{}{}
    // deadlock circular wait: this step makes progress, ownership, or termination explicit.
    <-left
    // deadlock circular wait: this step makes progress, ownership, or termination explicit.
  }()
  // deadlock circular wait: this step makes progress, ownership, or termination explicit.
  select {}
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 69: Pipeline Error Propagation

_ex-69 · exercises co-22, co-23, co-24_

This CSP example is rendered verbatim from `learning/code/ex-69-pipeline-error-propagation/main.go`.

```go
package main

import (
  // pipeline error propagation: this step makes progress, ownership, or termination explicit.
  "errors"
  // pipeline error propagation: this step makes progress, ownership, or termination explicit.
  "fmt"
)

// pipeline error propagation: this step makes progress, ownership, or termination explicit.
type result struct {
  // pipeline error propagation: this step makes progress, ownership, or termination explicit.
  value int
  // pipeline error propagation: this step makes progress, ownership, or termination explicit.
  err error
}

// pipeline error propagation: this step makes progress, ownership, or termination explicit.
func validateAndDouble(in <-chan int) <-chan result {
  // pipeline error propagation: this step makes progress, ownership, or termination explicit.
  out := make(chan result)
  // pipeline error propagation: this step makes progress, ownership, or termination explicit.
  go func() {
    // pipeline error propagation: this step makes progress, ownership, or termination explicit.
    defer close(out)
    // pipeline error propagation: this step makes progress, ownership, or termination explicit.
    for value := range in {
      // pipeline error propagation: this step makes progress, ownership, or termination explicit.
      if value < 0 {
        // pipeline error propagation: this step makes progress, ownership, or termination explicit.
        out <- result{err: errors.New("negative input")}
        // pipeline error propagation: this step makes progress, ownership, or termination explicit.
        return
      }
      // pipeline error propagation: this step makes progress, ownership, or termination explicit.
      out <- result{value: value * 2}
    }
    // pipeline error propagation: this step makes progress, ownership, or termination explicit.
  }()
  // pipeline error propagation: this step makes progress, ownership, or termination explicit.
  return out
}

// pipeline error propagation: this step makes progress, ownership, or termination explicit.
func main() {
  // pipeline error propagation: this step makes progress, ownership, or termination explicit.
  input := make(chan int, 3)
  // pipeline error propagation: this step makes progress, ownership, or termination explicit.
  input <- 2
  // pipeline error propagation: this step makes progress, ownership, or termination explicit.
  input <- -1
  // pipeline error propagation: this step makes progress, ownership, or termination explicit.
  input <- 4
  // pipeline error propagation: this step makes progress, ownership, or termination explicit.
  close(input)
  // pipeline error propagation: this step makes progress, ownership, or termination explicit.
  for item := range validateAndDouble(input) {
    // pipeline error propagation: this step makes progress, ownership, or termination explicit.
    if item.err != nil {
      // pipeline error propagation: this step makes progress, ownership, or termination explicit.
      fmt.Println("pipeline-error", item.err)
      // pipeline error propagation: this step makes progress, ownership, or termination explicit.
      return
    }
    // pipeline error propagation: this step makes progress, ownership, or termination explicit.
    fmt.Println("value", item.value)
  }
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 70: Bounded Parallelism

_ex-70 · exercises co-20, co-26_

This CSP example is rendered verbatim from `learning/code/ex-70-bounded-parallelism/main.go`.

```go
package main

import (
  // bounded parallelism: this step makes progress, ownership, or termination explicit.
  "fmt"
  // bounded parallelism: this step makes progress, ownership, or termination explicit.
  "sync"
  // bounded parallelism: this step makes progress, ownership, or termination explicit.
  "time"
)

// bounded parallelism: this step makes progress, ownership, or termination explicit.
func main() {
  // bounded parallelism: this step makes progress, ownership, or termination explicit.
  limit := make(chan struct{}, 2)
  // bounded parallelism: this step makes progress, ownership, or termination explicit.
  var group sync.WaitGroup
  // bounded parallelism: this step makes progress, ownership, or termination explicit.
  var lock sync.Mutex
  // bounded parallelism: this step makes progress, ownership, or termination explicit.
  active, peak := 0, 0
  // bounded parallelism: this step makes progress, ownership, or termination explicit.
  for task := 0; task < 6; task++ {
    // bounded parallelism: this step makes progress, ownership, or termination explicit.
    group.Add(1)
    // bounded parallelism: this step makes progress, ownership, or termination explicit.
    go func() {
      // bounded parallelism: this step makes progress, ownership, or termination explicit.
      defer group.Done()
      // bounded parallelism: this step makes progress, ownership, or termination explicit.
      limit <- struct{}{}
      // bounded parallelism: this step makes progress, ownership, or termination explicit.
      lock.Lock()
      // bounded parallelism: this step makes progress, ownership, or termination explicit.
      active++
      // bounded parallelism: this step makes progress, ownership, or termination explicit.
      if active > peak {
        // bounded parallelism: this step makes progress, ownership, or termination explicit.
        peak = active
      }
      // bounded parallelism: this step makes progress, ownership, or termination explicit.
      lock.Unlock()
      // bounded parallelism: this step makes progress, ownership, or termination explicit.
      time.Sleep(time.Millisecond)
      // bounded parallelism: this step makes progress, ownership, or termination explicit.
      lock.Lock()
      // bounded parallelism: this step makes progress, ownership, or termination explicit.
      active--
      // bounded parallelism: this step makes progress, ownership, or termination explicit.
      lock.Unlock()
      // bounded parallelism: this step makes progress, ownership, or termination explicit.
      <-limit
      // bounded parallelism: this step makes progress, ownership, or termination explicit.
    }()
  }
  // bounded parallelism: this step makes progress, ownership, or termination explicit.
  group.Wait()
  // bounded parallelism: this step makes progress, ownership, or termination explicit.
  fmt.Println("parallelism-limit-observed", peak)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 71: Context Value Request Scoped

_ex-71 · exercises co-20, co-26_

This CSP example is rendered verbatim from `learning/code/ex-71-context-value-request-scoped/main.go`.

```go
package main

import (
  // context value request scoped: this step makes progress, ownership, or termination explicit.
  "context"
  // context value request scoped: this step makes progress, ownership, or termination explicit.
  "fmt"
)

// context value request scoped: this step makes progress, ownership, or termination explicit.
type requestIDKey struct{}

// context value request scoped: this step makes progress, ownership, or termination explicit.
func handle(ctx context.Context) {
  // context value request scoped: this step makes progress, ownership, or termination explicit.
  requestID, _ := ctx.Value(requestIDKey{}).(string)
  // context value request scoped: this step makes progress, ownership, or termination explicit.
  fmt.Println("request-id", requestID)
}

// context value request scoped: this step makes progress, ownership, or termination explicit.
func main() {
  // context value request scoped: this step makes progress, ownership, or termination explicit.
  ctx := context.WithValue(context.Background(), requestIDKey{}, "req-42")
  // context value request scoped: this step makes progress, ownership, or termination explicit.
  handle(ctx)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 72: Select Fairness

_ex-72 · exercises co-20, co-26_

This CSP example is rendered verbatim from `learning/code/ex-72-select-fairness/main.go`.

```go
package main

// select fairness: this step makes progress, ownership, or termination explicit.
import "fmt"

// select fairness: this step makes progress, ownership, or termination explicit.
func main() {
  // select fairness: this step makes progress, ownership, or termination explicit.
  left := make(chan int, 1)
  // select fairness: this step makes progress, ownership, or termination explicit.
  right := make(chan int, 1)
  // select fairness: this step makes progress, ownership, or termination explicit.
  left <- 1
  // select fairness: this step makes progress, ownership, or termination explicit.
  right <- 1
  // select fairness: this step makes progress, ownership, or termination explicit.
  leftWins, rightWins := 0, 0
  // select fairness: this step makes progress, ownership, or termination explicit.
  for range 100 {
    // select fairness: this step makes progress, ownership, or termination explicit.
    select {
    // select fairness: this step makes progress, ownership, or termination explicit.
    case <-left:
      // select fairness: this step makes progress, ownership, or termination explicit.
      leftWins++
      // select fairness: this step makes progress, ownership, or termination explicit.
      left <- 1
    // select fairness: this step makes progress, ownership, or termination explicit.
    case <-right:
      // select fairness: this step makes progress, ownership, or termination explicit.
      rightWins++
      // select fairness: this step makes progress, ownership, or termination explicit.
      right <- 1
    }
  }
  // select fairness: this step makes progress, ownership, or termination explicit.
  fmt.Println("select-counts", leftWins, rightWins)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 73: Mutex Vs Channel Choice

_ex-73 · exercises co-20, co-26_

This CSP example is rendered verbatim from `learning/code/ex-73-mutex-vs-channel-choice/main.go`.

```go
package main

import (
  // mutex vs channel choice: this step makes progress, ownership, or termination explicit.
  "fmt"
  // mutex vs channel choice: this step makes progress, ownership, or termination explicit.
  "sync"
)

// mutex vs channel choice: this step makes progress, ownership, or termination explicit.
func main() {
  // mutex vs channel choice: this step makes progress, ownership, or termination explicit.
  var lock sync.Mutex
  // mutex vs channel choice: this step makes progress, ownership, or termination explicit.
  shared := 0
  // mutex vs channel choice: this step makes progress, ownership, or termination explicit.
  lock.Lock()
  // mutex vs channel choice: this step makes progress, ownership, or termination explicit.
  shared++
  // mutex vs channel choice: this step makes progress, ownership, or termination explicit.
  lock.Unlock()
  // mutex vs channel choice: this step makes progress, ownership, or termination explicit.
  updates := make(chan int)
  // mutex vs channel choice: this step makes progress, ownership, or termination explicit.
  total := make(chan int)
  // mutex vs channel choice: this step makes progress, ownership, or termination explicit.
  go func() {
    // mutex vs channel choice: this step makes progress, ownership, or termination explicit.
    sum := 0
    // mutex vs channel choice: this step makes progress, ownership, or termination explicit.
    for update := range updates {
      // mutex vs channel choice: this step makes progress, ownership, or termination explicit.
      sum += update
    }
    // mutex vs channel choice: this step makes progress, ownership, or termination explicit.
    total <- sum
    // mutex vs channel choice: this step makes progress, ownership, or termination explicit.
  }()
  // mutex vs channel choice: this step makes progress, ownership, or termination explicit.
  updates <- 1
  // mutex vs channel choice: this step makes progress, ownership, or termination explicit.
  updates <- 1
  // mutex vs channel choice: this step makes progress, ownership, or termination explicit.
  close(updates)
  // mutex vs channel choice: this step makes progress, ownership, or termination explicit.
  fmt.Println("mutex-for-shared-state", shared)
  // mutex vs channel choice: this step makes progress, ownership, or termination explicit.
  fmt.Println("channel-for-ownership", <-total)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 74: Csp Vs Actor Contrast

_ex-74 · exercises co-20, co-26_

This CSP example is rendered verbatim from `learning/code/ex-74-csp-vs-actor-contrast/main.go`.

```go
package main

// csp vs actor contrast: this step makes progress, ownership, or termination explicit.
import "fmt"

// csp vs actor contrast: this step makes progress, ownership, or termination explicit.
type increment struct {
  // csp vs actor contrast: this step makes progress, ownership, or termination explicit.
  reply chan int
}

// csp vs actor contrast: this step makes progress, ownership, or termination explicit.
func main() {
  // csp vs actor contrast: this step makes progress, ownership, or termination explicit.
  csp := make(chan int)
  // csp vs actor contrast: this step makes progress, ownership, or termination explicit.
  go func() {
    // csp vs actor contrast: this step makes progress, ownership, or termination explicit.
    csp <- 5
    // csp vs actor contrast: this step makes progress, ownership, or termination explicit.
  }()
  // csp vs actor contrast: this step makes progress, ownership, or termination explicit.
  fmt.Println("csp-handoff", <-csp)
  // csp vs actor contrast: this step makes progress, ownership, or termination explicit.
  mailbox := make(chan increment)
  // csp vs actor contrast: this step makes progress, ownership, or termination explicit.
  go func() {
    // csp vs actor contrast: this step makes progress, ownership, or termination explicit.
    state := 0
    // csp vs actor contrast: this step makes progress, ownership, or termination explicit.
    for message := range mailbox {
      // csp vs actor contrast: this step makes progress, ownership, or termination explicit.
      state++
      // csp vs actor contrast: this step makes progress, ownership, or termination explicit.
      message.reply <- state
    }
    // csp vs actor contrast: this step makes progress, ownership, or termination explicit.
  }()
  // csp vs actor contrast: this step makes progress, ownership, or termination explicit.
  reply := make(chan int)
  // csp vs actor contrast: this step makes progress, ownership, or termination explicit.
  mailbox <- increment{reply: reply}
  // csp vs actor contrast: this step makes progress, ownership, or termination explicit.
  fmt.Println("actor-mailbox-state", <-reply)
  // csp vs actor contrast: this step makes progress, ownership, or termination explicit.
  close(mailbox)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 75: Csp Synchronous Handoff

_ex-75 · exercises co-20, co-26_

This CSP example is rendered verbatim from `learning/code/ex-75-csp-synchronous-handoff/main.go`.

```go
package main

// csp synchronous handoff: this step makes progress, ownership, or termination explicit.
import "fmt"

// csp synchronous handoff: this step makes progress, ownership, or termination explicit.
func main() {
  // csp synchronous handoff: this step makes progress, ownership, or termination explicit.
  handoff := make(chan string)
  // csp synchronous handoff: this step makes progress, ownership, or termination explicit.
  sent := make(chan struct{})
  // csp synchronous handoff: this step makes progress, ownership, or termination explicit.
  go func() {
    // csp synchronous handoff: this step makes progress, ownership, or termination explicit.
    handoff <- "token"
    // csp synchronous handoff: this step makes progress, ownership, or termination explicit.
    close(sent)
    // csp synchronous handoff: this step makes progress, ownership, or termination explicit.
  }()
  // csp synchronous handoff: this step makes progress, ownership, or termination explicit.
  value := <-handoff
  // csp synchronous handoff: this step makes progress, ownership, or termination explicit.
  <-sent
  // csp synchronous handoff: this step makes progress, ownership, or termination explicit.
  fmt.Println("synchronous-handoff", value)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 76: Mini Worker Pool

_ex-76 · exercises co-20, co-26_

This CSP example is rendered verbatim from `learning/code/ex-76-mini-worker-pool/main.go`.

```go
package main

import (
  // mini worker pool: this step makes progress, ownership, or termination explicit.
  "fmt"
  // mini worker pool: this step makes progress, ownership, or termination explicit.
  "sync"
)

// mini worker pool: this step makes progress, ownership, or termination explicit.
func main() {
  // mini worker pool: this step makes progress, ownership, or termination explicit.
  jobs := make(chan int)
  // mini worker pool: this step makes progress, ownership, or termination explicit.
  results := make(chan int)
  // mini worker pool: this step makes progress, ownership, or termination explicit.
  var group sync.WaitGroup
  // mini worker pool: this step makes progress, ownership, or termination explicit.
  for range 2 {
    // mini worker pool: this step makes progress, ownership, or termination explicit.
    group.Add(1)
    // mini worker pool: this step makes progress, ownership, or termination explicit.
    go func() {
      // mini worker pool: this step makes progress, ownership, or termination explicit.
      defer group.Done()
      // mini worker pool: this step makes progress, ownership, or termination explicit.
      for job := range jobs {
        // mini worker pool: this step makes progress, ownership, or termination explicit.
        results <- job * job
      }
      // mini worker pool: this step makes progress, ownership, or termination explicit.
    }()
  }
  // mini worker pool: this step makes progress, ownership, or termination explicit.
  go func() {
    // mini worker pool: this step makes progress, ownership, or termination explicit.
    for _, job := range []int{2, 3, 4} {
      // mini worker pool: this step makes progress, ownership, or termination explicit.
      jobs <- job
    }
    // mini worker pool: this step makes progress, ownership, or termination explicit.
    close(jobs)
    // mini worker pool: this step makes progress, ownership, or termination explicit.
    group.Wait()
    // mini worker pool: this step makes progress, ownership, or termination explicit.
    close(results)
    // mini worker pool: this step makes progress, ownership, or termination explicit.
  }()
  // mini worker pool: this step makes progress, ownership, or termination explicit.
  total := 0
  // mini worker pool: this step makes progress, ownership, or termination explicit.
  for result := range results {
    // mini worker pool: this step makes progress, ownership, or termination explicit.
    total += result
  }
  // mini worker pool: this step makes progress, ownership, or termination explicit.
  fmt.Println("worker-pool-total", total)
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 77: Clean Shutdown Race Clean

_ex-77 · exercises co-20, co-26_

This CSP example is rendered verbatim from `learning/code/ex-77-clean-shutdown-race-clean/main.go`.

```go
package main

import (
  // clean shutdown race clean: this step makes progress, ownership, or termination explicit.
  "fmt"
  // clean shutdown race clean: this step makes progress, ownership, or termination explicit.
  "sync"
)

// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
func main() {
  // clean shutdown race clean: this step makes progress, ownership, or termination explicit.
  jobs := make(chan int, 3)
  // clean shutdown race clean: this step makes progress, ownership, or termination explicit.
  var group sync.WaitGroup
  // clean shutdown race clean: this step makes progress, ownership, or termination explicit.
  var lock sync.Mutex
  // clean shutdown race clean: this step makes progress, ownership, or termination explicit.
  processed := 0
  // clean shutdown race clean: this step makes progress, ownership, or termination explicit.
  group.Add(1)
  // clean shutdown race clean: this step makes progress, ownership, or termination explicit.
  go func() {
    // clean shutdown race clean: this step makes progress, ownership, or termination explicit.
    defer group.Done()
    // clean shutdown race clean: this step makes progress, ownership, or termination explicit.
    for job := range jobs {
      // clean shutdown race clean: this step makes progress, ownership, or termination explicit.
      lock.Lock()
      // clean shutdown race clean: this step makes progress, ownership, or termination explicit.
      processed += job
      // clean shutdown race clean: this step makes progress, ownership, or termination explicit.
      lock.Unlock()
    }
    // clean shutdown race clean: this step makes progress, ownership, or termination explicit.
  }()
  // clean shutdown race clean: this step makes progress, ownership, or termination explicit.
  jobs <- 1
  // clean shutdown race clean: this step makes progress, ownership, or termination explicit.
  jobs <- 2
  // clean shutdown race clean: this step makes progress, ownership, or termination explicit.
  jobs <- 3
  // clean shutdown race clean: this step makes progress, ownership, or termination explicit.
  close(jobs)
  // clean shutdown race clean: this step makes progress, ownership, or termination explicit.
  group.Wait()
  // clean shutdown race clean: this step makes progress, ownership, or termination explicit.
  lock.Lock()
  // clean shutdown race clean: this step makes progress, ownership, or termination explicit.
  fmt.Println("clean-shutdown-total", processed)
  // clean shutdown race clean: this step makes progress, ownership, or termination explicit.
  lock.Unlock()
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.

### Example 78: Concurrency Not Parallelism

_ex-78 · exercises co-20, co-26_

This CSP example is rendered verbatim from `learning/code/ex-78-concurrency-not-parallelism/main.go`.

```go
package main

import (
  // concurrency not parallelism: this step makes progress, ownership, or termination explicit.
  "fmt"
  // concurrency not parallelism: this step makes progress, ownership, or termination explicit.
  "runtime"
  // concurrency not parallelism: this step makes progress, ownership, or termination explicit.
  "sync"
)

// concurrency not parallelism: this step makes progress, ownership, or termination explicit.
func main() {
  // concurrency not parallelism: this step makes progress, ownership, or termination explicit.
  previous := runtime.GOMAXPROCS(1)
  // concurrency not parallelism: this step makes progress, ownership, or termination explicit.
  defer runtime.GOMAXPROCS(previous)
  // concurrency not parallelism: this step makes progress, ownership, or termination explicit.
  var group sync.WaitGroup
  // concurrency not parallelism: this step makes progress, ownership, or termination explicit.
  for range 2 {
    // concurrency not parallelism: this step makes progress, ownership, or termination explicit.
    group.Add(1)
    // concurrency not parallelism: this step makes progress, ownership, or termination explicit.
    go func() {
      // concurrency not parallelism: this step makes progress, ownership, or termination explicit.
      defer group.Done()
      // concurrency not parallelism: this step makes progress, ownership, or termination explicit.
      fmt.Println("independent-concurrent-task")
      // concurrency not parallelism: this step makes progress, ownership, or termination explicit.
    }()
  }
  // concurrency not parallelism: this step makes progress, ownership, or termination explicit.
  group.Wait()
  // concurrency not parallelism: this step makes progress, ownership, or termination explicit.
  fmt.Println("gomaxprocs", runtime.GOMAXPROCS(0))
}
```

**Run**: `go run main.go`.

**Key takeaway**: make synchronization, cancellation, and ownership explicit.
