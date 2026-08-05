// => slice len cap: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => slice len cap: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => slice len cap: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	// => slice len cap: marks one deliberate step in the slice len cap example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	values := make([]int, 0, 2)
	// => slice len cap: uses Go’s single loop keyword for iteration.
	// => keeps the loop state and termination condition local.
	for i := 0; i < 3; i++ {
		values = append(values, i)
		fmt.Println(len(values), cap(values))
	}
	// => slice len cap: marks one deliberate step in the slice len cap example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}
