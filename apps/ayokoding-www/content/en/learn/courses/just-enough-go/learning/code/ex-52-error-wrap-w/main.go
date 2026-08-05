// => error wrap w: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => error wrap w: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
	// => error wrap w: marks one deliberate step in the error wrap w example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"errors"
	// => error wrap w: marks one deliberate step in the error wrap w example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"fmt"
	// => error wrap w: marks one deliberate step in the error wrap w example.
	// => keeps the mechanism inspectable before it is composed with another concern.
)

// => error wrap w: marks one deliberate step in the error wrap w example.
// => keeps the mechanism inspectable before it is composed with another concern.
var ErrMissing = errors.New("missing")

// => error wrap w: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func load() error { return fmt.Errorf("load config: %w", ErrMissing) }

// => error wrap w: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { err := load(); fmt.Println(errors.Unwrap(err)) }
