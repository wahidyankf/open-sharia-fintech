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
