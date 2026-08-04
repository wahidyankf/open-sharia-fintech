---
title: "Beginner Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 10
---

Examples 1–26 establish Go's daily toolchain, executable package shape, modules, values, types,
functions, control flow, and deterministic cleanup. Each source lives beside the rendered example.

### Example 1: Hello World and Run

_ex-01 · exercises co-02, co-01_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-01-hello-world-run/main.go`.

```go
// => hello world run: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => hello world run: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => hello world run: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println("hello, Go") }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 2: Initialize a Module

_ex-02 · exercises co-03, co-01_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-02-go-mod-init/main.go`.

```go
// => go mod init: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => go mod init: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => go mod init: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  // Run: go mod init example/hello
  // That command writes go.mod; this program belongs to that module.
  // => go mod init: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  fmt.Println("module example/hello is ready")
  // => go mod init: marks one deliberate step in the go mod init example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 3: Build a Binary

_ex-03 · exercises co-01_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-03-go-build-binary/main.go`.

```go
// => go build binary: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => go build binary: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => go build binary: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  // Build with: go build -o hello main.go
  // The resulting hello executable can run without go run.
  // => go build binary: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  fmt.Println("hello binary")
  // => go build binary: marks one deliberate step in the go build binary example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 4: Compare Run and Build

_ex-04 · exercises co-01_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-04-go-run-vs-build/main.go`.

```go
// => go run vs build: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => go run vs build: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => go run vs build: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  // go run compiles and immediately executes a temporary program.
  // go build leaves a named executable as the release artifact.
  // => go run vs build: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  fmt.Println("compare go run . with go build -o hello")
  // => go run vs build: marks one deliberate step in the go run vs build example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 5: Use a Package and Import

_ex-05 · exercises co-02_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-05-package-and-import/main.go`.

```go
// => package and import: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => package and import: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
  // => package and import: marks one deliberate step in the package and import example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "fmt"
  // => package and import: marks one deliberate step in the package and import example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "example/package-import/greet"
  // => package and import: marks one deliberate step in the package and import example.
  // => keeps the mechanism inspectable before it is composed with another concern.
)

// => package and import: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  // Imports are explicit; an unused import is a compile error.
  // => package and import: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  fmt.Println(greet.Message("Go"))
  // => package and import: marks one deliberate step in the package and import example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}
```

**Run**: `go run .` from this example directory; inspect `greet/greet.go` for the imported package.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 6: Declare Variables

_ex-06 · exercises co-04_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-06-var-declaration/main.go`.

```go
// => var declaration: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => var declaration: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => var declaration: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { var name string = "Ada"; var year int = 2026; fmt.Println(name, year) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 7: Use Short Variable Declarations

_ex-07 · exercises co-04_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-07-short-var-decl/main.go`.

```go
// => short var decl: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => short var decl: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => short var decl: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { name := "Ada"; fmt.Printf("%s is %T\n", name, name) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 8: Inspect Zero Values

_ex-08 · exercises co-04_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-08-zero-values/main.go`.

```go
// => zero values: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => zero values: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => zero values: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  var n int
  var s string
  var ok bool
  var p *int
  fmt.Printf("%d %q %t %v\n", n, s, ok, p)
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 9: Group Constants

_ex-09 · exercises co-05_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-09-const-block/main.go`.

```go
// => const block: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => const block: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => const block: marks one deliberate step in the const block example.
// => keeps the mechanism inspectable before it is composed with another concern.
const (
  AppName     = "ship"
  DefaultPort = 8080
)

// => const block: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println(AppName, DefaultPort) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 10: Generate an Enum with iota

_ex-10 · exercises co-05_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-10-iota-enum/main.go`.

```go
// => iota enum: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => iota enum: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => iota enum: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type state int

// => iota enum: marks one deliberate step in the iota enum example.
// => keeps the mechanism inspectable before it is composed with another concern.
const (
  queued state = iota
  running
  done
)

// => iota enum: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println(queued, running, done) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 11: Convert Numeric Types

_ex-11 · exercises co-06_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-11-int-float-types/main.go`.

```go
// => int float types: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => int float types: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => int float types: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { n := 3; f := 2.5; fmt.Println(float64(n) * f) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 12: Compare Bytes and Runes

_ex-12 · exercises co-06_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-12-string-rune-byte/main.go`.

```go
// => string rune byte: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => string rune byte: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => string rune byte: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { s := "€"; fmt.Println(len(s), []rune(s), s[0]) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 13: Convert Explicitly

_ex-13 · exercises co-06_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-13-type-conversion/main.go`.

```go
// => type conversion: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => type conversion: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => type conversion: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { n := 7; var wide int64 = int64(n); fmt.Println(float64(wide)) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 14: Use Boolean Short-Circuiting

_ex-14 · exercises co-06_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-14-bool-and-comparison/main.go`.

```go
// => bool and comparison: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => bool and comparison: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => bool and comparison: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  calls := 0
  ready := false && func() bool { calls++; return true }()
  fmt.Println(ready, calls)
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 15: Write a Basic Function

_ex-15 · exercises co-07_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-15-func-basic/main.go`.

```go
// => func basic: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => func basic: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => func basic: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func twice(n int) int { return n * 2 }
func main()           { fmt.Println(twice(4)) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 16: Return a Value and Error

_ex-16 · exercises co-07_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-16-func-multiple-return/main.go`.

```go
// => func multiple return: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => func multiple return: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
  // => func multiple return: marks one deliberate step in the func multiple return example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "errors"
  // => func multiple return: marks one deliberate step in the func multiple return example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "fmt"
  // => func multiple return: marks one deliberate step in the func multiple return example.
  // => keeps the mechanism inspectable before it is composed with another concern.
)

// => func multiple return: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func divide(a, b int) (int, error) {
  if b == 0 {
    return 0, errors.New("zero divisor")
  }
  return a / b, nil
}

// => func multiple return: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { q, err := divide(8, 2); fmt.Println(q, err) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 17: Return Named Values

_ex-17 · exercises co-07_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-17-named-return-values/main.go`.

```go
// => named return values: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => named return values: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => named return values: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func bounds(values []int) (small, large int) {
  // => named return values: marks one deliberate step in the named return values example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  small, large = values[0], values[0]
  // => named return values: uses Go’s single loop keyword for iteration.
  // => keeps the loop state and termination condition local.
  for _, value := range values {
    // => named return values: makes the branch condition explicit rather than exceptional.
    // => keeps success and failure control flow visible.
    if value < small {
      small = value
    }
    // => named return values: makes the branch condition explicit rather than exceptional.
    // => keeps success and failure control flow visible.
    if value > large {
      large = value
    }
    // => named return values: marks one deliberate step in the named return values example.
    // => keeps the mechanism inspectable before it is composed with another concern.
  }
  // => named return values: returns a value through Go’s ordinary control-flow mechanism.
  // => keeps the caller responsible for the next decision.
  return
  // => named return values: marks one deliberate step in the named return values example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}

// => named return values: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println(bounds([]int{3, 1, 4})) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 18: Accept Variadic Arguments

_ex-18 · exercises co-07_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-18-variadic-func/main.go`.

```go
// => variadic func: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => variadic func: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => variadic func: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func sum(values ...int) int {
  // => variadic func: marks one deliberate step in the variadic func example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  total := 0
  // => variadic func: uses Go’s single loop keyword for iteration.
  // => keeps the loop state and termination condition local.
  for _, value := range values {
    total += value
  }
  // => variadic func: returns a value through Go’s ordinary control-flow mechanism.
  // => keeps the caller responsible for the next decision.
  return total
  // => variadic func: marks one deliberate step in the variadic func example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}

// => variadic func: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  // => variadic func: marks one deliberate step in the variadic func example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  values := []int{4, 5}
  // => variadic func: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  fmt.Println(sum(1, 2, 3), sum(values...))
  // => variadic func: marks one deliberate step in the variadic func example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 19: Scope a Value in an if

_ex-19 · exercises co-08_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-19-if-with-init/main.go`.

```go
// => if with init: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => if with init: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
  // => if with init: marks one deliberate step in the if with init example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "errors"
  // => if with init: marks one deliberate step in the if with init example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "fmt"
  // => if with init: marks one deliberate step in the if with init example.
  // => keeps the mechanism inspectable before it is composed with another concern.
)

// => if with init: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func lookup(ok bool) (string, error) {
  // => if with init: makes the branch condition explicit rather than exceptional.
  // => keeps success and failure control flow visible.
  if !ok {
    return "", errors.New("missing")
  }
  // => if with init: returns a value through Go’s ordinary control-flow mechanism.
  // => keeps the caller responsible for the next decision.
  return "release", nil
  // => if with init: marks one deliberate step in the if with init example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}

// => if with init: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  // => if with init: makes the branch condition explicit rather than exceptional.
  // => keeps success and failure control flow visible.
  if name, err := lookup(true); err != nil {
    fmt.Println(err)
  } else {
    fmt.Println(name)
  }
  // => if with init: marks one deliberate step in the if with init example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 20: Use a C-Style for Loop

_ex-20 · exercises co-08_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-20-for-c-style/main.go`.

```go
// => for c style: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => for c style: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => for c style: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  // => for c style: uses Go’s single loop keyword for iteration.
  // => keeps the loop state and termination condition local.
  for i := 0; i < 3; i++ {
    // => for c style: makes the observable result visible in stdout.
    // => gives the learner a direct value to verify.
    fmt.Println(i)
    // => for c style: marks one deliberate step in the for c style example.
    // => keeps the mechanism inspectable before it is composed with another concern.
  }
  // => for c style: marks one deliberate step in the for c style example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 21: Use a While-Style for Loop

_ex-21 · exercises co-08_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-21-for-while-style/main.go`.

```go
// => for while style: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => for while style: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => for while style: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  // => for while style: marks one deliberate step in the for while style example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  remaining := 3
  // => for while style: uses Go’s single loop keyword for iteration.
  // => keeps the loop state and termination condition local.
  for remaining > 0 {
    // => for while style: makes the observable result visible in stdout.
    // => gives the learner a direct value to verify.
    fmt.Println(remaining)
    // => for while style: marks one deliberate step in the for while style example.
    // => keeps the mechanism inspectable before it is composed with another concern.
    remaining--
    // => for while style: marks one deliberate step in the for while style example.
    // => keeps the mechanism inspectable before it is composed with another concern.
  }
  // => for while style: marks one deliberate step in the for while style example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 22: Range over Collections

_ex-22 · exercises co-08_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-22-for-range/main.go`.

```go
// => for range: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => for range: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => for range: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  // => for range: uses Go’s single loop keyword for iteration.
  // => keeps the loop state and termination condition local.
  for index, value := range []string{"go", "rust"} {
    fmt.Println(index, value)
  }
  // => for range: uses Go’s single loop keyword for iteration.
  // => keeps the loop state and termination condition local.
  for key, value := range map[string]int{"ok": 1} {
    fmt.Println(key, value)
  }
  // => for range: marks one deliberate step in the for range example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 23: Dispatch with switch

_ex-23 · exercises co-08_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-23-switch-statement/main.go`.

```go
// => switch statement: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => switch statement: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => switch statement: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  // => switch statement: selects one explicit branch without implicit fallthrough.
  // => keeps dispatch readable at the call site.
  switch command := "check"; command {
  // => switch statement: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  case "check":
    fmt.Println("validating")
  // => switch statement: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  case "publish":
    fmt.Println("releasing")
  // => switch statement: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  default:
    fmt.Println("unknown")
    // => switch statement: marks one deliberate step in the switch statement example.
    // => keeps the mechanism inspectable before it is composed with another concern.
  }
  // => switch statement: marks one deliberate step in the switch statement example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 24: Use a Conditionless switch

_ex-24 · exercises co-08_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-24-switch-no-condition/main.go`.

```go
// => switch no condition: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => switch no condition: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => switch no condition: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  // => switch no condition: marks one deliberate step in the switch no condition example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  n := -2
  // => switch no condition: selects one explicit branch without implicit fallthrough.
  // => keeps dispatch readable at the call site.
  switch {
  // => switch no condition: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  case n > 0:
    fmt.Println("positive")
  // => switch no condition: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  case n < 0:
    fmt.Println("negative")
  // => switch no condition: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  default:
    fmt.Println("zero")
    // => switch no condition: marks one deliberate step in the switch no condition example.
    // => keeps the mechanism inspectable before it is composed with another concern.
  }
  // => switch no condition: marks one deliberate step in the switch no condition example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 25: Defer Cleanup

_ex-25 · exercises co-09_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-25-defer-basic/main.go`.

```go
// => defer basic: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => defer basic: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => defer basic: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func closeResource() { fmt.Println("cleanup") }

// => defer basic: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  // => defer basic: marks one deliberate step in the defer basic example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  defer closeResource()
  // => defer basic: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  fmt.Println("work")
  // => defer basic: marks one deliberate step in the defer basic example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.

### Example 26: Observe Defer LIFO Order

_ex-26 · exercises co-09_

This small program isolates the Go rule before later examples combine it with data structures,
interfaces, errors, or concurrency. The code block is rendered verbatim from `learning/code/ex-26-defer-lifo-order/main.go`.

```go
// => defer lifo order: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => defer lifo order: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => defer lifo order: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  // => defer lifo order: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  defer fmt.Println("first deferred")
  // => defer lifo order: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  defer fmt.Println("second deferred")
  // => defer lifo order: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  defer fmt.Println("third deferred")
  // => defer lifo order: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  fmt.Println("body")
  // => defer lifo order: marks one deliberate step in the defer lifo order example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the output demonstrates the stated language rule without relying on a
previous example.

**Key takeaway**: Go favors a small, explicit surface that is easy to read and verify.
