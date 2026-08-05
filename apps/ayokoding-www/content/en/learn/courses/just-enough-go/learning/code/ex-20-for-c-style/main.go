// => for c style: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => for c style: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => for c style: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	// => for c style: uses Go’s single loop keyword for iteration.
	// => keeps the loop state and termination condition local.
	for i := 0; i < 3; i++ {
		// => for c style: makes the observable result visible in stdout.
		// => gives the learner a direct value to verify.
		fmt.Println(i)
		// => for c style: marks one deliberate step in the for c style example.
		// => keeps the mechanism inspectable before it is composed with another concern.
	}
	// => for c style: marks one deliberate step in the for c style example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}
