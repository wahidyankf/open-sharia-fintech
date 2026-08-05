package main

import (
	// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
	"fmt"
	// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
	"sync"
)

// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
func main() {
	// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
	jobs := make(chan int, 3)
	// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
	var group sync.WaitGroup
	// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
	var lock sync.Mutex
	// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
	processed := 0
	// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
	group.Add(1)
	// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
	go func() {
		// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
		defer group.Done()
		// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
		for job := range jobs {
			// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
			lock.Lock()
			// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
			processed += job
			// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
			lock.Unlock()
		}
		// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
	}()
	// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
	jobs <- 1
	// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
	jobs <- 2
	// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
	jobs <- 3
	// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
	close(jobs)
	// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
	group.Wait()
	// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
	lock.Lock()
	// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
	fmt.Println("clean-shutdown-total", processed)
	// clean shutdown race clean: this step makes progress, ownership, or termination explicit.
	lock.Unlock()
}
