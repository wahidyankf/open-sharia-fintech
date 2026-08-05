---
title: "Intermediate Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 20
---

Examples 27–54 cover collections, pointers, composition, receivers, interfaces, error values, and
JSON. Each has a colocated runnable source.

### Example 27: Compare an Array and Slice

_ex-27 · exercises co-10_

Compare an Array and Slice is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-27-array-vs-slice/main.go` so
the page and runnable artifact cannot drift.

```go
// => array vs slice: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => array vs slice: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => array vs slice: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  // => array vs slice: marks one deliberate step in the array vs slice example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  array := [3]int{1, 2, 3}
  // => array vs slice: marks one deliberate step in the array vs slice example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  slice := []int{1, 2, 3}
  // => array vs slice: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  fmt.Println(array, slice)
  // => array vs slice: marks one deliberate step in the array vs slice example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 28: Append to a Slice

_ex-28 · exercises co-10_

Append to a Slice is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-28-slice-append/main.go` so
the page and runnable artifact cannot drift.

```go
// => slice append: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => slice append: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => slice append: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  // => slice append: marks one deliberate step in the slice append example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  values := []int{1, 2}
  // => slice append: marks one deliberate step in the slice append example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  values = append(values, 3)
  // => slice append: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  fmt.Println(values)
  // => slice append: marks one deliberate step in the slice append example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 29: Inspect Slice Length and Capacity

_ex-29 · exercises co-10_

Inspect Slice Length and Capacity is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-29-slice-len-cap/main.go` so
the page and runnable artifact cannot drift.

```go
// => slice len cap: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => slice len cap: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => slice len cap: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  // => slice len cap: marks one deliberate step in the slice len cap example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  values := make([]int, 0, 2)
  // => slice len cap: uses Go’s single loop keyword for iteration.
  // => keeps the loop state and termination condition local.
  for i := 0; i < 3; i++ {
    values = append(values, i)
    fmt.Println(len(values), cap(values))
  }
  // => slice len cap: marks one deliberate step in the slice len cap example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 30: Allocate Slice Capacity

_ex-30 · exercises co-10_

Allocate Slice Capacity is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-30-make-slice-capacity/main.go` so
the page and runnable artifact cannot drift.

```go
// => make slice capacity: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => make slice capacity: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => make slice capacity: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  // => make slice capacity: marks one deliberate step in the make slice capacity example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  values := make([]int, 0, 10)
  // => make slice capacity: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  fmt.Println(len(values), cap(values))
  // => make slice capacity: marks one deliberate step in the make slice capacity example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 31: Share a Slice Backing Array

_ex-31 · exercises co-10_

Share a Slice Backing Array is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-31-slice-shares-backing/main.go` so
the page and runnable artifact cannot drift.

```go
// => slice shares backing: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => slice shares backing: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => slice shares backing: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  // => slice shares backing: marks one deliberate step in the slice shares backing example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  values := []int{1, 2, 3}
  // => slice shares backing: marks one deliberate step in the slice shares backing example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  view := values[:2]
  // => slice shares backing: marks one deliberate step in the slice shares backing example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  view[0] = 9
  // => slice shares backing: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  fmt.Println(values, view)
  // => slice shares backing: marks one deliberate step in the slice shares backing example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 32: Create a Map

_ex-32 · exercises co-11_

Create a Map is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-32-map-basic/main.go` so
the page and runnable artifact cannot drift.

```go
// => map basic: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => map basic: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => map basic: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  // => map basic: marks one deliberate step in the map basic example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  counts := map[string]int{"ok": 1}
  // => map basic: marks one deliberate step in the map basic example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  counts["warn"] = 2
  // => map basic: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  fmt.Println(counts)
  // => map basic: marks one deliberate step in the map basic example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 33: Use Map Comma-Ok

_ex-33 · exercises co-11_

Use Map Comma-Ok is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-33-map-comma-ok/main.go` so
the page and runnable artifact cannot drift.

```go
// => map comma ok: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => map comma ok: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => map comma ok: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  // => map comma ok: marks one deliberate step in the map comma ok example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  counts := map[string]int{"ok": 0}
  // => map comma ok: marks one deliberate step in the map comma ok example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  value, present := counts["missing"]
  // => map comma ok: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  fmt.Println(value, present)
  // => map comma ok: marks one deliberate step in the map comma ok example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 34: Delete and Iterate a Map

_ex-34 · exercises co-11_

Delete and Iterate a Map is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-34-map-delete-iterate/main.go` so
the page and runnable artifact cannot drift.

```go
// => map delete iterate: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => map delete iterate: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => map delete iterate: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  // => map delete iterate: marks one deliberate step in the map delete iterate example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  counts := map[string]int{"ok": 1, "warn": 2}
  // => map delete iterate: marks one deliberate step in the map delete iterate example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  delete(counts, "warn")
  // => map delete iterate: uses Go’s single loop keyword for iteration.
  // => keeps the loop state and termination condition local.
  for key, value := range counts {
    fmt.Println(key, value)
  }
  // => map delete iterate: marks one deliberate step in the map delete iterate example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 35: Read through a Pointer

_ex-35 · exercises co-12_

Read through a Pointer is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-35-pointer-basics/main.go` so
the page and runnable artifact cannot drift.

```go
// => pointer basics: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => pointer basics: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => pointer basics: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  // => pointer basics: marks one deliberate step in the pointer basics example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  value := 7
  // => pointer basics: marks one deliberate step in the pointer basics example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  pointer := &value
  // => pointer basics: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  fmt.Println(*pointer)
  // => pointer basics: marks one deliberate step in the pointer basics example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 36: Modify through a Pointer

_ex-36 · exercises co-12_

Modify through a Pointer is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-36-pointer-modify/main.go` so
the page and runnable artifact cannot drift.

```go
// => pointer modify: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => pointer modify: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => pointer modify: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func increment(value *int) { *value++ }

// => pointer modify: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  // => pointer modify: marks one deliberate step in the pointer modify example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  value := 7
  // => pointer modify: marks one deliberate step in the pointer modify example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  increment(&value)
  // => pointer modify: makes the observable result visible in stdout.
  // => gives the learner a direct value to verify.
  fmt.Println(value)
  // => pointer modify: marks one deliberate step in the pointer modify example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 37: Recover a Nil Pointer Panic

_ex-37 · exercises co-12_

Recover a Nil Pointer Panic is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-37-nil-pointer-panic/main.go` so
the page and runnable artifact cannot drift.

```go
// => nil pointer panic: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => nil pointer panic: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => nil pointer panic: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func dereference(pointer *int) (recovered any) {
  // => nil pointer panic: marks one deliberate step in the nil pointer panic example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  defer func() { recovered = recover() }()
  // => nil pointer panic: marks one deliberate step in the nil pointer panic example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  _ = *pointer
  // => nil pointer panic: returns a value through Go’s ordinary control-flow mechanism.
  // => keeps the caller responsible for the next decision.
  return nil
  // => nil pointer panic: marks one deliberate step in the nil pointer panic example.
  // => keeps the mechanism inspectable before it is composed with another concern.
}

// => nil pointer panic: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println(dereference(nil) != nil) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 38: Define a Struct

_ex-38 · exercises co-13_

Define a Struct is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-38-struct-definition/main.go` so
the page and runnable artifact cannot drift.

```go
// => struct definition: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => struct definition: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => struct definition: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Release struct {
  Name   string
  Number int
}

// => struct definition: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { release := Release{Name: "ship", Number: 1}; fmt.Println(release.Name) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 39: Build a Struct Literal

_ex-39 · exercises co-13_

Build a Struct Literal is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-39-struct-literal/main.go` so
the page and runnable artifact cannot drift.

```go
// => struct literal: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => struct literal: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => struct literal: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Release struct {
  Name   string
  Number int
}

// => struct literal: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { release := Release{Name: "ship"}; fmt.Println(release.Name, release.Number) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 40: Embed a Struct

_ex-40 · exercises co-13_

Embed a Struct is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-40-embedded-struct/main.go` so
the page and runnable artifact cannot drift.

```go
// => embedded struct: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => embedded struct: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => embedded struct: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Metadata struct{ Owner string }

// => embedded struct: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Release struct {
  Metadata
  Name string
}

// => embedded struct: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  release := Release{Metadata: Metadata{Owner: "Ada"}, Name: "ship"}
  fmt.Println(release.Owner)
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 41: Use a Value Receiver

_ex-41 · exercises co-14_

Use a Value Receiver is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-41-method-value-receiver/main.go` so
the page and runnable artifact cannot drift.

```go
// => method value receiver: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => method value receiver: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => method value receiver: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Counter int

// => method value receiver: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func (counter Counter) Incremented() Counter { return counter + 1 }

// => method value receiver: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { counter := Counter(1); fmt.Println(counter.Incremented(), counter) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 42: Use a Pointer Receiver

_ex-42 · exercises co-14_

Use a Pointer Receiver is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-42-method-pointer-receiver/main.go` so
the page and runnable artifact cannot drift.

```go
// => method pointer receiver: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => method pointer receiver: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => method pointer receiver: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Counter int

// => method pointer receiver: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func (counter *Counter) Increment() { *counter++ }

// => method pointer receiver: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { counter := Counter(1); counter.Increment(); fmt.Println(counter) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 43: Choose a Receiver

_ex-43 · exercises co-14_

Choose a Receiver is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-43-receiver-choice/main.go` so
the page and runnable artifact cannot drift.

```go
// => receiver choice: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => receiver choice: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => receiver choice: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Release struct{ Name string }

// => receiver choice: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func (release Release) Label() string { return release.Name }

// => receiver choice: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func (release *Release) Rename(name string) { release.Name = name }

// => receiver choice: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { release := Release{Name: "ship"}; release.Rename("dock"); fmt.Println(release.Label()) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 44: Satisfy an Interface Implicitly

_ex-44 · exercises co-15_

Satisfy an Interface Implicitly is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-44-interface-implicit/main.go` so
the page and runnable artifact cannot drift.

```go
// => interface implicit: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => interface implicit: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => interface implicit: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Stringer interface{ String() string }

// => interface implicit: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Release struct{ Name string }

// => interface implicit: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func (release Release) String() string { return release.Name }

// => interface implicit: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func printValue(value Stringer) { fmt.Println(value.String()) }

// => interface implicit: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { printValue(Release{Name: "ship"}) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 45: Use Two Interface Implementations

_ex-45 · exercises co-15_

Use Two Interface Implementations is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-45-interface-two-impls/main.go` so
the page and runnable artifact cannot drift.

```go
// => interface two impls: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => interface two impls: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => interface two impls: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Runner interface{ Run() string }

// => interface two impls: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Check struct{}

func (Check) Run() string { return "checked" }

// => interface two impls: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Publish struct{}

func (Publish) Run() string { return "published" }

// => interface two impls: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  for _, runner := range []Runner{Check{}, Publish{}} {
    fmt.Println(runner.Run())
  }
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 46: Store Values in any

_ex-46 · exercises co-15_

Store Values in any is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-46-empty-interface-any/main.go` so
the page and runnable artifact cannot drift.

```go
// => empty interface any: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => empty interface any: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => empty interface any: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  values := []any{"ship", 7, true}
  for _, value := range values {
    fmt.Printf("%T %v\n", value, value)
  }
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 47: Use a Safe Type Assertion

_ex-47 · exercises co-15_

Use a Safe Type Assertion is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-47-type-assertion/main.go` so
the page and runnable artifact cannot drift.

```go
// => type assertion: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => type assertion: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => type assertion: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  var value any = "ship"
  name, ok := value.(string)
  fmt.Println(name, ok)
  _, ok = value.(int)
  fmt.Println(ok)
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 48: Use a Type Switch

_ex-48 · exercises co-15_

Use a Type Switch is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-48-type-switch/main.go` so
the page and runnable artifact cannot drift.

```go
// => type switch: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => Type switching makes a dynamic any value explicit at its boundary.
// => Each case below narrows the value before it is used.

// => type switch: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => type switch: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func describe(value any) string {
  switch item := value.(type) {
  case string:
    return "string " + item
  case int:
    return fmt.Sprintf("int %d", item)
  default:
    return "other"
  }
}

// => type switch: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println(describe("ship"), describe(7)) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 49: Check an Error Value

_ex-49 · exercises co-16_

Check an Error Value is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-49-error-value-check/main.go` so
the page and runnable artifact cannot drift.

```go
// => error value check: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => error value check: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
  // => error value check: marks one deliberate step in the error value check example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "errors"
  // => error value check: marks one deliberate step in the error value check example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "fmt"
  // => error value check: marks one deliberate step in the error value check example.
  // => keeps the mechanism inspectable before it is composed with another concern.
)

// => error value check: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func open(name string) error {
  if name == "" {
    return errors.New("name is required")
  }
  return nil
}

// => error value check: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  if err := open(""); err != nil {
    fmt.Println(err)
  }
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 50: Create an Error

_ex-50 · exercises co-16_

Create an Error is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-50-errors-new/main.go` so
the page and runnable artifact cannot drift.

```go
// => errors new: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => errors new: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
  // => errors new: marks one deliberate step in the errors new example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "errors"
  // => errors new: marks one deliberate step in the errors new example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "fmt"
  // => errors new: marks one deliberate step in the errors new example.
  // => keeps the mechanism inspectable before it is composed with another concern.
)

// => errors new: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { err := errors.New("release unavailable"); fmt.Println(err.Error()) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 51: Implement a Custom Error

_ex-51 · exercises co-16_

Implement a Custom Error is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-51-custom-error-type/main.go` so
the page and runnable artifact cannot drift.

```go
// => custom error type: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => custom error type: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => custom error type: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type StatusError struct{ Code int }

// => custom error type: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func (err StatusError) Error() string { return fmt.Sprintf("status %d", err.Code) }

// => custom error type: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { var err error = StatusError{Code: 503}; fmt.Println(err) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 52: Wrap an Error

_ex-52 · exercises co-17_

Wrap an Error is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-52-error-wrap-w/main.go` so
the page and runnable artifact cannot drift.

```go
// => error wrap w: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => error wrap w: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
  // => error wrap w: marks one deliberate step in the error wrap w example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "errors"
  // => error wrap w: marks one deliberate step in the error wrap w example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "fmt"
  // => error wrap w: marks one deliberate step in the error wrap w example.
  // => keeps the mechanism inspectable before it is composed with another concern.
)

// => error wrap w: marks one deliberate step in the error wrap w example.
// => keeps the mechanism inspectable before it is composed with another concern.
var ErrMissing = errors.New("missing")

// => error wrap w: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func load() error { return fmt.Errorf("load config: %w", ErrMissing) }

// => error wrap w: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { err := load(); fmt.Println(errors.Unwrap(err)) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 53: Inspect Wrapped Errors

_ex-53 · exercises co-17_

Inspect Wrapped Errors is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-53-errors-is-as/main.go` so
the page and runnable artifact cannot drift.

```go
// => errors is as: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => errors is as: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
  // => errors is as: marks one deliberate step in the errors is as example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "errors"
  // => errors is as: marks one deliberate step in the errors is as example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "fmt"
  // => errors is as: marks one deliberate step in the errors is as example.
  // => keeps the mechanism inspectable before it is composed with another concern.
)

// => errors is as: marks one deliberate step in the errors is as example.
// => keeps the mechanism inspectable before it is composed with another concern.
var ErrMissing = errors.New("missing")

// => errors is as: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type StatusError struct{ Code int }

// => errors is as: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func (err *StatusError) Error() string { return "status error" }

// => errors is as: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  cause := &StatusError{Code: 503}
  err := fmt.Errorf("wrapped: %w", cause)
  var status *StatusError
  fmt.Println(errors.Is(fmt.Errorf("wrapped: %w", ErrMissing), ErrMissing))
  fmt.Println(errors.As(err, &status), status.Code)
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.

### Example 54: Marshal Struct Tags

_ex-54 · exercises co-18_

Marshal Struct Tags is a self-contained source slice. The code is rendered verbatim from `learning/code/ex-54-struct-tags-json/main.go` so
the page and runnable artifact cannot drift.

```go
// => struct tags json: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => struct tags json: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
  // => struct tags json: marks one deliberate step in the struct tags json example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "encoding/json"
  // => struct tags json: marks one deliberate step in the struct tags json example.
  // => keeps the mechanism inspectable before it is composed with another concern.
  "fmt"
  // => struct tags json: marks one deliberate step in the struct tags json example.
  // => keeps the mechanism inspectable before it is composed with another concern.
)

// => struct tags json: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Release struct {
  Name   string `json:"name"`
  Secret string `json:"-"`
}

// => struct tags json: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
  bytes, _ := json.Marshal(Release{Name: "ship", Secret: "hidden"})
  fmt.Println(string(bytes))
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the stated Go value, interface, error, JSON, generic, concurrency, test,
formatting, or cancellation rule is visible in the output.

**Key takeaway**: keep the smallest useful Go mechanism explicit before composing it.
