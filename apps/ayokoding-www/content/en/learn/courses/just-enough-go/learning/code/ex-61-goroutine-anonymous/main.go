// => goroutine anonymous: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => goroutine anonymous: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
	// => goroutine anonymous: marks one deliberate step in the goroutine anonymous example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"fmt"
	// => goroutine anonymous: marks one deliberate step in the goroutine anonymous example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"sync"
	// => goroutine anonymous: marks one deliberate step in the goroutine anonymous example.
	// => keeps the mechanism inspectable before it is composed with another concern.
)

// => goroutine anonymous: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	var wait sync.WaitGroup
	wait.Add(1)
	go func(label string) { defer wait.Done(); fmt.Println(label) }("anonymous")
	wait.Wait()
}
