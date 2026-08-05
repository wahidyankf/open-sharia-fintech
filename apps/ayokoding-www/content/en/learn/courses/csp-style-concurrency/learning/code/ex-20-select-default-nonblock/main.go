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
