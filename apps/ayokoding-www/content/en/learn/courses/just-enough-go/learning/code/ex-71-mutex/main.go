// => mutex: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => mutex: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
	// => mutex: marks one deliberate step in the mutex example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"fmt"
	// => mutex: marks one deliberate step in the mutex example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"sync"
	// => mutex: marks one deliberate step in the mutex example.
	// => keeps the mechanism inspectable before it is composed with another concern.
)

// => mutex: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	var mutex sync.Mutex
	count := 0
	var wait sync.WaitGroup
	for i := 0; i < 2; i++ {
		wait.Add(1)
		go func() { defer wait.Done(); mutex.Lock(); defer mutex.Unlock(); count++ }()
	}
	wait.Wait()
	fmt.Println(count)
}
