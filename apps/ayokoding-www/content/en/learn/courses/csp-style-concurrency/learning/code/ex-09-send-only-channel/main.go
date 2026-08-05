// => advances the send only channel behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => send only channel: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the send only channel behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import "fmt"

// => creates or types the channel that transfers ownership.
// => makes blocking and buffering part of the explicit contract.
func produce(out chan<- int) { out <- 7; close(out) }

// => creates or types the channel that transfers ownership.
// => makes blocking and buffering part of the explicit contract.
func main() { values := make(chan int); go produce(values); fmt.Println(<-values) }
