package main

import (
	// graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
	"fmt"
	// graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
	"sync"
	// graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
	"time"
)

// graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
func main() {
	// graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
	jobs := make(chan int, 3)
	// graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
	var group sync.WaitGroup
	// graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
	processed := 0
	// graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
	var lock sync.Mutex
	// graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
	group.Add(1)
	// graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
	go func() {
		// graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
		defer group.Done()
		// graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
		for job := range jobs {
			// graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
			time.Sleep(time.Millisecond)
			// graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
			lock.Lock()
			// graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
			processed += job
			// graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
			lock.Unlock()
		}
		// graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
	}()
	// graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
	for _, job := range []int{1, 2, 3} {
		// graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
		jobs <- job
	}
	// graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
	close(jobs)
	// graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
	group.Wait()
	// graceful shutdown: this step makes cancellation, ownership, or bounded work explicit.
	fmt.Println("gracefully-drained-total", processed)
}
