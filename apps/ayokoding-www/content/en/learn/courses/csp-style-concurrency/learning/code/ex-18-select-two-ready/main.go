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
