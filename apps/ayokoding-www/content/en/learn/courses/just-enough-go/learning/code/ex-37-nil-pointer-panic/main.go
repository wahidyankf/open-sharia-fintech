// => nil pointer panic: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => nil pointer panic: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => nil pointer panic: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func dereference(pointer *int) (recovered any) {
	// => nil pointer panic: marks one deliberate step in the nil pointer panic example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	defer func() { recovered = recover() }()
	// => nil pointer panic: marks one deliberate step in the nil pointer panic example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	_ = *pointer
	// => nil pointer panic: returns a value through Go’s ordinary control-flow mechanism.
	// => keeps the caller responsible for the next decision.
	return nil
	// => nil pointer panic: marks one deliberate step in the nil pointer panic example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}

// => nil pointer panic: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println(dereference(nil) != nil) }
