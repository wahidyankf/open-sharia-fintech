// => pointer basics: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => pointer basics: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => pointer basics: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	// => pointer basics: marks one deliberate step in the pointer basics example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	value := 7
	// => pointer basics: marks one deliberate step in the pointer basics example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	pointer := &value
	// => pointer basics: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	fmt.Println(*pointer)
	// => pointer basics: marks one deliberate step in the pointer basics example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}
