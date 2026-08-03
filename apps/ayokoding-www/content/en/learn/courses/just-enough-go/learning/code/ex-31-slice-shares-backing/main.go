// => slice shares backing: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => slice shares backing: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => slice shares backing: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	// => slice shares backing: marks one deliberate step in the slice shares backing example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	values := []int{1, 2, 3}
	// => slice shares backing: marks one deliberate step in the slice shares backing example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	view := values[:2]
	// => slice shares backing: marks one deliberate step in the slice shares backing example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	view[0] = 9
	// => slice shares backing: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	fmt.Println(values, view)
	// => slice shares backing: marks one deliberate step in the slice shares backing example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}
