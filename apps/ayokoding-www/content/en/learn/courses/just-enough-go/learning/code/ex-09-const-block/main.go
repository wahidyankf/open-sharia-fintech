// => const block: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => const block: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => const block: marks one deliberate step in the const block example.
// => keeps the mechanism inspectable before it is composed with another concern.
const (
	AppName     = "ship"
	DefaultPort = 8080
)

// => const block: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println(AppName, DefaultPort) }
