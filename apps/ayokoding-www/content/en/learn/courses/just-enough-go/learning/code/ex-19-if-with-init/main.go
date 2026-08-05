// => if with init: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => if with init: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
	// => if with init: marks one deliberate step in the if with init example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"errors"
	// => if with init: marks one deliberate step in the if with init example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"fmt"
	// => if with init: marks one deliberate step in the if with init example.
	// => keeps the mechanism inspectable before it is composed with another concern.
)

// => if with init: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func lookup(ok bool) (string, error) {
	// => if with init: makes the branch condition explicit rather than exceptional.
	// => keeps success and failure control flow visible.
	if !ok {
		return "", errors.New("missing")
	}
	// => if with init: returns a value through Go’s ordinary control-flow mechanism.
	// => keeps the caller responsible for the next decision.
	return "release", nil
	// => if with init: marks one deliberate step in the if with init example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}

// => if with init: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	// => if with init: makes the branch condition explicit rather than exceptional.
	// => keeps success and failure control flow visible.
	if name, err := lookup(true); err != nil {
		fmt.Println(err)
	} else {
		fmt.Println(name)
	}
	// => if with init: marks one deliberate step in the if with init example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}
