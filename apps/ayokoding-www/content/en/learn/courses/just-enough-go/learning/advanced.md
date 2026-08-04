---
title: "Advanced Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 30
---

Examples 55–78 apply JSON, generics, a deliberately shallow concurrency preview, testing,
formatting, and context cancellation. CSP depth belongs in the next course.

### Example 55: Round-Trip JSON

_ex-55 · exercises co-18_

Round-Trip JSON is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-55-json-marshal-unmarshal/main.go` so
the page and runnable artifact cannot drift.

```go
// => json marshal unmarshal: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => json marshal unmarshal: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
  // => json marshal unmarshal: marks one deliberate step in the json marshal unmarshal example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "encoding/json"
  // => json marshal unmarshal: marks one deliberate step in the json marshal unmarshal example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "fmt"
  // => json marshal unmarshal: marks one deliberate step in the json marshal unmarshal example.
  // => keeps the mechanism inspectable before it is composed with another concern.
)

// => json marshal unmarshal: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Release struct {
  Name string `json:"name"`
}

// => json marshal unmarshal: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  original := Release{Name: "ship"}
  bytes, _ := json.Marshal(original)
  var decoded Release
  json.Unmarshal(bytes, &decoded)
  fmt.Println(decoded == original)
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 56: Omit an Empty JSON Field

_ex-56 · exercises co-18_

Omit an Empty JSON Field is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-56-json-omitempty/main.go` so
the page and runnable artifact cannot drift.

```go
// => json omitempty: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => json omitempty: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
  // => json omitempty: marks one deliberate step in the json omitempty example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "encoding/json"
  // => json omitempty: marks one deliberate step in the json omitempty example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "fmt"
  // => json omitempty: marks one deliberate step in the json omitempty example.
  // => keeps the mechanism inspectable before it is composed with another concern.
)

// => json omitempty: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Release struct {
  Name string `json:"name,omitempty"`
}

// => json omitempty: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { bytes, _ := json.Marshal(Release{}); fmt.Println(string(bytes)) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 57: Write a Generic Function

_ex-57 · exercises co-19_

Write a Generic Function is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-57-generic-function/main.go` so
the page and runnable artifact cannot drift.

```go
// => generic function: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => generic function: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => generic function: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func Map[T, U any](values []T, transform func(T) U) []U {
  result := make([]U, len(values))
  for i, value := range values {
    result[i] = transform(value)
  }
  return result
}

// => generic function: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println(Map([]int{1, 2}, func(value int) string { return fmt.Sprint(value) })) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 58: Constrain a Generic Number

_ex-58 · exercises co-19_

Constrain a Generic Number is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-58-generic-constraint/main.go` so
the page and runnable artifact cannot drift.

```go
// => generic constraint: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => generic constraint: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => generic constraint: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Number interface{ int | float64 }

// => generic constraint: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func Double[T Number](value T) T { return value + value }

// => generic constraint: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println(Double(3), Double(2.5)) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 59: Use a Comparable Constraint

_ex-59 · exercises co-19_

Use a Comparable Constraint is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-59-comparable-constraint/main.go` so
the page and runnable artifact cannot drift.

```go
// => comparable constraint: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => comparable constraint: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => comparable constraint: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func Contains[T comparable](values []T, wanted T) bool {
  for _, value := range values {
    if value == wanted {
      return true
    }
  }
  return false
}

// => comparable constraint: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println(Contains([]string{"go", "rust"}, "go")) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 60: Start a Goroutine

_ex-60 · exercises co-20_

Start a Goroutine is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-60-goroutine-preview/main.go` so
the page and runnable artifact cannot drift.

```go
// => goroutine preview: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => goroutine preview: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
  // => goroutine preview: marks one deliberate step in the goroutine preview example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "fmt"
  // => goroutine preview: marks one deliberate step in the goroutine preview example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "sync"
  // => goroutine preview: marks one deliberate step in the goroutine preview example.
  // => keeps the mechanism inspectable before it is composed with another concern.
)

// => goroutine preview: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  var wait sync.WaitGroup
  wait.Add(1)
  go func() { defer wait.Done(); fmt.Println("goroutine") }()
  wait.Wait()
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 61: Start an Anonymous Goroutine

_ex-61 · exercises co-20_

Start an Anonymous Goroutine is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-61-goroutine-anonymous/main.go` so
the page and runnable artifact cannot drift.

```go
// => goroutine anonymous: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => goroutine anonymous: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
  // => goroutine anonymous: marks one deliberate step in the goroutine anonymous example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "fmt"
  // => goroutine anonymous: marks one deliberate step in the goroutine anonymous example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "sync"
  // => goroutine anonymous: marks one deliberate step in the goroutine anonymous example.
  // => keeps the mechanism inspectable before it is composed with another concern.
)

// => goroutine anonymous: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  var wait sync.WaitGroup
  wait.Add(1)
  go func(label string) { defer wait.Done(); fmt.Println(label) }("anonymous")
  wait.Wait()
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 62: Synchronize with an Unbuffered Channel

_ex-62 · exercises co-21_

Synchronize with an Unbuffered Channel is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-62-unbuffered-channel/main.go` so
the page and runnable artifact cannot drift.

```go
// => unbuffered channel: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => unbuffered channel: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => unbuffered channel: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { values := make(chan int); go func() { values <- 7 }(); fmt.Println(<-values) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 63: Buffer a Channel

_ex-63 · exercises co-21_

Buffer a Channel is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-63-buffered-channel/main.go` so
the page and runnable artifact cannot drift.

```go
// => buffered channel: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => buffered channel: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => buffered channel: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { values := make(chan int, 2); values <- 1; values <- 2; fmt.Println(<-values, <-values) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 64: Hand Off a Channel Value

_ex-64 · exercises co-21_

Hand Off a Channel Value is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-64-channel-handoff/main.go` so
the page and runnable artifact cannot drift.

```go
// => channel handoff: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => channel handoff: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => channel handoff: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { result := make(chan string); go func() { result <- "ship" }(); fmt.Println(<-result) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 65: Close and Range a Channel

_ex-65 · exercises co-21_

Close and Range a Channel is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-65-channel-close-range/main.go` so
the page and runnable artifact cannot drift.

```go
// => channel close range: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => Closing signals that no more values will be sent.
// => Range drains received values and stops only after closure.

// => channel close range: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => channel close range: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  values := make(chan int, 2)
  values <- 1
  values <- 2
  close(values)
  for value := range values {
    fmt.Println(value)
  }
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 66: Detect a Closed Channel

_ex-66 · exercises co-21_

Detect a Closed Channel is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-66-channel-comma-ok/main.go` so
the page and runnable artifact cannot drift.

```go
// => channel comma ok: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => channel comma ok: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => channel comma ok: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  values := make(chan int)
  close(values)
  value, open := <-values
  fmt.Println(value, open)
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 67: Select a Ready Channel

_ex-67 · exercises co-22_

Select a Ready Channel is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-67-select-basic/main.go` so
the page and runnable artifact cannot drift.

```go
// => select basic: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => Select waits for one of several channel operations to become ready.
// => One ready case is chosen without serially blocking on the other.
// => The printed branch is intentionally nondeterministic when both channels are ready.
// => The lesson is readiness selection, not an ordering guarantee.

// => select basic: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => select basic: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  left, right := make(chan string, 1), make(chan string, 1)
  left <- "left"
  right <- "right"
  select {
  case value := <-left:
    fmt.Println(value)
  case value := <-right:
    fmt.Println(value)
  }
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 68: Use a Non-Blocking Select

_ex-68 · exercises co-22_

Use a Non-Blocking Select is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-68-select-default-nonblock/main.go` so
the page and runnable artifact cannot drift.

```go
// => select default nonblock: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => A default branch makes this select non-blocking when no send or receive is ready.
// => That is a polling tool, not a substitute for cancellation design.

// => select default nonblock: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => select default nonblock: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  values := make(chan int)
  select {
  case value := <-values:
    fmt.Println(value)
  default:
    fmt.Println("not ready")
  }
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 69: Select with a Timeout

_ex-69 · exercises co-22_

Select with a Timeout is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-69-select-timeout/main.go` so
the page and runnable artifact cannot drift.

```go
// => select timeout: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => select timeout: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
  // => select timeout: marks one deliberate step in the select timeout example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "fmt"
  // => select timeout: marks one deliberate step in the select timeout example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "time"
  // => select timeout: marks one deliberate step in the select timeout example.
  // => keeps the mechanism inspectable before it is composed with another concern.
)

// => select timeout: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  select {
  case <-time.After(time.Millisecond):
    fmt.Println("timed out")
  }
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 70: Coordinate with a WaitGroup

_ex-70 · exercises co-23_

Coordinate with a WaitGroup is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-70-waitgroup/main.go` so
the page and runnable artifact cannot drift.

```go
// => waitgroup: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => waitgroup: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
  // => waitgroup: marks one deliberate step in the waitgroup example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "fmt"
  // => waitgroup: marks one deliberate step in the waitgroup example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "sync"
  // => waitgroup: marks one deliberate step in the waitgroup example.
  // => keeps the mechanism inspectable before it is composed with another concern.
)

// => waitgroup: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  var wait sync.WaitGroup
  for i := 0; i < 2; i++ {
    wait.Add(1)
    go func(value int) { defer wait.Done(); fmt.Println(value) }(i)
  }
  wait.Wait()
  fmt.Println("all done")
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 71: Guard State with a Mutex

_ex-71 · exercises co-23_

Guard State with a Mutex is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-71-mutex/main.go` so
the page and runnable artifact cannot drift.

```go
// => mutex: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => mutex: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
  // => mutex: marks one deliberate step in the mutex example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "fmt"
  // => mutex: marks one deliberate step in the mutex example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "sync"
  // => mutex: marks one deliberate step in the mutex example.
  // => keeps the mechanism inspectable before it is composed with another concern.
)

// => mutex: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  var mutex sync.Mutex
  count := 0
  var wait sync.WaitGroup
  for i := 0; i < 2; i++ {
    wait.Add(1)
    go func() { defer wait.Done(); mutex.Lock(); defer mutex.Unlock(); count++ }()
  }
  wait.Wait()
  fmt.Println(count)
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 72: Write a Basic Test

_ex-72 · exercises co-24_

Write a Basic Test is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-72-test-basic/main.go` so
the page and runnable artifact cannot drift.

```go
// => test basic: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => test basic: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => test basic: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func double(value int) int { return value * 2 }

// => test basic: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println(double(4)); fmt.Println("Put TestDouble in main_test.go and run go test") }
```

**Companion test source (`main_test.go`)**:

```go
package main

import "testing"

func TestDouble(t *testing.T) {
  if got := double(2); got != 4 {
    t.Fatalf("double(2) = %d", got)
  }
}
```

Run `go test` to exercise this exact test source.

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 73: Use a Table-Driven Test

_ex-73 · exercises co-24_

Use a Table-Driven Test is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-73-table-driven-test/main.go` so
the page and runnable artifact cannot drift.

```go
// => table driven test: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => table driven test: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => table driven test: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func double(value int) int { return value * 2 }

// => table driven test: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  for _, test := range []struct{ in, want int }{{2, 4}, {3, 6}} {
    fmt.Println(double(test.in) == test.want)
  }
}
```

**Companion test source (`main_test.go`)**:

```go
package main

import "testing"

func TestDoubleCases(t *testing.T) {
  for _, test := range []struct{ in, want int }{{2, 4}, {3, 6}} {
    if got := double(test.in); got != test.want {
      t.Fatalf("double(%d) = %d", test.in, got)
    }
  }
}
```

Run `go test` to exercise this exact test source.

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 74: Name Subtests

_ex-74 · exercises co-24_

Name Subtests is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-74-subtests-run/main.go` so
the page and runnable artifact cannot drift.

```go
// => subtests run: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => subtests run: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => subtests run: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  for _, name := range []string{"positive", "zero"} {
    fmt.Println("subtest:", name)
  }
}
```

**Companion test source (`main_test.go`)**:

```go
package main

import "testing"

func TestNamedCases(t *testing.T) {
  for _, name := range []string{"positive", "zero"} {
    t.Run(name, func(t *testing.T) { t.Log(name) })
  }
}
```

Run `go test` to exercise this exact test source.

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 75: Format with gofmt

_ex-75 · exercises co-25_

Format with gofmt is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-75-gofmt-format/main.go` so
the page and runnable artifact cannot drift.

```go
// => gofmt format: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => gofmt format: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => gofmt format: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println("run gofmt -w main.go to normalize this source") }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 76: Apply Exported Naming

_ex-76 · exercises co-25_

Apply Exported Naming is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-76-effective-go-naming/main.go` so
the page and runnable artifact cannot drift.

```go
// => effective go naming: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => effective go naming: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => effective go naming: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Release struct{ Name string }

// => effective go naming: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func newRelease(name string) Release { return Release{Name: name} }

// => effective go naming: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println(newRelease("ship").Name) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 77: Cancel a Context

_ex-77 · exercises co-26_

Cancel a Context is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-77-context-cancel/main.go` so
the page and runnable artifact cannot drift.

```go
// => context cancel: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => context cancel: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
  // => context cancel: marks one deliberate step in the context cancel example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "context"
  // => context cancel: marks one deliberate step in the context cancel example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "fmt"
  // => context cancel: marks one deliberate step in the context cancel example.
  // => keeps the mechanism inspectable before it is composed with another concern.
)

// => context cancel: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  ctx, cancel := context.WithCancel(context.Background())
  cancel()
  <-ctx.Done()
  fmt.Println(ctx.Err() == context.Canceled)
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 78: Time Out a Context

_ex-78 · exercises co-26_

Time Out a Context is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-78-context-timeout/main.go` so
the page and runnable artifact cannot drift.

```go
// => context timeout: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => context timeout: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
  // => context timeout: marks one deliberate step in the context timeout example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "context"
  // => context timeout: marks one deliberate step in the context timeout example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "fmt"
  // => context timeout: marks one deliberate step in the context timeout example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "time"
  // => context timeout: marks one deliberate step in the context timeout example.
  // => keeps the mechanism inspectable before it is composed with another concern.
)

// => context timeout: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  ctx, cancel := context.WithTimeout(context.Background(), time.Millisecond)
  defer cancel()
  <-ctx.Done()
  fmt.Println(ctx.Err() == context.DeadlineExceeded)
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.
