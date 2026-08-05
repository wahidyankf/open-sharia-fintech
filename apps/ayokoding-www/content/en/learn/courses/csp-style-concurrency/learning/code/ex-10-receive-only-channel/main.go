// => advances the receive only channel behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
package main

// => receive only channel: this line belongs to the focused CSP mechanism.
// => The example keeps ownership and synchronization visible.

// => advances the receive only channel behavior in this runnable slice.
// => keeps synchronization and ownership observable to the reader.
import "fmt"

// => creates or types the channel that transfers ownership.
// => makes blocking and buffering part of the explicit contract.
func consume(in <-chan int) int { return <-in }

// => creates or types the channel that transfers ownership.
// => makes blocking and buffering part of the explicit contract.
func main() { values := make(chan int, 1); values <- 7; fmt.Println(consume(values)) }
