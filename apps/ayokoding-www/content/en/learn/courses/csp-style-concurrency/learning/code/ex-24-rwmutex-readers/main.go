// => advances the rwmutex readers behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => rwmutex readers: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the rwmutex readers behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import (
	// => advances the rwmutex readers behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	"fmt"
	// => advances the rwmutex readers behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	"sync"
	// => advances the rwmutex readers behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
)

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() {
	// => coordinates the shared synchronization primitive.
	// => keeps lock or completion ownership local.
	var lock sync.RWMutex
	// => advances the rwmutex readers behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	value := 1
	// => advances the rwmutex readers behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	lock.RLock()
	// => advances the rwmutex readers behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	fmt.Println(value)
	// => advances the rwmutex readers behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	lock.RUnlock()
	// => advances the rwmutex readers behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	lock.Lock()
	// => advances the rwmutex readers behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	value = 2
	// => advances the rwmutex readers behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	lock.Unlock()
	// => advances the rwmutex readers behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	fmt.Println(value)
	// => advances the rwmutex readers behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
}
