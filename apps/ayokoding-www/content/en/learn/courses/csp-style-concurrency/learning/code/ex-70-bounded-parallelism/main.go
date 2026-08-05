package main

import (
	// bounded parallelism: this step makes progress, ownership, or termination explicit.
	"fmt"
	// bounded parallelism: this step makes progress, ownership, or termination explicit.
	"sync"
	// bounded parallelism: this step makes progress, ownership, or termination explicit.
	"time"
)

// bounded parallelism: this step makes progress, ownership, or termination explicit.
func main() {
	// bounded parallelism: this step makes progress, ownership, or termination explicit.
	limit := make(chan struct{}, 2)
	// bounded parallelism: this step makes progress, ownership, or termination explicit.
	var group sync.WaitGroup
	// bounded parallelism: this step makes progress, ownership, or termination explicit.
	var lock sync.Mutex
	// bounded parallelism: this step makes progress, ownership, or termination explicit.
	active, peak := 0, 0
	// bounded parallelism: this step makes progress, ownership, or termination explicit.
	for task := 0; task < 6; task++ {
		// bounded parallelism: this step makes progress, ownership, or termination explicit.
		group.Add(1)
		// bounded parallelism: this step makes progress, ownership, or termination explicit.
		go func() {
			// bounded parallelism: this step makes progress, ownership, or termination explicit.
			defer group.Done()
			// bounded parallelism: this step makes progress, ownership, or termination explicit.
			limit <- struct{}{}
			// bounded parallelism: this step makes progress, ownership, or termination explicit.
			lock.Lock()
			// bounded parallelism: this step makes progress, ownership, or termination explicit.
			active++
			// bounded parallelism: this step makes progress, ownership, or termination explicit.
			if active > peak {
				// bounded parallelism: this step makes progress, ownership, or termination explicit.
				peak = active
			}
			// bounded parallelism: this step makes progress, ownership, or termination explicit.
			lock.Unlock()
			// bounded parallelism: this step makes progress, ownership, or termination explicit.
			time.Sleep(time.Millisecond)
			// bounded parallelism: this step makes progress, ownership, or termination explicit.
			lock.Lock()
			// bounded parallelism: this step makes progress, ownership, or termination explicit.
			active--
			// bounded parallelism: this step makes progress, ownership, or termination explicit.
			lock.Unlock()
			// bounded parallelism: this step makes progress, ownership, or termination explicit.
			<-limit
			// bounded parallelism: this step makes progress, ownership, or termination explicit.
		}()
	}
	// bounded parallelism: this step makes progress, ownership, or termination explicit.
	group.Wait()
	// bounded parallelism: this step makes progress, ownership, or termination explicit.
	fmt.Println("parallelism-limit-observed", peak)
}
