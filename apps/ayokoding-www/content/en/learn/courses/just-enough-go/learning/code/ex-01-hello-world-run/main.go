// => hello world run: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => hello world run: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => hello world run: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println("hello, Go") }
