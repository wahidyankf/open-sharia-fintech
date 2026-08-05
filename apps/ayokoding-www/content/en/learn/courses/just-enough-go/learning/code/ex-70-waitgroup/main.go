// => waitgroup: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => waitgroup: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
	// => waitgroup: marks one deliberate step in the waitgroup example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"fmt"
	// => waitgroup: marks one deliberate step in the waitgroup example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"sync"
	// => waitgroup: marks one deliberate step in the waitgroup example.
	// => keeps the mechanism inspectable before it is composed with another concern.
)

// => waitgroup: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	var wait sync.WaitGroup
	for i := 0; i < 2; i++ {
		wait.Add(1)
		go func(value int) { defer wait.Done(); fmt.Println(value) }(i)
	}
	wait.Wait()
	fmt.Println("all done")
}
