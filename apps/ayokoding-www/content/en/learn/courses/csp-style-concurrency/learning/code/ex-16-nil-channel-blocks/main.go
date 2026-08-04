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
