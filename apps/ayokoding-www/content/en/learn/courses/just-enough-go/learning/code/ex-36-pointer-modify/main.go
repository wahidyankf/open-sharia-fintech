// => pointer modify: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => pointer modify: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => pointer modify: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func increment(value *int) { *value++ }

// => pointer modify: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	// => pointer modify: marks one deliberate step in the pointer modify example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	value := 7
	// => pointer modify: marks one deliberate step in the pointer modify example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	increment(&value)
	// => pointer modify: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	fmt.Println(value)
	// => pointer modify: marks one deliberate step in the pointer modify example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}
