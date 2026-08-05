// => func basic: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => func basic: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => func basic: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func twice(n int) int { return n * 2 }
func main()           { fmt.Println(twice(4)) }
