// => select timeout: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => select timeout: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
	// => select timeout: marks one deliberate step in the select timeout example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"fmt"
	// => select timeout: marks one deliberate step in the select timeout example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"time"
	// => select timeout: marks one deliberate step in the select timeout example.
	// => keeps the mechanism inspectable before it is composed with another concern.
)

// => select timeout: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	select {
	case <-time.After(time.Millisecond):
		fmt.Println("timed out")
	}
}
