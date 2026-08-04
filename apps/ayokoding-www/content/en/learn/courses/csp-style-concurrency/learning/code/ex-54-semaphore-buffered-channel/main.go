package main

import (
	// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
	"fmt"
	// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
	"sync"
	// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
	"time"
)

// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
func main() {
	// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
	sem := make(chan struct{}, 2)
	// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
	var group sync.WaitGroup
	// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
	var lock sync.Mutex
	// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
	active, peak := 0, 0
	// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
	for task := 1; task <= 5; task++ {
		// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
		group.Add(1)
		// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
		go func() {
			// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
			defer group.Done()
			// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
			sem <- struct{}{}
			// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
			lock.Lock()
			// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
			active++
			// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
			if active > peak {
				// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
				peak = active
			}
			// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
			lock.Unlock()
			// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
			time.Sleep(time.Millisecond)
			// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
			lock.Lock()
			// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
			active--
			// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
			lock.Unlock()
			// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
			<-sem
			// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
		}()
	}
	// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
	group.Wait()
	// semaphore buffered channel: this step makes cancellation, ownership, or bounded work explicit.
	fmt.Println("semaphore-peak", peak)
}
