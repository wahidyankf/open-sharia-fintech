// => channel handoff: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => channel handoff: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => channel handoff: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { result := make(chan string); go func() { result <- "ship" }(); fmt.Println(<-result) }
