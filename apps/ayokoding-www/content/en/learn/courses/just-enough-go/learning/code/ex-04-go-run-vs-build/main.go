// => go run vs build: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => go run vs build: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => go run vs build: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	// go run compiles and immediately executes a temporary program.
	// go build leaves a named executable as the release artifact.
	// => go run vs build: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	fmt.Println("compare go run . with go build -o hello")
	// => go run vs build: marks one deliberate step in the go run vs build example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}
