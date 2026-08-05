// => int float types: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => int float types: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => int float types: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { n := 3; f := 2.5; fmt.Println(float64(n) * f) }
