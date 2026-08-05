// => advances the select pseudo random behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => select pseudo random: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the select pseudo random behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import "fmt"

// => names one independently testable CSP stage or helper.
// => keeps dataflow separate from process orchestration.
func main() {
	// => advances the select pseudo random behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	counts := map[int]int{}
	// => advances the select pseudo random behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	for i := 0; i < 100; i++ {
		// => creates or types the channel that transfers ownership.
		// => makes blocking and buffering part of the explicit contract.
		left, right := make(chan int, 1), make(chan int, 1)
		// => advances the select pseudo random behavior in this runnable slice.
		// => keeps synchronization and ownership observable to the reader.
		left <- 1
		// => advances the select pseudo random behavior in this runnable slice.
		// => keeps synchronization and ownership observable to the reader.
		right <- 2
		// => waits only on the listed communication or cancellation events.
		// => keeps timeout and shutdown behavior visible.
		select {
		// => advances the select pseudo random behavior in this runnable slice.
		// => keeps synchronization and ownership observable to the reader.
		case <-left:
			// => advances the select pseudo random behavior in this runnable slice.
			// => keeps synchronization and ownership observable to the reader.
			counts[1]++
		// => advances the select pseudo random behavior in this runnable slice.
		// => keeps synchronization and ownership observable to the reader.
		case <-right:
			// => advances the select pseudo random behavior in this runnable slice.
			// => keeps synchronization and ownership observable to the reader.
			counts[2]++
			// => advances the select pseudo random behavior in this runnable slice.
			// => keeps synchronization and ownership observable to the reader.
		}
		// => advances the select pseudo random behavior in this runnable slice.
		// => keeps synchronization and ownership observable to the reader.
	}
	// => advances the select pseudo random behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
	fmt.Println(counts)
	// => advances the select pseudo random behavior in this runnable slice.
	// => keeps synchronization and ownership observable to the reader.
}
