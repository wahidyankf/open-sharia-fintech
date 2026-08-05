// => map delete iterate: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => map delete iterate: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => map delete iterate: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	// => map delete iterate: marks one deliberate step in the map delete iterate example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	counts := map[string]int{"ok": 1, "warn": 2}
	// => map delete iterate: marks one deliberate step in the map delete iterate example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	delete(counts, "warn")
	// => map delete iterate: uses Go’s single loop keyword for iteration.
	// => keeps the loop state and termination condition local.
	for key, value := range counts {
		fmt.Println(key, value)
	}
	// => map delete iterate: marks one deliberate step in the map delete iterate example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}
