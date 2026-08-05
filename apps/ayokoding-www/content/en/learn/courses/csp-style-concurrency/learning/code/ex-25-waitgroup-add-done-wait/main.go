// => advances the waitgroup add done wait behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => waitgroup add done wait: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the waitgroup add done wait behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import (
	// => advances the waitgroup add done wait behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	"fmt"
	// => advances the waitgroup add done wait behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	"sync"
	// => advances the waitgroup add done wait behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
)

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() {
	// => coordinates the shared synchronization primitive.
	// => keeps lock or completion ownership local.
	var wait sync.WaitGroup
	// => advances the waitgroup add done wait behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	wait.Add(1)
	// => starts the concurrent worker without sharing its local stack.
	// => requires a completion or cancellation path to avoid a leak.
	go func() { defer wait.Done(); fmt.Println("done") }()
	// => advances the waitgroup add done wait behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	wait.Wait()
	// => advances the waitgroup add done wait behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
}
