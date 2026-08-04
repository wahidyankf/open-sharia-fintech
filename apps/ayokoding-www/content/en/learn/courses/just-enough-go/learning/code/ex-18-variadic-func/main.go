// => variadic func: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => variadic func: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => variadic func: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func sum(values ...int) int {
	// => variadic func: marks one deliberate step in the variadic func example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	total := 0
	// => variadic func: uses Go’s single loop keyword for iteration.
	// => keeps the loop state and termination condition local.
	for _, value := range values {
		total += value
	}
	// => variadic func: returns a value through Go’s ordinary control-flow mechanism.
	// => keeps the caller responsible for the next decision.
	return total
	// => variadic func: marks one deliberate step in the variadic func example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}

// => variadic func: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	// => variadic func: marks one deliberate step in the variadic func example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	values := []int{4, 5}
	// => variadic func: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	fmt.Println(sum(1, 2, 3), sum(values...))
	// => variadic func: marks one deliberate step in the variadic func example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}
