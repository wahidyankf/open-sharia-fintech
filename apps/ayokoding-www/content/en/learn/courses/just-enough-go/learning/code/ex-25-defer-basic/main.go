// => defer basic: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => defer basic: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => defer basic: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func closeResource() { fmt.Println("cleanup") }

// => defer basic: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	// => defer basic: marks one deliberate step in the defer basic example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	defer closeResource()
	// => defer basic: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	fmt.Println("work")
	// => defer basic: marks one deliberate step in the defer basic example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}
