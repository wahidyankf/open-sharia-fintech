package main

import (
	// fan out parallel speedup: this step makes data flow and termination explicit.
	"fmt"
	// fan out parallel speedup: this step makes data flow and termination explicit.
	"sync"
	// fan out parallel speedup: this step makes data flow and termination explicit.
	"time"
)

// fan out parallel speedup: this step makes data flow and termination explicit.
func runSequential(jobs []int) time.Duration {
	// fan out parallel speedup: this step makes data flow and termination explicit.
	started := time.Now()
	// fan out parallel speedup: this step makes data flow and termination explicit.
	for range jobs {
		// fan out parallel speedup: this step makes data flow and termination explicit.
		time.Sleep(10 * time.Millisecond)
	}
	// fan out parallel speedup: this step makes data flow and termination explicit.
	return time.Since(started)
}

// fan out parallel speedup: this step makes data flow and termination explicit.
func runParallel(jobs []int, workers int) time.Duration {
	// fan out parallel speedup: this step makes data flow and termination explicit.
	started := time.Now()
	// fan out parallel speedup: this step makes data flow and termination explicit.
	queue := make(chan int)
	// fan out parallel speedup: this step makes data flow and termination explicit.
	var group sync.WaitGroup
	// fan out parallel speedup: this step makes data flow and termination explicit.
	for range workers {
		// fan out parallel speedup: this step makes data flow and termination explicit.
		group.Add(1)
		// fan out parallel speedup: this step makes data flow and termination explicit.
		go func() {
			// fan out parallel speedup: this step makes data flow and termination explicit.
			defer group.Done()
			// fan out parallel speedup: this step makes data flow and termination explicit.
			for range queue {
				// fan out parallel speedup: this step makes data flow and termination explicit.
				time.Sleep(10 * time.Millisecond)
			}
			// fan out parallel speedup: this step makes data flow and termination explicit.
		}()
	}
	// fan out parallel speedup: this step makes data flow and termination explicit.
	for _, job := range jobs {
		// fan out parallel speedup: this step makes data flow and termination explicit.
		queue <- job
	}
	// fan out parallel speedup: this step makes data flow and termination explicit.
	close(queue)
	// fan out parallel speedup: this step makes data flow and termination explicit.
	group.Wait()
	// fan out parallel speedup: this step makes data flow and termination explicit.
	return time.Since(started)
}

// fan out parallel speedup: this step makes data flow and termination explicit.
func main() {
	// fan out parallel speedup: this step makes data flow and termination explicit.
	jobs := []int{1, 2, 3, 4}
	// fan out parallel speedup: this step makes data flow and termination explicit.
	sequential := runSequential(jobs)
	// fan out parallel speedup: this step makes data flow and termination explicit.
	parallel := runParallel(jobs, 2)
	// fan out parallel speedup: this step makes data flow and termination explicit.
	fmt.Println("parallel-faster", parallel < sequential)
}
