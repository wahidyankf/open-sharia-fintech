// => empty interface any: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => empty interface any: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => empty interface any: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	values := []any{"ship", 7, true}
	for _, value := range values {
		fmt.Printf("%T %v\n", value, value)
	}
}
