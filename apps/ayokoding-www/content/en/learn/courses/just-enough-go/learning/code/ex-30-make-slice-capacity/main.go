// => make slice capacity: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => make slice capacity: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => make slice capacity: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	// => make slice capacity: marks one deliberate step in the make slice capacity example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	values := make([]int, 0, 10)
	// => make slice capacity: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	fmt.Println(len(values), cap(values))
	// => make slice capacity: marks one deliberate step in the make slice capacity example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}
