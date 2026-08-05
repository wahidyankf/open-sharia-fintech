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
