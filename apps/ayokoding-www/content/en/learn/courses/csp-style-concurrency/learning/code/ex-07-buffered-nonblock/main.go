// => advances the buffered nonblock behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => buffered nonblock: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the buffered nonblock behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import "fmt"

// => creates or types the channel that transfers ownership.
// => makes blocking and buffering part of the explicit contract.
func main() { values := make(chan int, 1); values <- 1; fmt.Println("sent without receiver") }
