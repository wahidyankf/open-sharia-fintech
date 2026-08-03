// => advances the mutex no copy behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => mutex no copy: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the mutex no copy behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import (
	// => advances the mutex no copy behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	"fmt"
	// => advances the mutex no copy behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	"sync"
	// => advances the mutex no copy behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
)

// => advances the mutex no copy behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
type Safe struct {
	// => coordinates the shared synchronization primitive.
	// => keeps lock or completion ownership local.
	mu sync.Mutex
	// => advances the mutex no copy behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	value int
	// => advances the mutex no copy behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
}

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func (s *Safe) Inc() { s.mu.Lock(); defer s.mu.Unlock(); s.value++ }

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() { var value Safe; value.Inc(); fmt.Println(value.value) }
