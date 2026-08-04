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
