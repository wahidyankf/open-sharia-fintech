// => subtests run: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => subtests run: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => subtests run: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	for _, name := range []string{"positive", "zero"} {
		fmt.Println("subtest:", name)
	}
}
