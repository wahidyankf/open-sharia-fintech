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
