---
title: "Beginner Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 10
---

Examples 1–26 establish goroutines, channels, select, and synchronization.

### Example 1: Goroutine Basic

_ex-01 · exercises co-02_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-01-goroutine-basic/main.go`.

```go
// => advances the goroutine basic behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => goroutine basic: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the goroutine basic behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import (
  // => advances the goroutine basic behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  "fmt"
  // => advances the goroutine basic behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  "sync"
  // => advances the goroutine basic behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
)

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() {
  // => A WaitGroup makes the goroutine completion observable.
  // => coordinates the shared synchronization primitive.
  // => keeps lock or completion ownership local.
  var wait sync.WaitGroup
  // => advances the goroutine basic behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  wait.Add(1)
  // => starts the concurrent worker without sharing its local stack.
  // => requires a completion or cancellation path to avoid a leak.
  go func() { defer wait.Done(); fmt.Println("ran") }()
  // => advances the goroutine basic behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  wait.Wait()
  // => advances the goroutine basic behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
}
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 2: Goroutines with WaitGroup

_ex-02 · exercises co-02, co-13_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-02-goroutine-waitgroup/main.go`.

```go
// => advances the goroutine waitgroup behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => goroutine waitgroup: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the goroutine waitgroup behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import (
  // => advances the goroutine waitgroup behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  "fmt"
  // => advances the goroutine waitgroup behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  "sync"
  // => advances the goroutine waitgroup behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
)

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() {
  // => coordinates the shared synchronization primitive.
  // => keeps lock or completion ownership local.
  var wait sync.WaitGroup
  // => advances the goroutine waitgroup behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  for i := 0; i < 3; i++ {
    // => advances the goroutine waitgroup behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
    wait.Add(1)
    // => starts the concurrent worker without sharing its local stack.
    // => requires a completion or cancellation path to avoid a leak.
    go func(value int) { defer wait.Done(); fmt.Println(value) }(i)
    // => advances the goroutine waitgroup behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
  }
  // => advances the goroutine waitgroup behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  wait.Wait()
  // => advances the goroutine waitgroup behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
}
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 3: Share by Communicating

_ex-03 · exercises co-01_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-03-share-by-communicating/main.go`.

```go
// => advances the share by communicating behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => share by communicating: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the share by communicating behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import "fmt"

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() {
  // => creates or types the channel that transfers ownership.
  // => makes blocking and buffering part of the explicit contract.
  values := make(chan []string, 1)
  // => advances the share by communicating behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  values <- []string{"owned"}
  // => advances the share by communicating behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  close(values)
  // => advances the share by communicating behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  value := <-values
  // => advances the share by communicating behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  value[0] = "receiver-mutates"
  // => advances the share by communicating behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  fmt.Println(value)
  // => advances the share by communicating behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
}
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 4: Unbuffered Rendezvous

_ex-04 · exercises co-04_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-04-unbuffered-rendezvous/main.go`.

```go
// => advances the unbuffered rendezvous behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => unbuffered rendezvous: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the unbuffered rendezvous behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import "fmt"

// => creates or types the channel that transfers ownership.
// => makes blocking and buffering part of the explicit contract.
func main() { values := make(chan int); go func() { values <- 7 }(); fmt.Println(<-values) }
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 5: Observe an Unbuffered Block

_ex-05 · exercises co-04_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-05-unbuffered-blocks/main.go`.

```go
// => advances the unbuffered blocks behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => unbuffered blocks: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the unbuffered blocks behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import (
  // => advances the unbuffered blocks behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  "fmt"
  // => advances the unbuffered blocks behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  "time"
  // => advances the unbuffered blocks behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
)

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() {
  // => creates or types the channel that transfers ownership.
  // => makes blocking and buffering part of the explicit contract.
  values := make(chan int)
  // => waits only on the listed communication or cancellation events.
  // => keeps timeout and shutdown behavior visible.
  select {
  // => advances the unbuffered blocks behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  case values <- 1:
    // => advances the unbuffered blocks behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
    fmt.Println("sent")
  // => advances the unbuffered blocks behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  case <-time.After(time.Millisecond):
    // => advances the unbuffered blocks behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
    fmt.Println("blocked")
    // => advances the unbuffered blocks behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
  }
  // => advances the unbuffered blocks behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
}
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 6: Use Buffered Capacity

_ex-06 · exercises co-05_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-06-buffered-capacity/main.go`.

```go
// => advances the buffered capacity behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => buffered capacity: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the buffered capacity behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import "fmt"

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() {
  // => creates or types the channel that transfers ownership.
  // => makes blocking and buffering part of the explicit contract.
  values := make(chan int, 3)
  // => advances the buffered capacity behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  values <- 1
  // => advances the buffered capacity behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  values <- 2
  // => advances the buffered capacity behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  values <- 3
  // => advances the buffered capacity behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  fmt.Println(len(values), cap(values))
  // => advances the buffered capacity behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
}
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 7: Send into Buffer Space

_ex-07 · exercises co-05_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-07-buffered-nonblock/main.go`.

```go
// => advances the buffered nonblock behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => buffered nonblock: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the buffered nonblock behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import "fmt"

// => creates or types the channel that transfers ownership.
// => makes blocking and buffering part of the explicit contract.
func main() { values := make(chan int, 1); values <- 1; fmt.Println("sent without receiver") }
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 8: Observe a Full Buffer

_ex-08 · exercises co-05_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-08-buffered-full-blocks/main.go`.

```go
// => advances the buffered full blocks behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => buffered full blocks: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the buffered full blocks behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import (
  // => advances the buffered full blocks behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  "fmt"
  // => advances the buffered full blocks behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  "time"
  // => advances the buffered full blocks behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
)

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() {
  // => creates or types the channel that transfers ownership.
  // => makes blocking and buffering part of the explicit contract.
  values := make(chan int, 3)
  // => advances the buffered full blocks behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  for i := 0; i < 3; i++ {
    // => advances the buffered full blocks behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
    values <- i
    // => advances the buffered full blocks behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
  }
  // => waits only on the listed communication or cancellation events.
  // => keeps timeout and shutdown behavior visible.
  select {
  // => advances the buffered full blocks behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  case values <- 3:
    // => advances the buffered full blocks behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
    fmt.Println("sent")
  // => advances the buffered full blocks behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  case <-time.After(time.Millisecond):
    // => advances the buffered full blocks behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
    fmt.Println("full blocks")
    // => advances the buffered full blocks behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
  }
  // => advances the buffered full blocks behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
}
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 9: Use a Send-Only Channel

_ex-09 · exercises co-06_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-09-send-only-channel/main.go`.

```go
// => advances the send only channel behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => send only channel: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the send only channel behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import "fmt"

// => creates or types the channel that transfers ownership.
// => makes blocking and buffering part of the explicit contract.
func produce(out chan<- int) { out <- 7; close(out) }

// => creates or types the channel that transfers ownership.
// => makes blocking and buffering part of the explicit contract.
func main() { values := make(chan int); go produce(values); fmt.Println(<-values) }
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 10: Use a Receive-Only Channel

_ex-10 · exercises co-06_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-10-receive-only-channel/main.go`.

```go
// => advances the receive only channel behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => receive only channel: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the receive only channel behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import "fmt"

// => creates or types the channel that transfers ownership.
// => makes blocking and buffering part of the explicit contract.
func consume(in <-chan int) int { return <-in }

// => creates or types the channel that transfers ownership.
// => makes blocking and buffering part of the explicit contract.
func main() { values := make(chan int, 1); values <- 7; fmt.Println(consume(values)) }
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 11: Close a Channel

_ex-11 · exercises co-07_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-11-close-channel/main.go`.

```go
// => advances the close channel behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => close channel: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the close channel behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import "fmt"

// => creates or types the channel that transfers ownership.
// => makes blocking and buffering part of the explicit contract.
func main() { values := make(chan int); close(values); fmt.Println(<-values) }
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 12: Range over a Channel

_ex-12 · exercises co-07_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-12-range-over-channel/main.go`.

```go
// => advances the range over channel behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => range over channel: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the range over channel behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import "fmt"

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() {
  // => creates or types the channel that transfers ownership.
  // => makes blocking and buffering part of the explicit contract.
  values := make(chan int, 2)
  // => advances the range over channel behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  values <- 1
  // => advances the range over channel behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  values <- 2
  // => advances the range over channel behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  close(values)
  // => advances the range over channel behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  for value := range values {
    // => advances the range over channel behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
    fmt.Println(value)
    // => advances the range over channel behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
  }
  // => advances the range over channel behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
}
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 13: Detect a Closed Channel

_ex-13 · exercises co-07_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-13-comma-ok-closed/main.go`.

```go
// => advances the comma ok closed behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => comma ok closed: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the comma ok closed behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import "fmt"

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() {
  // => creates or types the channel that transfers ownership.
  // => makes blocking and buffering part of the explicit contract.
  values := make(chan int)
  // => advances the comma ok closed behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  close(values)
  // => advances the comma ok closed behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  value, open := <-values
  // => advances the comma ok closed behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  fmt.Println(value, open)
  // => advances the comma ok closed behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
}
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 14: Recover a Send-on-Closed Panic

_ex-14 · exercises co-07_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-14-send-on-closed-panics/main.go`.

```go
// => advances the send on closed panics behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => send on closed panics: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the send on closed panics behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import "fmt"

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func try() (recovered any) {
  // => advances the send on closed panics behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  defer func() { recovered = recover() }()
  // => creates or types the channel that transfers ownership.
  // => makes blocking and buffering part of the explicit contract.
  values := make(chan int)
  // => advances the send on closed panics behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  close(values)
  // => advances the send on closed panics behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  values <- 1
  // => advances the send on closed panics behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  return
  // => advances the send on closed panics behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
}

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() { fmt.Println(try() != nil) }
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 15: Recover a Double-Close Panic

_ex-15 · exercises co-07_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-15-close-closed-panics/main.go`.

```go
// => advances the close closed panics behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => close closed panics: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the close closed panics behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import "fmt"

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func try() (recovered any) {
  // => advances the close closed panics behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  defer func() { recovered = recover() }()
  // => creates or types the channel that transfers ownership.
  // => makes blocking and buffering part of the explicit contract.
  values := make(chan int)
  // => advances the close closed panics behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  close(values)
  // => advances the close closed panics behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  close(values)
  // => advances the close closed panics behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  return
  // => advances the close closed panics behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
}

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() { fmt.Println(try() != nil) }
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 16: Observe a Nil Channel

_ex-16 · exercises co-08_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-16-nil-channel-blocks/main.go`.

```go
// => advances the nil channel blocks behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => nil channel blocks: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the nil channel blocks behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import (
  // => advances the nil channel blocks behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  "fmt"
  // => advances the nil channel blocks behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  "time"
  // => advances the nil channel blocks behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
)

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() {
  // => creates or types the channel that transfers ownership.
  // => makes blocking and buffering part of the explicit contract.
  var values <-chan int
  // => waits only on the listed communication or cancellation events.
  // => keeps timeout and shutdown behavior visible.
  select {
  // => advances the nil channel blocks behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  case <-values:
    // => advances the nil channel blocks behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
    fmt.Println("ready")
  // => advances the nil channel blocks behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  case <-time.After(time.Millisecond):
    // => advances the nil channel blocks behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
    fmt.Println("nil is never ready")
    // => advances the nil channel blocks behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
  }
  // => advances the nil channel blocks behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
}
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 17: Disable a Select Case with nil

_ex-17 · exercises co-08_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-17-nil-disables-select-case/main.go`.

```go
// => advances the nil disables select case behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => nil disables select case: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the nil disables select case behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import "fmt"

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() {
  // => creates or types the channel that transfers ownership.
  // => makes blocking and buffering part of the explicit contract.
  left, right := make(chan string, 1), make(chan string, 1)
  // => advances the nil disables select case behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  left <- "left"
  // => advances the nil disables select case behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  right <- "right"
  // => advances the nil disables select case behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  left = nil
  // => waits only on the listed communication or cancellation events.
  // => keeps timeout and shutdown behavior visible.
  select {
  // => advances the nil disables select case behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  case value := <-left:
    // => advances the nil disables select case behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
    fmt.Println(value)
  // => advances the nil disables select case behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  case value := <-right:
    // => advances the nil disables select case behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
    fmt.Println(value)
    // => advances the nil disables select case behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
  }
  // => advances the nil disables select case behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
}
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 18: Select One Ready Channel

_ex-18 · exercises co-09_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-18-select-two-ready/main.go`.

```go
// => advances the select two ready behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => select two ready: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the select two ready behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import "fmt"

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() {
  // => creates or types the channel that transfers ownership.
  // => makes blocking and buffering part of the explicit contract.
  left, right := make(chan string, 1), make(chan string, 1)
  // => advances the select two ready behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  left <- "left"
  // => advances the select two ready behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  right <- "right"
  // => waits only on the listed communication or cancellation events.
  // => keeps timeout and shutdown behavior visible.
  select {
  // => advances the select two ready behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  case value := <-left:
    // => advances the select two ready behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
    fmt.Println(value)
  // => advances the select two ready behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  case value := <-right:
    // => advances the select two ready behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
    fmt.Println(value)
    // => advances the select two ready behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
  }
  // => advances the select two ready behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
}
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 19: Sample Select Choice

_ex-19 · exercises co-09_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-19-select-pseudo-random/main.go`.

```go
// => advances the select pseudo random behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => select pseudo random: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the select pseudo random behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import "fmt"

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() {
  // => advances the select pseudo random behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  counts := map[int]int{}
  // => advances the select pseudo random behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  for i := 0; i < 100; i++ {
    // => creates or types the channel that transfers ownership.
    // => makes blocking and buffering part of the explicit contract.
    left, right := make(chan int, 1), make(chan int, 1)
    // => advances the select pseudo random behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
    left <- 1
    // => advances the select pseudo random behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
    right <- 2
    // => waits only on the listed communication or cancellation events.
    // => keeps timeout and shutdown behavior visible.
    select {
    // => advances the select pseudo random behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
    case <-left:
      // => advances the select pseudo random behavior in this runnable slice.
      // => keeps synchronization and ownership observable to the reader.
      counts[1]++
    // => advances the select pseudo random behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
    case <-right:
      // => advances the select pseudo random behavior in this runnable slice.
      // => keeps synchronization and ownership observable to the reader.
      counts[2]++
      // => advances the select pseudo random behavior in this runnable slice.
      // => keeps synchronization and ownership observable to the reader.
    }
    // => advances the select pseudo random behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
  }
  // => advances the select pseudo random behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  fmt.Println(counts)
  // => advances the select pseudo random behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
}
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 20: Use a Non-Blocking Select

_ex-20 · exercises co-09_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-20-select-default-nonblock/main.go`.

```go
// => advances the select default nonblock behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => select default nonblock: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the select default nonblock behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import "fmt"

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() {
  // => creates or types the channel that transfers ownership.
  // => makes blocking and buffering part of the explicit contract.
  values := make(chan int)
  // => waits only on the listed communication or cancellation events.
  // => keeps timeout and shutdown behavior visible.
  select {
  // => advances the select default nonblock behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  case value := <-values:
    // => advances the select default nonblock behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
    fmt.Println(value)
  // => advances the select default nonblock behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  default:
    // => advances the select default nonblock behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
    fmt.Println("not ready")
    // => advances the select default nonblock behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
  }
  // => advances the select default nonblock behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
}
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 21: Time Out a Select

_ex-21 · exercises co-10_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-21-select-timeout-after/main.go`.

```go
// => advances the select timeout after behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => select timeout after: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the select timeout after behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import (
  // => advances the select timeout after behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  "fmt"
  // => advances the select timeout after behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  "time"
  // => advances the select timeout after behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
)

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() {
  // => creates or types the channel that transfers ownership.
  // => makes blocking and buffering part of the explicit contract.
  values := make(chan int)
  // => waits only on the listed communication or cancellation events.
  // => keeps timeout and shutdown behavior visible.
  select {
  // => advances the select timeout after behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  case value := <-values:
    // => advances the select timeout after behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
    fmt.Println(value)
  // => advances the select timeout after behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  case <-time.After(time.Millisecond):
    // => advances the select timeout after behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
    fmt.Println("timed out")
    // => advances the select timeout after behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
  }
  // => advances the select timeout after behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
}
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 22: Guard a Counter with Mutex

_ex-22 · exercises co-11_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-22-mutex-guard-counter/main.go`.

```go
// => advances the mutex guard counter behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => mutex guard counter: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the mutex guard counter behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import (
  // => advances the mutex guard counter behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  "fmt"
  // => advances the mutex guard counter behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  "sync"
  // => advances the mutex guard counter behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
)

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() {
  // => coordinates the shared synchronization primitive.
  // => keeps lock or completion ownership local.
  var mu sync.Mutex
  // => coordinates the shared synchronization primitive.
  // => keeps lock or completion ownership local.
  var wait sync.WaitGroup
  // => advances the mutex guard counter behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  count := 0
  // => advances the mutex guard counter behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  for i := 0; i < 100; i++ {
    // => advances the mutex guard counter behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
    wait.Add(1)
    // => starts the concurrent worker without sharing its local stack.
    // => requires a completion or cancellation path to avoid a leak.
    go func() { defer wait.Done(); mu.Lock(); count++; mu.Unlock() }()
    // => advances the mutex guard counter behavior in this runnable slice.
    // => keeps synchronization and ownership observable to the reader.
  }
  // => advances the mutex guard counter behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  wait.Wait()
  // => advances the mutex guard counter behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  fmt.Println(count)
  // => advances the mutex guard counter behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
}
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 23: Avoid Copying a Mutex

_ex-23 · exercises co-11_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-23-mutex-no-copy/main.go`.

```go
// => advances the mutex no copy behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => mutex no copy: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the mutex no copy behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import (
  // => advances the mutex no copy behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  "fmt"
  // => advances the mutex no copy behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  "sync"
  // => advances the mutex no copy behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
)

// => advances the mutex no copy behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
type Safe struct {
  // => coordinates the shared synchronization primitive.
  // => keeps lock or completion ownership local.
  mu sync.Mutex
  // => advances the mutex no copy behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  value int
  // => advances the mutex no copy behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
}

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func (s *Safe) Inc() { s.mu.Lock(); defer s.mu.Unlock(); s.value++ }

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() { var value Safe; value.Inc(); fmt.Println(value.value) }
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 24: Use RWMutex Readers

_ex-24 · exercises co-12_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-24-rwmutex-readers/main.go`.

```go
// => advances the rwmutex readers behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => rwmutex readers: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the rwmutex readers behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import (
  // => advances the rwmutex readers behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  "fmt"
  // => advances the rwmutex readers behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  "sync"
  // => advances the rwmutex readers behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
)

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() {
  // => coordinates the shared synchronization primitive.
  // => keeps lock or completion ownership local.
  var lock sync.RWMutex
  // => advances the rwmutex readers behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  value := 1
  // => advances the rwmutex readers behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  lock.RLock()
  // => advances the rwmutex readers behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  fmt.Println(value)
  // => advances the rwmutex readers behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  lock.RUnlock()
  // => advances the rwmutex readers behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  lock.Lock()
  // => advances the rwmutex readers behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  value = 2
  // => advances the rwmutex readers behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  lock.Unlock()
  // => advances the rwmutex readers behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  fmt.Println(value)
  // => advances the rwmutex readers behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
}
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 25: Coordinate Add Done Wait

_ex-25 · exercises co-13_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-25-waitgroup-add-done-wait/main.go`.

```go
// => advances the waitgroup add done wait behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => waitgroup add done wait: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the waitgroup add done wait behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import (
  // => advances the waitgroup add done wait behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  "fmt"
  // => advances the waitgroup add done wait behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  "sync"
  // => advances the waitgroup add done wait behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
)

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() {
  // => coordinates the shared synchronization primitive.
  // => keeps lock or completion ownership local.
  var wait sync.WaitGroup
  // => advances the waitgroup add done wait behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  wait.Add(1)
  // => starts the concurrent worker without sharing its local stack.
  // => requires a completion or cancellation path to avoid a leak.
  go func() { defer wait.Done(); fmt.Println("done") }()
  // => advances the waitgroup add done wait behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  wait.Wait()
  // => advances the waitgroup add done wait behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
}
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.

### Example 26: Launch with WaitGroup.Go

_ex-26 · exercises co-13_

This self-contained CSP slice is rendered verbatim from `learning/code/ex-26-waitgroup-go/main.go`.

```go
// => advances the waitgroup go behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => waitgroup go: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the waitgroup go behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import (
  // => advances the waitgroup go behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  "fmt"
  // => advances the waitgroup go behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
  "sync"
  // => advances the waitgroup go behavior in this runnable slice.
  // => keeps synchronization and ownership observable to the reader.
)

// => coordinates the shared synchronization primitive.
// => keeps lock or completion ownership local.
func main() { var wait sync.WaitGroup; wait.Go(func() { fmt.Println("done") }); wait.Wait() }
```

**Run**: `go run main.go` from this example directory.

**Key takeaway**: the channel or synchronization primitive is the explicit coordination boundary.
