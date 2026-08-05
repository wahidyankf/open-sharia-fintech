// => named return values: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => named return values: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => named return values: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func bounds(values []int) (small, large int) {
	// => named return values: marks one deliberate step in the named return values example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	small, large = values[0], values[0]
	// => named return values: uses Go’s single loop keyword for iteration.
	// => keeps the loop state and termination condition local.
	for _, value := range values {
		// => named return values: makes the branch condition explicit rather than exceptional.
		// => keeps success and failure control flow visible.
		if value < small {
			small = value
		}
		// => named return values: makes the branch condition explicit rather than exceptional.
		// => keeps success and failure control flow visible.
		if value > large {
			large = value
		}
		// => named return values: marks one deliberate step in the named return values example.
		// => keeps the mechanism inspectable before it is composed with another concern.
	}
	// => named return values: returns a value through Go’s ordinary control-flow mechanism.
	// => keeps the caller responsible for the next decision.
	return
	// => named return values: marks one deliberate step in the named return values example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}

// => named return values: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println(bounds([]int{3, 1, 4})) }
