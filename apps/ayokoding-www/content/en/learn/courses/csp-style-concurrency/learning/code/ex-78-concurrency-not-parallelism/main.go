package main

import (
	// concurrency not parallelism: this step makes progress, ownership, or termination explicit.
	"fmt"
	// concurrency not parallelism: this step makes progress, ownership, or termination explicit.
	"runtime"
	// concurrency not parallelism: this step makes progress, ownership, or termination explicit.
	"sync"
)

// concurrency not parallelism: this step makes progress, ownership, or termination explicit.
func main() {
	// concurrency not parallelism: this step makes progress, ownership, or termination explicit.
	previous := runtime.GOMAXPROCS(1)
	// concurrency not parallelism: this step makes progress, ownership, or termination explicit.
	defer runtime.GOMAXPROCS(previous)
	// concurrency not parallelism: this step makes progress, ownership, or termination explicit.
	var group sync.WaitGroup
	// concurrency not parallelism: this step makes progress, ownership, or termination explicit.
	for range 2 {
		// concurrency not parallelism: this step makes progress, ownership, or termination explicit.
		group.Add(1)
		// concurrency not parallelism: this step makes progress, ownership, or termination explicit.
		go func() {
			// concurrency not parallelism: this step makes progress, ownership, or termination explicit.
			defer group.Done()
			// concurrency not parallelism: this step makes progress, ownership, or termination explicit.
			fmt.Println("independent-concurrent-task")
			// concurrency not parallelism: this step makes progress, ownership, or termination explicit.
		}()
	}
	// concurrency not parallelism: this step makes progress, ownership, or termination explicit.
	group.Wait()
	// concurrency not parallelism: this step makes progress, ownership, or termination explicit.
	fmt.Println("gomaxprocs", runtime.GOMAXPROCS(0))
}
