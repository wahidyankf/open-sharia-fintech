// => zero values: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => zero values: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => zero values: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	var n int
	var s string
	var ok bool
	var p *int
	fmt.Printf("%d %q %t %v\n", n, s, ok, p)
}
