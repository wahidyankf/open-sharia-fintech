// => go build binary: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => go build binary: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => go build binary: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	// Build with: go build -o hello main.go
	// The resulting hello executable can run without go run.
	// => go build binary: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	fmt.Println("hello binary")
	// => go build binary: marks one deliberate step in the go build binary example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}
