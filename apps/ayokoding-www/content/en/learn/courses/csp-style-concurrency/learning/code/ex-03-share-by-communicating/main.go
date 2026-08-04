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
