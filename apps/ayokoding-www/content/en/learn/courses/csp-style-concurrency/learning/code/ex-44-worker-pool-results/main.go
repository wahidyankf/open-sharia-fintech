package main

import (
	// worker pool results: this step makes data flow and termination explicit.
	"fmt"
	// worker pool results: this step makes data flow and termination explicit.
	"sort"
	// worker pool results: this step makes data flow and termination explicit.
	"sync"
)

// worker pool results: this step makes data flow and termination explicit.
type result struct {
	// worker pool results: this step makes data flow and termination explicit.
	job int
	// worker pool results: this step makes data flow and termination explicit.
	value int
}

// worker pool results: this step makes data flow and termination explicit.
func main() {
	// worker pool results: this step makes data flow and termination explicit.
	jobs := make(chan int)
	// worker pool results: this step makes data flow and termination explicit.
	results := make(chan result)
	// worker pool results: this step makes data flow and termination explicit.
	var group sync.WaitGroup
	// worker pool results: this step makes data flow and termination explicit.
	for range 2 {
		// worker pool results: this step makes data flow and termination explicit.
		group.Add(1)
		// worker pool results: this step makes data flow and termination explicit.
		go func() {
			// worker pool results: this step makes data flow and termination explicit.
			defer group.Done()
			// worker pool results: this step makes data flow and termination explicit.
			for job := range jobs {
				// worker pool results: this step makes data flow and termination explicit.
				results <- result{job: job, value: job * job}
			}
			// worker pool results: this step makes data flow and termination explicit.
		}()
	}
	// worker pool results: this step makes data flow and termination explicit.
	go func() {
		// worker pool results: this step makes data flow and termination explicit.
		for _, job := range []int{2, 3, 4} {
			// worker pool results: this step makes data flow and termination explicit.
			jobs <- job
		}
		// worker pool results: this step makes data flow and termination explicit.
		close(jobs)
		// worker pool results: this step makes data flow and termination explicit.
		group.Wait()
		// worker pool results: this step makes data flow and termination explicit.
		close(results)
		// worker pool results: this step makes data flow and termination explicit.
	}()
	// worker pool results: this step makes data flow and termination explicit.
	var collected []result
	// worker pool results: this step makes data flow and termination explicit.
	for item := range results {
		// worker pool results: this step makes data flow and termination explicit.
		collected = append(collected, item)
	}
	// worker pool results: this step makes data flow and termination explicit.
	sort.Slice(collected, func(i, j int) bool { return collected[i].job < collected[j].job })
	// worker pool results: this step makes data flow and termination explicit.
	fmt.Println("results", collected)
}
