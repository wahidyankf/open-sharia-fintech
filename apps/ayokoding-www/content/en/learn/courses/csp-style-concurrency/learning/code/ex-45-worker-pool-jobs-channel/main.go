package main

import (
	// worker pool jobs channel: this step makes data flow and termination explicit.
	"fmt"
	// worker pool jobs channel: this step makes data flow and termination explicit.
	"sync"
)

// worker pool jobs channel: this step makes data flow and termination explicit.
func main() {
	// worker pool jobs channel: this step makes data flow and termination explicit.
	const workers = 2
	// worker pool jobs channel: this step makes data flow and termination explicit.
	jobs := make(chan int)
	// worker pool jobs channel: this step makes data flow and termination explicit.
	exited := make(chan int, workers)
	// worker pool jobs channel: this step makes data flow and termination explicit.
	var group sync.WaitGroup
	// worker pool jobs channel: this step makes data flow and termination explicit.
	for id := 1; id <= workers; id++ {
		// worker pool jobs channel: this step makes data flow and termination explicit.
		group.Add(1)
		// worker pool jobs channel: this step makes data flow and termination explicit.
		go func(workerID int) {
			// worker pool jobs channel: this step makes data flow and termination explicit.
			defer group.Done()
			// worker pool jobs channel: this step makes data flow and termination explicit.
			for job := range jobs {
				// worker pool jobs channel: this step makes data flow and termination explicit.
				fmt.Println("processed", workerID, job)
			}
			// worker pool jobs channel: this step makes data flow and termination explicit.
			exited <- workerID
			// worker pool jobs channel: this step makes data flow and termination explicit.
		}(id)
	}
	// worker pool jobs channel: this step makes data flow and termination explicit.
	jobs <- 7
	// worker pool jobs channel: this step makes data flow and termination explicit.
	jobs <- 9
	// worker pool jobs channel: this step makes data flow and termination explicit.
	close(jobs)
	// worker pool jobs channel: this step makes data flow and termination explicit.
	group.Wait()
	// worker pool jobs channel: this step makes data flow and termination explicit.
	close(exited)
	// worker pool jobs channel: this step makes data flow and termination explicit.
	count := 0
	// worker pool jobs channel: this step makes data flow and termination explicit.
	for range exited {
		// worker pool jobs channel: this step makes data flow and termination explicit.
		count++
	}
	// worker pool jobs channel: this step makes data flow and termination explicit.
	fmt.Println("workers-exited-after-jobs-close", count)
}
