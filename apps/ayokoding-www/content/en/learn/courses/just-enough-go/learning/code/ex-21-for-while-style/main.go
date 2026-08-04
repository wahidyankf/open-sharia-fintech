// => for while style: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => for while style: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => for while style: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	// => for while style: marks one deliberate step in the for while style example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	remaining := 3
	// => for while style: uses Go’s single loop keyword for iteration.
	// => keeps the loop state and termination condition local.
	for remaining > 0 {
		// => for while style: makes the observable result visible in stdout.
		// => gives the learner a direct value to verify.
		fmt.Println(remaining)
		// => for while style: marks one deliberate step in the for while style example.
		// => keeps the mechanism inspectable before it is composed with another concern.
		remaining--
		// => for while style: marks one deliberate step in the for while style example.
		// => keeps the mechanism inspectable before it is composed with another concern.
	}
	// => for while style: marks one deliberate step in the for while style example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}
