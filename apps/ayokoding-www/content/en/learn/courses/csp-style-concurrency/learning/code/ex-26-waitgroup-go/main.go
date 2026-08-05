// => advances the waitgroup go behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => waitgroup go: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the waitgroup go behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import (
	// => advances the waitgroup go behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	"fmt"
	// => advances the waitgroup go behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	"sync"
	// => advances the waitgroup go behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
)

// => coordinates the shared synchronization primitive.
// => keeps lock or completion ownership local.
func main() { var wait sync.WaitGroup; wait.Go(func() { fmt.Println("done") }); wait.Wait() }
