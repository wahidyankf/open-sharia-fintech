// => comparable constraint: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => comparable constraint: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => comparable constraint: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func Contains[T comparable](values []T, wanted T) bool {
	for _, value := range values {
		if value == wanted {
			return true
		}
	}
	return false
}

// => comparable constraint: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println(Contains([]string{"go", "rust"}, "go")) }
