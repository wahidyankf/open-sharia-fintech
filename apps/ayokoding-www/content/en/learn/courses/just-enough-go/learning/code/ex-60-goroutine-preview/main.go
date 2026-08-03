// => goroutine preview: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => goroutine preview: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
	// => goroutine preview: marks one deliberate step in the goroutine preview example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"fmt"
	// => goroutine preview: marks one deliberate step in the goroutine preview example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"sync"
	// => goroutine preview: marks one deliberate step in the goroutine preview example.
	// => keeps the mechanism inspectable before it is composed with another concern.
)

// => goroutine preview: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	var wait sync.WaitGroup
	wait.Add(1)
	go func() { defer wait.Done(); fmt.Println("goroutine") }()
	wait.Wait()
}
