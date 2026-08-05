// => switch statement: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => switch statement: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => switch statement: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	// => switch statement: selects one explicit branch without implicit fallthrough.
	// => keeps dispatch readable at the call site.
	switch command := "check"; command {
	// => switch statement: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	case "check":
		fmt.Println("validating")
	// => switch statement: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	case "publish":
		fmt.Println("releasing")
	// => switch statement: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	default:
		fmt.Println("unknown")
		// => switch statement: marks one deliberate step in the switch statement example.
		// => keeps the mechanism inspectable before it is composed with another concern.
	}
	// => switch statement: marks one deliberate step in the switch statement example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}
