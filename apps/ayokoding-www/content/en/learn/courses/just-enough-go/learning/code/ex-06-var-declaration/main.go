// => var declaration: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => var declaration: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => var declaration: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { var name string = "Ada"; var year int = 2026; fmt.Println(name, year) }
