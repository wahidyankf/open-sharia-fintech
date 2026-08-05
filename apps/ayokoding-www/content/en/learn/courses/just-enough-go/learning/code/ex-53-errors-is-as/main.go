// => errors is as: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => errors is as: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
	// => errors is as: marks one deliberate step in the errors is as example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"errors"
	// => errors is as: marks one deliberate step in the errors is as example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"fmt"
	// => errors is as: marks one deliberate step in the errors is as example.
	// => keeps the mechanism inspectable before it is composed with another concern.
)

// => errors is as: marks one deliberate step in the errors is as example.
// => keeps the mechanism inspectable before it is composed with another concern.
var ErrMissing = errors.New("missing")

// => errors is as: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type StatusError struct{ Code int }

// => errors is as: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func (err *StatusError) Error() string { return "status error" }

// => errors is as: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	cause := &StatusError{Code: 503}
	err := fmt.Errorf("wrapped: %w", cause)
	var status *StatusError
	fmt.Println(errors.Is(fmt.Errorf("wrapped: %w", ErrMissing), ErrMissing))
	fmt.Println(errors.As(err, &status), status.Code)
}
