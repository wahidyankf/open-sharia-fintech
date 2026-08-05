// => defer lifo order: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => defer lifo order: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => defer lifo order: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	// => defer lifo order: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	defer fmt.Println("first deferred")
	// => defer lifo order: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	defer fmt.Println("second deferred")
	// => defer lifo order: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	defer fmt.Println("third deferred")
	// => defer lifo order: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	fmt.Println("body")
	// => defer lifo order: marks one deliberate step in the defer lifo order example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}
