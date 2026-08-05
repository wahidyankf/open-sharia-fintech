// => advances the mutex guard counter behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => mutex guard counter: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the mutex guard counter behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import (
	// => advances the mutex guard counter behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	"fmt"
	// => advances the mutex guard counter behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	"sync"
	// => advances the mutex guard counter behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
)

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() {
	// => coordinates the shared synchronization primitive.
	// => keeps lock or completion ownership local.
	var mu sync.Mutex
	// => coordinates the shared synchronization primitive.
	// => keeps lock or completion ownership local.
	var wait sync.WaitGroup
	// => advances the mutex guard counter behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	count := 0
	// => advances the mutex guard counter behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	for i := 0; i < 100; i++ {
		// => advances the mutex guard counter behavior in this runnable slice.
		// => keeps synchronization and ownership observable to the reader.
		wait.Add(1)
		// => starts the concurrent worker without sharing its local stack.
		// => requires a completion or cancellation path to avoid a leak.
		go func() { defer wait.Done(); mu.Lock(); count++; mu.Unlock() }()
		// => advances the mutex guard counter behavior in this runnable slice.
		// => keeps synchronization and ownership observable to the reader.
	}
	// => advances the mutex guard counter behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	wait.Wait()
	// => advances the mutex guard counter behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	fmt.Println(count)
	// => advances the mutex guard counter behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
}
