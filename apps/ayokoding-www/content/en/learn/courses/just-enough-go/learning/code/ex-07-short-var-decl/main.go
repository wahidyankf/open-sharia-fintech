// => short var decl: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => short var decl: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => short var decl: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { name := "Ada"; fmt.Printf("%s is %T\n", name, name) }
