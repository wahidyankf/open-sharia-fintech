package main

import (
	// worker pool bounded: this step makes data flow and termination explicit.
	"fmt"
	// worker pool bounded: this step makes data flow and termination explicit.
	"sync"
	// worker pool bounded: this step makes data flow and termination explicit.
	"time"
)

// worker pool bounded: this step makes data flow and termination explicit.
func main() {
	// worker pool bounded: this step makes data flow and termination explicit.
	const workers = 3
	// worker pool bounded: this step makes data flow and termination explicit.
	jobs := make(chan int)
	// worker pool bounded: this step makes data flow and termination explicit.
	var group sync.WaitGroup
	// worker pool bounded: this step makes data flow and termination explicit.
	var lock sync.Mutex
	// worker pool bounded: this step makes data flow and termination explicit.
	active, peak := 0, 0
	// worker pool bounded: this step makes data flow and termination explicit.
	for range workers {
		// worker pool bounded: this step makes data flow and termination explicit.
		group.Add(1)
		// worker pool bounded: this step makes data flow and termination explicit.
		go func() {
			// worker pool bounded: this step makes data flow and termination explicit.
			defer group.Done()
			// worker pool bounded: this step makes data flow and termination explicit.
			for range jobs {
				// worker pool bounded: this step makes data flow and termination explicit.
				lock.Lock()
				// worker pool bounded: this step makes data flow and termination explicit.
				active++
				// worker pool bounded: this step makes data flow and termination explicit.
				if active > peak {
					// worker pool bounded: this step makes data flow and termination explicit.
					peak = active
				}
				// worker pool bounded: this step makes data flow and termination explicit.
				lock.Unlock()
				// worker pool bounded: this step makes data flow and termination explicit.
				time.Sleep(time.Millisecond)
				// worker pool bounded: this step makes data flow and termination explicit.
				lock.Lock()
				// worker pool bounded: this step makes data flow and termination explicit.
				active--
				// worker pool bounded: this step makes data flow and termination explicit.
				lock.Unlock()
			}
			// worker pool bounded: this step makes data flow and termination explicit.
		}()
	}
	// worker pool bounded: this step makes data flow and termination explicit.
	for job := 0; job < 8; job++ {
		// worker pool bounded: this step makes data flow and termination explicit.
		jobs <- job
	}
	// worker pool bounded: this step makes data flow and termination explicit.
	close(jobs)
	// worker pool bounded: this step makes data flow and termination explicit.
	group.Wait()
	// worker pool bounded: this step makes data flow and termination explicit.
	fmt.Println("bounded-peak", peak)
}
