// => switch no condition: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => switch no condition: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => switch no condition: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	// => switch no condition: marks one deliberate step in the switch no condition example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	n := -2
	// => switch no condition: selects one explicit branch without implicit fallthrough.
	// => keeps dispatch readable at the call site.
	switch {
	// => switch no condition: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	case n > 0:
		fmt.Println("positive")
	// => switch no condition: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	case n < 0:
		fmt.Println("negative")
	// => switch no condition: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	default:
		fmt.Println("zero")
		// => switch no condition: marks one deliberate step in the switch no condition example.
		// => keeps the mechanism inspectable before it is composed with another concern.
	}
	// => switch no condition: marks one deliberate step in the switch no condition example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}
