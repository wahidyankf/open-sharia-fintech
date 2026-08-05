// => for range: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => for range: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => for range: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	// => for range: uses Go’s single loop keyword for iteration.
	// => keeps the loop state and termination condition local.
	for index, value := range []string{"go", "rust"} {
		fmt.Println(index, value)
	}
	// => for range: uses Go’s single loop keyword for iteration.
	// => keeps the loop state and termination condition local.
	for key, value := range map[string]int{"ok": 1} {
		fmt.Println(key, value)
	}
	// => for range: marks one deliberate step in the for range example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}
