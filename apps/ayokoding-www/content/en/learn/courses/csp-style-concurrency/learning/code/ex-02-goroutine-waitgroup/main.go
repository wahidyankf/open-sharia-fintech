// => advances the goroutine waitgroup behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => goroutine waitgroup: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the goroutine waitgroup behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import (
	// => advances the goroutine waitgroup behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	"fmt"
	// => advances the goroutine waitgroup behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	"sync"
	// => advances the goroutine waitgroup behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
)

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() {
	// => coordinates the shared synchronization primitive.
	// => keeps lock or completion ownership local.
	var wait sync.WaitGroup
	// => advances the goroutine waitgroup behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	for i := 0; i < 3; i++ {
		// => advances the goroutine waitgroup behavior in this runnable slice.
		// => keeps synchronization and ownership observable to the reader.
		wait.Add(1)
		// => starts the concurrent worker without sharing its local stack.
		// => requires a completion or cancellation path to avoid a leak.
		go func(value int) { defer wait.Done(); fmt.Println(value) }(i)
		// => advances the goroutine waitgroup behavior in this runnable slice.
		// => keeps synchronization and ownership observable to the reader.
	}
	// => advances the goroutine waitgroup behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	wait.Wait()
	// => advances the goroutine waitgroup behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
}
