// => unbuffered channel: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => unbuffered channel: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => unbuffered channel: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { values := make(chan int); go func() { values <- 7 }(); fmt.Println(<-values) }
