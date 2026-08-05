// => buffered channel: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => buffered channel: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => buffered channel: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { values := make(chan int, 2); values <- 1; values <- 2; fmt.Println(<-values, <-values) }
