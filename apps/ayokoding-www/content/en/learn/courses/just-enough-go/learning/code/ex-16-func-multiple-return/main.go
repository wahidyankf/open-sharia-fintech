// => func multiple return: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => func multiple return: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
	// => func multiple return: marks one deliberate step in the func multiple return example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"errors"
	// => func multiple return: marks one deliberate step in the func multiple return example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"fmt"
	// => func multiple return: marks one deliberate step in the func multiple return example.
	// => keeps the mechanism inspectable before it is composed with another concern.
)

// => func multiple return: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func divide(a, b int) (int, error) {
	if b == 0 {
		return 0, errors.New("zero divisor")
	}
	return a / b, nil
}

// => func multiple return: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { q, err := divide(8, 2); fmt.Println(q, err) }
