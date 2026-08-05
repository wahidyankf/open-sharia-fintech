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
