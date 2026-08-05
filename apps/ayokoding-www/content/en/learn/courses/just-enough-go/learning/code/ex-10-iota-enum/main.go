// => iota enum: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => iota enum: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => iota enum: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type state int

// => iota enum: marks one deliberate step in the iota enum example.
// => keeps the mechanism inspectable before it is composed with another concern.
const (
	queued state = iota
	running
	done
)

// => iota enum: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println(queued, running, done) }
