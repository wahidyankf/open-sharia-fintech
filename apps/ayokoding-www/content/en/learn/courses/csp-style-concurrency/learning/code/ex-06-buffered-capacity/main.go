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
