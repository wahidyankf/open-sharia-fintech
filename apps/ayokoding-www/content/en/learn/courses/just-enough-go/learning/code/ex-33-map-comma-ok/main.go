// => map comma ok: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => map comma ok: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => map comma ok: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	// => map comma ok: marks one deliberate step in the map comma ok example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	counts := map[string]int{"ok": 0}
	// => map comma ok: marks one deliberate step in the map comma ok example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	value, present := counts["missing"]
	// => map comma ok: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	fmt.Println(value, present)
	// => map comma ok: marks one deliberate step in the map comma ok example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}
