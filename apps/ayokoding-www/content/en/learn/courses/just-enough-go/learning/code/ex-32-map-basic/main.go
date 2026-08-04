// => map basic: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => map basic: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => map basic: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	// => map basic: marks one deliberate step in the map basic example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	counts := map[string]int{"ok": 1}
	// => map basic: marks one deliberate step in the map basic example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	counts["warn"] = 2
	// => map basic: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	fmt.Println(counts)
	// => map basic: marks one deliberate step in the map basic example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}
