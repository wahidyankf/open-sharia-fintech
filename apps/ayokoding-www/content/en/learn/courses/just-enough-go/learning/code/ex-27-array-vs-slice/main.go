// => array vs slice: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => array vs slice: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => array vs slice: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	// => array vs slice: marks one deliberate step in the array vs slice example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	array := [3]int{1, 2, 3}
	// => array vs slice: marks one deliberate step in the array vs slice example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	slice := []int{1, 2, 3}
	// => array vs slice: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	fmt.Println(array, slice)
	// => array vs slice: marks one deliberate step in the array vs slice example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}
