// => advances the unbuffered rendezvous behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => unbuffered rendezvous: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the unbuffered rendezvous behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import "fmt"

// => creates or types the channel that transfers ownership.
// => makes blocking and buffering part of the explicit contract.
func main() { values := make(chan int); go func() { values <- 7 }(); fmt.Println(<-values) }
