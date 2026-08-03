// => errors new: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => errors new: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
	// => errors new: marks one deliberate step in the errors new example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"errors"
	// => errors new: marks one deliberate step in the errors new example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"fmt"
	// => errors new: marks one deliberate step in the errors new example.
	// => keeps the mechanism inspectable before it is composed with another concern.
)

// => errors new: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { err := errors.New("release unavailable"); fmt.Println(err.Error()) }
