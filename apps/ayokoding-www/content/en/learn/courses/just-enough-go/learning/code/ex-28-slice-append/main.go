// => slice append: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => slice append: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => slice append: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	// => slice append: marks one deliberate step in the slice append example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	values := []int{1, 2}
	// => slice append: marks one deliberate step in the slice append example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	values = append(values, 3)
	// => slice append: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	fmt.Println(values)
	// => slice append: marks one deliberate step in the slice append example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}
