// => error value check: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => error value check: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
	// => error value check: marks one deliberate step in the error value check example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"errors"
	// => error value check: marks one deliberate step in the error value check example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"fmt"
	// => error value check: marks one deliberate step in the error value check example.
	// => keeps the mechanism inspectable before it is composed with another concern.
)

// => error value check: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func open(name string) error {
	if name == "" {
		return errors.New("name is required")
	}
	return nil
}

// => error value check: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	if err := open(""); err != nil {
		fmt.Println(err)
	}
}
