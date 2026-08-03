// => generic function: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => generic function: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => generic function: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func Map[T, U any](values []T, transform func(T) U) []U {
	result := make([]U, len(values))
	for i, value := range values {
		result[i] = transform(value)
	}
	return result
}

// => generic function: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println(Map([]int{1, 2}, func(value int) string { return fmt.Sprint(value) })) }
