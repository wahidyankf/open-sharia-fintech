// => package and import: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => package and import: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
	// => package and import: marks one deliberate step in the package and import example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"fmt"
	// => package and import: marks one deliberate step in the package and import example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"example/package-import/greet"
	// => package and import: marks one deliberate step in the package and import example.
	// => keeps the mechanism inspectable before it is composed with another concern.
)

// => package and import: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	// Imports are explicit; an unused import is a compile error.
	// => package and import: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	fmt.Println(greet.Message("Go"))
	// => package and import: marks one deliberate step in the package and import example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}
