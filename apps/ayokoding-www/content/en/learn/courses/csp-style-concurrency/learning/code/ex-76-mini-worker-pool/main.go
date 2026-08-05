package main

import (
	// mini worker pool: this step makes progress, ownership, or termination explicit.
	"fmt"
	// mini worker pool: this step makes progress, ownership, or termination explicit.
	"sync"
)

// mini worker pool: this step makes progress, ownership, or termination explicit.
func main() {
	// mini worker pool: this step makes progress, ownership, or termination explicit.
	jobs := make(chan int)
	// mini worker pool: this step makes progress, ownership, or termination explicit.
	results := make(chan int)
	// mini worker pool: this step makes progress, ownership, or termination explicit.
	var group sync.WaitGroup
	// mini worker pool: this step makes progress, ownership, or termination explicit.
	for range 2 {
		// mini worker pool: this step makes progress, ownership, or termination explicit.
		group.Add(1)
		// mini worker pool: this step makes progress, ownership, or termination explicit.
		go func() {
			// mini worker pool: this step makes progress, ownership, or termination explicit.
			defer group.Done()
			// mini worker pool: this step makes progress, ownership, or termination explicit.
			for job := range jobs {
				// mini worker pool: this step makes progress, ownership, or termination explicit.
				results <- job * job
			}
			// mini worker pool: this step makes progress, ownership, or termination explicit.
		}()
	}
	// mini worker pool: this step makes progress, ownership, or termination explicit.
	go func() {
		// mini worker pool: this step makes progress, ownership, or termination explicit.
		for _, job := range []int{2, 3, 4} {
			// mini worker pool: this step makes progress, ownership, or termination explicit.
			jobs <- job
		}
		// mini worker pool: this step makes progress, ownership, or termination explicit.
		close(jobs)
		// mini worker pool: this step makes progress, ownership, or termination explicit.
		group.Wait()
		// mini worker pool: this step makes progress, ownership, or termination explicit.
		close(results)
		// mini worker pool: this step makes progress, ownership, or termination explicit.
	}()
	// mini worker pool: this step makes progress, ownership, or termination explicit.
	total := 0
	// mini worker pool: this step makes progress, ownership, or termination explicit.
	for result := range results {
		// mini worker pool: this step makes progress, ownership, or termination explicit.
		total += result
	}
	// mini worker pool: this step makes progress, ownership, or termination explicit.
	fmt.Println("worker-pool-total", total)
}
